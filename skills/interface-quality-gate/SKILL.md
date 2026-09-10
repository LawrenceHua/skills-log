---
name: interface-quality-gate
description: A mechanical-plus-visual quality gate for any UI (web, app, dashboard, mobile) — an AI-tells lint pass, multi-viewport screenshot checks for overlap/clipping/responsive states, and a frontend-standards checklist — run after generating or reviewing an interface, before calling it done.
---

# interface-quality-gate

Generated UI tends to fail in a small number of recognizable ways: it looks AI-made even when it's functionally correct, it silently breaks at a viewport width nobody checked, or it overlaps/clips in a way a design review would catch instantly but a code review never would. This method treats visual/UX quality as something you actually check, not something you assume from "the code compiles."

## The method

**1. Run a mechanical AI-tells pass on the changed frontend files.** Whether via a bundled linter script or a manual read, check for: generic filler copy and hero labels, decorative status dots or badges with no real meaning behind them, fabricated/placeholder metrics presented as real, and in-app text that explains how the UI works instead of the UI just being clear. Treat findings as prompts to go look, not automatic failures — some are legitimate design choices.

**2. Do a visual check at real viewport widths, not just "it renders."** For anything runnable, use a browser-automation tool to screenshot the interface at both a desktop and a mobile width, then check:
   - No text overlap or clipped controls at either width.
   - Stable, non-collapsing dimensions for toolbars, cards, buttons, and any repeated tile/board element.
   - The first mobile viewport actually shows the relevant content (the real product/subject), not an empty or generic-looking hero.
   - Familiar actions use recognizable icons where one exists, rather than text-only buttons for everything.
   - UI density matches the domain — an operational/utility interface should read as quiet and scannable, not marketing-dense; a marketing page can afford more visual weight.
   - The color palette isn't accidentally dominated by a single hue unless that's an explicit brand requirement.
   - Every asset actually renders — no blank, broken, or purely decorative-and-uninformative images where the image is supposed to convey information.

**3. Check frontend standards that a screenshot alone won't catch.** Keyboard reachability and visible focus states on interactive elements, sufficient contrast, and labels on form controls. Avoid nesting cards inside cards for anything that isn't a genuinely repeated collection item.

**4. Separate verified issues from taste calls in your report.** Cite a concrete file/line or a specific screenshot + viewport for anything you're flagging as broken. Keep subjective "I'd make a different choice here" feedback in its own section so it doesn't get treated with the same weight as an actual defect.

## When to use

- After generating or substantially editing any web page, app screen, dashboard, or mobile layout, before calling the visual work done.
- Reviewing someone else's (or another model's) UI output for the recognizable AI-generated-UI failure modes.
- Setting up a repeatable pre-merge check for frontend changes so visual regressions get caught before a human has to notice them in production.

## How to use

**Install:** copy this folder into `~/.claude/skills/interface-quality-gate/` for personal use, or `.claude/skills/interface-quality-gate/` inside a project. Pair it with whatever browser-automation tool you already have (a Playwright-based skill/MCP, or equivalent) for the screenshot step — this method doesn't require a specific one.

**Invoke:**

```
I just finished this dashboard page. Run interface-quality-gate on it — AI-tells
pass, desktop + mobile screenshots, and the frontend-standards checklist —
before I call it done.
```

```
Review this generated landing page with interface-quality-gate and separate
the actual defects (overlap, broken responsive states, contrast) from taste
feedback.
```
