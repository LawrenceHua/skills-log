---
name: generated-media-qa-probes
description: Objective, self-tested checks for AI-generated video clips and voice takes before a human reviews them: real motion vs camera push, image-to-video conditioning, true detail vs upscale, voice similarity, and caption timing.
---

# Generated media QA probes

Five small measurements that answer the questions a reviewer would otherwise answer by eyeballing: *is it actually moving, did it start from my image, is the detail real, does the voice match, are the captions timed?* This skill measures; it never invents a pass threshold. Thresholds belong to the gate of the project that calls the probe.

## 0. The rule that makes any probe worth running

Run every probe on a **synthetic known-positive and a known-negative** first. A probe that reads about zero for everything proves nothing; a probe that reads noise as signal proves the opposite. Build the pair from a real still: one clip that is a pure camera zoom/pan over the still (motion must read ~0), one clip where only a subject region moves (motion must read high). If the negative does not collapse or the positive does, the probe is broken. Copy this habit for every new probe you add.

## 1. Motion: moving, or just a camera push over a still?

Total optical flow is misleading: a slow zoom over a frozen frame scores high.

1. Sample frames at a fixed rate (for example 8 fps) and compute dense optical flow (Farneback) between consecutive frames.
2. Per frame pair, take the mean of the **top 5 percent** of flow magnitudes (pixels). Scale your bar by frame size (for example `6.0 * min(H, W) / 256` px).
3. Estimate a global camera model between the same two frames from tracked corners (partial-affine fit with RANSAC), warp the earlier frame by it, and re-measure flow. The residual is the **compensated** motion.
4. Judge on the compensated number. Treat the uncompensated total as a diagnostic only.

Expected self-test shape: camera-only clip total ~2.5 px but compensated ~0.15 px; subject-only clip compensated ~ its total (~6.5 px). Numbers will differ by resolution; the *collapse* is what you check.

## 2. Image-to-video: did the clip start from the supplied still?

Motion proves "not frozen", not "image-conditioned": a pipeline that ignores its input image still moves.

1. Take frame 0 of the clip.
2. Compare it to the conditioning still **and** to a decoy (another still from the same shoot or style) with SSIM, PSNR and normalized cross-correlation, after resizing to one common size.
3. Pass only if the real still beats the decoy by a clear margin (for example SSIM gap > 0.05). Otherwise the verdict is NOT PROVEN, never "probably fine".
4. Self-test by swapping the two stills: the verdict must flip to NOT PROVEN.

## 3. Detail: real pixels or upscale mush?

Sharpness metrics (Laplacian variance) are not comparable across resolutions; a bigger canvas raises them.

1. Rescale every clip to **one delivery geometry** (for example 1080x1920) before measuring.
2. Compute the radially averaged power spectrum of sampled frames. Define a cutoff frequency as the highest radial frequency still within ~40 dB of the low-frequency plateau.
3. An upscale cannot carry energy above `source_width / canvas_width / 2` cycles per pixel. A clip whose cutoff sits near its own ceiling had real pixels; one far below it is soft.
4. Only compare clips measured at the same geometry.

## 4. Voice take: does it sound like the reference?

1. Transcribe the take with a speech model **without** prompting it with the expected script (prompting hides errors). Keep word times.
2. Compute speaker-embedding cosine similarity between the take and a clean reference recording (skip any throwaway carrier word at the start).
3. Check peak level in dBFS, count clipped samples (|x| at full scale), and flag isolated clicks (a sample-to-sample step above ~0.12 where samples a dozen positions before and after are both quiet). Clicks are flags to listen to, not a verdict.
4. Normalize numerals before comparing transcripts to the script ("1,600" vs "sixteen hundred") or word-error rate will lie.

## 5. Captions: forced word alignment

Align the **script's own tokens** to the audio (cross-attention plus DTW word timestamps from a speech model). Use the result for caption timing only. Never use forced-alignment text as a transcript for error-rate scoring, and never fill gaps with interpolated word times: a missing time is a finding.

## Environments

Probes 1-3 need only OpenCV, numpy and ffmpeg. Probes 4-5 need a speech-recognition model and a speaker-embedding model. Pin versions in a requirements file and rebuild the environment once from scratch to confirm the self-test numbers reproduce.

## Never

- Never call a clip moving because total flow is high; read the compensated residual.
- Never trust a probe that has not read a known-positive and a known-negative.
- Never call a clip image-to-video because it moves; run the decoy test.
- Never prompt the recognizer with the expected script when scoring a take.
- Never compare sharpness numbers across resolutions.
- Never score words by string equality across numerals, or treat click candidates as a verdict.
- Never invent a pass threshold; take it from the project's gate.

## When to use

- Gating or comparing AI-generated video or narration before human review.
- Someone asks "is this clip frozen?", "did the image-to-video model follow my image?", "does this voice take match the reference?", or "align captions to the audio".
- Writing a QA gate for a reel, short film or voiceover pipeline.

## How to use

1. Copy this folder into `~/.claude/skills/` (personal) or `.claude/skills/` inside a project, then ask Claude Code to use `generated-media-qa-probes` by name.
2. Ask it to write the small scripts for the probes you need and to run the known-positive/known-negative self-test first.

Example prompts:
- "Use generated-media-qa-probes to check whether `clip.mp4` is really moving or just a slow zoom, and show me the self-test results first."
- "Use generated-media-qa-probes to prove `clip.mp4` was conditioned on `still.png` rather than `other.png`."
