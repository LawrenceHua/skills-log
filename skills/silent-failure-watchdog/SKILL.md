---
name: silent-failure-watchdog
description: Build an independent observer for a scheduled job that exits 0 whether it worked or sat idle, alerting once per condition on stale, never-armed or self-contradicting state without crying wolf on normal absence.
---

# Silent-failure watchdog

Some jobs cannot fail loudly. A watcher that should have triggered a transfer, a cron that should have posted a digest, a loop that should have armed itself: all of them **exit 0 on every path**, including the path where they did nothing. Their failure mode is not an error, it is agreement. This skill defines the observer that turns that quiet agreement into one actionable alert, without becoming the noisiest alarm you own.

## 1. Classes of silence and which deserve an alarm

| Class | Looks like | Alarm? |
|---|---|---|
| never armed | state file has no "armed at" field, or is empty | yes, once: nothing is watching and everyone assumes otherwise |
| stale | the job's own artifact has not been touched in N times its cadence | yes, once |
| positive contradiction | the thing answers and says it is broken (health flag false, queue growing, counter stuck at zero while it should rise) | yes, once |
| absence | the thing does not answer at all | only if it is expected to be present |

**Absence is the trap.** Devices leave the network, services sleep, laptops close. An observer that treats "no answer" as failure alarms on every normal departure and gets muted before the one night it matters. Alarm on contradiction (reachable and wrong); stay silent on absence unless presence is expected.

## 2. Shape

- **A separate process on a separate schedule.** Never a branch inside the job it observes: a job that died before its own check cannot run that check.
- **Its own state directory**, one marker per condition (`watchdog-<condition>.alerted`), plus a log line every run whether or not it alerts. That log is how you notice the observer itself stopped.
- **Alert once per condition per window** (for example 6 hours): post, write the marker, re-post only after the window. **Clear the marker when the condition goes away** so the next occurrence re-arms.
- **Say the fix, not the symptom.** The alert names the condition, the evidence and the one action that resolves it. "Not answering" is not actionable; "power-cycle it" is.
- **Exit 0 when healthy, non-zero on alert**, so the scheduler's exit code is a second signal.

## 3. Never

- Never make the observer depend on the thing it observes: no shared lock, no shared environment, no import of the observed module.
- Never ask a thing about itself and call it corroboration. A health flag is worth reading because it is a contradiction signal, not an independent reference.
- Never put `grep -c` in an `||` chain: it exits 1 when the count is 0, so `count=$(... || echo 0)` takes the fallback on a valid zero.
- Never lock on an mtime: two runs in the same timestamp both proceed. Lock on the owner PID.
- Never release a PID-file lock directory with `rmdir`; it contains the pid file and the lock becomes permanent. Remove it recursively.
- Never test only the new flag. Run the tool's default (scheduled) invocation once too; a guard that passes `--selftest` while the scheduled path is broken is the defect it was meant to catch.

## 4. Prove it, in this order

1. **Self-test with one arm per class**, fixtures in a throwaway directory, and a local HTTP server on an ephemeral port for anything that probes the network. Require "N passed, 0 failed".
2. **A negative control in the real state directory**: make the condition true on the live host, run once, and require the alert path to execute (non-zero exit, marker written, message rendered). Then clear it and require a clean run with zero markers.
3. **An external reference that the alert did or did not happen.** The observer's own log is a report; the destination channel's newest message timestamp is the reference. Capture it before and after a healthy run and require it unchanged.
4. **The scheduler's own view** after install: lint the job definition, load it, then confirm the run counter rises and the last exit code is 0 on a real tick. A loaded job that never ran is a green light on an empty room.

## 5. Install without breaking the next run

Write the new script to a temp name, copy the **original's file mode** onto it, then atomically rename. A plain write-then-replace can strip the executable bit, so every caller gets "Permission denied" while a syntax check still passes. After install, check the executable bit and invoke the default path once.

## When to use

- A watcher or scheduled pass has no failure signal.
- Someone asks "is it actually running?", "why did nothing happen?", or "how would I know if it broke?"
- Adding an alert to an unattended process that must never cry wolf.

## How to use

1. Copy this folder into `~/.claude/skills/` (personal) or `.claude/skills/` inside a project, then ask Claude Code to use `silent-failure-watchdog` by name.
2. Name the job, its cadence, the artifact it should touch, and where alerts should go.

Example prompts:
- "Use silent-failure-watchdog to design an observer for my nightly sync job that always exits 0."
- "Use silent-failure-watchdog to review this watchdog script for false alarms on normal absence."
