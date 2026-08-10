---
name: adversarial-planning
description: A deep-planning protocol for non-trivial changes — parallel research agents map the current state and blast radius, competing designs are drafted, then a mandatory adversarial pass attacks the plan before a single line is implemented, producing an evidence-gated plan with per-change verification commands.
allowed-tools: [Task, Read, Grep, Glob, Bash]
---

# adversarial-planning

Most agent failures on non-trivial work are planning failures wearing an
implementation costume: the plan assumed a function signature that didn't
exist, missed a second caller of the thing being changed, or had no answer for
"how do we know each step worked?" This protocol front-loads the pain. It costs
real time (30+ minutes on a big change) and pays it back the first time the
attack pass finds the flaw you'd otherwise have found in production. A plan
that hasn't been attacked is not done.

## The protocol

Stay **read-only** until the plan is approved. No implementation during
planning, ever.

### Phase 1 — Research fan-out

Launch parallel read-only research agents (minimum 3), each with one lens:

1. **Current state** — read every file that will be touched. Map functions,
   dependencies, integration points. Report exact `file:line`, not prose.
2. **Blast radius** — trace all callers/importers of what's changing. List
   what could break.
3. **Patterns & precedents** — find similar implementations, existing tests,
   design docs in the repo; search the web for current best practice if an
   external API is involved (training data is stale for anything that moves).
4. **Live environment** *(only if the plan mutates a repo / deploys)* — current
   branch, dirty tree, unpushed commits, open PRs, anything else operating on
   this repo. Report each as a fact, never an assumption.

Pin research agents to a cheap/mid model — they're readers, and subagents
silently inherit your expensive main model unless pinned (see
`fanout-cost-pinning`).

### Phase 2 — Competing designs

Draft two designs with different mandates, on your strongest model:

- **Implementation-first**: exact files, functions, ordering, backward
  compatibility.
- **Risk-first**: failure modes, edge cases, races, rollback. For *each*
  change: a **precondition check** (if state-dependent), a **post-verification
  command**, and its **expected output**.

### Phase 3 — The attack (mandatory)

Attack the merged plan. Default stance: *"this plan is broken — prove it
isn't."* Hunt specifically for: the wrong assumption, the unhandled case, the
missing rollback, the step whose success can't be observed, the irreversible
action with no precondition.

Scale the attack to stakes: an inline hostile re-read for small plans; a
dedicated fresh-context skeptic agent (see this repo's `roast-me` skill or the
`hostile-reviewer` agent) for anything large, multi-system, or irreversible.
Fold every surviving objection back into the plan, or record explicitly why
it's acceptable.

### Phase 4 — Write the plan artifact

One file containing: the problem + single success criterion; execution order
(what parallelizes); per-change file paths, reasoning, risk level,
precondition + post-verification command + expected output; rollback for every
risky step; explicit tagging of any outward/irreversible step (push, deploy,
publish, delete) with whether it may run unattended or stays human-gated; and
the adversarial findings with their resolutions.

## Why the structure matters

- **Parallel single-lens researchers** beat one generalist pass: each agent
  reads deeply instead of skimming everything, and the lenses don't blur.
- **Per-change verification commands** turn execution into a checklist an
  agent can run unattended — and make "done" checkable (see
  `verification-labels`).
- **The attack pass is where the value is.** Research and design feel
  productive; the attack is the only phase whose job is being *right*.

## When to use

Non-trivial features, refactors, migrations, anything touching production, and
any task you intend to hand to an autonomous agent to execute unattended.

**Skip it for:** small well-understood edits — the overhead outweighs the risk.
Use a quick inline plan plus a self-review instead.

## How to use

**Install:** copy this folder into `~/.claude/skills/adversarial-planning/`
(personal) or `<your-project>/.claude/skills/adversarial-planning/`
(project-scoped).

**Invoke:**

```
Use the adversarial-planning skill for this change: [describe the feature or
migration]. Stay read-only, fan out the research agents, and don't show me the
plan until it has survived the attack pass.
```
