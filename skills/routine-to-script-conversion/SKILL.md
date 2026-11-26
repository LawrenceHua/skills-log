---
name: routine-to-script-conversion
description: Decide whether a recurring agent routine can run as a plain scheduled script that wakes a model only on exceptions, then package it as a portable run kit and prove it matches before switching.
---

# Routine to script conversion

Many agent routines do the same thing every run: read a file, compare numbers, append a log line, report "nothing new". A script does that without model usage and without prompt drift. This skill decides which routines qualify and converts them safely.

## Inputs

- The routine's saved prompt and schedule, copied word for word from the live scheduler or a current export. If you only have a summary, label the result "reconstructed" and do not invent schedules or thresholds.
- Its last 10 to 20 run records.

## 1. Five tests (all must pass to convert)

1. **Deterministic inputs.** Fixed files, commands or endpoints, with no open-ended search or prose reading.
2. **Rule-based verdict.** Thresholds, diffs or counts that can be written as code.
3. **Quiet history.** At least 80% of recent runs ended with no change and nothing sent.
4. **Safe output.** The script only writes logs or a status file. No sends, merges, trades, deletes or spending.
5. **A clear exception path.** A defined condition wakes an agent or person, through a channel that exists.

If the gathering and comparing are deterministic but exceptions need judgment, make it a **hybrid**: the script gathers and diffs, and the agent runs only when the diff is not empty. If the routine interprets outside content (mail, chat, web pages) or touches money or publishing, keep it as an agent routine.

Quote run evidence for every test.

## 2. Package it as a run kit

One folder, two files, usable by any agent or by cron.

`RUN.md`, in order: purpose and owner; caveats; schedule with timezone; steps (start with the check script, then what to do for each verdict); a checkable definition of healthy; things it must never do; when to tell a person and through which channel; last verified output with its time.

`check.sh`: read-only, a timeout on every probe that can hang, a fallback for every failed read, and exactly one output line. A probe that cannot read its input reports `UNKNOWN`, never a healthy value or a failure value.

```bash
#!/bin/bash
# Reads: free space on /. Writes: nothing.
set -uo pipefail
free=$(df -Pk / 2>/dev/null | awk 'NR==2 {print int($4/1048576)}')
free=${FORCE_FREE:-$free}   # test seam only; leave unset in the schedule
if ! [[ "$free" =~ ^[0-9]+$ ]]; then verdict=UNKNOWN; free=na
elif (( free < 15 )); then verdict=STOP
elif (( free < 20 )); then verdict=WARN
else verdict=OK; fi
echo "ts=$(date -u +%FT%TZ) disk_free_gib=$free verdict=$verdict"
case "$verdict" in OK) exit 0 ;; WARN|STOP) exit 1 ;; *) exit 2 ;; esac
```

Replace the thresholds with the ones the original routine uses.

## 3. Prove it

1. Syntax check and run once: `bash -n check.sh && bash check.sh; echo "exit=$?"`.
2. Force each branch with a test input and confirm the verdict changes, including the unreadable case (in the example, `FORCE_FREE=10`, `17`, `50` and `unreadable`).
3. Run script and routine side by side for a full day or enough cycles to be meaningful. Verdicts must match on every run, and every mismatch gets explained.
4. Confirm the wake channel by delivering one test exception to it.

## 4. Switch, reversibly

- Get the owner's approval before installing a scheduled job on a shared machine.
- Pause the old routine; do not delete it. Keep it for seven days and re-enable it if the script misses an exception.
- Have something notice when the script stops producing receipts. A silent scheduler looks exactly like a quiet system.
- Estimate and later confirm the saving: runs per day × the share that no longer need a model.

## Never

- Never let the check script write, restart, delete or call paid APIs.
- Never read or log secrets in it. A probe that needs one belongs in a separate wrapper that loads it at run time.
- Never convert a routine that sends or posts into an unattended script without the owner's explicit approval.
- Never claim it was verified without pasting the output.

## When to use

- A recurring routine consumes model usage and usually reports nothing.
- You are handing a routine to another agent or retiring the one that runs it.
- You are writing a new monitor and deciding whether it needs a model at all.

## How to use

1. Copy the `routine-to-script-conversion` folder into `~/.claude/skills/` for personal use, or `.claude/skills/` inside a project.
2. Ask Claude Code to use the skill by name.
3. Example prompts:
   - "Use the routine-to-script-conversion skill on this hourly prompt and its last 20 results. Should it convert, go hybrid or stay?"
   - "Use routine-to-script-conversion to write the run kit and check script for my nightly backup freshness check."
