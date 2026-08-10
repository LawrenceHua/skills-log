---
name: multi-cli-constitution
description: Keep multiple AI coding CLIs (Claude Code, Codex, Kimi, Cursor, etc.) behaviorally consistent by pointing them all at one shared "constitution" file — a capability routing table, polyfill recipes for missing features, and a compiled policy block injected identically into each tool's config — so the quality bar can't drift between tools.
---

# multi-cli-constitution

The moment you run a second AI CLI, your rules start forking: one tool knows
your verification vocabulary, the other doesn't; one has the house rule about
never force-pushing, the other cheerfully force-pushes. Copy-pasting rules
between config files guarantees drift. The fix is the same one codebases use:
a single source of truth, and generated copies that are never hand-edited.

## The three pieces

### 1. One constitution file

A single `~/.agents/AGENTS.md` (or wherever) that every CLI is pointed at —
most CLIs support either reading a shared instructions path natively or a
one-line pointer from their own config ("read ~/.agents/AGENTS.md before
substantial work"). It holds what must be identical everywhere:

- The **verification vocabulary** (see `verification-labels`) so every tool's
  "done" means the same thing.
- **House rules**: no git mutations unless asked, no force-push, how to handle
  secrets, when to stop and ask.
- The **capability routing table** and **model lanes** (below).

### 2. A capability routing table, not vendor loyalty

Route work to whichever CLI *natively has the feature the task needs*, with a
named fallback:

| Capability | Route to | Fallback |
|---|---|---|
| OS-level sandboxing | the CLI that has it | containerize + the others |
| Goal loop with budgets ("run until X") | the CLI with native goal mode | a GOAL.md file the agent re-reads each turn |
| Very long context (whole-repo judging) | the long-context CLI | chunk + map-reduce |
| Mass parallel fan-out | the CLI with native swarms | N parallel subprocess invocations + an aggregation pass |
| Scheduled/cron runs | the CLI with native scheduling | OS scheduler (launchd/systemd/cron) invoking headless mode |

The **polyfill column is the point**: for every capability, write down the
recipe for faking it in the tools that lack it. A missing native feature then
never blocks work — it just costs a polyfill.

### 3. A compiled policy block

For rules that must live *inside* each tool's own config file, don't hand-copy.
Keep one canonical policy source, and a tiny script that compiles it into a
marker-delimited block:

```
<!-- estate-policy:start (generated — do not hand-edit) -->
...identical text in every CLI's config...
<!-- estate-policy:end -->
```

Re-run the compiler after any policy change; diff the blocks across tools in
CI or a scheduled check to catch drift.

## Hard-won details

- **Date and sign config decisions inline.** When you downgrade a default
  (e.g. reasoning effort from max to high for cost), leave a dated comment in
  the config saying why — future-you will otherwise "fix" it back.
- **Cross-tool file locking.** Two CLIs editing one repo concurrently will
  trample each other. A simple lease file keyed by the repo's git origin (not
  the checkout path — worktrees break that) lets each tool claim a workspace
  and warn the others.
- **Shared subagent personas.** Keep verifier/reviewer agent definitions (see
  this repo's `agents/`) in the shared directory too, so every CLI fans out to
  the same bench.

## When to use

- The day you add a second AI CLI.
- After any incident where two tools behaved differently on the same rule.
- As the home for rules you find yourself pasting into more than one config.

**Skip it for:** single-CLI setups — one well-maintained instructions file is
already your constitution.

## How to use

**Install:** copy this folder into `~/.claude/skills/multi-cli-constitution/`.
Then create your own `~/.agents/AGENTS.md` with the three pieces above and add
a pointer line to each CLI's config.

**Invoke:**

```
Using the multi-cli-constitution skill: draft my ~/.agents/AGENTS.md from the
rules currently scattered across [list your CLI config files], build the
capability routing table for the tools I have, and flag every rule that
currently exists in one tool but not the others.
```
