---
name: manifest-bound-artifact-sync
description: Copy approved text artifacts through a fixed byte manifest and verify complete destination, staged, and committed changes before any authorized publication.
---

# Manifest-Bound Artifact Sync

## When to use

Use this skill to promote a selected set of text artifacts from mixed local folders into an approved version-controlled repository. It is useful when neighboring files contain private material, generated output, or unrelated work that must never be swept into a publication.

This is an additions-and-updates workflow. It does not delete destination files, edit source files, or imply permission to commit or publish.

## Working method

### 1. Pin scope and authority

Record the approved source roots, exact destination root, source-to-destination path mapping, destination branch, expected base commit, and intended audience. Separately record whether the user authorized local copying, committing, and remote publication. Proceed only as far as the existing authorization permits.

For remote publication, pin the approved repository destination and explicit branch. Inspect effective transport settings so an alias, alternate push destination, or URL rewrite cannot silently select a different repository. Do not print credentials or sensitive destination details in a public report.

Require exclusive write ownership of the destination paths for the operation. If another writer owns them or the ownership cannot be established, remain read-only. Start with a dry run even when execution is already authorized.

### 2. Verify the destination before discovery

Require the exact approved repository root and branch, a clean index and worktree, and no untracked files. Record the base commit. When synchronizing against a remote branch, verify that the local base equals a fresh read of that approved remote branch.

Inspect configured roots and every existing ancestor for symlinks. Reject symlink indirection, nested repository boundaries, and paths escaping an approved root. If a path or repository identity cannot be established, stop.

Do not clean, reset, stash, or overwrite unrelated work to make these conditions pass. Report the condition that needs resolution.

### 3. Select positively allowed artifacts

Enumerate only the approved source roots. Keep sources read-only. Apply a positive allowlist of artifact types and relative paths; exclusion patterns alone are insufficient.

For each candidate, inspect its complete relative path and decoded text. Exclude:

- Symlinks, including symlinked ancestors, and nonregular files.
- Binary or undecodable content, generated dependencies, caches, runtime state, and backup copies.
- Credential-bearing files, sensitive content, and material outside the intended publication scope.
- Material with uncertain ownership or permission to share.
- Paths that resolve outside an approved root or collide at the destination.

The mapping must be injective: two source paths cannot map to the same destination. Detect case and normalization collisions according to the destination filesystem. Reject reserved repository metadata paths and destinations inside nested repositories.

Inspect meaning as well as patterns. A clean pattern scan does not establish that a document is appropriate to share. If a generic rewrite is needed, prepare and review it separately in an authorized location; do not silently redact during copying or modify the original.

### 4. Freeze a reviewed byte manifest

Read each allowed source into an exact byte buffer. Compare it with the mapped destination using SHA-256 of the actual file bytes. Skip identical content with identical relevant mode.

For every remaining addition or update, freeze a manifest row containing:

- Source-relative and destination-relative paths.
- Change kind: addition or update.
- SHA-256 and byte length of the approved source buffer.
- Expected destination preimage SHA-256 and mode, or explicit absence.
- Approved destination mode where relevant.

Use the same raw-byte digest convention throughout. A repository object identifier is not a raw file SHA-256; never compare those different values as though they match.

The dry-run report lists the approved paths, change kinds, exclusions by safe reason, and intended endpoint: copied, committed, or published. Avoid reproducing rejected content. If the manifest is empty, report no eligible changes and stop without writes or an empty commit.

Review this exact manifest and its content under the applicable authorization. Freeze the result; any content, mapping, mode, or base change requires a revised reviewed manifest.

### 5. Revalidate and copy exact bytes

Immediately before the first write, repeat the destination, ownership, base, clean-state, and containment checks. For each row, re-read the source and confirm that its bytes and relevant mode still match the approved manifest. Confirm the destination still has the expected preimage or is still absent.

Recheck ancestors immediately before writing, including newly created directories. Copy the exact approved buffer to its mapped destination and apply only the approved mode. Do not re-render, re-encode, or normalize the text.

Use available filesystem protections against following links and overwriting unexpected files. These checks reduce accidental drift; they do not make a writable filesystem immune to races. If the available tools cannot enforce the required containment or exclusive ownership, stop.

### 6. Verify the entire local change set

Enumerate all actual changes against the recorded base, including untracked additions, deletions, type changes, and mode changes. The complete set must equal the manifest with no extra paths or unexpected change kinds. Re-read every destination and match its raw-byte digest and mode to the manifest.

If staging is authorized, stage only manifest paths. Then verify the complete index path set against the recorded base. Extract each staged blob's actual bytes and hash them with the same SHA-256 convention; verify modes too. Do not rely on a filename list or a successful stage command alone.

Filters or line-ending conversions can make staged bytes differ from copied bytes. Stop on such a mismatch and revise the reviewed manifest or workflow deliberately. Do not disable protections to force a pass.

If committing is authorized, confirm the base and verified index are unchanged immediately before committing. After the commit, verify its actual parent, full changed-path set, change kinds, modes, and the raw bytes of every committed artifact. The parent must be the recorded base and all changes must match the manifest. Recheck the worktree and index for unexpected leftovers or concurrent edits.

### 7. Publish only a verified commit when authorized

Read the approved remote branch again before publication. If it has moved, stop for reconciliation; never force publication. If a rebase is explicitly authorized, stop on conflicts and preserve the work for resolution. After any history rewrite, repeat the parent, complete change-set, and committed-byte checks against the approved new base before proceeding.

Push only the exact verified commit to the pinned repository destination and explicit branch. A branch name alone can move between checking and pushing. Keep hooks and other protections enabled.

Read the remote ref afterward and compare it with the verified commit. If a timeout or transport failure leaves acceptance uncertain, reconcile through a fresh remote read before considering another push. Do not retry blindly.

### 8. Report the proven endpoint

Report the count and safe relative paths of accepted artifacts, manifest verification result, exclusions by category, and the furthest verified endpoint. Distinguish local copies, staged content, a local commit, and a confirmed remote ref.

On any mismatch, stop subsequent writes, retain evidence without exposing private content, and preserve unrelated work. Do not perform a destructive automatic rollback. State the failed check and the next action needed to reconcile it.

## How to use

1. Copy the whole `manifest-bound-artifact-sync` folder into `~/.claude/skills/` for personal use, or into `.claude/skills/` inside a project.
2. Restart or refresh the session if needed so Claude Code discovers the skill.
3. Ask Claude Code to use `manifest-bound-artifact-sync` by name, specifying the source roots, destination, allowed artifact paths, and permitted endpoint.

Example prompts:

- "Use manifest-bound-artifact-sync to dry-run copying the approved templates from notes/templates into the repository's templates folder. Show the exact manifest and exclusions."
- "Use manifest-bound-artifact-sync to copy the reviewed documentation manifest and verify the complete local change set. Stop before staging or publication."
