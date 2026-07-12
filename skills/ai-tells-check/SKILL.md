---
name: ai-tells-check
description: A pre-flight linter for the highest-signal "AI-slop" tells in generated frontend/landing-page/marketing copy — em-dashes in UI text, numbered section eyebrows, version/BETA hero labels, generic filler phrases, decorative status dots. Flags, never auto-edits.
---

# ai-tells-check

Generated frontend and marketing copy tends to converge on a small set of visual and textual "tells" that make it read as obviously AI-made. This is a fast, mechanical, dependency-free pass you run after generating or reviewing any landing page, hero section, or marketing UI — a final check, not a replacement for actual design judgment.

## When to use

- Right after generating or substantially editing a landing page, hero section, or any marketing-facing UI.
- When someone asks "does this look AI-generated / too generic?"
- As a fast last check before you consider a design/copy pass done — pairs with (doesn't replace) whatever deeper design review process you already use.

## What it catches

- **Em-dashes in UI copy.** The single highest-signal tell — real product copy overwhelmingly avoids the em-dash; AI-generated marketing copy overuses it. Replace with a comma, a period, or a restructured sentence.
- **Numbered section "eyebrows."** Labels like `006 · How it works` or `00 / INDEX` in front of a section heading. This specific decorative-numbering pattern shows up disproportionately in AI-generated sites — drop the number, keep the label if it's genuinely useful.
- **Version/beta labels in the hero.** `V0.6`, `BETA` badges sitting in the primary hero — this reads as a placeholder that was never removed, not as an intentional design choice.
- **Generic filler phrases** — vague social-proof language that names no one in particular (e.g. "quietly in use at leading teams") without a real, checkable claim behind it.
- **Decorative status dots** — a colored dot next to a label with no actual live status behind it (not wired to any real state) is decoration pretending to be information.

## How to run it

Read through the generated HTML/JSX/copy and check line-by-line against the list above. For each hit, note the file and line, and propose the concrete fix (not just "remove it" — say what it should become, e.g. "replace the em-dash with a period and split into two sentences"). This is advisory: surface the findings, let a human or a design-focused pass decide what to change — never auto-edit copy on this pass alone.

If you want a fast automatable version: grep for the em-dash character directly, grep for a `\d{2,3}\s*[·/]` pattern near heading text, and grep for the literal strings `BETA`, `v0.`, and known filler phrases. Treat any hit as a candidate, not an automatic fail — false positives happen (a legitimate version number in a changelog page isn't a hero-label issue).

## Scope

This is a fast mechanical last check. It does not replace an actual design review, an accessibility audit, or a copywriting pass — it exists to catch the small set of tells that are cheap to detect and disproportionately damaging to how "made by a person who cared" a page reads.

## How to use

**Install:** copy this folder into `~/.claude/skills/ai-tells-check/` for personal use, or `.claude/skills/ai-tells-check/` inside a project repo so the whole team gets the same final check.

**Invoke:**

```
Run ai-tells-check on the landing page I just generated — any em-dashes,
numbered eyebrows, beta labels, or filler phrases to fix before I ship it?
```

```
Does this hero section look AI-generated? Check it against ai-tells-check
before I show it to anyone.
```
