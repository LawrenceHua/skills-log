---
name: sandboxed-cli-worker-controller
description: Run other AI coding CLIs as least-privilege, evidence-producing workers under one controller — stripped credentials and config, pinned binaries, content-free immutable receipts, and safe process-group cancellation — instead of trusting a worker's self-report or running it with full permissions.
---

# sandboxed-cli-worker-controller

Once you're routing work to more than one AI coding CLI (your primary tool plus one or more others for independent review, wide fan-out, or capability comparison), the risk isn't that the worker is a bad model — it's that it runs with more trust than the task needs, and that a crashed or hostile worker leaves no trustworthy record of what it actually did. This method treats every non-primary CLI as an untrusted, sandboxed worker with a narrow contract, and makes the evidence trail itself tamper-resistant.

## The method

**1. Strip each worker down to what the task needs.** Disable that worker's own user-level config, rules, hooks, and MCP servers for the run — it should see only what you hand it. Default to a read-only or plan-only tool allowlist (e.g. only read/search tools, no edit/execute) unless the task genuinely requires writes, and if it does, scope writes to an exact path. Disable session persistence so nothing survives between runs. Never expose a "bypass sandbox" or "auto-approve everything" switch through the controller — if a worker needs elevated access, that's a decision the controller's owner makes explicitly per run, not a standing flag.

**2. Pin and verify the actual binaries you're invoking.** Don't trust `worker-cli` resolved from `$PATH` at call time — pin by hash (and code-signing identity, where the platform supports it) to a known-good copy, copied into a disposable per-run execution directory, and write-protect it from the worker process itself. A worker that can overwrite its own launcher can escape the sandbox retroactively.

**3. Strip credentials from the child environment.** API keys, cloud credentials, and any override variables the worker doesn't strictly need for the task should not be inherited into its process environment. A worker that never has a credential can't leak it, accidentally or otherwise.

**4. Make every run produce a content-free, immutable receipt.** Log hashes, counters, exit status, timing, and a canonical status label for each run — never the prompt, the output, working directory paths, or tool arguments. This makes the audit trail itself safe to keep, inspect, and even share, independent of whatever sensitive material the worker touched. Write to two independent sinks (a primary indexed store and an append-only journal) so a corrupted or truncated primary store doesn't erase the record; require both to agree before treating a run's status as settled, and fail closed (report the run as unverified) on any conflict between them rather than picking one arbitrarily.

**5. Bound output and retention, and fail closed at the boundary.** Cap how much a single worker run can write (per line, per stream, and in total) before launch. When your ledger or journal hits its retention limit, stop and require deliberate archiving — never silently drop old evidence to make room for new.

**6. Cancel safely.** Track each run by both its process group and a per-run identity token, so cancellation survives the worker double-forking or re-parenting children. Only signal processes you can prove started during this run (re-check PID, owning user, process-group, and start time immediately before sending a signal) and scope cancellation strictly to that run's own process tree — killing a shared parent can take out an unrelated sibling run.

**7. Share one deadline across the whole run, not one per phase.** Set a single wall-clock budget covering admission, setup, the worker's execution, and any queued follow-up reviewers — a reviewer stage shouldn't get a fresh clock. Reserve a short, fixed window at the very end purely for safe cleanup, separate from the work budget, so a slow cleanup can't eat into (or blow through) the deadline you promised.

**8. Degrade under load instead of thrashing.** If the host is under memory/swap pressure, force workers to run serially rather than launching them all in parallel; cap normal fan-out to a small number of concurrent workers.

**9. A worker's clean exit is not a verified claim.** Even a fully sandboxed, receipt-producing run only proves the worker executed and stopped cleanly — it says nothing about whether its findings are true. The controller's owner still has to open the worker's cited evidence and check it before treating anything as settled.

## Ownership boundary

This controller should own exactly one thing: safely launching and evidencing worker runs. It should not also own git branches, worktrees, merges, or global hooks — if a worker run is later authorized to make changes, hand that off to a single explicit owner (a worktree, a branch) rather than letting the controller and something else both think they own the write path.

## When to use

- You want a second (or third) AI coding CLI's independent opinion on a change, but don't want to hand it your full local permissions, credentials, or config to get it.
- Running an unfamiliar or less-trusted CLI agent for the first time and wanting a real security boundary, not just "I'll read the diff after."
- Building any kind of multi-CLI review or fan-out pipeline where you need an audit trail that's safe to keep even though the underlying work might touch sensitive material.

## How to use

**Install:** copy this folder into `~/.claude/skills/sandboxed-cli-worker-controller/` for personal use. This is a controller *pattern* — implement steps 1–7 as thin wrapper scripts around whichever CLI tools you actually use; most modern CLI coding agents expose the sandbox/permission flags needed (read-only mode, explicit tool allowlists, disabled config discovery).

**Invoke:**

```
Set up a sandboxed-cli-worker-controller wrapper around this second CLI agent
before I hand it review work — stripped config, pinned binary, content-free
receipts, no bypass flags.
```

```
I want an independent second opinion from another CLI agent on this refactor,
but it should never see my API keys or be able to touch anything outside this
one directory. Use sandboxed-cli-worker-controller.
```
