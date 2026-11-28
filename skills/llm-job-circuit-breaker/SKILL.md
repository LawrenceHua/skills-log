---
name: llm-job-circuit-breaker
description: Guard a scheduled LLM job with an exclusive lock, a hard timeout, a substantive-output check and a persisted circuit breaker, so exhausted quotas and empty runs stop repeating on every tick.
---

# LLM job circuit breaker

Unattended model jobs waste money and time in quiet ways. One retries an exhausted quota or a billing error on every tick. Another exits 0 after printing only a banner and a spinner. A third hangs on a stalled stream and blocks every later run. This skill builds a wrapper around the model command that catches all three.

## 1. Lock

- Take an atomic lock (`mkdir <lockdir>`, or a file-lock tool) before starting the model command.
- With `mkdir`, record the owner's process id and process start time inside the lock. Reclaim it only when that process is gone. Matching the start time covers a reused process id. Do not reclaim on age alone.
- A directory without owner details may belong to a run that is still writing them. Treat it as held, and report it if it persists.
- Two later runs can both find the same dead owner. Make the reclaim itself exclusive, or use an OS file lock that is released when the process exits and needs no reclaim.
- If the lock is held, log a skip and exit.

## 2. Hard wall-clock timeout

Run the model command under a timeout that escalates to a kill, for example GNU `timeout --kill-after=30 <seconds> <command>` (often installed as `gtimeout` on macOS). GNU `timeout` returns 124 when the limit is hit. If it has to send `KILL`, expect 137. Handle both. A 137 can also come from something else killing the process, so record the elapsed time as well.

## 3. Count substantive output

Keep standard output, standard error and the exit code separate. Prefer the tool's structured output mode when it has one, and check for the result field you need.

For plain text, strip terminal escape codes, then drop blank lines, banners, spinners and error lines. Count what remains. Set the threshold from real good runs. Where the job has a concrete product (a file, a record, a message), check that too, because a long apology also passes a line count.

If "nothing to report" is a valid result, have the job print an explicit marker for it and count that as success.

## 4. Classify each run, in this order

| Order | Outcome | Evidence | Effect |
|---|---|---|---|
| 1 | `quota` | failed or empty run with a quota or billing signature in the tool's error channel or structured error | open the breaker now |
| 2 | `timeout` | the wrapper's time limit was reached | count toward the unproductive limit |
| 3 | `crash` | any other non-zero exit | exit non-zero and keep it visible for repair |
| 4 | `zero_output` | exit 0 that does not meet the `success` evidence: too little output or a missing product, with no "nothing to report" marker | count toward the unproductive limit |
| 5 | `success` | exit 0 with substantive output and any expected product, or with the explicit "nothing to report" marker | close the breaker and reset the counter |

- Match signatures against error output only. A successful answer that discusses "rate limits" or the number 429 must not open the breaker.
- Collect signatures from your provider's real error messages, and date the list.
- A short-lived rate limit with a retry delay is not an exhausted quota. Wait as instructed, within a cap.
- A path, syntax or configuration crash is a bug. Do not let a cooldown hide it.

## 5. Persist the breaker

Store state in a small file readable only by the job's user (mode `0600`). Write a temporary file, then rename it over the old one. Keep `state`, `reason`, `opened_at`, `cooldown_until` and `consecutive_unproductive`.

- **Locking:** read and write this state only while holding the lock, so two runs cannot both take the trial run.
- **Quota:** use the provider's reset time when it gives one, capped at your maximum cooldown. Otherwise use a long fallback, such as six hours.
- **Unproductive runs:** after two in a row, open for at least an hour.
- **While open:** do not start the model command. Log `SKIPPED CIRCUIT_OPEN` with the reason, end time and seconds left, then exit 0.
- **After the cooldown:** allow one trial run. Only success closes the breaker. A quota, timeout or empty result opens it again. So does a crash, which keeps the earlier reason, still exits non-zero and stays visible.
- **Missing state file:** treat it as closed, as on a first run.
- **Unreadable or invalid state:** report it and do not start the model until someone fixes or resets it.

A skip that exits 0 looks healthy to a scheduler. Send one alert when the breaker opens, and make the open state visible to whatever watches the job.

## 6. Controls and self-test

Provide `--status` (read-only), `--reset` (clears the breaker and logs who did it and why) and `--selftest`.

The self-test uses a temporary state directory and a fake model command that counts its calls. It must show that:

1. A good run keeps the breaker closed.
2. Invalid flags or timeout values are rejected with a non-zero exit.
3. A quota error opens the breaker, and the next run exits 0 without calling the model.
4. The set number of empty runs opens it, and the following run is skipped.
5. A hanging command is killed and classified as `timeout`.
6. A successful answer containing the word "quota" does not open it.
7. A crash exits non-zero and stays visible.
8. While the lock is held, a second run skips without calling the model.
9. After the cooldown, only one trial run calls the model.
10. A missing state file lets the first run start, while an invalid one blocks the model call.

The self-test must never touch live state.

## Never

- Never count banners, escape codes or error text as work.
- Never switch accounts or credentials to get around an exhausted quota.
- Never change to another paid model without saying so.

## When to use

- A cron job, timer or background agent calls a model with nobody watching.
- Logs show the same quota or billing error many times.
- Runs exit 0 but produce nothing, or one hung run blocks the schedule.

## How to use

1. Copy the `llm-job-circuit-breaker` folder into `~/.claude/skills/` for personal use, or `.claude/skills/` inside a project.
2. Ask Claude Code to use the skill by name.
3. Example prompts:
   - "Use the llm-job-circuit-breaker skill to wrap my scheduled summary script. Add the self-test first, using a fake model command."
   - "Use llm-job-circuit-breaker to review this agent loop and tell me what happens when the quota runs out overnight."
