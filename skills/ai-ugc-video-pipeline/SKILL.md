---
name: ai-ugc-video-pipeline
description: A hardened, gated pipeline for producing short-form AI-generated "UGC-style" marketing video with a consented identity-locked presenter, real product footage, and word-pop captions — with hard-won fixes for the media-validation, audio-sync, and judge-hallucination traps that make these pipelines silently ship broken output.
---

# ai-ugc-video-pipeline

Short-form AI-presenter marketing video (talking-head + real product footage + captions) has a specific set of failure modes that don't show up until you actually play the final file on a real device — not in ffprobe, not in a script that seeks around the timeline. This is a gated pipeline that catches them before delivery, plus the two audio bugs that are easy to reintroduce even once you know about them.

## When to use

- Producing a short-form (vertical, 9:16) AI-presenter product/marketing video.
- Re-cutting or iterating an existing one.
- Any pipeline that assembles AI-generated talking-head footage + real screen capture + generated captions via ffmpeg.

## Non-negotiable phase order — each phase gates the next

1. **PREP (spend nothing until this is green).** Research the current model landscape for your presenter/voice generation (pricing and endpoints for these APIs move monthly — verify against the live provider docs before committing spend). Write a few script variants, have a text judge pick one, stage your face/voice reference material (with real, documented consent for the identity being used), capture the real product footage you'll composite in, and write a rubric plus a hard budget cap before spending a cent.
2. **CALIBRATE.** Generate one short, cheap clip first to validate framing and identity acceptance before committing to full-length takes. If framing is wrong, fix the *reference image* you're feeding the model, not the model choice.
3. **GENERATE.** Minimal, deliberate takes. Only A/B between providers/models when you have evidence one is underperforming — don't shotgun requests. Stop generating once scores plateau; cap paid iterations (e.g. stop after 2 unless scores are still trending up).
4. **ASSEMBLE.** Use ffmpeg's **concat filter**, not the demuxer, for the final assembly (see the audio bugs below for why). Every rebuild gets a new filename — never overwrite in place, so you can always diff against the last good version.
5. **VERIFY.** Run your media-validation gates (below) and a text/honesty preflight on every script/caption/copy asset. No delivery on any failing gate.
6. **DELIVER.** Hand the file to a human for final approval, with a short ratings/notes doc. Posting to any platform is always a human-gated decision — never auto-post. If the presenter is a realistic synthetic likeness, use the platform's AI-content disclosure toggle even when in-video disclosure is a deliberate choice you've made separately.

## The two audio bugs that will ship silently if you don't guard for them

1. **A segment's audio track is shorter than its video track** (voiceover ends before the video clip does). In a stream-copy concat, the audio timeline slips and effectively dies early partway through the final file. **Fix:** pad every segment's audio to match its video length, and normalize every segment to the same sample rate/channel count before concatenating.
2. **Even with padding, the concat *demuxer* can leave tiny (~0.1s) packet-timing gaps** from audio-duration rounding. Tools that decode straight through (ffmpeg, a transcription tool) play through these gaps fine and won't flag anything — but some real players stop audio dead at the first gap, so a file that "passes" your automated check can still be broken for an actual viewer. **Fix:** do the final assembly as a single-pass concat *filter* (not the demuxer) with audio resampling forced to a continuous, gapless timeline.

**The probe that catches both:** scan the final file's audio packet timestamps for any gap larger than ~50ms. Validate media the way a real player consumes it — a continuous decode + a full-file transcript — not by seeking to timestamps and sampling, which can silently auto-resync around exactly the gap you're trying to catch.

## Judge protocol — LLM judges hallucinate on media, cross-check them

- Score against a fixed, moderate compression proxy (too-aggressive compression exaggerates artifacts and skews scores against the format, not the content).
- **Cross-check every judge claim about audio against a deterministic probe** (a transcript + the packet-gap scan above) before acting on it. A judge calling something "a glitch" can be right OR wrong for the wrong reason — don't trust or dismiss it on vibes; run the deterministic check first, then decide.
- For A/B comparisons: same audio track, pinned/fixed criteria, consistent ordering, and force strict structured output — free-text judge opinions are harder to act on and easier to rationalize away.
- Expect a judge to be harsh. Ship on evidence (every deterministic gate green + an actual human's approval), never on a judge's verdict alone.

## Honesty & safety gates — encode these as code, not as a vibe check

Run an automated preflight over every script/caption/copy asset before it ships:
- No fabricated claims about the product's capabilities or results.
- No unconsented use of anyone's face or voice — get and document real consent before generating with any real person's likeness, and check the generation provider's own usage policy for identity-based generation.
- No claims presented as real user outcomes that were actually generated/simulated.
- Any brand or product names that shouldn't be public stay out of scripts, captions, and the posting notes.
- Posting itself is always a separate, human-gated step — the pipeline's job ends at "ready for review," never "published."

## Budget discipline

Keep a running ledger (estimate vs. actual per generation) against a hard cap you set in PREP, and stop generating once scores plateau rather than continuing to spend past diminishing returns. Budgeting up front, and stopping on evidence rather than on "just one more take," is what keeps this pipeline affordable.

## How to use

**Install:** copy this folder into `~/.claude/skills/ai-ugc-video-pipeline/` for personal use, or `.claude/skills/ai-ugc-video-pipeline/` inside a project repo. You'll wire in your own choice of presenter/voice-generation provider and screen-capture tooling — this skill is the gating methodology and the hard-won failure-mode fixes, not a specific vendor integration.

**Invoke:**

```
Walk me through the ai-ugc-video-pipeline PREP phase for a 30-second product
demo video — help me write the script variants and the budget ledger before we
generate anything.
```

```
My assembled video has audio that cuts out partway through in some players but
plays fine in ffplay. Use ai-ugc-video-pipeline's audio-bug section to diagnose
and fix it.
```
