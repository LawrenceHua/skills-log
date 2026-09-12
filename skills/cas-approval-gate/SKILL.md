---
name: cas-approval-gate
description: An atomic compare-and-swap two-phase state machine that makes an autonomous agent's risky action provably impossible to execute without an explicit, allow-listed human's approval — closing the race-condition gap a plain "ask permission" flag leaves open.
---

# cas-approval-gate

"Ask before doing anything risky" is easy to say and easy to break under concurrency. A boolean `approved` flag in memory or a plain file can be read by two processes at once, both see it as approved, and both act — or a stale approval from an old request can get reused for a new one if nothing ties the approval to the exact request it was for. The fix isn't a stricter prompt; it's modeling the approval as an atomic state machine that can't be raced or replayed.

## The method

1. **Model the action as an explicit state machine**, with at minimum: `PENDING -> APPROVED -> EXECUTING -> COMPLETE`, plus terminal `REJECTED` and `EXPIRED` states. Every risky action starts as a `PENDING` record, never as an implicit "go ahead."
2. **Store state somewhere that supports atomic compare-and-swap** — a database row with a version column, a file under an exclusive lock, or any store with optimistic-concurrency semantics. Never a plain in-memory boolean or a file two processes could race on with a read-then-write.
3. **Gate the approval transition (`PENDING -> APPROVED`) on an allow-listed identity.** Only accept this transition from a request that names a specific, pre-approved human as the approver, and only if the record is currently `PENDING` — reject transitions from anyone else, and reject if the state has already moved past `PENDING` (so a duplicate or stale approval can't reactivate an old request).
4. **Gate the execution transition (`APPROVED -> EXECUTING`) on the same atomic compare-and-swap.** The executor reads the current state and only proceeds if its own swap from `APPROVED` to `EXECUTING` succeeds. If two executors race on the same record, exactly one wins the swap — so a single approval can never authorize the action twice.
5. **Give every `PENDING` record a hard expiry.** Once expired, treat it as if it never existed rather than letting a week-old, forgotten sign-off silently authorize today's very different action.
6. **Log every transition** — who approved what, when, and the actual outcome of the executed action — so an audit can reconstruct exactly which human authorized which specific action, without needing to trust the agent's own narration of what it did.

## When to use

- Any pipeline where an autonomous agent proposes actions that write code, spend money, or mutate shared state, and a simple "ask before doing it" instruction isn't sufficient because two concurrent runs, or a retried request, could otherwise both slip through.
- Reviewing an existing approval flow for a race condition — check whether the approval check and the execution step read-and-write the same state atomically, or whether there's a window between "check" and "act" where a duplicate could sneak through.
- Designing any human-in-the-loop gate for autonomous or scheduled agent actions, where "the agent says a human approved it" needs to be independently provable rather than trusted.

## How to use

**Install:** copy this folder into `~/.claude/skills/cas-approval-gate/` for personal use, or `.claude/skills/cas-approval-gate/` inside a project repo.

**Invoke:**

```
This daemon can currently propose code changes with just a boolean approved flag —
redesign the approval flow using cas-approval-gate so it can't be raced or replayed.
```

```
Review this approval-then-execute flow against the cas-approval-gate pattern — is
there a window where two concurrent executors could both act on one approval?
```
