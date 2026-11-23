---
name: assumed-healthy-contradiction-hunt
description: Hunt for systems that look green but are broken — health endpoints that return 200 over a dead dependency, shadow copies of tools, stranded message inboxes, zombie processes, orphaned locks — by scanning read-only, then trying to refute every hit before anyone edits anything.
---

# Assumed-healthy contradiction hunt

Healthy-looking systems fail in the gaps between instruments. A health endpoint returns `200` while the dependency behind it is down. A scheduler runs a stale copy of a script instead of the one you fixed. Messages pile up in an inbox nobody polls. A test fixture process has been running for nine days. A runner ticks cleanly and launches nothing. Nothing alerts, because every instrument is reading its own layer and each layer says "fine".

This skill is a proactive, read-only sweep for those contradictions, followed by a refute-first verification step so a suspicion becomes either a proven fact or a clean refutation before anyone changes code.

## When to use

- Someone asks "what looks fine but isn't?", "what are our blind spots?", or "audit what we assume is healthy".
- After an incident where every dashboard stayed green.
- Before trusting a long-running automated setup you did not watch over the last few days.
- Periodically (not on a tight loop) for any machine or service that runs unattended agents, schedulers, or background workers.

Do not use it for designing the observer of one specific scheduled job (build an independent watchdog for that), or for measuring performance regressions (use a baseline-and-guard health check).

## The method: four stages

### 1. Scan (read-only, cheap, deterministic)

Run fixed checks that need no model judgment. Keep the scan under a few seconds so it is safe to repeat. Write a small content-free receipt (timestamp, check names, counts, pass/fail) and never record message bodies, tokens, or URLs with credentials. Exit codes should be strict: clean, suspicions found, and hard alert are three different codes; a missing or malformed invocation refuses loudly rather than silently doing nothing.

Run these seven check classes:

| Check | What it catches | How to look |
|---|---|---|
| Shadow copies | A second copy of a tool or script outside the canonical location that a scheduler or hook actually runs | Resolve the real path of what each scheduled job and hook invokes; compare byte size and hash against the canonical copy; flag jobs pointing into build or temp directories |
| Green lies | A health endpoint reporting OK while a nested field says otherwise | Fetch the health payload and read every nested field: `up`, `ok`, `healthy`, `over_capacity`, `degraded`, a per-dependency status. A top-level `200` or `"status": "green"` is not the verdict |
| Zombie trees | Processes older than a day living in temp directories (test servers, `sleep`-forever helpers, night-run leftovers) | List processes with start time and working directory; flag old ones whose parent is gone |
| Mailbox split | Messages addressed to an identifier that no live consumer polls | If sessions are addressed by one id but consume by another (a wrapper pid versus a session uuid), compare pending rows per address against the address the live consumer actually reads |
| Loops with zero output | A runner that ticks but launches nothing, or a scorecard that has not updated | Compare "last run" timestamps and launch counters with expected cadence; a rising refusal count with zero launches is a defect, not quiet |
| WAL and orphan writers | A database write-ahead log growing without checkpoint, or file leases whose owner has gone | Check WAL size against a threshold (for example 64 MB); list leases past expiry |
| Peer pulse | A peer agent or worker that is registered but has stopped heartbeating | Compare last-heartbeat age with the cadence it promised |

### 2. Falsify (default REFUTED)

Never promote a suspicion on the scanner's summary alone. For each hit, send a read-only scout (or do it yourself in a fresh pass) whose default stance is "this is a false positive". The scout reads raw bytes, not summaries:

- the actual health payload, not the dashboard tile;
- the scheduler definition as parsed, not as remembered;
- the database tables opened read-only;
- the process table, not a log line about processes.

If the retained evidence does not contain the field that decides the question (a summary file that dropped per-test stderr, for example), record the finding as `INCONCLUSIVE`. Do not guess.

### 3. Deepen only when a pattern is confirmed

If confirmed suspicions share a structural cause — regex screening of trusted templates, addresses that change when a wrapper restarts, health wrappers that swallow child status, shadow binaries after a rebuild — then research the pattern before proposing an architecture change. A single hit gets a fix; a repeated shape gets a design change.

### 4. Steer, stage, and hand off

Route each verified finding to the session or person who owns the affected surface. Claim a narrow write lease before editing anything shared. Log the fix as "shipped, not verified" until a fresh reviewer re-runs the raw probe that originally exposed the contradiction. Hunting itself stays read-only: do not delete files, kill processes, or deploy as part of the scan.

## Traps that repeat

1. **Do not address a session by its wrapper process id** when its consumer polls by session uuid. Mail sent to the pid is stranded silently.
2. **Do not trust a top-level `200` or `status: green`.** Always read nested fields. A payload can say green while `up: false` and `over_capacity: true`.
3. **Do not assume a scheduler runs the canonical copy of a tool.** Resolve the real path and compare size or hash against the one you maintain.
4. **Do not parse an append-only JSON-lines file with a line-based parser** when a producer may have concatenated two objects without a newline; stream-decode object by object.
5. **Do not run a regex privacy or safety screen over your own static prompt templates.** Separate trusted templates from untrusted payloads, or the screen will refuse your own brief and the runner will log zero launches with a rising refusal count.
6. **Do not let the scanner write anything but a content-free receipt.**

## Triage routing

| Finding | Default next step |
|---|---|
| Shadow copy | Fix the scheduler definition to point at the canonical copy, or retire the build shadow under a lease |
| Green lie | Inspect the failing child service; fix the child, then fix the wrapper so it propagates child status |
| Zombie tree | Confirm it is parentless with the process table, then stage cleanup behind the owner's approval |
| Mailbox split | Update the router or peer manifest to the consumer's real address and re-deliver |
| Zero-launch loop | Hand to the owning loop with the raw receipt |
| Oversized WAL or expired lease | Checkpoint safely or release the lease |
| Silent peer | Confirm it is really stalled before dispatching work that depends on it |

## Honesty gates

- A scan that finds nothing proves only that these seven checks found nothing. State that.
- Include one negative control per check (a synthetic bad case the check must catch) so a scanner that cannot fail is not trusted. Run those controls whenever the scanner changes.
- Any fix prompted by a hunt carries a "shipped, not verified" label until someone other than the fixer reproduces the original probe and sees it pass.

## How to use

1. Copy this folder into `~/.claude/skills/` for personal use, or into `.claude/skills/` inside a project.
2. Ask Claude Code to use the `assumed-healthy-contradiction-hunt` skill by name.
3. Example prompts:
   - "Use the assumed-healthy-contradiction-hunt skill to sweep this machine's scheduled jobs and local services. Scan read-only first, then try to refute each hit before proposing a fix."
   - "Our status page was green during the outage. Use the assumed-healthy-contradiction-hunt skill to check whether any health endpoint hides a failing dependency, and report which findings are proven versus inconclusive."
