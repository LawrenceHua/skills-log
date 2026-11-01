---
name: claim-provenance-fields
description: Word a probe result as a claim a stranger can re-run — name the probe, artifact, control and reference behind every number, spot the six shapes of a true-looking but void claim, and pick the right status label.
---

# Claim provenance fields

A claim's value is decided by the probe behind it and its honesty by how it is worded. This skill is the second half: how to state a result so a stranger can re-run it and get the same answer — or see immediately why they cannot.

It differs from a document audit (which checks citations and arithmetic in a text) and from a work loop (which governs doing the work). A document can be perfectly honest about a claim that is void, and well-verified work is reported every day in a sentence that proves nothing.

## A claim is four fields

| field | question | void when |
|---|---|---|
| **probe** | which field or byte did I read? | the answer is a state, a name, or a file someone else wrote |
| **artifact** | what will the user actually see? | a status code or a queue acknowledgement stands in for it |
| **control** | what proves the probe can register a yes? | the control failed or is missing from the report |
| **reference** | what external number is this compared to? | the builder chose it |

All four answered, each with a command that re-derives it: `VERIFIED`. Any field missing: name the missing field and label down.

**Split compound sentences.** "The fix is verified, and the success rate is up 3×" is two claims in two rows; otherwise the cheap verified half lends credit to the expensive unverified one.

## Six ways a true-looking claim is void

1. **An inference is not a probe.** "The state is 3, therefore the menu is closed" — the field that answers it directly may exist in a response nobody opened. Name the field you read, or do not make the claim.
2. **A status code is not the payload.** An HTTP 202 and a small JSON ack prove the request was *queued*, not that the screenshot, file, or message the user will see exists. Verify the artifact.
3. **A null result is not a pass.** Every harness has an accepted/rejected split; if rejected equals attempted, the run measured nothing. A test that rejected all of its inputs on a stale token and reports "0 failures" is a green that never ran.
4. **A gate whose positive control failed decides nothing.** The control runs first. A failed control makes the row UNJUDGED — report it `INCONCLUSIVE` with the control named, not FAIL or PASS. A "4 of 8" measured while the control never passed is a measurement of the test setup.
5. **The reference must not be the builder's.** Name the external reference *and the pass threshold before the probe runs*; a threshold picked after the number is known is the same defect. A regression is caught only because a previous release was measured the same way — the project's own target might have passed it.
6. **Name the clock.** Say which clock produced a value and whether an independent one measured the same interval. Two numbers that "add up" are not agreement unless they measure the same statistic over the same population — summing two medians is not the median of the pooled data, and a synthetic request timed to a response is not a human action timed to a visible result. Re-derive any claimed agreement with a one-line calculation before quoting it.

## The labels

Use these strings verbatim so downstream tools can parse them. `UNKNOWN` is a legitimate fifth value.

| label | means | must carry |
|---|---|---|
| `VERIFIED` | a probe you did not write returned it, against a reference you did not choose | the command, its output, and the reference |
| `CODE-SHIPPED-NOT-VERIFIED` | the change is in the artifact; the path the user takes never saw it | the artifact identity (commit, build id) and which runtime check did not run |
| `BLOCKED` | the check is impossible for a named reason | the probe that refused, its exact error, the missing fact and its owner ("not run" is not blocked) |
| `INCONCLUSIVE` | the check ran and could not decide | the failed control's own line, from the same run |
| `UNKNOWN` | nothing was measured or it is not knowable now | the question and the command that would answer it |

A label without its command is a narrative.

## Decision tree

```
1 Can I name the field or byte I read?        no -> UNKNOWN, say what would answer it
2 Can I name the command that re-reads it?    no -> it is an inference: UNKNOWN
3 Does it depend on a control that must pass? failed/absent -> INCONCLUSIVE, name the control
4 Is the claim about change or improvement?   no previous measurement -> a report, not a verification
5 Is the check impossible for a named reason? yes -> BLOCKED, name the fact and its owner
6 Otherwise                                   -> VERIFIED + the command + the reference
```

## Two minutes on someone else's report

Look for:
- Verbs that hide inference: should, appears, seems, implies, therefore, consistent with, effectively.
- "Verified" with no command, or a command that reads a different field than the sentence names.
- A percentage with no `n`, or an `n` that is not the population in the claim (a rate over synthetic users is not a rate for real ones).
- A win with no previous-release number, or a baseline the author picked.
- "0 failures" with no accepted/rejected split.
- A pass whose control is missing entirely.
- A latency with no clock named.
- A status code, timestamp, or queue ack quoted as the artifact.
- An empty counter read as zero: `-1`, `null`, `[]` are not measurements.
- A done row whose evidence column reads "checked by author".

## Writing it down

One line per claim: **value → reference → command**. Keep the `UNKNOWN` rows; a table with none is hiding one. When someone else re-runs the command and gets the same answer, the claim has provenance; until then it has only a label.

## When to use

- Someone asks "can I claim it?", "is it verified?", or "does this prove it?"
- Before writing a status label into a handoff, README, close-out, or stakeholder message.
- A report says "it works" and you need to know what that rests on.

## How to use

1. Copy the `claim-provenance-fields` folder into `~/.claude/skills/` (personal) or `.claude/skills/` inside a project, then ask Claude Code to use the skill by name.
2. Example prompts:
   - "Use claim-provenance-fields on this test report and give each claim a label, the command that backs it, and the missing field if it is not VERIFIED."
   - "Apply claim-provenance-fields to my draft close-out and split any compound claims."
