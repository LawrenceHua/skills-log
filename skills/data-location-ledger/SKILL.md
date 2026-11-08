---
name: data-location-ledger
description: Keep an append-only map of where files and datasets live across disks and cloud, consult it before scanning any disk, and write intent before every move, upload or delete.
---

# Data location ledger

Searching disks to find "where did that go" is slow, can freeze tools on protected folders, and still cannot tell
you why the data exists or how to get it back. A small append-only event log answers those questions and stays true
only if every move, upload and delete is recorded.

## The ledger

One JSON-lines file, append-only (for example `~/.local/share/data-ledger/events.jsonl`). One event per line:

```json
{"ts":"2026-01-01T00:00:00Z","actor":"agent-a","action":"intent|move|upload|delete|note",
 "path":"~/projects/old-export","dest":"/Volumes/Archive/2026-01-01/old-export",
 "bytes":123456789,"sha256_manifest":"<manifest file>","receipt":"<file proving it>",
 "contains":"what it is","meaning":"why it exists","owner":"personal|employer|client|unknown",
 "intent_id":"<id of the prior intent>","failed":false}
```

Rules for the file itself:

- Never edit or reorder past lines. To correct a wrong fact, append a newer event for the same path; readers take
  the newest.
- Carry paths, sizes and hashes only. Never put secrets, file contents or environment values in any field.
- A derived index (latest event per path) can be regenerated at any time; the log is the source of truth.

## 1. Ask before you search

Look the path up in the ledger (a `grep` of the log or a small script that folds it to the latest event per path).
Interpret the result:

| Result | Meaning | Do |
|---|---|---|
| Found | `dest` of the newest event is where it is now | use it; confirm the path exists |
| Not registered | the ledger only knows what was recorded | do ONE bounded search (explicit directory, `timeout`, `| head`), then record what you found |
| Registered but missing | broken trail, dangling symlink, unmounted disk | stop and report; do not guess a new location |
| Restricted owner (`employer`, `client`) | the data belongs to someone else | show the location only; do not move, upload or delete |

"Not registered" never means "does not exist". An unmounted external disk means "not checked": mount it and ask
again.

## 2. Record every destructive step, intent first

```sh
# 1. write the intent BEFORE acting; keep its id
echo '{"ts":"...","actor":"me","action":"intent","verb":"delete","path":"<path>","intent_id":"i-001"}' >> events.jsonl
# 2. do the action after its own safety gates (liveness check, backup, manifest compare)
# 3. record the outcome, pointing at the intent and the proof
echo '{"ts":"...","actor":"me","action":"delete","path":"<path>","intent_id":"i-001","bytes":123,"receipt":"<file>"}' >> events.jsonl
```

- **Move:** copy, hash both sides into manifests, compare, record the `move` with the manifest, and only then remove
  the source.
- **Upload:** the source stays; record `action: upload` with the remote destination.
- **Failed step:** record it with `"failed": true`; it must change no location.
- **Found something by search:** record a `note` with `contains`, `meaning` and `owner`.

Audit rule: any `delete` or `move` with no earlier matching `intent` is a defect. Check with a short script that
joins on `intent_id`.

## Never

- Never scan large or protected folders (`find` or `grep -r` over external volumes, home documents, library folders)
  before consulting the ledger; a scan into a protected folder can freeze the whole tool.
- Never record a step that did not happen: a false fact survives in an append-only log until a newer event replaces it.
- Never move, upload or delete data whose owner is employer or client; the owner decides.
- Never delete without a prior intent event.
- Never let an agent infer `owner: personal`. Infer restricted owners from names if you like; personal must be said
  by a person.

## Verify

- Look up a path you just moved: the newest event shows the new location, the older event shows where it came from,
  and a restore command (a copy from `dest` back to `path`) is obvious from the record.
- Run the audit join: zero deletes or moves without an intent.

## When to use

- Someone asks "where did that folder go" or "do we still have a copy".
- Before any `find`, `grep -r` or `du` over several disks.
- Before and after moving, archiving, uploading or deleting data.

## How to use

1. Copy this folder to `~/.claude/skills/data-location-ledger/` (personal) or
   `.claude/skills/data-location-ledger/` inside a project.
2. Ask Claude Code to use the `data-location-ledger` skill by name.

Example prompts:

- "Use data-location-ledger to set up the event log, then record that I moved `~/old-datasets` to the external disk
  with a manifest."
- "Where did last year's export go? Use data-location-ledger to check the ledger before searching any disk."
