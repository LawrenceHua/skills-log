---
name: work-queue-stall-triage
description: Diagnose a growing work queue read-only by measuring launches, completions, workers and age, naming the stall pattern and its owner, and escalating once per new pattern instead of on every run.
---

# Work queue stall triage

"Throughput is down" is a symptom shared by very different faults. Nudging the queue by hand hides the fault and can duplicate work. Measure, name the pattern, tell the owner once.

## Inputs

- Read-only queue status: open items, counts by state, last launch and last completion times.
- Worker or slot status: running count and open claims.
- The tail of the scheduler or runner log.
- The previous escalation, with its time and numbers.

## 1. Measure

Record open backlog, its change since the last run and over 24 hours, arrivals, launches and completions in the last 1, 6 and 24 hours, running workers, and the age of the oldest open item. Note the read time.

If a measurement command fails, report that. Do not estimate.

## 2. Name the pattern

| Pattern | Signature | Likely owner |
|---|---|---|
| **No workers** | work is ready, the runner is ticking, launches and running workers are zero | dispatcher or slot pool |
| **Re-commit loop** | the log shows the same item ids returning to the same state every tick | state-machine logic in the runner |
| **Runner silent** | no ticks in the log | scheduler or the runner process |
| **Intake flood** | completions normal, arrivals far higher | capacity or duplicate filtering |
| **Waiting on a person** | most old items sit behind an approval or answer | the decision maker; this is not a software fault |
| **Machine pressure** | admission refused for disk, memory or load | host owner |
| **Busy but unproductive** | launches normal, completions near zero | worker failures; sample their results |

Check "waiting on a person" and "nothing ready" before calling zero launches a fault. If two patterns apply, report both with their counts. If none fits, say `unclassified` and include the evidence.

## 3. Escalate with hysteresis

1. Escalate on the first run that confirms the problem, for example two consecutive runs of decline.
2. Send one note to the owner of the broken part: pattern, numbers, repeating item ids and a log excerpt with secrets removed. Send a person one short line only if they must decide something.
3. On later runs, record the numbers and stay quiet. Escalate again only if the pattern changes or the backlog has grown more than 10% since the last escalation.
4. When it recovers, send one recovery note.

## 4. Confirm recovery

After the owner's fix, require launches within two runner ticks and a falling backlog over three runs. A single completion is not recovery.

## Never

- Never run the runner, verifier or intake step by hand to push items through.
- Never edit queue state, runner code or the state database during diagnosis.
- Never restart services or kill sessions you do not own.

## When to use

- A queue or throughput monitor reports a decline or a growing backlog.
- A scheduled monitor keeps sending the same alert.

## How to use

1. Copy the `work-queue-stall-triage` folder into `~/.claude/skills/` for personal use, or `.claude/skills/` inside a project.
2. Ask Claude Code to use the skill by name.
3. Example prompts:
   - "Use the work-queue-stall-triage skill on my job queue. Status comes from `<command>` and the runner log is in `<folder>`."
   - "Use work-queue-stall-triage to decide whether this is a stall or an intake flood, and whether it is worth a new escalation."
