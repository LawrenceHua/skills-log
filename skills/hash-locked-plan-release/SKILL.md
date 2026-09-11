---
name: hash-locked-plan-release
description: Gate execution of any nontrivial plan behind a recorded consultation, an explicit user agreement, and a content-hash lock, so a plan can never run under an agreement that was given to a different version of it.
---

# hash-locked-plan-release

Plans drift. Someone approves version 1 of a migration plan, an agent quietly tightens or loosens a detail while "clarifying," and execution proceeds against version 2 — which nobody actually agreed to. A plain approval checkbox in a chat transcript can't catch this, because nothing forces the approval to stay bound to the exact content it was given for. The fix is structural: make every plan a versioned, hashed artifact, and make the execution gate check the hash, not just the presence of a prior "yes."

## The method

1. **Represent each plan as a small state record**, not just a paragraph in a conversation. Track: an id, the plan body, a revision number, a SHA-256 hash of the body, a lifecycle state, and an append-only note ledger. A single JSON file per plan (e.g. `plans/<id>/plan.json` plus `plans/<id>/notes.jsonl`) is enough — you don't need a database or a custom binary, just files your agent reads and writes with its normal file tools.
2. **Lifecycle:** `DRAFT -> CONSULTING -> RELEASED -> EXECUTING -> RELEASED -> COMPLETE`. `EXECUTING` is transient — a finished or interrupted run returns to `RELEASED` so further commands can reuse the same release. `COMPLETE` only accepts a `RELEASED` plan, never one mid-execution.
3. **Hold a dedicated consultation for that plan only** before anything executes. Ask about the goal, tradeoffs, assumptions, failure modes, and risks — and don't pull in unrelated history, other projects, credentials, or env files while doing it. Record concise structured notes, never a raw transcript: `{role: user|expert, kind: question|concern|response|decision|agreement, text, seq}`.
4. **Any edit to the plan body bumps the revision, recomputes the hash, returns the state to `CONSULTING`, and revokes any existing release.** This is the load-bearing rule: a revision cannot inherit a prior agreement. If the plan changed, the gate must reopen.
5. **Release requires, in this order within one consultation round:** a user question or concern → a later expert response or decision → a still-later explicit user agreement. Bind the release record to the exact hash and revision it was granted for. Execution tooling then refuses to run unless the live plan hash matches the released hash — so if the plan file changes after release but before execution, the gate blocks instead of silently proceeding on stale content.
6. **Treat this as a behavioral workflow gate, not a security boundary.** A direct edit to the state file or a command that bypasses the wrapper can still get around it. Don't describe it as sandboxing or access control — its job is to make the *intended* path honest, not to defend against a hostile operator.

## Optional: standing autonomy for a proven, bounded class of revisions

Once a specific plan has gone through a real, explicit-agreement release, you can let the user opt that plan's *future low-risk revisions* into a standing-autonomy policy, so they don't have to re-approve every trivial tweak:

- The policy is itself a receipt: it binds a policy id to the originating plan's id, hash, revision, and the real agreement sequence that authorized it. A policy can only be created from a genuine explicit-agreement release — never from a prior autonomous one (that would let autonomy bootstrap itself).
- For a later covered revision, the agent records its recommendation and a risk summary, then releases that exact hash under the policy — no new user note is invented, but the recommendation and risk summary are logged as the audit trail.
- The policy can be revoked without erasing its history; revocation blocks future autonomous releases but doesn't retroactively unwind a release already made while it was active.
- **Hard stops standing autonomy may never bypass, regardless of policy:** destructive or irreversible actions, credentials or billing changes, material scope expansion, unauthorized public or production mutation, and any genuinely user-only judgment call. Those always pause and ask explicitly — the policy only covers the boring, already-proven middle, not new categories of risk.

## When to use

- Any agent workflow that separates "plan" from "execute" and needs a plan edit to always revoke a stale go-ahead, instead of trusting a sign-off given to different content.
- Recurring, low-risk operations a user is willing to pre-authorize by class once, rather than re-approving every single run — while still hard-stopping on destructive/credential/production/scope-expanding changes.
- Reviewing an existing plan-then-execute pipeline for the specific gap where an approved plan can be edited after approval and executed without a fresh sign-off.

## How to use

**Install:** copy this folder into `~/.claude/skills/hash-locked-plan-release/` for personal use, or `.claude/skills/hash-locked-plan-release/` inside a project repo.

**Invoke:**

```
Before you touch anything, run this plan through hash-locked-plan-release: hold a
consultation on the plan, get my explicit agreement, hash-lock it, and don't execute
if the plan changes after that without reopening the gate.
```

```
Audit our plan-then-execute pipeline against hash-locked-plan-release — is there any
path where an approved plan can be edited and executed without a fresh agreement?
```
