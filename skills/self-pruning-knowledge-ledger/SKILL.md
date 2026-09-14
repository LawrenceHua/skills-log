---
name: self-pruning-knowledge-ledger
description: Keep an always-loaded rules/lessons file from growing without bound by having a pipeline append one-line distilled entries, snapshot the full file before every prune, and tier older entries into on-demand deep-reference files instead of re-loading the whole history every session.
---

# Self-Pruning Knowledge Ledger

An always-loaded rules or lessons-learned file (a system prompt addendum, a
`CLAUDE.md`-style file, a project memory index) tends to grow forever once
something is appending to it automatically — every session pays the token
cost of every lesson ever learned, even the ones from months ago that only
matter for a narrow edge case. This method keeps the file useful and capped
without ever discarding the underlying knowledge.

## The method

**1. Split into two tiers from day one.** A small **live** file that's always
loaded, and one or more **archive** files that are only read on demand. Never
let a single file try to be both.

**2. Append new lessons as exactly one line each.** A short dated identifier
comment, a bolded title, and one sentence stating the rule — not a paragraph,
not an example, not a "why" (link out to the source decision/incident if you
need the why). If a new lesson doesn't compress to one line, it's not ready
to go in the ledger yet.

**3. Snapshot before you prune, never after.** Before the live file is
edited to remove anything, copy the complete current live file verbatim to a
dated archive path. Only treat the prune as safe once that copy exists —
this makes "we can always regenerate the archive from the live file" false
in the other direction, but "we can always recover what the live file used
to say" true, which is the property you actually want.

**4. Prune by recency, not by judgment call.** Keep the most recent N entries
(pick N to fit your token budget, e.g. 60–100 one-liners) inline in the live
file. Move everything older into a dated or topic-named deep-reference file,
and leave exactly one pointer line in the live file naming what it covers and
when to read it ("read `reference/rules-2026-07.md` when you need the July
rules covering X, Y, Z"). Don't summarize the deep-reference file's contents
in the live file — that defeats the point of moving it out.

**5. Automate the whole loop.** Discipline that depends on remembering to
prune manually decays. Write a small script or pipeline step that appends
new entries and runs the snapshot-then-prune cycle automatically once the
live file crosses its size threshold. Record in the file's own metadata
which process owns it, so a human editing it by hand knows they're working
alongside automation, not instead of it.

**6. Inject a relevant subset where you can, but keep the live-file cap as
the floor.** If your loading mechanism supports it (a hook, a router, a
retrieval step), prefer showing only the entries relevant to the current
prompt instead of the whole live file every time. But don't rely on that
alone — even the "relevant subset" mechanism needs a bounded live file to
select from, so keep steps 1–4 regardless of whether you ever build routing.

**7. When migrating an existing giant file into this pattern, log the
handoff.** Note the original size and the date it moved, in the new file's
own metadata. Six months later, nobody should have to guess why an old
decision references content that isn't inline anymore.

## When to use

- An assistant's always-loaded system prompt, rules file, or project memory
  index has grown large enough to burn meaningful context on every turn, and
  it keeps growing because something (a pipeline, a habit, a teammate) keeps
  appending to it.
- You want lessons learned to accumulate indefinitely without ever forcing a
  choice between "keep everything inline forever" and "periodically delete
  old lessons and lose them."

## How to use

**Install:** copy this folder into `~/.claude/skills/self-pruning-knowledge-ledger/`
for personal use, or into `<project>/.claude/skills/` to share it via version
control.

**Invoke:**

```
This rules file has grown to N thousand tokens and gets loaded every session.
Use self-pruning-knowledge-ledger to redesign it: cap the live file, snapshot
before pruning, and split older entries into a deep-reference file.
```

```
Set up the automation so every time we log a new lesson learned, it gets
appended as a one-line ledger entry, and the file auto-prunes to the newest
80 entries once it crosses budget — following self-pruning-knowledge-ledger.
```
