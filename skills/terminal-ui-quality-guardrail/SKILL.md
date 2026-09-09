---
name: terminal-ui-quality-guardrail
description: Review terminal and text-interface changes for clear hierarchy, readable contrast, keyboard-visible state, and useful status information before treating a visual change as complete.
---

# Terminal UI Quality Guardrail

Use this after changing a terminal theme, prompt, status line, title, pane layout, or text-based interface. The purpose is to make an interface legible under pressure, including when color or mouse input is unavailable.

## Start with the task, not decoration

Write down the three facts a person needs while the interface is idle and while work is active. Typical examples are the current workspace, the active operation, and an actionable problem state. Put stable identity in the title or header; put changing detail in a status area.

Avoid filling permanent space with timestamps, slogans, or duplicated labels. A short, stable title is easier to scan than a title that changes with every event.

## Review the information hierarchy

Check each view at a normal terminal width and at a narrow width:

1. The primary task and current state are visible without scrolling.
2. Warnings and failures use both wording and an additional visual distinction; color alone never carries the meaning.
3. Secondary diagnostics can be found without competing with the primary task.
4. Truncation preserves the meaningful beginning or provides an unambiguous overflow indicator.
5. Repeated labels and decorative separators do not consume the line needed for an actionable message.

For a status line, prefer a small ordered set such as `state · workspace · mode · remaining context`. Omit fields that are absent instead of rendering misleading placeholders.

## Check visual accessibility

- Use readable foreground/background contrast for normal text. Treat muted text as supporting information, not the only place an instruction appears.
- Give selected, focused, running, waiting, and failed states distinct text or symbols in addition to color.
- Preserve a visible keyboard focus indicator for interactive terminal controls.
- Respect reduced-motion preferences. Progress may update, but it should not depend on flashing or continual movement to be understood.
- Test a light and a dark background when themes can change.

## Exercise real states

Capture or inspect these states where the interface supports them: idle, active, success, warning, failure, empty, narrow layout, long workspace name, and keyboard focus. If a state cannot be exercised, record that gap instead of assuming it looks correct.

Check that changes do not hide important output, steal focus during long-running work, or turn an error into a transient toast that disappears before it can be read.

## Finish with evidence

Run the interface's existing visual or regression checks. Pair that with a manual keyboard pass and a screenshot or terminal capture of the changed state. Report the exact commands and what was observed; a passing syntax check does not prove an interactive interface is usable.
