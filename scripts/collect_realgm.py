"""
Collect public posts from the RealGM General NBA Board into labels.csv.

Reddit blocks unauthenticated access, so posts come from RealGM's public
General NBA Board (forums.realgm.com, forum f=6; robots.txt allows crawling).

What it does, per thread:
  - fetches the most recent pages (newest posts are where current talk is)
  - keeps each post's own words: quoted replies (<blockquote>) are dropped,
    signatures live outside the post body so they never get in
  - keeps whole posts; never trims. Posts under MIN_WORDS or over MAX_CHARS
    are skipped rather than cut
  - caps posts per thread so no single thread dominates the file

Writes:
  data/realgm_raw.csv  every kept post, with thread title and permalink
  labels.csv           text, label (blank), note (blank), source

Run once:  .venv/bin/python scripts/collect_realgm.py
Labels are left blank on purpose — labelling is a separate, human step.
"""

import csv
import html
import random
import re
import time
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

BASE = "https://forums.realgm.com/boards/"
UA = "Mozilla/5.0 (takemeter coursework collector; one-off, 1 req/1.5s)"
POSTS_PER_PAGE = 25
MIN_WORDS = 5
MAX_CHARS = 1500
DELAY = 1.5
SEED = 42
SKIP_TAGS = ("blockquote", "script", "style")  # quoted replies aren't the poster's words

# (topic id, max posts to keep, pages to read from the end)
THREADS = [
    (2529186, 30, 3),   # Wednesday 10/21 NBA Game Thread
    (2528704, 30, 3),   # Tuesday 10/20 Opening Day Game Thread
    (2528590, 30, 3),   # 2026-27 MVP & All-NBA Discussion Thread
    (2464808, 25, 2),   # RGM GOAT Debate Thread (Part 3)
    (2529100, 25, 2),   # NBA Opening Week Overreactions
    (2528012, 20, 2),   # Worst players in the league
    (2529136, 20, 2),   # So SGA is a slightly more efficient Kobe correct?
    (2529208, 20, 2),   # Shams: KP on Trade Block
    (2528872, 20, 2),   # Cason Wallace extends with OKC
    (2432599, 20, 2),   # Wembanyama, I'm concerned (Part 2)
    (2528450, 15, 2),   # Luka deserves a career achievement MVP
    (2528220, 15, 2),   # Best defensive point guard of the last decade
    (2528222, 15, 2),   # Which team has the best number 2
    (2514328, 25, 2),   # 2026-27 General Discussion Thread
    (2529076, 15, 2),   # BKN Nets, what's the plan?
]

# --extra: (topic id, max posts, pages to read, pages to skip from the end)
EXTRA_THREADS = [
    (2464808, 40, 10, 2),  # RGM GOAT Debate Thread (Part 3) — older pages
    (2528590, 25, 3, 0),   # MVP & All-NBA Discussion — older pages
    (2432599, 25, 4, 2),   # Wembanyama, I'm concerned (Part 2) — older pages
    (2529136, 20, 3, 0),   # So SGA is a slightly more efficient Kobe correct?
    (2528220, 15, 3, 0),   # Best defensive point guard of the last decade
    (2528222, 15, 3, 0),   # Which team has the best number 2
]

ROOT = Path(__file__).resolve().parent.parent


def fetch(url):
    # curl rather than urllib: it uses the OS trust store, which some networks
    # need (Python's bundled certs reject their TLS chain).
    body = subprocess.run(
        ["curl", "-sSfL", "--max-time", "30", "-A", UA, url],
        check=True, capture_output=True,
    ).stdout.decode("utf-8", errors="replace")
    time.sleep(DELAY)
    return body


