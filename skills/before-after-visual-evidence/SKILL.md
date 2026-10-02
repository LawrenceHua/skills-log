---
name: before-after-visual-evidence
description: Capture matched before-and-after screenshots, compare pixels, and document intended changes and visual regressions.
---

# Before and After Visual Evidence

Use repeatable image pairs to review a visual change. Preserve the original captures, inspect the images, and separate observed differences from assumptions about implementation.

## When to use

- Reviewing changes to layout, typography, colors, spacing, or responsive presentation.
- Checking whether a targeted visual fix disturbed another part of a screen.
- Preparing visual evidence for a change review.

Skip changes with no rendered effect. Screenshots supplement interaction and accessibility tests; they do not replace them.

## Working method

1. **Define the comparison.** List the screens, states, and intended changes. Choose the minimum and maximum supported viewport widths, record their heights, and add intermediate widths where a changed breakpoint or layout needs coverage. Identify the actual baseline and changed build for each target. Use sanitized sample data and avoid capturing personal information or credentials.

2. **Preflight the available tools.** Identify a screenshot tool and a pixel comparison tool actually available in the environment. Check their supported settings and output formats. Launch the required browser or application, open the target, and capture a small test image. Open that image to confirm capture works. Verify the comparison tool can read the format and produces a difference image and a documented metric. Do not infer readiness from an installation directory or invent a helper script. If tooling is unavailable, report the missing capability and follow the task's authorization rules for installation.

3. **Lock rendering conditions.** Record browser or renderer version, viewport dimensions, image scale or device pixel ratio, zoom, theme, locale, fonts, and screenshot scope. Use the same data, selected controls, scroll position, open overlays, and loading state on both sides. Wait for fonts, images, and relevant content to finish rendering. Freeze animation and time-dependent content consistently when possible. Record unavoidable variation. Any masks must match across the pair and must not hide the area being reviewed.

4. **Preserve a trustworthy baseline.** Capture the unchanged target before editing, or use an existing capture with sufficient provenance to reproduce its conditions. Save lossless images under a new evidence folder, such as `evidence/visual-review/before/`, and record each image's target and settings. Never reconstruct a supposed before image from the changed screen. If a trustworthy baseline cannot be obtained, state **baseline unavailable**; a review of the current screen cannot establish a before-and-after result.

5. **Capture the changed targets.** Repeat the same capture procedure and settings against the changed build. Save to a separate `after/` folder. Pair images by screen, state, and viewport. Check image dimensions before comparison. Do not resize or crop away a mismatch to force comparability. A changed full-page height may be a meaningful finding; report it and use matching viewport or region captures when needed for a valid pixel comparison.

6. **Generate actual pixel comparisons.** Run the available comparison tool for every valid pair and retain its difference image and raw result. Record the tool, settings, and metric units: for example, differing pixel count, or percentage of compared pixels. For a percentage, record the denominator and any excluded areas. Check the tool's documented result semantics: an exit status indicating differences is distinct from an execution error. Missing outputs, unreadable inputs, or failed execution make the comparison inconclusive. Do not apply a universal acceptable difference threshold.

7. **Inspect every image.** Open every before image, after image, and difference image. Review text wrapping, clipping, alignment, spacing, contrast, missing content, and responsive changes. Classify findings as intended changes, regressions, or inconclusive differences. Name the screen region and visible effect. A small metric can conceal a serious defect; a large metric can reflect an intended redesign. Describe visual observations without claiming they prove DOM structure, computed styles, accessibility, or functional behavior.

8. **Preserve the review evidence.** Keep the baseline, changed captures, difference images, and notes together without overwriting earlier runs. Include capture settings, build references, metrics, findings, limitations, and artifact paths. After a fix, capture a new result against the preserved baseline. Report unresolved regressions and unavailable comparisons explicitly.

## How to use

Copy the `before-after-visual-evidence` folder into `~/.claude/skills/` for personal use, or `.claude/skills/` inside a project. Ask Claude Code to use the skill by name.

Example prompts:

- “Use before-after-visual-evidence to review this spacing change at our smallest and largest supported viewport widths.”
- “Use before-after-visual-evidence to compare the old and new dialog states, preserving screenshots and documenting any regressions.”
