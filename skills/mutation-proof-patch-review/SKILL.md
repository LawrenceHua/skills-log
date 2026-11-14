---
name: mutation-proof-patch-review
description: Judge a code change by proving each behavior change is covered by a test that fails when that change is reverted, using scratch copies and a raw failing-test delta instead of a green suite.
---

# Mutation-proof patch review

A green test suite says the candidate passes its own tests. It does not say the tests would notice if the new behavior were missing. This skill makes the reviewer demonstrate that, one behavior hunk at a time, before a change is called ready.

## The rule

A change is **not ready** while any behavior hunk has no test that fails when that hunk is reverted. Hunks that only rename, reformat or move code are exempt, but the reviewer must say so for each one.

## Method

1. **Start from refuted.** Review in a fresh context, on a fresh clone of the candidate, with the default stance that the claim of readiness is false. Do not read the author's reasoning, only the diff, the test list and the gate output.
2. **List the behavior hunks.** Split the diff into hunks. Label each one `behavior`, `refactor` or `docs`. Write the list down before running anything; a hunk you did not list cannot be silently skipped later.
3. **Bind the suite to the source.** Record a hash of the candidate source tree and the full list of collected test ids (a count alone is not enough: a collection error can shrink the list without failing). The proof below is only valid for that hash.
4. **Make one mutant per behavior hunk.** In a scratch archive of the candidate, revert exactly one hunk (or flip one condition, or delete one call). One change per mutant, so a failure is attributable.
5. **Run the suite against the mutant.** Capture the raw failing test ids, not a pass/fail summary.
   - At least one test that is relevant to that hunk must fail. Then the hunk is covered.
   - Nothing fails: the hunk is uncovered. Record it as a finding and request a test.
   - Something unrelated fails: the mutant is broken or the failure is environmental. Rebuild the mutant; do not count it.
6. **Compare against a second environment when you have one.** Run the unmodified candidate on another machine or container and diff the raw failing test ids. A failure that exists only on one side is the finding, not the totals.
7. **Write the verdict.** `READY-FOR-REVIEW` only if every behavior hunk is covered and the baseline suite is green on the recorded hash. Otherwise `NOT-READY` with the list of uncovered hunks.

## Isolation rules

- Run mutants and scratch suites in disposable copies of the candidate, never inside the candidate itself and never against a real home directory. Give the run a private temp directory and a throwaway home.
- A mutant run must not post, send or deploy anything. Count external side effects (for example queued notifications) before and after, and stop if the number moved.
- Delete scratch copies afterwards by listing exactly what you created; never glob-delete.

## Report format

```
candidate-hash: <hash>
tests-collected: <n>  (ids saved to <file>)
hunk 1  behavior  mutant fails: test_a, test_b   -> covered
hunk 2  behavior  mutant fails: (none)           -> UNCOVERED
hunk 3  refactor  exempt: pure rename
baseline: <n> passed, <m> failed (ids listed)
verdict: NOT-READY (hunk 2)
```

## Pitfalls

- A mutant that fails to compile "fails" every test. Confirm the mutant imports and runs before counting failures.
- A test that fails for a hunk it does not exercise is not coverage. Read the failing assertion.
- Reverting more than one hunk at once hides which test covers which.
- Total counts (`120 passed`) hide a swapped set of failures. Always compare ids.

## When to use

- Reviewing an agent-written or agent-assisted patch before merge.
- A reviewer says "tests pass" and you need to know whether the tests protect the new behavior.
- Any round where a worker reported success and a separate judge decides readiness.

## How to use

1. Copy this folder into `~/.claude/skills/` (personal) or `.claude/skills/` inside a project, then restart or refresh your session.
2. Ask Claude Code to use the `mutation-proof-patch-review` skill by name.

Example prompts:

- "Use the mutation-proof-patch-review skill on the diff between main and this branch. List the behavior hunks first, then show which test fails for each reverted hunk."
- "The worker says all tests pass. Apply mutation-proof-patch-review and give me the verdict with uncovered hunks."
