---
name: nightly-slippage-review
description: Write a nightly evidence-backed review of what was claimed but unverified, promised but not done and broken, carry unfinished items forward with a day count, and hand the owner at most five decisions.
---

# Nightly slippage review

Daily summaries list what got done. The costly items are the others: claims nobody checked, approved work that never started, and a routine that stopped without an error. This review goes looking for those.

The review reads only, apart from the review file and one log line.

## 1. Take live readings first

Before reading anyone's report, measure the few things that matter yourself (disk, memory, key services, deployed version). Where a monitor disagrees with your reading, record the live value and list the monitor as a defect.

## 2. Gather sources, newest first

- today's approvals and instructions;
- the action log of agents and scripts;
- inboxes and handoff or state files;
- scheduled routine status and last output times;
- yesterday's review, especially unfinished items.

List the sources used with their read times. If one cannot be read, say so; its absence is not a clean result.

## 3. Write the file with a fixed section order

One file per day, such as `day-review-<date>.md`. Never overwrite an existing day; append a "Late addendum".

```
# Day review <date>
Written <time> by <author>. Sources: <list with read times>
## 0. Today in one line
## 1. Claimed but not verified      (claim, who, where, missing evidence)
## 2. Promised or approved, not done (original words or reference, age)
## 3. Broken                        (symptom, live evidence, owner)
## 4. Routines and monitors         (silent, failing, duplicated)
## 5. Improvements planned, not applied
## 6. One fresh finding             (a pattern not raised before, or "none found")
## 7. Fixes applied tonight         (each with evidence)
## 8. For the owner's morning       (at most five, one decision each)
```

Keep it short enough to read in a few minutes, around 150 lines.

## 4. Rules for each item

- Name the evidence (file and line, command output or URL), or mark it `UNVERIFIED`.
- Label status consistently: `VERIFIED`, `CODE-SHIPPED-NOT-VERIFIED`, `BLOCKED`, `INCONCLUSIVE` (see the `verification-labels` skill).
- Mark nothing done because someone said it was done.
- Carry every unfinished item from yesterday's sections 1, 2, 3 and 5 with `(carried, day N)`. Drop one only with evidence that it closed or a recorded decision to abandon it.
- An item carried for several days should reach section 8 as a keep, drop or reassign decision.

## 5. Finish

Add one line to the action log with the time, the review path and the reason it ran. Send section 8 through the channel the owner actually reads.

## Never

- Never turn the review into a repair session. Apply only small, reversible fixes you own; list the rest under section 5.
- Never restart services or change queues during the review.
- Never copy secrets, message bodies or personal data into the review.

## When to use

- As a scheduled end-of-day pass over several agents or automations.
- When someone asks what slipped today.

## How to use

1. Copy the `nightly-slippage-review` folder into `~/.claude/skills/` for personal use, or `.claude/skills/` inside a project.
2. Ask Claude Code to use the skill by name.
3. Example prompts:
   - "Use the nightly-slippage-review skill. Action logs are in `<folder>` and yesterday's review is next to them."
   - "Use nightly-slippage-review to find what was promised this week and has no evidence of completion."
