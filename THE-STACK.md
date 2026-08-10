# The Stack — two years of AI-agent tooling, distilled

I've been building with AI tools daily since 2024: IDE assistants first (Cursor),
then a home-grown multi-agent orchestration platform (OpenClaw), then CLI agents
(Claude Code on a Max subscription), then a second execution CLI (Codex), a
long-context CLI (Kimi), and finally a self-hosted local agent runner (PairChat).
Along the way I accumulated ~300 scheduled jobs, 100+ skills, and a lot of scar
tissue.

This document is the distillation: **the agents that should be running, the
skills worth having, and the architecture that emerged** — generalized so you can
adopt it with whatever tools you use. Every referenced skill lives in this repo's
[`skills/`](skills/) directory; every agent definition lives in [`agents/`](agents/).

---

## The journey (what each era taught)

| Era | Tooling | The lesson that survived |
|---|---|---|
| IDE assist | Cursor, autocomplete-style agents | Speed without verification just produces wrong code faster. The bottleneck moved from *writing* code to *checking* it. |
| First orchestration | A self-built multi-agent platform (100+ agents, Slack-triggered, launchd-scheduled) running automated QA/bug-fix pipelines | Agents will confidently report success on work that failed. Every pipeline needs **proof-gated stages**, not vibes-gated ones — and a watchdog layer, because unattended systems rot silently. |
| CLI agent | Claude Code + skills, subagents, hooks, persistent memory | The unit of leverage is not the prompt — it's the **reusable skill** and the **fresh-context verifier**. Codify a workflow once, invoke it forever. |
| Multi-CLI | A second CLI on a flat-rate subscription for heavy execution, a third for 1M-context judging, a local runner for cheap/free work | Route by **capability and cost tier**, not tool loyalty. The strongest model plans and verifies; a cheaper capable model executes; a third model judges in a fresh context. |

Three ideas kept re-earning their place across every era:

1. **Never trust a "done" claim without reproduced evidence** — not from a model,
   not from yourself.
2. **Fresh context beats shared context for verification** — the agent that did
   the work must never be the agent that grades it.
3. **Everything unattended needs a watcher, and the watchers need a watcher.**

---

## Part 1 — The discipline layer (adopt this before any tooling)

None of the orchestration matters without this. These are conventions, not
software — they cost nothing to adopt.

**Verification labels.** Every status claim gets exactly one of four labels:
`VERIFIED` (you reproduced the evidence with a command you can quote),
`CODE-SHIPPED-NOT-VERIFIED` (the change exists but nothing proved it works),
`BLOCKED`, or `INCONCLUSIVE`. The moment "done" is allowed to mean anything
weaker than VERIFIED, agent output becomes unusable.
→ [`skills/verification-labels`](skills/verification-labels/SKILL.md)

**Proof mapped to claim type.** "Tests pass" requires a test run this session.
"Deployed" requires a probe against the live URL. "Fixed" requires reproducing
the original failure and watching it not happen.
→ [`skills/quality-gate-registry`](skills/quality-gate-registry/SKILL.md)

**Fail-closed guards.** Any gate, permission check, or precondition whose
missing-data fallback *allows* the action is a gate that doesn't exist.
→ [`skills/fail-closed-guards`](skills/fail-closed-guards/SKILL.md)

**Compaction contract.** Long agentic sessions get summarized (auto or manual).
Force the summary into a fixed template that quotes exact strings — paths,
errors, flags — because paraphrase is where context dies.
→ [`skills/compaction-contract`](skills/compaction-contract/SKILL.md)

**Prompt-engineering scar tissue.** Never spell out a forbidden phrase verbatim
in a ✗-example (models pattern-match into it); check generated marketing copy
for AI tells before shipping it.
→ [`skills/negative-prompt-leakage`](skills/negative-prompt-leakage/SKILL.md),
[`skills/ai-tells-check`](skills/ai-tells-check/SKILL.md)

---

## Part 2 — Skills you should definitely have

The full catalog is in the [README](README.md); this is the shortlist I'd
install on a fresh machine, in order.

