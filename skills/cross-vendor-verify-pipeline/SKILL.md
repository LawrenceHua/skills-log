---
name: cross-vendor-verify-pipeline
description: A three-role coding pipeline — one model plans, a second (different-vendor) model executes, and a third independently redoes the build/test run itself rather than reading the executor's diff — so "it passed" is never taken on the executor's word alone.
---

# cross-vendor-verify-pipeline

Asking a model to verify its own work has an obvious blind spot: whatever it silently skipped or misunderstood while executing, it's likely to miss the same way while checking. And a *second* model that only reads the first model's diff and self-report inherits a softer version of the same problem — it's grading a story about the work, not the work itself. The fix is to split planning, execution, and verification across genuinely separate roles, and to make verification mean *redoing*, not *reading*.

## The method

1. **Interrogate before planning.** Batch every clarifying question about scope, constraints, and success criteria into one round, and get them answered before any planning work starts — resolving ambiguity mid-execution is more expensive than resolving it up front.
2. **Plan with one model.** Have a single model produce a concrete, written plan file: the steps, the files touched, and the explicit verification criteria — detailed enough that a different model could execute from it without needing the planner's live context.
3. **Execute with a second, different-vendor model.** Hand the plan to a separate model, ideally from a different vendor or model family than the planner, so a systematic blind spot in one vendor's training doesn't quietly compound across both planning and execution.
4. **Verify by redoing, not reading.** Have a third, independent agent actually re-run the build and the test suite itself from a clean checkout, rather than reading the executor's diff or trusting its self-reported "tests pass." A model grading its own transcript — or another model's transcript — will tend to miss exactly what that transcript quietly skipped.
5. **Add a dedicated test-integrity check.** Before trusting a green run, confirm the passing tests actually exercise the changed behavior — check that a test was genuinely added or modified for new behavior, and that a previously-failing test now fails for the right reason and passes for the right reason. A suite that passes because nothing new was actually tested is not evidence of anything.
6. **Gate the final ship on the independent re-run passing** — not on the executor's report of what it did.

## When to use

- Any coding task important enough to want a genuine second opinion on execution quality, especially work you'll hand off and not watch step-by-step.
- Delegating a substantial change to an agent you won't personally review line-by-line, where "it says it passed" isn't sufficient evidence to ship.
- Designing a multi-model pipeline and deciding where the actual trust boundary should sit — this method puts it at "was the result independently reproduced," not "did the executor report success."

## How to use

**Install:** copy this folder into `~/.claude/skills/cross-vendor-verify-pipeline/` for personal use, or `.claude/skills/cross-vendor-verify-pipeline/` inside a project repo.

**Invoke:**

```
Use cross-vendor-verify-pipeline for this refactor — plan it with one model, execute
with a different one, and have a third independently rerun the build and tests before
we call it done.
```

```
This PR only got checked by reading the diff — apply the verification step from
cross-vendor-verify-pipeline: have a fresh agent rerun the tests from a clean checkout.
```
