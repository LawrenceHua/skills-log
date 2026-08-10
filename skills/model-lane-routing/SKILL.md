---
name: model-lane-routing
description: Route each role in an AI workflow to a model lane by what the role needs — the strongest model plans and adversarially verifies, a cheaper capable model executes at scale, and a third (ideally different-vendor, long-context) model judges results in fresh context — with live-pricing re-verification before any cost-based decision.
---

# model-lane-routing

Using one model for everything either overpays (the apex model formatting JSON)
or underdelivers (the budget model designing your architecture). Two years of
running multi-model pipelines converges on a small set of *lanes* — stable
role→tier assignments — that survive every model generation even as the
specific model names underneath them churn.

## The lanes

| Lane | What runs here | Tier |
|---|---|---|
| **Plan / verify** | Architecture, deep planning, security review, adversarial verification, any high-stakes or irreversible decision | Strongest model you have access to |
| **Execute** | Implementation, refactors, tests, docs — the bulk of the work | Cheapest model that reliably handles it (usually one tier down) |
| **Judge** | Grading the executed work against the plan, in a fresh context | A *different* model than the executor — ideally different vendor, ideally long-context so it can hold the whole diff + spec |
| **Mechanical** | Classification, routing, bulk edits, rubric scoring | Cheapest/fastest tier |

The apex pipeline that falls out: **strongest model plans and attacks its own
plan → capable-cheap model executes → different model judges → strongest model
signs off on the evidence.** Each hand-off crosses a fresh-context boundary, so
no model grades work it produced.

## Rules that keep it honest

- **Different judge than executor.** Same-model judging inherits the same blind
  spots. Cross-vendor judging is the cheapest diversity you can buy.
- **Subagents inherit unless pinned.** In most agent frameworks a spawned
  subagent silently runs on your main-loop model. Fan out 10 readers without
  pinning and you've paid apex prices for grep. Pin every subagent's model
  explicitly (see `fanout-cost-pinning`).
- **Verify pricing before any cost-based routing decision.** Model prices move
  — sometimes by 3× in a single generation, in either direction. A routing
  table built on remembered prices is a routing table built on fiction. Check
  the vendor's live pricing page, dated, before you commit.
- **Probe, don't assume, cheap-model competence.** Before routing a task class
  to a budget model, run one real payload through it. Budget reasoning models
  in particular can be slower *and* worse than a mid-tier non-reasoning model
  on extraction/formatting work — measure on your actual task, not the
  leaderboard.
- **Flat-rate beats metered for bulk.** If you hold a subscription CLI with a
  strong model (any vendor), heavy execution routed there is effectively free
  relative to metered API calls — a second CLI on a different vendor's
  subscription is often the highest-ROI purchase in the whole stack (see
  `offload`).
- **Escalate on effort, not just model.** Most frontier models expose a
  reasoning-effort dial. The sweet spot for daily work is one notch below max;
  reserve the top setting for the hardest verify/design calls. And beware:
  a max-effort setting that works on short prompts can silently produce *no
  output* on long briefs — test the combination you'll actually run.

## When to use

- Designing any multi-agent or multi-step pipeline.
- A monthly cost review: list what ran on the apex tier last month and demote
  everything that didn't need it.
- Whenever a new model generation ships — re-map lanes to names, keep the lanes.

**Skip it for:** single-model casual use where cost and quality are both fine.

## How to use

**Install:** copy this folder into `~/.claude/skills/model-lane-routing/`, and
put your own concrete lane→model-name mapping in your always-loaded
instructions file (it's the part that changes every generation; date it).

**Invoke:**

```
Using the model-lane-routing skill: assign lanes for this pipeline
[describe the workflow], with today's verified pricing for each candidate
model, and flag anything currently running a tier above its lane.
```
