---
name: routine-overlap-audit
description: Sweep scheduled routines across several agents for duplicates, drift between live configuration and the written record, and stale or missing handoff files, then recommend fixes without changing another agent's schedule.
---

# Routine overlap audit

Two quiet failures build up in a multi-agent setup. Two agents run the same check, which doubles usage and alerts. Handoff files age, so a replacement agent works from old facts. Neither produces an error.

## Inputs

- Each agent's **live** routine list (name, schedule, enabled state, purpose), exported from the scheduler or tool that runs it.
- The written routine record per agent.
- Handoff files (current state, runbook, routine record) with modification times.
- Freshness limits, for example state no older than 3 days and routine records no older than 7.

## 1. Build one table

One row per routine: agent, name, schedule, targets (machines, files, channels) and action type (read, write or message). A routine list you could not read is `UNKNOWN`, not empty.

## 2. Find duplicates

Group by target and action. Flag:

- two agents doing the same kind of action on the same target within each other's interval;
- one agent with two routines whose instructions are nearly identical.

Before recommending a pause, compare what each actually checks and who receives its output. A deliberate independent second check is not a duplicate; label it so. Otherwise name one keeper, with the reason.

## 3. Find drift

Compare the live list with the written record: missing, extra, schedule changed, enabled state changed. Report both values. The live list says what runs; it does not say what was intended.

## 4. Check freshness

Mark each agent's files fresh, stale or missing. Coverage is the number of active agents with all required files fresh divided by all active agents.

Modification time shows a file was written, not that it is right. Spot-check one open item from each fresh state file against its live source.

## 5. Follow up

- Queue one reminder per stale agent, oldest first, at most one per agent per 24 hours.
- Publish a coverage table and a list of duplicates and drift, with a recommendation for each.
- Escalate to a person only if coverage stays below target (for example 80%) for three days, or an owner declines to fix it.
- On the next sweep, confirm reminded files changed and approved pauses appear in the live lists.

## Never

- Never pause, edit or delete another agent's routine. Recommend it to the owner; deletion needs explicit approval.
- Never copy secrets out of routine instructions into the report.

## When to use

- As a daily or weekly sweep across agents.
- Before creating a new routine, to see whether one already covers it.
- When usage or alert volume climbs without more work being done.

## How to use

1. Copy the `routine-overlap-audit` folder into `~/.claude/skills/` for personal use, or `.claude/skills/` inside a project.
2. Ask Claude Code to use the skill by name.
3. Example prompts:
   - "Use the routine-overlap-audit skill on these exported schedules and handoff folders. Which routines duplicate each other?"
   - "Before I add an hourly disk check, use routine-overlap-audit to see whether another agent already runs one."
