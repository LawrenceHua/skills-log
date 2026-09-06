---
name: cloud-delivery
description: Treat "delivered" as an exact-commit-SHA state machine — bind a pushed branch to a verified CI pass and a matching preview deployment at that same SHA, and refuse to call anything shipped from a stale, mismatched, or inferred signal.
---

# cloud-delivery

"CI is green" and "the preview looks right" are both easy to say from stale information — a CI run from three commits ago, or a preview deployment that's actually serving an older SHA because the new build hasn't finished rolling out yet. The fix is to stop treating delivery as a vibe and start treating it as a state machine keyed on one thing: the exact commit SHA.

## The method

**1. Bind every check to one SHA, not "the branch."** A CI status and a preview deployment are only evidence of anything if they're both for the *exact* commit you just pushed — not the branch's current HEAD (which may have moved), not "whatever's currently deployed" (which may be stale), not an earlier run from before your latest push.

**2. Refuse to publish from a stale or diverged base.** Before pushing, confirm the target base (e.g. `main`) hasn't moved past what your branch was built against. A candidate that doesn't contain the exact current base is refused outright, not rebased silently and re-tried — silent rebasing hides exactly the kind of drift this method exists to catch.

**3. State machine, not a single boolean.** Track delivery through explicit states: local checks passed → pushed → remote PR/check opened → CI passed at that SHA → preview deployment ready → preview's reported source SHA matches the bound head SHA. Each state requires the previous one to still be true, checked fresh — not assumed from an earlier state.

**4. A preview success never substitutes for a CI success, or vice versa.** They test different things (build/test correctness vs. actual runtime behavior) and can diverge — a deployment platform can report "ready" for a build that used a cached, stale artifact. Verify both, independently, both bound to the same SHA.

**5. Three outcomes, not two.** Don't collapse the result to pass/fail:
   - **VERIFIED** — the exact head/base binding, every required check, and the SHA-matched preview are all current in one observation window.
   - **BLOCKED** — something is definitively wrong: a dirty tree, a candidate that doesn't contain the current base, SHA drift, a failed check, a missing required check.
   - **INCONCLUSIVE** — the provider was unreachable, a response couldn't be parsed, or the check simply hasn't finished within a bounded wait. Never round this up to VERIFIED just because nothing failed outright.

**6. Draft, don't merge.** This state machine answers "is this candidate provably good," not "should it go live." Stop at a verified draft PR and a verified preview; treat merge, production promotion, and any provider-setting change as a separate, explicitly authorized step.

## Reference implementation sketch

A minimal version needs a small config file per repo declaring what "delivered" means for it (required check names, whether a preview is required, preflight commands to run locally first) and a controller script that:

1. Runs local preflight (build, test) and records the exact head SHA it validated.
2. Pushes exactly `<sha>:refs/heads/<branch>`, reads the ref back, opens or updates one draft PR, and records its head SHA.
3. Polls the CI provider's check-runs API for that exact SHA until every required check is present and either passed or explicitly failed (never treats "still pending" as pass).
4. Polls the deployment provider for a ready preview whose reported source commit matches the same SHA.
5. Writes an append-only receipt recording each state transition — timestamps and the exact SHA at each step, not raw log output or credentials.

Keep this read-only with respect to production: authenticate using your existing CLI/tool sessions (a source-control CLI login, a deploy-platform CLI login) rather than embedding tokens in config or receipts.

## When to use

- Publishing a branch and wanting a trustworthy, provable answer to "is this candidate actually good," not just "did I run some commands."
- Diagnosing an unreliable push/CI/deploy pipeline where "it worked on my machine" and "the dashboard looks green" keep disagreeing with what actually shipped.
- Setting up a new repository for repeatable, auditable delivery instead of ad hoc "push and check manually."

## How to use

**Install:** copy this folder into `~/.claude/skills/cloud-delivery/` for personal use, or `.claude/skills/cloud-delivery/` inside a project repo. Adapt the reference controller to your actual CI and deployment providers' APIs.

**Invoke:**

```
Push this branch using cloud-delivery — don't tell me it's ready until CI
and the preview both verify at the exact SHA I pushed.
```

```
Our last three "green" deploys were actually stale. Set up cloud-delivery's
SHA-binding state machine for this repo so that can't happen silently again.
```
