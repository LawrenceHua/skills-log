---
name: observable-share
description: Before anything gets shared outward — a report, a dashboard tile, a status post — require three written answers (what's the one thing this says, what live source backs every number, what watches it and fixes it when it breaks), plus a hard word budget and a "stale must look stale" rule.
---

# observable-share

Every shared surface eventually goes stale. The failure mode that actually hurts isn't staleness — it's staleness that looks healthy. A number rendered from a snapshot taken weeks ago, in the same font weight and the same color as a number that refreshed thirty seconds ago, reads as equally trustworthy to whoever's looking at it. Nothing is broken. Nothing alerts. The surface is just quietly lying by omission, and it can do that for weeks before anyone notices.

This skill is a gate to run **before** writing the copy or the component, not a cleanup pass after. Retrofitting a monitor onto something already shipped is how surfaces go stale in the first place.

## The three questions

Answer each in writing before opening an editor. Order matters — answering "what's the source" before "what's the one thing this says" produces a page that's accurate and unreadable.

1. **What is the ONE thing this surface says?** One sentence. If it takes two, the surface is doing two jobs — split it or cut one. Everything else on the surface must support that sentence or get deleted.
2. **What live source is every number wired to?** Every number names a source and a `generated_at`. A number that can't name its source doesn't render.
3. **What watches it, and what does it do when it breaks?** A surface with no monitor will go stale silently. Register the monitor — and its remediation, not just an alert — before the surface ships.

## The freshness rule

- Every number carries **value, denominator, and `generated_at`**. A count without its denominator is a rumor, not a number — "28,645 findings" can quietly mean "1,431 events re-graded 20x," and the bare count overstates reality by an order of magnitude.
- Stale renders **visibly stale**: a pill, a dimmed value, an explicit date. The viewer must be able to tell at a glance, without hovering.
- If a number genuinely can't be live, render its real date and no live indicator. Honest beats fake-live.
- `generated_at` comes from the **source**, never from `now()` at render time. A timestamp the renderer writes proves the renderer ran — it says nothing about whether the underlying data is current.
- Prefer the payload's own embedded timestamp over file mtime. A freshness check that a plain file-touch can satisfy isn't a freshness check.

## The word budget

Show, don't tell — these are budgets, not suggestions:

| Surface | Budget |
|---|---|
| Section intro | ≤ 40 words |
| Card / tile | ≤ 15 words |
| A status post to chat/email | ≤ 80 words, one claim, one link |
| Chart or table | a caption, not a paragraph |

Prefer a visualization to a sentence, a number to an adjective, a hover to a second paragraph. If the copy is explaining what a chart already shows, cut the copy, not the chart. Never put a count in a title or label — "Gates" not "14 gates." A count in a value can go stale visibly; a count baked into a label goes stale silently, because nothing renders it as data.

## Monitors that fix, not monitors that shout

A monitor earns its place by staying quiet most of the time:

- **Post only on change** — a verdict flipping, an edge breaking or healing. Never a heartbeat that repeats what the last post already said; repetition trains everyone to ignore the channel.
- **One periodic heartbeat regardless of change**, so silence can never be mistaken for health. A watcher and the thing it watches can share a failure domain — both go quiet together, and quiet reads as fine, for days, unless a heartbeat forces a signal either way.
- **Auto-remediate what's safely reversible**: restart a dead job, re-run a failed publish, re-bootstrap an unloaded scheduled task, refresh a stale cache. Cap the retry attempts and log every one.
- **Never auto-remediate anything outward or destructive**: posting, sending, deploying, deleting, spending. Those always escalate to a human.
- **Escalate on repeat.** The same fault firing twice inside a window means the remediation isn't working — say so instead of silently retrying forever.

## Registering a surface

Keep a small registry (one JSON file is enough) with one entry per shared surface:

```json
{
  "id": "weekly-ops-summary",
  "what_it_says": "Is the pipeline healthy right now?",
  "url": "https://example.com/ops",
  "sources": [
    {"stat": "error rate", "from": "/api/metrics", "refresh_s": 60}
  ],
  "monitor": "scripts/watch_ops_surface.py",
  "remediation": "re-run the publisher; escalate after 2 consecutive failures",
  "word_budget": 40
}
```

A checker script reads the registry and fails on: a stat with no named source, a source with no refresh mechanism, a surface with no monitor, or copy over budget.

## Procedure

1. Answer the three questions in writing before opening an editor.
2. Register the surface.
3. Build it — wire every number through the source named in the registry, not a value typed in by hand.
4. Run the checker. Fix what it reports.
5. Confirm the monitor actually fires: break the source deliberately, watch the monitor notice, watch the remediation run. A monitor that's never been observed catching anything is decoration, not a monitor.
6. Only then share the link.

## Anti-patterns (all worth checking for before you ship)

- A number rendered from a file committed weeks ago, styled identically to a live one.
- A tile whose label carries a count, so the label silently goes wrong the moment the count changes and nothing can detect it.
- A "live" panel that renders nothing when its feed is unavailable — so a broken feed and a quiet-but-healthy feed look identical. Render the broken state explicitly.
- A monitor that posts on every run, training everyone to ignore it.
- A dashboard that's grown a paragraph of prose above every chart.
- A publisher that writes a local file and calls the job shipped. Local isn't live — probe the actual URL.

## When to use

- Before writing copy or a component for anything that will be read by someone other than you: a report, a dashboard, a status post, a shared doc with numbers in it.
- When a shared surface has drifted stale without anyone noticing, and you want to know why nothing alerted.
- Reviewing an existing dashboard or report before trusting the numbers on it.

## How to use

**Install:** copy this folder into `~/.claude/skills/observable-share/` for personal use, or `.claude/skills/observable-share/` inside a project repo.

**Invoke:**

```
Before I build this status page, run me through observable-share — help me answer
the three questions and design the registry entry.
```

```
Apply the observable-share freshness rule to this dashboard — which numbers are
missing a generated_at, and which ones would look identical whether they're
30 seconds or 30 days old?
```
