---
name: doc-iterate
description: Process inline review-comment markers (e.g. "[NAME: ...]") left in shared Markdown docs — apply the requested edit in place, preserve a history of what changed, and flag anything that contradicts an earlier decision instead of guessing. Use for async doc review between collaborators without a full comment/suggestion system.
allowed-tools: [Read, Write, Edit, Bash, Grep]
---

# doc-iterate

A lightweight async-review protocol for shared Markdown docs (specs, briefs,
runbooks, FAQs) when you don't have — or don't want to force everyone into —
a heavyweight commenting tool. Reviewers leave inline markers directly in the
file; a pass (automated or on-demand) applies the non-contradictory ones,
preserves what was said, and escalates anything genuinely ambiguous instead
of silently resolving it.

## When to use

- Two or more people are iterating on the same living doc (a PRD, a runbook,
  a decision log) and you want a lower-friction alternative to a full
  suggestion/comment workflow.
- You want doc edits to be **auditable** — every change traceable to a named
  comment, not silently rewritten.
- You want a periodic or on-demand pass that applies small edits but refuses
  to auto-resolve genuine disagreements.

**Skip it for:** one-off single-author docs, anything that needs a full
structural rewrite (that's a separate, deliberate pass — not a marker), or
docs where the "history" trail doesn't matter.

## The marker convention

Use HTML-comment syntax so markers are invisible in rendered Markdown but
easy for a script (or you) to find — and so they don't collide with prose
that merely *talks about* the convention:

| Marker | Use |
|---|---|
| `<!-- REVIEWER_A: comment text -->` | A substantive edit request, reword, or disagreement, placed inline near the relevant paragraph |
| `<!-- REVIEWER_A-NOTE: comment text -->` | A big-picture comment that doesn't map to one paragraph — put it at the end of the section |
| `<!-- REVIEWER_B: comment text -->` | A response or counter-proposal from a second reviewer |
| `[CONTRADICTION: A vs B]` | Inserted by the process when a marker conflicts with an earlier documented decision — needs a human call, never auto-resolved |
| `[FLAGGED: reason]` | Inserted when a marker can't be safely applied automatically (e.g. it requires a code change, not a doc edit) — escalate it, don't guess |

Use real names or initials in place of `REVIEWER_A`/`REVIEWER_B`. No nested
markers — if you're replying to a marker, add a separate marker rather than
nesting comment syntax.

## The process (per pass)

1. **Pull the latest version** of the tracked doc(s) (e.g. `git pull
   --rebase` if it lives in a repo).
2. **Find every marker** across your tracked-files whitelist (see below —
   don't scan the whole repo; scope it deliberately).
3. **For each marker, apply the requested change in place**, then:
   - Strip the marker once applied.
   - Append a one-line entry to an append-only history block at the end of
     the file (or a sibling `CHANGES.md`) — never lose the original comment
     text, even after it's "resolved."
   - If the requested change **contradicts** an earlier documented decision
     in the same doc, do NOT silently pick a side — replace it with
     `[CONTRADICTION: A vs B]` and leave both positions visible.
   - If the requested change actually requires a **code** change (not just
     prose), don't touch code from this pass — mark it `[FLAGGED: needs
     code change]` and route it to wherever you track follow-up work (an
     issue tracker, a TODO list).
4. **Commit the updated doc(s)** back to the repo (if applicable).
5. **Report a one-line summary**: "Iterated N docs · X comments applied · Y
   flagged · Z contradictions" to whatever channel your team actually
   watches (chat, email, a PR comment) — keep it short.

## Tracked-files whitelist (keep this explicit)

Only run this over a small, explicit list of files — not everything with a
marker in it. This keeps the blast radius small and avoids scanning archived
or historical material. Maintain the list wherever you keep the script's
config (a `TRACKED_FILES` list, a small YAML/JSON config, whatever fits your
project).

## Failure modes and how to handle them

| Mode | Behavior |
|---|---|
| Push conflict | Rebase and retry once; if it still conflicts, don't force-push — leave it unapplied and flag it |
| A sync/publish step fails (e.g. mirroring to a wiki) | Skip that step for this cycle; keep the primary commit; note "sync skipped" in the summary |
| Marker requires a code change | Don't touch code from this pass — route to your issue tracker instead |
| Zero markers found | Skip the cycle entirely — no commit, no notification |
| The LLM/contradiction-check step is unavailable | The core apply-a-marker step is mostly deterministic; skip only the "detect subtle contradictions" step, which is the one part that benefits from a model |

## Discipline that keeps this from becoming bloat

- **Small cycles.** If a single marker implies more than an hour or two of
  real work, route it to your issue tracker — don't do it inline.
- **Tracked files only** — the explicit whitelist above.
- **Readable diffs.** No silent restructuring; a real restructure is a
  separate, deliberate pass with its own review.
- **History is append-only.** Never lose the original comment, even once
  it's been acted on.
- **Only publish/sync on success.** Don't show collaborators a half-broken
  render.

## How to use

**Install:** copy this folder into `~/.claude/skills/doc-iterate/` for
personal use, or `.claude/skills/doc-iterate/` inside a project repo so
teammates get it too.

**Invoke** by asking directly, or via `/doc-iterate` where your setup
supports named invocation:

```
Run doc-iterate over docs/PRD.md and docs/RUNBOOK.md — apply any
[REVIEWER: ...] markers you find, flag contradictions, and give me a
one-line summary of what changed.
```

```
Dry-run doc-iterate on the specs/ folder — show me what markers you'd
apply and what you'd flag, but don't commit anything yet.
```
