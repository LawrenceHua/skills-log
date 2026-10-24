---
name: product-decision-bias-check
description: Review a product decision (pricing, free tier, defaults, feature removal, announced changes) with four bias questions about comparison, zero price, ownership, and expectation, without leaning on contested effect sizes.
---

# Product decision bias check

Engineers often treat a product decision as an argument to be won with better reasoning. Several well-known judgment effects are not reasoning failures. They describe how preference is constructed, and they apply to the person making the decision as much as to the user. A pricing page or default that ignores them is not neutral; it is accidentally choosing an anchor. This skill is a set of questions to ask about your own framing, not a set of numbers to cite.

## The four questions

### 1. Relativity: what is this being compared to?

People rarely judge an option against its value; they judge it against what sits next to it. A decoy tier that nobody buys can make the target tier look reasonable.

- Where it bites: three-tier pricing, a premium plan that exists mainly to anchor, and your own effort estimates, which are relative to the last task you did.
- Ask: what is this next to, and did I choose that comparison or inherit it?

### 2. Zero price: what does "free" buy, and who pays?

Free is a different category from a small price. It can create outsized demand and also remove the sense of obligation a small price creates, so free users behave differently, not only pay differently.

- Where it bites: a free tier that undermines paid conversion, a "free forever" promise made in a launch note, and internal work that is free to the requester but costly to the team (unpriced work is often treated as valueless work).
- Ask: what does free buy here, what is the second-order cost (support load, expectations, conversion), and who absorbs it?

### 3. Ownership: if it did not exist, would I ask for it?

Once a feature exists it acquires defenders, and the person who built it is badly placed to judge it. Sunk cost is the famous version; the product version is a roadmap that only grows.

- Where it bites: every "should we remove this" discussion.
- Ask: if this were absent today, would anyone request it? Who would notice if it disappeared?

### 4. Expectation: was this measured blind?

Telling people something is better changes how they report experiencing it. A user told the new version is faster may report it as faster.

- Where it bites: satisfaction and speed metrics collected after an announcement.
- Ask: did participants know what to expect before we measured?

## Caution on sources

Behavioral-economics popularizations from the late 2000s cite dramatic effect sizes, and some of the best-known studies have been questioned or retracted after data problems were reported. The broad finding, that preferences are context-dependent and constructed, is well supported across the field. Specific headline numbers from popular books are not. If a decision needs a number, get it from your own users, an experiment you ran, or a replicated study you have opened.

## Applying it in a review

1. Name the comparison. Every price, default, and plan sits beside something; write down what.
2. Check the free offering for second-order costs.
3. Ask the removal question for anything older than about two quarters.
4. Require a blind read for any metric that changed after an announcement.
5. Write the decision and its rationale down, because the next person will be inside a different bias and needs to know why this one looked obvious.

## One-line test

Would this decision still look right if the options had been shown in a different order?

## When to use

- You are about to set or change pricing, a free tier, a default, or a plan comparison page.
- A decision feels obviously correct and you want a quick sanity pass.
- You are reviewing someone else's product proposal or experiment readout.

## How to use

1. Copy this folder into `~/.claude/skills/` for personal use, or into `.claude/skills/` inside a project.
2. Ask Claude Code to use the `product-decision-bias-check` skill by name.

Example prompts:

- "Use the product-decision-bias-check skill on this pricing proposal and tell me which comparison and free-tier assumptions I have not examined."
- "We want to remove an old feature. Run product-decision-bias-check and list the evidence we would need beyond the team's opinion."
