---
name: research-decision-brief
description: "Turn a contested research question into a conditional recommendation grounded in source evidence and contextual acceptance checks."
---

# Research decision brief

Produce a defensible choice from competing explanations or approaches. The deliverable is a compact argument with evidence, limitations, and a condition that would change the choice.

## When to use

Use when a research answer must inform a decision: choosing an approach, assessing a disputed claim, or comparing a proposal against a viable alternative. A simple factual lookup or open-ended reading list usually needs less structure.

## Working method

### 1. Make the question answerable

State one question in this form: "Given these constraints, should we prefer this approach over the strongest alternative, and under what conditions would that choice change?"

Record the relevant population or setting, intended outcome, timeframe, resource constraints, and user-supplied acceptance criteria. Separate hard requirements from preferences. If a missing fact could reverse the recommendation, ask for it or make the recommendation explicitly conditional. Do not silently invent a requirement.

Set an evidence budget: time, sources to inspect, or a small number of decisive checks. Define the decision that the research will support; research alone does not authorize implementation or publication.

### 2. Identify live alternatives

List the plausible competing explanations or approaches, including the current approach when relevant. Avoid padding with obviously inferior options. For each, identify its strongest argument, the assumptions it needs, and the observation that would distinguish it from its nearest competitor.

Note where disagreement actually lies: different objectives, different evidence, incompatible assumptions, or different tolerance for uncertainty. This determines what to read next.

### 3. Triage and read sources

Rank candidate sources by relevance to the question, methodological rigor, and recency where facts may change. Consider primary evidence, study design, sample quality, disclosed limitations, and applicability. Recency alone does not outweigh stronger evidence.

Read the actual source before using it for a material claim. Search snippets, titles, and secondhand citations are discovery leads. If the source is inaccessible, mark that limitation and avoid attributing an unverified finding to it. Trace pivotal secondary claims to primary evidence when feasible.

Use authorized local material when sufficient. Do not send private documents or revealing search terms to external services without permission. If external research is unavailable, state the resulting coverage limit.

### 4. Build a claim ledger

Use a compact table:

| Claim | Supporting evidence and locator | Counter-evidence and locator | Inference or limitation | Status |
|---|---|---|---|---|

Give each material claim a stable label and a source locator a reader can follow, such as a section, page, or table. Separate what a source observed from your interpretation of it. Mark numerical estimates as measured, reported, or inferred.

Use `SUPPORTED` for claims with relevant positive evidence, `CONTESTED` for substantive conflicting evidence, `UNSUPPORTED` when positive evidence is absent, and `INCONCLUSIVE` when the available evidence cannot discriminate between alternatives. A supported claim may still have limited applicability. Do not count repeated reports of the same underlying study as independent confirmation.

### 5. Test the emerging recommendation

Assess each dimension with `PASS`, `WEAK`, or `FAIL` and one evidence-based reason:

- **Validity:** Does the evidence answer the question, and can its findings transfer to this setting?
- **Feasibility:** Can the approach satisfy the stated time, resource, and implementation constraints?
- **Ethics:** Are the relevant privacy, consent, fairness, and harm concerns acceptably addressed?

Use `WEAK` for a material uncertainty; missing evidence is not a pass. Record each hard acceptance criterion separately with its evidence and result. A failed hard requirement excludes an unconditional recommendation even if the average comparison favors that option.

### 6. Try to overturn the decisive claims

Select the few claims whose failure would change the choice. For each, state a falsifying observation and perform a bounded check: inspect an opposing source, examine a methodological limitation, or test a boundary case using available evidence. A second reader can help if available; do not imply an independent review occurred when it did not.

Require positive supporting evidence before retaining a claim. Failure to find a contradiction never establishes truth. Record what was checked, what it showed, and what remains unresolved. Update the ledger and recommendation when the check changes their basis.

### 7. Deliver the decision brief

Use this compact structure:

1. **Question and constraints.** Include the decisive acceptance criteria.
2. **Conditional recommendation or inconclusive result.** State the choice and the condition that would reverse it.
3. **Why this choice.** Compare the strongest alternative using the claim ledger and source locators.
4. **Checks and limitations.** Include validity, feasibility, ethics, acceptance results, and adversarial findings.
5. **Next decisive evidence.** Name the smallest missing observation that could change the decision, if any.

Stop when additional evidence within scope is unlikely to change the choice, or when the agreed budget is exhausted. Budget exhaustion limits the conclusion; it does not make an unresolved question settled. Return an inconclusive result when evidence cannot justify a choice.

## How to use

Copy the `research-decision-brief` folder into `~/.claude/skills/` for personal use, or `.claude/skills/` inside a project. Then ask Claude Code to use the skill by name.

- "Use research-decision-brief to compare a rules-based classifier with a model classifier under the latency and accuracy requirements in this document."
- "Use research-decision-brief on these supplied studies. Recommend whether the proposed intervention fits our stated constraints, and identify evidence that would reverse the recommendation."
