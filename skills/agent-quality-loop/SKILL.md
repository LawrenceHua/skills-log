---
name: agent-quality-loop
description: Iteratively grade and improve a conversational AI agent's prompt quality without needing real end-users — run synthetic dialogs through it, score them on deterministic hard checks plus an LLM judge, then apply targeted human-approved prompt edits between rounds until quality plateaus.
---

# agent-quality-loop

For any prompt-driven conversational agent (voice, chat, SMS — anything with a system prompt and a set of expected behaviors), you can measure and improve quality without needing a stream of real user interactions. Run a fixed set of synthetic scenarios through the agent, score the results on both mechanical checks and an LLM judge, and iterate on the prompt with a human (or you) in the loop — never auto-editing based on the judge alone.

## When to use

- After any meaningful change to a conversational agent's system prompt.
- Before a demo or release, as a regression gate beyond your unit tests.
- Whenever someone says "test this yourself and make it better" about a prompt-driven agent.

## What one round does

1. **Load a fixed scenario set** — a handful (10-20 is plenty to start) of realistic conversations covering your agent's main behaviors and edge cases, written once and reused every round so scores are comparable over time.
2. **Run each scenario as a synthetic dialog.** Use the real system prompt against scripted user turns (or an LLM playing the "other side" of the conversation for scenarios that need a reactive counterpart). Capture every turn the agent produces, plus any tool calls.
3. **Grade each scenario on two layers:**
   - **Hard checks** (deterministic, code — not an LLM call): did the right tool get called with the right arguments? Are there banned phrases? Does the response meet a length/format constraint? Did it fabricate any fact it shouldn't have?
   - **LLM judge** (a fast/cheap model, scored 1-5 across a few axes you define — e.g. naturalness, correctness, conciseness, no-fabrication).
4. **Compute a composite score per scenario** and an overall pass rate, and write it to a results report.

## What "good" looks like (set your own bar, then hold it)

- 100% hard-check pass rate across all scenarios.
- LLM judge average at or above your chosen threshold (e.g. 4.3/5).
- No single scenario scoring below your floor on any individual axis.
- **Stable across repeat runs** — cheap/fast judge models have real run-to-run flakiness (a few percent isn't unusual), so don't trust a single round when deciding if you've plateaued; require 2-3 consecutive stable runs.

## Loop control — author-in-the-loop, never auto-edit

This is a **human-in-the-loop** loop. The judge finds problems; a human (or an agent working under explicit approval) writes the fix. Never let an LLM auto-apply prompt edits based on its own judge score — that's the fastest way to silently degrade a prompt while the numbers look fine.

Each round:
1. Run the scenario set (a few minutes, and budget a few cents to low tens-of-cents in judge-model cost per round).
2. Read the results — find the worst-scoring scenario.
3. Read its actual turns and the judge's specific feedback.
4. Make one targeted, minimal prompt edit (a couple of lines, not a rewrite).
5. Re-run your full existing test/eval suite to confirm no regression elsewhere.
6. Re-run the scenario set — confirm the targeted scenario improved AND nothing else got worse.
7. Repeat until you hit your target or plateau.

**Stop conditions:**
- Target hit → done.
- 3 consecutive rounds with no composite-score improvement → plateau, stop and reassess the approach rather than keep iterating blindly.
- A prompt edit causes a regression elsewhere → revert and try a different angle instead of stacking another fix on top.
- A generous round cap (e.g. 10) without convergence → stop, write up what you tried, and get a second opinion before continuing.

## Anti-patterns to avoid

- **Auto-editing prompts from the judge's output.** The judge flags problems; a human (or an explicitly-approved agent edit) writes the fix.
- **Running the loop when nothing changed.** Judge calls cost real money — only re-run after an actual prompt edit.
- **Trusting a single round for a plateau/regression call** — cheap judge models are flaky; require repeat-run stability before concluding anything.
- **Softening the rubric when scores don't improve.** If the prompt genuinely isn't getting better, tighten the prompt — don't lower the bar to make the numbers move.
- **Adding new scenarios mid-iteration.** That resets your baseline mid-comparison. Add new scenarios only at the start of a fresh measurement phase.

## What this loop does NOT cover

Be explicit about what's out of scope so nobody mistakes a green loop for full coverage: audio/voice tone quality (only a human listening can judge that for voice agents), latency, and anything downstream of the prompt (the actual telephony/messaging integration, for instance) — those need their own separate tests.

## How to use

**Install:** copy this folder into `~/.claude/skills/agent-quality-loop/` for personal use, or `.claude/skills/agent-quality-loop/` inside a project repo. You'll need to write your own scenario set and hard-check logic for your specific agent — this skill is the loop methodology, not a plug-and-play scorer.

**Invoke:**

```
Run an agent-quality-loop round on the support-bot prompt I just edited — score
it against our scenario set, find the worst scenario, and propose one targeted
fix before we re-run.
```

```
Set up an agent-quality-loop for this new voice agent: help me write 15 scenarios
covering the main flows and edge cases, define the hard checks, and pick a judge
rubric.
```
