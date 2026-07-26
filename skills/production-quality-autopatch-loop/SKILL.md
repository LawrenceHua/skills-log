---
name: production-quality-autopatch-loop
description: Continuously score live production conversation/interaction transcripts against a quality rubric, auto-draft a minimal prompt-only fix as a pull request, and auto-merge it only once it clears a strict multi-reviewer safety gate.
---

# production-quality-autopatch-loop

Most prompt-quality work happens reactively: a user complains, someone reads the transcript, someone edits the prompt by hand, someone deploys. This closes that loop automatically — real production interactions get scored the moment they end, a minimal prompt fix gets drafted and opened as a PR, and it only ever merges itself if an independent, unanimous, scope-limited review says it's safe to.

This is a different shape than a synthetic-dialog quality loop (score canned scenarios, human approves each edit): here the signal is real production traffic, and the safety comes from the merge gate being strict enough that auto-merge is trustworthy rather than from a human reviewing every diff.

## The blueprint

```
              Transcript                              Open PR
              emitted           ┌────────────┐      (via CLI)
Product ─────────────────────────►│  scorer +  │──────────────►  Git host
(call/SMS/                        │  proposer  │
 chat/etc)                        └─────┬──────┘
                                        │
                              hard $  │  LLM-judge scoring
                              budget  │  against your rubric
                              cap     ▼
                              ┌────────────────┐
                              │ score_call()   │  weighted rubric +
                              │ propose_fix()  │  hard-rule compliance
                              └────────┬───────┘
                                       │
                              ┌────────▼────────┐
                              │  merge gate     │  unanimous multi-model
                              │ (scheduled job) │  review + prompt-only +
                              └────────┬────────┘  diff-size cap
                                       │
                              ┌────────▼────────┐
                              │ publish KPIs    │  before/after quality
                              │ (scheduled job) │  numbers, wherever you
                              └────────┬────────┘  track dashboards
                                       │
                              ┌────────▼────────┐
                              │ Quality panel   │
                              │ (optional)      │
                              └─────────────────┘
```

## Implementation steps

### 1. Identify your product's transcript shape

Every product logs interactions differently — a call has turn-by-turn role-tagged events, an SMS thread has a message log plus whatever reasoning trace you keep, a chat product has its own event stream. Whatever the shape, the transcript must include: who said what, what the AI's final outcome/summary was, and what actually happened for the user (success, abandonment, error).

### 2. Locate or write a lightweight spec to score against

The scorer needs a "what this should do" reference. If you don't have one, the minimum useful version is: a one-line description of what the product does, 3-7 hard rules the AI must never violate, and a definition of what a successful interaction looks like. Five minutes to write, and nothing downstream works without it.

### 3. Define a 5-6 dimension rubric

A rubric that travels well across most conversational/interactive products:

