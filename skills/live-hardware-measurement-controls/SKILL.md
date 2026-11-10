---
name: live-hardware-measurement-controls
description: Measure a physical device or live system without fooling yourself: name the reference, prove the positive control, treat all-rejected runs as null, allow one actor, subtract starved windows, label whose clock made the number.
---

# Live hardware measurement controls

Gates on real devices tend to fail in six ways: a green that could not fail, a fail that could not pass, a
null counted as a pass, a rate that described a synthetic input, a latency that measured the harness, and a
comparison against a value the builder chose. These rules are what those failures buy. Load them before you
quote any number about a device.

## Rules, each with the failure that produced it

1. **Name the reference; never compare to a value the builder chose.**
   A regression is only visible if the previous release was measured the same way. Prefer, in order: the
   previous release on the same device, a device-side counter, the server's own transport log. "Expected
   200 ms" written by the builder is a wish.

2. **A gate whose positive control fails decides nothing.**
   Example: a button gate returned 4/8 while its wake-path control never triggered, because the test audio
   arrived 5 dB above the noise floor, not enough margin. Fix the control, prove the positive path N out of
   N, then judge the path under test. Print the control's level every run.

3. **A null result is not a pass.**
   A 15-minute walk through a menu ran hundreds of gestures and every one was rejected on stale names; it
   would have printed "0 crashes" as green. Every harness prints its accepted/rejected split, and
   `rejected == attempts` is a null.

4. **Two actors on one device destroy the result.**
   Before flashing, pressing or starting a window, confirm no other process or lane holds it:
   ```sh
   pgrep -fl <your-harness-name>          # expect empty
   ls -t <ops-log-dir> | head -3          # expect no fresh run from another lane
   ```
   A second actor once auto-installed firmware mid-gate and invalidated the window.

5. **A starved detector looks exactly like a miss.**
   Count only windows where the starvation counter did not move. If starvation happens mainly at connect
   time, a "missed detection" during a connect is a scheduling effect, not a detector failure. Say which.

6. **A harness clock is not a device clock; name which produced the number.**
   Device event records carry their own timestamps and sequence numbers; harness latency columns lie when
   the event endpoint blocks or the ring buffer truncates. A "latency" of detection-to-listening is not
   press-to-acknowledge. Label the clock.

7. **Prove the gate can fail before trusting a green.**
   Run the failing shape on purpose: the old release, a stale bound, the wrong sentence. Keep negative
   controls in the script as a self-test mode, not in the prose.

8. **An empty counter is not a zero.**
   A sentinel such as -1 means "no samples". `no_data`, `unreadable` and `filtered` are three different
   outcomes; say which one an empty result is.

9. **Do not normalise on an ambiguous verb.** If the device says `created:false`, report that, not
   "registered successfully".

10. **Qualify synthetic figures.** A press-acknowledge time measured by a software-triggered request over
    the LAN is a round trip on the harness clock, its population includes rejected presses, and it may pool
    several builds. Quote it only with those qualifiers. "How fast it feels" needs a human or a high-speed
    capture; if neither was done, write `UNKNOWN`.

## The loop

```
capture turns -> per-session report -> gap harvest -> ranked optimisation list
   -> build -> measure on the device again -> capture turns
```

Make the capture step append-only and the report step read-only; a report command that writes is a bug.
Declare budgets on the report command (for example an acknowledge budget in ms), because a budget is a
declared reference, not a value harvested from the device.

## Which counter answers which question

| Question | Counter | Trap |
|---|---|---|
| Alive, and where in its state machine | diagnostics `fw`, `state`, `uptime` | a state with a menu open is not "ready" |
| Did the button get through | applied vs rejected counters | rejected is not dropped; label which |
| Did a detection happen | detection windows, fail count, last phrase | subtract starved windows first |
| Is the room loud enough | peak level vs floor level | a 5 dB margin is not a control |
| Did a fix hold | the previous release's number, same harness | never the builder's target |

## Reporting

- One line per claim: number, reference, command that re-derives it.
- Use VERIFIED, CODE-SHIPPED-NOT-VERIFIED, BLOCKED or INCONCLUSIVE verbatim. A percentage from one voice,
  one run or one unguarded window is INCONCLUSIVE.
- When a gate cannot run, name the missing fact. That is BLOCKED, not a failure.
- End every measurement with a diagnostics readout and leave the device in a known baseline state.
- Store the raw receipt file, not a summary of it.

## When to use

- Deciding whether a firmware fix worked, or whether a device is release-ready.
- Quoting a wake rate, latency, button result or stress-test result.
- Writing or reviewing a hardware regression gate.

## How to use

1. Copy this folder into `~/.claude/skills/` (personal use) or `.claude/skills/` inside a project.
2. Ask Claude Code to use the `live-hardware-measurement-controls` skill by name.

Example prompts:

- "Use live-hardware-measurement-controls to audit this button-latency script: what is its reference, and
  can it fail?"
- "Use live-hardware-measurement-controls to rewrite my report so each number carries its reference and
  re-derivation command."
