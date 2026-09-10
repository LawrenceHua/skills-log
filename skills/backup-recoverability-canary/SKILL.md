---
name: backup-recoverability-canary
description: Before treating an encrypted off-site backup as grounds to delete local originals, prove round-trip recoverability with a synthetic canary — upload known test data, verify it through the encrypted path, and independently escrow the recovery key — instead of trusting "upload succeeded."
---

# backup-recoverability-canary

"The backup job completed" and "this backup is actually recoverable" are different claims. An encrypted remote backup can report success while being silently unrecoverable — a misconfigured encryption remote, a key that was never actually escrowed anywhere else, or a checksum step that got skipped. This method proves recoverability with a disposable synthetic canary before that backup is ever used as justification to delete the local original, and separately proves the recovery key itself isn't a single point of failure.

## The method

**1. Never let deletion follow directly from "upload succeeded."** Treat "backup exists" and "backup is provably recoverable" as two separate gates, and require the second one, freshly checked, before authorizing removal of any local original.

**2. Run a synthetic canary through the real encrypted path.** Generate throwaway test data (not real data) and a narrowly-permissioned local test key. Configure an encrypted remote pointing at your actual backup destination, upload the synthetic canary through it, and run whatever integrity check your backup tool provides natively (many encrypted-remote tools, like `rclone`'s `crypt` backend, offer a native `cryptcheck`-style hash comparison between plaintext and ciphertext).

**3. Have a fallback when the native check is structurally impossible.** Some configurations — for example, an encrypted remote layered on top of another encrypted remote — expose no hashes for a native integrity check to compare against. When that's the case, fall back to: inspect the raw ciphertext to confirm it's actually encrypted (not silently stored in plaintext), then do a full download back through the encrypted path and compare its checksum against the original. Record which check path you actually used in the result — a fallback path proves the same thing, but you want to know which one ran.

**4. Bind the result to the exact tool version that produced it.** Record the hash (and, if available, the version-control revision) of the script or tool that ran the canary. A "verified" result from six tool-versions ago is not evidence the current setup still works — treat verification as something that expires when the tooling changes, not something you check once and remember forever.

**5. Escrow the recovery key independently, and verify the escrow copy too.** A single copy of the encryption/recovery key, even if backed up, is a single point of failure if that backup and the key live behind the same account, the same disk, or the same person's memory. Store a second, independent copy of the key in a genuinely separate system (a different backup mechanism, with its own independent password/credentials) — then actually restore and hash-verify that second copy too, rather than trusting that "it's stored somewhere else" is sufficient on its own.

**6. Report one of three states from current evidence only.** `VERIFIED` — the canary round-tripped through the real path and the key escrow copy was independently restored and verified, both in this check. `BLOCKED` — a required step couldn't run (missing access, the remote isn't reachable). `INCONCLUSIVE` — a step produced an ambiguous or partial result. Never infer "still verified" from an old result; a changed remote, rotated credentials, or an updated tool version invalidates it.

## Safety invariants

- Never print, log, or upload real key material — only its hash or a redacted reference, where you need to record it at all.
- Never inspect or copy credential files, `.env` files, or the tool's own config as a side effect of running the canary.
- Keep any state file this check writes narrowly permissioned (owner-read-only) and in a fixed, non-symlinked location.
- This check proves mechanics, not policy — it never issues a deletion command itself. Pair a `VERIFIED` result with a separate, explicitly human-approved retention/deletion step; don't let the canary's success silently become the deletion trigger.

## When to use

- Before deleting local originals of anything you're relying on an encrypted backup to preserve — session histories, archives, personal records.
- Setting up a new encrypted backup destination and wanting proof it actually works end-to-end, not just that the first upload didn't error.
- Periodically, on a schedule, for any backup path that gates a real deletion decision — tooling and credentials drift, and a canary from months ago doesn't cover today's configuration.

## How to use

**Install:** copy this folder into `~/.claude/skills/backup-recoverability-canary/` for personal use. Implement the canary against whichever encrypted-backup tool you actually use (`rclone crypt` + a restore, `restic`, or an equivalent — the method is the same regardless of tool: synthetic data, real encrypted path, independent key escrow, round-trip proof).

**Invoke:**

```
I want to delete these local files now that they're backed up to the encrypted
remote. Run backup-recoverability-canary first — prove the round trip actually
works and that the recovery key is independently escrowed.
```

```
It's been a few months since I last checked this backup's recoverability and
the tool version changed. Re-run backup-recoverability-canary before I trust it
for anything new.
```
