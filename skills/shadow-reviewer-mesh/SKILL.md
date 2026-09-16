---
name: shadow-reviewer-mesh
description: Run a second, independent AI agent as a concurrent read-only reviewer while your primary agent keeps working, so a second set of eyes finds gaps in real time — treating its output as an advisory lead, never as proof, until you personally reproduce the finding.
---

# shadow-reviewer-mesh

An agent that writes and reviews its own change shares its own blind spots — it won't catch what it didn't think to check the first time. But bolting a second review on only at the very end wastes the parallelism a second agent offers, and worse, agent findings often get treated as proof simply because they came from a model instead of "did I personally reproduce this." The fix is to run the second reviewer *concurrently*, keep it strictly advisory, and never let its say-so substitute for evidence you generated yourself.

## The method

1. **Decide whether a second reviewer is actually warranted.** Reach for one when: it's explicitly requested; the change touches a high-risk surface (deploys, live traffic, payments/PII/security, shared prompts, test harnesses, rollback paths); the diff is nontrivial enough that pre-commit review would catch real issues; or a test suite passes but you're not confident it covers realistic edge cases. Skip it for small deterministic edits or simple questions — a reviewer that adds latency without changing the answer isn't worth spawning.
2. **Scope it before launching.** Write down the objective, the exact scope (which files/modules/checks), and what evidence would actually count as a resolved finding. A reviewer without a bounded scope wanders and produces vague, unreproducible findings.
3. **Launch it read-only and concurrent.** Start the reviewer in read-only/plan mode (no edit permission) while you keep working the critical path yourself — don't block on it. Give it an explicit output contract: return confirmed risks, weak/unproven concerns, and recommended follow-up checks, each backed by evidence (a file:line, a command, a log line), not just an opinion.
4. **Cap the wait.** A short cap (on the order of a couple of minutes) is enough for a routine side-review; a longer one only when someone explicitly asked for a maximum-quality pass. An advisory review that stalls the actual work has gone negative.
5. **Reproduce before acting.** Treat every returned finding as a lead, not a fact — run the test it claims fails, read the code it cites, hit the endpoint it flagged. Reject anything you can't ground after a reasonable look; a plausible-sounding but unreproducible finding is noise, not signal.
6. **Run your own gates regardless.** Tests, build, lint — run them yourself after edits no matter what the reviewer reported. Its pass/fail opinion is never a substitute for your own check.
7. **Close with an evidence-based report**, not a review-based one: which reviewer(s) ran, which findings were confirmed vs. rejected and why, and what you personally verified. Never say "fixed" or "ready" because a reviewer said so — say it because you reproduced it.

**Safety notes:** never hand a reviewer secrets, `.env` contents, credentials, or raw private history. If it's allowed to edit anything, inspect the diff yourself before continuing. Never let it deploy, mutate credentials, or touch production without separate, explicit approval for that exact action.

## When to use

- Any nontrivial change you're about to ship without another human's eyes on it, especially one touching production, security, payments, or shared infrastructure.
- Right after a local test suite goes green but you're not confident it exercises the real edge cases.
- Auditing an existing "just ask another model" review habit that's quietly started treating a second opinion as proof instead of a lead to verify.

## How to use

**Install:** copy this folder into `~/.claude/skills/shadow-reviewer-mesh/` for personal use, or `.claude/skills/shadow-reviewer-mesh/` inside a project repo.

**Invoke:**

```
Before you commit this, run shadow-reviewer-mesh — spin up a second read-only agent
scoped to the auth module, and reproduce anything it flags before you act on it.
```

```
We keep shipping fixes because a reviewer agent said "looks good." Apply
shadow-reviewer-mesh's rule going forward: its output is a lead, not proof, until
we reproduce it ourselves.
```
