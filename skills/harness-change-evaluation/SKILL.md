---
name: harness-change-evaluation
description: Test a change to an agent harness (prompt, rule, tool, hook, routing) as a hypothesis, using held-out real-failure tasks, one change at a time, a fixed model, and end-to-end scoring against a baseline.
---

# Harness change evaluation

Any change to the scaffolding around a model (a system prompt edit, a new rule, a tool, a hook, a routing policy) is a hypothesis, not an improvement. A demo, a single good trace, or the model's own report that it "follows the rule now" are not evidence. This skill is the smallest evaluation that can tell you whether a change helped.

## Method

1. **Collect cases from real failures.** Gather 20-50 tasks drawn from situations where the harness actually went wrong or was costly. Each case needs a clean starting state (a fixed repository snapshot or input set) and a known-good outcome you can check mechanically or with a rubric. Include some cases that should succeed and some that the change should leave alone.
2. **Keep the evaluation set private from the worker.** The cases must not appear in the prompt, rules, or retrieved context the agent sees, otherwise you are measuring memorization.
3. **Fix everything except one component.** Same model, same settings, same tools. Change exactly one harness component per experiment, so any difference has one cause.
4. **Run baseline first.** Record the unmodified harness on every case. Without a baseline, a score means nothing.
5. **Score end to end.** For each run record: task completed (yes/no against the known-good outcome), whether an independent reviewer accepts the result, cost (tokens or money), and wall time. Include a negative control: cases where the rule should not fire, so a change that only blocks things does not look like an improvement.
6. **Repeat for variance.** Agent runs are noisy. Run each case at least 2-3 times, or report ranges, and do not call a difference real if it is inside the noise.
7. **Decide with a pre-stated rule.** Write before running: "keep the change only if completion improves by at least N cases without more than M extra cost, or if it removes a named failure class." If it does not beat the baseline, revert it.
8. **Record the version.** Store the harness version or content hash next to the scores so a later regression can be traced.

## Common mistakes

- Grading with the same context that produced the work. Use a separate evaluator that sees the task, the output, and the command to re-run, not the worker's reasoning.
- Changing the prompt and the model in the same experiment.
- Using only the single failure that motivated the change as the test.
- Counting a rule as successful because it blocks things, without measuring what it blocked wrongly.
- Inferring quality from the model's self-report that it complied.

## Reporting format

Lead with the decision (keep, revert, or inconclusive), then a table: `case set | baseline | candidate | cost delta | time delta`, then the failure class addressed and anything the change made worse. Label the result with what the evidence supports; if only a few runs were possible, say the result is inconclusive.

## When to use

- You edited a system prompt, rules file, tool description, hook, or routing policy and want to know if it actually helped.
- You are choosing between two harness variants.
- A rule keeps accumulating and you need to know which parts earn their place.

Skip it for typo fixes and for changes whose effect is mechanically obvious and checked by a single deterministic test.

## How to use

1. Copy this folder into `~/.claude/skills/` for personal use, or into `.claude/skills/` inside a project.
2. Ask Claude Code to use the `harness-change-evaluation` skill by name.

Example prompts:

- "Use the harness-change-evaluation skill to design a 30-case test for the new rule I added to my project instructions, including a baseline and negative controls."
- "I have two versions of my review prompt. Use harness-change-evaluation to set up a fair comparison and tell me what decision rule to commit to before running it."
