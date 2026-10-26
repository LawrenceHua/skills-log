---
name: cross-interface-capability-audit
description: Compare agent interfaces through a dated capability matrix that distinguishes configuration, observed availability, unknown inputs, and confirmed changes.
---

# Cross-interface capability audit

Measure which capabilities each agent interface exposes before recommending changes. An interface is a specific application, session profile, or project configuration; two profiles of the same application may expose different tools. Equal capability counts do not imply equal capabilities.

## When to use

- A task works through one interface but appears unavailable through another.
- You need a capability inventory or a comparison with an earlier snapshot.
- You want to rank useful configuration changes without treating every difference as a defect.

## Build the inventory

1. **Fix the scope.** List interfaces, profiles, and capability types, such as skills, tool servers, individual tools, and scheduled actions. List the allowed configuration files, resolved skill folders, and read-only inventory APIs. Record exclusions. Do not collect credentials, environment values, conversation contents, or unrelated files.
2. **Inspect each source.** Read the actual schema and inventory boundaries. Resolve pagination and included configuration files within the allowed scope. Record permission errors, parse failures, truncation, and partial coverage rather than converting them into empty lists.
3. **Normalize identity.** Give each capability a canonical identity independent of its display name. Use a stable source identity or resolved content when available to recognize aliases. Preserve alias-to-identity mappings and versions; identical names alone do not justify merging, and different versions remain distinct observations. Keep uncertain matches separate.
4. **Separate declaration from observation.** A configuration entry establishes configured presence. A readable resolved folder or an advertised tool list establishes only that observation. Neither proves the tool can execute. Record execution evidence separately only if an authorized check already exists; do not invoke consequential operations to fill the table.

Use one row per capability and interface, plus a source-coverage table. Replace the placeholders with sanitized values; a source reference should locate the evidence without exposing secret-bearing configuration.

| Field | Record |
|---|---|
| Capability identity / type | Stable identity and category |
| Interface / profile | The specific surface examined |
| Aliases / identity basis | Names seen and why they were grouped |
| Declared / configured presence | present, absent, or unknown, separately |
| Observation | resolved, advertised, executed, absent, or not examined |
| Evidence | Sanitized source reference, capture date, version if available |
| Limits | Coverage gaps, uncertainty, and any execution restrictions |

| Source state | Meaning |
|---|---|
| observed | Readable inventory with records; mark coverage complete or partial |
| valid empty | Successfully read complete inventory with zero records |
| unreadable | Missing, inaccessible, malformed, or failed retrieval; include reason |
| not examined | No inspection performed; include reason |

An absent cell is justified only by a complete, readable inventory covering that capability type and interface. A readable file that cannot be parsed is unreadable for this purpose. A valid empty inventory is evidence of absence within its stated scope; an unreadable source is not.

## Compare snapshots deterministically

1. Preserve each dated snapshot and its scope, source coverage, identity rules, and schema interpretation.
2. With no earlier snapshot, report **no baseline**. Do not report zero drift.
3. Check that interface profiles, capability categories, scope, and normalization rules match. If they differ, compare only the common scope or mark the comparison incomparable.
4. Match rows by canonical identity, capability type, and interface/profile. Compare declared, configured, and observed fields separately. Report an addition only when the earlier complete inventory establishes absence; report a removal only when the current complete inventory establishes absence. Otherwise label it newly observed or unknown, not added or removed.
5. Separate alias or version changes from additions and removals. Evidence-date refreshes alone are not capability changes. Unknown inputs cannot establish removals or an unchanged inventory.
6. Cross-check consequential differences against an independent source, such as a resolved folder versus a configuration index, or an interface's advertised list versus a parser result. Confirm field names and schema on a known record. If corroboration is unavailable, retain the difference as unconfirmed.

## Turn evidence into useful work

Rank gaps by concrete tasks affected, importance of those tasks, available alternatives, and confidence in the evidence. An intentionally restricted interface may be correct. Give each recommendation the affected task, observed difference, independent check, uncertainty, and smallest proposed change.

Automation may append recommendations to a review queue. It must not turn its own findings into authoritative knowledge or change configuration as part of the audit. A separate review decision records what was accepted and why.

Return the matrix, coverage table, confirmed changes, unknown comparisons, and ranked review queue. Keep availability and execution claims separate throughout.

## How to use

1. Copy this folder into `~/.claude/skills/` for personal use, or into `.claude/skills/` inside a project.
2. Ask Claude Code to use the `cross-interface-capability-audit` skill by name.

Example prompts:

- "Use cross-interface-capability-audit to compare the approved configuration files and advertised tool lists for these two agent profiles. Rank gaps by the tasks they affect."
- "Use cross-interface-capability-audit to compare these dated inventory snapshots. Separate confirmed removals from unknown coverage and alias changes."
