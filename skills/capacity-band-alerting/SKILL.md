---
name: capacity-band-alerting
description: Alert on low disk or other shrinking capacity using named bands with hysteresis and a time-to-floor forecast, so owners hear about real decline without a message for every wobble across a threshold.
---

# Capacity band alerting

Free disk space can move by several gigabytes an hour on a busy machine. An alert at every threshold crossing gets muted. Silence while space drifts toward zero is worse. The same applies to other capacity that runs out, such as inodes, queue room or prepaid credit.

## Inputs

- A band table, for example free space thresholds of 50, 30, 20 and 10 GiB, with the lowest named as the stop floor. Size yours to the volume and its normal swings.
- A margin for leaving a band.
- Saved state: the current band, the last alert's band, time and forecast, and any acknowledgement.
- Recent readings with timestamps: at least five, and preferably enough to cover a full day.

## Steps

1. **Read live.** Record free and used space for each relevant volume, in consistent units. Volumes that share one pool may report the same free space. Do not add it twice.
2. **Place the reading in a band with hysteresis.** Move to a worse band as soon as free space falls below its threshold. Move back only when it rises above that threshold plus the margin, such as the larger of 3 GiB or 15% of the threshold. Apply this rule across several bands if a reading jumps. The stop floor follows the same rule: you are in it until free space rises above the floor plus the margin.
3. **Estimate the trend.** Smooth single spikes with a three-reading median, then fit a slope per hour. Keep the newest raw reading as the current value. After a large step, such as a cleanup or a big download, report the step and start a new trend window once you have enough readings.
4. **Forecast.** Only when the slope shows decline: hours to floor is (current free minus floor) divided by the rate of decline. Report hours to zero the same way. With too few readings or a very uneven series, say "no forecast".
5. **Decide.**

| Situation | Action |
|---|---|
| in the stop floor band | alert on entry, then repeat at a set short interval |
| band worse than before | alert |
| under a day to floor or two days to zero, with no forecast alert yet for this decline | alert with the forecast |
| same or better band, with no new forecast crossing | log only, unless the stop floor row applies |
| recovered two or more bands | mention once in the next routine summary |

An acknowledgement pauses stop floor repeats for a set period, or until free space falls by another margin, whichever comes first. Repeats then resume while the volume is still in that band.

If a band bounces back and worsens again, send at most one alert for that band per 24 hours, unless the forecast has clearly shortened. This limit does not apply to stop floor repeats.

6. **Name the owner and the next decision.** Say who may free or add capacity and what approval it needs.
7. **Log every run:** reading, band, slope, forecast, decision and what was sent. Mark an alert as sent only after delivery succeeds.

## Output

- Quiet run: one log line.
- Alert: current value and read time, band, trend, forecast, owner and the one decision needed.

## Stop rules

- If a reading is unavailable, record that. Do not alert on or forecast from stale numbers as if they were current. Report the loss of readings through its own alert if it continues.
- Triage is read-only. Do not delete, move or compress files, purge caches or kill processes.

## Check the alerting itself

- Replay a recorded series: bouncing at one threshold above the floor should give one band alert, and a steady decline should alert before the floor.
- Replay a decline that is acknowledged at the floor and keeps falling. It must alert again.
- Later, compare forecasts with what happened. Record large misses and adjust the window or margin.

## When to use

- A disk or capacity monitor alerts so often that people ignore it.
- A volume filled up although each individual reading looked tolerable.
- You are writing a scheduled capacity check.

## How to use

1. Copy the `capacity-band-alerting` folder into `~/.claude/skills/` for personal use, or `.claude/skills/` inside a project.
2. Ask Claude Code to use the skill by name.
3. Example prompts:
   - "Use the capacity-band-alerting skill to rewrite my low-disk cron check. Include a replay test with a series that bounces around one threshold."
   - "Use capacity-band-alerting on these free-space readings and tell me whether this deserves an alert."
