---
name: design-with-intent
description: Edit a visual experience against an explicit intent brief, with journey evidence, protected details, independent critique, and a bounded stop rule.
---

# Design with intent

Give a visual experience a clear point of view, then revise it against evidence. One editor owns coherence across the journey. Correctness checks establish whether it works; editorial review establishes whether its choices serve the intended audience.

## When to use

Use this skill when building or reviewing an interface, page, presentation, or other visual experience whose first draft feels interchangeable, inconsistent, or prematurely finished. Scale the review to the user's task. A small utility needs clarity, not decorative complexity. Skip isolated spelling corrections or work without a visual experience.

## Working method

### 1. Make intent observable

Before building or revising, write a short brief:

- **Audience, job, and context:** Who is using this, what outcome do they need, and under what constraints?
- **One to three traits:** Pair each trait with visible evidence. For example, “reassuring” could mean explaining what happens after submission, rather than adding soft colors.
- **References:** Describe useful qualities generically, such as the legibility of a transit diagram. Identify the principle to borrow, not a surface to copy.
- **Quality criterion:** State what the person must understand or accomplish and how the review will check it.
- **Avoidances:** Name choices that undermine this purpose, such as playful motion during a time-sensitive task.

Use existing design tokens and components. Express intent through content, hierarchy, behavior, and purposeful details. Propose a justified system change explicitly if needed; do not quietly create a competing visual system.

### 2. Establish editorial ownership and evidence

Assign one editor role to resolve competing suggestions and own the final assessment. Reserve a timebox for critique and revision. State the critical journey, representative conditions, and review coverage required.

Keep the initial rendered version as round zero. Save screenshots or an equivalent inspectable artifact, with viewing conditions and the version reviewed. Use safe sample content where evidence might expose sensitive information. Retain each later reviewed version so improvement claims can be checked against predecessors.

### 3. Walk the experience and check its meaning

Start where a person actually enters, including any introductory or access step. Follow their task through its outcome. For a presentation, follow the reading sequence and the decision it asks the audience to make.

Check representative narrow and wide layouts where relevant, keyboard navigation, enlarged text, and reduced motion when animation is present. At each step record what is visible, the expected action, the observed result, and evidence. Check transitions, return visits, back navigation, and recovery from mistakes.

Separate two review tracks:

- **Correctness:** Do controls work? Is content readable and accessible? Are counts, dates, and labels accurate and consistent? Do empty, loading, error, unavailable, stale, and sample states communicate their actual meaning? Missing data must not imply success or a measured zero.
- **Editorial judgment:** Is the purpose apparent? Does hierarchy match the person's priorities? Do wording, pacing, and details express the brief throughout? Support judgments with observable examples.

Use approved previews, fixtures, or test environments to exercise failures. Do not send messages, spend money, alter live data, or disrupt services merely to review a flow. If a critical step cannot be safely observed, record it as unseen and leave the assessment incomplete.

### 4. Test recognition and protect purposeful details

Cover the name and logo. Could an unrelated experience replace them without changing anything meaningful? Identify observable choices that express this brief: a distinctive explanation, a recurring visual device, or behavior anticipating the audience's situation. If none remain, revisit the brief and its execution. Do not add novelty solely to pass this test.

Keep a protected-details register:

| Detail and location | Purpose for the audience | Evidence it helps | When to reconsider |
|---|---|---|---|
| Describe the choice | Connect it to the brief | Record observation or uncertainty | State a failure condition |

Before removing a registered detail, the editor checks its purpose and records the decision. Protection never excuses accessibility, usability, or correctness failures. A quiet utilitarian design may need no unusual detail; record why.

### 5. Critique, decide, and revise

When available, ask a fresh reviewer to inspect the brief and rendered journey without the builder's explanation. Ask what they understand, where they hesitate, and which choices contradict the brief. A separate reviewer context challenges assumptions; an AI critique is not validation by real users. Disclose unavailable independent review.

Keep a critique log:

| Round | Observation and evidence | Severity | Disposition and reason | Intended change | Recheck result |
|---|---|---|---|---|---|
| Number | Location and observed problem | Blocker, major, or minor | Fix, reject with evidence, or defer | Expected improvement | New evidence or still open |

A blocker prevents the core task, misleads materially, or makes a critical step inaccessible. A major issue substantially impairs comprehension, usability, or the stated intent. A minor issue has limited impact.

Evaluate each finding. Fix confirmed blockers and major issues before acceptance. Reject unsupported findings with evidence, not preference alone. Deferring a blocker or major issue leaves the assessment incomplete; deferred minor issues need a reason and next action.

Apply the smallest purposeful revision and inspect the changed journey again. Retain before-and-after evidence and check nearby behavior for regressions. Do not invent findings or make gratuitous changes to meet an iteration quota.

### 6. Stop with an honest assessment

Accept only when no blockers or major failures remain unresolved, critical steps have been observed, and two consecutive review passes find no new blockers or major failures. A second pass may examine the unchanged version. Any subsequent change requires renewed review of affected evidence.

If the timebox expires first, return **incomplete** or **needs review**, listing open findings, unseen steps, and the next action. Report independent-review gaps and coverage limits even when the observed scope meets the stop rule. Deliver the brief, protected-details register, critique log, retained evidence, and editor's assessment together.

## How to use

Copy the entire `design-with-intent` folder into `~/.claude/skills/` for personal use, or into `.claude/skills/` inside a project. Refresh the session if needed, then ask Claude Code to use `design-with-intent` by name.

Example prompts:

- “Use design-with-intent to review this appointment-booking prototype. Check the journey from first visit through confirmation, including unavailable times, and retain the critique evidence.”
- “Use design-with-intent to revise this instructional slide deck for first-time readers. Define the intent, preserve purposeful details, and report review gaps.”
