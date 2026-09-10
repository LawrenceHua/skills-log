---
name: delegation-brief-contract
description: A fixed structure for the handoff brief when an orchestrating loop delegates implementation work to an agent — the mechanism, an exclusive working path, hard prohibitions, exact gates, the proof standard, the stop line, and the report format — so a thin brief doesn't turn into rework.
---

# delegation-brief-contract

An agent you delegate to starts with none of your session's context. A brief that says "investigate why X is broken and fix it" gets you a plausible-sounding fix you can't actually trust without redoing the diagnosis yourself — which defeats the point of delegating. This method fixes the handoff: the orchestrating loop's job is to diagnose down to a named mechanism and write a complete brief; the agent's job is every edit, test run, and commit; and nothing gets called done until the returned evidence is independently checked.

## The division of labor

**The orchestrator keeps, and never delegates:**
- Diagnosis to the point of naming the mechanism — being able to say *what* is broken and *why*, with the evidence (a log line, a failing probe, a file:line), not just *that* something seems off.
- Writing the brief itself: constraints, prohibitions, the exact gates, what proof will be accepted.
- Judging the returned evidence with a default-skeptical stance, and reproducing any load-bearing claim locally before it counts as done.
- Anything only a human principal may decide: destructive actions, production mutation, credential or billing changes, merges, external messages.

**The agent owns, once the mechanism is named:**
- Every edit.
- Running gates and test suites, iterating until they're green.
- Commits, branches, opening pull requests.
- Sweeps across many files, mechanical migrations, burn-downs.

## Diagnose, then delegate

The handoff point isn't "I noticed a problem" — it's "I know the mechanism." Reaching that point is legitimate work to do yourself: read the failing log, run the probe, find the line. Keep it strictly read-only. The moment you're about to make an edit yourself, stop and write the brief instead of finishing it.

The one exception is a **read-only probe** you run because its answer determines what the brief should say (a query, a health check, a log tail). A probe that writes a file to make itself easier to run is no longer just a probe — throw that scratch file away rather than letting it become part of the deliverable. And don't delegate a one-token typo fix you already have open and proven — that's not what this discipline is for; the target is treating yourself as the implementer for anything nontrivial.

## What the brief must contain

A thin brief guarantees rework. Every delegation carries:

1. **The mechanism**, stated as an established fact with its evidence — the exact file:line, error text, or probe output. Not "investigate why X."
2. **An exclusive working path.** Never a shared live checkout another process might also be writing to. Say explicitly where the agent may write. This matters more than it sounds: consider a repo where a background job commits its own state every few minutes — an edit landing mid-cycle can silently corrupt that cycle's own evidence, with no way to detect or undo it after the fact. For anything with a concurrent writer (a cron job, another agent, a live service), build and test in an isolated copy the agent owns exclusively, then land the reviewed change through an explicit pause or lock the concurrent writer respects — and re-check the actual current state immediately before landing, since it may have moved while you worked.
3. **Hard prohibitions**, spelled out in full even when they feel obvious — the agent hasn't seen your standing rules. No production mutation, no credential or billing changes, no merges, no force-push, no writes outside the scoped path.
4. **The exact gates** to run, as literal commands, and what a passing result looks like.
5. **The proof standard**, named explicitly: for a behavioral fix, a new test must be shown *failing* against the pre-fix code before its later pass counts as proof. Evidence the agent generated entirely for itself, with no independent check, isn't evidence.
6. **The stop line** — what the agent must not do at the end. Usually: open the change for review and stop; do not merge, deploy, or send anything outward.
7. **The report format.** Ask for, in this order: what's actually done (with evidence) — the current or blocking step — what comes next. Leading with the decision-relevant facts gets faster, more accurate follow-up decisions than a terse status line followed by detail. Close with an explicit final status (verified / shipped-but-unverified / blocked / inconclusive) and the exact command or blocker that justifies it.

Tell the agent explicitly to push back if something in the brief turns out to be wrong — it should say so with evidence rather than "fixing" something that was never actually broken.

## Fan out on independent work

Independent workstreams should go out together so they run concurrently. Work that touches the same files gets serialized, or given separate isolated working copies — two agents writing into one checkout will corrupt each other in ways that look exactly like a code bug later.

Give each delegated task the cheapest capable model for its job; reserve your strongest model for synthesis and adversarial verification of what comes back.

## Verifying what comes back

Treat an agent's report as a claim, not a result:

- Re-run the decisive command yourself, or send an independent verifier at it — a verifier that only reads the implementer's own transcript verifies nothing.
- Confirm the gates actually ran, against the code that actually shipped, in the environment that actually executes it.
- Watch for the silent-failure shapes: a suite that passed vacuously (nothing was actually exercised), a gate that supplied its own evidence, or a verdict that improved only because the evidence for it disappeared.

If the report is thin or the proof is missing, send it back with the specific gap named. Don't quietly finish it yourself — that recreates the exact habit this method exists to prevent.

## When to use

- Any task that means "go fix / build / rework / clean up" something — including something you noticed yourself while reviewing or monitoring.
- Coordinating work across more than one delegated agent, especially when their scopes might overlap.
- A delegated task came back with a confident-sounding report you're not sure you can trust yet.

## How to use

**Install:** copy this folder into `~/.claude/skills/delegation-brief-contract/` for personal use, or `.claude/skills/delegation-brief-contract/` inside a project repo shared with collaborators.

**Invoke:**

```
I know the mechanism here — <file:line, the exact error>. Write a
delegation-brief-contract brief for an agent to fix it, with an isolated
working path and a mutation-tested proof standard, and dispatch it.
```

```
This agent's report says the bug is fixed but I haven't verified anything.
Walk delegation-brief-contract's verification checklist before I accept it.
```
