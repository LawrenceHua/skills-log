---
name: compaction-contract
description: A fixed five-section template for summarizing/compacting long AI-agent sessions that quotes exact strings (paths, errors, flags, commands) instead of paraphrasing them — so work can resume across a context boundary without re-deriving anything.
---

# compaction-contract

Every long agentic session eventually hits a context limit and gets summarized —
automatically by the tool, or manually when you hand off to a fresh session.
That summary is where work goes to die: a paraphrased error message can't be
grepped for, a "we updated the config" line doesn't say *which* flag, and the
next session burns twenty minutes re-discovering state the old session already
had. The fix is to treat the summary as a machine-readable handoff artifact
with a contract, not free-form prose.

## The contract

Put this in your always-loaded instructions file (e.g. `~/.claude/CLAUDE.md`),
addressed to the agent, so it applies to both auto-compaction and manual
handoffs:

```markdown
When compacting this conversation (auto or manual), structure the summary with
these sections and quote exact strings — never paraphrase a path, error, flag,
or value:

## Modified files
  - one bullet per file created/edited this session, full path verbatim
    (only files actually changed — not files merely read or grepped)
## Failing tests / commands
  - the exact error text + the command to re-run it
## Decisions
  - each decision + why + any option rejected
## Next step / resume anchor
  - the most recent in-progress task and what to do next
## Active flags / env / unverified
  - every flag=value, env var, branch name, and anything not yet verified

Recall of these specifics over brevity: when unsure whether one matters,
keep it. Compress routine narrative and tool-call noise freely.
```

## Why each section is there

- **Modified files** — the resumed session's first question is always "what did
  we actually touch?" Restricting it to *changed* files (not read ones) keeps it
  a work manifest, not a browsing history.
- **Failing tests / commands** — exact error text is greppable and re-runnable;
  "there was a type error in the auth module" is neither.
- **Decisions (+ rejected options)** — without this, the fresh session
  re-litigates settled questions, sometimes choosing the option you already
  rejected for a reason it can no longer see.
- **Resume anchor** — one unambiguous "you are here" beats a narrative of
  everything that happened.
- **Flags / env / unverified** — the silent killers. A feature flag set
  mid-session, an env var exported in one terminal, a claim that was never
  verified: each is invisible in prose summaries and each derails the next
  session. "Unverified" pairs with the `verification-labels` vocabulary —
  anything CODE-SHIPPED-NOT-VERIFIED must survive the compaction boundary.

The meta-rule — **specifics over brevity** — inverts the usual summarization
instinct. A summary that loses one exact error string to save ten lines made a
bad trade: narrative compresses safely, identifiers don't.

## When to use

- Standing instruction in any agent CLI that auto-compacts long sessions.
- Manually, at the end of a work session, to produce a handoff note for
  tomorrow's session (or a teammate's).
- Before intentionally clearing a context to reclaim room mid-task.

**Skip it for:** short sessions that will never be resumed.

## How to use

**Install:** paste the contract block above into your always-loaded
instructions file (`~/.claude/CLAUDE.md` or your tool's equivalent). Optionally
also copy this folder into `~/.claude/skills/compaction-contract/` for
reference.

**Invoke:**

```
Compact this session now following the compaction-contract template — exact
strings for every path, error, flag, and command; compress everything else.
```
