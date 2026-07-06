---
name: production-gauntlet
description: A looped, dual-verification stress-test and KPI gate to run before calling any non-trivial change "done" — define a thorough KPI list, stress-test it yourself (adversarial review, edge/failure injection, deterministic gates), get an independent second opinion (a different model or a teammate) on the same KPIs, then loop fix-and-retest until every applicable KPI is green on both sides.
allowed-tools: [Bash, Read, Task]
---

# production-gauntlet

A thorough KPI list plus a loop, checked from two independent angles.
Nothing is "done" until every applicable KPI is green from both angles and
a production-professionalism checklist passes — **verified by actually
observing it work, not by asserting it.** If a KPI genuinely can't be met,
say so out loud and stop; never fake the gate.

## When to use

At each meaningful step of non-trivial work — before saying "done, shipped,
works" and before moving to the next step. Especially reach for this after
implementing, fixing, refactoring, or deploying anything that matters, or
whenever someone asks "is this production-ready," "stress test this," or
wants walk-away quality they don't have to double-check themselves.

For unattended runs, wrap the whole loop with a verifiable stop condition
("all gauntlet KPIs green, working tree clean") so it continues until the
bar is actually met rather than until you get tired of checking.

## The loop

1. **Define the KPI list** for this specific change from the menu below.
   Drop only the rows that genuinely don't apply, and say out loud which
   ones you dropped and why — never narrow the list silently.

2. **Stress it yourself:**
   - **Adversarial review** — get a fresh-context reviewer (a subagent with
     no prior investment in the change) to attack the diff: correctness,
     security, performance, edge cases, process.
   - **Edge and failure injection** — empty/missing/malformed inputs,
     timeouts, stale credentials, concurrency, the unhappy path. Guards
     must fail closed, not open.
   - **Deterministic gates** — unit/functional tests, plus an offline
     grade for anything model- or prompt-driven (run it **at least three
     times** — a single grading pass on anything probabilistic is noise).
   - **Verify by observing**: actually run it, read the output, read the
     logs, look at the rendered result. Never just assert it works.

3. **Get an independent second opinion.** Hand the exact same KPI list to a
   genuinely different reviewer — a different model, a different session
   with no shared context, or a teammate — so a *different* system probes
   the same change and reports pass/fail with its own evidence. This
   catches blind spots the first pass can't see by construction. Any KPI
   where the two sides **disagree** counts as failing until it's resolved
   with evidence — two independently-green results is the bar, not one.

4. **Gate.** If any KPI fails, the two sides disagree, or the
   professionalism checklist has a gap → fix it → go back to step 2. Cap
   the number of loop iterations sensibly, and log anything you drop along
   the way.

5. **Done only when:** every applicable KPI is green from both angles and
   the professionalism checklist is complete. Report using the
   VERIFIED / CODE-SHIPPED-NOT-VERIFIED distinction — never conflate "I
   wrote it" with "I proved it works."

## KPI menu (keep every row that's relevant)

| KPI | Green means |
|---|---|
| **Correctness** | Does what it claims, proven by running it — not by reading the code |
| **No regression** | Graded against a baseline with a deterministic gate; anything prompt/model-driven gets a 3-run check with no consistent per-scenario drop |
| **Reliability / failure modes** | Fails closed on missing data; handles errors, timeouts, and edges; no crash loop |
| **Performance** | Latency/throughput within target; no measured degradation under load |
| **Security** | No secret/PII leak; authorization correct; injection-guarded; no destructive default |
| **Observability** | Success AND failure both emit logs/events; failures are visible, never silent |
| **Reversibility** | Rollback is recorded and one command away; the change is reversible and backed up somewhere durable |
| **Data integrity** | Nothing is lost; state reconciles across wherever it's stored |
| **UX quality** | User-facing output is clean and professional — no leaked internals, reads as finished |
| **Documented** | What changed, why, how to verify it, how to roll it back |

## Production-professionalism checklist

- [ ] Verified by observation, not claimed ("I ran X and saw Y")
- [ ] Two independent reviewers/engines agree it passes
- [ ] No regression — deterministic gate green (3-run for anything model-driven)
- [ ] Rollback recorded and reversible; source is backed up, not local-only
- [ ] Observable — both success and failure are logged
- [ ] Honest status: VERIFIED vs. CODE-SHIPPED-NOT-VERIFIED, open items named
- [ ] No silent narrowing — anything dropped, capped, or sampled is logged

## Notes

- This composes with (doesn't replace) whatever review and verification
  gates you already have — an adversarial code review, a
  verification-before-completion discipline, an offline quality grade, a
  continuous QA rubric. What this adds on top is the **independent second
  opinion** and the **loop-until-green** discipline.
- A grading harness only proves what it actually exercises — confirm which
  KPI each gate really covers, and check the rest (runtime guards,
  integrations) with direct functional tests against the real, deployed
  artifact.

## How to use

**Install:** copy this folder into `~/.claude/skills/production-gauntlet/`
for personal use, or `.claude/skills/production-gauntlet/` inside a project
repo. The "independent second opinion" step works with whatever second
reviewer you have access to — a different model, a fresh session, a
colleague — swap it in for whatever's available.

**Invoke:**

```
Run this change through the production-gauntlet before we declare it done —
full KPI list, adversarial review, and get a second independent opinion
before you tell me it's shipped.
```

```
Loop the production-gauntlet on this fix until every KPI is green from two
independent angles — don't stop at the first pass.
```
