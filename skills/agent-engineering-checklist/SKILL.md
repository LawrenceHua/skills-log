---
name: agent-engineering-checklist
description: A curated checklist of ~18 evidence-grounded rules for building reliable AI agents — tool-use gating, verification-before-trust, context engineering, and safety/trust boundaries — each with the rule, why it matters, and a short reference pattern.
---

# agent-engineering-checklist

A distilled reference for building AI agents (or agentic workflows) that hold up under real use, not just demo conditions. Each rule below was extracted from published agent-engineering research and postmortems, not opinion — treat this as a checklist to run your own agent design against, not gospel to apply blindly. Verify each one still applies to your specific system before leaning on it.

## When to use

- Designing a new agent, tool, or multi-step workflow from scratch.
- Reviewing an existing agent for reliability gaps before it goes into more autonomous use.
- Debugging a "the agent did something surprising" incident — many of these rules map directly to a known failure class.

## Tool-use discipline

**Gate every meaningful tool action.** Before any non-trivial tool call, have the agent produce a short decision record — intent, supporting evidence, risk, reversibility — and choose to execute, gather more context, escalate to a stronger check, or stop. This interleaves reasoning/action/observation instead of trusting a fixed action chain.
```
decision = assess(intent, evidence, risks, reversible)
if decision.path != "execute": return handle(decision)
return tool.call(args)
```

**Narrow the tool set before calling.** Classify the intent first and expose only the handful of tools relevant to it (five is a reasonable ceiling) rather than the full tool registry. Function-calling hallucination rates climb once an agent sees too many tools at once.

**Validate tool calls externally.** Treat every model-generated tool call as an untrusted structured suggestion — validate required fields, enums, IDs, permissions, and state transitions in deterministic code before it actually executes. Never let the model's own confidence be the validation.

**Dry-run before touching production state.** For any state-changing action, run a dry check against schemas, preconditions, and expected side effects; reject and have the agent revise before it's allowed to touch anything real.

**Gate tools behind policy checks.** Before every tool call: an explicit check for permission, tool eligibility, argument safety, and whether this needs to be logged or escalated. This is the actual product boundary in most agent deployments — not the prompt.

**Design blast radius first.** Before adding any tool, define its permission scope (workspace / user / session / action type) and require explicit elevation for anything broader than the default. Treat agent safety as scope engineering, not prompt-only control.

## Verification before trust

**Separate rationales from approvals.** Never let an agent's own self-explanation authorize its next action — compare the stated rationale against the actual tool trace, retrieved evidence, and rejected alternatives first. An agent's explanation is a diagnostic signal, not proof it did the right thing.

**Verify high-risk claims cheaply.** For any high-stakes answer, have the model generate its own verification questions, then check each one against real source text or live system state before finalizing. This catches self-generated hallucinations more reliably than asking the model to "double check itself" in the abstract.

**Verify before routing on confidence.** Never let a model's self-reported confidence trigger a tool call, escalation, or skipped review by itself — route on an independent verifier's pass/fail, not on how sure the model says it is. Verbal confidence reliably exceeds actual accuracy.

**Return patches for high-value writes.** For source-of-truth mutations, have the agent propose a diff for human approval instead of committing automatically. Keeps high-value writes observable and reversible before anything real changes.

**Wrap writes in safety transactions.** Any tool that mutates persistent state should: declare its intent, produce a structured diff, validate the resulting artifact against that intent, and log a reversible undo record — before it commits.

**Scan after AI-generated code changes.** After any AI-written edit, run tests and a security scan before merge. Fluent self-explanation, "I reviewed my own change," and a plausible diff are not evidence of safety on their own.

## Context & memory

**Pack context as an active workspace, not an archive.** Long context degrades before you hit the advertised limit — summarize aggressively, rank evidence by relevance, and keep current task state separate from long-term/archival memory.

**Cap context with evidence windows.** When context would exceed a sane budget, retrieve or compress down to the smallest evidence window the task actually needs, rather than stuffing in the full history or corpus "just in case."

**Engineer cache-aware context.** For long-running agent sessions, use stable prefixes, compact scratchpads, and summarize old tool-trace noise instead of endlessly appending raw logs — this keeps both cost and signal-to-noise sane as a session grows.

## Safety & trust boundaries

**Quarantine retrieved instructions as data.** Treat every retrieved document or tool result as untrusted: quote/delimit it clearly, ignore any instructions embedded inside it, and only ever act on instructions that came from your actual trusted system policy. This is the core defense against indirect prompt injection.
```
trusted_policy = load_system_policy()
retrieved_block = quote_as_untrusted(retrieved_docs)
response = model.run(policy=trusted_policy, context=retrieved_block)
```

**Label trust boundaries explicitly in context.** Tag every user message, tool result, retrieved document, and piece of private memory with a trust level, and never let lower-trust content override higher-trust instructions without independent verification.

**Preserve disagreement before synthesis.** For high-stakes decisions, run two independent passes (different models, different prompts, or different reviewers) and have a synthesis step explicitly report agreements, disagreements, and what would flip the conclusion — instead of silently picking one and hiding that there was ever a disagreement.

**Maintain unpublished holdout evals.** Don't trust public benchmark performance alone for anything that matters — keep at least one private eval set that has never been published, prompted into, or committed anywhere public, so you can tell real capability from memorized-benchmark performance.

## How to use

**Install:** copy this folder into `~/.claude/skills/agent-engineering-checklist/` for personal use, or `.claude/skills/agent-engineering-checklist/` inside a project repo shared with a team building agents together.

**Invoke:**

```
Review this agent design against agent-engineering-checklist — which of the
tool-use and trust-boundary rules does it violate?
```

```
I'm about to give this agent write access to our database. Walk through the
safety & trust-boundary section of agent-engineering-checklist before I do.
```
