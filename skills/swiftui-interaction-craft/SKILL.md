---
name: swiftui-interaction-craft
description: Build or review SwiftUI screens for iOS 26 with restrained Liquid Glass, interruptible spring motion, haptics tied to real state changes, accessibility fallbacks and measured main-thread performance.
---

# SwiftUI interaction craft

A polished screen comes from restraint and proof. Glass belongs in the right layer, motion responds to the hand, haptics mean something and nothing stalls the interface. The numbers below are starting points. Check current Apple documentation for API availability and behavior.

## 1. Liquid Glass and hierarchy

- Prefer standard bars, sheets, tab views and controls. Built with the iOS 26 SDK, many adopt the new material without custom code.
- Use custom `.glassEffect()` for floating controls and navigation. Keep it off scrolling content cards, dense tables and other places where text must stay easy to read.
- Group nearby custom glass shapes in a `GlassEffectContainer`. Do not stack glass on glass.
- Put custom code behind `if #available(iOS 26, *)` when you support earlier versions, with a solid or material fallback.
- Over photos or camera views, add a gradient or dimming layer behind text.
- Test with Reduce Transparency and Increase Contrast on. For custom surfaces, read `accessibilityReduceTransparency` and `colorSchemeContrast` from the environment and adapt.

## 2. Layout and access

- Give controls a touch target of at least 44 by 44 points. For a small icon, enlarge the frame inside the button label, then apply `.contentShape(Rectangle())`. The shape alone does not make a small frame bigger.
- Use text styles or scaled fonts. Check the largest accessibility text sizes, and switch to a vertical layout with `ViewThatFits` or a size-category check where needed.
- Give icon-only controls accessibility labels. Walk the main task with VoiceOver and check the reading order.

## 3. Motion and gestures

- Starting springs: `.spring(response: 0.32, dampingFraction: 0.86)` for cards and state changes, and `response: 0.22, dampingFraction: 0.90` for small toggles. Tune on a device.
- Let people interrupt. Do not disable input while an animation settles.
- On release from a drag, carry the gesture's speed into the settling motion. If you pass an initial velocity to an interpolating spring, check which units it expects.
- When `accessibilityReduceMotion` is on, replace large slides, zooms and parallax with a short cross-fade or no animation.

## 4. Haptics

Use `.sensoryFeedback(_:trigger:)` (iOS 17 and later) and bind the trigger to a real state change.

| Event | Typical feedback |
|---|---|
| picker or filter value changes | selection |
| a save or scan is confirmed | success |
| something needs caution | warning |
| an operation fails | error |

Do not fire on scrolling, on redraws or for an optimistic action that has not been confirmed. Never make a haptic the only signal.

## 5. Performance

- Frame budgets are about 8.3 ms at 120 Hz and 16.7 ms at 60 Hz. The app shares that time with the system.
- Move image decoding, model inference, parsing and storage work off the main actor. A plain `Task {}` created in main-actor code inherits that actor, so wrapping work in it does not move it. Use a separate actor or a function that is explicitly run concurrently. Check your Swift version and concurrency settings.
- Limit how often live data, such as a camera overlay, updates view state. Ten to fifteen times a second is a reasonable first limit for text readouts.
- Keep launch light. Defer analytics, model warm-up and remote configuration until after the first screen appears. Set a launch target and measure it.
- Measure a release build on a physical device with Instruments. A simulator run does not prove smoothness.

## 6. Verification

Record a result for each:

1. Build and tests pass.
2. Screens checked in light, dark and large text.
3. Reduce Motion, Reduce Transparency and Increase Contrast each checked.
4. VoiceOver pass on the main task.
5. Haptics felt on a physical device.
6. Instruments trace showing hitches and main-thread stalls.

Mark anything not run as not verified. Uploading to testers or submitting for review is a separate step that needs the account owner's approval.

## Never

- Never put glass over primary content where it lowers readability.
- Never block the main actor with file, network or model work.
- Never claim a frame rate that you did not measure on hardware.

## When to use

- You are building or polishing a SwiftUI screen for iOS 26.
- Motion feels stiff, haptics feel random or scrolling hitches.
- You are reviewing interface code before a test release.

## How to use

1. Copy the `swiftui-interaction-craft` folder into `~/.claude/skills/` for personal use, or `.claude/skills/` inside a project.
2. Ask Claude Code to use the skill by name.
3. Example prompts:
   - "Use the swiftui-interaction-craft skill to review this scanning screen. List problems by section and say which checks need a physical device."
   - "Use swiftui-interaction-craft to add a floating action bar with an earlier-iOS fallback and Reduce Motion support."
