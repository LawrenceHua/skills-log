---
name: public-repo-exposure-review
description: Turn an internal working repository into a public one without leaking identifiers, history or images: decide the public set by allowlist, build the tree fresh, run a scanner ladder proven able to fail, and flip visibility only as a recorded decision.
---

# Public repo exposure review

A public repository is permanent, indexed and forkable. Deleting it later does not unring it: forks, caches and clones exist within minutes. Every step below costs less than the flip.

A typical near-miss: a working repo with no remote, one `git remote add` from public, carrying a device hardware address in dozens of files, private LAN addresses in dozens of docs, the owner's email in a few dozen, absolute home-directory paths, internal tool names, and a post-mortem describing a real vulnerability that had been live. No secret scanner would have flagged most of it.

This skill answers one question: *what may leave, and who decided?* It is not a "does it work" review.

## 1. Decide the public set before you scan anything

First decide whether the repository must be public at all. A product page can ship from a private source (static build, hosted page); publishing the source is a larger, separate decision. A deadline is a reason to publish the page, not the repo.

A scanner finds only what it knows. The allowlist is the one control that covers classes no scanner has.

| Usually in | Usually out |
|---|---|
| a **new** README written for the public | internal docs: briefs, handoffs, decision logs, post-mortems (honest by design, hence unsafe) |
| a curated media set (after step 4) | forked third-party source (link upstream instead; avoids a licence question) |
| LICENSE, CONTRIBUTING, issue templates | server source that includes an account or adoption path |
| | binaries and firmware images (opaque to grep) |
| | logs, event rings, audio and transcripts of named people |
| | `.env` files, account registries, deploy config |

"Docs" means docs written for the public, not the docs that already exist. In one measured tree, more than half of all identifier findings sat in Markdown: the doc set was the leak surface, not the code.

Decide by walking the directory you are about to publish, never by `git ls-files`. Untracked files are missed by a tracked-file listing and shipped by `cp -R`.

## 2. Build private-first; the flip is a decision

1. Build the sanitized tree in a **new** directory with a fresh `git init`. Never sanitize in place; the internal record must survive.
2. Push it to a **private** repository first.
3. Run the scanner ladder (step 3) on a **fresh clone of that private repo**, not on the working tree.
4. Hand it to an independent reviewer (step 7) whose default verdict is REFUTED.
5. Flip visibility as a decision with a named owner: dated, listing what was scanned, by whom, with which tool versions. Never make it a step inside a script; a script that can flip visibility eventually will, unattended.

## 3. The scanner ladder

```sh
# 0  prove the ladder can fire on a seeded fixture first (step 5)
# 1  secrets by value, history and plain directory
gitleaks git . --redact --no-banner
gitleaks dir . --redact --no-banner
# 2  secrets by verification, including unknown
trufflehog filesystem . --results=verified,unknown
# 3  identifier classes neither tool knows (your own script, see below)
python3 redaction_check.py .
```

**Read the scanned-count, not the exit code.** Some scanners pointed at a directory with no `.git` print a fatal error, scan zero bytes and still exit 0. A ladder whose output carries no byte or commit count has no evidence it looked.

| Scanner | Catches | Cannot catch |
|---|---|---|
| secret scanner (by value) | credential shapes, high-entropy strings | a hardware address, an email, a hostname, a repo name |
| verifying scanner | provider-verified and unknown credentials | anything that is not a credential |
| your identifier checker | the classes you list by pattern | a value that looks ordinary, such as a name in a screenshot |

Write the identifier checker yourself, one rule per class: hardware (MAC) addresses, private IPv4 ranges, email addresses, absolute home-directory paths, internal hostnames, internal repository names, personal handles, project and tenant ids, key-shaped strings.

## 4. Images and audio are content, not metadata

