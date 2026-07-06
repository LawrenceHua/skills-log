---
name: autobuild-loop
description: An end-to-end, self-verifying build pipeline — plan, then a multi-role expert swarm, then docs, then a QA gate, then a code-quality gate, then a smoke/canary check, then a summary — where every stage is gated behind the previous stage's verification artifact, so nothing downstream starts on an unproven upstream result. Use for a defined-end-state build you want to walk away from and trust came back correct.
allowed-tools: [Bash, Read, Task]
---

# autobuild-loop

A build orchestrator that chains: **deep planning → a multi-role expert
swarm → documentation → a QA gate → a code-quality gate → a smoke/canary
check → a final summary.** The property that makes this trustworthy (and
different from just "running a bunch of steps") is that **every stage is
gated**: a stage may not start until the prior stage produced a
verification artifact with a passing verdict. Downstream stages read that
artifact, never a narrative "looks good" from the previous stage.

## Kill switch (read first)

Before anything else, agree on a simple stop mechanism — e.g. a flag file
in your project or state directory (`touch .autobuild/EMERGENCY_STOP`) that
every stage checks for and honors immediately. If a long-running pipeline
needs to be halted, creating that flag and ending the session is the
reliable lever — don't rely on killing processes out from under an agent
mid-write.

## When to use

- A defined-end-state build whose "done" you can verify by an observable
  output (tests pass, a build succeeds, a specific endpoint responds
  correctly).
- You want to hand off a multi-hour build and come back to a trustworthy
  report, not a pile of unverified claims.

**Skip it for:** a small, low-risk change you'd just make directly — this
pipeline's overhead (multiple sub-agents, multiple gates) is deliberate and
only worth it for real builds. If you can't write down the success probe in
advance, that's a sign to scope the task down before invoking this.

## Preflight (assert before stage 1; refuse to start on failure)

1. The kill-switch flag is absent.
2. Whatever "elevated permission / autonomous mode" your session is running
   under is still fresh (not stale/expired) — a long unattended run should
   finish or checkpoint well before that mode would silently lapse.
3. Your safety/deny-list configuration is intact (not accidentally emptied).
4. Acquire a simple run lock (a lock file with a live PID) so two pipelines
   can't corrupt the same shared state concurrently.

## Sub-agent safety

- Every research/swarm sub-agent runs **read-only**. Only the orchestrating
  session applies edits, and only within the target repo plus its own
  run/state directory.
- Confine all pipeline writes to the target repo and a dedicated run
  directory (e.g. `.autobuild/<run_id>/`) — nothing outside that scope.
- Cap the swarm's fan-out depth and worker count explicitly (e.g. depth
  ≤ 2, max 4 parallel workers, a hard per-agent timeout) — an uncapped
  fanout can runaway-spawn.

## Run-state contract (so it can resume across turns/sessions)

Keep a tiny state file (or a few marker files) per run that records which
stage last completed. On re-entry, check what's already marked done and
skip straight to the next unfinished stage — never re-run a stage that
already passed its gate.

## The 7 stages and their exit evidence

| # | Stage | What it reuses | Exit evidence |
|---|---|---|---|
| 1 | **Plan** | your deep-planning process/skill | a plan file exists and states an observable success criterion |
| 2 | **Swarm** | a multi-role expert fanout (see the companion `expert-fanout` skill) | each role's report exists, plus a synthesis |
| 3 | **Docs** | your documentation-writing process | the doc file exists |
| 4 | **QA** | a real, observed probe — tests, a build, an actual request against the running thing | probe passed, verdict VERIFIED |
| 5 | **Code quality** | a code review pass | zero critical/high findings |
| 6 | **Canary/smoke** | a small positive+negative check | the positive case passes and the negative case correctly fails |
| 7 | **Summary** | a plain final report | a summary file exists, honestly labeling VERIFIED vs. CODE-SHIPPED-NOT-VERIFIED |

The rule that makes this trustworthy: **a stage may not start until the
prior stage's verification artifact says VERIFIED**, keyed to this run.
Downstream stages consume that artifact directly — never a summary of what
someone *said* happened.

## Verification probe for this skill itself

Before trusting the pipeline on a real task, prove it on a toy task first:
run it end to end and confirm the canary stage genuinely rejects a bad
input (prints something like `positive=VERIFIED negative=FAILED(correctly)`)
— that's what proves the gate isn't rubber-stamping everything, before you
ever let it run unattended.

## Running it unattended

Only after it's proven attended on a toy task, wrap it with a
run-until-done condition anchored on **observable** state, e.g.: "run the
full pipeline for `<TASK>`; after each stage, show the stage marker and its
verification artifact; stop successfully only when all 7 stage markers
exist, every artifact's verdict is VERIFIED, the code-quality gate shows
zero highs, and the canary shows the positive passing and the negative
correctly failing; stop as a failure — do not retry — if any artifact isn't
VERIFIED, the canary's negative case comes back VERIFIED (i.e. it didn't
actually fail), cost exceeds your budget, or the kill-switch flag appears;
cap it at N turns, and if it hits the cap, report which stage markers exist
so it can resume." Never treat prose like "done" or "production-ready" as
completion — only the command output counts.

## Anti-patterns

- Don't let the swarm redefine the task mid-flight — lock the target brief
  at stage 1 and pass it verbatim to every role.
- Don't run the code-quality gate before QA — a failing build makes style
  review moot.
- Don't claim done without the canary passing and a non-empty set of
  verification artifacts — that's exactly the "shipped with zero evidence"
  failure this pipeline exists to prevent.
- Don't spawn writable sub-agents, and don't bypass whatever depth/worker
  cap you set on the swarm stage.

## How to use

**Install:** copy this folder into `~/.claude/skills/autobuild-loop/` for
personal use, or `.claude/skills/autobuild-loop/` inside a project repo.
This skill describes the pipeline shape and gating discipline — wire each
stage to whatever planning, review, and test tooling you actually use.

**Invoke:**

```
Run autobuild-loop for "add rate limiting to the public API, with tests and
a rollback plan." Show me each stage's verification artifact as it
completes, and don't let any stage start until the previous one is
genuinely VERIFIED.
```

```
Resume the autobuild-loop run from yesterday — check which stages are
already marked done and pick up at the next one.
```
