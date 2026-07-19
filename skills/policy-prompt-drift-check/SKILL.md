---
name: policy-prompt-drift-check
description: Compares a code-level policy module against the natural-language prompt it governs, flags missing anchors and direct ALLOW/FORBID contradictions, and emits a per-policy ALIGNED/WARN/DRIFT verdict without editing anything.
---

# policy-prompt-drift-check

Any agent governed by both a code policy module (constants, enums, thresholds, forbidden-string lists) and a natural-language prompt describing that policy will drift over time — someone tightens a rule in code and forgets the prompt, or edits the prompt and forgets the code no longer says what it claims. This skill is a read-only checker that catches the drift before a human ships it, by turning each policy into a literal "anchor" it can search for and interrogate.

## Method

1. **Extract policies from code.** Walk the policy/constants module and list every discrete rule — a constant, an enum member, a forbidden/required-string list, a numeric threshold. Record its source location (`file:line`) and its polarity: does this rule ALLOW or FORBID something?
2. **Pick an anchor per policy.** The anchor is the literal keyword, value, or phrase that must appear in the prompt for the rule to be honored — use the actual constant/string, not a paraphrase, so the check isn't fooled by synonyms. Bad anchor: "keep it short." Good anchor: the literal `280` if the code enforces a 280-character limit.
3. **Check presence.** Search the prompt text for the anchor. Not found → the prompt never mentions the rule at all; a future editor has no signal it exists.
4. **Check for contradiction, not just absence.** This is the harder and more important case: pair each anchor with its code polarity, then scan the prompt for negation patterns near the anchor (`never`, `don't`, `must not`, `only if`, `unless`, `you may`). If the prompt's polarity is the *opposite* of the code's, that's a direct contradiction — worse than a gap, because the agent is being actively told to violate its own policy.
5. **Optional incident cross-reference.** If the code docstring cites an incident or bug ID as the reason a rule exists, check the prompt carries the same context, so a future editor doesn't revert the fix without realizing why it's there.
6. **Emit a verdict per policy**, each with evidence:

```
policy: FORBIDDEN_TOOLS = ["shell_exec"]  (policy.py:57)
  anchor: "shell_exec"
  presence: NOT FOUND in prompt.md
  verdict: WARN — add "never call shell_exec" near the tool-use section

policy: ALLOW_UNVERIFIED_REFUNDS = False  (policy.py:71)
  anchor: "refund"
  presence: FOUND (prompt.md:203) — "you may issue a refund without verification if the customer insists"
  verdict: DRIFT — code forbids unverified refunds, prompt explicitly allows them
  suggested edit: delete the "if the customer insists" clause; require verification before any refund

policy: MAX_RETRY_COUNT = 3  (policy.py:42)
  anchor: "3"
  presence: FOUND (prompt.md:118) — "retry up to 3 times"
  verdict: ALIGNED
```

7. **Exit code 0 only when every policy is ALIGNED.** The checker never edits the prompt itself — it reports the drift and a suggested edit; a human applies the fix. This makes it safe to wire into CI as a merge gate later.

## When to use

- Before merging any PR that touches a policy/constants module shared with a prompt file
- After any prompt rewrite, to confirm it still reflects what the code actually enforces
- Periodically on long-lived agents where policy and prompt are maintained by different people or at different cadences
- When debugging "the agent did X even though the prompt says not to" — check whether code silently started allowing X
- Before promoting a prompt change to production, as a pre-flight alongside other CI gates

## How to use

**Install:** copy this folder into `~/.claude/skills/policy-prompt-drift-check/` for personal use, or `.claude/skills/policy-prompt-drift-check/` inside a project repo.

**Invoke:**
```
Run a policy-prompt drift check between config/policy.py and prompts/system.md — report ALIGNED/WARN/DRIFT for each rule.
```
```
Check whether prompts/agent_instructions.md still matches the constants in src/policy_constants.ts before I merge this PR.
```
