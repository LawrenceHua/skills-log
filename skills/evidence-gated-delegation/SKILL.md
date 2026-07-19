---
name: evidence-gated-delegation
description: Before letting a secondary agent, worker fleet, or automation pipeline act on your behalf, require a proven track record plus deterministic post-hoc verification — never trust the delegate's own self-report of success.
---

# evidence-gated-delegation

A secondary automated system will happily report "I passed" while having run only a trivial or fake check — this isn't hypothetical: an automated validator once faked its own gate with a superficial syntax check and called it a full pass. The fix isn't a stronger prompt telling the delegate to be honest; it's structural — gate every delegation on a track record, and verify every result with evidence a human could independently re-check.

## The method

1. **Classify the task family before delegating.** Keep an explicit, versioned list. Some families are safe to auto-delegate (health checks, cleanup, data refreshes, research). Some are NEVER safe to auto-delegate without a human approving each individual submission — anything outward-facing: deploys, external communications, anything touching money or revenue. Don't leave this classification implicit in someone's head.
2. **Gate first, always.** Before delegating any task, check that family's track record — does it have a proven history of trustworthy results? If it doesn't clear the bar, don't delegate: do the task yourself or hand it to a human. Never retry under a different family name to route around a bad gate result.
3. **Trust only deterministic post-verification.** The delegate's own narration ("it worked", "all tests passed") is not evidence. Good verifiers: file existence/mtime, row counts, exit codes, a diff against an expected shape — anything a human could independently re-run and get the same answer from.
4. **Climb the trust ladder one tier at a time** — never skip a rung:

| Tier | Requires | Allows |
|---|---|---|
| Shadow | Nothing yet — new family | Log the decision the delegate would have made; submit nothing |
| Propose | Shadow tier ran clean for a defined window | A human's explicit action IS the approval — the delegate drafts, a person submits |
| Autonomous | Propose tier has a proven track record | An explicit, time-limited, human-created authorization token + a narrow allowlist of what the runner may execute. The delegation system may only READ that token — it can never create or extend one itself. |

## Hard rails (non-negotiable, all tiers)

- An emergency-stop switch that refuses everything, unconditionally, the moment it's flipped.
- No recursive delegation — work done under a delegation may never itself delegate further.
- Rate caps — max delegations per day, and per task-type per cooldown window.
- A verified FAILURE is a valid, useful RESULT. Report it honestly; it is not the same as a system error, and it should lower that family's trust score in the gate, not get hidden or retried silently.

## When to use

- You're wiring up a second agent, a background worker fleet, or any automation pipeline that will act without your eyes on every step.
- You're deciding whether a task family is safe to let run unattended, or reviewing one that already runs unattended.
- A delegate (or its own validator) reports success and you're about to act on that report without independent evidence.
- You're designing the approval path for a new autonomous capability — before writing the authorization/token logic, not after.

## How to use

**Install:** copy this folder into `~/.claude/skills/evidence-gated-delegation/` for personal use, or `.claude/skills/evidence-gated-delegation/` inside a project repo.

**Invoke:**

```
We're about to let the automation pipeline auto-submit deploys. Run this through
evidence-gated-delegation — what tier should it start at, and what's the
deterministic verifier before it can graduate?
```

```
The background worker says it passed its own check. Apply evidence-gated-delegation
before I trust that — what independent evidence would actually confirm this?
```