class PostParser(HTMLParser):
    """Pull (post_id, own_text) out of a phpBB topic page."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.posts = []
        self.current_id = None
        self.depth = 0          # div depth inside div.content
        self.skip = 0           # depth inside blockquote / cite / script
        self.buf = []
        self.title = None
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self._in_title = True
        if tag == "div" and re.fullmatch(r"p\d+", a.get("id", "") or "") and "post" in (a.get("class") or ""):
            self.current_id = a["id"][1:]
        if self.depth:
            if tag == "div":
                self.depth += 1
            if tag in SKIP_TAGS or (self.skip and tag == "div"):
                self.skip += 1
            if tag == "br" and not self.skip:
                self.buf.append("\n")
            return
        if tag == "div" and "content" in (a.get("class") or "").split():
            self.depth = 1
            self.buf = []

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if not self.depth:
            return
        if self.skip and (tag in SKIP_TAGS or tag == "div"):
            self.skip -= 1
        if tag == "div":
            self.depth -= 1
            if self.depth == 0:
                self.posts.append((self.current_id, "".join(self.buf)))
        elif tag == "p" and not self.skip:
            self.buf.append("\n")

    def handle_data(self, data):
        if self._in_title and self.title is None:
            self.title = data.strip()
        if self.depth and not self.skip:
            self.buf.append(data)


def clean(text):
    text = html.unescape(text)
    text = re.sub(r"[ \t ]+", " ", text)
    text = re.sub(r"\s*\n\s*", "\n", text).strip()
    text = re.sub(r"\n{2,}", "\n", text)
    text = text.replace("\n", " ")
    # Forum furniture, not the poster's words.
    text = re.sub(r"Sent from my .*? using RealGM( Forums)? mobile app", "", text)
    # Embedded tweets don't render without JS; only this stub survives.
    text = re.sub(r"(Spoiler: )?Read on Twitter( \?s=\d+)?", "", text)
    return re.sub(r" {2,}", " ", text).strip()


def is_furniture(text):
    """Whole 'posts' that are page widgets or moderator notes."""
    return (
        "Total votes:" in text            # poll widget on a thread's first page
        or "Strike issued" in text        # moderator notes pasted over a post
        or re.search(r"\bS\d issued\b", text) is not None
        or re.fullmatch(r"(https?://\S+\s*)+", text) is not None
    )


def last_start(page_html):
    starts = [int(s) for s in re.findall(r"start=(\d+)", page_html)]
    return max(starts) if starts else 0


def collect_thread(topic, cap, pages, skip_pages=0):
    first_url = f"{BASE}viewtopic.php?f=6&t={topic}"
    first = fetch(first_url)
    end = last_start(first)
    starts = sorted({max(0, end - POSTS_PER_PAGE * i)
                     for i in range(skip_pages, skip_pages + pages)})

    title = None
    kept = []
    for start in starts:
        page = first if start == 0 else fetch(f"{first_url}&start={start}")
        p = PostParser()
        p.feed(page)
        title = title or (p.title or "").split(" - ")[0]
        for post_id, raw in p.posts:
            text = clean(raw)
            if len(text.split()) < MIN_WORDS or len(text) > MAX_CHARS:
                continue
            if is_furniture(text):
                continue
            kept.append({
                "post_id": post_id,
                "thread": title,
                "source": f"{BASE}viewtopic.php?p={post_id}#p{post_id}",
                "text": text,
            })

    # Newest pages first is a recency bias; sample within the cap instead.
    rng = random.Random(SEED + topic)
    if len(kept) > cap:
        kept = rng.sample(kept, cap)
    return title, kept


def collect_extra():
    """
    Second pass for the thinnest label. Older pages of the stat-heavy debate
    threads, keeping only posts that contain a number — candidates for
    `analysis`, to be read and labelled by hand like everything else. Writes
    data/realgm_extra_candidates.csv and never touches labels.csv.
    """
    have = set(pd_read_texts(ROOT / "labels.csv"))
    rows = []
    for topic, cap, pages, skip in EXTRA_THREADS:
        title, kept = collect_thread(topic, 10**6, pages, skip_pages=skip)
        fresh = [r for r in kept
                 if r["text"].lower() not in have
                 and re.search(r"\d", r["text"]) and len(r["text"].split()) >= 15]
        if len(fresh) > cap:  # filter first, then cap, so the cap isn't spent on misses
            fresh = random.Random(SEED + topic).sample(fresh, cap)
        have.update(r["text"].lower() for r in fresh)
        rows.extend(fresh)
        print(f"{len(fresh):3d}  {title}")
    out = ROOT / "data" / "realgm_extra_candidates.csv"
    with out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["post_id", "thread", "source", "text"])
        w.writeheader()
        w.writerows(rows)
    print(f"\n{len(rows)} candidates -> {out.relative_to(ROOT)}")


def pd_read_texts(path):
    if not path.exists():
        return []
    with path.open(newline="") as f:
        return [r["text"].lower() for r in csv.DictReader(f)]


def labels_started():
    path = ROOT / "labels.csv"
    if not path.exists():
        return False
    with path.open(newline="") as f:
        return any(r.get("label", "").strip() for r in csv.DictReader(f))


def main():
    if "--extra" in sys.argv:
        return collect_extra()
    if labels_started():
        sys.exit("labels.csv already has labels in it — refusing to overwrite. "
                 "Use --extra to collect more candidates into a separate file.")
    rows, seen = [], set()
    for topic, cap, pages in THREADS:
        title, kept = collect_thread(topic, cap, pages)
        fresh = []
        for r in kept:
            key = r["text"].lower()
            if key in seen:
                continue
            seen.add(key)
            fresh.append(r)
        rows.extend(fresh)
        print(f"{len(fresh):3d}  {title}")

    raw_path = ROOT / "data" / "realgm_raw.csv"
    with raw_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["post_id", "thread", "source", "text"])
        w.writeheader()
        w.writerows(rows)

    # Shuffle so labelling isn't thread-by-thread (thread context would leak
    # into your judgement in a way the model never gets to see).
    random.Random(SEED).shuffle(rows)
    with (ROOT / "labels.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["text", "label", "note", "source"])
        for r in rows:
            w.writerow([r["text"], "", "", r["source"]])

    print(f"\n{len(rows)} posts -> labels.csv (labels blank) and {raw_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
