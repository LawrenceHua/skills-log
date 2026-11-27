---
name: skill-discovery-eval
description: Test whether real requests reach the right handler and surface the right skill, using a fixed labelled case set, a no-dispatch router run, a model-free description coverage check and a failure table with causes.
---

# Skill discovery eval

A skill that never surfaces for the request it was written for does nothing. Adding skills, editing descriptions or changing a router can break discovery silently. This eval measures it with requests worded the way users write them.

## 1. Build a fixed case set

One JSON object per line:

```json
{"id": "C01", "cat": "finance", "text": "Buy ten shares for me now", "targets": ["finance"], "skills": ["read-only-monitor"], "must_hold_or_refuse": true}
```

- `targets`: acceptable destinations. `skills`: skills that should surface; leave empty when none should.
- Use at least 30 cases covering status questions, how-to requests, research, security, actions that need approval (which must hold or refuse), ambiguous wording and requests nothing should handle.
- Take wording from real requests, with private details removed. Do not copy phrases from skill descriptions, which inflates the score.
- Label expected answers before running anything. Keep some cases unused while editing descriptions.

## 2. Check the harness before believing a score

- The router can see the full skill catalogue. Count what it loaded; a hit rate near zero often means it saw one skill or none.
- It is configured as in production, including any permission or class settings. A missing setting can hold every case and look like a routing failure.
- One obvious control case passes.

## 3. Run the router for labels only

Point it at a temporary state folder and stop after classification. Nothing is dispatched. Never use a path that can act, and never use the live state.

If the router calls a local model, check free disk and memory first, run outside busy hours and unload the model afterwards. If resources are short, run step 4 only.

Score destination accuracy, expected skill in the top three, and correct hold or refusal on gated cases. Report counts along with percentages, and report incomplete runs as incomplete. Any gated case that would have been dispatched is a failure whatever the averages say.

## 4. Check description coverage without a model

This rough proxy asks whether descriptions contain the words users use:

```python
import json, pathlib, re, sys

STOP = {"a", "an", "the", "to", "of", "and", "or", "for", "my", "me", "is", "it",
        "on", "in", "this", "that", "with", "use", "when", "i"}

def words(text):
    return {w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP}

catalog = {}
for path in pathlib.Path(sys.argv[2]).glob("*/SKILL.md"):
    match = re.search(r"^description:\s*(.+)$", path.read_text(encoding="utf-8"), re.M)
    if match:
        catalog[path.parent.name] = words(path.parent.name + " " + match.group(1))

hits = total = 0
with open(sys.argv[1], encoding="utf-8") as cases:
    for line in cases:
        if not line.strip():
            continue
        case = json.loads(line)
        if not case.get("skills"):
            continue
        query = words(case["text"])
        scored = sorted((-len(query & v), name) for name, v in catalog.items())
        top = [name for score, name in scored[:3] if score < 0]
        total += 1
        if set(top) & set(case["skills"]):
            hits += 1
        else:
            print(case["id"], "wanted", case["skills"], "got", top)
print(f"skills loaded: {len(catalog)}  hit@3: {hits}/{total}")
```

Run it as `python3 coverage.py cases.jsonl <skills-folder>`. It reads single-line descriptions only, so check the loaded count against your catalogue. It measures wording overlap, not what a model would choose.

## 5. Record each miss

| Case | Got | Wanted | Cause | Fix |
|---|---|---|---|---|

Typical causes: missing skill, weak description, destination not permitted, a permission gate, ambiguous case label. Fix one cause at a time, rerun the same set, then check the unused cases. Save the date, catalogue size and headline numbers as the next baseline.

## When to use

- After adding or rewording skills, or changing a router.
- As a periodic check that a growing skill library is still reachable.

## How to use

1. Copy the `skill-discovery-eval` folder into `~/.claude/skills/` for personal use, or `.claude/skills/` inside a project.
2. Ask Claude Code to use the skill by name.
3. Example prompts:
   - "Use the skill-discovery-eval skill to draft 30 labelled cases for my skills folder, then run the coverage check."
   - "Use skill-discovery-eval to explain why these requests miss the skill written for them."
