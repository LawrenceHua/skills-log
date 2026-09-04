---
name: ci-triage
description: Triage every red CI run across your repos in one sweep by classifying each failure's root signature — "never started" (infra/billing) vs. "step failed" (a real code/gate problem) — so a rerun is only ever attempted on the classes it can actually fix.
---

# ci-triage

CI failures come in two fundamentally different shapes, and conflating them wastes days: a job that **never started** (no runner assigned, zero steps ran, no logs at all) versus a job that **ran and a step inside it failed**. The first is infrastructure — billing, an offline runner, a scheduling mismatch — and no rerun, no code fix, and no amount of staring at "flaky tests" will clear it. The second is CI doing its job correctly. Because a never-started job produces no logs, it visually looks identical to "the tests are flaky" — which is exactly how an infrastructure outage hides for days behind a code-quality story.

This skill is a repeatable sweep: pull every non-green run across your repos for a time window, classify each one by signature, and only recommend a rerun for the classes where a rerun is actually the correct response.

## The sweep

```bash
# for each repo you track:
gh run list -R <owner>/<repo> --status failure --limit 50 --json databaseId,conclusion,workflowName,headBranch,createdAt

# then for each failed run, pull the real cause:
gh run view <run-id> -R <owner>/<repo> --log-failed
```

Keep a small registry file (repo names, one per line, or `owner/repo` pairs) so the sweep covers your whole estate in one pass instead of repo-by-repo guessing. If a branch is *expected* to be red until some blocking PR merges, keep a short, actively-pruned list of those exceptions — a stale exception here is exactly how a real regression hides.

## Classification table

| Class | Signature | Rerun fixes it? | What it actually means |
|---|---|---|---|
| **Billing / never-started** | "payment failed" / "spending limit" / "cannot be run" | No | A hosted-runner job never started at all. Raise the limit or provision a self-hosted runner — but check whether the job carries deploy credentials before moving it to a persistent runner that also executes untrusted PR code. |
| **Never-started (other)** | no runner assigned, zero steps, no log | No | Missing/offline runner or an unmatched job-label. Check your runner registration before anything else. |
| **Slot/concurrency timeout** | "wait exhausted" / a specific queue-timeout exit code | **Yes** | Local concurrency back-pressure, not a code problem. If it recurs, raise the concurrency cap — back-pressure should never present as a test failure. |
| **Tool-cache miss** | "not found in local cache" / permission errors under a runner tool-cache path | Yes, after the runner's environment is fixed | A setup step missed its tool cache and fell back to a path that doesn't exist on this runner. Fix the runner's environment and pre-populate the cache before rerunning. |
| **Missing/shallow ref** | "couldn't find remote ref" / "unknown revision" / a diff step failing on `HEAD^` | No | A base/diff ref that no longer exists, or a shallow checkout missing history it needs. Deepening the checkout (`fetch-depth: 0`) fixes the shallow case; a genuinely missing ref needs a workflow fix, not a rerun. |
| **Type/compile error** | `error TS…` or your language's compile-error format | No | A real type error — often introduced by a *data* change, not a code change (an emptied array literal can infer as an impossible type). |
| **External 5xx** | "failed with status 5xx" from a third-party call | Maybe | Someone else's outage. Consider making that step alert-and-continue rather than hard-failing the whole run. |
| **Dependency error** | `ModuleNotFoundError` / `Cannot find module` | No | A genuinely missing dependency, or a wrong working directory / module path. |
| **Test failure** | `FAILED ...` / "N failed, M passed" | No | The gate working as intended. Check for time-decay (see below) before assuming it's a real regression. |
| **Gate refusal** | a custom repo gate exits non-zero with an explanatory message | No | The message *is* the instruction. Never "fix" this by loosening the gate. |
| **Lint/policy** | linter or policy-check failure | No | Fix the file; don't weaken the check to make it pass. |
| **Cancelled** | run cancelled | Yes (usually moot) | Almost always superseded by a newer push. Benign. |

## Recurring traps worth knowing before you triage

- **A billing wall looks exactly like flakiness.** A hosted-runner job that dies in a few seconds with no runner, no steps, and no logs is not a flaky test — it never got a chance to run at all.
- **When your hosting/deploy provider's own build step re-runs your test suite, a red check and a failed deploy on the same commit are one defect, not two.** Triage the underlying cause once.
- **A test asserting on a rolling date/time window decays into red purely from the clock advancing**, with no related code change. Tell: every branch fails at once, out of nowhere. Pin the window.
- **A workflow file can be valid YAML and invalid CI config at the same time** — some CI providers discard the whole file silently, reporting "zero jobs" rather than an error. Lint the workflow file itself after any edit, not just the code it runs.
- **A queue-wait timeout as long as the job's own timeout starves the job it was meant to protect.** Keep wait budgets well under the job timeout.
- **Local green predicts nothing about a gate that only exists inside the CI workflow itself.** Read the actual failing step's log, not just the job name — a job that passes locally can still fail a PR if the CI-only gate isn't reproduced locally.

## Verification standard

"Green" means the CI provider's own run conclusion — never a local test pass standing in for it.

```bash
gh run view <id> -R <owner>/<repo> --json conclusion,status
```

For a deployment specifically, confirm the deployment's own state *and* separately probe the live URL (`curl -sI https://<host>` → expect 200) — a "successful" deploy record with a broken live URL is still broken.

For every class you claim to have fixed, record: the failing run id → the fix commit → the green rerun id. Anything short of that chain is an unverified claim, not a fix.

## Working rules once you act on a finding

- Fix in a fresh clone or branch — never in a checkout something else (a bot, a scheduled job) is actively using; touching it corrupts its evidence.
- Branch and open a PR for every change; run the repo's own local gate first, and lint any workflow file you touched.
- A red run on someone else's in-flight branch isn't automatically yours to fix — report the mechanism, don't edit their work.
- Never widen a gate into passing vacuously just to clear a red. A gate that silently passes when it can't determine its input is worse than the red it replaced.

## When to use

- CI is failing across more than one repo and you want to know if it's one root cause wearing many disguises before you fix anything.
- Failure-notification emails are piling up and you want to stop the noise at the source, not per-repo.
- Before diagnosing any single red run — to make sure a one-off isn't actually part of an estate-wide class (a billing block or a runner regression can redden a dozen repos at once and look like a dozen unrelated bugs).

## How to use

**Install:** copy this folder into `~/.claude/skills/ci-triage/` for personal use, or `.claude/skills/ci-triage/` inside a project repo.

**Invoke:**

```
Run a ci-triage sweep over the last 3 days across my repos, classify every
red run by signature, and tell me which ones a rerun will actually fix.
```

```
This deploy failed and the Actions run on the same commit is also red —
use ci-triage to figure out if that's one defect or two, and which class
it falls into before I touch anything.
```
