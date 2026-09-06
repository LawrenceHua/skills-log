---
name: architecture-decision-records
description: Capture architectural decisions as structured ADRs (Michael Nygard format) the moment they're made — auto-detects decision moments, extracts context/alternatives/consequences, and only ever writes a file after explicit user approval, maintaining a version-controlled index.
---

# architecture-decision-records

"Why did we choose X over Y?" is a question that should have a one-file answer. Without a habit of capturing decisions at the moment they're made, the answer ends up scattered across commit messages, chat history, and memory nobody trusts a year later. This captures the decision in structured form right when it happens, gated on explicit approval so nothing gets written without a human actually reading and agreeing to the draft.

## The method

**1. Detect the decision moment.** Trigger on: explicit user phrasing ("let's record this decision," "ADR this"), the user choosing between named alternatives (a framework, library, pattern, or architectural approach), the user saying "we decided to...", the user asking "why did we choose X," or a planning pass that surfaces multiple options and a chosen one.

**2. Gate initialization on consent.** If no ADR directory exists yet, ask before creating one — "this project has no ADR directory; should I create it with an index and a template?" Never create the directory or its first file without an explicit yes.

**3. Extract the decision in structured form.** For each detected decision, pull out:
   - **Title** — a short noun phrase
   - **Context** — the situation, constraints, and forces at play, in a few sentences
   - **Decision** — the actual choice, stated in one to three sentences
   - **Alternatives considered** — at least two, each with pros, cons, and why it was rejected
   - **Consequences** — positive, negative, and risks, stated honestly rather than only justifying the choice made

**4. Draft in a fixed format** (Michael Nygard's ADR format, adapted with an explicit alternatives section):

```markdown
# ADR-NNNN: <Title>

**Date:** YYYY-MM-DD
**Status:** proposed | accepted | deprecated | superseded by ADR-NNNN
**Deciders:** [who]

## Context

## Decision

## Alternatives Considered

### Alternative 1: <Name>
- Pros: …
- Cons: …
- Why not: …

## Consequences

### Positive
### Negative
### Risks
```

**5. Approval gate before any write.** Present the draft; write the file only after explicit approval. On rejection, discard the draft without writing anything — don't save a "maybe" version anywhere.

**6. Maintain the index.** Append every accepted ADR to a table in the directory's index file (`ADR | Title | Status | Date`), append-only — never rewrite prior entries.

**7. Serve lookups from the index.** When someone asks "why did we choose X," check the index first; if there's a match, read that ADR and present its Context and Decision directly rather than reconstructing the answer from memory. If there's no match, offer to record one now.

## When to use

- Choosing between significant alternatives — a framework, library, pattern, or architecture.
- Someone says "we decided to..." or asks "why did we choose X?"
- During a planning pass that surfaces and resolves multiple architectural options.

Not for a minor implementation choice (a variable name, a function's internal shape) or a bug fix with no architectural impact — check for an existing ADR before writing a new one for something already recorded.

## How to use

**Install:** copy this folder into `~/.claude/skills/architecture-decision-records/` for personal use, or `.claude/skills/architecture-decision-records/` inside a project repo shared with a team.

**Invoke:**

```
We just picked Postgres over a document store for this service — record
that as an ADR before we move on.
```

```
Why did we choose the current caching strategy? Check
architecture-decision-records for an existing entry before answering from
memory.
```
