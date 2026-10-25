---
name: story-first-video-production
description: Plan and produce a narrative video through causal story beats, continuous-action coverage, a timed rough cut, and separate technical and editorial review.
---

# Story First Video Production

## When to use

Use this to develop a narrative film, explainer, demonstration, or short video whose meaning depends on action unfolding over time.
It is especially useful when attractive images or passing media checks have obscured weak storytelling, pacing, or continuity.
Begin before generating footage, or use the same process to diagnose an existing cut.

## How to use

Copy the `story-first-video-production` folder into `~/.claude/skills/` for personal use, or into `.claude/skills/` inside a project.
Then ask Claude Code to use the skill by name.
Use the editor, recording equipment, and generation tools already available to you; this skill requires no bundled scripts.

Example prompts:

- "Use story-first-video-production to plan a repair tutorial in which a failed first attempt leads to a useful discovery. Give me the beat plan and rough-cut review criteria before footage generation."
- "Use story-first-video-production to review this complete cut. Identify where the action loses continuity or the story stops progressing, with timestamps and specific revisions."

## 1. Establish the creative and acceptance brief

Write a concise brief with the audience, intended effect, central question, and what the viewer should understand or feel at the end.
Set the delivery format, orientation, approximate duration, viewing context, and accessibility needs from the request.
Define the creative identity: visual language, performance style, narration perspective, sound character, and caption treatment.
Use these choices consistently while allowing scene-specific decisions that serve the story.
Set observable acceptance criteria before production: what action must be visible, what causal change must be understood, and what the final export must support.
Do not inherit arbitrary runtimes, shot counts, narration speeds, or quality scores from another project.

Confirm rights to source material and consent for identifiable likenesses or voices where relevant.
Use only the user's existing approved budget and tools; a production plan grants no authority to spend or publish.
If a necessary asset, permission, or budget decision is missing, identify the gap before the dependent step.

## 2. Make the story move through consequences

Use hook, complication, escalation, turn, and landing as a planning shape, adapting it to the subject.
For each beat, state what the subject wants, what happens, and what changes because of it.
The hook creates a specific question or tension that the video can actually resolve.
The complication obstructs the goal; escalation changes the stakes or makes the first response insufficient.
The turn changes the subject's understanding or available action, rather than merely introducing another event.
The landing resolves the central question through a visible consequence, useful demonstration, or earned emotional result.

Read the beats as "because this happened, therefore that follows."
If two beats can swap places without changing anything, strengthen their relationship or remove repetition.
For factual work, distinguish documented events, interpretation, and dramatization.
Preserve attribution and uncertainty; do not invent a consequence to make a cleaner arc.
Check that narration adds context, perspective, or tension instead of describing everything already visible.

## 3. Plan scenes as continuous action

Give each scene a subject doing something concrete in a specific setting.
Name the relevant props, their states, the light source, and the environmental details that explain the action.
Choose details for their narrative function rather than filling the frame with unrelated objects.
Plan wide, medium, and close coverage where each scale reveals something useful about the same continuous action.
A wide shot can establish geography, a medium shot can show the action, and a close shot can expose the decisive detail.
Use the scales the action needs; do not enforce a quota of angles.

For every cut, specify the outgoing action and the incoming action that continues or responds to it.
Track screen direction, eyelines, hand and prop positions, clothing, light, and setting across shots.
Keep a continuity ledger: scene, established fact, shot references, deliberate change, and unresolved mismatch.
If time or location changes, supply a readable transition rather than disguising a continuity error.

## 4. Write a timed beat and shot plan

Assign provisional start/end times while reading narration aloud or using a timed voice draft.
Leave room for reactions, comprehension, action completion, and intentional silence.
Use this reusable table; add rows for the actual story rather than filling every cell with a new shot:

| Time in–out | Beat and causal change | Visible action / shot scale | Narration or dialogue | Sound / caption cue | Continuity / asset need |
|---|---|---|---|---|---|
| Planned interval | What changes and why the next beat follows | Subject action, framing, and cut point | Exact line or purposeful silence | Intended sound and readable text | State to preserve and material required |

Give every planned shot a job: establish, reveal, demonstrate, react, or connect.
Remove shots that repeat information without changing understanding or feeling.
Include title cards, transitions, credits, and any opening or closing silence in the same timeline.
Treat timings as hypotheses to test, not evidence that the pace works.

## 5. Review a complete timed rough cut

Build the entire timeline with stills, sketches, existing footage, or other low-cost stand-ins.
Include intended narration, dialogue, music, sound cues, caption placement, title cards, and transitions at their planned times.
Use temporary audio when necessary and label substitutions that could affect the judgment.
Watch from beginning to end without pausing, then annotate specific timestamps.
Ask where attention drops, where a line outruns comprehension, and where a visual fails to support its beat.
Revise content, pauses, ordering, and cuts before commissioning or generating expensive motion.

A still rough cut can test timing, narration, captions, music, and transitions.
It cannot establish acting quality, physical continuity in motion, or whether final generated subjects actually perform.
Keep those unresolved checks explicit; do not mark the film accepted because the rough cut feels promising.

## 6. Produce only the motion the approved cut needs

Make a shot-level production list from the revised timeline, reusing suitable material where rights allow.
For generated footage, describe the subject's action, prop interaction, setting, light, framing, and required starting and ending states.
Camera movement may support the action, but a pan or push over a still subject does not prove the subject acts.
Inspect each selected clip for the intended action, believable interaction, identity consistency, and usable cut points.
Reject or repair a shot that contradicts the beat, even if it looks polished.
Update the continuity ledger when a production constraint changes an established fact.
Revisit the rough cut if the replacement changes timing or meaning.

## 7. Assemble and review the actual export

Conform the full timeline, mix speech and sound for intelligibility, and retain intentional pauses.
Place final title cards before synchronizing captions, then recheck caption timing across all later offsets.
Check text accuracy, readable duration, safe placement, and collisions with visual information.
Play the complete exported file in a suitable player, including its opening, transitions, and ending.

Keep two review records with evidence appropriate to each:

- **Technical:** measured duration, frame size, playback, audio continuity, caption synchronization, and requested delivery specifications. Name the tool or manual probe actually used.
- **Editorial:** causal clarity, action, performance, pacing, continuity, sound choices, and whether the landing earns its effect. Cite viewing timestamps and the observed issue.

A technical pass cannot establish a strong story, and an editorial preference cannot substitute for a missing playback check.
If a tool is unavailable, record the check as unperformed rather than inventing a result.

## Stop rule and final deliverables

Finish when the complete export meets the brief, required checks have evidence, and no unresolved defect prevents the intended viewing experience.
Revise against a named defect and a predicted improvement; stop speculative generation when review identifies no further necessary change.
If the approved resources are exhausted first, deliver the best reviewed version with its exact shortfalls and the next decision required.

Final checklist:

- Creative brief and acceptance criteria.
- Causal beat plan, timed shot plan, and continuity ledger.
- Reviewed full rough cut with the limits of stand-ins recorded.
- Final export with captions and any requested supporting files.
- Separate technical results and editorial viewing notes, including unresolved issues.
- Rights, consent, and budget gaps resolved or clearly identified; delivery and publication status stated accurately.
