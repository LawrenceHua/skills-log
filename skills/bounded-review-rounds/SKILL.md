---
name: bounded-review-rounds
description: Run multi-reviewer code review with approvals bound to one content hash, a three-round limit and a real, false or out-of-scope triage of every objection, so review loops end in an approval or a smaller redesign.
---

# Bounded review rounds

Model reviewers can always find one more objection. Without a stopping rule a change goes through many rounds, each approval applies to a version that no longer exists, and nothing lands. This is a contract for running the rounds and ending them.

## 1. Fix what is being reviewed

Stage the change and record one hash for it, such as the commit id or a SHA-256 over a manifest of file hashes. One hash gets one review. Any edit produces a new hash and cancels earlier approvals.

Choose reviewers before round 1: two, from model families that differ from each other and from the author. Name one stand-in for a reviewer that returns no verdict.

## 2. Write the review prompt

In this order:

1. A time box, and a request to put the verdict first.
2. The stance: an independent reviewer who refutes when a defect is plausible and unaddressed.
3. The threat model (round 1), such as "a confused or prompt-injected agent using the normal tools".
4. Context: what changed and why, with file and line references, kept short.
5. Results: exact test commands and their counts.
6. Three to five questions that would expose a defect.
7. The answer format: first line `VERDICT: APPROVE` or `VERDICT: REFUTE`, then `DEFECTS:`.
8. The full diff.

If reviewers may not clone or run anything, say so and include everything they need. Build each round's prompt fresh. Never include secrets or private data.

If the author's sandbox cannot call reviewers, hand off through files: write the prompt, then create an empty `READY-<n>` marker. A separate runner writes each reviewer's output and exit status and then `DONE-<n>`. Confirm the runner is alive before waiting, and cap the wait.

## 3. Read each verdict from its output

- Take the first `VERDICT` in the reviewer's output file. Some tools prefix it with a bullet.
- A wrapper's non-zero exit status does not cancel a well-formed verdict, and a zero status does not create one. Read both.
- Empty output, or draft text in an error stream, is **no verdict**. It can serve as notes.
- A slow answer inside the time box is not a reason to resend.

## 4. Triage every objection

Write one line per defect in a triage file for the round:

| Class | Meaning | Required evidence |
|---|---|---|
| `REAL` | the defect exists | a failing test or command that reproduces it |
| `FALSE` | the claim is wrong | the line or output that shows why |
| `SCOPE` | true or plausible, but outside this change | copied to a follow-up list; does not cause a round |

From round 2 on, a refutation blocks only if it names an input and the wrong output **and** you can reproduce it on the staged code.

## 5. Stop

- **Approved:** both required reviewers approve the **same hash**. Write a marker such as `APPROVED-<hash>` and stop. Do not send an unchanged hash again.
- **Round limit:** three rounds per brief. A round with a missing verdict is retried and does not count; if the retry and the stand-in also return nothing, report the review as blocked.
- **Defect still open after round 3:** make the change smaller and start a new brief. Do not open round 4 on the same design. Report `BLOCKED` with one paragraph describing the smaller change.
- Approvals followed by a later refutation are normal when the hash moved in between. Only the approval marker for the current hash counts.

Watch for a reviewer that approves every round while others find reproducible defects. Its approvals add little; replace it or weigh it accordingly.

## 6. After approval

Where the change reads real data, replay it on recorded inputs. After applying it, probe the live behaviour once and write down the rollback.

## Never

- Claim an approval that is not recorded against the exact hash.
- Count a single reviewer as two, or an empty answer as agreement.
- Extend the round limit to argue about a functional defect.

## When to use

- A change has been through several review rounds and is still not landing.
- Setting up automated cross-model review for agent-written code.
- Deciding whether an earlier approval still applies after an edit.

## How to use

1. Copy the `bounded-review-rounds` folder into `~/.claude/skills/` for personal use, or `.claude/skills/` inside a project.
2. Ask Claude Code to use the skill by name.
3. Example prompts:
   - "Use the bounded-review-rounds skill on this branch. Hash it, prepare the round 1 prompt for two reviewers, and tell me what counts as approval."
   - "We are on round 6 with one reviewer still objecting. Use bounded-review-rounds to triage the open items and decide whether to shrink the change."
