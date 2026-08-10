---
name: background-agent-roster
description: The twelve standing background agents worth running on any machine that hosts unattended AI automation — meta-monitor, health scanner, watchdog, zombie reaper, self-healer, skill miner, morning brief, memory sync, CLI hygiene, cost monitor, notification doctor, keep-awake — with the receipt-file discipline that keeps the whole roster honest.
---

# background-agent-roster

Once AI automation runs unattended — scheduled jobs, watchers, pipelines — the
failure mode changes: things don't break loudly, they *stop quietly*. A job
dies and nothing notices for three weeks. Distilled from an estate that grew to
~300 scheduled jobs, these are the twelve that earn a slot on any machine, and
the two rules that keep them honest.

## The two rules (more important than any single job)

1. **Every job leaves a receipt.** A timestamped file or log line written on
   every successful run. A job with no receipt is indistinguishable from a job
   that never ran — and "it's scheduled" is not evidence it executed.
2. **Auto-fix only what's idempotent and whitelisted.** Restarting a crashed
   service: fine. Anything else surfaces as a finding for a human. And the
   repair layer must never be able to kill the agent doing the repairing —
   put your primary agent processes on an explicit never-touch list.

## The roster

| # | Agent | Cadence | Job |
|---|---|---|---|
| 1 | **Estate meta-monitor** | 30 min | Reads every other job's receipt; alerts on stale receipts and non-zero exit codes. The watcher of the watchers — the only job whose purpose is catching silent staleness. |
| 2 | **Deterministic health scanner** | 2 h | No-LLM sweep: stale state files, config/security drift, orphan scheduler entries, zombie processes, world-readable secrets. Fast, free, catches the boring failures. |
| 3 | **Fleet watchdog** | 1–5 min | Probes critical local services (ports, health endpoints). Acts only after N consecutive failures — the strike rule prevents restart-flapping on a single blip. |
| 4 | **Zombie reaper** | 10 min | Kills orphaned agent subprocesses that outlived their parent session. Scoped by parent-process rules + the never-touch list. |
| 5 | **Self-healer** | 10 min | Restarts crashed services, clears stale locks, prunes logs past a size cap. The "don't page a human for transient issues" layer. |
| 6 | **Session→skill miner** | weekly | Scans the week's agent session transcripts for repeated workflow patterns; drafts skill candidates into a review queue. Human-approved, never auto-promoted. |
| 7 | **Morning brief** | daily, early | Digests overnight receipts, failures, and deltas into one message (or audio) so the day starts with state, not archaeology. |
| 8 | **Memory sync** | 5–15 min | Commits and pulls the agent memory store through git (see `agent-memory-sync`) so context survives sessions and machines. |
| 9 | **CLI hygiene** | nightly | Compacts/archives old agent sessions, repairs corrupted session files, runs a smoke test after CLI updates to catch regressions. |
| 10 | **Cost monitor** | daily | One rollup of yesterday's AI/API spend against a baseline, alerting on spikes. Dozens of scheduled agents will surprise you on the bill exactly once. |
| 11 | **Notification doctor** | 30 min | Inventories alert sources, dedupes repeats, auto-fixes only whitelisted idempotent issues. Owning alert fatigue beats ignoring banners. |
| 12 | **Keep-awake** | always | `caffeinate` (macOS) or the OS equivalent, as a supervised service. Trivial but load-bearing — everything above dies if the host sleeps mid-run. |

## Build order

Start with **1, 2, 8, 12** (meta-monitor, health scanner, memory sync,
keep-awake): they protect everything you add later. Add **10** (cost) before
your job count hits double digits. The rest as the estate grows — each new
always-on process should arrive *with* its receipt and its meta-monitor entry,
not get them retrofitted.

## Scheduler notes

- macOS: launchd user agents (`~/Library/LaunchAgents/*.plist`) — survive
  reboots, support both intervals and calendar times. Linux: systemd user
  timers or cron. Either way, one label/unit per job, logs to files.
- Idle-between-runs is the normal state for interval jobs — "not currently
  running" is not "broken". The receipt file, not the process table, is the
  health signal.
- Delta-gate expensive jobs: skip the run when inputs haven't changed since
  the last receipt.

## When to use

The week you set up your first unattended AI automation — the roster is much
cheaper to grow alongside the estate than to retrofit after the first silent
three-week outage.

**Skip it for:** purely interactive use with nothing scheduled.

## How to use

**Install:** copy this folder into `~/.claude/skills/background-agent-roster/`.

**Invoke:**

```
Using the background-agent-roster skill: inventory every scheduled job on this
machine, tell me which of the twelve roster slots are covered / missing, which
jobs have no receipt file, and draft the meta-monitor for what exists.
```
