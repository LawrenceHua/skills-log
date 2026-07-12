---
name: roast-me
description: Multi-round adversarial questioning that forces you to defend a design BEFORE you build it — generates hard questions across failure modes, edge cases, future-proofing, security, performance, and compliance, then iterates on your answers instead of accepting the first pass.
---

# roast-me

The fastest way to find the holes in a plan is to have someone hostile read it before you commit to building it. This skill is that hostile reader: it asks pointed questions and waits for you to actually answer them — it does not try to answer them for you, because doing so would defeat the entire point.

## When to use

- Before implementing anything bigger than a one-line change.
- Before sending a design doc, charter, or proposal to a stakeholder.
- Before locking in an architecture decision you'll find expensive to reverse.
- Whenever you catch yourself thinking "this should be straightforward" about something non-trivial — that's usually the moment a hostile pass finds the thing you didn't consider.

## What it does

1. **Take the input** — a design, a doc, a plan, or a description of a change you're about to make.
2. **Generate N hard questions** across these lenses:
   - **Failure modes** — "what happens if the dependency this relies on goes down?"
   - **Edge cases** — "what if the input is empty / malformed / arrives twice?"
   - **Future-proofing** — "what breaks when you need to add a third instance of this thing?"
   - **Security** — "what's the worst thing a malicious actor could do with this surface?"
   - **Performance** — "what does this look like at 100x the current scale?"
   - **Compliance / policy** — "does this touch any rule, law, or internal policy you haven't checked against?"
   - **Fit with your own stated principles** — "does this match the priorities you've already told me matter? Which ones, specifically?"
3. **Wait for the answers.** Don't self-answer — the value is in forcing the human (or the agent actually doing the work) to reason it through, not in generating a plausible-sounding Q&A pair.
4. **Run a second round** based on the answers, probing whatever weaknesses the first-round answers didn't actually address.
5. **Repeat** until one of: the user says stop, no new weaknesses surface, or you hit 5 rounds — most of the real value shows up in rounds 1-2; by round 4-5 you're usually into diminishing returns.

## Anti-pattern guardrails

- **Don't auto-answer your own questions.** The skill's job is to produce sharp questions; a human (or whoever owns the decision) answers them.
- **Don't get generic.** "Have you considered the user's needs?" is worthless. "This copy uses a word that conflicts with the tone rule you set last week — how do you reconcile that?" is the bar — specific, evidence-based, tied to something concrete.
- **Don't loop forever.** Hard cap at 5 rounds.
- **Don't replace judgment.** The questions surface gaps; a human still decides which gaps actually matter enough to act on.

## Output format

Per round:
```
ROUND N — questions to answer:

1. [security] If the third-party API key behind this feature leaks, what's the
   blast radius? Can a bad actor cause damage that gets billed to us?
2. [future-proof] What breaks when you need a second instance of this — where
   would you even add it?
3. [compliance] Does the relevant regulation require a specific disclosure
   here? Does your current flow show it, and at what point in the flow?
...

When you've answered, ask to roast again.
```

## How to use

**Install:** copy this folder into `~/.claude/skills/roast-me/` for personal use, or `.claude/skills/roast-me/` inside a project repo.

**Invoke:**

```
Roast me on this plan before I start building: [paste the design/plan].
Ask hard questions, don't answer them for me — I'll respond and you go again.
```

```
I'm about to lock in this architecture decision. Run roast-me on it — probe
failure modes, security, and what happens when we 10x scale.
```
