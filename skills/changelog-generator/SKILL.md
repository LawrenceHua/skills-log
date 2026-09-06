---
name: changelog-generator
description: Generate consistent, auditable release notes directly from Conventional Commits — auto-detects the correct MAJOR/MINOR/PATCH semver bump, renders a Keep a Changelog-style document, and pairs with a CI commit-format linter and a mandatory human-approval gate before anything gets written.
---

# changelog-generator

A changelog written by hand after the fact drifts from what actually shipped, and skips entries nobody remembered to mention. This generates it directly from the commit history using the Conventional Commits convention, so the changelog can't diverge from the commits it's summarizing — with a human editorial pass still required before anything lands on the main branch.

## The method

**1. Require Conventional Commits.** Every commit message follows `type(scope): summary`, with `type` from the standard set (`feat`, `fix`, `perf`, `security`, `refactor`, `style`, `docs`, `test`, `build`, `ci`, `chore`) and breaking changes marked either with `!` after the type/scope or a `BREAKING CHANGE:` footer. Enforce this with a CI linter that runs read-only against the commit range and returns non-zero on a malformed type or subject — catching it at PR time is far cheaper than catching it at release time. Only `feat`, `fix`, `perf`, `security`, and breaking changes need to appear in the rendered changelog; `docs`/`test`/`build`/`ci`/`chore` still have to pass the linter but are omitted from the reader-facing document.

**2. Map commit types to changelog sections.** Render a Keep a Changelog-style document with fixed sections — `Added` (from `feat`), `Fixed` (from `fix`), `Changed` (from `refactor`/`style`), `Security`, `Deprecated`, `Removed`, `Performance` — and omit any section with zero entries rather than printing an empty header.

**3. Auto-detect the semver bump.** Any breaking-change marker → MAJOR (or MINOR if the current version is still pre-1.0, per semver's own pre-release exception). Any non-breaking `feat` → MINOR. Everything else → PATCH. This removes the single most common release mistake — a human picking the wrong bump level under release-day time pressure.

**4. Write prepend-only, never overwrite.** New entries go at the top of the changelog file; historical sections are never rewritten or destructively replaced. This makes the changelog file itself an append-only audit log of every release.

**5. Human approval gate, always.** The generator drafts; it never writes to the changelog on the main branch without an explicit human pass. Commit messages are written for other engineers — changelog entries are written for users, and need a wording pass for clarity even when the underlying commit-type classification is correct.

**6. Validate the draft before it ships.** Before treating a draft as done: every bullet reads as user-meaningful (not internal implementation detail), every breaking-change entry includes the migration action a user needs to take, security fixes stay isolated in their own section, and there are no duplicate bullets across sections.

## Reference implementation sketch

Neither `changelog_generator.py` nor `commit_linter.py` ships with this skill — they're the minimal script you write against the contract below:

```bash
# Generate from a git tag range
git log v1.3.0..v1.4.0 --pretty=format:'%s' | changelog_generator.py \
  --next-version v1.4.0 --format markdown

# Lint commit messages in CI (non-zero exit blocks merge)
commit_linter.py --from-ref origin/main --to-ref HEAD --strict
```

The generator itself is a straightforward parse-classify-render pipeline: parse each commit subject into `(type, scope, breaking?, summary)`, classify into a changelog section plus a semver-bump vote, render the section templates, and emit both a human-readable Markdown draft and a machine-readable JSON form for CI to consume.

## When to use

- Before tagging any release.
- In CI, to auto-draft release notes and to block a PR whose commits don't follow the required format.
- Anywhere a project currently writes changelogs by hand after the fact and entries drift or get skipped.

Not for a marketing announcement (different audience, different tone) and not needed for an unversioned deploy with no discrete release boundary.

## How to use

**Install:** copy this folder into `~/.claude/skills/changelog-generator/` for personal use, or `.claude/skills/changelog-generator/` inside a project repo. Wire the linter into your CI as a required check on commit ranges.

**Invoke:**

```
Generate the changelog for v1.4.0 from the commits since v1.3.0 using
changelog-generator, and tell me the semver bump it detected.
```

```
Before we tag this release, run changelog-generator's commit linter over
the last 20 commits and flag anything that doesn't follow Conventional
Commits.
```
