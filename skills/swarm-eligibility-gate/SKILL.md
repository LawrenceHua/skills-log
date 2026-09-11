---
name: swarm-eligibility-gate
description: Decide whether a task actually warrants fanning out multiple parallel agents before doing it, route eligible work across three generic roles with required-return contracts, and downgrade gracefully instead of silently duplicating work when a role is unavailable.
---

# swarm-eligibility-gate

Fanning out parallel agents by reflex on every "substantial" task burns time and money on trivial requests, while under-using it on genuinely parallel work wastes the opposite way. Both failure modes come from the same root cause: no explicit gate for *whether* to swarm, and no fallback plan for when a role in the swarm can't run. This skill is an eligibility checklist plus a role-routing table plus a graceful-downgrade ladder, meant to sit on top of whatever multi-agent tooling you already have — it doesn't replace your orchestration mechanism, it decides when to reach for it.

## 1. Decide whether to swarm at all

Only fan out when **all** of these are true:

- The request has at least two genuinely independent questions or artifacts.
- Running them in parallel would reduce elapsed time or materially improve verification quality (e.g. an independent adversarial check, not just "more hands").
- Each node can be given a distinct scope, an explicit input/output contract, and an observable anchor (a file, command, or artifact) to check its work against.
- There's a free slot for a root/synthesizer agent that isn't displacing a live critical worker.

Do **not** swarm: a one-file lookup, a simple explanation, trivial formatting, a tightly serial investigation where step 2 can't start until step 1's exact result is known, or anything the user has explicitly restricted to one model, local-only work, or no delegation. Default to two or three nodes for eligible work — never treat a bigger swarm as inherently more thorough.

## 2. Route roles deliberately

Map every node to one of three generic roles, and route each to whatever tier of model/agent you have that fits:

| Role | Use for | Required return |
|---|---|---|
| **Mapper** (fast, cheap tier) | Planning, dependency mapping, bounded research, risk/cost inventory | Exact anchors, a dependency graph, non-overlapping next actions, and named blockers |
| **Refuter** (fast, cheap tier, fresh context) | Adversarial review, test-validity audit, evidence/currentness checks | A default-REFUTED verdict, a reproducible command or probe, and file:line or receipt-level evidence |
| **Writer** (your strongest/most expensive tier) | Only approved, critical-path implementation, migrations, or bulky build work | An isolated diff, the named gates it passed, an exact artifact/commit reference, and a bounded handoff note |

The refuter must never inherit the writer's reasoning as evidence — it inspects the produced artifact independently, fresh-context, and starts from "this claim is false until I reproduce it."

## 3. Build the graph before launching

1. Record starting anchors: repo/branch/commit (or equivalent state marker), any existing locks or leases, user-declared scope, cost/provider limits, and the final evidence gates the work must clear.
2. Give each node a short contract: `input`, `output`, `write scope`, `prohibitions`, `anchor`, `status vocabulary`.
3. Reserve write ownership to exactly one writer per logical path — if more than one node could touch the same files, isolate them (separate worktrees, or serialize instead of parallelizing that pair). Keep mapper and refuter read-only unless a node is explicitly given a disjoint write scope.
4. State the reduce contract before launch: expected node count, where artifacts land, the deterministic merge/dedupe step, and which single agent performs final synthesis. Synthesis is never a majority vote — the root compares claims against current artifacts and reproduces load-bearing gates itself.

## 4. Operate the swarm

- Cap active workers at available slots minus the root. Prefer two nodes for ordinary work; use three only when the third role is genuinely load-bearing.
- Post a concise status update on a fixed cadence during a long run: node state, last verified anchor, blocker, next dependency.
- Treat an empty, timed-out, rate-limited, or otherwise unavailable node as a **missing input**, not a clean pass — check whether it's still running or already finished before retrying, and label the gap `INCONCLUSIVE` rather than inventing a result for it.
- Reduce raw returns with deterministic code or a compact table; count expected versus received nodes and surface anything missing before synthesizing.

## 5. Fall back safely instead of duplicating work

If a role or slot isn't available, downsize the graph rather than quietly doing the same work twice or skipping verification without saying so:

- **One worker slot:** run mapper then refuter sequentially and call it a "sequential two-pass," not a swarm.
- **No mapper available:** do a bounded local map yourself, and keep the refuter for independent verification.
- **No refuter available:** do not claim independent verification happened — label the result `CODE-SHIPPED-NOT-VERIFIED` or `INCONCLUSIVE`, whichever fits.
- **No writer available:** leave the approved implementation as a handoff for later; never silently reroute it to an unapproved or unexpectedly-metered backend just to keep moving.

Close the graph only when every expected node has an anchor-backed result or an explicit blocker, the final artifact has been checked against its exact reference, and the root labels the outcome `VERIFIED`, `CODE-SHIPPED-NOT-VERIFIED`, `BLOCKED`, or `INCONCLUSIVE` along with the decisive command or probe that justifies the label.

## When to use

- Before reaching for a multi-agent fan-out by reflex on a "substantial-sounding" task — run the eligibility checklist first.
- Any existing multi-agent pipeline where role assignment currently just means "throw it at whichever model/agent is handy" instead of a deliberate mapper/refuter/writer split.
- A swarm run that came back with a missing or timed-out node, to decide the safe downgrade instead of silently re-running everything or shipping unverified.

## How to use

**Install:** copy this folder into `~/.claude/skills/swarm-eligibility-gate/` for personal use, or `.claude/skills/swarm-eligibility-gate/` inside a project repo.

**Invoke:**

```
Run this task through swarm-eligibility-gate before you fan out agents — does it
actually qualify, and if so what's the mapper/refuter/writer split?
```

```
One of the swarm nodes just timed out. Apply swarm-eligibility-gate's fallback
ladder — what's the safe downgrade instead of just re-running the whole thing?
```
