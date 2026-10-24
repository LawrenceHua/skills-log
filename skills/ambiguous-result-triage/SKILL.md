---
name: ambiguous-result-triage
description: Interpret empty, partial, or blocked results correctly by separating no data from unreadable from none, classifying blocked items by next step instead of asking questions, and suspecting the probe before the artifact when a check disagrees with earlier evidence.
---

# Ambiguous result triage

Most wrong status reports are not lies. They come from treating an ambiguous result as a clean one: a search that found nothing, a throttled request that returned fewer rows, a stuck task reported as "blocked", or a check that disagrees with something already verified. This skill gives three rules for handling those.

## Rule 1: Ask whose evidence it is before asking whether it is right

A zero from a narrow query is a claim about the query, not about the world. Searching three of four repositories is not evidence of absence. A rate-limited API returning fewer rows is not a drop in activity.

Keep three outcomes distinct, because each has a different next step:

| Outcome | Meaning | Next step |
|---|---|---|
| `no_data` | The source was read successfully and has nothing matching | Report absence, with the query and scope used |
| `unreadable` | The source could not be read (permission, timeout, throttle, parse failure) | Fix access or retry; report as unknown, not as zero |
| `none` | The check is not applicable or was not run | Say it was not run |

Collapsing these is how a monitor reports green forever. Before reporting a number or an absence, write one line: what produced this, and what did it not cover?

## Rule 2: Classify a blocked item, do not just call it blocked

"Blocked" is a classification failure, not a status. Sort every blocked item into exactly one bucket:

1. **Decidable.** A reasonable default exists. Take it, record the rollback, and move on.
2. **Needs the owner.** Only the owner can supply the input or approval. Batch these into one list, each with the exact ask and the default you will use if no answer comes.
3. **Waiting on a build or job.** This is sequencing, not a block. Note what it waits on and when you will check.
4. **External.** Name the service or party and the date you expect resolution.
5. **Unrecoverable.** Close it in writing with the reason.

Never return a question when a decision with a recorded default is possible.

## Rule 3: When a probe contradicts verified work, suspect the probe first

If a check reports a defect in something you already confirmed with a command, test the probe before changing the artifact. Common probe faults:

- A truncated read that hides the closing marker of a document and makes it look broken.
- Quoting or expansion that makes every path look missing.
- A partial clone, stale cache, or wrong working directory that makes files look deleted.
- A comparison that normalizes one side but not the other.

Steps: re-run the original verifying command, run the probe on a known-good sample, then widen the probe's input or fix its quoting. Only when the probe passes on known-good input do you treat its finding as real.

## Related habits

- A panel nobody can load, or a button nobody monitors, implies someone is watching. If there is no reader, fix the reader before building the surface.
- Never lower a threshold to make a gate pass. If the gate refuses, either the thing is not ready or the gate is wrong, and the second needs an argument, not an edit.

## When to use

- Writing a status report, monitor, or summary where some inputs were empty, partial, or unreadable.
- Triaging a task list full of items marked "blocked".
- A new check reports a failure in something you have already verified.

## How to use

1. Copy this folder into `~/.claude/skills/` for personal use, or into `.claude/skills/` inside a project.
2. Ask Claude Code to use the `ambiguous-result-triage` skill by name.

Example prompts:

- "Use the ambiguous-result-triage skill on this weekly report and mark every zero as no_data, unreadable, or not run."
- "Here are 12 blocked tasks. Use ambiguous-result-triage to classify each by next step and give me one batched list of owner asks with defaults."
