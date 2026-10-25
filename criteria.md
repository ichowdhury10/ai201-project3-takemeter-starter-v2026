# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

> **Authorship:** drafted by Claude Code (Claude Opus 5.5) at my request, under
> the course's corrected guidance that allows a model to write the criteria.
> Each one includes a check: *could someone verify it without asking me what I
> meant?* Written on October 25, 2026, before any training run. The only data
> facts used were the label counts and the test-split sizes, which are the same
> for all three seeds: 64 test posts, made up of 32 `take`, 18 `reaction` and
> 14 `analysis`.

## 1.

**Overall accuracy on the held-out test split is at least 0.65 for each of
seeds 42, 7 and 2024.**

**Why this target:** Always guessing `take` scores exactly 32/64 = 0.50 on every
seed's test split, so 0.50 is the floor here, not 0.33. 0.65 is 42 of 64: ten
more posts right than the always-`take` guesser. One post is worth 1.6 points
on a 64-post test set, so a smaller margin over 0.50 could be a friendly split
rather than a model that learned anything.

**Could someone check it without asking me?** Yes. It's `accuracy` in each
seed's entry of `results_three_seeds_before.json`. All three must be ≥ 0.65.

---

## 2.

**F1 for `analysis` is at least 0.60 for each of seeds 42, 7 and 2024.**

**Why this target:** `analysis` is the distinction this project exists for, and
it's my smallest label: 94 posts, 14 per test split. A single post changes its
F1 by roughly 0.05–0.07, so the target can't sit near the edge of what's
reachable. It's set above criterion 3's target because `analysis` has a visible
surface signal (numbers, stat abbreviations like TS%, VORP and PER). It isn't
higher because the second collection pass deliberately added `take` and
`reaction` posts that contain numbers. A model that has only learned "has a
digit → analysis" should land below 0.60.

**Could someone check it without asking me?** Yes. It's
`per_label.analysis.f1` for each seed. All three must be ≥ 0.60.

---

## 3.

**F1 for `reaction` is at least 0.50 for each of seeds 42, 7 and 2024.**

**Why this target:** `reaction` is my broadest label. It holds feelings about
games, jokes, jabs at other posters, questions, shared news and off-topic chat,
because the `banter` label was folded into it. Posts that look nothing alike
share this label, which makes it the hardest for the model to learn as one
thing, so it gets a looser target than `analysis`, with 18 test posts each seed.
0.50 is still a real bar: a model that never predicts `reaction` scores 0 here,
and one that predicts it at random at its 28% rate lands near 0.28.

**Could someone check it without asking me?** Yes. It's
`per_label.reaction.f1` for each seed. All three must be ≥ 0.50.

---

## 4.

**On each of seeds 42, 7 and 2024, accuracy on the model's most-confident third
of test posts is at least 0.15 higher than on its least-confident third.**

**Why this target:** A confidence score is only useful if it separates the
predictions you can trust from the ones a person should check. The hard cases
in this dataset (a stat used to gloat about tonight's game, one game's +/-
stretched into a trade verdict) are exactly the posts I'd want flagged as
unsure. Each third is 21 posts, so 0.15 is about 3 posts. A gap smaller than
that is within one or two posts of noise and wouldn't show the confidence means
anything.

**Could someone check it without asking me?** Yes. In each seed's `confidence`
block, `accuracy_most_confident_third − accuracy_least_confident_third` must be
≥ 0.15 for all three seeds.

---

## 5.

**When the 30 staff posts are labelled under the staff taxonomy, agreement with
the staff labels is at least 0.70 (21 of 30), as reported by `agreement.py`.**

**Why this target:** This is the only outside check on whether the boundary
rules are applied consistently. The staff taxonomy (analysis / hot_take /
reaction, with "the fact has to do work") is close to mine, so a labelling
process that applies its own rules tightly should transfer. It isn't higher than
0.70 because several staff posts were chosen to be ambiguous, and their running
forum isn't basketball. It isn't lower because anything under 21/30 would mean
my labels for my own 425 posts can't be trusted either.

**Could someone check it without asking me?** Yes. It's the agreement rate
`agreement.py` prints (and writes to `agreement_results.json`). It must be
≥ 21/30.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