- Strip metadata first (`magick mogrify -strip <files>`, or `exiftool -all= -overwrite_original`). Then re-read the metadata and paste the result; "stripped" is a probe, not a claim.
- Then open every image and look at it. A URL bar, a notification banner with a sender address, a path in a dialog, a hardware address on a device label, a person's name: all content. Scanners read bytes; nothing scans a picture.
- List rejected frames by filename in the review record. A rejection with no filename is a promise.
- A recorded human voice is personal data; a synthetic clip is not. Attribute every clip before publishing.

## 5. Prove the checker can fail

Give the identifier checker a `--selftest`. Each rule needs its own seeded sample that must be caught **by that rule** (a finding attributed to another rule is cross-contamination, not coverage) and its own clean sample that must not be caught. Keep a frozen `EXPECTED_RULES` list so deleting a rule, with or without its fixture, makes the selftest fail and name the rule. A checker that only fails when *zero* findings appear will pass with most rules missing.

A scanner that has never caught anything is untested, not clean. Run the ladder on the fixture first, then the tree, and record both exit codes.

## 6. The README is a claim surface

Public numbers need a source the artifact supports. Split claims explicitly into **works today / in progress / not built**, and drop any reliability adjective that was never measured. A public page that overclaims is one the owner must apologise for in public.

## 7. The reviewer brief

Give the reviewer the tree, the commands and the public set, never your reasoning or summary.

- Default verdict: REFUTED. The job is to find one thing that should not be public.
- It runs the scans itself and quotes output: scanner, version, command, scanned-count, exit code.
- It must also try a leak by hand: read the README as a stranger, open ten images, grep for the product's own LAN address, inspect history.
- A review quoting no command output is a second opinion, not a review.

## 8. History is part of the repo

```sh
git log --format='%ae %ce' | sort | uniq -c            # one identity, and the allowed one
git log --format='%s%n%b' | grep -niE '192\.168|([0-9a-f]{2}:){5}[0-9a-f]{2}|[[:alnum:]._-]+@[[:alnum:].-]+'
git log --oneline | wc -l                              # more than your commits? inherited history
git ls-files -s | awk '$1=="120000"{print $4}'         # symlinks that escape the tree
```

- A wrong author address can fail deploys on hosts that match commit identity, not just look untidy. Export `GIT_AUTHOR_*` / `GIT_COMMITTER_*`; do not rely on a checkout-local `user.email`.
- The sanitized repo must not inherit internal history. Fresh `git init`, new commits. A history rewrite does not delete what is already public: old commits stay reachable by SHA in forks and pull-request refs, and a shallow clone still ships one complete tree.
- Symlinks publish paths, and a followed link publishes the file.

## 9. Pre-flip checklist

1. Public set written down, every excluded class with its reason.
2. Sanitized tree built new; original untouched.
3. Private repo pushed; ladder run on a fresh clone of it.
4. Ladder exit codes and scanned-counts recorded; checker selftest shown failing, then passing.
5. Zero findings from all scanners, or each survivor accepted in writing by the owner.
6. Every image opened; rejected frames listed by filename.
7. README numbers re-derived from the tree; works / in-progress split explicit.
8. History: one identity, no inherited commits, no escaping symlinks, no identifiers in messages.
9. Reviewer's REFUTED report attached with quoted output.
10. The flip recorded as a decision with a named owner and the final URL.

## When to use

- Before making a repository public, open-sourcing it, or sharing a tree outside its team.
- When asked to sanitize, leak-check or secret-scan before publishing.
- When publishing a product page and deciding whether the source has to go with it.

## How to use

1. Copy this folder to `~/.claude/skills/public-repo-exposure-review/` (personal) or `.claude/skills/public-repo-exposure-review/` inside a project.
2. Ask Claude Code to use the `public-repo-exposure-review` skill by name.

Example prompts:

- "Use the public-repo-exposure-review skill: we want to open-source this repo next week. Propose the public set as an allowlist and the scanner ladder, but do not flip visibility."
- "Use public-repo-exposure-review to review this fresh private clone as a REFUTED-by-default reviewer and quote every scanner's version, command, scanned-count and exit code."
