---
name: right-sized-execution-path
description: Choose the shortest of five execution paths (reply, live probe, timed research, additive change, full build) that still answers a request truthfully, and escalate openly when the evidence shows it needs more.
---

# Right-sized execution path

A setup that pushes every request through intake, planning, dispatch, build, review and release makes a status question take twenty minutes. A setup that treats every request as a quick answer ships guesses. Choose the path before starting the work, using what the request needs.

## 1. Pick the lowest path that fully satisfies the request

| Path | Use it when | Do | Skip |
|---|---|---|---|
| **P0 Grounded reply** | a question or follow-up that the conversation and material already read can answer | answer, citing what you relied on | delegation, build, release |
| **P1 Live probe** | status, counts, "where is X", "did the job run" | find where the truth lives, take one read-only reading, answer | delegation, build, release |
| **P2 Timed research** | discovery, comparisons, tool or approach evaluation | sourced research inside a stated time box, then an evidence check and a report | build, release |
| **P3 Additive change** | a new style, template, option or tweak inside a system that already works | add it as a separate, selectable piece, dry-run in isolation, verify | a rewrite of the existing system |
| **P4 Full build** | new features, multi-file refactors, releases, security, sign-in, infrastructure or data changes | plan, build, independent verification, release gate, live check | nothing |

"Lowest" means lowest among the paths that do not trade away accuracy or safety. Approval rules, stop switches and destructive-action limits apply on every path.

## 2. Tell similar requests apart

One topic can land on three different paths. Classify by the requested outcome, not by the subject.

| Request about a publishing pipeline | Path |
|---|---|
| "Are posts going out?" | P1: read the delivery record and check one published item |
| "Add the pacing from this example as a style" | P3: add a preset beside the existing ones |
| "The encoder keeps failing, fix it" | P4: full engineering work |

A reply to another agent's message is P0 unless it asks you to change code, configuration or production.

If two paths still fit and they differ in what gets changed, ask one question or take the read-only path first.

## 3. Quality rules that fast paths keep

1. **Speed does not lower truthfulness.** Quote the reading you took, with its time. If you could not take one, say `UNKNOWN` and why.
2. **Ground a reply in the exact thing it answers:** the parent message, the file, the record. A remembered summary is not a reading.
3. **Escalate openly.** If a probe shows broken state that needs edits, report the finding at once and propose the move to P3 or P4. Do not silently turn a status question into a long repair.
4. **Additive means additive.** On P3, leave existing behaviour, presets and pipelines in place, and confirm one existing option still works after your change.
5. **Moving up is allowed at any point.** State the new path and the evidence that forced it. Moving down to avoid a required check is not.

## 4. Running a timed research pass (P2)

Sweep outward in four rings, changing sources on each pass so the same few articles are not read twice:

1. **Foundations:** papers, standards, official documentation, established benchmarks.
2. **Builder ground truth:** source code, commit activity, open issues, model or package cards, datasets.
3. **Practitioners:** engineering write-ups, post-mortems, competition and hackathon solutions.
4. **Niche and new:** small-team and solo-builder workflows that larger sources have not covered. Label these as early evidence.

When a time box is set, each pass logs the new sources added, contradictions between rings that were resolved or remain open, and actions you would take with citations. Stop early only when a pass adds nothing, and say that it did.

## 5. Report the choice

Start longer work with one line: `Path P<n> because <reason>; will check <evidence>; escalates if <trigger>.` Short answers on P0 and P1 need no preamble.

## When to use

- A request arrives and it is unclear how much process it deserves.
- Quick questions keep turning into long agent runs, or real engineering is being answered from memory.
- Someone asks to add something to a working system and a rewrite is tempting.

## How to use

1. Copy the `right-sized-execution-path` folder into `~/.claude/skills/` for personal use, or `.claude/skills/` inside a project.
2. Ask Claude Code to use the skill by name.
3. Example prompts:
   - "Use the right-sized-execution-path skill on this request, name the path, then do it: did last night's export run?"
   - "Use right-sized-execution-path. I want this landing page layout available as a new template without touching the current ones."
