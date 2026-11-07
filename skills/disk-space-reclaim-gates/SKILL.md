---
name: disk-space-reclaim-gates
description: Free space on a nearly full Mac or Linux dev machine without losing work or trusting a lying measurement: baseline, why a delete freed nothing, ownership and liveness checks, git clone and worktree gates, safe execution, verification.
---

# Disk space reclaim gates

Measure first, classify owner and liveness, gate every git checkout, delete only what is provably dead, then prove the free-space number actually moved.

## 1. Measure first, before touching a file

1. Run `df -Pk "$HOME"` before and after; report Used, Available and Capacity %. With other writers active, attribution is only good to about 10 percent; claim no finer.
2. A delete whose `df` change is far smaller than the bytes removed is **pinned**, not failed. Look in this order:
   - **Local snapshots** (macOS: `tmutil listlocalsnapshots /`). APFS keeps every block a snapshot references. If the backup is finished or stopped, `tmutil deletelocalsnapshots <date>` works as the plain user. In one case a 9 GiB delete moved `df` 0.7 GiB; deleting the snapshot freed 21 GiB.
   - **Swap on the VM volume** (`df -g`, `sysctl vm.swapusage`). Swap lives on its own volume in the same container, so swap growth is disk loss that `du` never sees. Rank memory holders with `top -l 1 -o cmprs`. Orphaned whole-disk scans (`find`, `du` over `/`, parent pid 1) can hold gigabytes; stop them by exact pid, never by name.
3. Volumes in one APFS container share one free pool. Delete regenerable bulk in place and move only what you need.

## 2. Owner first, then liveness

1. Classify the owner of every candidate before any move or delete. Work or client material is kept where policy says; never move it to personal storage or the cloud to make room (a disclosure cannot be undone). Under pressure, compress in place.
2. Classify git checkouts by `git -C <path> config --get remote.origin.url` and `git rev-parse --git-common-dir`, never by folder name. Run any keyword census on a folder known to match before believing a zero.
3. Liveness needs every check below; one hit keeps the folder:
   - a path-reference gate (processes with the path open, loaded scheduler jobs, crontab and config entries naming it);
   - docs and README/handoff files that mention the basename;
   - installed tools and scheduler definitions (also grep wrappers that exec into the folder: definition, then wrapper, then folder is two hops);
   - tracked source in your production repos;
   - any agent claim/lease files.
4. Recent-touch rule: `find <path> -mindepth 1 -newermt "-12 hours" ! -newermt now`. Without `! -newermt now`, future-dated files make a dead tree look live. Use `git --no-optional-locks status`; a plain `git status` rewrites `.git/index` and fakes recent activity.
5. A label is not liveness. A tree called "archive" can have a running collector. Read the scheduler's job list.

## 3. Git checkouts and worktrees

Bucket every entry before removing anything and keep that record as the only copy of pre-sweep state: DIRTY, NO-GIT, LOCAL-ONLY-COMMITS, CLEAN-UNVERIFIED, MERGED-CLEAN, LIVE, BROKEN-LINKAGE.

1. Reclaim a checkout only after all gates: not live; idle 7 days; no child worktrees; clean with no stash; HEAD on an off-machine remote-tracking ref, else a verified bundle: `git bundle create <file> --all`, `git bundle verify <file>`, then prove the restore with `git clone <file> <dir>`.
2. Row test for sweeps: no tracked changes; `git log @{u}..` empty if an upstream exists; `git branch -r --contains HEAD` non-empty. A stale remote ref only causes a false refusal, the safe direction.
3. A bare clone is the object store of its linked worktrees. Deleting it can lose branch histories. Hold any clone that hosts children.
4. Dirty work and NO-GIT folders (no remote, no copy) are reported, never reclaimed.
5. A directory's name is not its ownership. Before deleting a cache-named directory run `git -C <wt> ls-files -- <dir> | head -1`; any output means tracked source, skip.
6. Symlinks into external volumes free 0 bytes; classify and skip. Keep caches the next build will reuse.
7. `git worktree prune` drops administrative records only (0 bytes); confirm the path is absent first.

## 4. Execute

1. Print every resolved absolute path first; delete from an explicit absolute allowlist in a loop; never run a recursive delete on a path computed at run time.
2. Caches use the vendor command (`pnpm store prune`, `npm cache clean --force`, `brew cleanup -s`), not `rm`. A held lock refuses.
3. Sparse files: a VM disk image may show 900 GB apparent and 5 GB allocated, and a cross-volume `mv` can begin materialising it. Compare apparent with allocated size before any cross-volume move.
4. Quarantine (move) only when reversibility is the point; every row carries a restore command and the index stays beside what it indexes.
5. The Trash waits for an explicit owner decision. A sweep that must repeat becomes a report-only tool with `--apply` to act and the gates built in.

## 5. Verify

Re-run `df -Pk "$HOME"` and state the percentage change. Confirm zero removals from protected buckets and prove one restore from a bundle. Note macOS units: `du -sk` is KiB, plain `du -s` is 512-byte blocks, BSD `du` has no `--apparent-size`.

## 6. Scripts and monitors that lie

- A bare PATH (non-login ssh, a scheduler job, `env -i`) may lack your package manager's bin directory, so `timeout` is "not found". A scan that hides stderr then prints an empty result with exit 0. Export PATH, start with `command -v timeout || exit 3`, and dry-run the capture.
- A capture a few dozen bytes long is an error message, not evidence. Read it.
- Never scan `$HOME`, Desktop, Documents, Downloads or Library on macOS: a blocked privacy-protected scan can freeze the whole agent process. Name subdirectories and bound every scan with a path, `timeout` and `| head`.

## Never

- Never call a delete failed, or a reclaim done, from the delete alone; read `df`.
- Never accept SAFE from a path gate's default roots alone; add the doc, scheduler and tracked-source greps.
- Never delete a clone that hosts child worktrees, a dirty tree, a stash or unpushed commits without a verified bundle and a restore test.
- Never move a sparse file or bulk tree across volumes without checking apparent versus allocated size.
- Never read an empty scan as zero.

## When to use

- The disk is full or filling with no obvious large files.
- `df` did not move after a delete.
- Someone proposes cleaning worktrees, caches, scratch directories or old clones.

## How to use

1. Copy this folder into `~/.claude/skills/` (personal) or `.claude/skills/` inside a project, then ask Claude Code to use `disk-space-reclaim-gates` by name.
2. Ask it to start read-only: baseline, snapshot and swap check, then a candidate list with owner and liveness evidence before any deletion.

Example prompts:
- "Use disk-space-reclaim-gates: my disk is 96% full and I deleted 10 GB with no change in df. Find out why."
- "Use disk-space-reclaim-gates to classify the worktrees under ~/work and tell me which are provably safe to reclaim."