**Core discipline (day one):**
1. [`verification-labels`](skills/verification-labels/SKILL.md) — the four-label done-claim vocabulary
2. [`quality-gate-registry`](skills/quality-gate-registry/SKILL.md) — which proof each claim type requires
3. [`fail-closed-guards`](skills/fail-closed-guards/SKILL.md) — guards that refuse on missing data
4. [`roast-me`](skills/roast-me/SKILL.md) — adversarial questioning before you build

**Planning & building (week one):**
5. [`adversarial-planning`](skills/adversarial-planning/SKILL.md) — research swarm → design → mandatory attack pass → evidence-gated plan
6. [`expert-fanout`](skills/expert-fanout/SKILL.md) — N independent domain experts in parallel, then synthesis
7. [`staff-code-review`](skills/staff-code-review/SKILL.md) — multi-agent review panel with adversarial verification
8. [`production-gauntlet`](skills/production-gauntlet/SKILL.md) — looped KPI gate before anything is called done

**Multi-agent & multi-model (when one tool stops being enough):**
9. [`model-lane-routing`](skills/model-lane-routing/SKILL.md) — plan on the strongest model, execute on the cheapest capable one, judge on a third
10. [`fanout-cost-pinning`](skills/fanout-cost-pinning/SKILL.md) — pin every subagent's model; they silently inherit your expensive main model otherwise
11. [`offload`](skills/offload/SKILL.md) — route self-contained work to flat-rate or local backends
12. [`multi-cli-constitution`](skills/multi-cli-constitution/SKILL.md) — one shared rules file every CLI points at
13. [`evidence-gated-delegation`](skills/evidence-gated-delegation/SKILL.md) — delegates earn autonomy through verified track record

**Ops & memory (when you run things unattended):**
14. [`background-agent-roster`](skills/background-agent-roster/SKILL.md) — the standing background jobs (below) as install recipes
15. [`agent-memory-sync`](skills/agent-memory-sync/SKILL.md) — git-backed persistent memory that survives sessions and machines
16. [`environment-drift-hunter`](skills/environment-drift-hunter/SKILL.md) — scheduled deterministic drift/secret/zombie scanning
17. [`skill-estate-guardian`](skills/skill-estate-guardian/SKILL.md) — lint your own AI tooling for rot
18. [`git-identity-guard`](skills/git-identity-guard/SKILL.md) — never push with the wrong identity again

---

## Part 3 — Agents that should always be running

Distilled from ~300 scheduled jobs down to the twelve patterns that earn their
slot anywhere. Concrete install recipes (launchd/cron/systemd) are in
[`skills/background-agent-roster`](skills/background-agent-roster/SKILL.md).

| # | Agent | Cadence | Why it earns the slot |
|---|---|---|---|
| 1 | **Estate meta-monitor** | 30 min | Checks that every *other* automation ran recently and its receipts are fresh. Monitors go silently stale; this is the job that catches that. |
| 2 | **Deterministic health scanner** | 2 h | No-LLM sweep for stale state, config/security drift, orphan jobs, zombie processes. Cheap checks catch the boring failures. |
| 3 | **Fleet watchdog (strike rule)** | 1–5 min | Probes critical local services; restarts/alerts only after N consecutive failures, so one blip doesn't cause restart-flapping. |
| 4 | **Zombie reaper** | 10 min | Kills orphaned agent subprocesses that outlived their session — with an explicit never-touch list for parent services. |
| 5 | **Self-healer** | 10 min | Auto-restarts crashed services, clears stale locks, prunes logs. The "don't page a human for transient issues" layer. |
| 6 | **Session→skill miner** | weekly | Mines the week's agent transcripts for repeated workflow patterns and drafts skill candidates — human-approved, never auto-promoted. |
| 7 | **Morning brief** | daily | Synthesizes overnight job results, failures, and deltas into one digest so the day starts with state, not archaeology. |
| 8 | **Memory sync** | 5–15 min | Commits/pulls the agent memory store through git so context survives sessions and machines. |
| 9 | **CLI hygiene** | nightly | Compacts old sessions, repairs corrupted session files, watches for CLI-update regressions. Long-lived agent CLIs degrade silently without it. |
| 10 | **Cost/token monitor** | daily | One rollup of yesterday's AI spend. Dozens of scheduled agents will surprise you on the bill exactly once. |
| 11 | **Notification doctor** | 30 min | Inventories alert sources, dedupes noise, auto-fixes only whitelisted idempotent issues. Owns alert fatigue instead of ignoring it. |
| 12 | **Keep-awake** | always | Trivial (`caffeinate` / OS equivalent) but load-bearing: every job above dies if the host sleeps mid-run. |

