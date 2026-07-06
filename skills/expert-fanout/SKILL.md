---
name: expert-fanout
description: Spawn N domain-expert subagents in parallel to audit a codebase, product, or design from different angles, then synthesize convergent vs. divergent recommendations. Use when a single-perspective fix keeps failing, when you want a "second opinion" before a risky change, or when you've been head-down on one surface too long.
allowed-tools: [Task, Read, Write]
---

# expert-fanout

A multi-lens audit skill. Instead of one review pass, you spawn several
independent reviewers — each with a genuinely **different** role — and then
synthesize their reports into what most of them agree on (high confidence),
what only one of them raised (needs a tiebreaker), and where they flatly
contradict each other (the real next design question).

This is the "fresh eyes when you've been staring at the same code too long"
skill. It works because independent lenses surface the same root cause from
different angles far more reliably than one reviewer re-reading their own
work.

## When to use

- You've applied 3+ surgical patches in a row to the same surface and the
  bug keeps reappearing — the fix is probably at the wrong layer.
- You're about to ship a high-stakes change and only one person/session has
  seen the design.
- You want to compare two architecture options and there's no real
  disagreement in the room yet to stress-test them.
- Someone explicitly asks for "a second opinion" or "fresh eyes."

**Skip it for:** one-shot tasks (rename a variable, fix a typo), work where
the root cause is already clear and a fix is queued, pure lookups ("what
does this function do?"), or anything under ~30 lines of low-risk change —
a 4x-agent audit isn't worth the overhead there. If unsure, just ask: "worth
a fanout, or a surgical fix?"

## How the method works

### 1. Lock the target brief

Before spawning anything, write a short **Target Brief**: what system/files
are in scope, why now (which loop you're trying to break), what "good"
looks like (concrete success criteria), and what's explicitly **out of
scope**. Skipping this is the #1 way a fanout produces mush — without a
shared brief, every agent quietly redefines the problem and the reports
don't line up.

### 2. Pick N expert roles (N=4 is a good default)

Each role must bring a genuinely different lens — two "systems architects"
is wasted budget, not redundancy-for-safety. A solid default bank to pick
from:

| Role | Lens | Skip if... |
|---|---|---|
| **Systems Architect** | component boundaries, data flow, where state lives | system is a single small module |
| **Backend / Domain Engineer** | invariants, transactions, correctness under concurrency | no server-side logic |
| **Staff Engineer** | hot paths, latency, refactor leverage, dead code | not performance- or complexity-sensitive |
| **Frontend / Product Designer** | visual hierarchy, UX flow, consistency, accessibility | no UI surface |
| **Security Engineer** | authn/authz, secrets, injection, least privilege | no user input or external surface |
| **SRE / Reliability Engineer** | failure modes, retries, observability, blast radius | pre-production, no users yet |
| **Data Engineer** | schema, pipelines, freshness, source of truth | no structured data / pipelines |
| **Product Strategist** | positioning, differentiation, who it's for | internal tool with no go-to-market |
| **AI/Agent Architect** | agent loops, judge/critic separation, memory, tool-use validation | product has no LLM in the hot path |
| **Synthesis Agent** | reads all other reports, dedupes, ranks, surfaces contradictions | N < 3 (just read them yourself) |

Swap roles to fit the surface: a data pipeline gets a Data Engineer instead
of a Conversation Designer; a security-critical change adds a Security
Engineer as a 5th role rather than replacing one of the default four.

### 3. Spawn N agents in parallel, read-only

For each role, give the subagent: the Target Brief, its specific lens, and
an explicit instruction to be evidence-based and blunt ("cite file:line for
every claim, refuse to be polite, no generic advice"). Each agent runs
**read-only** — it produces a ranked list of findings, it does not touch
code. Ask each for the same report shape:

- TL;DR (harsh, specific)
- Evidence (file paths, line numbers, log excerpts)
- Ranked recommendations (impact × ease, ~3-5 items, top first)
- Per recommendation: pain → proposed change → rough size → risk → why

Right-size the model per role: the read-only domain reviewers can run on a
mid-tier model; reserve your strongest available model for whichever agent
does the final synthesis, since that's where judgment calls compound.

### 4. Synthesize

Once all N reports are in, read them together and produce one synthesis:

- **Convergent** — anything 2+ agents independently raised. This is your
  highest-confidence signal; execute these first.
- **Divergent** — raised by only one agent. Needs a tiebreaker: your own
  judgment, or one more targeted agent.
- **Contradictions** — where two agents actively disagree (e.g. "ship as one
  service" vs. "split it up"). Surface these explicitly — the disagreement
  *is* the next real design question, don't paper over it.
- **Off-table** — items raised but explicitly rejected, so they don't
  resurface next time unchanged.

### 5. Execute the top batch only

Pick the top 3-5 convergent items, confirm scope, and land them as one
atomic change. Verify against the success criteria from step 1. The whole
point of ranking is that not everything makes the cut — "execute everything
they recommended" is a pile-on, not a synthesis.

## Anti-patterns to reject

- Spawning 4 copies of the same role — that's redundancy, not a fanout.
- Skipping the target brief because "it's obvious" — it never is, once N
  independent agents start filling in the gaps themselves.
- Executing every recommendation instead of ranking and picking a batch.
- Treating divergence as a stalemate — it's the next question, not a dead end.
- One agent role-playing N personas in a single context — it converges to
  its own prior. Real, independently-spawned subagents are the point.

## How to use

**Install:** copy this folder into `~/.claude/skills/expert-fanout/` for
personal use, or into `.claude/skills/expert-fanout/` inside a project repo
to share it with your team via version control. Restart or refresh your
Claude Code session so it picks up the new skill.

**Invoke** by asking directly, or (where your setup supports named skill
invocation) with `/expert-fanout`:

```
Fan out experts on this repo's payment module: systems architect, backend
engineer, security engineer, and SRE. Read-only, ranked recommendations,
then synthesize convergent vs. divergent findings.
```

```
We've patched this race condition three times and it keeps coming back.
Spawn a 4-expert fanout to find the real root cause before I patch it again.
```
