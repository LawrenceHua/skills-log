---
name: unattended-deletion-runner-hardening
description: Build, test, and review a tool that deletes or moves files in unattended passes — lock handling, preview-and-approve bound to a hash, a fail-closed git-state gate, isolated tests, mutation-proved fixes, and fresh-context review.
---

# Unattended deletion runner hardening

A runner that deletes while nobody watches must refuse by default, ask before each pass, and prove its own fixes. This is the protocol for writing, testing, running, and reviewing one (stale-worktree sweeps, retention jobs, disk reclaim).

Related but separate: a per-path "is anything still referencing this?" screen, and knowledge of which space is safe to reclaim. This skill covers the runner around them.

## 1. Runner protocol

1. **A lock refusal is not a pass.** Before each pass, wait in short polls while the lock file is held or another instance of the tool is running; if the newest run's error says it "holds the lock", retry the same pass uncounted. (A collision can burn every pass of a night, each one empty and failed.)
2. **Stop on the last apply row per path being an error, not on any error row.** Write an intent row (phase: before) ahead of every removal and a final DONE or REFUSED row after it; an intent row alone is not a failure.
3. **Size passes.** Small first pass (e.g. 5 rows), then a bounded larger size under a time cap; a maximum pass count; a pause after each completed pass so other lanes can take the lock. Re-read the hold/ack file before each pass and again immediately before applying.
4. **Message a live recipient.** Final notices addressed to an already-exited session are lost; also keep a copy for the verifier.
5. **Bind approval to the preview.** Approval id = first 12 hex of sha256 over the pass number, planned start time, and the preview paths joined by newlines — any change to pass, time, or paths changes the id. Planned start = now plus a margin, rounded up to a whole minute and moved out of blocked windows. The preview message's first line carries id, row count, and planned start, then every path verbatim.
6. **Apply only on an exact approval line** (e.g. `GO <id>`) present before the planned start. Silence skips the pass; an approval for another id never counts. If the preview was delivered with too little time left, log "landed late" and skip.
7. **The skip path applies nothing and counts no pass.** Wait, then preview again with a new id. After three silent previews in a row, stop the run and say why in the summary and final messages; an approval resets the count.
8. **After approval, re-filter and re-gate.** Apply new exclusions, intersect with the saved preview so a refill cannot add an unseen row, and pass every path through the git gate. Immediately before applying, recheck the hold, apply windows, load ceiling, and tool lock; recompute the cap and keep only the first cap previewed rows in preview order. A failed recheck skips and is not "silent".
9. **Dropped rows persist for the run.** Append `<UTC>\t<path>\t<reason>` to a file named for the run start and skip those paths on every later screen. When nothing is left, log it and stop; never loop on rows that already failed.
10. **Classify by origin, not by folder name.** Use the remote URL and the git common directory (`git config --get remote.origin.url`, `git rev-parse --git-common-dir`); checkouts belonging to another organization can pass a name screen.

## 2. The git-state gate (read-only)

Per path, print `PASS`, `FAIL`, or `NOGIT`, the path, and the reason. The process exit code is 0 for any verdict, so the caller must read the first field.

1. **PASS** requires all of: no tracked changes (`git status --porcelain --untracked-files=no` empty), nothing ahead of its upstream (`git log --oneline @{u}..` empty when an upstream exists), and `git branch -r --contains HEAD` non-empty. A large share of "clean and idle" candidates typically fail the last two.
2. **NOGIT** needs all three: `git rev-parse --show-toplevel` exits 128, stderr says "not a git repository", and the path has no `.git` entry at all. A gitfile pointing at a missing git directory prints the same stderr and must FAIL. Timeouts and any other failure are FAIL.
3. **Unset** `GIT_DIR`, `GIT_WORK_TREE`, `GIT_COMMON_DIR`, `GIT_INDEX_FILE`, and `GIT_CEILING_DIRECTORIES` for every git call; a stray `GIT_DIR=/nonexistent` makes a healthy repo look broken. Missing, ambiguous, or crashed output drops the row.
4. Run liveness checks first: even `git status` can refresh an index timestamp that other screens read.