Two rules govern the whole roster:

- **Every job leaves a receipt** (a timestamped file or log line) — that's what
  the meta-monitor checks. A job with no receipt is indistinguishable from a job
  that never ran.
- **Auto-fix only what's idempotent and whitelisted.** Everything else surfaces
  as a finding for a human. (And the repair layer must never be able to kill the
  agent that's doing the repairing.)

---

## Part 4 — The verifier bench (drop-in agent definitions)

Five single-purpose, read-only subagent personas, in [`agents/`](agents/).
The design rules matter more than the personas:

- **Fresh context, always.** The verifier never shares context with the work it
  checks — no shared history means no shared blind spots.
- **Read-only, tool-restricted.** Verifiers get no Edit/Write, and their
  prompts forbid mutating commands. (Bash-for-verification can still mutate in
  principle — for unattended runs, back the contract with hard deny rules in
  your tool's permission settings; see `agents/README.md`.) An agent that can
  edit can "fix" its way to a passing verdict.
- **Refute by default.** The claim is false until the verifier reproduces the
  evidence itself, this run, with output it can quote.
- **Pin the model per role.** Graders can be cheap and fast; adversarial
  verification is where the strong model earns its cost.

| Agent | Role |
|---|---|
| [`adversarial-verifier`](agents/adversarial-verifier.md) | Refute-by-default checker for any "done/fixed/shipped" claim |
| [`hostile-reviewer`](agents/hostile-reviewer.md) | Adversarial PR review — security, correctness, ML/data, process, perf, a11y |
| [`completeness-critic`](agents/completeness-critic.md) | End-of-run gap-finder: what was never checked at all |
| [`cheap-grader`](agents/cheap-grader.md) | Fast structured rubric scoring on the cheapest model tier |
| [`researcher`](agents/researcher.md) | Web research with source-quality ratings and falsifiable, quoted claims |

---

## Part 5 — Composing multiple CLIs and models

Once you run more than one AI CLI, three patterns keep them coherent:

**One constitution file.** A single shared rules file (routing table, verification
vocabulary, house rules) that every CLI is pointed at, plus a marker-delimited
policy block compiled *identically* into each tool's own config — so the quality
bar can't drift between tools.
→ [`skills/multi-cli-constitution`](skills/multi-cli-constitution/SKILL.md)

**Model lanes.** Strongest model plans and adversarially verifies; a cheaper
capable model executes at scale; a third (ideally different-vendor, long-context)
model judges the result in a fresh context. Re-verify pricing before any
cost-based routing decision — prices move.
→ [`skills/model-lane-routing`](skills/model-lane-routing/SKILL.md)

**Capability routing with polyfills.** Route tasks to whichever tool natively
has the needed feature (sandboxing, goal loops, huge context, cron, video), and
keep written polyfill recipes for faking any missing feature — so no single
vendor gap ever blocks work.

---

## Adopting this from zero

- **Day 1:** Adopt the verification labels and the compaction contract (they're
  just conventions). Install `roast-me`, `quality-gate-registry`,
  `fail-closed-guards`.
- **Week 1:** Install the verifier bench (`agents/`). Start ending every
  significant change with an adversarial-verifier pass. Add `adversarial-planning`
  in front of anything non-trivial.
- **Month 1:** Stand up the first four background agents (meta-monitor, health
  scanner, watchdog, memory sync) with receipts. Add the cost monitor before the
  bill surprises you.
- **Later:** Second CLI/model lane, offload routing, the full roster.

The through-line, if you keep only one sentence: **an agent's claim about its own
work is marketing; only reproduced evidence is state.**
