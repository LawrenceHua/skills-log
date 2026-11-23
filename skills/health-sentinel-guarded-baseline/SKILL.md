---
name: health-sentinel-guarded-baseline
description: Build or use a health check for an agent or dev setup that fails closed (UNKNOWN, never healthy, for a check that did not run), compares against a saved baseline while labelling that comparison as a report rather than proof, and classifies process exits and memory signals instead of counting them.
---

# Health sentinel with a guarded baseline

One command should answer "is my agent setup healthy, what changed, and what can I improve safely?" with evidence a second person can re-run. Most home-grown health scripts fail the same way: they print green for checks that never ran, they count normal shutdowns as failures, and they compare today's output to yesterday's output of the same script and call that verification. This skill is the design and operating discipline that avoids those failures.

## When to use

- You are writing or reviewing a health or diagnostics script for agent tooling, scheduled jobs, or a developer machine.
- Someone asks "is the stack healthy?", "what got worse?", "why is everything slow?", or "what am I spending on context?".
- You want an unattended improvement pass that cannot silently break anything.

## Core rules the sentinel must enforce on itself

1. **Never report healthy for a check that did not run.** A config dump that failed, a missing binary, an unreadable log, an unreachable service: each becomes `UNKNOWN` with the reason attached. An empty result must say why it is empty (no data, unreadable, filtered, unreachable are different facts).
2. **A comparison against your own earlier output is a report, not a verification.** Print that caveat next to every baseline comparison, every time. To verify a change, name a reference the builder did not produce: a live probe, a third-party tool, or a fresh-context reviewer whose default is "refuted".
3. **Every check must be able to fail.** Give each rule a self-test case it must reject: a termination signal that must not count as a failure, a malformed profile that must yield `UNKNOWN`, a missing directory that must not become a zero. If a check can no longer fail it is decoration, and the self-test should say so.
4. **Read-only by default.** Only an explicit apply flag may change anything, and it refuses outright while a kill switch file exists.

## Exit codes (wire alerts to the right ones)

| Code | Meaning |
|---|---|
| 0 | all checks pass |
| 1 | a warning or a non-critical failure |
| 2 | a critical failure (core config, a required lane, a required bundle) |
| 3 | a check could not run (`UNKNOWN`) |
| 4 | refused because the kill switch is engaged |

Alert on 2 and 3, not on 1. Treating "could not run" as just another failure hides the most dangerous state.

## What to check

- **Effective configuration drift.** Do not read config files; ask the tool to print its composed, effective config and compare the values that drive cost (tool-output inline budget, compaction trigger and retention, pruning). A value that appears in a file but not in the composed output did nothing.
- **Silently skipped plugins or bundles.** A loader that logs a refusal to stderr and continues leaves the model without a capability and nobody informed. Diff the composed tree against what you intended to load.
- **Dead lanes.** For each model or worker lane, look at the result of its last real call, not a static "ready" probe. A lane whose probe says ready while its last real call failed is dead.
- **Scheduled jobs.** Classify, do not count. A signalled unload (exit `-15` or `-9`) is not a failure. A job holding a process id is running, and its exit code is the previous run's. Counting every non-zero exit overstated failures by roughly six times in one real setup.
- **Resources.** Report disk percentage and the page-in rate over a short window, not total swap used. Swap used is a historical allocation: gigabytes of swap with near-zero swap-ins per second is normal, and chasing it sends you after a bottleneck that is not there.
- **Skill or plugin mesh.** Run the sync tool's check mode and require exit 0.
- **Context cost.** Measure mean context per request from session logs with a capped sample. Context length, not tool-call volume, tends to be the cost driver, and one compaction setting (trigger at a high percentage of the window and retain a large fraction) can be the single largest defect. Re-check it after any upgrade or profile reset.

## Commands to expose

| Situation | Command |
|---|---|
| Is the stack OK, before or after work | `doctor` |
| Something got worse, or verify an optimization held | `guard` (compare against the saved baseline) |
| Record what good looks like now | `guard --save`, only once state is known good |
| Why is it slow, what am I spending | `measure` |
| What can be improved safely | `optimize` as a dry run |
| Prove the checks can still fail | `selftest` |
| Is automation halted | `status` |

## Safeguards

- **Kill switch.** One file (for example `HALT` in the state directory) stops every mutating path; `status` still works; deleting the file resumes.
- **Receipts.** Every apply writes a timestamped backup and an append-only history line.
- **A config change is not shipped until it is composed.** After editing a profile, print the effective config and find the new value in it. An edit that does not appear did nothing.
- **Config loads at session start.** A running session keeps what it loaded. Never claim a gain from the session that made the change; verify in a new one.
- **Managed or sandboxed profiles.** If a profile cannot be dumped in place, copy it to a scratch name, dump that, then delete the copy.

## Unattended pass, in order

1. `doctor --measure` (what is true now).
2. `guard` (what changed since the saved reference).
3. `optimize` as a dry run (what it would change).
4. Apply only after reading the proposal: one change at a time, rollback named.
5. `guard --save` only once the state is known good.

Do not run `doctor --measure` in a tight loop; `guard` exists so you do not need to poll.

## Reporting

Use four labels and name the command that justifies each: `VERIFIED`, `CODE-SHIPPED-NOT-VERIFIED`, `BLOCKED`, `INCONCLUSIVE`. A baseline comparison alone is at most "no change versus the saved reference", never `VERIFIED`.

## How to use

1. Copy this folder into `~/.claude/skills/` for personal use, or into `.claude/skills/` inside a project.
2. Ask Claude Code to use the `health-sentinel-guarded-baseline` skill by name.
3. Example prompts:
   - "Use the health-sentinel-guarded-baseline skill to review my `healthcheck.sh`. Tell me which checks can report green without having run, and which can never fail."
   - "Use the health-sentinel-guarded-baseline skill to diagnose why my agent setup feels slow and expensive. Measure context per request and page-in rate before blaming memory, and give me a dry-run list of safe changes."
