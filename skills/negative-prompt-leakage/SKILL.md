---
name: negative-prompt-leakage
description: When writing FORBIDDEN/NEVER/✗ example blocks in an LLM system prompt, never spell out the literal forbidden phrase — models pattern-match into the bad example and reproduce it; use a short abstract marker instead.
---

# negative-prompt-leakage

LLMs treat a "forbidden" example as an example of the shape the response should take, not just a label to avoid. If a ✗-block spells out the full bad sentence verbatim, the model has effectively been shown a copy-paste-ready template of exactly what you told it not to do — and it will produce that sentence far more often than if the bad pattern had never appeared in its context at all.

## When to use

- You're writing or editing any prompt (system prompt, tool instructions, an agent's persona/style guide) that includes a FORBIDDEN / DON'T / NEVER / ✗ list of bad examples.
- A model keeps producing an output you explicitly told it not to produce, despite the prompt listing it as forbidden — that's the signature symptom of this bug, not a sign you need a stronger warning.
- Before shipping any new negative example into a prompt that's already in production.

## The rule

**Don't write the full forbidden sentence:**
```
FORBIDDEN OPENERS:
  ✗ "Hey, I'm calling on behalf of a customer to ask about your hours."
  ✗ "Quick moment — I'm reaching out on behalf of someone to ask a question."
```

**Write a short, abstract pattern token instead:**
```
FORBIDDEN OPENER PATTERNS:
  ✗ 'on behalf of <someone>' — never use this preamble.
  ✗ 'quick moment' / 'quick minute' preamble.
```

The token names the *pattern*, not a ready-to-reuse sentence. The model can still understand and enforce the rule — it just no longer has a literal bad string sitting in its context that it can lift verbatim.

## Why this happens

This is an empirical failure mode, not a hunch: a production voice-AI prompt kept opening calls with a specific forbidden phrase despite the prompt explicitly listing that exact sentence as forbidden. Hours of "make the warning stronger" fixes failed, because the prompt was teaching the bad pattern in multiple places at once:

1. A "forbidden examples" block that spelled out the full bad sentence.
2. A second file with the same full-sentence ✗-example.
3. A third, unrelated code path that was *actively injecting* a similar phrase into the prompt at runtime — nobody had noticed because the injection looked intentional.

The fix was mechanical: replace every literal ✗-sentence with an abstract pattern token, switch the "here's what a good opener looks like" example to a **positive** example only, and delete the accidental runtime injection. After that, the forbidden phrase stopped appearing entirely — not "less often," gone.

## How to spot leakage before shipping a prompt change

| Smell | Fix |
|---|---|
| A full sentence sits inside a ✗ block | Replace it with an abstract pattern token |
| A ✗-block has 4+ examples | Cap it at ~2, and make each one more abstract |
| ✓ and ✗ examples share the same block | Split them — put ✗ in its own "forbidden" section |
| The ✗-example shares a 3+ word phrase with the actual task | It will leak — abstract it harder |
| The forbidden phrase shows up in more than one file | Search every prompt source, not just the one you're editing — fix every site |

When a forbidden phrase keeps appearing despite being "in the ✗-list," search all of your prompt sources for the literal bad text — you're very likely to find a second (or third) site quietly teaching it.

## When NOT to apply this rule

- **Deterministic detectors** — constants, regexes, or matcher tables that need the full literal phrase to match aren't prompts, they're code. `FORBIDDEN_PHRASES = ["on behalf of a customer"]` used in a string-match filter is correct as-is.
- **Docs and runbooks** that are never fed into an LLM's context — full examples are fine there, they're for a human reader.
- **Regression test fixtures** — a test suite that replays a known-bad output on purpose should keep the literal bad text, because the point is to prove the fix actually caught it.

The rule applies specifically to text that ends up inside an LLM's system prompt or a message it will read as context before generating.

## How to use

**Install:** copy this folder into `~/.claude/skills/negative-prompt-leakage/` for personal use, or `.claude/skills/negative-prompt-leakage/` inside a project repo so your whole team gets the same review pass on every prompt edit.

**Invoke:**

```
Before you save that system prompt change, run the negative-prompt-leakage check on
it — any full-sentence forbidden examples that should be abstract pattern tokens?
```

```
Our support bot keeps saying the exact phrase we told it never to say. Use
negative-prompt-leakage to find every place in our prompts that's accidentally
teaching it that pattern.
```
