---
name: claim-receipt-reconciliation
description: Capture immutable check receipts and reconcile a completion draft against current-session evidence, correcting unsupported claims and recording each decision.
---

# Claim Receipt Reconciliation

Turn a completion report into a traceable set of assertions. Each check gets an immutable receipt; each draft gets a separate reconciliation record. This is a manual procedure unless the user already has working automation for it. Installing this skill creates no automatic gate.

## When to use

Use before sending a completion report that claims something was changed, tested, delivered, or made operational, especially when several checks support different parts of the report. It also fits a handoff where the next reader needs to distinguish observed results from unfinished verification.

## How to use

Copy this whole skill folder into `~/.claude/skills/` for personal use, or into `.claude/skills/` inside a project. Ask Claude Code to use `claim-receipt-reconciliation` with the draft, current session identifier, and approved evidence location.

### 1. Define what would prove the claim

For each intended assertion, identify the target, revision or version, environment, scope, and observable success condition. Split compound assertions when one check cannot establish all their parts. A local file edit, a passing check, and a published result need different evidence.

Choose an authorized probe that actually observes the condition. Record what it cannot establish. Do not repeat a state-changing action merely to obtain a receipt; use an authorized read-only check when available. If the necessary check exceeds authorization, leave the claim unresolved and identify that missing check.

### 2. Capture an immutable receipt

Run the approved check and capture its method, verifier identity or role, start and finish times, execution outcome, and observed semantic result. An exit code of zero describes process execution; it does not prove that the requested behavior occurred.

Keep a bounded, privacy-safe excerpt that preserves the decisive observation and relevant failures. Mark truncation and redaction explicitly. If omitted material is needed to assess the claim, the excerpt is insufficient: retain an approved supporting artifact or leave the result inconclusive. Never invent output or silently turn an interpretation into a direct observation.

Use a new unique receipt identifier and exclusive file creation in the approved evidence directory. Never overwrite an earlier receipt. Every rerun produces another receipt, including failures and timeouts. Reopen and validate the saved file before appending its identifier, session, target, revision, time, and relative path to an append-only lookup index.

The index is a locator, not proof. A failed receipt write supplies no qualifying saved evidence. If indexing fails, report the recording failure and repair it before treating the recording workflow as complete; do not pretend an index row was saved.

A compact receipt shape is:

```json
{
  "id": "<unique-receipt>",
  "session": "<current-session>",
  "claim": "<specific-assertion>",
  "target": "<target>",
  "revision": "<version>",
  "scope": "<environment-and-boundary>",
  "expected": "<observable-condition>",
  "probe": {
    "method": "<authorized-check>",
    "verifier": "<role>",
    "started": "<timestamp>",
    "finished": "<timestamp>",
    "execution": "<outcome>",
    "exit_code": null
  },
  "observation": "<sanitized-decisive-evidence>",
  "truncated": false,
  "redacted": false,
  "semantic_result": "supported|contradicted|inconclusive",
  "limitations": []
}
```

Use a numeric exit code only when the check produces one. Save, for example, under `evidence/<session>/receipts/<unique-receipt>.json`; keep the index alongside the receipts.

### 3. Reconcile the actual draft

Extract completion assertions from sentences and clauses, including implicit claims such as “ready for use.” Assign stable claim identifiers and retain their original wording.

Find candidate receipts within the current session. Match the precise target, revision, scope, and success condition unambiguously; similar wording alone is insufficient. Reopen each receipt and its necessary supporting evidence instead of trusting an index label.

Check timing and later evidence. A revision change can invalidate an earlier pass. A later failure for the same condition must remain visible; an earlier success cannot conceal it. If observations conflict and the current state is unresolved, describe that conflict. Missing, ambiguous, stale, or insufficient evidence never verifies the claim.

### 4. Correct and return the report

Keep supported assertions and attach inline relative evidence links. Revise unsupported assertions to the narrowest accurate statement, preserving their subject and intended meaning. Distinguish a failed check from an unperformed check. A missing receipt does not establish that code was shipped, changed, or even attempted.

Return the corrected draft and a table containing claim, evidence, decision, limitation, and next check. Save a separate structured sidecar for this exact draft revision:

```json
{
  "draft": "<draft-revision>",
  "session": "<current-session>",
  "matches": [{"claim_id": "<id>", "receipt_ids": ["<id>"]}],
  "downgrades": [{"claim_id": "<id>", "reason": "<reason>", "replacement": "<text>"}],
  "missing_checks": [{"claim_id": "<id>", "check": "<needed-observation>"}]
}
```

Read back the sidecar. Report any save failure and keep unsupported wording corrected even when recording is blocked. Reconcile again after material draft or evidence changes.

## Example prompts

- “Use claim-receipt-reconciliation to check this release summary against the receipts from this session.”
- “Record the authorized checks, then correct my completion draft and list the evidence still missing.”