| Dimension | What it measures |
|---|---|
| Hard-rule compliance | did any non-negotiable rule get violated? (weight this 2x — it's correctness, not polish) |
| Warmth / naturalness | sounds human, not templated or robotic |
| Specificity | references the actual context, not generic filler |
| Personality / distinctiveness | closes with something specific to this interaction, not boilerplate |
| Conciseness | no filler turns, no announce-then-ask patterns |
| Turn-taking or responsiveness | for voice: didn't talk over or repeat itself; for text/SMS: replied promptly and recovered gracefully from unclear input |

### 4. Wire the trigger

Two options, and they're not mutually exclusive:

- **Per-interaction (preferred):** fire the scorer the moment an interaction ends, from a detached subprocess so it can never block or slow down the live request path.
- **Scheduled batch (fallback):** on a fixed interval, scan the last window of transcripts, score the worst few, and propose a fix for the single worst one. Use this when there's no clean hook point in the product code yet.

### 5. Set a hard budget cap

The scorer calls an LLM judge per interaction — that's real, ongoing cost. Enforce a hard per-session dollar cap with a halt threshold below it (e.g., a $10 cap that halts new scoring at $9 spent) and a fixed reset window (daily is reasonable). Track cost by provider so adding a new scoring model doesn't silently blow the cap.

### 6. Wire the auto-PR opener

Requires: an authenticated git-host CLI, CI enabled on the repo, provider API keys for whatever judge model(s) you use configured as repo secrets, and a review workflow file that runs on every PR from this pipeline.

### 7. Wire the merge gate — every one of these must hold, no exceptions

1. The branch name matches a dedicated prefix convention (e.g. `auto-quality/*`) so it's unambiguous which PRs this pipeline opened.
2. The diff touches **only** prompt/config files — never application code.
3. The diff is under a hard line-count cap (small enough that "unanimous review approved it" is a meaningful signal, not a rubber stamp).
4. An automated multi-model review ran and every reviewer approved — any reviewer erroring or being skipped blocks the merge, it does not default to pass.
5. No failing or cancelled status checks.
6. A secret/brand-token sweep passes clean before merge.

On merge: reload or restart whatever service reads that prompt file, so the fix actually takes effect instead of sitting deployed-but-inert.

### 8. Publish KPIs

Push a small set of before/after numbers somewhere you'll actually look at them — a dashboard, a status channel, even a markdown file that gets checked weekly. The loop is only as good as your ability to notice when it stops working.

## KPIs to track

| KPI | What it shows | Healthy direction |
|---|---|---|
| Mean composite score across interactions | Overall quality | trending up |
| % of interactions above your "good" threshold | Hit rate | trending up |
| Regressions caught by replaying known-bad transcripts | Bug-catch rate | low and stable, not climbing |
| Auto-PRs opened | Improvement velocity | tracks interaction volume |
| Auto-PRs merged | Pipeline health | high — low merge rate usually means the review gate, not the proposer, is the bottleneck |
| Mean cost per improvement | Cost efficiency | low, well under your budget cap |
| Time from interaction-end to PR-open | Loop latency | under a minute or two |

## Failure modes + recovery

| Failure | Symptom | Fix |
|---|---|---|
| Idempotency breaks | Same interaction produces multiple PRs | Your "already-scored" state got wiped — restore it from the proposal log rather than re-deriving it |
| Budget cap never resets | Scoring halts and stays halted | Confirm the reset job actually ran; manually clear the budget state file if needed |
| Review workflow never fires | PRs sit open forever, nothing merges | Check CI is enabled at the account/repo level — a billing or permissions change silently disables this |
| Auto-merger merges a bad fix | A recent merge visibly regressed quality | Revert the specific PR immediately; the service should auto-restart on the revert merging too |
| Scorer rates everything perfectly | Rubric too loose to be useful | Tighten the threshold or strengthen the weakest rubric dimension |
| Scorer rates everything poorly | Rubric too harsh, drowns real signal in noise | Loosen the threshold or rebalance dimension weights |

## Adaptation checklist for a new product

- [ ] Identify the transcript source (file, DB query, log stream)
- [ ] Confirm a lightweight spec/PRD exists; write one if not (5 minutes)
- [ ] Adapt the rubric dimensions to the interaction type
- [ ] Point the pipeline at the right repo and prompt-file paths
- [ ] Confirm CI is enabled and provider secrets are set
- [ ] Add the per-interaction hook (detached, non-blocking)
- [ ] Add the scheduled fallback + merge-gate job
- [ ] Wire KPI publishing somewhere you'll actually see it
- [ ] Baseline: score 5+ historical interactions before trusting new scores
- [ ] Verify the merge gate actually blocks by opening one intentionally-flawed mock PR

## When to use

- A conversational or text-generating product just shipped its first real user-facing interactions and you want quality regressions caught automatically instead of by complaint.
- An existing product's quality is regressing and you want a standing guard against it, not a one-time audit.
- You have a specific bug report you can replay from a transcript and want the fix pipeline to prove it addressed the actual weakness, not just the reported symptom.

Skip this if: there's no spec to score against, there are no transcripts yet to generate signal, prompts aren't cleanly separated from code (so there's no clean diff target), or your budget for judge-model calls is near zero.

## How to use

**Install:** copy this folder into `~/.claude/skills/production-quality-autopatch-loop/` for personal use, or `.claude/skills/production-quality-autopatch-loop/` inside a project repo, then ask your assistant to use the skill by name.

**Invoke:**

```
Use production-quality-autopatch-loop to design a self-improvement pipeline
for my customer support bot. Transcripts land in a Postgres table per
conversation; the prompt lives at prompts/support.md in this repo. Help me
define the rubric and the merge-gate rules.
```

```
Adapt production-quality-autopatch-loop for a new product — walk through the
per-product adaptation checklist with me and flag anything I'm missing before
we wire the auto-merge gate.
```