## 3. Test without touching real state

1. **The test base is an override variable with a guard:** refuse to start when it is at, inside, or above the real base, or empty. Do not write a test plan that needs both the guard and a scratch directory inside the guarded base.
2. **Put fixtures and the temp dir outside every git work tree.** A suite run with its temp dir inside a repo failed over a hundred assertions through unrelated containing-repository refusals; the rerun outside git passed with no source change.
3. **Stub time and neighbors:** a moving fake clock, fake sleep, date, process-list, lock-holder, and load probes, and message senders; assert exact approval ids and planned starts. Keep one test real: hold an actual lock with a live process and kill that exact pid.
4. **Run suites in a clean environment** (`env -i` with a minimal PATH, a fabricated HOME and TMPDIR, `LC_ALL=C`, no bytecode writing, low priority), one heavy suite at a time, after checking load against the ceiling.
5. **Never edit a file a running suite executes or imports.** A shell reads a script by offset, so an in-place edit changes what the running script does. Edit a copy, syntax-check it (`bash -n`, `python3 -m py_compile`), then rename it over the original.

## 4. Prove each fix

1. **Revert each change alone, in a copy,** and run its matching case: it must fail on a *behavioral assertion*. Timeouts, syntax errors, import failures, and an unrelated early refusal are invalid kills. A case that still passes after its revert means the change is not done.
2. **Report survivors.** Where two guards cover one protection, show a combined reversion that removes it and fails the safety assertion, then restore and pass again. A changed refusal reason while the operation still refuses proves nothing.
3. **Audit every removed guard and assertion;** the original test methods must all survive.

## 5. Review protocol

1. Implementers report `CODE-SHIPPED-NOT-VERIFIED` with files, exact commands, logs, test count, zero skips, and hashes. Only an independent reviewer moves it, in a fresh context, starting from "refuted": it gets the commit and raw source and tests, not the claims; it mutates its own copies and re-runs earlier attacks against the candidate; its verdict gives file:line, input, expected versus actual, and a reproduction command. It does not implement or clean up scratch.
2. **Blind the fix worker:** it gets the finding *category* only, never the reviewer's scripts or inputs. The orchestrator reproduces each rejected finding before dispatching a fix, and each fix round is judged by a new fresh-context reviewer.
3. VERIFIED covers the stated requirements only and grants no authority to run on real data. Write the material limits down, list unmet gates, and never call a blocked broad guard "passed" — narrow the audit to named files.

## 6. Evidence hygiene

- Pin `LC_ALL=C` when fingerprinting file lists; default collation hashes the same list differently.
- Keep evidence and replay mutations on a new physical copy; do not clean up audit scratch.
- Disk-free deltas under concurrent activity do not reconcile to savings.
- A shared tool lock can starve a second lane; say in advance who yields.

## Never

- Never count a lock refusal as a pass.
- Never stop or continue on "any error row" — the intent row precedes every removal.
- Never apply a preview without an exact approval for its id, or one that landed late.
- Never read a timeout, a broken gitfile, or an unknown git failure as NOGIT, or clear a row by folder name.
- Never put fixtures inside the real base or a git work tree, or edit a script while it is executing.
- Never accept a fix whose test still passes when the fix is reverted, or hand a fix worker the reviewer's scripts.
- Never read VERIFIED as permission to run on real data.

## When to use

- Writing or changing a cleanup, retention, or deletion runner.
- Asking why a runner skipped, stopped, or burned its passes.
- Wanting approve-before-delete for unattended runs.
- Reviewing a deletion tool before it touches real data.

## How to use

1. Copy the `unattended-deletion-runner-hardening` folder into `~/.claude/skills/` (personal) or `.claude/skills/` inside a project, then ask Claude Code to use the skill by name.
2. Example prompts:
   - "Use unattended-deletion-runner-hardening to review my stale-worktree cleanup script before I schedule it."
   - "Design the preview-and-approve flow for my nightly cleanup using unattended-deletion-runner-hardening, including the approval id format."
