---
name: skill-suite-router
description: Once a personal AI-agent skill library grows past a few dozen entries, group related skills behind a handful of thin "suite" router skills — each just a routing table to the real standalone skills — so the top-level skill list stays short and trigger phrases stop colliding.
---

# skill-suite-router

An AI-agent skill (or slash-command, or custom-tool) library that grows organically eventually hits a scaling problem that has nothing to do with any individual skill's quality: the list itself gets long enough that (a) the model has to scan a large catalog every time it decides whether anything applies, and (b) two skills with overlapping trigger phrasing start competing for the same request. Splitting skills up further doesn't fix this — it makes it worse. The fix is a layer of grouping, not more or fewer skills.

## The pattern

Introduce a small number of **suite** skills, one per broad category (e.g. "engineering quality," "design and frontend," "product discovery," "project operations"). Each suite skill:

- **Contains no logic of its own.** It is a routing table: one row per real, standalone skill in that category, with a one-line "use it when" trigger description.
- **Never gets invoked as the final worker.** Its only job is to name the correct standalone skill to actually invoke next. The standalone skills keep existing exactly as they did before — nothing about them changes.
- **Stays short enough to read in one glance** — a markdown table, not a wall of prose. If a suite's table gets long enough to become its own scanning problem, split the category further rather than letting one suite sprawl.

```markdown
---
name: suite-engineering-quality
description: Routes code-quality, architecture-review, debugging, testing, and
  safety-gate requests to standalone skills. Use when the user asks to review
  an API, audit an architecture, find a root cause, or verify a completion claim.
---

Umbrella suite — constituents remain standalone skills; this suite only routes.
Invoke the selected constituent by its own name; do not invoke this suite instead.

| Standalone skill | Use it when |
|---|---|
| api-review | A REST/GraphQL API needs a consistency/security/breaking-change pass. |
| root-cause-debug | A bug or test failure needs systematic investigation before a fix. |
| fail-closed-guards | A guard or precondition needs review for a fail-open default. |
| verify-before-done | A completion/fix/deploy claim needs fresh verification evidence. |
```

## Why this works better than a flat list

- **Triggering gets cheaper and less ambiguous.** The model (or you) narrows to a category first — a coarse, low-collision decision — then picks among a handful of options inside that category, instead of scanning every skill in the library against every request.
- **The real skills don't get diluted.** Because a suite carries no logic, there's no "should this rule live in the suite or in the skill" ambiguity — it always lives in the skill. The suite is purely an index.
- **Growth stays linear, not combinatorial.** Adding skill #80 to the library means adding one row to one suite table, not re-tuning every other skill's trigger phrasing to avoid a new collision.
- **It's cheap to build and cheap to be wrong about.** Because a suite is just a table, mis-categorizing a skill costs one row-move, not a rewrite.

## When to introduce a suite layer

Not from the start — a flat list of a handful of skills is easier to reason about than premature categorization. Introduce suites when you notice any of:

- You (or the model) have started asking "wait, which of these two overlapping skills should fire for this?" more than once.
- The skill list is long enough that you scroll to find something you know exists.
- You're about to write skill #30+ and don't have a mental map of what already exists in that area.

## How to build one

1. **Group your existing skills by rough category** — 4–8 categories is usually the right range; fewer and the suites aren't doing much, more and you've just moved the scanning problem up one level.
2. **For each category, write one suite skill**: a one-line description naming the category and its trigger shape, and a table of `{standalone skill name, one-line "use it when"}`.
3. **State the routing contract explicitly in the suite's own body** — "this suite only routes; invoke the named constituent, not this suite" — so it's unambiguous even to a model that hasn't seen this pattern before.
4. **Leave every standalone skill untouched.** The suite is additive; nothing about the underlying skills should change.
5. **Revisit categories periodically**, not on a schedule — when a suite's table starts feeling too long, or when a new skill doesn't cleanly fit any existing category, that's the signal to re-split.

## When to use

- Your personal or team skill/command library has grown past roughly 30–40 entries and you're starting to lose track of what exists.
- Two skills keep firing for the same kind of request and you want a structural fix, not a trigger-phrase tweak.
- You're onboarding someone else (or a fresh agent session) onto a large skill library and want a fast way to say "here's the map."

## How to use

**Install:** this is a pattern to apply across your existing skills directory, not a single file to copy in. Create one `suite-<category>/SKILL.md` per category directly under `~/.claude/skills/` (or your project's `.claude/skills/`), following the template above.

**Invoke:**

```
My skills directory has grown past 40 entries and two of them keep
colliding on trigger phrasing. Apply skill-suite-router — group them into
suites and show me the routing tables before you create any files.
```

```
Add a new skill for X. Using skill-suite-router, tell me which existing
suite it belongs in, or whether it needs a new category.
```
