---
name: preplan-interrogation-gate
description: Before locking a plan for autonomous or walk-away execution, run one bounded round of clarifying questions covering objective, constraints, and objectively-testable acceptance criteria — stopping once another answer wouldn't change the plan — so ambiguity gets resolved before there's no one left to ask.
---

# preplan-interrogation-gate

Once you hand a plan to an agent for unattended or long-running execution, there's no natural checkpoint left to ask "wait, what did you mean by X?" — every unstated assumption baked in at plan time becomes a silent, uncorrected guess for the rest of the run. Discovering that gap at the end, after hours of unattended work, is far more expensive than resolving it up front. The fix is a dedicated, deliberately bounded interrogation phase that runs before any planning starts.

## The method

1. **Front-load the questions.** Before writing any plan for work that will run with limited or no supervision, batch every clarifying question that could materially change the plan into one round (or a small handful). A handful of questions per round is usable; asking one at a time is slow, asking dozens at once isn't.
2. **Cover the load-bearing categories:** the objective and who/what it's for; hard constraints (technical, budget, timeline); any style/reference/taste preferences that matter for judged output; acceptance criteria phrased so each one is objectively testable, not subjective; the completion rule (stop at a draft for review vs. proceed automatically if checks pass); risk tolerance for anything destructive or hard to reverse; and any budget or time cap.
3. **Apply a stopping rule, not a fixed question count.** Stop asking once an additional answer would not change the resulting plan. Interrogation has its own cost — endless clarifying questions are a failure mode too, not just thoroughness.
4. **Never re-ask something already answered.** Check what's already stated in the task or earlier in the conversation before drafting questions.
5. **Fold every answer into the plan as a checkable item, not background context.** Each acceptance-criteria item collected this way should be precise enough to serve two roles at once: the executor's contract for what it's allowed to consider done, and the completion gate's rubric for what a verifier checks against.
6. **Close the interrogation phase before locking the plan.** Only after this phase is done do you move to writing and locking the actual plan (this pairs naturally with a hash-locked release step, if you already gate plan execution that way). Treat any requirement discovered after this point as a genuine plan revision, not a quiet in-flight adjustment.

## When to use

- Handing off any defined-end-state task to unattended or long-running autonomous execution, where you won't be present to answer a question mid-run.
- A recurring pattern where autonomous runs "guessed wrong" on something that was actually answerable up front, if only someone had asked.
- Auditing an existing plan-then-execute pipeline for missing acceptance criteria — if a criterion can't be checked objectively, it was under-interrogated.

## How to use

**Install:** copy this folder into `~/.claude/skills/preplan-interrogation-gate/` for personal use, or `.claude/skills/preplan-interrogation-gate/` inside a project repo.

**Invoke:**

```
Before you start this overnight build, run preplan-interrogation-gate — ask me
everything you'd need to know now, since I won't be around to answer once it starts.
```

```
That autonomous run guessed wrong about the deploy target. Next time, use
preplan-interrogation-gate to lock that down as an explicit acceptance criterion
before planning even starts.
```
