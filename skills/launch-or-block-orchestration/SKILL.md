---
name: launch-or-block-orchestration
description: Run a hierarchical multi-agent program (coordinator, sub-orchestrators, planners, executors, verifiers) without stalling in its own admission layer — check launch preconditions once at launch, keep pre-execution review to one planner pass plus one verifier pass, require receipts for every fan-out claim, and treat a night with zero real launches as a harness defect.
---

# launch-or-block-orchestration

Multi-level agent orchestration has a characteristic failure that looks like diligence: the coordinator keeps re-checking capacity, re-issuing short-lived permission windows, and spawning "one more review round" — and hours pass with **zero real work launched**. Nothing crashed. Every gate did its job. The system was just so busy protecting the launch that it never made one. This method fixes the admission layer so that every launch attempt ends in exactly one of two states: **launched**, or **blocked with a named, checkable reason**.

## 1. Fixed roles, no overlap

Give every participant one role and a "never" list. Overlap is where verification quietly stops being independent.

| Role | Owns | Never |
|---|---|---|
| **Coordinator** | Diagnosis down to the mechanism, the briefs, judging returned evidence, the merge go/no-go, updates to the human | Implements, monitors in a polling loop, merges over a judge's HOLD |
| **Portfolio orchestrator** | One queue per workstream, capacity accounting, a periodic status line | Runs a whole task itself; edits outside a lane's own working copy |
| **Sub-orchestrator** (one per workstream) | Planner → executors → verifier for its workstream; its own plan file | Pushes without external admission; claims verified without a verifier receipt |
| **Planner** | Scope, base revision, working copy, file list, ETA, acceptance command | Starts implementation |
| **Executor** | Edits, tests, commits — inside its own working copy | Touches another lane's files; skips hooks; force-pushes; marks a change ready or merges it |
| **Organizer** | Ledger rows, status facts, receipt files | Invents a status; edits a running lane's brief |
| **Verifier** | Re-runs the decisive command, opens the named receipt, starts from "this claim is false" | Trusts the executor's summary |
| **Judge** | A written verdict file ending in `LAND` or `HOLD` | Authored the patch it judges |

## 2. Receipts or it didn't happen

- Every sub-thread appends one line to a per-lane ledger: `role | thread id | start | end | produced`.
- Every lane report opens with a status line: `VERIFIED | CODE-SHIPPED-NOT-VERIFIED | BLOCKED | INCONCLUSIVE`.
- A verification block is quoted in full, not summarized. A judge verdict is a file path plus its verdict line.
- **A fan-out claim with no ledger entry is graded `CLAIMED`, not `VERIFIED`.** "I spawned four reviewers" in prose is a claim about the model's narration, not evidence that four threads ran.

## 3. Check launch preconditions ONCE, in the launcher

Admission checks belong to the component that launches, run at the moment of launch:

- **Capacity:** count live top-level lanes by checking process liveness (not by counting directories), plus a load ceiling and a memory ceiling.
- **External admission:** any downstream queue you'd push into (CI, a review queue, an API rate budget) is under its ceiling.
- **Write ownership:** an exclusive lease on exactly the files the lane will touch (see the `workspace-lease` skill).

Then launch. Do **not** re-verify these at every message hop, every mesh sync, or every status tick — a floor like "at least 120 seconds of window remaining" re-checked at each hop will be crossed by the hop latency itself, and the launch that was fine at t=0 gets refused at t=90.

**Memory-pressure gotcha (macOS):** "swap used" is sticky — it stays high long after pressure subsides. A gate keyed on swap percentage alone can idle a healthy machine all night (observed: swap at 90%, system-wide free memory at 33%, no warning level, gate refusing everything). Gate on the OS memory-pressure reading and free percentage; treat high swap as admissible when free memory is comfortable and pressure level is normal.

## 4. The launch-or-block rules

1. **No invented allocation.** No role may create grants, TTLs, time windows, or admission tokens beyond what this protocol defines. A self-issued 5-minute grant with a floor check is a machine for expiring.
2. **Pre-execution review is bounded: at most one planner pass and one verifier pass.** A HOLD must name the specific missing receipt or failed check. It does not spawn another review round to think about it more.
3. **Expiring windows escalate, they don't repeat.** If a window expires, the next one is at least **3× the measured round-trip**. A *second* expiry is a `BLOCK` sent to the coordinator carrying the numeric constant that failed — never a re-issue at the same TTL.
4. **Close before you open.** Finished agent threads are closed before new ones start. Thread ceilings are hard limits (`depth × slots`); "agent thread limit reached" means a leak in the orchestrator, not a reason to retry harder.
5. **Zero real launches in a working period is a defect to report** — a line in the next status update naming the gate that consumed the time — not a protocol to defend.

## 5. Spend order and quota loss

Order lanes: subscription or free capacity first, then local models, then metered paid. **Losing quota means PAUSE plus a recorded status fact — never a relaunch loop.** Rotating accounts or credentials to get around a quota is not a fallback; it's a policy violation.

## 6. Merge authority

Merge requires a judge `LAND` **and** the coordinator's go. Never merge over red required checks. Drafts stay drafts until the human or the coordinator flips them. A report is a claim: the coordinator or a verifier re-runs the decisive command before "done."

## 7. Hard never-list (all roles)

Kill processes or servers you didn't start. Edit scheduler definitions, policy/state files, or auth/credential stores. Write outside your lane's working copy. Print secrets. Bare `git stash`. Add a network call the brief didn't name.

## When to use

- Setting up or debugging a coordinator that launches sub-agents in layers.
- A multi-agent run that "worked all night" but produced nothing.
- Deciding who may merge, who verifies, and what counts as a receipt.
- Auditing an orchestration for self-issued grants, per-hop re-checks, and unbounded review loops.

## How to use

**Install:** copy this folder into `~/.claude/skills/launch-or-block-orchestration/` for personal use, or `.claude/skills/launch-or-block-orchestration/` inside a project repo. Then ask Claude Code to use the skill by name.

**Invoke:**

```
My orchestrator spent six hours in review loops and launched no executors. Use
launch-or-block-orchestration to find which admission gate is eating the time and
rewrite it as a single launch-time check.
```

```
Design the role table, receipt format, and merge rules for a three-workstream agent
program using launch-or-block-orchestration. Fan-out claims without a ledger line
should grade CLAIMED.
```
