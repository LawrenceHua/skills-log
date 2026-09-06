---
name: ai-eval-rigor-checklist
description: A checklist of ~20 evidence-grounded rules for evaluating AI models, agents, and RAG pipelines rigorously — eval design, retrieval-grounding tests, agent-trajectory grading, and precise language for deletion/unlearning claims — distinct from building the agent itself.
---

# ai-eval-rigor-checklist

Most eval mistakes aren't in the model or the agent — they're in the eval itself: a single seed presented as a score, a benchmark result with no provenance, a "the agent succeeded" verdict that only checked the final answer and ignored how it got there. This is a checklist to run your own evaluation harness against, organized by what you're evaluating. Pair it with a general agent-reliability checklist for how to *build* the agent — this one is about how to trust the number you got when you measured it.

## When to use

- Designing a benchmark or eval harness for a model, agent, or RAG pipeline.
- Reviewing someone else's (or your own past) eval results before trusting them for a routing or release decision.
- Before switching models, checkpoints, or quantization levels on a system already in use.
- Writing up a deletion, unlearning, or "we removed that data" claim that needs to survive scrutiny.

## Eval design fundamentals

**Evaluate across repeated seeds.** A single sampled score is a point estimate with unknown variance. Run multiple seeds and report mean, variance, and confidence intervals — a model that "wins" by less than the seed-to-seed noise hasn't won anything.

**Record eval provenance fields.** Every benchmark result needs its seed, run ID, exact model/checkpoint, dataset version, and sampling configuration recorded before it's allowed to inform a routing or release decision. A score with no provenance can't be reproduced or audited later.

**Define four-part simulation evals.** For agent evals, specify all four of: a sandboxed target environment, difficulty-controlled inputs, the exact tools/permissions available, and an objective grader — before running the model. Skipping any one of these turns the eval into vibes.

**Test across operator personas.** Run the same task with expert, intermediate, and novice user profiles under identical model/tools/time budget, and compare outcomes separately. A system that only works when the user already knows the right way to phrase things will fail in production.

**Version every routed call.** When routing across models, attach the model ID, prompt version, route reason, timeout, fallback target, and a trace ID to every call. Without this you can't explain after the fact why a given request went where it went.

**Replay traces before upgrades.** Before switching any model, checkpoint, or quantization level, replay real historical traces grouped by failure category (failed tool calls, long-context summarization, retrieval grounding, etc.) — don't trust a benchmark delta alone to predict a production regression.

## Retrieval & grounding evaluation

**Track provenance through RAG answers.** Preserve source URL, source family, retrieval timestamp, and an explicit claim-to-source mapping for every generated answer, and require citations for anything touching policy, finance, medical, or legal content.

**Test RAG evidence dependence.** Run the same question three ways — with supporting evidence, with no evidence, and with distractor evidence — and only pass the system if the answer actually tracks which evidence it was given.

**Counterfactually test RAG evidence.** Remove or swap the retrieved evidence for a known-good answer and require the system to change its answer, abstain, or fail its own citation check — an answer that stays the same regardless of evidence is reciting memorized text, not grounding in retrieval.

**Partition evals by knowledge zone.** Label every knowledge-eval item as known, boundary, or unknown ahead of time, then report accuracy, refusal rate, and confidence separately per zone — a single blended accuracy number hides whether the system knows what it doesn't know.

**Probe correct boundary answers before trusting them.** A single correct answer near a knowledge boundary is not evidence of real knowledge until it survives paraphrases, calibrated-confidence checks, and adjacent-unknown probes — boundary correctness is disproportionately likely to be lucky.

## Agent trajectory evaluation

**Grade trajectories, not just answers.** Score the tool calls, retries, permission requests, loops, and any production-invalid shortcuts an agent took, in addition to final task success. Two agents that reach the same correct answer are not equally trustworthy if one got there by silently retrying a destructive action.

**Score complete agent traces.** Evaluate the plan, the retrieval step, the tool choices, any self-correction behavior, and the final answer as separate scored dimensions — not one pass/fail verdict for the whole run.

**Score full fuzzy trajectories for safety evals.** Safety-relevant evals need multi-step scenarios with real tools, partial information, and user nudges toward a bad action, scored across the whole trajectory (what it asked, what it assumed, whether and how it refused) — not a single-turn refusal prompt.

**Perturb tasks to test invariants.** Generate paraphrase, reorder, rename, and equivalent-format variants of the same task and assert that the agent's intermediate commitments stay semantically identical across all of them. An agent that only works on the exact original phrasing has memorized the eval, not solved the task.

**Perturb planner dependencies.** For multi-step planners, change exactly one input dependency and assert that only the plan nodes and tool calls actually downstream of that dependency change — anything else moving indicates the planner is coupling state it shouldn't.

**Assert agent hidden-state contracts.** Treat an agent's plans, memories, retrieved snippets, tool arguments, router choices, and summaries as first-class outputs with explicit contracts you can inspect and test — not internal scratch space you only look at when something visibly breaks.

**Add one hidden-property eval per pass/fail check.** For every output-level pass/fail eval, add a direct check for the underlying property you actually care about — state consistency, evidence dependence, recoverability — because pass/fail alone can hide the exact failure mode you're trying to prevent.

## Precise language for deletion & unlearning

**Name the forgetting control precisely.** Never call an intervention "unlearning" unless it actually targets data-influence deletion. If it doesn't, label it what it is: behavior suppression, policy adaptation, or exposure reduction. Overclaiming the mechanism misleads anyone relying on the guarantee.

**Match deletion claims to stronger probes.** Any claimed data deletion needs before/after extraction tests, membership-style probes, regression checks, and adversarial prompts — not just "we removed the source and the model doesn't say it anymore in casual testing."

## Reproducibility & versioning

**Select prompts on held-out tasks.** When evolving prompts, reflections, workflows, or playbooks, generate candidates on a training split and pick the winner only on a validation split the optimizer never saw — otherwise you're overfitting the prompt to the exact eval set.

**Version agent text artifacts as code.** Every generated prompt, checklist, reflection, workflow, or playbook should carry a parent ID, a diff against its predecessor, its measured metrics, the decision made, and an archive of rejected candidates — treat prompt evolution with the same rigor as code review.

**Test hallucination failure patterns explicitly.** For RAG, memory, and agent-feedback systems, evaluate for the recurring hallucination patterns specifically — persistent false memories that survive correction, synthetic-summary drift compounding across turns, and source misattribution — rather than a generic "did it hallucinate y/n" check.

## How to use

**Install:** copy this folder into `~/.claude/skills/ai-eval-rigor-checklist/` for personal use, or `.claude/skills/ai-eval-rigor-checklist/` inside a project repo shared with a team building or evaluating AI systems together.

**Invoke:**

```
Run our RAG eval design against ai-eval-rigor-checklist — are we testing
evidence dependence and boundary knowledge, or just blended accuracy?
```

```
Before we say this fine-tune "unlearned" the flagged data, check the
deletion & unlearning section of ai-eval-rigor-checklist.
```
