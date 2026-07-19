---
name: cross-repo-work-recap
description: Pull a structured, evidence-backed recap (shipped / in-flight / at-risk) of work across multiple local git repos over a time window, cross-referenced with personal notes.
---

# cross-repo-work-recap

When you work across several repos at once, "what did you actually get done this week" turns into a memory-reconstruction exercise every time someone asks. Git history already has the real answer — the fix is pulling it the same way every time, and refusing to call anything "done" without a commit hash, branch name, or file reference backing the claim.

## Method

1. **Enumerate repos.** Maintain a fixed list (a text file of local repo paths) rather than re-discovering it from scratch each time. A directory scan (e.g. `find ~/code -maxdepth 2 -name .git`) is a reasonable fallback for repos not yet on the list, but a scan alone misses repos outside the search root and silently drifts when repos move — treat the list as the source of truth and the scan as a supplement.
2. **Fix the window once.** Default to the last 7 days; accept an override ("past N days", "since \<date\>"). Compute the window bound a single time (e.g. `since=$(date -v-7d +%Y-%m-%d)`) and reuse it for every repo, so the recap compares the same period across projects instead of drifting per-repo.
3. **Pull per-repo evidence.** For each repo:
   - `git log --since=<window> --oneline --all` — commits landed, across every branch, not just the current checkout.
   - `git branch -vv` or `git for-each-ref --sort=-committerdate` — what merged, what's still open, what hasn't moved since before the window (stale).
   - `git log --since=<window> --stat` (or `--name-only`) — which paths/directories churned most.
   - Grep commit messages for unfinished-work markers (`TODO`, `WIP`, `fixup!`) — candidates for AT RISK, not proof of anything by themselves.
   - If the repo hosts PRs, pull open-PR state (e.g. `gh pr list`). An open PR with no commits in the window is going-stale IN-FLIGHT, not shipped.
4. **Cross-reference personal notes.** If a running journal or notes file exists, scan entries dated inside the window. Use it only to add context — why a branch stalled, what an incident was, what the original goal was — never as the source of a SHIPPED claim. Notes describe intent; git describes what happened.
5. **Bucket the output — never narrate, always cite.** Every line needs a concrete reference (commit hash, branch name, PR link, or file path) or it does not belong in SHIPPED or IN-FLIGHT. If you can't point to it, it goes in AT RISK with a note on what's missing.

Example shape:

```
## repo-a
SHIPPED
- Rate-limit middleware landed (a1b2c3d..e4f5g6h, 6 commits, merged to main)
- Startup config validation (f0e1d2c)

IN-FLIGHT
- feature/retry-backoff — 3 commits since <date>, PR #142 open, no review yet
- Auth token refresh — last commit 2 days ago, branch active

AT RISK / UNFINISHED
- fix/cache-invalidation — no commits in 9 days, branch exists, no PR
- Commit e5f6a7b: "TODO handle 429s" — not addressed since

## repo-b
SHIPPED
- (none this window — last commit was 11 days ago)
```

## When to use

- Someone asks "what did you ship this week" and you're about to answer from memory.
- Weekly or biweekly status update, standup, or self-review spanning more than one repo.
- You suspect a branch or feature has gone stale and want dates to confirm it, not gut feel.
- Before writing "done" in a report, PR description, or handoff doc — get the reference first.

## How to use

**Install:** copy this folder into `~/.claude/skills/cross-repo-work-recap/` for personal use, or `.claude/skills/cross-repo-work-recap/` inside a project repo.

**Invoke:**

```
Give me a cross-repo work recap for the last 7 days — pull git log across
all my repos and bucket it into shipped, in-flight, and at-risk with evidence.
```

```
What actually landed across my repos in the past 2 weeks? Cross-reference
my notes file for context but back every "shipped" claim with a commit or PR.
```
