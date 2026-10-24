---
name: document-evidence-audit
description: Stress-test a research or strategy document before anyone acts on it by checking that every number has a source or is flagged as a judgment, every link resolves, the arithmetic is consistent, key risks are addressed, and unknowns are stated.
---

# Document evidence audit

A confident document is convincing by construction: it has sources, percentages, and fluent prose. None of that is evidence the numbers are real. Careful reading produces the first version of a document; it does not audit it. Run this audit before you repeat a figure from any document, including one you wrote yourself.

## The five checks

### 1. Every number carries a citation or admits it is a judgment

Scan every percentage, multiple, currency figure, count, and date. Each one needs, within a few lines, either:

- a source link, or
- an explicit marker such as "my assumption", "I chose this", or "a judgment, not a measured value".

A number with neither is the most common failure and the most dangerous, because it reads exactly like a sourced number. The test: a skeptical reader should be able to tell, for every figure, whether it came from evidence or from the author.

### 2. Every source resolves

Fetch each link and record the status. Three failures all look like citations in prose:

- **Typo in the URL** (trailing punctuation, a doubled path segment). It never resolves and nobody notices because it looks right.
- **Access denied to a non-browser client** (401/403). The page exists but a checker cannot read it, so the claim is unverifiable by that checker.
- **Soft 404.** A 200 response that actually serves "page not found".

Then open the live page and confirm it says what the document claims it says. A dead or unreadable source is a fabricated source in practice: if nobody can check it, it is not evidence.

### 3. The arithmetic is internally consistent

Recompute rather than eyeball:

- A growth rate that cannot produce the stated multiple (rule of 72: 72 / rate% is roughly years to double).
- A cumulative figure that does not match the annualized one.
- A drawdown or loss larger than the gain that preceded it, presented as a net positive.
- Percentages that do not sum to the total they claim to describe.
- Units mixed between rows (monthly vs yearly, thousands vs millions).

### 4. Costs, downside, and sample window are addressed

For any document that recommends an action with a payoff, four things decide whether it is real:

| Must be present | Because |
|---|---|
| Costs (fees, friction, labor, maintenance) | An edge smaller than its costs is not an edge. |
| Taxes or other deductions, where they apply | A return the owner cannot keep is not the return. |
| Worst case or drawdown | It decides whether a real person can live with the plan. |
| Sample period or window | A claim without a window is a claim about nothing. |

A document with upside and no downside is a pitch, not research.

### 5. The document states what it could not determine

Search for phrases like "could not", "unknown", "unverified", "inconclusive", "not determined". Every real investigation has unknowns. A document with none is either trivial or hiding something, and the second is far more likely. An honest gap is worth more than a confident guess.

## How to run it

1. Extract every figure into a table: `line | figure | cited? | source resolves? | recomputed OK?`. A short script that greps for digits, percent signs, and currency symbols makes this fast; the judgment calls stay manual.
2. Fetch all links in one pass and record status codes. Open any that return success but look suspiciously thin.
3. Recompute every derived number with a calculator or script, not mentally.
4. Walk the four required topics in check 4 and mark each present, partial, or absent.
5. Search for the unknowns section. If it is absent, that is a finding.
6. Then do the part no tool can do: for each claim ask, "how would I check this if I did not believe it?" If the answer is "I couldn't", that is a finding.
7. Report findings with line numbers so the author can fix them instead of arguing.

## Rules

- Run it on your own work first. It will find things; that is the point.
- Passing means "the numbers are what they say", not "the conclusion is right". The audit checks honesty, not profitability or wisdom.
- Never weaken a check to make a document pass. If a threshold is wrong, change it openly and say so.
- When a probe reports a defect in something you already verified, suspect the probe first (a truncated read, a quoting error, a partial download) before concluding the document is broken.

## When to use

- Before reporting research findings to a person who will act on them.
- Before any irreversible, costly, or financial decision.
- When an agent hands you a confident document and you are about to trust it.
- When re-examining earlier work to learn which claims survive.
- Before citing a source you have not personally opened.

Skip it for trivial lookups and for statements that are only a receipt ("I ran this command and it printed X"); re-run the command instead.

## How to use

1. Copy this folder into `~/.claude/skills/` for personal use, or into `.claude/skills/` inside a project.
2. Ask Claude Code to use the `document-evidence-audit` skill by name.

Example prompts:

- "Use the document-evidence-audit skill on `report.md` and give me a findings table with line numbers before I send it."
- "An agent wrote this strategy memo. Run document-evidence-audit on it, fetch every link, and tell me which figures are unsourced."
