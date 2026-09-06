---
name: workspace-lease
description: A file-leasing protocol that lets multiple concurrent AI-agent sessions — across separate git worktrees or clones of the same repository — claim exclusive write ownership of exact paths before editing, with atomic scoped commits and cross-worktree overlap detection.
---

# workspace-lease

A git worktree gives you isolation, not ownership. Two agent sessions in two separate worktrees (or two separate clones) of the same origin can still both edit the same logical file — filesystem isolation says nothing about who's allowed to touch what, and a naive "just work in separate worktrees" setup lets two sessions silently clobber each other's changes to the same path.

## The method

Key every lease by the pair `(normalized repo origin, repo-relative path)`, not by worktree or clone location. That's the piece that makes leases work across isolation boundaries: the same logical file claimed from two different clones is still one lease.

**1. Claim before writing.** Before an agent session edits a file, it claims the smallest exact set of paths it needs — prefer exact file paths over whole-directory claims; only claim a directory tree when a shell command might touch paths you can't enumerate up front. A claim is atomic: either it succeeds and no other live session holds an overlapping path, or it's refused.

**2. No force, no steal.** If a claim is refused because another session holds it, the calling session stays read-only, narrows its manifest, or waits — there is deliberately no override. A lease you can force past isn't a lease, it's a suggestion.

**3. Heartbeat and expire.** Sessions renew their claims periodically; a session that goes silent (crashed, was killed, network dropped) has its leases expire automatically after a timeout so a stale lock can't permanently block other work. Expired leases are pruned on next use, not on a separate cleanup pass.

**4. Guard the commit, not just the edit.** Claiming a file before editing it doesn't stop a later broad `git commit -a` from sweeping in unrelated dirty paths outside your lease. Before committing, bind the exact staged-file manifest to your active leases and current HEAD, and reject the commit if the staged set doesn't match what you declared. For the write itself, build the commit off-ref first (so a concurrent branch move can't redirect it to the wrong lineage), then compare-and-swap the target branch ref to point at it.

**5. Check for overlap before integrating.** Right before a merge, cherry-pick, or handoff, run a cross-worktree dirty-path scan across every known worktree/clone of the origin — including both sides of a rename — and refuse the integration if the same logical path is dirty in more than one place at once, even if leases were technically respected along the way. A clean lease registry is concurrency evidence, not a substitute for this final check.

**6. Read-only work doesn't claim.** Scouts, reviewers, and any session that's only reading never need to take a lease — leases exist to serialize writes, not reads.

## Reference implementation sketch

A minimal version is a single JSON registry file, protected by an OS-level file lock and written via atomic replace, living outside any individual repo checkout:

```
{
  "leases": [
    {"origin": "git@host:org/repo.git", "path": "src/parser.py",
     "session": "agent-session-id", "claimed_at": "...", "expires_at": "..."}
  ]
}
```

- `claim(origin, path_or_tree, session_id)` — atomic acquire; refuse on overlap with a live lease.
- `heartbeat(session_id)` — renew all of a session's active leases.
- `release(session_id)` / `release(session_id, path)` — end ownership.
- `check(origin, paths)` — verify a session's claims cover a manifest, without touching anything.
- `guard_diff(repo)` — scan every known worktree/clone of the same origin for the same dirty logical path in more than one place.

Path comparisons should be case-folded (so a case-insensitive filesystem can't create two "different" paths for the same file) and normalize renames so both the old and new path are covered.

## When to use

- Any time more than one AI-agent session (same tool or different tools) might write to worktrees or clones of the same repository at once.
- Before creating a new isolated worktree for a session, and before resuming a session that was paused — a resumed session should re-claim, never assume its old leases are still valid.
- Before any commit, merge, cherry-pick, or handoff between sessions.

## How to use

**Install:** copy this folder into `~/.claude/skills/workspace-lease/` for personal use, or `.claude/skills/workspace-lease/` inside a project repo shared across multiple agent tools or sessions. Build the reference registry (or adapt an existing lock-file library) for your environment.

**Invoke:**

```
Before you start editing, claim a workspace-lease on the files you're about
to touch, and don't commit anything outside that claim.
```

```
Two sessions are working in separate worktrees of this repo right now — run
workspace-lease's overlap guard before either one merges.
```
