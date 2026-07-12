---
name: skill-estate-guardian
description: Continuously lint your own AI-agent tooling (skills, subagent definitions, workflow scripts, hooks, MCP config) for the defect classes that quietly rot an agent estate — leaked brand tokens, retired model IDs, unpinned subagent models, "mandatory gate" docs with no real enforcement, dead/unreachable skills — and re-run it every time you add or edit one.
---

# skill-estate-guardian

Every skill, subagent definition, workflow script, and hook you write becomes part of what every future session inherits. Drift here is high-leverage in the bad direction: a stray brand token in a skill's `description:` leaks into every session's tool list; a subagent call with no pinned model silently bills at whatever your priciest default is; a doc that says "MANDATORY — no opt-out" but has no hook actually wired to it is a lie your own agent will trust. This skill turns "audit my AI tooling for that stuff" from a one-off cleanup into a repeatable checklist you run on a schedule and after every edit.

## When to use

- You just created or edited a SKILL.md, subagent definition, workflow script, or hook, and want a fast pre-flight check before considering it done.
- You suspect drift has accumulated — skills that no longer fire, hooks pointing at scripts that moved, models that were retired months ago still referenced in a subagent config.
- Periodically (weekly is reasonable) as a maintenance pass over your whole skills directory and settings.

## The defect classes to check

Run each of these as a manual audit pass (grep + read), or write a small script that automates the mechanical ones. None of these require an LLM call — they're all deterministic pattern checks.

| Check | What to look for | Why it matters |
|---|---|---|
| **Frontmatter sanity** | `name:` in the YAML matches the directory name; `description:` is non-empty, third-person, and concrete (not "helps with X stuff") | A vague or missing description means the skill never actually triggers on the right prompts |
| **Stale paths** | Any absolute path referenced in a skill/hook that no longer exists on disk | The doc is actively lying about live infrastructure — grep every path mention and check it resolves |
| **Retired model IDs** | Hardcoded references to a model ID/alias that's been deprecated or retired | Silently routes to a dead model, or a wildly mispriced one |
| **Leaked internal tokens** | Company/product/employer names, internal hostnames, teammate names, or absolute personal paths inside a skill's frontmatter or body — especially if that skill is ever shared, published, or copied to another machine | These strings leak into every session's available-skills list and into anything you export/publish |
| **"Gate that lies"** | Doc language like "mandatory," "always runs," "no opt-out" describing a check that has no actual hook, cron, or enforcement wired up anywhere | The agent (and you) will trust an enforcement mechanism that doesn't exist |
| **Loader-invisible nesting** | A skill directory with no top-level SKILL.md, but a SKILL.md nested one level deeper | Most skill loaders only discover top-level files — this skill is silently dead weight |
| **Unpinned subagent models** | A subagent spawn call (in a workflow script or agent definition) with no explicit model set | It silently inherits whatever your default/most-expensive model is, instead of the cheapest model that fits the job |
| **Broken hook wiring** | A hook command in your settings file that points at a script path which doesn't exist, or isn't executable | Silent, broken automation — nothing tells you it stopped firing |
| **Wrong exit-code semantics** | A "blocking" pre-action hook that exits with a non-blocking status code | A gate that looks like it blocks but actually always lets the action through |
| **Duplicate/diverged skills** | The same skill name existing in more than one location with different content | Ambiguous which copy is authoritative — a silent source-of-truth bug |
| **Dead-weight skills** | Skills that never fire (check your session logs / telemetry if you have any) and no longer match anything you actually do | Advisory only — a zero-fire skill might just be niche, not dead; confirm before archiving |

## How to run it

**Fast pass (single file, right after you write it):** re-read the file you just created/edited against the table above. This catches most of the mechanical issues (frontmatter, stale paths, leaked tokens, unpinned models) in under a minute.

**Full pass (your whole estate):**
1. List every skill's SKILL.md, agent definition, and workflow script.
2. For each, check frontmatter sanity, grep for absolute-path patterns, grep for any brand/company names you've decided are never allowed in a shareable artifact, and grep for retired model IDs.
3. For every workflow script and agent definition, grep for subagent-spawn calls with no `model:` argument set.
4. For every hook entry in your settings file, confirm the referenced script exists and is executable, and that any "must block" hook uses the blocking exit code your harness actually honors (not just any non-zero code — some harnesses only treat a specific code as blocking).
5. Rank findings P0 (breaks something / leaks something) → P2 (doc-truth nit), and fix P0/P1 before moving on.

## For judgment calls a checklist can't make

Some questions aren't mechanical — "is this skill genuinely redundant with that one?", "does this description actually trigger on the prompts I meant it to?", "is this a real dead skill or just a niche one I haven't needed this month?" For those, don't trust a single pass: read the two skills side by side yourself, or ask a fresh session (with no memory of why you wrote either one) to compare them and report overlap versus genuine difference. Default to skeptical — a first-pass "these are redundant" verdict is worth re-checking by actually opening both files before you delete either.

## Fixing philosophy

1. **Reversible first.** Move/rename over delete. If you're disabling a hazardous cron or hook, rename it (e.g. append `.disabled`) rather than deleting it outright, so it's a one-line change to bring back.
2. **Verify before you fix.** A deterministic scan over-flags on purpose — better a false positive than a missed real one. Before editing anything that touches a live/production path, read it and confirm the finding is real.
3. **Don't inflate severity to look thorough.** Most "this skill's whole premise is broken" findings turn out to be "the doc oversells what's actually a manual step" — that's a doc-truth fix, not an outage.
4. **Cheapest model that fits, always pin it explicitly.** Route your cheap/fast model to mechanical grading and triage subagents, and reserve your most capable model for genuine synthesis or judgment calls — but never leave a subagent call unpinned and hoping for the best.

## How to use

**Install:** copy this folder into `~/.claude/skills/skill-estate-guardian/` for personal use — this is inherently a personal/per-machine skill since it audits your own local tooling.

**Invoke:**

```
Run skill-estate-guardian over everything I just wrote in this session — any
leaked paths, unpinned models, or gate docs with no real enforcement?
```

```
It's been a month since I last cleaned up my skills directory. Do a full
skill-estate-guardian pass and give me a ranked P0/P1/P2 list.
```
