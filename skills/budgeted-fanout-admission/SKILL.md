---
name: budgeted-fanout-admission
description: Admit a fixed batch of independent tasks through ordered access, budget, and resource gates while reserving concurrent usage and accounting for every partition.
---

# Budgeted Fan-out Admission

Coordinate a bounded batch without losing refused work or spending the same allowance twice. Record admission, execution, and acceptance separately. This procedure installs no scheduler.

## When to use

Use for independent edits, analyses, or checks that could run concurrently but share spending limits or host resources.

Resolve shared writes and dependencies before partitioning, or work sequentially.

## How to use

Copy this whole skill folder into `~/.claude/skills/` for personal use, or into `.claude/skills/` inside a project. Ask Claude Code to use `budgeted-fanout-admission` with the task inventory and authorized execution limits.

### 1. Freeze the batch contract

Create an inventory with a unique batch identifier and one stable identifier per requested partition. Record each brief, inputs, exclusive write scope, required output, acceptance check, dependencies, permitted execution routes, and owner. Retain even items that never launch.

Set the concurrency ceiling, batch and partition time limits, budget unit and cap, warning and hard-stop boundaries, resource limits, and transient-pressure retry count and total waiting limit. Include verification and retry costs in the allowance. Define what happens to running work at a hard stop; do not assume cancellation is authorized or that it reverses charges.

Choose one coordinator to own admission and the usage ledger. Choose relative result and evidence paths. Missing required limits or unavailable gate data prevent admission until resolved.

### 2. Check effective access without exposing secrets

Use the selected route's documented read-only status or capability check. Establish that the intended identity can use the requested execution mode and scope. A tool version, installed executable, or credential-file presence alone is insufficient.

Record the decision, capability scope, timestamp, and sanitized diagnostic. Do not read or print credentials. An unavailable probe or denied capability stops admission for that route. A route change is allowed only if it was already authorized; run the access check again for the selected replacement. Never silently switch providers, accounts, permissions, or notification channels.

### 3. Apply the budget policy

Obtain current usage for the relevant accounting window, including external consumption where it shares the cap. Distinguish measured usage from estimates and explain any uncertainty or reporting delay.

Apply the declared policy in order:

- **Proceed:** the proposed reservation fits all limits.
- **Warn:** proceed only under the contract's warning rule and with the warning recorded; use a cheaper route only if previously authorized.
- **Hard stop:** admit no additional work under that policy; retain unlaunched partitions as deferred.

Serialize all admission decisions through the coordinator. Before admitting a partition, reserve its bounded allowance against the shared cap. Available budget equals the cap minus settled consumption minus outstanding reservations, without double-counting usage already included in a reservation. Running and admitted-but-not-started work retain reservations.

Use enforceable worker limits or a defensible upper bound for each reservation. A point estimate is not a spending ceiling. Reconcile usage reports before releasing allowances; uncertain or delayed charges remain conservatively reserved. If reliable concurrent accounting is unavailable, avoid concurrent admission and wait for usage reconciliation between launches. If even sequential cost bounds cannot be established, defer instead of guessing.

### 4. Admit host resources for each partition

After access and budget checks, examine current resource pressure and the next partition's demand. Account for resources reserved by other admitted work, not just the current number of processes.

For temporary pressure, retry only within the declared count and waiting limit. Recheck budget freshness before eventual launch. Hard refusal, missing telemetry, or exhausted retries produces an explicit deferred item with reason and resumption condition. Release an unlaunched reservation only after confirming no worker started.

Create an isolated working location and confirm exclusive ownership of its write scope. A separate folder or worktree prevents some collisions; it is not a security sandbox and does not restrict credentials, networking, or access elsewhere. Preserve actual execution restrictions and stop if required isolation cannot be established.

### 5. Launch and collect per-partition evidence

Before launch, record the partition, scope, route, gate decisions, reserved allowance, working location, and limits. After launch, capture the returned execution identifier and start time. If launch acknowledgement is uncertain, reconcile that attempt before retrying; keep its reservation until resolved.

Collect bounded output, finish time, exit status, changed artifacts, usage, and the acceptance-check result. Mark usage as measured or estimated, with its unit and basis. Exit zero or nonempty output establishes neither task completion nor acceptance. Keep execution outcome and verified task result separate.

### 6. Reconcile the complete inventory

Report every requested identifier exactly once in its current state: pending, admitted, running, completed, failed, deferred, or canceled. Completed records successful execution; report semantic acceptance separately. Preserve failed or canceled attempts and their usage when a partition is retried.

Report requested count, current-state counts, and cumulative admissions separately; cumulative admissions overlap final states. Reconcile spending, outstanding reservations, and uncertainty against the cap. Preserve every deferred brief and its next condition. End with artifacts, acceptance evidence, remaining work, and any unresolved accounting. Do not declare the batch verified while required acceptance checks, partitions, or usage reconciliation remain unresolved.

## Example prompts

- “Use budgeted-fanout-admission for these independent checks with the supplied routes, limits, and budget policy.”
- “Review this proposed batch and identify which partitions can be admitted now and which must remain deferred.”
