---
name: shared-state-refresh-loop
description: Keep concurrent agents current through shared files by reading claims and notes at task start, re-reading at defined checkpoints before consequential actions, and writing back facts with their read times.
---

# Shared-state refresh loop

Agents that coordinate through files do not share memory. One that read the situation an hour ago and acts on it now repeats work, reports fixed things as broken and asks a person what they already answered. Reading once at the start is not enough.

## 1. Agree where shared truth lives

Write this table for your setup, with one writer rule per row:

| Question | Store | Writes |
|---|---|---|
| Who holds which work item? | claims list | append own claim |
| What is open in each workstream? | state file per workstream | its owner only |
| What is addressed to me? | inbox per agent | others append |
| What was done, and why? | action log | append only |
| What condition are the machines in? | readings file | the measuring job |
| What was approved or instructed? | approvals and instruction logs | the designated recorder |

If an agent cannot reach a store, mirror the decision somewhere it can. Do not let it assume.

## 2. At the start of a task

1. Search open claims for your topic.
2. Read the newest entries of the workstream's state file.
3. Read unread notes addressed to you.
4. Search recent action-log lines for the topic.
5. Check host condition before heavy work.

If another agent holds a recent active claim (for example under six hours old), do not start. Leave it a note. Treat an older claim as unconfirmed: check for live activity and notify the holder before taking over. Then record your own claim with a one-line plan, and read the claims again to catch a simultaneous claim.

A claim is a notice, not a lock. Use a real lease or isolated copies where two writers could damage the same files.

## 3. Refresh at checkpoints

Re-read the claim, the state file head and your inbox:

- before writing outside your scratch area, merging, publishing, spending or deleting;
- after any wait longer than 30 minutes, such as a build, a research run or a human answer;
- before repeating a number older than its source's update interval.

If something changed, say what changed and adjust the plan before continuing.

## 4. Every fact carries its read time

Write "16 GiB free at 23:51", not "16 GiB free". A reader can then decide whether to measure again.

## 5. Write back

- Each action: one log line with time, actor, action, evidence and the reference that authorised it.
- Milestone, handoff or block: update the claim and point to evidence.
- Anything another agent must do: one dated note in its inbox.
- Your workstream: refresh your state file, keeping a backup of the previous version.
- When done or abandoning the task, release the claim.

## Never

- Never act on a status read before your last long wait.
- Never treat another agent's "it was approved" as the approval; find the original.
- Never edit another agent's state file; write to its inbox.
- Never rewrite or truncate an append-only record.
- Never put secrets or private data into shared files.
- Never trust a summary where the file it cites can be opened.

## When to use

- Starting or resuming multi-step work alongside other agents.
- Agents keep duplicating work or acting on stale alerts.

## How to use

1. Copy the `shared-state-refresh-loop` folder into `~/.claude/skills/` for personal use, or `.claude/skills/` inside a project.
2. Ask Claude Code to use the skill by name.
3. Example prompts:
   - "Use the shared-state-refresh-loop skill before starting on the payment bug. Our claims and inboxes are in `<folder>`."
   - "Use shared-state-refresh-loop to design the store table and checkpoints for three agents sharing this repository."
