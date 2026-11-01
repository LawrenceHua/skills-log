---
name: safe-archive-transfer
description: Safely archive, back up, sync, or migrate files, repositories, datasets, and credential-bearing project trees to cloud or remote storage with one manifest, a secret preflight, and verified recoverability before any local deletion.
---

# Safe archive transfer

Protect confidentiality and recoverability across the whole transfer. The invariant: **no bytes move until one manifest and one secret policy cover every source root.**

## Workflow

1. **Bound the operation.**
   - Separate read-only discovery, external transfer, credential changes, and local deletion into distinct phases.
   - Confirm destination ownership, retention/versioning/trash behavior, quota, encryption expectations, and whether source retirement is actually requested.
   - Treat prior blanket approval as scoped to the task, not permission for unrelated deletion or credential changes.

2. **Build one source manifest.**
   - Enumerate every promised root, including repositories or datasets outside the main tree.
   - Record the destination, filters, approximate bytes and files, symlink behavior, and restore location for each root.
   - Reuse the same manifest and filters for preflight, transfer, verification, and reporting. Never scan one tree and upload a broader one.

3. **Finish the secret preflight before the first byte moves.**
   - Scan names for live `.env*` files while allowing explicit templates (`.env.example`, `.sample`, `.template`).
   - Scan for private keys, PEMs, keystores, credential and service-account files, auth configs, database dumps, and provider token files. Use a content scanner such as `gitleaks` when available, and never print matched values.
   - Classify every match as template, excluded live secret, or intentionally encrypted payload. Treat "no secrets" as refuted until every source root has been scanned with the same or a broader policy.
   - For an intentionally encrypted payload: create it in private staging, verify its format, do a user-assisted decrypt-and-list before any upload, and show the plaintext source is excluded from the plan.
   - Keep passphrases out of the agent transcript. The user types them directly into the trusted tool, stores them in a password manager, and replies only that the step is done.
   - Validate authentication with a narrow provider probe; never print raw connector or sync-tool configuration.

4. **Harden the transfer runner.**
   - Strict failure handling (`set -euo pipefail` or equivalent).
   - Preserve critical exit statuses: do not pipe a decisive copy or check through `tail` or `grep` unless the original status is captured explicitly.
   - Make each manifest entry an explicit phase with a result; print "done" only after every required transfer and check passed.
   - Use resumable operations, an atomic single-instance lock, logs that exclude credential values, and staged-plus-atomic installation if the runner may already be executing.

5. **Execute conservatively.**
   - The real runner must fail closed on a machine-readable per-root preflight result; prose or an unchecked checklist is not a gate.
   - Dry-run from the final manifest and filters, inspect representative included and excluded paths, and exercise secret-shaped canary filenames before the real transfer.
   - Do not delete or rewrite local originals during upload. Pause on unexpected paths, authorization errors, partial failures, or a killed watcher.
   - After an interruption, cancellation, or denial, reconcile local processes, remote partial objects, and per-phase state before resuming.

6. **Verify recoverability.**
   - Check every promised source/destination pair, not only the largest. Keep the transfer/check exit code plus file counts and bytes.
   - Confirm encrypted bundles are present and plaintext counterparts absent remotely; do a user-assisted decrypt-and-list or a representative restore without exposing the passphrase.
   - Audit remote contents with the same secret policy, including provider trash, versions, and object history when deletion semantics matter.

7. **Retire sources separately.**
   - Require a new, explicit deletion decision after transfer and restore verification.
   - Prefer quarantine or trash with a manifest and a retention window. Delete permanently only when the exact targets and rollback implications are understood.

## If a credential is exposed

- Pause every transfer that uses it.
- Do not echo, quote, log, or pass it as a command-line literal.
- Revoke or rotate only with explicit authorization, then verify the old credential fails with a narrow non-secret probe.
- Re-authorization that needs provider consent is a user action; ask the user to complete it without pasting generated tokens.
- Treat already-uploaded secret objects as present until destination enumeration and deletion verification prove otherwise; rotate the underlying secret if it may be live.

## Completion status

Use exactly one:

- `VERIFIED`: every manifest phase transferred and checked, and the restore probe passed.
- `CODE-SHIPPED-NOT-VERIFIED`: scripts or filters changed, but transfer, check, or restore proof is incomplete.
- `BLOCKED`: required authorization, quota, credential consent, or user-only passphrase work prevents continuing.
- `INCONCLUSIVE`: checks ran, but remote state or recoverability remains uncertain.

## When to use

- Before any bulk copy or upload with rclone, rsync, a drive client, S3 tooling, or tar.
- Migrating project trees that may contain credentials to another machine or service.
- Especially when you plan to delete the local originals afterward.

## How to use

1. Copy the `safe-archive-transfer` folder into `~/.claude/skills/` (personal) or `.claude/skills/` inside a project, then ask Claude Code to use the skill by name.
2. Example prompts:
   - "Use safe-archive-transfer to plan moving these four project folders to object storage. Build the manifest and secret preflight before anything uploads."
   - "I want to delete my local copies after backing up. Use safe-archive-transfer to tell me what has to be verified first."
