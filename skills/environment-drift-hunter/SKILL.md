---
name: environment-drift-hunter
description: Runs a scheduled and on-demand battery of deterministic, no-LLM checks over a local dev/automation setup and surfaces a ranked, evidence-backed finding list with concrete fixes and an autofix-safe flag.
---

# environment-drift-hunter

Any nontrivial local setup — several repos, a handful of scheduled jobs, hooks, a personal dashboard, notes that double as memory — drifts silently over time. Docs stop matching code, jobs stop working, permissive defaults creep in, secrets sneak into commits. Normally you find this through pain: something breaks, then you go hunting. This flips the order — a fast, deterministic scanner that runs on a schedule and on demand, so you find the drift before it finds you.

## The method

The scanner never calls an LLM — every check is mechanical (grep, stat, process list, git plumbing), which keeps it free and fast enough to run every couple of hours without anyone noticing the cost.

### Check categories

| Category | What it looks for |
|---|---|
| Doc-vs-reality drift | A README/doc claim that contradicts what the code or config actually does |
| Zombie/orphaned processes | High-resource processes whose owning app hasn't been touched in a long time |
| Orphan scheduled jobs | A background job writes a file nothing has read in a long time — pure waste |
| Silently failing jobs | The same scheduled job failing N runs in a row, unnoticed |
| Broken symlinks / dead hardcoded paths | A symlink or config path pointing at something that no longer exists |
| Referenced-but-unset env vars | Code/config reads an env var that's never set anywhere reachable |
| Broken hook/automation chains | A configured hook command that no longer exists or isn't executable |
| Stale git worktrees / dead branches | Worktrees or branches that are merged or abandoned but still sitting around |
| Security-default drift | A config falls back to a permissive/insecure/debug-only default |
| Unauthenticated exposure | Anything sensitive reachable without auth |
| Credential-shaped strings in git history | Committed strings that look like keys, tokens, or passwords |
| Unmasked sensitive data in logs | Local log files printing secrets or PII in the clear |
| Stale claims in personal notes/memory | A note asserts something exists that a grep proves is gone |
| Disk pressure | Oversized logs, caches, temp clutter |

### Finding output contract

Every finding carries the same five fields, so findings from every category stack into one ranked list:

- **severity** — how bad if ignored
- **evidence** — the specific file/path/log line/process that proves it
- **category** — which row of the table above it came from
- **fix** — one concrete line, not a vague suggestion
- **autofix_safe** — `true` or `false`

### Autofix-safe vs recommend-only

| autofix_safe = true | autofix_safe = false (always recommend-only) |
|---|---|
| Delete a stray backup/temp file | Modify production/application code |
| Remove a zero-diff stale worktree | Push or force-push to a remote |
| Prune a dead branch with no unmerged commits | Rotate or revoke a credential |
| Clear a rotated log the app no longer reads | Change a security default in a live config |
| Remove an orphan job's dead output file | Kill a process you can't confirm is safe to kill |

The line is reversibility: autofix-safe actions are trivially undoable and touch nothing another system depends on. Anything that could break a live path, leak further, or isn't cleanly reversible stays a recommendation with the fix spelled out, never an automatic action.

### Delta-gated scheduling

Run on a rolling schedule (every couple of hours is reasonable) plus on demand. Each run diffs its finding set against the last surfaced set, and only emits output when the SET actually changed — a new finding appeared, one got fixed, or a severity changed. A scan that reports the same ten findings every two hours trains you to ignore it; a scan that only speaks up when something's different keeps every alert worth reading.

## When to use

- You maintain more than one repo, job, or hook chain and haven't audited them together in weeks.
- Something just broke and you want to know if it was drift — then confirm the rest of the setup didn't drift too.
- Before an audit, a handoff, or sharing your setup with someone else.
- As a standing background job, not just a one-off cleanup pass.

## How to use

**Install:** copy this folder into `~/.claude/skills/environment-drift-hunter/` for personal use, or `.claude/skills/environment-drift-hunter/` inside a project repo.

**Invoke:**

```
Run environment-drift-hunter over my setup and give me the ranked finding list —
flag which ones are safe to autofix.
```

```
It's been a couple weeks since the last scan. Do a full environment-drift-hunter
pass, only show me what changed since last time, and autofix the safe ones.
```
