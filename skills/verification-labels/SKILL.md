---
name: verification-labels
description: A four-label vocabulary (VERIFIED, CODE-SHIPPED-NOT-VERIFIED, BLOCKED, INCONCLUSIVE) that every completion claim from an AI agent must carry, each backed by the exact command or probe that justifies it — so "done" can never silently mean "probably done".
---

# verification-labels

The most expensive failure mode in agentic work isn't wrong code — it's a
confident "done" that turns out to mean "I wrote code that should work." You
ship it, it breaks, and now you're debugging in production what a 10-second
probe would have caught. The fix is structural, not motivational: ban the
unlabeled "done" entirely, and force every status claim into one of four labels
that separate *implementation* from *proof*.

## The four labels

- **`VERIFIED`** — you (or the agent) reproduced the evidence *this session*
  with a real command whose output you can quote. Tests were run, not assumed.
  The deployed URL was probed, not inferred from a green pipeline. Always name
  the exact command/probe next to the label.
- **`CODE-SHIPPED-NOT-VERIFIED`** — the change exists (written, committed, even
  deployed) but nothing has proved it behaves correctly. This is an honest and
  common state; the label's whole job is stopping it from masquerading as
  VERIFIED.
- **`BLOCKED`** — verification is impossible right now for a stated reason (no
  access, missing credentials, an environment that's down). Name the blocker.
- **`INCONCLUSIVE`** — verification was attempted and the result doesn't
  clearly pass or fail (flaky test, ambiguous output). Name what was attempted
  and what came back.

Two rules make the vocabulary bite:

1. **The label travels with the claim.** Not in a footnote — in the same
   sentence: "Login fix: `VERIFIED` — `npm test -- auth.spec` 14/14 passing."
2. **A claim with no reproducible probe is `CODE-SHIPPED-NOT-VERIFIED` by
   definition**, no matter how confident the narrative around it sounds.
   Confidence is not evidence.

## Why this works

- It converts an argument ("are you sure it works?") into a lookup ("what label
  did it get, and what was the probe?").
- It makes the *gap* visible and cheap to close: a status report with three
  `CODE-SHIPPED-NOT-VERIFIED` lines is a to-do list of probes, not a fight.
- It survives delegation. When a subagent or a second CLI reports back, you
  re-label its claims yourself: nothing a delegate self-reports is VERIFIED
  until you've reproduced it (see `evidence-gated-delegation`).
- Paired with a claim→proof map (see `quality-gate-registry`), it fully
  specifies what "done" costs for each kind of work: "deployed" needs a live
  probe, "fixed" needs the original failure reproduced-then-absent, "tests
  pass" needs a test run in this session.

## When to use

- In every agent's standing instructions (CLAUDE.md / system prompt / rules
  file), so all status output is born labeled.
- At the end of any multi-step task, before telling a human it's finished.
- When reviewing another agent's (or person's) status report — re-derive the
  labels from the evidence offered, not from the adjectives used.

**Skip it for:** conversational answers and throwaway explorations where
nothing is claimed to be done.

## How to use

**Install:** copy this folder into `~/.claude/skills/verification-labels/`
(personal, all projects) or `<your-project>/.claude/skills/verification-labels/`
(project-scoped). Better still, paste the four-label contract directly into
your always-loaded instructions file — it's small enough.

**Invoke:**

```
Before you finish: relabel every status claim in your summary using the
verification-labels skill. Anything without a quoted probe becomes
CODE-SHIPPED-NOT-VERIFIED, and list the exact command that would upgrade it.
```

```
Give me a two-bucket report of this session: VERIFIED (with the command and
output for each) vs CODE-SHIPPED-NOT-VERIFIED (with the probe that's missing).
```
