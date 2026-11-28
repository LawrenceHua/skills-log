---
name: red-job-exit-classification
description: Sort scheduled jobs that show a non-zero exit into deliberate stops, designed negative results, repairs awaiting their next run, out-of-scope jobs and real failures, using current evidence and never by forcing them green.
---

# Red job exit classification

A non-zero exit does not always mean a script is broken. A job may refuse to run because someone paused it. A monitor may use its exit code to report a real problem it found. Showing all of these as "failed" buries true breakage and tempts people to force them green. Calling a real crash "gated" is just as harmful. This skill sorts each red job by its mechanism.

## 1. Read the mechanism before labelling

Stay read-only. For each job, collect:

- The live scheduler record: last exit status, run count, state and the loaded command (for example `launchctl print gui/$(id -u)/<label>`, or `systemctl status <unit>` and `systemctl show <unit>`; add `--user` for user units).
- The job definition and the script it runs, including every path that returns this exit code.
- A bounded tail of its error and output logs, matched to the latest run.
- Any stop file, pause switch or approval state the script reads, as it is now.
- The job's written contract, if it says what each exit code means.

## 2. Assign exactly one class

Test the rows from top to bottom and stop at the first one whose proof is met. A job that is not yours is `out_of_scope` even if it also crashed.

| Class | Required proof | Show as | Allowed action |
|---|---|---|---|
| `out_of_scope` | the job belongs to another person, team or tenant | listed as not yours, with its exit code and owner | tell the owner if needed and change nothing |
| `deliberate_stop` | the latest run hit a named stop switch, closed approval, safety guard or open circuit breaker, and the code shows that this produces the observed exit | paused, with the gate named | leave it in place; whoever owns the gate decides |
| `negative_result` | the documented contract uses this exit to report a finding, and the latest output holds that finding | attention needed, with the finding | repair the condition it reports, if that is yours to do |
| `fixed_awaiting_run` | the cause is repaired and a side-effect-free test passes, but no scheduled run has happened since | awaiting run, with the due time | wait for the schedule |
| `real_failure` | anything else: crash, bad path, stale or corrupt input, or an exit nobody can explain | failed or needs investigation | fix the root cause or escalate with the log tail |

When the evidence does not prove any of the first four rows, the class is `real_failure`. Do not read another tenant's logs or data to classify a job you are not allowed to inspect.

## 3. Rules that keep labels honest

- **The explanation must fit this run.** A stop file that exists today does not explain a stack trace. Match the time, exit code and message.
- **One code can have several causes.** If the same code means both "paused" and "crashed", use the message or a structured status to separate them, or treat it as a failure.
- **A scheduler's last exit can be old.** Check the run count and last run time. Signal-based endings after an unload or restart need their own reading.
- **Explanations expire.** Record the evidence, gate name, time and a review date. Check again when the exit code, command or gate changes, or the date passes.
- **A negative result is not success.** It stays visible until the condition clears.

## 4. Repair and confirm

For a real failure that is yours to fix:

1. Back up the file and keep its permissions.
2. Fix and syntax-check a copy, then replace the original with an atomic rename.
3. Run a test that you have confirmed has no outside effects.
4. If you changed the job definition, reload it and confirm the loaded command. With systemd, run `daemon-reload` (with `--user` for user units) and check whether a timer also needs a restart. With launchd, `bootout` and then `bootstrap` the job. `bootout` stops a running instance, and loading can start some jobs at once, so check both before doing it.
5. After a real run under the scheduler, confirm that it is newer than the fix and ended as expected. With launchd, the `runs` count should have risen since your reading after any reload. With systemd, check that `ExecMainStartTimestamp` is later than the fix. Until then, report it as awaiting a run.

Do not start a job by hand when a run can spend money, send messages, publish or place orders, just to clear an old exit code.

## 5. Report

One row per red job: name, class, exit code, last run time, evidence (file and line, or log excerpt with secrets removed), owner and next step. Give counts per class, with real failures first.

## Never

- Never remove or bypass a stop switch, approval or safety limit to reduce the red count.
- Never lower a threshold, swallow an exception or force exit 0 on a failing check.
- Never drop an unresolved failure from the report.

## When to use

- A job dashboard or scheduler listing shows many non-zero exits.
- Someone asks which red jobs are really broken.
- An agent has been asked to "get everything green".

## How to use

1. Copy the `red-job-exit-classification` folder into `~/.claude/skills/` for personal use, or `.claude/skills/` inside a project.
2. Ask Claude Code to use the skill by name.
3. Example prompts:
   - "Use the red-job-exit-classification skill on every non-zero job in my scheduler. Stay read-only and cite the evidence for each class."
   - "Use red-job-exit-classification to check whether this job is really paused or has been crashing behind the pause label."
