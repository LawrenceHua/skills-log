---
name: data-illustration
description: Turn a set of scores/metrics into an accurate AND illustrative graphic — the data literally drives the shape of the artwork, so it's provably faithful while reading as a designed illustration instead of a generic chart.
---

# data-illustration

Plain chart libraries (bars, lines, radar) are accurate but forgettable. The opposite failure — an AI-generated "data visualization" image — is beautiful but can't actually encode a number faithfully, so it's decoration pretending to be data. This skill does both honestly: the data drives the geometry of a generated SVG (the accurate, reproducible core), and any AI-generated imagery is layered in only as atmosphere, never to convey a value.

## When to use

- Someone wants to visualize scores/metrics/dimensions but a plain bar/line/pie chart would be boring or feel off-brand.
- Requests like "make this visualization actually look designed," "something more illustrative than a chart," or "generate a real graphic for the dashboard, not a default chart."
- Prefer this over hand-coding a one-off chart whenever the output is meant to look intentionally designed rather than default-library.

## The accuracy contract (non-negotiable)

1. **Every quantity in the output is computed from the input values, in code.** Shape length, radius, label text, the center read-out number — all derived programmatically, never eyeballed or drawn by an image model.
2. **AI image generation is decoration only.** If you layer in a generated backdrop, constrain the prompt to abstract texture — no text, no numbers, no figures, no logos. If image generation is unavailable, the graphic must still be complete and correct without it.
3. **Everything is labeled.** Every encoded element gets a label, the headline number gets a center read-out, and a one-line legend states what the form actually means. A beautiful graphic nobody can decode is a failure, not a win.

If you're ever tempted to let an image model "draw the chart" directly — stop. That breaks the contract and the result will be subtly (or badly) wrong.

## The default form: an organic "bloom"

N dimensions/scores → N petals radiating from a center point. Per petal:
- **Length** encodes the value (longer = higher), against faint integer guide rings so it's still readable as a number, not just a vibe.
- **Fullness** widens slightly with the value — higher scores read as visually "lusher."
- **Color** maps to the value's band via a semantic ramp (e.g. green for high, amber for mid, warm red/terracotta for low).
- **A tip label** states the dimension name and its exact number.
- **A center disc** shows the average, color-graded by its own value, with a short caption.
- **A legend line** states the encoding in plain language ("petal length = score out of 5").

This reads as a unique organism per dataset — not a generic radar chart — while every value is still exactly readable.

## Building it

1. Take the input as a simple `{dimension: value}` map plus a title and an average.
2. Write a small script (any language with SVG output is fine) that computes each petal's geometry directly from the values — angle = evenly spaced by dimension count, radius = a function of the value, color = a lookup against your band thresholds.
3. Render labels and the legend as real SVG text elements, not baked into any image layer.
4. **Optional atmosphere layer:** generate an abstract, on-theme backdrop image via whatever image-generation API you have access to, composite it under the illustration at low opacity behind a vignette so the center stays legible. Cache this — generate it once at build/author time, never on every page render (it's slow and costs money).
5. Make the output self-contained (a single `.svg`, with any backdrop embedded as a data URI) so there's no separate asset to manage.
6. If you want the shapes to be interactive (hover/click to reveal each dimension's definition + exact score + source), wrap each element with data attributes (`data-dimension`, `data-score`, `data-definition`) that a small script can read to drive a side panel.

## Extending the form

The bloom is the default, not the only option — pick the form that fits the data shape, but keep the accuracy contract no matter which you use:
- **Ridgeline/contour** for a distribution or a value tracked over many items.
- **Isotype** (repeated glyphs, the last one partially filled) when counting is the point and you want it to read as literal quantity.
- **Constellation** when relationships between items matter more than their individual magnitudes.

## Anti-patterns

- Letting an image model render the chart or the numbers — the values will be wrong or fabricated.
- A gorgeous graphic with no labels or legend — undecodable is useless, no matter how nice it looks.
- A generated backdrop loud enough to compete with the data layer's legibility — keep it low-opacity, behind a vignette.
- Calling an image-generation API on every page render instead of caching — slow and needlessly expensive.

## How to use

**Install:** copy this folder into `~/.claude/skills/data-illustration/` for personal use, or `.claude/skills/data-illustration/` inside a project repo.

**Invoke:**

```
Turn these 6 scores into a data-illustration bloom instead of a boring bar
chart — title it "Q3 Retro", give it a center average, and add a legend.
```

```
This dashboard's chart looks generic. Use data-illustration to make it an
accurate, labeled illustration instead — no AI-drawn numbers, everything
computed from the real data.
```
