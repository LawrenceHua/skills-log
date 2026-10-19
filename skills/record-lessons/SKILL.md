---
name: record-lessons
description: After a task succeeds or fails, record one append-only lesson as cue / lesson / evidence and mark it adopted only when independent evidence backs it.
---

# Record lessons

After a task, write down what a future run of the same kind of task should do differently. Do not write a diary of what happened.

## Entry format (one entry per lesson)

```
### <short title>
- cue: <when this applies: the task type, situation, or symptom you will recognise next time>
- lesson: <what to do, as one imperative instruction>
- evidence: <file:line, run link, CI link, commit SHA, receipt path, or log line that proved it>
- status: candidate | adopted
- scope: procedure | domain   (procedure = how you work; domain = facts about this project)
- date: <YYYY-MM-DD, local time zone>
- source: <task or thread id>
```

Cue, lesson, and evidence are all required. A lesson with no evidence is not a lesson; do not record it.

## Procedure

1. **Notice.** At the end of a task (success or failure), ask: what would I do differently next time, and what proved it?
2. **Draft** at most 3 entries. Each is one imperative instruction, specific enough to act on ("run the isolated test target before the full suite", not "be careful with tests"). If a new entry shares a cue with an existing one, merge or supersede instead of duplicating.
3. **Attach evidence.** Cite where the proof lives. Never paste secrets; cite where a secret lives, never its value.
4. **Set status.**
   - `candidate` (default): your own run suggests it, one run's evidence supports it, or you judged it yourself.
   - `adopted`: only with **independent** evidence, such as a test that fails without the lesson and passes with it, a CI run, a live check, or a reviewer other than you confirming it. Your own "it worked" does not count.
5. **Guard loosening.** A lesson that relaxes a rule (approvals, tests, guardrails, security, spend) is never adopted on your own say-so. It needs the owner's or user's explicit OK, cited in the evidence.
6. **Supersede, never edit.** When later evidence contradicts a lesson, append a new entry with `supersedes: <title>`. Leave the old entry untouched.
7. **Route it.** Domain lessons and candidates go in your own memory. Once a procedure lesson is adopted, fold it into the relevant skill (or create one with a trigger line) and cite the lesson title. Never write into another agent's memory or skills; hand the lesson to that agent's owner.

## Rules

- Append-only: never rewrite or delete past entries.
- No secrets, tokens, passwords, connection strings, cookies, or personal data, not even redacted fragments.
- One lesson per entry.
- If your system keeps an audit log, record only that a lesson was added (title and status).

## When to use

- After finishing or failing any non-trivial task where a future run should behave differently.
- When the same mistake or discovery shows up a second time.
- When deciding whether a hunch deserves to become a standing rule.

## How to use

1. Copy this folder into `~/.claude/skills/` for personal use, or into `.claude/skills/` inside a project.
2. Ask Claude Code to use the `record-lessons` skill by name.

Example prompts:

- "Use the record-lessons skill: the migration failed because the staging config differed from production. Record what we should do next time, with evidence."
- "Use record-lessons to review my candidate lessons from this week and tell me which have independent evidence to be adopted."
