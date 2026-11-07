---
name: approval-to-artifact-trace
description: Prove an approval actually became a shipped artifact by walking five legs from the approver's words to the live result, finding the dead leg, and verifying the last one from outside the system.
---

# Approval to artifact trace

An approval is not an artifact. Between someone saying "yes" and a post, release or deploy actually existing, there are several legs, and each can be perfectly green while the next is dead. A classic failure: items go live while the publisher's own ledger reads zero and its scheduled job logs "halted" on every slot, because a *different* job did the posting.

## The five legs

1. **Words**: the approver says it, in chat or on a card.
2. **Card**: a decision surface is posted and a response comes back.
3. **Decision**: a durable record naming who, when, and the exact bytes authorised (a content hash).
4. **Execution**: one of *possibly several* jobs acts on that record.
5. **Artifact**: bytes exist in the world: a post, a release, a deploy.

Always say which leg you are reporting. "Approved" is leg 3. "Posted" is leg 5. Most bad status lines are a leg-3 fact written in leg-5 grammar.

## Locate the dead leg, cheapest probe first

- **Leg 4, who executes?** Enumerate every scheduled job, queue worker or service that could act on the decision. Never assume there is one.
- **Legs 3 and 4, was the decision a human's, and did an executor act on it?** List the newest decision records with decider id, outcome, revision, bound hashes, and the timestamps of the card and of the decision.
- **Leg 5, count the artifact at the outermost leg**, not the ledger you already know. A true count of the wrong leg (a release ledger at 0) is still misleading.
- **Leg 4 detail:** read the executor's own log line, including why it waited.

If an "unreconciled" record appears beside a success receipt, check whether a posted receipt already carries the same container or media id before calling it a lost item. Then check when the next reconcile tick fires; many clear themselves.

## Prove the last leg from outside the system

The executor's receipt is a **report**; the artifact's own address is the **reference**. Fetch the permalink logged-out (an HTTP 200 with the expected content is the claim). Without it the honest label is CODE-SHIPPED-NOT-VERIFIED. If the surface needs authentication you cannot supply, the label is INCONCLUSIVE and you name the reference you could not reach.

## Read the decision record like an auditor

- A decision applied one second after the card was issued is not a human response. Find the pre-applied row or auto-approver before reporting "the owner approved it".
- A decision applied tens of minutes after the card is human-shaped.
- A decision bound to one content hash authorises exactly those bytes. A re-cut, re-encode or new cover needs a new decision; an authorisation is never transferable to a rebuilt file.
- Derive the approver's id from a card they answered rather than carrying it as a constant.

## Waiting is not blocked

A log line such as "waiting: quiet hours until 07:00; the one-time exception names another item" carries three facts: the grant is alive, the clock is the blocker (not the approver), and a one-time exception is scoped to the subject it named. Quote the reason and name the next fire time instead of escalating.

## A receipt can record that governance did not run

If a live item's receipt shows its gate as "not run", bytes went live whose gate state the receipt does not attest. Report it as a finding. Never back-fill a gate result: a result written after the post describes the post, it does not check it.

## Never

- Never count the one job you know about and call it the whole system; several executors may exist.
- Never read a locked or halted path as evidence that nothing shipped; the lock governs its own job.
- Never label an artifact VERIFIED from the executor's log line; fetch its address.
- Never infer "no approval" from an empty ledger in a different id space than the path you are asking about.
- Never hand-reconcile what the next tick reconciles.
- Never widen a grant, re-point a hash, or edit a halt to make the chain look finished. The chain is evidence; report the dead leg.

## When to use

- Approval was granted but nothing shipped.
- Someone asks "did it actually post / ship / deploy?"
- The count of live artifacts disagrees with a ledger, or an executor reports success and nobody can see the result.

## How to use

1. Copy this folder into `~/.claude/skills/` (personal) or `.claude/skills/` inside a project, then ask Claude Code to use `approval-to-artifact-trace` by name.
2. Give it the approval, the expected artifact, and where decision records and executor logs live.

Example prompts:
- "Use approval-to-artifact-trace: the release was approved yesterday but I can't see it live. Which leg is dead?"
- "Use approval-to-artifact-trace to verify from outside the system that the post our publisher logged as successful really exists."
