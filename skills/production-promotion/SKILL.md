---
name: production-promotion
description: Merge and verify an exact-SHA delivery candidate all the way into production — binding the merge commit, the deployed production SHA, and a live probe together — instead of treating a successful merge as a successful release.
---

# production-promotion

A merge is not a release. Once a pull request is merged, three more things have to line up before you can honestly call it live: the merge commit itself, what your deploy platform actually rolled out, and what's actually answering requests. This method treats "promoted to production" as a chained SHA-verification, not a single click.

## The method

**1. Admission gate — only promote what was already provably good.** Require that the exact commit you're about to merge already passed CI and a matching preview deployment at that same SHA (see a pre-merge delivery-verification method, such as binding CI+preview to one SHA before merge). Require a human's explicit authorization for *this* production promotion, in the current session — an earlier approval for a different commit or a different day doesn't count. Stop on head/base drift, changed checks, an ambiguous merge method, or missing access, rather than guessing.

**2. Merge only the declared way.** Confirm the repository's required merge method (squash, merge commit, rebase) and use only that, on only that PR. Never force-push, push the default branch directly, bypass branch protection, or bundle unrelated changes into the same merge.

**3. Read the merge SHA back — don't assume it.** After merging, fetch the merge commit SHA from the host (not from local memory of what you just did). Confirm both the admitted head SHA and its base SHA are ancestors of that merge commit, and that the default branch's tip now equals it (when your workflow expects a direct-tip merge).

**4. Confirm the deploy platform rolled out *that* SHA.** Query your deployment provider for the production environment's current deployment and require both "ready" status and an exact match between its recorded source commit and the GitHub merge SHA. A green preview, or a production deployment serving a different (often slightly stale) SHA, does not pass — deploy platforms can report "ready" for a cached or superseded build.

**5. Probe the live thing, not the platform's opinion of it.** Hit every production URL/alias with an HTTP check and exercise the critical user journey in an actual browser. Record the final URL, status, and what you actually saw. "The provider says ready" is necessary but not sufficient — you want to know what a real request gets back right now.

**6. On a failed probe, stop and preserve evidence — don't auto-remediate.** Do not automatically revert, redeploy, change aliases, or touch provider settings. A failed live check after a clean merge is itself a finding; surface it and let a human decide the recovery action, unless they've pre-authorized an exact rollback path.

**7. Report one of four states, not a yes/no.**
- **VERIFIED** — merge provenance, deployed production SHA, and live probes all match, checked fresh in this session.
- **CODE-SHIPPED-NOT-VERIFIED** — the merge happened, but production provenance or the live check is missing or failed.
- **BLOCKED** — authorization, required policy, or an external gate prevents the promotion.
- **INCONCLUSIVE** — a readback was ambiguous, stale, or timed out.

## When to use

- Promoting an already-verified pull request into production and wanting a provable answer to "is this actually live," not just "did the merge button work."
- Diagnosing a "the deploy said success but users are still seeing the old version" incident — usually a stale-cache or rollout-lag SHA mismatch this method catches directly.
- Any release process where a merge and a deploy are separate systems that can silently disagree about which commit is running.

## How to use

**Install:** copy this folder into `~/.claude/skills/production-promotion/` for personal use, or `.claude/skills/production-promotion/` inside a project repo. Point steps 3–5 at your actual source-control host API and deploy-platform API.

**Invoke:**

```
This PR is fully green with a verified preview. Promote it to production using
production-promotion — merge, then prove the live site is actually serving this
exact commit before you tell me it's done.
```

```
Users are reporting the old behavior even though the dashboard says the deploy
succeeded. Run production-promotion's SHA-chain check to find where it actually
diverged.
```
