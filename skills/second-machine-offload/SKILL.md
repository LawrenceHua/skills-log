---
name: second-machine-offload
description: Turn a second machine you own (a laptop, a home server, a spare desktop) into a safe batch worker for CPU-bound jobs — a health check, a secrets-excluding file sync, and a single round-trip command that pushes work, runs it, and pulls results back with a verifiable receipt.
---

# second-machine-offload

If you have access to a second machine — a laptop that's usually idle, a home server, a spare box on the same network — CPU-bound batch work (compiles, transcodes, test sweeps, bulk data crunching, simulations) doesn't have to tie up your primary machine. The pattern below turns that second machine into a safe, scriptable worker without ever putting your primary machine's credentials on it.

## Is a job a good fit?

Offload when **all** of these hold:

- **CPU- or wall-clock-bound, and self-contained** — a compile, a transcode, a test sweep, bulk parsing, a simulation, a format conversion.
- **No secrets needed.** No tokens, API keys, `.env` files, keychain items, or auth sessions. The second machine should hold none of your primary machine's credentials, ever.
- **No dependency on your primary machine's own services** — not its local databases, its local ports, or anything under its private directories.
- **Results fit in files.** The job's output has to land in a designated output directory you can pull back.

Do **not** offload anything touching credentials, anything that needs services only running on your primary machine, interactive work (there's no terminal on the far end), or anything that would fill more disk than the second machine can spare.

## Pre-flight: is the second machine healthy?

Before pushing a job, confirm you can reach it and that now is a reasonable time to load it up:

```bash
ssh <second-machine> 'uptime && df -h ~ | tail -1'
```

If you run this often enough to matter, have a lightweight background check (a cron/timer entry, once every 10–15 minutes) write a small JSON snapshot — reachable, on AC power, free disk — so later checks read a file instead of re-probing every time. Fail closed: if the snapshot is missing or stale, just run the health check directly rather than assuming healthy.

## The three building blocks

**1. Run one command over there.**

```bash
ssh <second-machine> -- 'cd <remote-workdir> && <command>'
```

Wrap this in a small script that: refuses to run if the machine is on battery (unless explicitly overridden — draining someone's laptop battery for your batch job is worse than a slower local run), times out after a sane ceiling, and propagates the remote command's real exit code.

**2. Move files, excluding anything secret-shaped.**

```bash
rsync -av --exclude='*.env' --exclude='*.pem' --exclude='*.key' \
  --exclude='id_*' --exclude='.credentials' --exclude='.netrc' \
  <local-dir>/ <second-machine>:<remote-workdir>/
```

Refuse (don't just warn) if the source directory contains anything matching those patterns — that refusal is a feature. Move the secret-shaped file out of the sync source rather than adding a bypass flag.

**3. The whole round trip — prefer this one over doing the two above by hand.**

```bash
#!/usr/bin/env bash
# offload.sh <job-name> <local-workdir> -- <command...>
set -euo pipefail
job="$1"; local_dir="$2"; shift 2; [ "$1" = "--" ] && shift
remote_dir="offload/${job}-$(date -u +%Y%m%dT%H%M%SZ)"

rsync -av --exclude='*.env' --exclude='*.pem' --exclude='*.key' \
  --exclude='id_*' --exclude='.credentials' --exclude='.netrc' \
  "$local_dir"/ "<second-machine>:$remote_dir"/

ssh <second-machine> "cd $remote_dir && caffeinate -i nice -n 10 $*" \
  && rc=0 || rc=$?

mkdir -p "$local_dir/out"
rsync -av "<second-machine>:$remote_dir/out"/ "$local_dir/out"/ || true

cat > "receipts/${job}-$(date -u +%Y%m%dT%H%M%SZ).json" <<EOF
{"job":"$job","rc":$rc,"remote_dir":"$remote_dir","pulled_at":"$(date -u -Iseconds)"}
EOF
exit $rc
```

This pushes the local working directory, runs the command remotely under a sleep-prevention wrapper at a lowered priority (so it doesn't starve anything else already running on that machine), pulls the `out/` directory back, and writes a small JSON receipt. Your command's job is to write its results into `out/` — nothing else gets pulled back.

## Verify a run

Don't trust "the script exited" — check the receipt:

```bash
cat receipts/<job-name>-<stamp>.json
```

`rc` of `0` means the remote command succeeded. If `rc` is `0` but `out/` came back empty, the command wrote its results somewhere other than the agreed output directory — that's a bug in the job, not in the offload mechanism.

## Traps worth knowing before your first real job

- **A restricted SSH key changes the environment.** If you (correctly) scope the offload key down — no port forwarding, no shell, a stripped `PATH` — plain tool names that rely on your normal shell's `PATH`/`rc` files will fail with "command not found." Prefix commands with whatever sets up the environment you need (e.g. sourcing a package manager's shell hook) inside the wrapper script, once, so every job inherits it.
- **Two Python/Node/etc. installs can both be on the remote `PATH`.** If it matters which one runs, call it by absolute path rather than by bare name.
- **No `sudo`, ever, on the far end.** If a job needs root, it's not a fit for this pattern.
- **Scope the writable area to exactly one directory** on the second machine, and enforce it in the script (refuse any path outside it) rather than trusting yourself to remember.
- **On-battery jobs get refused by default.** This is deliberate, not a bug to route around.
- **No spaces in remote job names/paths** — keep job identifiers to `[A-Za-z0-9._-]`.

## When to use

- You have access to more than one machine and a batch job (build, test sweep, data crunch, transcode) is about to tie up the one you're actively working on.
- You want to parallelize independent work across machines you own.
- Before trusting an unattended batch job on a second machine, to confirm it's reachable and not about to run on battery.

## How to use

**Install:** copy this folder into `~/.claude/skills/second-machine-offload/` for personal use, or `.claude/skills/second-machine-offload/` inside a project repo. Fill in your second machine's SSH alias and a writable remote directory before first use.

**Invoke:**

```
The build/test sweep for this repo is going to take a while — offload it to
my second machine using second-machine-offload and bring the results back
into ./out when it's done.
```

```
Check whether my second machine is healthy and not on battery before we
offload anything to it today.
```
