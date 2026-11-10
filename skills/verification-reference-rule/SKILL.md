---
name: verification-reference-rule
description: Before labelling any check, name the reference the claim was compared against and prove that reference is current and non-empty; a checklist of probe-hygiene tests covering counts, regex misses, denominators, clocks and fixtures.
---

# Verification reference rule

A label such as VERIFIED is only as good as the reference behind it. Before you write one, name what the
claim was compared against, then test the reference itself. Each rule below is a test a second reviewer can
apply.

## The rules

1. **If you chose the reference, the claim is a report, not a verification.** A builder comparing an
   artifact to its own description proves consistency, not correctness. Use a live third party, a
   measurement you did not produce, an artifact from before you touched it, or a reviewer whose default is
   REFUTED.
2. **Prove the reference before anything else.** A probe reading a stale baseline, a truncated log, an
   empty file or a path that no longer exists returns a confident answer about nothing. Assert the
   reference is non-empty, current, and the thing you named.
3. **A summary is a pointer, not a reference.** A dashboard, a prior report, a status string or a file the
   claimant wrote tells you where to look. Read the artifact.
4. **A count is not a set; a match is a location, not a behaviour.** Read the line you matched.
5. **A pattern miss is not an absence.** A regex encodes a format the artifact may not share: longer line,
   wider indent, split across lines, different order. Print the surrounding region before reporting
   something missing.
6. **A number whose denominator is not the thing it names is not a measurement.** A percentage over the
   wrong population is arithmetic wearing a unit.
7. **A truncated string is not the whole string.** If you cut a quote, you may not paraphrase the cut.
8. **Never write the conclusion before the evidence line.** A claim and its evidence in one command must
   agree, or you asserted the result rather than finding it.
9. **A status code, timestamp or `done` is history.** Measure the artifact now. Done means delivered, never
   accepted.
10. **An empty result must say why it is empty.** `no_data`, `unreadable`, `filtered` and `unreachable`
    are different facts. `unknown` is a real state; `None` is not `False`.
11. **Generate timestamps; never type them.** Take the clock from the system (`date -u`) or the file's own
    recorded time, and state the zone. A local time carrying a `Z` is wrong by its offset.
12. **A total over nested reports double-counts.** If a log has per-suite and aggregate totals, take the
    aggregate once or sum leaves only. If you cannot state the denominator, you have no aggregate.
13. **An assertion's failure message is a hypothesis.** When a failing test suggests it might be expected
    or stale, check that against the docs, code path or live runtime before letting it downgrade a real
    defect.
14. **A brief that predicts which failures a change will clear must name, for each, the condition the
    change alters.** A failure with no such condition is pre-existing and out of scope. Predicting it will
    clear is how a brief manufactures a miss.
15. **A fixture that omits the field the branch reads exercises the wrong code.** Example: 9 of 13
    classifier self-test cases returned "no log" before reaching the age check because every synthetic
    record lacked the log-path field. The classifier was right and the suite was empty. Give the fixture
    the field, then watch the class change.
16. **A probe that fails for an environmental reason manufactures a class.** A hardcoded user id made every
    scheduler query return nothing, and 66 healthy jobs were reported as "no counter". Assert the probe
    itself succeeded before aggregating; treat one uniform answer across dozens of items as a broken
    probe, not a finding.

## Recurring failure classes

A class listed here is not thereby covered; it is listed because it recurs, and it is caught only if a rule
above names its test: hand-written timestamp where the clock was available; local time labelled UTC; a
constant's name read instead of its value; a class name assumed to equal its filename; a bare-substring
count where an anchored pattern was meant; a total summed across nested reports; a quoted assertion
misquoted at the cut; a conclusion echoed before the grep that should prove it; a producer's exit code or
attempt counter believed over its own state file.

## Procedure

1. Write the claim in one sentence.
2. Name the reference and who produced it. If it was you, find another.
3. Run the cheapest probe that proves the reference is current and non-empty.
4. Run the claim's probe. Print the evidence line before the conclusion.
5. Run one deliberately wrong input and confirm the probe fails.
6. Label: VERIFIED with the command, CODE-SHIPPED-NOT-VERIFIED, BLOCKED with the blocker, or INCONCLUSIVE
   with what was checked and why it was not decisive. Do not flatten mixed results into one green status.

## When to use

- Before writing a completion report, a status line or a "no issues found".
- Reviewing someone else's "it works" or a monitor that reports green.
- Writing a self-test for a classifier, gate or probe.

## How to use

1. Copy this folder into `~/.claude/skills/` (personal use) or `.claude/skills/` inside a project.
2. Ask Claude Code to use the `verification-reference-rule` skill by name.

Example prompts:

- "Use verification-reference-rule on this test report before I tell the team it passed."
- "Use verification-reference-rule to review my log-classifier self-test and find fixtures that skip the
  branch under test."
