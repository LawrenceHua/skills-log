---
name: deletion-safety-gate
description: Before deleting a worktree, clone, cache, or "stale" build directory, run a fail-closed reference check that screens loaded scheduled jobs, on-disk job definitions, crontab, config/script path fields, running processes, and shared git object stores for the path — SAFE only if every screen completes and finds zero references.
---

# deletion-safety-gate

Clean git history (`git status --porcelain` empty, nothing unpushed, a recovery ref recorded) proves a directory's *history* is safe to lose. It proves nothing about whether the *path* is still referenced somewhere that runs on a schedule. A directory can be a perfectly clean, fully-pushed git checkout and still be the working directory a scheduled job launches out of every hour — deleting it silently breaks that job the next time it fires, often with no error until then.

This is a read-only instrument: it never deletes, moves, writes, or restarts anything. It only answers SAFE or REFUSE, and only SAFE authorizes you to proceed with the deletion yourself.

## The core technique

Before deleting any path, search every place a path can be referenced, in **three spellings** — the absolute form, the `~/`-relative form, and the bare `/<parent>/<basename>` form. That third form matters more than it looks: scripts and job definitions often reference the same directory through different path prefixes, and a scan that only checks the absolute form misses those.

## What to screen

| Screen | What it catches |
|---|---|
| **Loaded scheduled jobs** (whatever your OS/init system runs — cron, a service manager, a scheduled-task system) | The **live**, currently-loaded state: program path, arguments, and environment variables. This catches jobs whose definition file was edited or deleted after it was loaded — the live version can differ from what's on disk. |
| **Job definitions on disk** (crontab, timer/service unit files, and their backups) | Definitions that reference the path but aren't currently loaded — including backup copies, which still name the path and can get reinstalled later. |
| **Config and scripts** | JSON/YAML/TOML/shell/config files anywhere in your config surface that hold the path as a plain string value. This is the class a job-definition-only scan structurally can't see. |
| **Running processes** | Process argv, including a process still running from an inode that's already been deleted on disk (the file is gone but the process holding it open isn't). |
| **Shared object stores** (e.g. a git "hub" checkout that other worktrees link against) | Whether the path is something other checkouts structurally *depend on* — deleting a hub doesn't just remove one checkout, it can destroy the object store every linked worktree needs, which is unrecoverable rather than merely inconvenient. |

## Fail-closed contract

A path is reported SAFE only when **every screen ran to completion and found zero references.** All of the following are REFUSE, not "probably fine":

- any screen found a reference to the path;
- any screen could not be completed (an unreadable file, the scheduler being unreachable, a scan-depth cap hit);
- the path doesn't exist (a nonexistent target usually means something upstream resolved the wrong path);
- the path is your home directory or filesystem root;
- the path sits inside a directory you've explicitly marked protected regardless of reference count;
- the check itself errored for any reason.

There is no code path in a correct implementation of this that turns "I couldn't tell" into SAFE.

## Reference implementation sketch

A minimal version is a stdlib-only script with one function per screen, each returning a list of references found (empty = clean for that screen):

```python
import glob, json, os, subprocess

def spellings(path: str) -> list[str]:
    home = os.path.expanduser("~")
    abs_p = os.path.abspath(path)
    forms = {abs_p}
    if abs_p.startswith(home):
        forms.add("~" + abs_p[len(home):])
    forms.add("/" + "/".join(abs_p.strip("/").split("/")[-2:]))
    return list(forms)

def screen_running_processes(forms: list[str]) -> list[str]:
    out = subprocess.run(["ps", "-axo", "command"], capture_output=True, text=True).stdout
    return [line for line in out.splitlines() if any(f in line for f in forms)]

def screen_config_surface(forms: list[str], roots: list[str]) -> list[str]:
    hits = []
    for root in roots:
        for f in glob.glob(f"{root}/**/*", recursive=True):
            if os.path.isfile(f) and os.path.getsize(f) < 2_000_000:
                try:
                    text = open(f, errors="ignore").read()
                except OSError:
                    return ["UNREADABLE:" + f]  # fail closed, not skip
                if any(form in text for form in forms):
                    hits.append(f)
    return hits

def gate(path: str, roots: list[str]) -> str:
    if not os.path.exists(path) or path in ("/", os.path.expanduser("~")):
        return "REFUSE"
    forms = spellings(path)
    screens = [
        screen_running_processes(forms),
        screen_config_surface(forms, roots),
        # add: loaded scheduled jobs, on-disk job definitions, crontab, git-hub-store
    ]
    return "REFUSE" if any(screens) else "SAFE"
```

Wire it as a hard precondition in any deletion sweep, one path at a time — never batch-delete on the strength of a single aggregate "looks clean":

```bash
for d in candidates/*/; do
  python3 pathref_guard.py gate "$d" && echo "SAFE $d" || echo "REFUSE $d"
done
```

## Audit mode: find what's already dead

The reverse check is just as useful on its own schedule: scan your config surface for absolute paths that **no longer exist** on disk, ranked by how live the consumer is —

1. A currently-loaded scheduled job reads this path — fix first, this is actively broken right now.
2. A job definition on disk, not currently loaded.
3. A crontab entry.
4. An authored-but-not-yet-installed job definition — installing it would schedule a job whose input is already missing.
5. No scheduled consumer found — lowest priority, likely just doc rot.

## What this deliberately does not screen (name the gap, don't paper over it)

- Open file descriptors — a full `lsof` sweep is too heavy to run as a routine gate.
- Remote/CI references (a hosted CI provider's own job definitions).
- Paths held only inside a database, a compiled binary, or a running process's memory rather than in argv or a config file.
- Paths assembled at runtime from variables (`os.path.join(base, name)`) — no static scan can see those. The `/<parent>/<basename>` spelling mitigates some of this; it doesn't eliminate it.

## When to use

- Before deleting, sweeping, pruning, or reclaiming disk from any worktree, clone, cache, or "stale" build directory.
- Before a bulk cleanup pass across many candidate directories at once.
- As a periodic audit, independent of any deletion, to find config paths that are already pointing at nothing.

## How to use

**Install:** copy this folder into `~/.claude/skills/deletion-safety-gate/` for personal use, or `.claude/skills/deletion-safety-gate/` inside a project repo. Fill in the screens (scheduled-job source, crontab, your config-surface root directories) for your actual OS and setup.

**Invoke:**

```
Before deleting these five old worktrees, run deletion-safety-gate on each
path and only actually delete the ones it reports SAFE.
```

```
Run deletion-safety-gate in audit mode over my config directories and tell
me which referenced paths no longer exist on disk.
```
