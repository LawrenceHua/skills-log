---
name: versioned-visual-feedback
description: Turn element-specific visual feedback into verified source revisions while preserving the viewed version, request outcomes, and design history.
---

# Versioned visual feedback

Keep a visual design, its editable source, and the user's requests connected through successive revisions. The unit of work is a request about something the user actually saw, followed by a source change and an inspected render.

## When to use

Use this skill when someone reviews a page, interface, diagram, or other editable visual artifact and asks for changes to selected elements or regions. It fits both a running preview with selectable elements and a captured image with annotated regions.

Use it when multiple rounds of feedback need a reliable history, especially when requests arrive after the preview has changed. A static image can collect feedback, but implementation requires access to the corresponding editable source. If that source is unavailable, record the request and the limitation.

## How to use

Copy the whole `versioned-visual-feedback` folder into `~/.claude/skills/` for personal use, or into `.claude/skills/` inside a project. Then ask Claude Code to use `versioned-visual-feedback` by name.

Example prompts:

- "Use versioned-visual-feedback on this checkout preview. In revision 2, I selected the order summary heading. Make it easier to distinguish from the item names and show the revised render."
- "Use versioned-visual-feedback for this diagram. In the attached revision 4 capture, the selected lower-right legend overlaps a connector. Move the legend clear of the connector and retain the earlier revisions."

### 1. Establish the design and preview

Keep one stable design identity across the work. Record its editable source, current revision, and preview location. Use an existing revision mechanism or clearly labeled source snapshots so earlier meaningful revisions remain inspectable. Do not replace the history with only the latest image.

Choose available, authorized preview tooling. Prefer a live preview of editable local content or an existing running preview when supported. Use a captured image when live embedding is unavailable. Respect access and framing controls; do not bypass them to embed a page. This workflow requires no particular framework, new server installation, or hosting service.

Label each capture with its design identity, revision, viewport, and relevant state. Refresh it after source changes. A capture shows appearance at that moment; it does not establish that controls work.

### 2. Capture and read requests

Have the user select a visible element or region and describe the desired change. Selection can use native preview controls, an annotation, or a precise description tied to the displayed view. Preserve the version the user saw even if a newer version now exists.

Pull outstanding requests from the available queue before editing. If no queue exists, keep a small manual table in the conversation or existing project notes. This is manual tracking, not an assumed automatic feature.

| Request label | Viewed revision | Target | Desired change | Status | Resulting revision and evidence |
|---|---|---|---|---|---|
| A | 2 | Selected summary heading | Strengthen visual distinction | Pending | Awaiting source edit |

Use pending, in progress, applied, blocked, or deferred consistently. Keep completed requests available for reference and do not apply them twice. Record only feedback the user supplied.

### 3. Reconcile before changing source

Confirm the target still exists and that the current source corresponds to the recorded design. Compare outstanding requests with the current revision. A request against an older revision may already be satisfied, refer to a moved element, or conflict with newer feedback.

Resolve ambiguous targets, stale intent, and conflicting requests explicitly. Ask for the missing decision when necessary; do not silently invent a preference. Keep blocked and deferred requests visible with their reason, and continue independent requests when possible.

### 4. Edit, preserve, and render

Make a bounded source change that addresses the request. Preserve the resulting meaningful revision under the same design identity, with a reference to the request that motivated it. Retain earlier inspectable source revisions and their available previews.

Render the actual changed source. Do not present a retouched screenshot as proof of implementation. Refresh the preview or capture and record its revision and view conditions. If rendering fails, keep the request open and explain what prevented inspection.

### 5. Verify and acknowledge

Inspect the revised render against the user's requested outcome. Check relevant viewport behavior, accessibility, and interaction only to the extent affected. For a changed control, exercise the affected behavior when possible; a screenshot cannot prove interaction.

A saved file, hot reload, or passing lint check alone is insufficient. Mark a request applied only after inspecting evidence that supports its outcome. Otherwise record the completed edit separately from the unresolved verification.

Acknowledge each applied request with its resulting revision and evidence reference. Close the batch with the current preview, inspectable revision history, applied and open request outcomes, and coverage limits. State any untested states or unavailable interaction checks. Stop at the requested scope; do not invent feedback or keep polishing indefinitely.
