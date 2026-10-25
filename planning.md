# TakeMeter — planning notes

## Milestone 1 — Community

**RealGM General NBA Board** — <https://forums.realgm.com/boards/viewforum.php?f=6>

A public NBA discussion forum (no login needed to read). It has the range the
project needs: nightly game threads, long-running debate threads (GOAT, MVP,
"Kobe vs SGA"), trade-news threads, and short opinion threads ("Worst players
in the league", "Opening Week Overreactions").

r/nba was the first choice. Reddit now blocks unauthenticated access — scripts
get a 403 or a redirect to a login page, and it was blocked in the browser tool
too — so RealGM replaced it. Same sport, a different community: older, more
argumentative, more stats-literate than r/nba, and its posters argue with each
other directly far more often.

### Candidate distinctions seen in the posts (before designing labels)

1. **Some posts cite a number or a named game, series or record; most don't.**
   "Kuzma had the third worst VORP last year" versus "Presti has been pretty bad
   lately." The number is usually what the whole post leans on.
2. **A lot of posts are aimed at another poster, not at basketball.** "Lol why
   do you continue to make stuff up?", "Again you prove my point." The GOAT
   thread especially is half argument-about-the-argument. Moderators issue
   strikes for it.
3. **Game-thread posts react to the moment.** "Only 4 FTs for Shai, that cant
   be...", "Looking forward to both ESPN games tonight!" They're about how the
   poster feels about tonight, not a claim meant to last.
4. **Prediction posts are everywhere and carry no reasoning.** Lists of picks
   ("Heat beat Wolves, Lakers beat Warriors…"), score predictions, All-NBA
   teams. Confident, but unargued.
5. **Long, careful posts with no facts in them.** Reasoned trade or rotation
   arguments ("sometimes you just have to pay guys…") that read as serious but
   cite nothing checkable. These turned out to be the hardest to place.

---

## Milestone 2 — Labels

Three labels, chosen so every post can be placed with two questions:

1. Does the post argue a basketball claim of its own (a verdict, prediction,
   ranking or explanation about players, teams, games or the league)?
   **No → `reaction`.**
2. Does that claim lean on a specific, checkable fact?
   **Yes → `analysis`. No → `take`.**

| Label | Definition |
|---|---|
| `analysis` | Makes a basketball claim that leans on at least one specific, checkable fact — a stat, a record, a contract figure, a date, or a named game or series. |
| `take` | Makes a basketball claim — a verdict, prediction, ranking or explanation — with no checkable fact doing the work, however calm or loud it is. |
| `reaction` | Responds to something — a game moment, a piece of news, or another poster — without arguing a basketball claim of its own: a feeling, a joke, a jab, a question, or a fact shared without an argument. |

`take` replaced `hot_take`. On this board most unsupported claims are calm
("I think Scottie Barnes would probably be my pick"), and calling them *hot*
made me hesitate on every mild one. What the label measures is support, not
heat.

### The fourth label that didn't hold: `banter`

Distinction 2 suggested a fourth label for poster-versus-poster posts. It didn't
survive contact with the data. I couldn't state the line between `banter` and
`reaction` in a sentence — "Lol why do you continue to make stuff up?" and
"Sacramento never ceases to amaze" do the same job (responding, not claiming),
just to different targets. Folding it into `reaction` made the first question
above clean. The cost is that `reaction` is the broadest label.

### Hardest boundary: `analysis` vs `take`

The borderline post:

> Paul George +9. George is better than Brown. Celtics won the trade

It cites a checkable number and makes a claim. Is that analysis?

**Decision rule.** It's `analysis` if the claim leans on a specific, checkable
fact (a stat, record, contract figure, date, or named game or series) **about
the same thing the claim is about** — even if the tone is heated or the fact is
cherry-picked. I'm labelling form, not correctness. It's `take` when:

- the only numbers are the poster's own estimates ("2-3 fewer shots, 3-5 more
  FTs") or common knowledge (a player's height, age or team), or
- a small fact is stretched into a much bigger verdict — one game's +/- used to
  settle a trade or a career.

So the PG post is `take`: one game's +9 can't carry "won the trade".

### Second rule: `take` vs `reaction`

- Strip out any jabs at other posters. If a basketball claim survives, label by
  the claim. If what's left is only about the exchange (who's lying, who's
  trolling), it's `reaction`.
- A post about a game that just happened whose point is the feeling — gloating,
  shock, celebration — is `reaction`, even if it quotes the box score
  ("What happened tonight son? 41/24 w/ 3 blocks").
- Joking claims are still claims. "Paul George number 1 in the MVP race" in the
  overreactions thread is `take`.
