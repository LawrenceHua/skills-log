# Skills Log

Every Sunday, 10 genuinely useful skills from my day-to-day AI-agent
workflow, generalized for anyone to use.

These aren't marketing blurbs — each `SKILL.md` is a working methodology
you can drop straight into an AI coding assistant that supports the
[Claude Code Agent Skills](https://docs.claude.com/en/docs/claude-code)
format (plain Markdown with a small YAML frontmatter header). If your tool
doesn't support skills natively, the files are still plain Markdown, so you
can paste one directly into a chat as context and ask the assistant to
follow it.

## Quick start

1. **Clone this repo:**
   ```bash
   git clone https://github.com/LawrenceHua/skills-log.git
   ```
2. **Copy the skill(s) you want** into your assistant's skills directory:
   - Personal, available in every project: `~/.claude/skills/<skill-name>/`
   - Project-scoped, shared via version control: `<your-project>/.claude/skills/<skill-name>/`
   ```bash
   cp -r skills-log/skills/expert-fanout ~/.claude/skills/
   ```
3. **Restart or refresh your session** so it picks up the new skill.
4. **Invoke it** by asking directly in natural language ("use the
   expert-fanout skill to review this"), or via a named slash command where
   your tool supports it (e.g. `/expert-fanout`).

No skill here needs private infrastructure, an API key, or a specific
company's tooling to work — every methodology is self-contained. A few
(`offload`, `production-gauntlet`) mention plugging in a secondary
backend or reviewer; any capable second tool you have works.

**Skills are plain Markdown**, so they also work as pasted context in other
tools: if your assistant doesn't have a native skills system, just paste
the relevant `SKILL.md` into the conversation and say "follow this
methodology."

## September 12: safety recovery, ship gates, and delegation hygiene

Seven practical methods: recovering from a silent safety-classifier model downgrade, a six-gate pre-push checklist for stateful services, a race-condition-proof human approval gate, verified destination routing before an external send, cross-CLI delegation hygiene, a three-direction design pipeline with mandatory hostile review, and a three-role coding pipeline where verification means independently redoing the work.

| Skill | What it does | Use it for |
|---|---|---|
| [`safeguard-fallback-reroute`](skills/safeguard-fallback-reroute/SKILL.md) | Recovers full-quality output when a safety classifier silently downgrades your session to a weaker fallback model, instead of accepting the fallback's degraded work as final | Noticing a silent model downgrade mid-session and working up a reframe/decompose/invert/escalate recovery ladder instead of retrying the same prompt |
| [`pre-push-ship-checklist-template`](skills/pre-push-ship-checklist-template/SKILL.md) | A six-gate checklist for shipping a change to any stateful service — ownership map, multi-source rule audit, structural gate, regression replay, safe restart, and one real end-to-end smoke test | Shipping a change to a long-running stateful service where a broken deploy is expensive to notice after the fact |
| [`cas-approval-gate`](skills/cas-approval-gate/SKILL.md) | An atomic compare-and-swap two-phase state machine that makes an autonomous agent's risky action provably impossible to execute without an explicit, allow-listed human's approval | Pipelines where an autonomous agent proposes code-writing, spending, or state-mutating actions, and closing race-condition gaps in an existing approval flow |
| [`verified-destination-routing-gate`](skills/verified-destination-routing-gate/SKILL.md) | Before posting or mutating a single external destination, classifies the payload into exactly one destination class and verifies it against a freshly-read allowlist — never a cached ID — refusing on any ambiguity | Any bot or automation that posts to one of several possible external destinations, where sending to the wrong one would be embarrassing or hard to undo |
| [`cross-cli-delegation-preflight`](skills/cross-cli-delegation-preflight/SKILL.md) | Operational hygiene rules for delegating work across multiple local AI CLIs or backends — a secretless probe first, a free-tier-first default, opaque aliases, and scoped idempotent grants for remote-triggered mutations | Any setup that routes tasks across more than one AI CLI or backend and needs consistent safety hygiene regardless of which one does the work |
| [`product-design-factory`](skills/product-design-factory/SKILL.md) | A design pipeline that grounds a surface in one job statement, generates exactly three comparable directions before picking one, and requires an independent hostile review before calling it done | Designing or redesigning a product surface where you want a genuine comparison between options and a real quality bar before shipping |
| [`cross-vendor-verify-pipeline`](skills/cross-vendor-verify-pipeline/SKILL.md) | A three-role coding pipeline — one model plans, a second different-vendor model executes, and a third independently redoes the build/test run itself rather than reading the executor's diff | Coding tasks important enough to want a genuine second opinion on execution quality, especially work you'll hand off and not watch step-by-step |

## September 11: plan-release gating and swarm eligibility

Two practical methods: locking plan execution to the exact hash a user actually agreed to (so an edited plan can never run under a stale sign-off), and deciding whether a task genuinely warrants a multi-agent fan-out before reaching for one.

| Skill | What it does | Use it for |
|---|---|---|
| [`hash-locked-plan-release`](skills/hash-locked-plan-release/SKILL.md) | Gates execution of any nontrivial plan behind a recorded consultation, an explicit user agreement, and a content-hash lock, so a plan can never run under an agreement given to a different version of it | Plan-then-execute agent workflows where a plan edit must always revoke a stale go-ahead, and pre-authorizing a proven low-risk revision class without loosening hard stops on destructive or scope-expanding changes |
| [`swarm-eligibility-gate`](skills/swarm-eligibility-gate/SKILL.md) | Decides whether a task actually warrants fanning out multiple parallel agents before doing it, routes eligible work across three generic roles with required-return contracts, and downgrades gracefully instead of silently duplicating work when a role is unavailable | Deciding whether a substantial task actually benefits from parallel agents before reaching for a fan-out by reflex, and choosing a safe downgrade when a swarm node times out or is unavailable |

## September 10: delivery, delegation, and interface-quality skills

Eight practical methods spanning post-merge production verification, safely delegating to and sandboxing other AI CLIs, code-graph-aware editing, a reusable delegation-brief structure, backup recoverability proof, UI quality gating, and system-prompt architecture.

| Skill | What it does | Use it for |
|---|---|---|
| [`production-promotion`](skills/production-promotion/SKILL.md) | Merges and verifies an exact-SHA delivery candidate all the way into production — binding the merge commit, the deployed production SHA, and a live probe together | Promoting an already-verified PR into production and proving the live site is actually serving that exact commit |
| [`headless-agent-launch-verification`](skills/headless-agent-launch-verification/SKILL.md) | Launches a headless/background CLI coding-agent run so it can't silently hang or lie about completing, and verifies what it actually did | Delegating substantial work to a background CLI coding agent, and debugging a run that came back suspiciously empty |
| [`sandboxed-cli-worker-controller`](skills/sandboxed-cli-worker-controller/SKILL.md) | Runs other AI coding CLIs as least-privilege, evidence-producing workers under one controller — stripped credentials/config, pinned binaries, content-free immutable receipts, safe cancellation | Getting an independent second CLI agent's review or fan-out work without handing it full local permissions or credentials |
| [`code-graph-blast-radius`](skills/code-graph-blast-radius/SKILL.md) | Queries a code-dependency-graph tool for a shared symbol's actual upstream callers before editing it, instead of relying on grep alone | Refactors, renames, or edits to shared utilities where you need to know what could break before you touch it |
| [`delegation-brief-contract`](skills/delegation-brief-contract/SKILL.md) | A fixed structure for the handoff brief when an orchestrating loop delegates work to an agent — mechanism, exclusive working path, prohibitions, gates, proof standard, stop line, report format | Writing a delegation brief that doesn't turn into rework, and verifying what a delegated agent reports back |
| [`backup-recoverability-canary`](skills/backup-recoverability-canary/SKILL.md) | Proves round-trip recoverability of an encrypted off-site backup with a synthetic canary and independent key escrow, before trusting it as grounds to delete local originals | Deleting local originals after backing them up to an encrypted remote, or periodically re-checking an existing backup's recoverability |
| [`interface-quality-gate`](skills/interface-quality-gate/SKILL.md) | A mechanical-plus-visual quality gate for any UI — AI-tells lint pass, multi-viewport screenshot checks, frontend-standards checklist | Reviewing any generated or edited web page, app screen, dashboard, or mobile layout before calling it done |
| [`agent-prompt-architecture`](skills/agent-prompt-architecture/SKILL.md) | A repeatable method for designing and auditing an agent's system prompt, rules file, tool-use guidance, and memory/compaction instructions | Improving a system prompt or rules file that isn't working, or auditing one for bloat and contradictions before adding to it |

## September 9: design and workflow skills

Three practical methods for making terminal interfaces clearer, transferring tool workflows safely, and keeping product design coherent from user journey through verification.

| Skill | What it does | Use it for |
|---|---|---|
| [`terminal-ui-quality-guardrail`](skills/terminal-ui-quality-guardrail/SKILL.md) | Reviews terminal and text-interface changes for hierarchy, readable contrast, keyboard-visible state, and useful status information | Checking a terminal theme, status line, prompt, pane layout, or text interface after a visual change |
| [`safe-cross-tool-configuration-transfer`](skills/safe-cross-tool-configuration-transfer/SKILL.md) | Transfers a useful workflow pattern between developer tools through safe inspection, native translation, and reversible verification | Adapting a rule, command, hook, skill, or integration without copying private configuration |
| [`coherent-product-design-workflow`](skills/coherent-product-design-workflow/SKILL.md) | Grounds a product change in user jobs and real states, then compiles reusable interface rules and verifies the primary journey | Designing or redesigning a product surface whose states, components, accessibility, and visual rules must remain coherent |

## This week's 10 skills (2026-W37)

| Skill | What it does | Use it for |
|---|---|---|
| [`agent-history-recall`](skills/agent-history-recall/SKILL.md) | Builds a queryable local catalog of every past AI-agent session, decision, and note, then answers "what did we decide about X" via hybrid search over the catalog instead of re-reading raw transcript trees or guessing from model memory | Answering "what did we decide about X" from your own project history instead of guessing or re-reading old transcripts |
| [`ai-eval-rigor-checklist`](skills/ai-eval-rigor-checklist/SKILL.md) | A checklist of ~20 evidence-grounded rules for evaluating AI models, agents, and RAG pipelines rigorously — eval design, retrieval-grounding tests, agent-trajectory grading, and precise language for deletion/unlearning claims | Reviewing an eval harness, benchmark, or RAG/agent grading setup before trusting its numbers |
| [`workspace-lease`](skills/workspace-lease/SKILL.md) | A file-leasing protocol that lets multiple concurrent AI-agent sessions — across separate git worktrees or clones of the same repository — claim exclusive write ownership of exact paths before editing, with atomic scoped commits and cross-worktree overlap detection | Running multiple AI-agent sessions against worktrees or clones of the same repo without them clobbering each other's edits |
| [`graph-engineering`](skills/graph-engineering/SKILL.md) | Designs multi-agent work as a real directed graph instead of a chain — bounded nodes with explicit input/output contracts, edges only for genuine data dependencies, a fan-out/reduce/synthesize pattern, and isolated verifiers that never share context with the work they're checking | Designing or auditing a multi-agent fan-out pipeline for hidden fake edges and shared-context verifiers |
| [`cloud-delivery`](skills/cloud-delivery/SKILL.md) | Treats "delivered" as an exact-commit-SHA state machine — binds a pushed branch to a verified CI pass and a matching preview deployment at that same SHA, and refuses to call anything shipped from a stale, mismatched, or inferred signal | Proving a pushed branch is actually good — CI and preview both verified at the exact same commit SHA — before calling it shipped |
| [`scoping-cutting`](skills/scoping-cutting/SKILL.md) | An MVP-scoping framework combining Shape Up appetite-setting, "cut the list in half twice," an end-to-end "scooter not axle" value test, Wizard-of-Oz testing before automating, and an upfront kill-on-time commitment | Defining MVP scope or fighting scope creep on a feature that keeps growing |
| [`changelog-generator`](skills/changelog-generator/SKILL.md) | Generates consistent, auditable release notes directly from Conventional Commits — auto-detects the correct MAJOR/MINOR/PATCH semver bump, renders a Keep a Changelog-style document, and pairs with a CI commit-format linter and a mandatory human-approval gate | Auto-drafting release notes and the correct semver bump straight from Conventional Commits |
| [`api-design-reviewer`](skills/api-design-reviewer/SKILL.md) | A static REST API design review — lints naming/method/status-code/error-format conventions, diffs two spec versions to classify breaking vs. non-breaking changes, audits the versioning strategy, and produces a weighted design scorecard | Reviewing a REST API's design consistency before it ships, or diffing two spec versions for breaking changes |
| [`architecture-decision-records`](skills/architecture-decision-records/SKILL.md) | Captures architectural decisions as structured ADRs (Michael Nygard format) the moment they're made — auto-detects decision moments, extracts context/alternatives/consequences, and only ever writes a file after explicit user approval | Capturing why a significant architecture choice was made, in a structured, approved, indexed ADR |
| [`runbook-generator`](skills/runbook-generator/SKILL.md) | Generates a standardized operational runbook for a service — start/stop/health-check/maintenance/incident-response/rollback/escalation sections, each critical step paired with an expected-output verification check | Writing an operational runbook for a service whose every critical step is paired with a verification check |

## This week's 7 skills (2026-W36)

| Skill | What it does | Use it for |
|---|---|---|
| [`observable-share`](skills/observable-share/SKILL.md) | Before anything gets shared outward, requires three written answers (what's the one thing this says, what live source backs every number, what watches it and fixes it when it breaks), plus a hard word budget and a "stale must look stale" rule | Any report, dashboard, or status post with numbers in it, especially catching staleness that looks healthy |
| [`overnight-product-factory`](skills/overnight-product-factory/SKILL.md) | An unattended build-and-deploy pipeline that only ships on a hard gate — a unique canary token must round-trip through both the QA probe and the live health probe, and a failed deploy triggers an independently-verified rollback | Handing a defined product idea to an agent overnight and getting back a trustworthy SHIPPED/BUILT/STOPPED_AT_GATE report instead of an unverified "done" claim |
| [`second-machine-offload`](skills/second-machine-offload/SKILL.md) | Turns a second machine you own into a safe batch worker for CPU-bound jobs — a health check, a secrets-excluding file sync, and a single round-trip command with a verifiable receipt | Offloading compiles, transcodes, test sweeps, or bulk data jobs off your primary machine without ever putting its credentials on the second one |
| [`ci-triage`](skills/ci-triage/SKILL.md) | Triages every red CI run across your repos by classifying each failure's root signature — infrastructure "never started" vs. a genuine "step failed" — so a rerun is only attempted on the classes it can actually fix | Stopping a billing outage or runner regression from being misdiagnosed as a wave of unrelated flaky tests |
| [`deletion-safety-gate`](skills/deletion-safety-gate/SKILL.md) | Before deleting a worktree, clone, or cache, runs a fail-closed reference check across scheduled jobs, config files, running processes, and shared git object stores — SAFE only if every screen completes and finds zero references | Any bulk cleanup or "reclaim disk space" pass, so you never delete a directory a scheduled job is still executing out of |
| [`gate-erosion-audit`](skills/gate-erosion-audit/SKILL.md) | Audits an existing safety gate or verifier for five specific ways enforcement silently stops working — fail-open on error, opt-in-by-default, self-supplied evidence, a single unenforced entry point, and asymmetric normalization | Reviewing a gate you're about to trust more, or after a "the gate should have caught this" incident |
| [`skill-suite-router`](skills/skill-suite-router/SKILL.md) | Once a personal AI-agent skill library grows past a few dozen entries, groups related skills behind thin "suite" router skills that only route, so the top-level skill list stays short and trigger phrases stop colliding | A skill/command library that's gotten long enough that two skills compete for the same trigger phrasing |

## Special release — The Stack (2026-08-10)

A one-time distillation of two years of daily AI-tooling use (IDE assistants →
a home-grown multi-agent orchestration platform → CLI agents → a multi-CLI,
multi-model estate) into three things:

- **[`THE-STACK.md`](THE-STACK.md)** — the full write-up: what each era taught,
  the discipline layer, the skills worth installing in order, the twelve
  background agents that should always be running, and how to compose multiple
  CLIs and models.
- **[`agents/`](agents/)** — five drop-in, read-only subagent definitions (the
  "verifier bench"): adversarial-verifier, hostile-reviewer,
  completeness-critic, cheap-grader, researcher.
- **Eight new skills** filling gaps the earlier batches assumed but never
  covered:

| Skill | What it does | Use it for |
|---|---|---|
| [`verification-labels`](skills/verification-labels/SKILL.md) | A four-label vocabulary (VERIFIED / CODE-SHIPPED-NOT-VERIFIED / BLOCKED / INCONCLUSIVE) every agent completion claim must carry, each backed by the exact probe that justifies it | Making "done" impossible to fake in agent status reports, and turning "are you sure?" arguments into evidence lookups |
| [`compaction-contract`](skills/compaction-contract/SKILL.md) | A fixed five-section session-summary template that quotes exact paths/errors/flags instead of paraphrasing them | Long agentic sessions that get compacted or handed off, so the next session resumes without re-deriving state |
| [`adversarial-planning`](skills/adversarial-planning/SKILL.md) | Deep planning for non-trivial changes: parallel research agents, competing designs, then a mandatory attack pass before any implementation | Features, refactors, migrations, and anything you'll hand to an autonomous agent to execute unattended |
| [`model-lane-routing`](skills/model-lane-routing/SKILL.md) | Stable role→model-tier lanes (strongest plans/verifies, cheaper executes, a different vendor judges) that survive model-generation churn, with live-pricing re-verification | Designing multi-model pipelines and monthly cost reviews |
| [`fanout-cost-pinning`](skills/fanout-cost-pinning/SKILL.md) | Pins every spawned subagent to the cheapest adequate model, closing the silent-inheritance leak where parallel readers run on your apex-priced main model | Anything that fans out parallel subagents, and investigating a surprising AI bill |
| [`multi-cli-constitution`](skills/multi-cli-constitution/SKILL.md) | One shared rules file + capability routing table + compiled policy block that keeps several AI CLIs behaviorally identical | The day you add a second AI coding CLI |
| [`background-agent-roster`](skills/background-agent-roster/SKILL.md) | The twelve standing background agents worth running on any machine hosting unattended AI automation, plus the receipt-file discipline that keeps them honest | Growing a scheduled-automation estate without silent three-week outages |
| [`agent-memory-sync`](skills/agent-memory-sync/SKILL.md) | Git-backed persistent agent memory — one fact per file, typed frontmatter, an always-loaded index, and a scheduled commit/rebase/push sync | Making what an agent learned survive sessions, machines, and even switching agent tools |

## This week's 3 skills (2026-W31)

| Skill | What it does | Use it for |
|---|---|---|
| [`chat-platform-agent-bridge`](skills/chat-platform-agent-bridge/SKILL.md) | Wires an external chat platform (Telegram, Discord, SMS, etc.) into an AI agent so you can send it a prompt from your phone and get the reply back in the same chat, with untrusted-input quarantining and sender allow-listing built in | Sending your agent a prompt from your phone while away from your desk, or building a lightweight remote control for an unattended agent without exposing a web endpoint |
| [`production-quality-autopatch-loop`](skills/production-quality-autopatch-loop/SKILL.md) | Continuously scores live production conversation/interaction transcripts against a quality rubric, auto-drafts a minimal prompt-only fix as a pull request, and auto-merges it only once it clears a strict multi-reviewer safety gate | A deployed conversational or text-generating product where you want quality regressions caught from real traffic and small prompt fixes shipped automatically, never auto-merging an unreviewed or oversized change |
| [`agent-burst-resource-prep`](skills/agent-burst-resource-prep/SKILL.md) | A pre-flight routine that frees RAM and drops memory pressure on your machine so it can safely run a larger batch of parallel AI-agent sessions than usual, then restores normal state afterward | Right before spawning a larger-than-normal parallel AI-agent fan-out, or after noticing a big parallel run swapping/thrashing instead of speeding up |

This week's batch was intentionally short — most of what was newly modified in the source skill collection this cycle either duplicated a method already published in an earlier week, or was too tightly coupled to private/internal infrastructure to responsibly generalize. Better a short honest batch than padding with weak entries.

## Week of 2026-07-19

| Skill | What it does | Use it for |
|---|---|---|
| [`architecture-invariant-audit`](skills/architecture-invariant-audit/SKILL.md) | A read-only, dependency-free script that checks a layered codebase against documented architecture rules (layer crossings, legacy reuse, anti-pattern regressions, doc drift) and fails CI when they're violated | Enforcing a layered architecture boundary, tracking a strangler-pattern legacy file's shrink, or catching a previously-fixed anti-pattern before it regresses elsewhere |
| [`policy-prompt-drift-check`](skills/policy-prompt-drift-check/SKILL.md) | Compares a code-level policy module against the natural-language prompt it governs, flags missing anchors and direct ALLOW/FORBID contradictions, and emits a per-policy ALIGNED/WARN/DRIFT verdict | Before merging a PR that touches a policy/constants module shared with a prompt file, or after any prompt rewrite |
| [`git-identity-guard`](skills/git-identity-guard/SKILL.md) | Pre-push check that verifies the active git author email, authenticated gh CLI account, and target remote all match what you declared for this repo, and refuses to push on any mismatch | Working across a personal and a work GitHub account (or several client accounts) on the same machine |
| [`safe-project-retirement`](skills/safe-project-retirement/SKILL.md) | Enumerates every surface tied to a dead project (repos, scheduled jobs, dashboards, notes), gets human confirmation, then archives everything reversibly with an undo manifest instead of deleting it | Cleaning up a finished or abandoned project without hunting down every cron job and dashboard entry by hand |
| [`cross-repo-work-recap`](skills/cross-repo-work-recap/SKILL.md) | Pulls a structured, evidence-backed recap (shipped / in-flight / at-risk) of work across multiple local git repos over a time window, cross-referenced with personal notes | Answering "what did you actually get done this week" across several repos without reconstructing it from memory |
| [`agent-observability-bundle`](skills/agent-observability-bundle/SKILL.md) | Builds a fully-local, zero-cost observability bundle for an AI coding agent — a status line, a hallucination-blocking turn-end hook, and an optional periodic quality grader | Getting visibility into context usage, cost, and unverified "done" claims from your AI coding agent without a paid monitoring service |
| [`text-to-image-bakeoff`](skills/text-to-image-bakeoff/SKILL.md) | Wraps OpenAI gpt-image-1, Fal's Flux Pro, and Google Imagen text-to-image APIs behind one small script with a bake-off comparison mode, backend health tracking, and a reusable prompt template | Generating hero art or concept backdrops when no image-generation MCP/tool is available, or comparing providers before picking a default |
| [`evidence-gated-delegation`](skills/evidence-gated-delegation/SKILL.md) | Before letting a secondary agent, worker fleet, or automation pipeline act on your behalf, requires a proven track record plus deterministic post-hoc verification — never trusts the delegate's own self-report | Wiring up a second agent or automation pipeline that will act without your eyes on every step |
| [`legitimate-work-reroute`](skills/legitimate-work-reroute/SKILL.md) | Recovers full-quality output when a safety classifier misreads legitimate, authorized defensive-security work as an attack because of how the request is worded, without ever evading a genuine restriction | An authorized defensive-security task comes back visibly weaker or refused because it was worded in attack-shaped language |
| [`environment-drift-hunter`](skills/environment-drift-hunter/SKILL.md) | Runs a scheduled and on-demand battery of deterministic, no-LLM checks over a local dev/automation setup and surfaces a ranked, evidence-backed finding list with an autofix-safe flag | Catching doc-vs-code drift, orphan jobs, security-default drift, and committed secrets before they turn into a real incident |

## Week of 2026-07-12

| Skill | What it does | Use it for |
|---|---|---|
| [`negative-prompt-leakage`](skills/negative-prompt-leakage/SKILL.md) | Warns against spelling out literal forbidden phrases in ✗-example prompt blocks — models pattern-match into them and reproduce the exact thing you forbade | Prompts where the model keeps producing an output you explicitly told it never to produce |
| [`fail-closed-guards`](skills/fail-closed-guards/SKILL.md) | Makes sure a guard's missing-data fallback REFUSES the action instead of allowing it, and that every write-site actually populates the field the guard reads | Writing or reviewing any permission check, gate, or precondition with a fallback default |
| [`twilio-a2p-10dlc-compliance`](skills/twilio-a2p-10dlc-compliance/SKILL.md) | Decodes Twilio 10DLC A2P rejection codes, gives the exact website compliance checklist, and covers the non-obvious delete-and-repost resubmission mechanics | A FAILED/rejected Twilio A2P campaign, or building an SMS opt-in flow before submitting one |
| [`skill-estate-guardian`](skills/skill-estate-guardian/SKILL.md) | Lints your own AI-agent tooling (skills, agents, workflows, hooks) for leaked tokens, retired model IDs, unpinned models, and gate docs with no real enforcement | A pre-flight check after writing/editing a skill or agent, or a periodic estate cleanup |
| [`roast-me`](skills/roast-me/SKILL.md) | Multi-round adversarial questioning across failure modes, edge cases, security, and performance that forces you to defend a design before you build it | Stress-testing a plan or architecture decision before you commit to building it |
| [`ai-tells-check`](skills/ai-tells-check/SKILL.md) | A fast linter for the highest-signal "AI-slop" tells in generated frontend/marketing copy — em-dashes, numbered eyebrows, BETA labels, filler phrases | A fast last check after generating any landing page, hero section, or marketing UI |
| [`data-illustration`](skills/data-illustration/SKILL.md) | Turns scores/metrics into an accurate, data-driven SVG illustration instead of a generic chart, with AI-generated imagery layered in only as atmosphere | Visualizing scores/metrics/dimensions when a plain bar/line/pie chart would be boring or off-brand |
| [`agent-engineering-checklist`](skills/agent-engineering-checklist/SKILL.md) | A curated checklist of ~18 evidence-grounded rules for building reliable AI agents — tool-use gating, verification-before-trust, context engineering, trust boundaries | Designing a new agent/workflow, or reviewing an existing one for reliability gaps |
| [`agent-quality-loop`](skills/agent-quality-loop/SKILL.md) | Iteratively grades and improves a conversational agent's prompt quality via synthetic dialogs + hard checks + an LLM judge, with human-approved targeted edits | After any meaningful change to a conversational agent's system prompt, or as a pre-release regression gate |
| [`ai-ugc-video-pipeline`](skills/ai-ugc-video-pipeline/SKILL.md) | A gated pipeline for AI-presenter short-form marketing video, with hard-won fixes for the media-validation, audio-sync, and judge-hallucination traps | Producing or re-cutting a short-form AI-presenter product/marketing video |

## Week of 2026-07-06

| Skill | What it does | Use it for |
|---|---|---|
| [`expert-fanout`](skills/expert-fanout/SKILL.md) | Spawns N domain-expert subagents in parallel to audit a codebase/product/design from different angles, then synthesizes convergent vs. divergent findings | Breaking a surgical-patch loop, getting a second opinion before a risky change |
| [`doc-iterate`](skills/doc-iterate/SKILL.md) | Processes inline `[REVIEWER: ...]` comment markers in shared docs, applies edits in place, flags contradictions | Async doc review between collaborators without a heavyweight commenting tool |
| [`bug-replay`](skills/bug-replay/SKILL.md) | Turns every fixed bug into a permanent regression fixture and replays the whole set before shipping | Catching regressions on bugs you already fixed |
| [`ship-as-artifact`](skills/ship-as-artifact/SKILL.md) | Renders a finished deliverable as a self-contained hosted page instead of a terminal dump | Reports, briefs, audits, and design/mockup previews meant to be shared |
| [`offload`](skills/offload/SKILL.md) | Routes self-contained work onto a secondary AI backend to save your primary quota, then verifies the result yourself | Being low on quota, parallelizing work, getting an independent second opinion |
| [`quality-gate-registry`](skills/quality-gate-registry/SKILL.md) | Maps every "done" claim to the specific proof required before you say it | Preventing confidently reported but unverified "it works" claims |
| [`staff-code-review`](skills/staff-code-review/SKILL.md) | A maximum-depth, multi-agent review panel that auto-locates the diff, fans out cross-functional reviewers, and adversarially verifies findings | Pre-merge high-stakes diffs, production-readiness audits |
| [`production-gauntlet`](skills/production-gauntlet/SKILL.md) | A looped, dual-verification KPI gate you run before calling anything non-trivial "done" | Wanting real walk-away quality on something you built, fixed, or deployed |
| [`autobuild-loop`](skills/autobuild-loop/SKILL.md) | An end-to-end build pipeline (plan → swarm → docs → QA → code quality → canary → summary) gated stage-by-stage on verification artifacts | A defined-end-state build you want to walk away from and trust |
| [`skill-miner`](skills/skill-miner/SKILL.md) | Mines your own session transcripts for repeated workflow patterns and drafts candidate reusable skills for approval | Discovering which of your repeated workflows deserve to become skills |

## Machine-readable feed

[`skills.json`](skills.json) lists every skill from every week in a
structured format (`{ updated, weeks: [{ week, date, skills: [{ name, slug,
description, useFor, path }] }] }`), if you want to build tooling on top of
this feed instead of reading the table by hand.

## License

MIT — see [LICENSE](LICENSE).
