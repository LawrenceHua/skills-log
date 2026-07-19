---
name: agent-observability-bundle
description: Build a fully-local, zero-cost observability bundle for an AI coding agent — a status line, a hallucination-blocking turn-end hook, and an optional periodic quality grader — so you can see what the agent is doing and catch unverified "done" claims before they cost you.
---

# agent-observability-bundle

Most AI coding agent setups run blind: you can't see the context window filling up, you can't tell if "tests pass" was actually verified, and quality drift is invisible until it's a pattern. You can build all three checks yourself, locally, for free — no paid service, no external API, three small scripts wired into the tool you already use.

## The three components

| Component | What it checks | Cost |
|---|---|---|
| Status line | Active model + effort level, context window % full (and whether compaction fired), session duration, running token/cost totals (day/month), lines changed, current working directory | Near-zero — cache expensive lookups (e.g. monthly token aggregation) in a background-refreshed file instead of recomputing on every render |
| Hallucination gate | Scans the just-written response for completion-claim language ("tests pass", "deployed", "done", "fixed", "verified") and blocks the turn from ending if no tool call/command output in the transcript backs up the claim | Free — local pattern matching, or a cheap/small local model for fuzzier cases |
| Quality grader | Opt-in, slower check: a cheap judge model scores the session on goal-completion, overall quality, and unsupported-claim rate; appends to a trend file | Cheap — runs once per session-end or on-demand, not per turn |

### 1. Status line

Write a script your terminal/agent tool invokes on every render. It should surface, at minimum:
- model + effort/reasoning level currently active
- context window fill percentage, plus a marker if compaction has already run this session
- wall-clock session duration
- running token and cost totals for the day and month
- lines changed so far
- current working directory, formatted so it's clickable or copy-pasteable in your terminal

Anything that requires scanning multiple files or aggregating history (monthly totals, for example) should be computed by a separate background job that writes its result to a small cache file — the status line script itself should only ever do cheap reads, since it fires on every single render.

### 2. Hallucination gate

Wire a hook into your agent tool's turn-end / stop event. On every turn:
1. Pull the response text the agent just wrote.
2. Match it against a list of completion-claim phrases ("tests pass", "deployed", "fixed", "verified", "done", "shipped", etc.).
3. If a match is found, scan backward through the transcript for a tool call or command output that actually supports the claim (a test run, a build log, a deploy confirmation).
4. If no supporting evidence exists, block the turn from ending and force the agent to either produce the evidence or downgrade the claim (e.g. to "implemented, not yet verified").

Keep this local and pattern-based first — it needs to run on every turn, so it has to be cheap. Only reach for a small model call if plain pattern matching produces too many false positives/negatives for your workflow.

### 3. Periodic quality grader

This one is opt-in and slower, so it doesn't need to run on every turn — once per session-end, or via a manual command, is enough. Feed the session transcript to a cheap judge model and have it score:
- goal completion (did the session actually finish what it set out to do)
- overall response quality
- rate of unsupported/uncorroborated claims

Append the result to a trend history file so declining quality shows up as a visible line over weeks, not as a surprise after it's already a pattern.

## Idempotent install

Ship one installer script that:
1. Copies the status line script, the gate hook, and the grader script into place.
2. Backs up the existing tool config (settings/hooks file) before touching it, so the install is reversible.
3. Wires the hook(s) into that config.
4. Tells the user to restart their session to pick up the change.

Re-running the installer should be safe — it should detect an existing install, skip re-copying identical files, and never duplicate hook entries in the config.

## Local logs

Everything stays on disk, nothing leaves the machine:
- `~/.your-tool/logs/gate-decisions.jsonl` — one line per gate check (blocked/passed, matched phrase, evidence found or not)
- a JSON/Markdown quality report written per session by the grader
- a trend history file the grader appends to, so you can chart quality over time

## When to use

- You're running an AI coding agent daily and have no visibility into context usage, cost, or session length
- You've been burned by an agent claiming "tests pass" or "deployed" when neither actually happened
- You want to know if agent output quality is drifting downward before it becomes a recurring problem
- You want observability without adopting a paid monitoring/observability SaaS product

## How to use

**Install:** copy this folder into `~/.claude/skills/agent-observability-bundle/` for personal use, or `.claude/skills/agent-observability-bundle/` inside a project repo.

**Invoke:**
```
Set up the agent observability bundle — status line, hallucination gate, and periodic quality grader — for this project.
```
```
Add a turn-end hook that blocks completion claims like "tests pass" or "deployed" unless the transcript has a matching tool call.
```
