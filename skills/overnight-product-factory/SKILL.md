---
name: overnight-product-factory
description: An unattended build-and-deploy pipeline that only ships on a hard gate — a unique canary token baked into the artifact must round-trip through both the QA probe and the live health probe, and any failed deploy triggers an independently-verified rollback before the run is allowed to end.
---

# overnight-product-factory

Autonomous "build this overnight and I'll check in the morning" runs fail in one specific way more than any other: the agent *says* it shipped, but nothing live actually proves it. A build can pass its own tests, deploy cleanly, and still be serving the previous version — a caching layer didn't invalidate, a deploy pointed at the wrong target, a health check was checking the wrong URL. Self-reported "done" from the same agent that did the work is not evidence of anything. This pipeline is built around two mechanisms that close that gap: an **anti-fake-ship canary token**, and an **independently-verified rollback**.

## The pipeline shape

1. **Research** — gather context from multiple angles (market/user need, technical feasibility, risk/legal, what already exists in the repo worth reusing) before committing to a design.
2. **Plan** — turn research into a direction: UX, architecture, and an explicit safety/scope boundary.
3. **Scope-lock** — run the plan past refute-by-default reviewers (feasibility, legal/safety, scope). Anything they rule not viable as scoped moves **out** of this run into a "needs human sign-off" list — it is never auto-built or auto-shipped.
4. **Build** — implement in an isolated workspace (a fresh worktree/branch/sandbox), never the main checkout, so a bad run can't corrupt work in progress elsewhere.
5. **QA (loop until green)** — build, typecheck, unit/integration tests, and a real end-to-end probe against the running artifact. On failure, a self-repair pass fixes the root cause and re-runs, up to a capped number of rounds. The e2e probe must also read back the run's canary token (below) and return the exact value observed.
6. **Stress** — hammer the build with malformed/edge inputs, load, a simulated dependency outage, and basic abuse cases. This is part of the hard gate, not a nice-to-have — a build that passes happy-path QA but folds under a malformed request doesn't ship.
7. **Finalize** — commit every fix made during build/QA/stress. A fresh, independent agent then proves the working tree is actually clean by returning the raw output of the relevant status/diff commands (e.g. `git status --porcelain`, `git rev-parse HEAD`, `git diff --stat HEAD`) — not a claim that it's clean. Missing or inconsistent evidence fails the run closed, so the next stage reviews the committed artifact, not a dirty or stale tree.
8. **Verify** — a hostile review of the committed artifact against the original spec (does the code actually do what was asked, or does the gate just look green?), plus a completeness pass (what got skipped?).
9. **Ship (the hard gate)** — deploy only if QA, stress, the clean-tree proof, and verify are all green, and nothing was ruled not-viable in step 3. Deploy captures a rollback reference and runs a live health probe against the actual deployed target. **A run may only be reported as shipped if the live probe passes AND returns the matching canary token** — anything else is "built" or "stopped at the gate," never "shipped."

## The two mechanisms that make this trustworthy

**Anti-fake-ship canary token.** Each run generates a unique token and bakes it into the artifact at a place the artifact can report back (an endpoint, a version string, a health-check field). Both the QA e2e probe and the ship-time health probe must independently observe that exact token. A missing, empty, or stale token is treated as a failed probe — never as "probably fine." This is what catches the class of failure where the deploy step reports success but the live target didn't actually update.

**Independently-verified rollback.** The agent that performs the deploy and runs the health probe is never the same agent that gets to vouch for a rollback. If the probe fails, a separate, fresh-context agent re-runs the probe itself, executes the rollback, and returns structured evidence: the HEAD before rollback, the HEAD after (which must match the captured rollback reference), the failing probe's actual output, and the rollback command's own log. The pipeline cross-checks that evidence for internal consistency — a bare "rolled back: true" with no supporting evidence is treated as a failed rollback, and the run reports "stopped at the gate," not "shipped."

## Cleanup is unconditional and evidence-gated

Whatever workspace isolation mechanism you use (a worktree, a sandbox, a scoped lease), the cleanup phase runs on **every** exit path — success, gate-stop, or error — after the ship/rollback stage has extracted whatever it needed. Cleanup itself returns evidence (the post-cleanup state of the isolated workspace), and if that evidence shows the workspace is still present, the run's outcome is capped at "built" or "stopped at the gate" and the report flags "cleanup unverified" — a claimed cleanup with no proof isn't a cleanup.

## Honest reporting

The final report distinguishes exactly three outcomes and never blurs them:

- **SHIPPED** — live probe passed, with a matching canary token.
- **BUILT** — the quality gate passed, but nothing was deployed (or deploy was intentionally skipped).
- **STOPPED_AT_GATE** — something in QA, stress, verify, finalize, or ship failed and the run halted rather than shipping a red build.

A red gate never ships, regardless of how close it got. Watch the first several runs closely — especially any run configured to deploy straight to production — before trusting the pipeline fully unattended.

## When to use

- You want to hand a single, well-defined product idea to an agent overnight and wake up to either a shipped result or an honest "stopped here and why" — never a false "done."
- You're already comfortable with an agent building and testing unattended, but want a hard technical guarantee (not just a promise) that a deploy claim is real.
- Building on top of an existing gated-pipeline pattern but need the extra deploy-specific guarantees: a live-vs-stale distinction and a rollback that isn't self-vouched.

## How to use

**Install:** copy this folder into `~/.claude/skills/overnight-product-factory/` for personal use, or `.claude/skills/overnight-product-factory/` inside a project repo. This skill describes the pipeline shape, the gates, and the two anti-fake-ship mechanisms — wire each stage to whatever planning, sub-agent, and deploy tooling you actually use.

**Invoke:**

```
Run overnight-product-factory on this idea: "<product idea>", targeting
<repo/path>. Deploy rule: stop at a reviewed PR, don't auto-deploy to
production. Report SHIPPED / BUILT / STOPPED_AT_GATE with evidence for
whichever one it is.
```

```
Take this idea end-to-end overnight with the canary-token ship gate and
independently-verified rollback — I want to wake up to a report I can
trust without re-checking it myself.
```
