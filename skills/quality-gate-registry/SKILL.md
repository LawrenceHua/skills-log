---
name: quality-gate-registry
description: Map every "done" claim (tests pass, build works, bug fixed, deployed, verified) to the specific proof required before you say it out loud — prevents confidently reporting unverified work as complete.
allowed-tools: [Bash, Read]
---

# quality-gate-registry

A short, mechanical registry that maps completion *claims* to completion
*proof*. Its whole job is to stop the single most common AI-assistant
failure mode: reporting "done" based on having written code, rather than
having observed it work.

## When to use

Use this any time you're about to tell someone something is finished —
especially when the task involves tests, a build, a deployment, a
production check, a website/browser verification, a bug fix, or a
security/auth/payment-adjacent change. It's also useful as a standing
discipline: run it as a final check before any "done" claim, not just the
risky-sounding ones.

## The four evidence buckets

Before finalizing an answer, classify what you actually have:

- **VERIFIED** — a command, browser probe, deploy probe, or source check
  actually ran and passed in this session.
- **CODE-SHIPPED-NOT-VERIFIED** — files changed, but the runtime check
  either didn't run or didn't pass yet.
- **BLOCKED** — a specific permission, auth, environment, or external
  dependency prevented verification.
- **INCONCLUSIVE** — the evidence is mixed, partial, or contradictory.

Never collapse the last three into "done." Say which bucket you're in, out
loud, in the same sentence as the claim.

## Claim → required proof

| Claim | Required proof |
|---|---|
| Tests pass | The exact test command and its passing result |
| Build works | The exact build/typecheck/lint command and its passing result |
| Bug fixed | The original reproduction no longer fails, or a targeted test now covers it |
| Deployed | The deployment command/status plus a live URL or service probe |
| Website works | A browser or HTTP check against the actual target environment |
| UI looks right | A screenshot or viewport check, ideally at more than one size |
| Prompt/agent improved | A before/after eval, replay, grader, or synthetic scenario — not just "it reads better" |
| Security/auth/payment safe | Fail-closed checks, explicit negative tests, and confirmation no secret is exposed |
| "No issues found" | The scope actually reviewed, the files checked, and any remaining checks not yet run |

If the required proof isn't available, say the claim is unverified and name
the next concrete check that would close the gap — don't leave it as a bare
assertion.

## How to use

**Install:** copy this folder into `~/.claude/skills/quality-gate-registry/`
for personal use, or `.claude/skills/quality-gate-registry/` inside a
project repo so the whole team gets the same discipline.

**Invoke:**

```
Before you tell me this is done, run it through quality-gate-registry —
what's actually VERIFIED vs. just CODE-SHIPPED-NOT-VERIFIED here?
```

```
Apply quality-gate-registry to your last message — you said "deployed and
working," what's the actual proof for that?
```
