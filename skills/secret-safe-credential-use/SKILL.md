---
name: secret-safe-credential-use
description: Use an API key, token or password in agent work without printing, copying or storing it, by checking presence by name, injecting it into one child process at use time and scanning outputs for leaks.
---

# Secret-safe credential use

An agent that can run commands can leak a secret in a dozen quiet ways: a debug echo, a traced shell, a process argument, a config dump, a pasted log. This skill keeps the value inside one process for one command.

**The rule:** never put a secret value in chat, files, logs, prompts or commits. Refer to where it lives (a vault item, a keychain service name, an environment variable name). Creating, rotating and revoking credentials belongs to the human owner.

## 1. Check presence, not value

```sh
# macOS Keychain: the exit code answers "is it there?"; all output is discarded
security find-generic-password -s "<service-name>" >/dev/null 2>&1 && echo PRESENT || echo "NOT-FOUND-OR-UNREADABLE"

# Environment variable: report set or unset only
[ -n "${MY_API_KEY:-}" ] && echo SET || echo UNSET
```

If a credential is missing, ask the owner to add it. Do not search the disk for a copy.

## 2. Use it for exactly one command

Prefer a tool's own stored login (for example a cloud or source-control CLI that is already signed in) over handling any token yourself.

```sh
# OS keychain: read inside a subshell, fail closed, hand it to one child
(
  set +x
  v="$(security find-generic-password -s "<service-name>" -w)" || exit 3
  [ -n "$v" ] || exit 3
  MY_API_KEY="$v" exec <command>
)
```

On Linux the lookup line can use your secret store's CLI (for example `secret-tool lookup service <service-name>`). With a password manager that supports references, keep only references on disk:

```sh
# refs.env holds lines like  MY_API_KEY=op://<vault>/<item>/<field>
op run --env-file=refs.env -- <command>
```

The program must read the secret from its environment or standard input, never from a command-line argument, because arguments show up in process listings. Environment variables can still be visible to the same user or an administrator, so keep the child short-lived.

## 3. Scheduled jobs

The job definition (cron line, launchd plist, systemd unit) carries only indirection: a wrapper that looks up the secret at launch, or a path to an owner-only (`0600`) file that the wrapper loads. Never write a value into the definition's environment block.

Do not dump job definitions or process environments to "check" them. Commands that print a job's or container's full environment will print the secret.

## 4. Prove nothing leaked

- To show two stored values match without revealing them, compare short prefixes of their SHA-256 hashes. Do this only for long random keys, never for human-chosen passwords.
- Before sharing logs, receipts or evidence folders, run a maintained secret scanner with redaction turned on (for example `gitleaks dir <folder> --redact`).
- To check for one specific value without putting it in an argument or on screen, feed it as a pattern file and list file names only. Guard against an empty value, which would match everything:

```bash
(
  set +x
  v="$(security find-generic-password -s "<service-name>" -w)" || exit 3
  [ -n "$v" ] || exit 3
  grep -rlF -f <(printf '%s\n' "$v") <folder>
)
```

A clean scan covers the patterns and values it checked, nothing more.

## 5. If a secret escaped

A value that reached a chat, a commit, a shared file or a third-party service is an incident. Report the **location** (never the value) to the owner immediately. Deleting the line or rewriting history does not undo exposure; the owner decides on rotation.

## Never

- Never `echo`, `cat`, `printenv` or trace (`set -x`) around a secret.
- Never print a vault read to the terminal.
- Never pass a secret as a command-line argument; use the environment or standard input.
- Never open credential files to read their contents. Checking that they exist, their size or their permissions is fine.
- Never copy browser cookies or session files to another place or agent.
- Never reuse a credential another workflow has been told is off limits.
- Never paste a secret into a model prompt, search query, ticket or pull request.

## When to use

- A task needs an API key, token or password.
- You are writing a scheduled job or service that needs one.
- A log, report or evidence bundle might contain one before you share it.

## How to use

1. Copy the `secret-safe-credential-use` folder into `~/.claude/skills/` for personal use, or `.claude/skills/` inside a project.
2. Ask Claude Code to use the skill by name.
3. Example prompts:
   - "Use the secret-safe-credential-use skill to run this deploy script with the key stored in my keychain, without the value ever appearing in output."
   - "Use the secret-safe-credential-use skill to review this scheduled job for places where the token could leak."
