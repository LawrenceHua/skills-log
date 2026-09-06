---
name: scoping-cutting
description: An MVP-scoping framework combining Shape Up appetite-setting, "cut the list in half twice," an end-to-end "scooter not axle" value test, Wizard-of-Oz testing before automating, and an upfront kill-on-time commitment — for defining scope, fighting scope creep, and shipping faster.
---

# scoping-cutting

Most scope creep isn't a discipline failure, it's a missing default: without an explicit scoping method, a feature naturally expands to fill however much time is available, because "smaller" was never actually forced. This combines several well-known scoping techniques into one procedure, credited to their originators rather than presented as a single invented method.

## The iron law

**Cut the list in half. Then cut it in half again. Then build it.** (37signals, *Getting Real* — "Half, Not Half-Assed") — teams consistently overestimate what "minimum" means; the second cut is the one that actually gets you to minimum.

## Procedure

**1. Name the single hypothesis.** What is this version actually trying to validate? If you find yourself listing more than one hypothesis, you have more than one scope — split it into separate ships rather than bundling them.

**2. Set appetite, don't estimate.** (Ryan Singer, *Shape Up*) Ask "what's the maximum time we're willing to spend before shipping something," not "how long will this take." Then design a version of the solution that fits inside that budget. Vary the scope to fit the time, never the deadline to fit the scope.

**3. Cut the list.** Write out everything that feels like it "must" be in this version. Cut it in half. Cut what's left in half again. That's what you build.

**4. Build the scooter, not the axle.** (Henrik Kniberg's "Making Sense of MVP" illustration) When building toward a car, don't ship just an axle — an incomplete piece of the bigger thing that delivers no value on its own. Ship a scooter: a smaller but *complete*, end-to-end version of the value proposition, on the same skateboard→scooter→bike→car path toward the eventual car. Test every proposed cut against: "if we shipped exactly this right now, does it deliver complete value end-to-end, or is it half of something bigger?" If it's half of something bigger, cut differently until you find the scooter.

**5. Test manually before automating.** (Wizard-of-Oz testing) Ask whether the thing can be validated by a human doing it manually for the first handful of cases before any automation gets built. If a manual test would take a day and the automated version would take a week, test manually first — you'll often learn the automation isn't worth building at all.

**6. Commit to kill-on-time, upfront.** (Jason Fried) Before starting, commit explicitly: "if this isn't done by [appetite end date], we kill it" — not extend it. Make this a one-line commitment stated before the work starts, not a debate held once the deadline arrives. Killing a project on schedule is healthier than a project that never ends.

**7. Build the pivot option in from the start.** (Paige Costello) Explicitly note on the roadmap that this item might be cut or pivoted. Once something is on a roadmap without that caveat, it starts to feel mandatory by default — stating the pivot option upfront counters sunk-cost pressure later.

## Anti-patterns this catches

- **Estimating instead of time-boxing** — asking "how long will this take" instead of "what can we ship in this fixed budget."
- **Building the axle** — shipping an incomplete slice of a bigger feature instead of a smaller, complete one.
- **Never killing anything** — extending deadlines indefinitely instead of cutting scope or actually stopping.
- **Skipping the manual test** — defaulting straight to building automation when a day of manual testing would answer the question faster and cheaper.
- **Over-engineering the MVP** — building more than the single hypothesis needs before you've validated it.

## Output contract

A completed scoping pass should produce, explicitly:
- The single hypothesis being validated
- The appetite (a time budget, not an estimate)
- The cut list at each stage (original → first cut → second cut → final)
- The scooter check, answered yes or no: does this deliver complete value end-to-end?
- The Wizard-of-Oz check, answered yes or no: can this be tested manually first?
- The kill-on-time commitment, with a concrete date
- The pivot-option declaration

## Example

A team wants "auto-suggest labels based on past corrections."
- **Hypothesis:** users accept more suggestions when they match the user's own past correction patterns.
- **Appetite:** one day.
- **First cut:** a full pattern-matching engine, a UI for reviewing suggestions, and a reporting dashboard.
- **Second cut:** the top-3 patterns per user, surfaced inline, no dashboard.
- **Scooter version:** top-3 patterns hardcoded from existing data, shown inline with accept/reject — no reporting, no configuration UI. Delivers the full value proposition end-to-end at minimum scope.
- **Wizard-of-Oz alternative:** manually pre-load a handful of users' past patterns into the suggestion list and measure the correction-rate change before building the matching engine at all.
- **Kill-on-time:** if not shipped by end of day, kill it — not extend to tomorrow.

## When to use

- Defining MVP scope for a new feature or project.
- Scope creep is happening mid-build and the feature keeps growing.
- You want to ship faster and need a forcing function, not just intent.
- Making an explicit build-vs-cut tradeoff decision.

Not for a straightforward bug fix (nothing to scope), and not a substitute for validating the underlying problem exists before scoping a solution to it.

## How to use

**Install:** copy this folder into `~/.claude/skills/scoping-cutting/` for personal use, or `.claude/skills/scoping-cutting/` inside a project repo shared with a team.

**Invoke:**

```
Use scoping-cutting on this feature idea before we start building — give me
the hypothesis, appetite, cut list, and the scooter check.
```

```
This build has ballooned past its original scope. Run scoping-cutting to
find the scooter version we should actually ship this week.
```
