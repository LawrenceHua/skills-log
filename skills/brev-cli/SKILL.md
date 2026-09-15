---
name: brev-cli
description: Manage GPU and CPU cloud instances from the command line with the Brev CLI — search, create, SSH/exec, editor integration, file copy, port-forwarding, and safe teardown, for ML training, fine-tuning, and inference workloads.
---

# brev-cli

A working command reference for [Brev](https://brev.dev)'s CLI, which provisions and manages GPU/CPU cloud instances for ML workloads (training, fine-tuning, RL, inference, batch processing) and general remote compute. Useful any time you'd otherwise be hand-writing cloud-provider API calls or clicking through a console to get a throwaway GPU box.

## Quick start

```bash
brev search              # available GPUs, sorted by price
brev search cpu          # CPU-only instances
brev create my-instance  # smart defaults: cheapest matching GPU
brev ls                  # your instances
brev shell my-instance   # interactive SSH
brev exec my-instance "nvidia-smi"   # non-interactive command
brev open my-instance code           # open in VS Code on the remote box
```

## Searching for instances

```bash
brev search gpu --wide                        # + RAM/ARCH columns
brev search --gpu-name A100
brev search --min-vram 40 --sort price
brev search --stoppable --min-total-vram 40 --sort price

brev search cpu --provider aws --min-ram 64 --arch arm64 --min-vcpu 16 --sort price --json
```

## Creating instances

```bash
brev create my-instance --type g5.xlarge
brev create my-instance --type g5.xlarge,g5.2xlarge     # fallback chain
brev create my-instance --gpu-name A100 --min-vram 40    # filters instead of an exact type
brev create my-cluster --count 3
brev create my-instance --startup-script @setup.sh
brev create my-instance --dry-run                        # preview the match, create nothing

# pipe search results straight into create, and create straight into open/exec
brev search --gpu-name A100 | brev create my-box | brev open cursor
brev search --gpu-name A100 | brev create my-box | brev exec @setup.sh
```

## Working on an instance

```bash
brev shell my-instance                    # interactive SSH
brev exec my-instance "python train.py"   # one command
brev exec my-instance @setup.sh           # run a local script remotely (@ reads the file)
brev exec instance1 instance2 "nvidia-smi"  # fan out to several instances at once

brev open my-instance code      # VS Code
brev open my-instance cursor
brev open my-instance windsurf
brev open my-instance tmux      # terminal + tmux

brev copy ./local-file my-instance:/remote/path/
brev copy my-instance:/remote/file ./local-path/

brev port-forward my-instance -p 8080:8080
brev ports create my-instance 8080 --protocol http --public
brev ports create my-instance 8888 --protocol http --authorize me@example.com
brev ports ls my-instance
```

## Listing and lifecycle

`brev ls` and `brev ls nodes` are two separate namespaces — external nodes registered to an org never show up in plain `brev ls`, so check both before concluding a machine doesn't exist.

| | `brev ls` (cloud instances) | `brev ls nodes` (external nodes) |
|---|---|---|
| Status values | `RUNNING` / `STOPPED` | `Connected` / `Disconnected` |
| `stop`/`start`/`delete` | yes | no — Brev doesn't own their lifecycle |
| `--json` shape | `.workspaces[]` array | top-level array |

```bash
brev ls --json | jq -r '.workspaces[].name'
brev ls nodes --json | jq -r '.[] | select(.status=="Connected") | .name'

brev delete my-instance
brev stop my-instance
brev start my-instance
brev reset my-instance      # recover from a stuck/errored instance

# bulk ops via pipe
brev ls | awk '/RUNNING/ {print $1}' | brev stop
brev ls | awk '/STOPPED/ {print $1}' | brev delete
```

## Organizations

```bash
brev org ls
brev org set my-org      # or: brev set my-org
brev invite               # generate an invite link
```

## Safety rules

**Never do these without explicit confirmation from the person you're operating on behalf of:**
- Delete an instance (`brev delete`)
- Stop a running instance (`brev stop`)
- Create more than one instance in a batch (`--count > 1`)
- Create an expensive instance (H100, multi-GPU)

**Always do these first:**
- Show the instance's cost and type before creating it.
- Confirm the instance name explicitly before deleting anything.
- Run `brev ls` (and `brev ls nodes`) before assuming an instance does or doesn't exist.

## Troubleshooting

- **"Instance not found":** check `brev ls` and `brev ls nodes` separately (different namespace), and confirm you're in the right org with `brev org ls`.
- **"Failed to create instance":** try a different type (`brev search --sort price`) or check quota/credits with an org admin.
- **SSH connection fails:** `brev refresh` to regenerate SSH config; confirm the instance is actually running.
- **Editor won't open:** confirm the editor binary is on `PATH` (`which code` / `which cursor`); set a default with `brev open --set-default code`.

## When to use

- Spinning up a GPU box for training, fine-tuning, or inference and tearing it down cleanly afterward.
- Searching for the cheapest instance that satisfies a VRAM/RAM/vCPU constraint before committing to one.
- Scripting a repeatable "search → create → copy data → run → collect results → delete" cycle instead of doing it by hand each time.

## How to use

**Install:** copy this folder into `~/.claude/skills/brev-cli/` for personal use, or `.claude/skills/brev-cli/` inside a project repo. Requires the `brev` CLI itself to be installed and authenticated separately.

**Invoke:**

```
Use brev-cli to find the cheapest available A100 with at least 40GB VRAM,
create an instance, and open it in VS Code.
```

```
Spin up 3 CPU instances with at least 64GB RAM for a batch job, run
setup.sh on each, and show me how to tear them all down when the job
finishes.
```
