---
name: evidence-judged-worker-fallback-chain
description: Run an unattended coding worker with an ordered fallback to a second model family, judging each worker by commits and a verdict line rather than exit code, with no silent substitution and a result bundle for the next step.
---

# Evidence-judged worker fallback chain

An unattended worker can run out of quota, crash, or exit cleanly having done nothing. This skill chains workers so work continues from the same repository state, without letting a fallback silently replace the model you chose and without trusting an exit code.

## Contract for every lane

Each lane (one worker run in its own folder) leaves these files, even on failure:

| file | meaning |
|---|---|
| `out/started` | written before the worker runs; a second launch seeing it is a skip |
| `out/rc` | the worker's exit code, or `CHAIN-STOP` if a precondition failed |
| `out/finished` | written last |
| `out/new-commits.txt` | commits made after the base commit |
| `out/REPORT.md` | the worker's report, which must end with a verdict line |
| `out/result.bundle` | a portable git bundle of the repo, the starting point for the next lane or machine |

The verdict line is exactly one of `READY-FOR-REVIEW` or `NOT-READY`.

## Judge the worker by evidence

A worker counts as done only when all three hold:

1. exit code is zero,
2. at least one commit exists past the base commit,
3. `out/REPORT.md` contains a verdict line.

Anything else means the worker did not finish. Do not read its prose summary to decide.

## The chain

1. Run worker A (your first choice) in a standalone clone of the repo, not a linked worktree, so the sandbox can commit.
2. If A is not done by the test above, start worker B (a different model family) in the **same repo state**, with one sentence prepended to the brief: a previous worker was here, check the repo before redoing anything.
3. If B also fails, stop and write `out/FALLBACK_NEEDED`. A person or the orchestrating loop decides what runs next. The chain never invents a third option.
4. After the last worker, always create the bundle and the new-commits list.

## No silent substitution

- Disable any built-in "fall back to another model" behavior in each worker's own tool (use the tool's no-fallback switch or environment variable). The chain, not the tool, owns the fallback order, and every hop is recorded.
- If a worker reports its quota is exhausted, record that as the reason, write the marker file and stop; do not retry the same family in a loop.
- Metered or paid APIs do not belong in an automatic chain. They need an explicit human decision.

## Waiting on gates and earlier rounds

- A launcher should proceed only when a fresh capacity reading says heavy work is allowed and a seat is free. Poll on a fixed interval with a bounded number of tries, log each decision, and give up with a recorded reason rather than waiting forever.
- When a round depends on an earlier round, wait for its `out/rc`, require its report to say `READY-FOR-REVIEW`, clone its head, then start. A missing or `NOT-READY` predecessor writes `CHAIN-STOP` and exits zero: the orchestrator decides, the chain does not guess.

## Hygiene

- Give each lane a private temp directory and a timeout on every model call.
- Count externally visible side effects (pending approvals, queued messages) before and after; a test run once created dozens of real ones.
- Treat any example launch script as a template. Copy and edit paths; never run one unmodified.

## When to use

- Overnight or walk-away coding runs where one model family may hit a limit.
- Multi-round builds where each round starts from the previous round's commits.
- Debugging a chain that "succeeded" but produced no commits.

## How to use

1. Copy this folder into `~/.claude/skills/` (personal) or `.claude/skills/` inside a project, then restart or refresh your session.
2. Ask Claude Code to use the `evidence-judged-worker-fallback-chain` skill by name.

Example prompts:

- "Use the evidence-judged-worker-fallback-chain skill to write a run script that tries worker A, then worker B from the same repo state, and always leaves the out/ files and a bundle."
- "My last overnight run exited 0 but nothing changed. Apply evidence-judged-worker-fallback-chain and tell me which of the three done-conditions failed."
