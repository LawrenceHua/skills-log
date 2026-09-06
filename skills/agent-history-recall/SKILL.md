---
name: agent-history-recall
description: Build a queryable local catalog of every past AI-agent session, decision, and note, then answer "what did we decide about X / why does Y work this way" via hybrid search over the catalog instead of re-reading raw transcript trees or guessing from model memory.
---

# agent-history-recall

Once you've run AI-agent sessions for months, the honest history of a project lives scattered across hundreds of transcripts, memory files, and commit messages — nobody re-reads all of that to answer "why does this work this way." Two bad defaults fill the gap: the model guesses from its own training-time memory (confidently, often wrong), or a human/agent greps through a random subset of old files and treats whatever surfaces as the answer. Neither is search — both are luck.

## The method

Treat your own agent history as a corpus to index, not an archive to re-read.

**1. Catalog every session as it closes.** Whenever an agent session, decision, or durable note ends, append one record to a flat catalog: source (which tool/CLI produced it), a partition/project tag, a class (session transcript, standalone decision, owner rule, incident writeup...), a timestamp, and the searchable text itself. One record per event — never one giant merged file.

**2. Index for hybrid search.** Build both a full-text index (for exact terms — error strings, flag names, file paths) and a vector/embedding index (for paraphrased questions — "why did we pick X" when the record says "chose X because"). A hybrid query that merges both beats either alone: full-text catches literal strings an embedding smooths over; vector search catches intent when the wording doesn't match.

**3. Query narrowly before broadly.** Give the query interface real filters, not just a free-text box:
   - a partition/project scope, so a question about one codebase doesn't surface noise from another
   - a class filter, so "what did we decide" doesn't return raw session transcripts when you want the decision records
   - a date range, so you can time-box to "since the last release" or "before the migration"
   - a direct ID lookup, for when you already know which record you want

   Start narrow (partition + class + date range), widen only if the narrow query comes back empty.

**4. Read-only, no generation on the hot path.** The catalog is queried, never written to, by the recall step — no network calls, no on-the-fly embedding generation, no LLM summarization of the results by default. That keeps it fast and cheap enough to invoke on every "what did we decide" question instead of being a heavyweight fallback.

**5. Say "not found" plainly.** If the catalog returns nothing for a query, that is itself the answer — don't fill the gap with a plausible-sounding guess from general training knowledge. A wrong confident answer is worse than "I don't have a record of that."

## Minimal reference shape

A serviceable version of this needs almost no infrastructure:

- **Storage:** a single SQLite file. One table: `id, source, partition, class, ts, text, embedding BLOB`.
- **Full-text:** SQLite's FTS5 virtual table over `text`.
- **Vector:** any local embedding model, stored as a BLOB column; cosine-similarity scan is fast enough up to tens of thousands of rows without a dedicated vector DB.
- **Ingestion:** a small script that watches your session-log directory (or hooks into your agent tool's session-end event) and appends one row per completed session/decision.
- **Query CLI contract:** `recall "<question>" [--partition NAME] [--class CLASS] [--since DATE] [--until DATE] [--mode hybrid|fts|vector] [--k N]`, returning the top-K records as JSON (one record per line) so it composes with other tooling.

This is deliberately small enough to build in an afternoon and grows in place as your history grows — the payoff compounds the longer you keep feeding it.

## When to use

- Answering "what did we decide about X" or "why does Y work this way" when the answer lives in your own project history, not in the current code.
- Before repeating a decision you suspect you already made and rejected once.
- Onboarding a new session (or a new agent tool) onto a long-running project without re-reading every prior transcript by hand.
- Any time you'd otherwise ask an LLM to guess from general knowledge about a decision that is actually project-specific and already recorded somewhere.

Not for questions the current code already answers directly — read the code for that; reserve recall for the "why," not the "what."

## How to use

**Install:** copy this folder into `~/.claude/skills/agent-history-recall/` for personal use, or `.claude/skills/agent-history-recall/` inside a project repo. If you don't already have a session-history catalog, build the minimal SQLite version above first — the skill is the search discipline, and it needs a corpus to search.

**Invoke:**

```
Use agent-history-recall to check what we already decided about retry
backoff before you propose a new policy.
```

```
Query agent-history-recall scoped to this project, class=decision,
since 3 months ago, for anything about the auth rewrite.
```
