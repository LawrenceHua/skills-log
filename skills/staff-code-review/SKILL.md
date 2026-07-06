---
name: staff-code-review
description: A maximum-depth, multi-agent code and architecture review that auto-locates the diff to review from git state, fans out a full cross-functional panel (architect, frontend, backend, QA, security, SRE, product design), adversarially verifies every finding against the real code, and synthesizes a prioritized P0/P1/P2 risk register with a production-readiness verdict.
allowed-tools: [Task, Read, Bash, Grep, Glob]
---

# staff-code-review

A review only earns the name "staff-level" if it's (1) **grounded in the
actual code** — every claim cites a file and line, no generic advice, (2)
covers **more than correctness** — security, reliability, scale, ops,
accessibility, data, (3) is **adversarially verified** — plausible-but-wrong
findings get killed before they reach you, and (4) ends in a **prioritized,
actionable verdict**, not a wall of nits. This skill orchestrates all four.

This is the deep, always-maximum-depth panel — reserve it for pre-merge
high-stakes diffs and production-readiness audits. For a quick one-shot diff
lint, use a lighter single-pass review instead; this skill's whole value is
the extra depth, so don't scale it down for a small diff.

## When to use

- Before merging a high-stakes or pre-merge diff.
- "Review the changes we just made" / a production-readiness audit.
- A whole-system review where you want more than one lens on the code.

**Skip it for:** a trivial one-line change, or when you just want a quick
lint — that's a cheaper, single-pass review, not this.

## Phase 0 — find the target automatically

The person invoking this should not have to name a branch, path, or diff.
Locate the target deterministically from git state itself, in this order:

1. **Honor an explicit hint** if one was given (a path, a branch/ref, a PR
   number) — that always wins.
2. **Otherwise infer it from git**: check `git status --porcelain` for a
   dirty working tree (uncommitted changes are usually the live work),
   `git log <default-branch>..HEAD` for commits ahead of the base branch,
   and `git worktree list` for any sibling worktrees that might be the real
   target. Prefer the most recently touched, most likely candidate.
3. **Echo the detected scope back in one line before fanning out** — e.g.
   "Reviewing the 7-file working-tree change on `feature/checkout-retry`:
   payment retry logic + webhook handling" — so a wrong guess gets caught
   before any reviewers are spent.
4. **Only ask the user** if nothing usable turns up and the conversation
   gives no signal either.

State the target environment in one line too (e.g. "2 servers, moderate
traffic, small ops team") — severity below is relative to that, not to an
abstract ideal.

## Phase 1 — fan out the panel

Launch the personas in parallel, each with: the repo facts, the diff to
review, its specific lens, and the same finding schema. Give each a
disjoint piece of the write-up if they're producing sections of one
document. Every persona must:

- Read the real code and cite file:line for every finding — forbid generic
  advice.
- For each issue: *what* · *why it bites* · *evidence* · *severity* · *fix*.
- Be honest about both gaps and **strengths** — a review that only lists
  problems isn't trustworthy.

**Panel and lenses:**

1. **Solutions Architect** — component boundaries, data model, API design,
   event flow, migration story.
2. **Frontend** — component structure, state, validation-as-UX (not just a
   gate), accessibility, error surfacing.
3. **Backend** — domain invariants, transactions, correctness under
   concurrency, idempotency, input validation.
4. **QA** — enumerate realistic end-to-end scenarios (happy, ambiguous,
   failure, edge), each with acceptance criteria, mapped against existing
   tests to find what's untested.
5. **Security** — authn/authz on every route, secret handling, brute-force
   and injection surface, data scope, session handling, headers.
6. **SRE/DevOps** — behavior when dependencies are down, concurrency/races,
   retries, idempotency, offline behavior, observability, deploy/rollback.
7. **Product Designer** — flow efficiency, consistency with the rest of the
   product, copy, accessibility of the interaction.

Right-size the model per role if your tooling supports it: reserve your
strongest model for the architecture/security personas and for final
synthesis; a mid-tier model is fine for the more mechanical domain passes.

## Phase 1.5 — go deeper than a single pass

What separates this from a one-shot review is iteration and redundancy:

- **Loop until dry.** After the first round, re-run the finders on the same
  scope and dedupe against everything already found. Keep going until two
  consecutive rounds surface nothing new — a single pass always leaves a
  tail; this drains it.
- **Multi-skeptic verification.** Every P0/P1 finding gets checked by
  multiple independent skeptics with *distinct* angles (plain correctness,
  security/exploitability, does-it-actually-reproduce) — majority vote, not
  one reviewer's opinion. Kill or downgrade anything that can't survive two
  out of three.
- **A completeness critic, last.** One final pass asks: "what did this
  review not look at — a file in the diff nobody owned, a claim nobody
  verified, a failure mode not modeled, a test not actually run?" Its gaps
  become one more round of finding.

## Phase 2 — adversarial verification (mandatory)

Before trusting any finding, attack it. For every P0/P1, spawn a dedicated
skeptic subagent whose default posture is "this finding is wrong — prove
it's real" by reading the cited code itself. Kill or downgrade anything
that can't be reproduced from the actual source. This is what separates a
staff review from a linter dump.

## Phase 3 — synthesize the verdict

Produce one master document:

- **Verdict** — one line: production-ready or not, blocker count — plus a
  scorecard (a rough grade per area).
- **Consolidated risk register** — one table, deduped across personas,
  sorted by severity: `ID | Finding | Evidence (file:line) | Severity | Owner`.
- **Severity rubric** — **P0** = data loss, money error, security hole,
  outage, or a blocked core flow. **P1** = wrong behavior under realistic
  conditions, a missing core feature, or a compliance gap. **P2** =
  edge-case correctness, quality, perf-at-scale, accessibility, polish.
- **Strengths** — call out what's actually right, so nobody "fixes" it.
- **Roadmap** — sprint-ordered, P0s first, each item mapped to a finding ID.
- **Production-readiness checklist** — boxes the team can actually check off.
- **Open questions** — anything the review couldn't determine.

## Rules

- No finding without file:line — if you can't cite it, you didn't verify it.
- Severity is relative to the stated target environment, not an abstract ideal.
- Always include strengths alongside an explicit verdict.
- Keep each persona's context small — roughly one subsystem each.
- Always run the full panel and the full adversarial pass — don't scale
  down by diff size; that's a different, cheaper tool.
- Review is read-only. If findings lead to a code change, that's a separate
  step after the verdict is approved.

## How to use

**Install:** copy this folder into `~/.claude/skills/staff-code-review/`
for personal use, or `.claude/skills/staff-code-review/` inside a project
repo. The target-locating logic in Phase 0 is plain git commands — no
external dependency required.

**Invoke:**

```
Run a staff-code-review on whatever I've been working on in this repo —
full panel, adversarial verification, prioritized risk register.
```

```
Staff-code-review the diff between main and this branch before we merge —
I want the P0/P1/P2 register and an explicit production-readiness verdict.
```
