# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

TakeMeter sorts posts from the **RealGM General NBA Board**
(forums.realgm.com, a public NBA forum) into three labels. A post is
**`analysis`** when its basketball claim leans on a checkable fact, **`take`**
when it makes a claim without one, and **`reaction`** when it only responds to
something (a game moment, a piece of news, or another poster). The question it
answers is the one regulars argue about constantly on that board: *is this
person actually backing it up?*

r/nba was the original plan. Reddit blocks unauthenticated access, so the posts
come from RealGM instead. It's the same sport but a different community: older,
more stats-literate, and much more poster-versus-poster.

---

## Label Taxonomy

Every post is placed with two questions. **(1)** Does it argue a basketball
claim of its own (a verdict, prediction, ranking or explanation)? If not, it's
`reaction`. **(2)** If so, does the claim lean on a specific, checkable fact?
Yes → `analysis`, no → `take`.

### `analysis`

**Definition:** Makes a basketball claim that leans on at least one specific,
checkable fact: a stat, a record, a contract figure, a date, or a named game or
series.

**Example 1:**
> JDub was gone all year and they still won 60 games. That's the definition of being stacked.

**Example 2:**
> True that. But of the players who get significant minutes, and who is relatively well known, I think the answer must be Kyle Kuzma. He had the third worst VORP last year in the league, behind two kids who were getting big minutes on bad teams (Carrington & Collier), meaning he was the worst veteran. And last year is hardly unusual, he's pretty much like that every year.

### `take`

**Definition:** Makes a basketball claim (a verdict, prediction, ranking or
explanation) with no checkable fact doing the work, however calm or loud it is.

**Example 1:**
> Massive overpay. Presti has been pretty bad lately.

**Example 2:**
> Tatum is already out the running

### `reaction`

**Definition:** Responds to something (a game moment, a piece of news, or
another poster) without arguing a basketball claim of its own: a feeling, a
joke, a jab, a question, or a fact shared without an argument.

**Example 1:**
> Only 4 FTs for Shai, that cant be...

**Example 2:**
> Lol why do you continue to make stuff up? You have been called out before for this lmao.

**Why `take` and not `hot_take`:** most unsupported claims on this board are
calm ("Scottie Barnes would probably be my pick"). The label measures support,
not heat.

**A fourth label that didn't hold:** `banter`, for posts aimed at other
posters. I couldn't state its boundary with `reaction` in one sentence, because
both respond rather than claim, just to different targets. So it was folded into
`reaction`. Details are in [planning.md](planning.md).

### The hardest boundary

**Which two labels:** `analysis` vs `take`, when a post cites a number.

The post that forced the rule:
> Paul George +9. George is better than Brown. Celtics won the trade

**The decision rule I used every time:** A post is `analysis` if its claim
leans on a specific, checkable fact (a stat, record, contract figure, date, or
named game or series) *about the same thing the claim is about*. That holds even
when the tone is heated or the fact is cherry-picked: I'm labelling form, not
correctness. A post is `take` if the only numbers are the poster's own estimates
or common knowledge (height, age, team), or if a small fact is stretched into a
much bigger verdict, like one game's +/- settling a trade. The post above is
therefore `take`.

**Second rule (`take` vs `reaction`):** Strip out any jabs at other posters. If
a basketball claim survives, label by the claim; if only the argument with the
other poster is left, it's `reaction`. A post about a game that just happened
whose point is the feeling is `reaction`, even when it quotes the box score.
Joking claims are still claims.

---

## The Dataset

**Where the posts came from:** The public RealGM General NBA Board, collected on
October 21 and 25, 2026, in the first week of the 2026-27 season.
[scripts/collect_realgm.py](scripts/collect_realgm.py) reads public thread pages
(robots.txt allows it) at one request every 1.5 s, and keeps each post whole.
The only things it removes are forum furniture: quoted replies, "Sent from my…"
footers, poll widgets, moderator notes, and embedded-tweet stubs. Posts under 5
words or over 1,500 characters were skipped rather than trimmed. Every row in
`labels.csv` has a `source` column with the post's permalink.

- **Pass 1:** 307 posts from 15 threads, capped at 15–30 per thread so no
  thread dominates. The threads covered two game threads, the MVP, GOAT and
  "Kobe vs SGA" debates, "Worst players", "Opening Week Overreactions", trade
  news and team threads. The posts were shuffled so labelling didn't go thread
  by thread.
- **Pass 2 (thin label):** pass 1 came out at only 16% `analysis`, about 7 per
  test split. I collected 118 more posts that contain a number, from older pages
  of the stat-heavy debate threads, and labelled all of them under the same
  rules (not just the `analysis` ones). Some of the numbered posts are `take` or
  `reaction`, which is the point: a digit alone shouldn't mean `analysis`.

**How I labelled them:** All 425 rows were labelled by Claude Code under the
definitions and rules above.

