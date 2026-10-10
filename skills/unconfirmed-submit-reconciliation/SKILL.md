---
name: unconfirmed-submit-reconciliation
description: "Resolve uncertain browser submissions through authenticated history and payload matching while keeping repeat writes stopped."
---

# Unconfirmed submit reconciliation

## When to use

Use this skill after a browser or application submission was attempted but its outcome is uncertain: a timeout, lost response, stalled screen, or missing confirmation. It applies when the intended application's account history can be inspected through existing authenticated access.

The purpose is to establish what happened to that attempt. This method never retries, edits, deletes, schedules, or sends a new message.

## Working method

### 1. Freeze repeat writes

Immediately stop all retries for the uncertain attempt, including any queued automatic retry you can pause through an already authorized local control. Do not interact with the submit control again or reload a page in a way that could resubmit a form.

Record that reconciliation is pending. A timeout, empty history view, or missing success notification does not prove failure. If another process may repeat the write and you cannot safely pause it, report that limitation immediately; do not claim repeat writes are contained.

### 2. Preserve a minimal private attempt record

Keep a durable record in an authorized private location with:

- An account alias and the intended destination.
- The attempted payload, or a protected reference to the exact local content.
- The actual submitted form, if it was captured.
- An approximate time window and its time basis.
- Evidence that submission was attempted and the outcome observed.
- Missing or uncertain fields explicitly marked unknown.
- The current reconciliation status and a clear instruction not to retry.

Never log credentials, cookies, session tokens, or unrelated account data. Retain only enough content to distinguish this attempt. Do not upload the record publicly.

Separate a draft from the actual form sent. If the two cannot be shown to agree, do not silently treat the draft as proof of the transmitted payload.

### 3. Validate the history surface

Use the intended application's authoritative account history through existing authenticated access. Check the active account and destination before interpreting records.

If the wrong account is active, the destination cannot be verified, access is missing, or inspection would require an account switch or login change, stop with an unresolved status. Do not change authentication, accounts, or permissions under this skill.

A notification, cached screen, or draft view may be supporting evidence, but it does not substitute for an authoritative history record. Prefer a record detail view that exposes a stable identifier and its observed current state.

### 4. Search within a bounded scope

Set a relevant time window, maximum history pages or records, and a stopping point before searching. Use the application's existing read-only search and pagination. Respect permission limits and cooldowns.

Record the filters, pages inspected, visible time coverage, and any incomplete or unavailable ranges. Expand the search only within the authorized limit. If an additional read is appropriate after delayed visibility, make it bounded and respect the application's cooldown; never turn the delay into a reason to resubmit.

An empty result means no match was observed in that inspected scope. It does not establish that the original write failed or that no record exists elsewhere.

### 5. Match the attempted write

Compare each candidate with all available attempt evidence: account, destination, time, and actual payload. Require evidence for the submitted fields needed to distinguish it from similar writes.

Allow only known transport transformations, such as documented markup handling. Preserve the original form alongside the transformed comparison form and record the transformation's basis. Do not invent normalization rules after seeing a near match.

Fuzzy similarity, a matching title, or lossy comparison is insufficient. Exclude records known to predate the attempt. Similar earlier records are not evidence that this attempt succeeded. If missing timing or click evidence prevents distinguishing prior attempts, leave attribution unresolved. Missing payload evidence or multiple plausible records also prevents confirmation.

Confirm only when exactly one record is unambiguously tied to the attempt, has a stable identifier, and has an observed live state. If the bounded view leaves unresolved plausible duplicates, retain an unresolved result.

### 6. Record the outcome and stop

Use these outcomes consistently:

| Outcome | Required interpretation |
|---|---|
| Confirmed record | One unambiguous authoritative record matches the attempt; retain its private locator and observed state |
| Unresolved: no match observed | The inspected scope has no sufficient match; the attempt may still have succeeded |
| Unresolved: ambiguous matches | Multiple or similar records cannot be distinguished reliably |
| Unresolved: incomplete evidence | Payload, timing, account, destination, or history coverage is insufficient |
| Unresolved: access blocked | Existing authenticated access cannot establish the intended account or history |

For a confirmed record, distinguish existence from visibility, moderation, delivery, and deletion state. A matching record marked pending or removed does not establish that the intended audience can see it. A historical identifier without an observable current state is insufficient for confirmation.

Append observations to the original private attempt record rather than overwriting the attempted state. Include the checked scope, matching rationale, unresolved fields, and bounded stop reason. This record must allow a later session to see that a write was attempted and avoid blindly repeating it.

End reconciliation at confirmation or the bounded stop. Any later write requires a separate decision based on new evidence and applicable authorization.

## How to use

Copy the `unconfirmed-submit-reconciliation` folder into `~/.claude/skills/` for personal use, or into `.claude/skills/` inside a project. Then ask Claude Code to use the skill by name.

Example prompts:

- "Use unconfirmed-submit-reconciliation to inspect the existing account history after this form timed out. Keep retries stopped and report the exact search scope."
- "Use unconfirmed-submit-reconciliation to compare this uncertain submission with similar earlier records. Leave the result unresolved unless one authoritative record uniquely matches."
