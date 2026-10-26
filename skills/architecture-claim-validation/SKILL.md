---
name: architecture-claim-validation
description: Validate architecture claims through separate model-integrity, code-anchor, and evidence checks, then challenge the checks with isolated negative controls.
---

# Architecture claim validation

An architecture model is a set of claims to test. A well-formed model, a resolving code reference, and a supported claim are three different results. Keep them separate so a clean structural check cannot stand in for evidence about behavior.

## When to use

- An architecture document may have drifted from the implementation.
- A claim cites code but its supporting behavior has not been examined.
- You need to assess whether a manual checklist or existing validator rejects unsupported claims.

## Define a small, checkable model

Split broad statements into claims that can be tested independently. Use a table or structured document with these fields:

| Field | Required content |
|---|---|
| Claim ID / statement | Unique stable ID and one bounded assertion |
| Status / scope | implemented or proposed; component, revision, and environment covered |
| Source IDs | References to evidence records supporting this claim |
| Evidence record | Unique source ID, source type, location, actual capture date, and what was observed |
| Code reference | Repository alias, revision when available, relative file path, and symbol |
| Deferral | Missing evidence, reason, responsible role, and target review date |

Use real calendar dates in a consistent format such as `YYYY-MM-DD`. A capture date records when the evidence was inspected, not when the claim was written. Mark unavailable revisions explicitly; do not invent one. Documentation can support a proposed design without proving implementation. A claim with no supporting evidence needs a complete deferral; a partially supported claim must state which part remains deferred.

Maintain a separate repository mapping: `alias | approved checkout location | repository identity evidence | observed revision`. Use relative paths or `~/` placeholders in shared copies. Verify that each checkout belongs to the intended repository from available repository metadata before resolving anchors. A familiar directory name is insufficient.

## Check three layers independently

1. **Model integrity.** Check unique claim and source IDs, allowed status values, nonempty statements, valid cross-references, and real capture dates. Every claim needs evidence or a complete deferral. Every code source needs its repository alias, relative path, and symbol. A missing capture date or code reference makes that evidence unsupported. A complete deferral can satisfy the bookkeeping check but never verifies the claim.
2. **Anchor resolution.** Under a verified repository mapping, inspect the referenced revision when available, then locate the file and symbol. Record the inspected revision. A missing or unverified mapping yields unknown, not a clean pass or a broken-code finding. A file or symbol absent at the identified revision is a broken anchor and cannot support the claim. If the requested revision is unavailable, report unknown rather than silently checking a different revision.
3. **Claim support.** Read the referenced implementation, relevant callers, configuration, and tests. Compare their behavior with the exact statement, including exceptions and boundary conditions. A resolving anchor proves location only. Record whether tests were merely read or actually run; cite existing results with their revision and scope. If the evidence contradicts the statement, report the contradiction. If it covers only part of the claim, narrow the supported scope or leave the remainder unresolved.

Keep source and runtime evidence in separate columns. Source inspection supports claims about the inspected revision. Runtime observations support only the behavior and environment observed. A healthy endpoint does not reveal the deployed revision; without independent deployment identity evidence, the link to a source revision remains unknown.

## Challenge the checking method

Keep the original model and repository mapping untouched. Make a separate disposable copy for each control below, changing one condition in each copy. Use a known, structurally valid starting model and record its initial per-claim results. Apply the same manual checklist or existing validators to each copy; no particular validator is required or bundled.

| Single change on a disposable copy | Expected outcome |
|---|---|
| Remove the only evidence-or-deferral entry from a claim that has no support | Model integrity rejects that claim as lacking evidence or deferral |
| Replace a source capture date with invalid text | Model integrity rejects the date; affected evidence cannot support a claim |
| Remove the code reference from a code evidence record | Model integrity rejects the missing reference; anchor resolution cannot pass |
| Make a previously verified repository mapping unavailable in the copied mapping | Anchor resolution reports unknown; the claim cannot receive a verified code-support result |

For the first control, start with an unsupported claim that has only a deferral and remove that deferral. This changes one condition without accidentally removing evidence from several claims.

Record the changed field, expected result, observed result, and which checking layer caught it. A narrow validator may cover only one layer, but the combined procedure must produce every expected refusal or unknown result. Do not call it adequate if a required rejection passes, an unavailable mapping becomes success, or a deferral becomes verification. Report the gap before trusting a clean result.

## Report claim by claim

Use `claim ID | model integrity | anchor resolution | source support | runtime support | evidence/scope | unresolved work`. Explicit outcomes such as pass, fail, supported, contradicted, deferred, unknown, and not examined are preferable to a single overall green status.

List unresolved work with the responsible role and target review date. Only describe a claim as verified when the relevant integrity, anchor, and substantive evidence checks support it within the stated scope. Proposed or deferred work remains labeled as such. Report limitations even when every resolvable anchor exists.

## How to use

1. Copy this folder into `~/.claude/skills/` for personal use, or into `.claude/skills/` inside a project.
2. Ask Claude Code to use the `architecture-claim-validation` skill by name.

Example prompts:

- "Use architecture-claim-validation on this architecture model and the approved repository mappings. Report integrity, anchor resolution, and actual support separately for each claim."
- "Use architecture-claim-validation to challenge our existing checks with disposable negative controls. Preserve the original model and report any unsupported case the checks accept."
