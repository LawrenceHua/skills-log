---
name: fanout-cost-pinning
description: Before any multi-agent fan-out, explicitly pin every subagent's model to the cheapest tier adequate for its role — because subagents silently inherit the main session's (usually most expensive) model, turning ten parallel file-readers into ten apex-priced sessions.
---

# fanout-cost-pinning

There's a cost leak hiding in most agent frameworks: a spawned subagent that
isn't explicitly assigned a model **silently inherits the main loop's model**.
If your interactive session runs on the strongest tier (it usually does),
every reader, grepper, and inventory sweep you fan out runs there too — at
roughly 5–10× the per-token price of the tier the task needed (within one
vendor's ladder; more if a cross-vendor budget tier would have done),
multiplied by N parallel agents, invisibly, on every fan-out. Found the hard
way via a bill, not an error message.

## The rule

**No fan-out without a model pin per agent.** Before spawning, assign each
subagent the cheapest tier adequate for its role:

| Subagent role | Tier |
|---|---|
| Inventory sweeps, file listing, mechanical greps | cheapest/fastest |
| Reading, research, summarizing, drafting | mid |
| Synthesis across many inputs, high-stakes verification, adversarial review | strong — this is where the expensive tier actually earns its keep |

Two corollaries:

- **Put the pin in the agent definition, not the call site.** If your framework
  supports reusable agent/persona files with a `model:` field (see this repo's
  `agents/`), pin there once — call sites forget.
- **Fan-out multiplies everything.** Parallel agents trade tokens for
  wall-clock: each spawned context re-loads its own instructions and tool
  results, so a 10-agent sweep can cost ~5–10× a single-agent pass *before*
  the inheritance bug. Fan out for genuinely independent work, not as a
  blanket speedup — and pin every lane when you do.

## The audit

Worth running once a month, or after any framework update:

1. List every place you spawn subagents (skills, scripts, workflow files,
   agent definitions).
2. For each: is there an explicit model? If absent → it inherits → pin it.
3. Check your usage dashboard's per-model breakdown: apex-tier token volume
   that doesn't match your interactive usage is usually unpinned fan-out.

## When to use

- Writing anything that spawns parallel subagents.
- Reviewing an existing skill/workflow that fans out.
- Investigating a surprising AI bill.

**Skip it for:** frameworks that bill identically across tiers, or single-agent
work with no spawning.

## How to use

**Install:** copy this folder into `~/.claude/skills/fanout-cost-pinning/`.

**Invoke:**

```
Audit this repo's skills and agent definitions with the fanout-cost-pinning
skill: find every subagent spawn without an explicit model, and propose the
cheapest adequate tier for each based on its role.
```
