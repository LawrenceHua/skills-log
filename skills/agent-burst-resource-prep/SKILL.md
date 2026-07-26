---
name: agent-burst-resource-prep
description: A pre-flight routine that frees RAM and drops memory pressure on your machine so it can safely run a larger batch of parallel AI-agent sessions than usual, then restores normal state afterward.
---

# agent-burst-resource-prep

Running many AI-agent sessions in parallel (a big fan-out review, a large migration, a multi-agent workflow) is RAM-hungry. Whatever safe concurrency limit you normally run at assumes headroom for your machine's other background processes. Push past that limit without preparing for it and you get swapping and thrashing — the burst runs slower than if you'd stayed at the lower concurrency, not faster. This is a short, reversible routine to run immediately before a big fan-out, and reverse immediately after.

## The method

Three things, done together, then undone together:

### 1. Pause your own known RAM-hungry background helpers

Keep an explicit list of the background processes on your machine that are safe to pause for the duration of a burst — chatty pollers, periodic sync jobs, notification loops, anything that isn't in the critical path of the burst itself. Pause them (not kill — you want a clean resume), run the burst, then resume them.

Keep an equally explicit **never-touch list**: anything the burst itself depends on to actually run (your agent runtime/gateway process, safety watchdogs, a local model server if you use one, any human-approval worker in the loop). Confusing these two lists is the main way this kind of script causes an outage instead of preventing one.

### 2. Drop OS-level memory pressure

On macOS, running the built-in memory-pressure-relief command (`purge`, needs `sudo`) forces the compressor to release RAM it's holding for cached-but-idle pages. On Linux, the equivalent is dropping the page cache (`sync; echo 1 > /proc/sys/vm/drop_caches`, also needs root) or simply closing memory-heavy foreground apps. If you don't have passwordless sudo configured for this, skip the step rather than blocking the rest of the routine on it — pausing background helpers alone still buys real headroom.

### 3. Raise your own concurrency ceiling, if you gate it

If you already have something that caps how many agent sessions you'll run at once (a wrapper script, a queue, a simple counter), make the higher ceiling conditional on an explicit flag — a single file whose presence means "burst mode is on, allow the higher number." Anything that reads the flag should default to the lower, safe number when the flag is absent, never the other way around.

## A minimal script shape

```
agent-burst.sh on
  → pause each process in the pausable list
  → attempt the OS memory-pressure drop (skip silently if it fails)
  → write the burst-mode flag file

agent-burst.sh off
  → resume each paused process
  → remove the burst-mode flag file

agent-burst.sh status
  → report: flag present? which processes are currently paused?
```

Keep `on` idempotent (running it twice shouldn't double-pause anything) and make `off` the unconditional safe path — it should always fully restore state even if `on` only partially completed.

## Smoke test

```
agent-burst.sh status     # confirm OFF
agent-burst.sh on         # confirm ON: processes paused, memory dropped (or skipped), flag file exists
agent-burst.sh status     # confirm ON
agent-burst.sh off        # confirm OFF: processes resumed, flag file gone
```

## Rollback

If pausing something turns out to break a workflow you needed running, just run `off` — it should always fully restore. If the OS memory-pressure step is denied (no passwordless privilege), the routine should still proceed with the process-pause and flag-write steps; only the compressor drop is skipped.

## When to use

- Right before spawning a fan-out of parallel AI-agent sessions larger than your machine's normal safe concurrency.
- When you've noticed a large parallel run swapping or slowing down rather than speeding up.
- As a standing habit before any workflow you know is agent-count-heavy (a broad multi-file migration, a large adversarial-review panel, a big research sweep).

Turn it back off as soon as the burst finishes — this is a temporary state, not a new normal.

## How to use

**Install:** copy this folder into `~/.claude/skills/agent-burst-resource-prep/` for personal use, or `.claude/skills/agent-burst-resource-prep/` inside a project repo, then ask your assistant to use the skill by name.

**Invoke:**

```
Use agent-burst-resource-prep to help me write an on/off/status script for my
machine. I want to pause my sync daemon and my notification poller during a
burst, but never touch my agent runtime or my local model server. Ask me
which processes are safe to pause before writing anything.
```

```
I'm about to run a 15-way parallel agent review and my machine only
comfortably handles 8 at once normally. Walk me through agent-burst-resource-prep
before I kick it off, then remind me to turn it back off when it's done.
```
