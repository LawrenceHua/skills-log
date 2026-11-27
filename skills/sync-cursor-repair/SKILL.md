---
name: sync-cursor-repair
description: Repair a recurring sync or relay that repeats old failures, recopies items or misses new ones by finding the stale cursor, catching up without deleting, and deriving the cursor from the newest success receipt on every run.
---

# Sync cursor repair

A sync job remembers how far it got through a cursor: a timestamp, line number, id or failure streak. When that value lives in the job's prompt, a hard-coded setting or a cached file nobody updates, the job drifts. It escalates old failures, skips new items or copies everything again.

## Inputs

- The job definition (script, scheduled prompt or configuration).
- Its success receipts: an append-only log, receipt files or the destination's own index.
- Source and destination item lists (ids and timestamps are enough).

## Steps

1. **List every place the job gets its position.** Look for values written into a prompt ("last success at ..."), state files, environment variables and failure counters.
2. **Find the newest real success** in the receipts. Record its time with timezone, the newest source item it processed, the counts and any checksum.
3. **Compare.** Count source items beyond that point. Spot-check at least three items before it at the destination by id or checksum.
4. **Classify the drift.**

| Finding | Meaning | Action |
|---|---|---|
| cursor older than the newest receipt | stale cursor | fix where it is read |
| cursor newer than what the destination holds | items were skipped | catch up first |
| failure streak above zero after a successful run | stale counter | it will raise a false alert; derive it from receipts |
| receipts missing or corrupt | position unknown | stop and report; do not invent one |

5. **Catch up if items were skipped**, using the job's normal copy path. Copy only; delete nothing at either end. Run the job's usual secret or content filter on the batch. If the batch is far larger than normal (about ten times), or targets a store with a single designated writer, hand it to that owner.
6. **Fix the read point, not the value.** Make each run derive its cursor from the newest success receipt and ignore any built-in "last success" or streak value. Pasting today's value into the prompt only goes stale again.
7. **Make every run write a receipt**: run time, newest source item processed, counts, checksum and status.
   - Store the position as the newest **item** handled, not the time the run happened. Items that arrive during a run are otherwise skipped.
   - Advance only after the write succeeds, so a crashed run reads the items again.
   - Re-read a small overlap and de-duplicate by id, which covers late or out-of-order items.
8. **Verify on the next scheduled run.** It should read the new cursor, copy only newer items, write a receipt and raise no old alert.

## Output

- One line: where the stale cursor was, the correct position and how many items were missed.
- A catch-up receipt if anything was copied.
- The job definition change as before and after text.

## Stop rules

- Change your own job directly. For someone else's job, send them the proposed change.
- After two failed verification runs, report with both receipts.
- Never print secrets or tokens in logs or reports.

## When to use

- A relay keeps reporting a failure that was fixed.
- A sync says there is nothing new while new items exist.
- A job recopies the same items on each run.

## How to use

1. Copy the `sync-cursor-repair` folder into `~/.claude/skills/` for personal use, or `.claude/skills/` inside a project.
2. Ask Claude Code to use the skill by name.
3. Example prompts:
   - "Use the sync-cursor-repair skill on my hourly notes sync. It still reports last week's failure; the script is in `<folder>`."
   - "Use sync-cursor-repair to find out whether this importer skipped records, using its run log and the destination index."
