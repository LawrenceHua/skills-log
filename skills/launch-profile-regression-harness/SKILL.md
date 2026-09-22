---
name: launch-profile-regression-harness
description: For a CLI/TUI tool with multiple named launch profiles or config variants, actually boot each one in a real pseudo-terminal and assert it starts cleanly, instead of only statically linting config — run it as a scheduled, stripped-environment background watcher so a broken profile is caught between sessions.
---

# launch-profile-regression-harness

Static config linting catches malformed syntax but not a profile that parses fine and still fails to boot — a theme file that loads but breaks the renderer, a plugin/skill that's structurally valid JSON but crashes on init, a launch flag combination nobody tested together. The only check that actually catches this class of bug is starting the thing and watching what happens, so this method wraps every named launch profile in a real smoke test instead of trusting that "the config parsed" means "the tool works."

## The method

**1. Enumerate every named launch profile or config variant the tool supports** — the default, plus every custom theme/persona/feature-flag combination you maintain. Each one is a separate thing that can break independently of the others.

**2. Boot each profile in a real pseudo-terminal (PTY) for a short, bounded window.** A PTY-based launch (not just invoking the binary with output piped to a file) is what exposes TUI-specific failures — a renderer that only crashes when it detects an interactive terminal, a status line that throws on a missing terminal capability. Assert: no fatal error on stderr, the process reaches an interactive-ready state within a timeout, and it exits cleanly when signaled to stop.

**3. Layer checks from cheap to expensive.** Run them in this order so a fast failure doesn't wait on a slow one: strict config-schema validation (fail loudly on unknown/malformed keys), theme/style file parsing, launcher script syntax, structural validation of installed extensions/plugins/skills, then the PTY boot smoke-test per profile.

**4. Separate hard failures from soft findings.** A profile that won't boot, or a config that fails to parse, is a hard failure that blocks. Output from the tool's own built-in health/doctor command is useful context but should surface as a warning, not a blocker, unless it corresponds to one of your own hard CLI-surface checks — a health command's opinions and your regression harness's pass/fail criteria are not the same contract.

**5. Run it on a schedule, not just on demand.** A human only launches the profile they use daily; the one used twice a month is exactly the one that silently breaks and stays broken for weeks. A periodic background run (every N minutes, or on every config-file change) catches regressions between sessions instead of at the next inconvenient moment.

**6. Strip the watcher's environment.** The interactive shell you launch profiles from normally carries your full environment, and that's expected. The background watcher process should not — launch it through a minimal environment allowlist (only what the tool truly needs to start, like a home/config-root variable) so a scheduled regression check never becomes a second place your shell's ambient secrets and tokens are loaded into memory.

**7. Keep new profiles and the harness itself additive.** Ship alternate launch profiles and the regression harness as new wrapper scripts and new config files, not edits to the tool's core/default config. A broken experimental profile should never be able to take down the default launch path, and the harness should be removable without touching anything else.

## When to use

- You maintain more than one launch profile, theme, or config variant for a CLI/TUI tool and want confidence that a config change didn't silently break one of them.
- Setting up a background watcher for a developer tool's health, where you want boot-time failures caught automatically instead of at the next manual launch.
- Reviewing an existing "lint the config" check that has never actually caught a boot-time failure, to see whether it's missing the PTY-smoke-test layer entirely.

## How to use

**Install:** copy this folder into `~/.claude/skills/launch-profile-regression-harness/` for personal use, or `.claude/skills/launch-profile-regression-harness/` inside a project repo. Point the harness at whichever CLI/TUI tool and profile set you actually maintain — the layered-checks-then-PTY-boot structure is the same regardless of tool.

**Invoke:**

```
Build a launch-profile-regression-harness for my CLI tool's launch profiles —
config validation, theme parsing, then a PTY boot smoke-test for each profile,
runnable both on demand and as a scheduled watcher.
```

```
Audit my terminal tool's existing health check against launch-profile-regression-harness:
does it actually boot each launch profile in a PTY, or does it only lint the config?
```
