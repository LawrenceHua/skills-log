---
name: coherent-product-design-workflow
description: Turn a product change into a coherent interface by defining the user job and states first, compiling reusable visual and interaction rules, then verifying the primary journey across real conditions.
---

# Coherent Product Design Workflow

## When to use

Use this for a new interface, a major screen redesign, or a product surface that has grown inconsistent. Start from the user's job and observable behavior; visual style follows from the contract.

## How to use

Install the skill for personal use or one project:

```bash
cp -R skills/coherent-product-design-workflow ~/.claude/skills/
# or: cp -R skills/coherent-product-design-workflow <project>/.claude/skills/
```

Then ask your assistant, for example:

- `Use coherent-product-design-workflow to define the primary journey and states for this settings redesign.`
- `Audit this interface for component and state inconsistencies, then give me the smallest complete vertical slice to build.`

## Ground the work

Write one target sentence:

> Help **this user** complete **this job** through **this primary action**, with **this observable success signal**.

List non-goals and trust constraints beside it. Inspect the current journey, actual content, error conditions, and available evidence before choosing colors or layout patterns.

## Model the experience

Map the primary journey from entry to recovery. For every screen or component, define:

- the user's immediate goal;
- the primary action and a safe exit;
- loading, empty, invalid, error, success, disabled, and returning states;
- keyboard behavior and narrow-screen behavior;
- the signal that tells the user the action worked.

Do not design only the ideal state. A consistent error and empty state often determines whether a product feels trustworthy.

## Compile a small system

Define reusable roles before composing pages:

- semantic color roles for content, surfaces, interactive states, success, warning, and error;
- a bounded type scale and spacing scale;
- rules for borders, elevation, motion, focus, and touch targets;
- component contracts covering anatomy, variants, state, responsive behavior, and content limits.

Use these roles in components instead of scattering raw visual values through page code. When a new value recurs, add a named role with a reason.

## Build one complete vertical slice

Choose the highest-value journey and implement it across real data and state transitions before broadening page coverage. Reuse working product logic; a static mock cannot establish that the journey works.

Keep page composition, reusable components, styling rules, and state handling separately understandable. This makes later changes less likely to create visual drift.

## Verify with real conditions

Exercise the primary journey at common desktop and narrow widths. Include keyboard-only navigation, long content, slow responses, empty results, errors, and reduced motion where the product supports it. Check that focus is visible, text remains readable, controls have usable targets, and no horizontal overflow appears.

Capture the relevant evidence and run the project's existing functional, accessibility, visual, and performance checks. Treat each result separately: a rendered screenshot, a passing test, and a production observation answer different questions.

## Iterate from evidence

When a review finds a defect, fix the underlying contract or component rule rather than applying a page-specific cosmetic patch. Keep a concise record of the user job, states exercised, commands run, evidence locations, and unresolved limitations so a future change can start from facts.
