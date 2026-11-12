---
name: long-horizon-handoff-protocol
description: Keep long multi-session agent work from turning into confident fiction: treat context as a cache, write an on-disk handoff file at 60-70% usage, prefer a clean reset plus handoff over a summary of a summary, and attach a receipt to every claim.
---

# long-horizon-handoff-protocol

Long tasks fail quietly. Context fills with logs, the agent starts quoting results it never re-ran, a compaction paraphrases an error string, and the next session builds on a summary of a summary. This protocol moves durable state out of the conversation and into files, and puts a receipt on every claim. It complements a compaction template (which shapes the summary) by deciding when to stop, what goes on disk and how to restart.

## Principle: context is a cache, not memory

The goal is not to keep everything in context; it is to keep the right things and be able to rebuild the rest.

- **Target 40-60% context use** for hard work. At **60-70%**, write the handoff before starting another feature. Do not wait for overflow.
- **Retrieval first.** Use search and bounded range reads; open the raw file or log. Never paste a whole repo, transcript or web page into the prompt.
- **Files are durable.** Plans, feature lists, decisions, failing commands, receipts and handoffs go on disk. The conversation is the working set.
- **Compaction is a fallback, not the plan.** A clean reset with a strong handoff file beats a lossy summary for long tasks.
- **Three or four handoffs is the practical ceiling.** Beyond that, state decays. Switch to a durable ledger and restart from it.
- **Long input is a retrieval problem.** Build a small index, cite `path:line`, read the relevant regions.

## The handoff file

Write `HANDOFF.md` at every clean milestone and before any compaction. Fill every section; write "None." rather than deleting one.

1. **Objective** — one sentence.
2. **Latest user intent** — the newest instruction, quoted.
3. **Done when** — 3-7 observable criteria (a named test passes, a command exits 0, a file exists with expected content).
4. **Modified files** — exact paths, branch or worktree. Only files actually changed.
5. **Relevant files read** — paths the next agent should re-read, not everything you skimmed.
6. **Decisions** — what, why, the option rejected, any default you took.
7. **Failing commands** — exact command, exit code, decisive error line.
8. **Passing checks** — command and what it verified.
9. **Active flags / env / branch** — every flag=value, variable name (never its value), branch.
10. **Tool state** — background processes or sessions still running, with ids; what was stopped.
11. **Open questions / blockers** — and the exact words that would unblock each.
12. **Next step / resume anchor** — one concrete action.
13. **Must preserve** — files or contracts that must not be overwritten.

Pre-fill git state mechanically (branch, status, last ten commits) so the file starts from facts. Then run a trivial lint before you trust it:

```sh
grep -nEi 'TODO|TBD|FIXME' HANDOFF.md && echo "incomplete" || echo "no placeholders"
grep -nEi '(api[_-]?key|secret|token|password)\s*[:=]\s*\S{12,}' HANDOFF.md && echo "possible secret"
```

A handoff with a placeholder or a secret-shaped string is not a handoff.

## Start sequence (fresh session or after reset)

1. **Ground.** Print the working directory, `git status`, `git log -10`. Read `HANDOFF.md` and any result or ledger files. Re-run the last failing command. Never trust a summary of a summary.
2. **Frame.** One sentence of goal, 3-7 done criteria, the independent check, the blast radius, the rollback.
3. **Plan.** For non-trivial work write `PLAN.md`: phases, files, checks, rollback, open decisions.
4. **Build.** Read before editing, keep edits small, run the narrowest meaningful check after each risky batch, then broaden.
5. **Verify.** Deterministic checks first, then a fresh-context evaluator that sees the brief, the artifact, the diff and the command to re-run, but not the builder's reasoning. Default its verdict to refuted.
6. **Hand off** at a clean milestone, leaving the workspace clean.

## Receipts: every material claim carries one

A receipt is a file and line range, a command with exit code and the decisive output line, a URL with retrieval date, a hash, a test result, a screenshot, or for "no data" the exact query and its empty result.

- Do not quote a result you did not run this turn as current; re-run it or mark it `UNKNOWN` or `STALE`.
- Separate **FACT** (has a receipt), **INFERENCE** (reasoning from receipts) and **UNKNOWN** (not checked).
- If you cannot name the source, write `UNKNOWN`. Never invent a version, API, price, date or path.
- Absence of evidence is not green: a missing log, an empty result or a never-run test is a finding.
- No self-grading. The builder's confidence is not evidence.
- Do not flatten mixed results; report per item.
- Secrets never enter a handoff, receipt, prompt or PR body. Name variables, print presence booleans.

## Report format

Lead with the conclusion, then: what changed (exact paths); evidence per item (command and decisive output); residual risk and what would prove it wrong; one next action. Use fixed labels: `VERIFIED`, `CODE-SHIPPED-NOT-VERIFIED`, `BLOCKED`, `INCONCLUSIVE`.

## When to use

- A task spanning many files, sessions or agents, or one you expect to compact.
- Resuming after a reset, compaction or a different agent taking over.
- Any "go deep, verify, keep going" request where a confident wrong status would be costly.

Skip it for a one-command edit or a quick answer.

## How to use

**Install:** copy this folder into `~/.claude/skills/long-horizon-handoff-protocol/` for personal use, or `.claude/skills/long-horizon-handoff-protocol/` inside a project. Then ask Claude Code to use the skill by name.

**Example prompts:**

```
We're at about 65% context on this migration. Use long-horizon-handoff-protocol
to write HANDOFF.md, lint it, and tell me the single resume anchor.
```

```
Start a fresh session on this repo with long-horizon-handoff-protocol: read the
existing handoff, re-run the last failing command, and report FACT vs UNKNOWN
before touching any file.
```
