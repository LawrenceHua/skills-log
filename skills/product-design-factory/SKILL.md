---
name: product-design-factory
description: A design pipeline that grounds a product surface in one job statement, generates exactly three comparable design directions before picking one, compiles a token/component contract, builds one real vertical slice, and requires an independent hostile review before calling it done.
---

# product-design-factory

Design work drifts when there's no forcing function for comparison or for critique. Left unstructured, it tends toward "the first idea that looked okay," reviewed only by the person who built it. This pipeline forces both: a real choice between distinct directions before committing, and a reviewer with no investment in the outcome before calling it finished.

## The method

1. **Ground the surface in one job statement.** Write a single sentence describing the job the surface does for the user, plus the states it must handle — empty, loading, error, success. Any proposed element that doesn't serve that sentence is scope to cut, not a nice-to-have to keep.
2. **Generate exactly three comparable directions.** Produce three genuinely different visual or interaction directions for the same job — not three trivial color variants of the same layout. Three is the target: fewer collapses into "there was no real choice," more dilutes attention without adding signal.
3. **Compile a token and component contract before building.** Lock down the shared tokens (spacing scale, color roles, type scale) and component contracts (props, states) that the chosen direction will use. Deciding this up front keeps the eventual build internally consistent instead of improvised screen-by-screen.
4. **Build one real vertical slice.** Implement one working end-to-end path through the surface — not a set of disconnected static mockups. A vertical slice surfaces integration problems (state transitions, real data shapes, actual loading behavior) that flat designs hide entirely.
5. **Run a fixed battery of deterministic quality gates on the slice.** Use the same checklist every time — contrast ratios, responsive breakpoints at defined widths, correct rendering of empty/error states, keyboard and focus behavior — rather than an ad hoc pass that varies by who's reviewing.
6. **Require an independent hostile review before promotion.** Have a reviewer with no investment in this specific design — a different person, or a fresh reviewing context with no memory of building it — actively try to find what's wrong, not confirm it looks fine. Don't call the design done until that review passes; the person or context that built it is structurally unable to catch its own blind spots.

## When to use

- Designing or redesigning a product surface where you want a genuine comparison between options rather than shipping the first workable idea.
- Any design review process that currently has no forcing function for either comparison (multiple real directions) or critique (an independent reviewer).
- A surface important enough to warrant a real quality bar — production UI, a customer-facing flow, anything you'd regret having to redo.

## How to use

**Install:** copy this folder into `~/.claude/skills/product-design-factory/` for personal use, or `.claude/skills/product-design-factory/` inside a project repo.

**Invoke:**

```
Run this feature through product-design-factory — start with the one-sentence job
statement, then give me three genuinely different directions before we build anything.
```

```
We already picked a direction and built it — apply the independent hostile review
step from product-design-factory before we call it done.
```