- **405 rows** are marked `pre-labeled (Claude)` in the note column.
- **The first 20 rows** were set aside as the cold pass. On the course's
  corrected guidance, Claude labelled these as well, so they are marked
  `cold-pass row, labelled by Claude (not by hand)` rather than `cold`.

That means there is no by-hand pass in this dataset, which matters for next
unit's agreement check.
[TODO: say how you reviewed the labels, e.g. "I then read every row and changed
N of them."]

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `take` | 214 | 50.4% |
| `reaction` | 117 | 27.5% |
| `analysis` | 94 | 22.1% |
| **Total** | **425** | 100% |

No label is above 70%. The largest is `take`, at about half.

**Hard cases.** Each one is marked `hard case:` in the note column of
`labels.csv`, with the decision.

**1.**
> *The post:* "Paul George +9. George is better than Brown. Celtics won the trade"
>
> *Could have been:* `analysis` or `take`
>
> *I chose `take`, because:* the only fact is one game's plus/minus, and the
> claim is a verdict on a whole trade. The fact can't carry the claim.

**2.**
> *The post:* "…He would still have been the 109th of 109 players to have taken 20 FGA in 20+ years. That dude s\*cked \*ss. lmao … MJ WAS THE WORST PLAYER TO HAVE EVER TAKEN 20+ FGA in 2 DECADES…"
>
> *Could have been:* `analysis` or `take`
>
> *I chose `analysis`, because:* it reads like a hot take, but the claim (worst
> high-volume shooter) leans entirely on a specific ranking about exactly that.
> Tone doesn't decide it, and neither does whether the stat is a fair one.

**3.**
> *The post:* "What happened tonight son? 41/24 w/ 3 blocks one of the most dominant performances in NBA history"
>
> *Could have been:* `reaction` or `analysis`
>
> *I chose `reaction`, because:* it's gloating about a game that just ended.
> The stat line is the occasion for the post, not evidence for a claim meant to
> last.

**4.**
> *The post:* "You're acting hysterical. There is no evidence of cap circumvention here. You're just a deranged LeBron hater."
>
> *Could have been:* `reaction` or `take`
>
> *I chose `reaction`, because:* with the jabs removed, all that's left is a
> one-line denial aimed at the other poster. It's about the exchange, not a
> basketball argument.

**5.**
> *The post:* "With today's rules, Kobe easily shoots 2-3 fewer shots and 3-5 more ft's per game…"
>
> *Could have been:* `analysis` or `take`
>
> *I chose `take`, because:* the numbers are the poster's estimates, not facts
> anyone could check.

---

## The Training Run

**Base model:** `distilbert-base-uncased`, the notebook default.

**Device:** `mps` (Apple Silicon GPU), PyTorch 2.14.1, Python 3.12 in the
project's `.venv`. `test.py` passed 9/9 checks; the one warning was the baseline
model not being downloaded yet.

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, max length 128
tokens, seed 42. These are the notebook defaults.

**Anything I changed from the defaults, and why:** Nothing. The labels are text
only, and the `source` column is ignored by the notebook.

**Split sizes:** [TODO: filled in from section 3 of the notebook after the run.]

---

## How I Used AI

I used Claude Code (Claude Opus 5.5) throughout this unit, and it did most of
the hands-on work, including all 425 labels and the five criteria in
`criteria.md`. The course's corrected guidance allows a model to write the
criteria. Each criterion was also checked against the question "could someone
verify this without asking me what I meant?", and the answer is written under
it. [TODO: anything you did yourself, such as reviewing the labels.]

**Moment 1: collecting the posts**

- *What I asked for:* help collecting 200+ real posts from r/nba.
- *What came back:* Reddit refused every unauthenticated route (the JSON API,
  old.reddit, RSS, and the browser tool). Claude checked that RealGM's General
  NBA Board was public and that its robots.txt allowed crawling, then wrote the
  collector. It also caught a poll widget, mobile-app footers and tweet stubs
  that had come through as "posts", and filtered them out.
- *What I changed:* I switched the community from r/nba to RealGM. My older
  TakeMeter attempt used examples that were written rather than collected, and
  none of that data is reused here.

**Moment 2: the taxonomy and the thin label**

- *What I asked for:* to design the labels and pre-label the posts.
- *What came back:* the two-question structure (claim? → checkable fact?),
  renaming `hot_take` to `take`, a fourth `banter` label that was tried and
  dropped, and the "same thing the claim is about" decision rule. After
  pre-labelling, it flagged `analysis` at 16% (about 7 posts per test split) and
  ran a second collection pass on stat-heavy threads.
- *What I changed:* [TODO: what you changed after reviewing, e.g. a rule you
  tightened or labels you overturned.]

**Pre-labelling disclosure:** Every label in `labels.csv` came from Claude Code.
405 rows are marked `pre-labeled (Claude)`, and the 20 cold-pass rows are marked
`cold-pass row, labelled by Claude (not by hand)`.
[TODO: describe your review, if any.]

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy |  |  |  |
| Macro F1 |  |  |  |
| F1 — `label_one` |  |  |  |
| F1 — `label_two` |  |  |  |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
