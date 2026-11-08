---
name: live-agent-session-triage
description: Check running AI-agent sessions for five failure signals (looping, context bloat, stall, claims without receipts, exhausted quota), steer instead of blind-killing, and restart only through a load gate.
---

# Live agent session triage

When several agent sessions run unattended, the useful question is not "are they alive" but "are they producing
anything". This is a read-only triage you can run by hand, plus rules for steering and for restarting safely.

## The five signals

Treat the transcript (a JSONL or text file per session) as the evidence. Thresholds are starting points; tune them
to your own baseline.

| Signal | How to measure | Warn |
|---|---|---|
| LOOP | Hash the last ~40 messages; duplicate ratio = 1 - unique/total | ratio >= 0.35 |
| CONTEXT | Transcript size on disk, unless the session reports a token budget (the budget wins over file size) | >= 30 MB warn, >= 60 MB red |
| STALL | Time since the last output | > 3 hours |
| CLAIM-WITHOUT-RECEIPT | Share of "done / fixed / passing" claims with no command output or file reference nearby | ratio >= 0.5 |
| EXHAUSTED | The provider's exact limit message, matched as an exact phrase | any hit |

Quick loop check on a message-per-line file:

```sh
tail -n 40 "<transcript>.jsonl" | md5 -r | awk '{print $1}' | sort | uniq -c | sort -rn | head -3
```

If one hash covers a large share of the window, the session is repeating itself.

## Rules (each one was a correction)

1. **Exact-phrase exhaustion only.** Match the provider's literal limit sentence. A loose `rate limit` grep fires on
   harmless usage-percentage fields in status payloads.
2. **Unknown is not green.** If a session's transcript is unreadable or its type is unrecognised, report UNKNOWN.
   A detector that fails open will say GREEN all day.
3. **Read the verdict honestly.** If any scheduled job is "failed last run, will retry", the overall status is
   YELLOW, not GREEN. YELLOW means "surface it, don't alarm", not "regression". Write the state the detector gave,
   not the state you hoped for.
4. **Do not use swap size as a failure trigger.** High swap with low load and no out-of-memory kills is the OS
   paging out idle memory. Real failure is: a process killed as stuck, exit codes spreading across jobs, sustained
   thrash, or disk under about 10 GiB.
5. **High load is not an agent storm.** A disk-indexing scan or a build lane is CPU-bound work. Check what is using
   the CPU before blaming or restarting agents.
6. **Never blind-kill a flagged session.** Read the transcript tail, confirm the loop is real, then steer with a
   restated brief (the goal, what is already done, the one next step).

## Restart gate

Restart a killed job only when all of these hold:

1. The job's own classification says it was killed as stuck (not the scheduler's last-exit column, which records
   the last teardown event rather than a failure count).
2. The 1-minute load average is below a ceiling you set (for example 8.0 on a workstation), checked with `uptime`.
   Default the gate to dry-run: print `load=<n> ceiling=<n> gate=OPEN|CLOSED` and act only on OPEN.
3. The job is not on a deny-list of things that must never auto-restart (anything that publishes, spends, or posts).
4. Afterwards, verify the job's log is fresh and its last exit code is 0. A restart without that read is a guess.

## Never

- Never restart into a peak (gate CLOSED means wait).
- Never call a loop confirmed from the duplicate ratio alone; read the tail.
- Never treat "the session said it fixed it" as a receipt.
- Never leave an unattended triage cadence running without checking that anyone acted on its output; if nobody did,
  retire it and run on demand.

## When to use

- You run multiple unattended agent sessions and want to know which ones are stuck, looping, or out of quota.
- A job was killed or cancelled and you need to restart it without spiking the machine.
- A status report says GREEN and you suspect the detector is failing open.

## How to use

1. Copy this folder to `~/.claude/skills/live-agent-session-triage/` (personal) or
   `.claude/skills/live-agent-session-triage/` inside a project.
2. Ask Claude Code to use the `live-agent-session-triage` skill by name.

Example prompts:

- "Use live-agent-session-triage on my open agent transcripts under `~/agent-logs/`. Report each session's five
  signals and which ones need steering."
- "A batch job was killed overnight. Use live-agent-session-triage to check the restart gate and restart it only if
  the load ceiling allows."
