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

## This week's 10 skills (2026-W30)

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
