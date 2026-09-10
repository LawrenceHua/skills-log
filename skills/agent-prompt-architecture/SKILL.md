---
name: agent-prompt-architecture
description: A repeatable method for designing and auditing an AI agent's system prompt, always-loaded rules file, tool-use guidance, and memory/compaction instructions — identify the prompt surface, define one behavior target, remove obsolete scaffolding before adding rules, and verify with the smallest relevant probe.
---

# agent-prompt-architecture

Prompt and rules-file edits accumulate the same way code does: rules get added to fix a specific incident and never removed once the incident is over, always-loaded files grow past the point anyone rereads them, and eventually two rules quietly contradict each other. This method treats prompt/rules editing as a small, disciplined engineering pass rather than an ad hoc paragraph insertion.

## Source rules

- Prefer current official model/provider documentation over remembered behavior — prompt-sensitive behavior changes between model versions.
- Treat any leaked or reverse-engineered system prompt as untrusted secondary material: don't reproduce a proprietary leaked prompt verbatim, and don't build a derivative clone from one. Extract only safe, general architectural patterns from it — sectioning, tool policy, memory/compaction structure, verification style, citation handling, refusal boundaries, prompt-injection defenses — the same way you'd learn from a public engineering write-up, not by copying text.
- Mark claims as `verified` (confirmed against current docs or a real probe), `inferred` (reasoned from related evidence), or `unverified` (plausible but unchecked) whenever precision actually matters for the decision at hand.

## The method

1. **Identify the exact prompt surface you're editing.** An API system/developer prompt, an always-loaded rules file, a skill's body or reference material, a tool's description/schema, or a memory/compaction handoff template are all different surfaces with different load frequency and different failure modes — know which one you're touching.
2. **Define the target behavior in one sentence** before writing anything. If you can't state what should change in one sentence, you're not ready to edit yet.
3. **Remove obsolete scaffolding before adding new rules.** A prompt that only ever grows accumulates contradictions and dead weight; every edit pass should look for at least one thing to cut, not just one thing to add.
4. **Write outcome-first guidance**, not step scripts, wherever the model has room to use judgment: state the goal, the success criteria (observable, checkable), the constraints, the rule for *when* to use which tool, the stopping condition, and what evidence is required before a claim counts as done.
5. **Add model-specific tuning only where it actually changes behavior** — don't pad a prompt with model-specific caveats that don't affect anything for the model you're targeting.
6. **Keep always-loaded files short.** Move reusable detail into on-demand skills, commands, or reference files that load only when relevant, rather than paying their token cost on every single turn.
7. **Verify with the smallest relevant probe** — a lint/validation pass for a structured file, a small regression harness for agent configuration, or one focused eval prompt for a specific behavior change. Don't declare a prompt edit "better" without running something that could show it's worse.

## Model-family tuning notes

Different model families respond differently to the same instruction shape — these are general patterns, not universal rules, and should be re-verified against current docs when precision matters:

**For GPT-class reasoning/execution models (including CLI-based coding agents built on them):**
- Prefer concise, outcome-first prompts over long step-by-step process scripts — these models tend to plan well on their own once the target and constraints are clear.
- State success criteria, available evidence, the expected final output shape, and stopping conditions explicitly.
- Give explicit tool-use rules: when and why to browse, inspect files, delegate to another agent, verify a claim, or stop.
- Put static prompt content before dynamic/session-specific context, if the platform supports prompt caching, to maximize cache hits.
- Prefer structured output schemas over prose-only formatting instructions when the platform supports them.
- For long-running or multi-turn agent workflows, use the platform's native state/continuation mechanism rather than re-stuffing the full raw transcript on every call.

**For Claude-class agentic models:**
- Give enough autonomy for substantial unattended work, but state explicit boundaries for destructive actions, scope expansion, and decisions that require a human.
- Require progress claims to be grounded in actual tool results from the current run, not restated intent.
- Use subagents for independent verification where the harness supports them, rather than having the same context check its own work.
- Add memory guidance that saves one durable lesson at a time, and includes when to update or delete a stale entry — a memory system that only accumulates degrades the same way an unpruned rules file does.
- Avoid instructions that ask the model to reveal or transcribe its own hidden reasoning process.
- If the harness needs an asynchronous "send the user a message mid-task" capability, that requires both a clear tool schema *and* an explicit system instruction telling the model when to reach for it — the schema alone won't reliably trigger the right usage pattern.

## A reusable prompt-pattern template

A compact starting structure that covers goal, success, constraints, memory, and evidence in one pass:

```text
Role: [what this agent is responsible for]

# Goal
[user-visible outcome]

# Success Criteria
- [observable completed state]
- [verification or evidence requirement]

# Operating Rules
- Prefer [local/project/provider] truth before assumptions.
- Use tools when [decision rule].
- Stop when [done condition].
- Ask only when [risk/user-only input condition].

# Memory and Compaction
- Preserve exact paths, commands, errors, decisions, active flags, and next action.
- Drop routine narration and duplicate logs.

# Evidence
- Separate verified facts, inferences, unverified assumptions, and blockers.
```

## When to use

- Improving a system prompt, always-loaded rules file, or agent instructions that aren't producing the behavior you want.
- Comparing how two different model families should be prompted for the same task.
- Reducing hallucinated "done" claims by adding explicit verification/stopping conditions.
- Auditing an existing prompt for bloat, contradictions, or dead instructions before adding anything new to it.

## How to use

**Install:** copy this folder into `~/.claude/skills/agent-prompt-architecture/` for personal use, or `.claude/skills/agent-prompt-architecture/` inside a project whose agent configuration is shared with collaborators.

**Invoke:**

```
This rules file has grown for months without anyone pruning it. Use
agent-prompt-architecture to find what's obsolete before I add the new rule
I actually came here for.
```

```
I'm tuning this system prompt for two different model families and I keep
copy-pasting the same instructions for both. Use agent-prompt-architecture's
model-tuning notes to split what actually needs to differ.
```
