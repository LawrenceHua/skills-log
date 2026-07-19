---
name: git-identity-guard
description: Pre-push check that verifies the active git author email, authenticated gh CLI account, and target remote all match what you declared for this repo, and refuses to push on any mismatch or missing declaration.
---

# git-identity-guard

If you switch between a work GitHub account and a personal one (or juggle several client accounts on the same machine), it's easy to commit or push under the wrong identity — wrong `user.email`, wrong `gh auth` session, or a push aimed at a personal fork instead of the canonical upstream. The fix isn't remembering harder, it's checking automatically and refusing to proceed when the check can't confirm you're right.

## Method

1. **Declare intent once per repo.** Add a small, uncommitted (or team-shared) file at the repo root, e.g. `.git-identity`:
   ```
   email = you@your-work-domain.com
   gh_user = your-work-username
   push_remote = upstream
   push_remote_url_contains = github.com/your-org/canonical-repo
   ```
   No file present = intent is undetermined, which is itself a failure condition (step 4), not a pass-through.

2. **Read current state, in this order:**
   - `git config user.email` (repo-local config; only fall back to global if no local value is set — a silent fallback is itself worth flagging)
   - `gh auth status` — which account is currently authenticated
   - `git remote get-url <remote>` for the remote the push actually targets (not just whichever remote happens to be default)

3. **Compare** each found value against the declared value. All three must match exactly (or the URL must contain the declared substring).

4. **Fail closed.** If everything matches, proceed silently — no output, no delay. If anything mismatches, or `.git-identity` is missing/unparseable, block the push and print a report:
   ```
   git-identity-guard: MISMATCH — refusing to push

     field          expected                                          found
     -------------- ------------------------------------------------- -------------------------------------------------
     user.email     you@your-work-domain.com                          you@your-personal-domain.com
     gh account     your-work-username                                your-personal-username
     remote(push)   upstream -> github.com/your-org/canonical-repo    origin -> github.com/your-personal-username/repo-fork.git

   Fix one of:
     git config user.email "you@your-work-domain.com"
     gh auth switch --user your-work-username
     git push upstream HEAD:main   # instead of origin
   ```
   Never auto-correct or auto-push on the user's behalf — surface the diff, name the exact fix command, and let a human confirm it.

5. **Optional: wire it as a hook.** Drop the check into `.git/hooks/pre-push` (exit non-zero on mismatch) so it runs automatically instead of needing to be invoked by hand before every push.

## When to use

- Before pushing from a machine where you regularly switch between a work and a personal GitHub account
- In any repo that has both an `origin` fork and an `upstream` canonical remote, where pushing to the wrong one is easy
- Onboarding a new client or org repo, to lock in "this repo is always identity X, remote Y" from day one
- After you've noticed a stray commit under the wrong author email and want to stop it from recurring
- Setting up a fresh clone or a new machine profile, before the first push from it

## How to use

**Install:** copy this folder into `~/.claude/skills/git-identity-guard/` for personal use, or `.claude/skills/git-identity-guard/` inside a project repo.

**Invoke:**
```
Check my git identity before I push this branch — am I set up as the right account for this repo?
```
```
Set up a git-identity-guard for this repo: I should always push as my-work-username to upstream, never origin.
```
