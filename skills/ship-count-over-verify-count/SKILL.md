---
name: ship-count-over-verify-count
description: Keep a body of work pointed at what a real person can use rather than what has been verified — separate rehearsal from release, name the smallest shippable unit, and sort every blocker into one of five buckets.
---

# Ship count over verify count

Verification is a rehearsal. A user touching the thing is the performance. When both are happening this skill is unnecessary; when only the first is, it is the only thing that matters.

**The daily question, answered in one line before any work: what did a real person get today that they did not have yesterday?** An app on a device, a page live, a message answered. If the answer is nothing, say so first and treat the rest of the day as a recovery.

## The rehearsal test

- Count what shipped, not what was verified. Both numbers matter; only one is the product.
- A growing audit log, a climbing test count, an ever-sharper gate, and a rising handoff file with no shipped unit is a program rehearsing.
- A day is not a failure because nothing shipped — a hold or an approval can make shipping impossible. **It is a failure when the program does not notice.**
- Never present hardened work as progress toward delivery. "The fix is verified and cannot ship until X" is honest; "the fix is done" is not.

## The smallest shippable unit

- Name the smallest change in what a real person experiences *before* starting. One item published beats four stuck in a gate; one build on one real device beats a suite in a simulator.
- Prefer the unit that needs no permission. If every path to a user crosses a hold, the unit is unavailable — and the priority becomes making the clearance request unmissable, not finding a way around.
- Stage everything that does not need permission, so that when approval arrives the remaining work is minutes. List the remaining acts in order, each with its exact command or URL.
- Pre-staging is not permission. Never let a staged artifact look shipped or describe it as live.
- When the last step is one human act, make it singular and trivial: one file to open, one word to reply, one button to press. A list of five acts to publish one item is a failure of the ask; collapse it before sending.

## The five buckets

Classify every blocked item into exactly one, and act on the first three immediately:

1. **DECIDABLE** — a default exists. All four must hold: executable by an agent, reversible locally, downside bounded and known, and unruled (no standing decision, hold, or grant already covers it — an existing clearance *is* a ruling, so execute rather than re-ask). Take the default, record it with its rollback, proceed. Never return this as a question.
2. **OWNER'S HANDS** — only a human can do it (a login, a signature, a legal acknowledgement). Collect every such item into **one batched list**, each with its exact URL and expected duration. Batching governs the list; it does not merge separate decisions into one request.
3. **WAITING ON A BUILD** — blocked by work in flight. Not blocked; sequenced. Record the dependency and take the next item.
4. **EXTERNAL** — a quota, a reset date, a third party's outage. Name the service and the date, then route around it. Never wait.
5. **UNRECOVERABLE** — the inputs do not exist. Close it in writing with the reason; chasing costs more than the loss.

Bucket 2 is a legitimate answer, not a failure of nerve. The classification failure is writing "waiting on owner" without naming the bucket and why it is not DECIDABLE. "Owner's hands — only they can sign; everything upstream is staged" is finished thinking; "waiting on owner" alone is not.

## Holds, fences, and permission

- A hold wins over a deadline. A release date is not authority to cross a fence, and pressure to ship is exactly when a bypass starts looking reasonable.
- Under a hold, do the verifiable work, pre-stage the deliverable, and make the clearance request the **first line** of the owner-facing message — the item whose absence blocks everything else, with what it unblocks and how long it takes.
- Never quietly satisfy a gate by reinterpreting it. Deleting the affordance a test objects to, widening a threshold, or editing the test turns a real finding into a green.
- When a fix is verified but a fence blocks the ship, label it for what it is — verified locally, nothing reached a user.

## Reporting

- Lead with what a person can now do. Evidence second. Method third.
- Name the single next act that changes what a user experiences, and who must take it.
- When the answer is "nothing shipped", say it in the first line. A recovery report that opens with the audit is the failure it describes.

## When to use

- Work has run for days without reaching a user.
- A plan is all hardening and audits.
- A hold or an approval is the real blocker.
- Someone asks "what shipped?", "are we making progress?", or "why is nothing live?"

## How to use

1. Copy the `ship-count-over-verify-count` folder into `~/.claude/skills/` (personal) or `.claude/skills/` inside a project, then ask Claude Code to use the skill by name.
2. Example prompts:
   - "Use ship-count-over-verify-count on this project's last week of work: what actually reached a user, and what is the smallest shippable unit?"
   - "Sort these 12 blocked tasks into the five buckets from ship-count-over-verify-count and give me one batched list of what only I can do."
