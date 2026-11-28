---
name: monitor-reading-reconciliation
description: Before acting on or repeating a number from a monitor, dashboard, alert or agent report, take a direct reading of the same thing, reconcile the two and report any defect in the monitor.
---

# Monitor reading reconciliation

Monitors can poll late, watch the wrong volume or host, reuse an old cached value or compute something other than their label says. Repeating their verdict without checking spreads the error. This short check turns "the monitor says" into "I measured".

## Inputs

- The claim: value or verdict, source and the time it was measured.
- A direct, read-only way to measure the same thing.
- How much that quantity normally varies.

## Steps

1. **Restate the claim:** what was measured, on which target, in what units, over what period and when. Put both times in one time zone.
2. **Measure directly now** with the most basic suitable tool: the filesystem's own report instead of a dashboard tile, a request to the service instead of a status page, a modification time and content hash instead of "file updated". Check that your command reads the same target and definition. Check units too, such as GB against GiB.
3. **Reconcile.**

| Finding | Test | Report |
|---|---|---|
| agree | difference within normal variation | the direct value, citing both |
| stale monitor | the monitor's measurement is old and the quantity changed since | the direct value and the delay |
| wrong target or definition | different host, volume, file, unit or window | the exact difference and the monitor as defective |
| real disagreement | both current, same definition, different values | measure a third way before acting; if unresolved, give both and say so |

A later direct reading does not prove an earlier alert was wrong. A spike or short outage may have passed. Check history or logs before calling it a false alarm.

4. **Decide from checked evidence.** Use the direct reading for the current state. Do not delay an urgent protective step that is already authorized, safe and reversible while you sort out a disagreement.
5. **For a stale monitor, a wrong target or definition, or an unresolved disagreement,** send the monitor's owner one short defect note with both readings, their times and the commands. Agreement needs no note.
6. **Log** claim, direct value, finding and monitor name, so repeat defects stand out. Turn a repeated defect into a repair request.

## Output

One line: `<quantity> = <direct value> (read <time>, <command>) | monitor <value> at <time> | <finding>`.

## Stop rules

- If checking would need write access, credentials you do not hold or a risky command, do not do it. Label the claim unverified and name what would verify it.
- Read-only: do not change the system to match the monitor, or the monitor to match the system, unless it is yours to change.
- An accurate report from an agent is still not an approval to act.

## When to use

- You are about to act on, escalate or repeat a monitor's number or status.
- Two dashboards or reports disagree.
- An alert surprises you.

## How to use

1. Copy the `monitor-reading-reconciliation` folder into `~/.claude/skills/` for personal use, or `.claude/skills/` inside a project.
2. Ask Claude Code to use the skill by name.
3. Example prompts:
   - "Use the monitor-reading-reconciliation skill on this low-disk alert before you tell me what to do."
   - "Use monitor-reading-reconciliation to check each number in this status report against a direct reading, and list monitor defects."
