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

## This week's 10 skills

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
