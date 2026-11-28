---
name: operating-posture-gate
description: Read a short machine posture before heavy agent work, so a slow outside network, a priority burst, low storage or memory pressure changes behavior in agreed ways instead of causing needless restarts and retry storms.
---

# Operating posture gate

Agents sharing a machine often misread conditions. A slow internet connection looks like crashed local services, so one restarts them. Background jobs compete with an urgent build. Many clients retry a slow API at once. This skill has every agent read the same small posture first and follow the same rules.

## 1. Take the reading

Measure read-only:

- **Local health:** latency and response bodies from your own services on the same machine.
- **Outside network:** latency and error rate for several unrelated external endpoints that are meant to be checked, using light requests and enough samples to mean something.
- **Storage:** free space on each volume that matters.
- **Memory and CPU:** load per core, the operating system's memory-pressure signal and the current swap-in rate. Swap space in use alone can be left over from earlier work.
- **Priority leases:** any unexpired claim that urgent work is running.

Save it to one small file with a timestamp. A reading older than your limit is `UNKNOWN`: measure again, and until then hold off on optional heavy work.

## 2. Name the conditions

Thresholds are examples. Set yours from a normal week.

| Condition | Example trigger | Behavior |
|---|---|---|
| `UNKNOWN` | the reading is stale or a probe failed | hold optional heavy work; report once if it persists, so a broken probe does not stall work silently |
| `NETWORK_SLOW` | local checks healthy, while outside p95 exceeds 2 seconds or more than 20% of requests fail | back off outside calls and leave local services running |
| `URGENT_WORK` | an unexpired lease, or sustained urgent foreground work | background maintenance and optional evaluations yield |
| `DISK_LOW` | free space below your floor | stop creating large files; propose reclaim through the approved process |
| `MACHINE_BUSY` | high load per core, or sustained memory pressure with active swapping | run heavy builds and tests one at a time and add no workers |
| `NORMAL` | all readings are current and none of the four conditions above applies | normal limits |
| `MAINTENANCE_OK` | `NORMAL`, plus spare capacity and enough time since the last maintenance run | bounded maintenance may also run |

Several problem conditions can be true. Record all of them and apply every restriction that matches. Where two limits differ, the stricter one wins.

If local checks also fail, do not call it an external problem. Diagnose the machine.

Require a few good readings before leaving a degraded condition, so behavior does not flip on one sample.

## 3. When the outside network is degraded

- Lengthen retry delays, for example by doubling them, and add random jitter.
- Cap concurrent outside requests with one limit shared by all agents, for example four. Per-agent caps add up.
- Use cached data where it is acceptable, and show its age.
- Defer optional polls.
- Keep local-only work at normal speed.
- Do not restart healthy local services.
- Do not blindly retry a request that may already have changed something. Read the state first.

## 4. Priority leases

A lease states owner, reason, start and expiry. It has a maximum length and expires by itself. Clear it when the work ends. Keep secrets and private project details out of the reason. A lease tells optional work to wait. It does not allow anyone to kill another process or skip a safety check.

## 5. Maintenance-window work

Under `MAINTENANCE_OK`, run only a fixed list of bounded tasks, with a minimum gap between runs. Check posture again between tasks and stop if a problem condition appears. Keep a receipt for each run. A maintenance window does not authorize deletion, deployment or paid calls.

## Output

One line before heavy work: the conditions, the key readings with their age, and what you will do differently.

## Never

- Never restart services because outside requests are slow while local checks pass.
- Never kill another agent's or a person's process to make room.
- Never free space with unreviewed deletion.
- Never treat a missing or stale reading as healthy.

## When to use

- Before starting many parallel agents, a bulk API job or a large build.
- When timeouts rise and the cause is unclear.
- When deciding whether background maintenance should run now.

## How to use

1. Copy the `operating-posture-gate` folder into `~/.claude/skills/` for personal use, or `.claude/skills/` inside a project.
2. Ask Claude Code to use the skill by name.
3. Example prompts:
   - "Use the operating-posture-gate skill before this batch run. Tell me which conditions apply and what limits you will use."
   - "Use operating-posture-gate to work out whether these timeouts are my machine or the outside network before anything is restarted."
