---
name: ship-as-artifact
description: Whenever you finish something a person will read, review, or share — a report, brief, plan, audit, roadmap, comparison, or a design/mockup preview — render it as a self-contained hosted page (e.g. a Claude Artifact) and hand over the link, instead of dumping a wall of terminal markdown or leaving a raw file on disk.
allowed-tools: [Read, Write, Edit, Bash]
---

# ship-as-artifact

A finished deliverable belongs on a page, not buried in scrollback. When
you've produced something worth reading, publish it somewhere it can be
opened, scanned, and shared — and link it. Make the rendered page the
default output for deliverables; a raw terminal dump is the exception, not
the rule.

## When to use

Reach for this the moment you're about to hand over one of these:

- **Documents** — reports, briefs, audits, plans, roadmaps, specs, research
  writeups, competitive comparisons, runbooks, post-mortems, status
  summaries, meeting notes.
- **Designs** — UI mockups, before/after comparisons, component previews,
  dashboard concepts, wireframes, style explorations.
- **Anything visual-first** — tables, matrices, timelines, decision trees,
  dashboards where structure and glanceability carry the meaning.

**Skip it for:** a quick factual answer, a single command or its output, a
code diff (that goes inline or as a file the reviewer opens in their
editor), a throwaway check, or something the person is actively editing in
their own tool. Rule of thumb: if it's longer than a screen and someone will
re-read or share it, it's an artifact.

## The method (5 steps)

1. **Write the content to a file** — HTML for anything visual or designed,
   Markdown for plain prose. If your tool wraps the page in
   `<html>/<head>/<body>` for you, write only the page *content*, not the
   full document shell.

2. **Calibrate the design investment first.** A status memo deserves clean
   and utilitarian; a landing-page-style deliverable deserves real
   typographic care. Don't over-design a one-page status update, and don't
   under-design something meant to persuade.

3. **Make it self-contained and theme-aware.** If the hosting surface runs
   under a strict content-security policy (no external scripts, fonts, or
   network calls), inline all CSS/JS, embed any images as `data:` URIs, and
   support both light and dark rendering. Give it a stable title and a
   simple icon so it's recognizable across revisions.

4. **Publish it** with whatever hosting mechanism your tool provides (e.g.
   Claude Code's `Artifact` tool, which returns a shareable URL) and hand
   over the link. To revise, edit the same source file and re-publish to
   the same location so the URL doesn't change.

5. **Hand over the link with one line of "what it is,"** not a re-summary
   of the whole thing. The page carries the detail; your message carries
   the pointer plus the one or two things the reader must decide or notice.

## Show, don't tell

The reason a rendered page beats a markdown dump is that you can render the
actual thing:

- **Reports** — real typographic hierarchy, summary-before-detail
  structure, tables with severity/status indicators, callouts for the
  decisions the reader owns. Lead with the one finding that reframes
  everything.
- **Designs/mockups** — render the design itself in HTML/CSS so people
  *see* it, side-by-side with the "before." Make interactive things look
  interactive.
- **Previews of an external surface** (a chat message card, an email, a
  UI component) — build the preview so it stays safe under a strict CSP:
  embed the payload as an inline object and construct any deep-link
  client-side on click, rather than fetching anything externally.

Strip the throat-clearing — trust the visual to do the work instead of
narrating it in prose above it.

## Verify before you link

- **It renders**: no unclosed tags, no layout collisions, no horizontal
  page scroll (wrap wide tables/code/diagrams in their own scrollable
  container).
- **Both themes are legible**: check contrast in light AND dark if your
  target supports both.
- **Numbers are real**: every figure on the page traces back to something
  you actually verified, not a guess.
- **Provenance**: for anything that could be mistaken for hand-authored
  fact, add a small footer noting it's AI-assisted, the date, and what it's
  based on — a footer, not a banner.

## Common gotchas under a strict CSP

- No external scripts, webfonts, remote images, or network calls — inline
  everything, embed images as `data:` URIs, and prefer a system font stack
  over inlining a heavy webfont.
- Use relative units and flex/grid so the page is responsive; the body
  should never scroll sideways.
- Support both themes via a media query as the default, plus an explicit
  override for hosts that let the viewer toggle themes — style through
  reusable tokens rather than duplicating rules inside the media query.
- Keep the same title/icon across revisions so people recognize the same
  page after an update; only change identity on a genuine topic pivot.

## Updating a page someone hands back to you

If someone gives you a link to a page you (or another session) published
earlier and asks for changes, fetch its current content, edit locally, and
republish to that same URL/location rather than minting a new one.

## How to use

**Install:** copy this folder into `~/.claude/skills/ship-as-artifact/` for
personal use, or `.claude/skills/ship-as-artifact/` inside a project repo.
This works out of the box with Claude Code's built-in `Artifact` tool; if
your environment has a different way to publish a static page (a gist, a
local static-site preview, an internal doc tool), swap step 4 accordingly —
the methodology in steps 1-3 and 5 stays the same.

**Invoke:**

```
Write up this competitive analysis and ship it as an artifact instead of
dumping it in chat — I want a link I can forward.
```

```
Turn this before/after redesign into a rendered side-by-side mockup and
publish it so the team can click through it, rather than describing it
in text.
```
