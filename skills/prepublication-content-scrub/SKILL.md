---
name: prepublication-content-scrub
description: Review exact outgoing artifacts for protected terms, sensitive patterns, and private context, then verify the rewritten final copy.
---

# Prepublication content scrub

Review the material that will actually leave the workspace. Combine local literal and pattern checks with a separate manual review of meaning, rewrite only the outgoing copy, and record what the final review covered.

## When to use

- Preparing public documentation, examples, release notes, or attachments from private working material.
- Checking a draft that may contain identifying details in prose, links, filenames, images, or metadata.
- Rechecking a previously reviewed artifact after its contents or intended audience change.

## Working method

1. **Define the outgoing boundary.** Identify the exact files or message body, intended audience, and destination. Include accompanying filenames, titles, link targets, attachments, captions, comments, and document metadata. Keep a manifest of the reviewed artifacts using safe relative paths or neutral labels. Distinguish private source material from the outgoing copy. If the outgoing set cannot be enumerated, mark the review INCOMPLETE.

2. **Derive the private rules.** Use the user's explicit constraints to identify protected names, aliases, internal terminology, identifying relationships, and prohibited detail categories. Keep literal terms in private working context; never copy the dictionary into a public report, example, committed rules file, or outgoing artifact. Do not open credential stores to assemble it. Add supplied spelling or capitalization variants where relevant. Record the categories covered without reproducing the protected values. If a necessary restriction is unclear, identify the missing category and resolve it before declaring the review complete.

3. **Run available local checks.** Search every readable outgoing text surface for the protected literals, using case-insensitive matching where appropriate. Use available local pattern checks for credential-shaped content, contact details, private addresses, internal links, project identifiers, and absolute personal paths. Record which checks actually ran and their scope. Configure results to return counts and safe locations instead of matching text. Keep private terms out of command history and shared logs; use a private local checking interface that does not echo inputs. If suitable tooling is unavailable, record the missing coverage rather than claiming a scan ran. This skill provides a review procedure, not a bundled scanner or comprehensive pattern library.

4. **Review coverage gaps manually.** Read the outgoing material in context. Look for identities exposed through combinations of ordinary facts, recognizable private workflows, unique incidents, quoted conversations, and examples copied too closely from a source. Inspect rendered images, screenshots, hidden comments, embedded links, and metadata when they are included. Text extraction alone does not establish coverage of these surfaces. Label this work as manual semantic review; it is neither automated detection nor exhaustive protection. Record inaccessible or unsupported surfaces as coverage gaps.

5. **Triage without repeating the leak.** Inspect suspected matches privately to distinguish real disclosures from harmless text. Report only a safe artifact label, section or line location, category, and required correction. Use a neutral label if a filename is itself sensitive. Do not include raw matches, snippets, encoded versions, or sensitive before-and-after diffs in the review record. Unresolved findings remain BLOCKED; an unexplained match must not silently become a false positive.

6. **Rewrite the outgoing copy.** Replace identifying details with generic roles, relative paths, or descriptive placeholders. Preserve useful steps, prerequisites, and decision rules. Rewrite whole examples when substituting individual names would leave recognizable context. Remove material whose useful method cannot be separated confidently from private details. Leave the original private source untouched. Inspect the replacement text for both usability and accidental disclosure.

7. **Recheck the final bytes.** Rerun the applicable literal and pattern checks on the complete final artifact set, then manually review rewritten passages and affected context. Confirm that packaging or rendering did not reintroduce hidden content. Bind the result to the reviewed revision or a locally computed digest when available; any later edit invalidates that result. If building or modifying a detector, also test harmless synthetic positive and negative fixtures for its intended behavior. Use unmistakable test markers, never realistic credentials. Routine content review does not require building a detector.

8. **Record a scoped result.** Use BLOCKED when a detected disclosure remains, INCOMPLETE when required coverage is missing, and CLEAN only when the declared checks and manual review are complete with no unresolved findings. If both a disclosure and a coverage gap exist, report BLOCKED and list the gap. CLEAN means only that the stated review found no remaining issue within its scope. It does not authorize publication or prove anything was sent. Preserve existing publication authorization without inventing an additional approval requirement.

## Review record

Keep the record safe for its audience and compact:

- Artifact labels and reviewed revision or digest, if available.
- Intended audience and protected categories covered.
- Literal and pattern checks actually run, plus their results.
- Manual surfaces reviewed and remaining limitations.
- Safe finding locations, corrections, and final recheck results.
- Status: CLEAN, BLOCKED, or INCOMPLETE, with a scoped reason.

## How to use

Copy the entire skill folder into `~/.claude/skills/` for personal use, or `.claude/skills/` inside a project. Then ask Claude Code to use the skill by name.

Example prompts:

- "Use prepublication-content-scrub on this public guide and its attachments. Apply my supplied privacy constraints, rewrite the outgoing copy, and report final coverage without quoting matches."
- "Use prepublication-content-scrub to recheck the revised release notes. Keep the private source unchanged and distinguish automated checks from manual review."
