---
name: capped-expert-routing
description: Route a non-trivial question to one or two domain-expert subagents under a hard concurrency cap, with a capacity and ownership check first, then synthesize convergent findings and disagreements.
---

# Capped expert routing

Pick the right domain expert or experts for a task, run them as read-only researchers within a fixed cap, then synthesize one answer. The cap keeps cost, machine load, and conflicting edits under control.

## Procedure

1. **Frame.** Restate the task in 2-3 lines and list the domains it touches (for example: application code, UI/UX, system design, security, data, infrastructure, product, ML).
2. **Choose.** Pick one primary expert and at most one secondary to run in parallel. A third lens runs only afterward, and only if it would change the answer. Trivial or single-fact questions get one expert and no fan-out.
3. **Read shared state.** If you keep an expert index or per-expert notes (last refresh date, current-state summary, dated digests), read them first so experts start from known context. Flag anything stale.
4. **Capacity and ownership check** before spawning. Standing cap: at most 2 read-only readers, or 1 executor plus 1 reviewer; one writer per artifact.
   - Check machine load and how many agent sessions are already running.
   - Check whether anything holds a lease or claim on the target files.
   - If capacity or ownership is unclear, run the experts sequentially yourself instead of fanning out.
5. **Brief and fan out.** Give each expert the same restated brief plus its own lens question. Experts are read-only: they research and report. Any resulting change goes to a single executor with one reviewer. Pin a cost-appropriate model on each subagent rather than letting it inherit the main model silently.
6. **Synthesize.** Report:
   - convergent findings (likely right),
   - disagreements, naming which evidence wins and why,
   - one recommendation with a confidence level,
   - dated citations carried through from the experts.
7. **Escalate shape if needed.** For a multi-lens audit of a whole codebase or system, switch to a dedicated fan-out review using these experts as the role bank rather than stretching the cap.

## Expert lane table (adapt to your own bench)

| expert | lane |
|---|---|
| coding | application code: write, review, debug, test, library versions |
| design | product UI/UX: flows, design systems, accessibility |
| architect | boundaries, data flow, queues, failure modes, decision records |
| ai-agents | LLMs, agent loops, tool use, evals, model choice |
| security | appsec, dependency CVEs, secrets hygiene, prompt-injection risk |
| data-eng | pipelines, schemas, databases, data-quality gates, backups |
| devops | CI/CD, runners, containers, deploys, releases |
| product-growth | strategy, pricing, funnels, experiments |

## When to use

- A question spans two domains, or needs current, cited research rather than a recall answer.
- You want a second specialist view but must stay within a machine or budget cap.
- You are about to fan out by reflex and want a bounded default instead.

## How to use

1. Copy this folder into `~/.claude/skills/` for personal use, or into `.claude/skills/` inside a project. Define your expert subagents (one per lane) separately; this skill only routes.
2. Ask Claude Code to use the `capped-expert-routing` skill by name.

Example prompts:

- "Use capped-expert-routing: should we move our job queue from polling to event-driven? Involve architecture and devops."
- "Use capped-expert-routing to review this auth change; pick the right experts, respect the 2-reader cap, and synthesize."
