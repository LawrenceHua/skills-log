---
name: sensitive-index-atomic-swap
description: Build a searchable catalog or cache over a sensitive raw source (chat transcripts, tickets, logs with PII) by ingesting only an explicit field allowlist, building into disposable staging, and atomically swapping it live only after a zero-error reconciliation pass — so a half-built or leaky index never goes live and raw sensitive content never enters the derived artifact.
---

# sensitive-index-atomic-swap

Building a local index, cache, or catalog over sensitive raw data (session transcripts, support tickets, logs with personal data) has two failure modes that "just write the index" doesn't guard against: the index accidentally captures raw sensitive content it was never meant to carry, and a crashed or partial build leaves a corrupted or half-populated index sitting where the live one used to be. Both are avoidable with the same two disciplines — ingest through a strict allowlist, and never mutate the live artifact in place.

## The method

**1. Define an explicit field allowlist before writing any ingestion code.** Decide exactly which fields get extracted from the raw source — an ID, a timestamp, a file path, a category tag, a short structured status — and validate every record against that shape as it's parsed. Anything that doesn't validate is skipped and logged as an error, never guessed or coerced in. Raw free-text bodies, message content, or tool output from the source are never copied into the derived catalog; if you need full-text search, index only fields you've explicitly decided are safe to store more broadly than the source itself.

**2. Build into a fresh, disposable staging location, never in place.** Write the new catalog to a new temp file or directory (a scratch SQLite file, a scratch directory) that has no relationship to the live artifact other than a final swap step. A build that fails halfway leaves nothing behind except its own temp files — the live catalog is untouched because the build process never opened it for writing.

**3. Reconcile before promoting.** After the build finishes, check that the record count matches what the source scan actually produced, that zero validation/parse errors occurred, and that any derived cross-references (e.g., a summary record claiming to describe session X) actually resolve to a real record that was ingested this run — not an assumption. Report `coverage`, record counts, and every cross-reference status explicitly; don't infer "looks complete" from the absence of an exception.

**4. Atomically swap only on a fully clean reconciliation.** Only a zero-error, fully-reconciled build gets promoted — via an atomic rename/move, not a copy-then-delete — to replace the live artifact. Any failure at the build or reconciliation stage exits without touching the live catalog and cleans up only its own staging artifacts.

**5. Treat anything pulled in from existing curated material as still sensitive.** If the pipeline also indexes human-written summaries or notes that reference the raw source, index them too, but don't assume they're automatically scrubbed just because a human wrote them — they inherit the same "sensitive local state" handling as the raw source.

**6. Harden the write path itself.** Reject symlinks anywhere in the path chain of state, output, or staging locations — a symlink swapped in after your existence check but before your write is a classic TOCTOU hole that silently redirects output outside the intended directory. Keep state directories and files narrowly permissioned. Give the pipeline read-and-build capability only — never fold a deletion or cleanup-of-originals capability into the same tool that builds the index, so an indexing bug can never cascade into data loss.

**7. Report outcomes from the current build's receipt only.** Label the result `VERIFIED` (clean build, promoted), `BLOCKED` (a required step couldn't run), or `INCONCLUSIVE` (ambiguous/partial result) — never assume a catalog built weeks ago is still an accurate reflection of the source, and never let "it worked last time" stand in for this run's reconciliation numbers.

## When to use

- Building any local searchable index, cache, or catalog over a source containing sensitive raw content — chat/session transcripts, support tickets, medical or financial records, PII-bearing logs — where the derived artifact needs to be safe to query or share more broadly than the source itself.
- Any indexing/caching pipeline that currently writes into the live artifact in place, where you want a crashed or buggy build to be a non-event instead of a corrupted index.
- Auditing an existing ingestion pipeline for the specific gap where raw sensitive fields get copied into a derived artifact "just in case they're useful later."

## How to use

**Install:** copy this folder into `~/.claude/skills/sensitive-index-atomic-swap/` for personal use, or `.claude/skills/sensitive-index-atomic-swap/` inside a project repo. Implement the allowlist and staging/swap logic against whichever storage you actually use (a single SQLite file swapped via atomic rename works for most cases up to hundreds of thousands of records).

**Invoke:**

```
Rebuild our session-history catalog using sensitive-index-atomic-swap — allowlist
only id/timestamp/path/tag fields, build into a temp store, and only swap it live
if reconciliation comes back zero-error.
```

```
Audit this ingestion pipeline against sensitive-index-atomic-swap: is there any
field it copies from the raw source that isn't on an explicit allowlist, and does
a failed build ever leave a partial index live?
```
