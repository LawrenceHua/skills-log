---
name: scheduled-job-proof-layers
description: Prove a scheduled automation (cron, timer, launchd-style agent) really works by verifying four independent layers — source, installed scheduler definition, runtime code actually loaded, and a fresh semantic receipt — because "last exit = 0" and "the fix is merged" each prove far less than they sound like.
---

# scheduled-job-proof-layers

A scheduled job can fail to do its job while every dashboard stays green. The scheduler says it ran and exited 0. The fix was merged yesterday. Tests pass. And the job is still executing last week's code from a stale checkout, under a definition nobody updated, writing a receipt nobody reads. This method splits "the automation works" into four layers, each proven independently, and refuses to say `VERIFIED` until all four agree.

## The core rule

**A scheduler reporting "last exit = 0" proves one thing: a process exited successfully.** It does not prove the installed definition is the one you intended, that the runtime is executing the code you merged, or that the outcome the job exists to produce actually happened. Merged code plus stale runtime bytes is `CODE-SHIPPED-NOT-VERIFIED` for the automation — not a partial pass.

## The four layers

| Layer | Question it answers | Proof to collect |
|---|---|---|
| **1. Source** | Is the intended code correct at the intended revision? | Tests/lint/typecheck run against a named commit SHA (record the SHA) |
| **2. Installed definition** | Is the scheduler actually configured the way you think? | The definition read back from the *live* scheduler: name/label, exact command and arguments, environment, working directory, schedule, enabled state |
| **3. Runtime code** | Are the bytes the job executes the bytes you shipped? | The commit the runtime checkout is on (and whether it's clean), plus content hashes of the transitive sources the job loads — entry script, imported modules, config files, prompt/template files, wrapper scripts |
| **4. Semantic receipt** | Did the last run produce the intended outcome, *after* the change? | A receipt or provider readback from a run that started after the deploy: the output artifact, the record in the downstream system, the message actually delivered — with a timestamp newer than the change |

Each layer can be green while another is red. That is the point: a single "it works" signal collapses four separate ways to be wrong.

## Procedure

1. **Name the claim and the revision.** Write down what the automation is supposed to do and the exact SHA you believe is deployed. Every later check is against that SHA.
2. **Layer 1 — source.** Run the narrowest relevant tests on that SHA. Record the command and result. This layer alone earns no "deployed" claim.
3. **Layer 2 — read the live definition, not the file you edited.** Query the scheduler itself:
   - cron: `crontab -l` (and the system crontab / cron.d entries if applicable)
   - systemd: `systemctl --user cat <unit>` and `systemctl --user list-timers`
   - launchd: `launchctl print gui/$(id -u)/<label>`
   The definition file on disk can differ from what's loaded — an edited-but-never-reloaded definition is a classic silent failure. Compare command, arguments, environment, working directory, and schedule against intent.
4. **Layer 3 — pin the runtime bytes.** In the directory the job actually runs from:
   ```bash
   git -C <runtime-dir> rev-parse HEAD
   git -C <runtime-dir> status --short
   shasum -a 256 <entry-script> <each-transitively-loaded-file>
   ```
   Compare `HEAD` and the hashes to your Layer 1 SHA. Build the file list from what the job really loads (follow its imports and config reads), not from the files you happened to change. A job that runs from a copy, a virtualenv, a container image, or a vendored directory needs *that* location checked.
5. **Layer 4 — read a fresh receipt.** Find the receipt or downstream record produced by a run that started *after* the deploy. Confirm it shows the intended outcome (the row exists, the file has the expected content, the notification arrived) — not merely that a run happened. If the newest receipt predates the change, this layer is unproven.
6. **Label per layer, then overall.** Use the lowest label any layer earns:
   - `VERIFIED` — all four layers proven this session, with the commands.
   - `CODE-SHIPPED-NOT-VERIFIED` — code is merged/tests pass, but Layer 2, 3, or 4 is stale, unread, or mismatched. Name which.
   - `BLOCKED` — a layer can't be read (no access to the scheduler, runtime host unreachable). Name the blocker.
   - `INCONCLUSIVE` — evidence is ambiguous (receipt is present but can't be tied to the new revision).

## Don't re-run the job as a diagnostic (unless it's provably harmless)

The tempting shortcut for Layer 4 is to trigger the job by hand and see what happens. **Don't do that if a run can commit or push, invoke paid models or metered APIs, publish artifacts, send messages, or write to any external system** — a diagnostic run is a real run and its side effects are real. Instead:

- Prefer reading the existing receipts and provider state.
- If you must exercise it, use a **no-side-effect rehearsal you have proven is one**: a dry-run flag verified to skip the writes, a sandbox target, a stubbed provider. "Proven" means you checked what the rehearsal does (read the flag's code path or watch the outbound calls), not that the flag is named `--dry-run`.
- If no safe rehearsal exists, wait for the next scheduled run and read its receipt, or get explicit approval for one real run.

## When it works by hand but fails on schedule

A failure that appears only under the scheduler is a **harness suspect** until proven otherwise. Scheduled runs differ from your shell in interpreter, `PATH`, working directory, environment variables, user, and available credentials. Reproduce with the same conditions before touching the code:

```bash
env -i HOME="$HOME" PATH="<the scheduler's PATH>" \
  sh -c 'cd <the scheduler'"'"'s working dir> && <the exact scheduled command>'
```

(Only for jobs that pass the side-effect check above.) If it fails there too, the bug was never in your logic — it was in the environment contract.

## Report shape

```
Automation: <name>   Intended SHA: <sha>
L1 source:       VERIFIED   — <test command> @ <sha>
L2 definition:   VERIFIED   — <scheduler readback command>; command/env/schedule match
L3 runtime code: MISMATCH   — runtime HEAD <sha2>; <file> hash differs
L4 receipt:      INCONCLUSIVE — newest receipt <ts> predates change
Overall: CODE-SHIPPED-NOT-VERIFIED — runtime still on old bytes; next action: update runtime checkout, re-read L3, wait for next run, read L4
```

## When to use

- After merging a fix to any cron job, timer, background agent, or scheduled pipeline, before saying it's fixed.
- When a job's scheduler status is green but its output looks stale or wrong.
- When a fix "works on my machine" but the scheduled run still fails.
- Before trusting a health dashboard that only reports process exit codes.

## How to use

**Install:** copy this folder into `~/.claude/skills/scheduled-job-proof-layers/` for personal use, or `.claude/skills/scheduled-job-proof-layers/` inside a project repo. Then ask Claude Code to use the skill by name.

**Invoke:**

```
I just merged a fix to the nightly export job. Use scheduled-job-proof-layers to
tell me whether it's actually fixed — check all four layers and label the result.
```

```
The scheduler shows my sync job exiting 0 every hour but the destination is stale.
Walk scheduled-job-proof-layers and find which layer is lying — and don't re-run
the job unless you can show the rehearsal has no side effects.
```
