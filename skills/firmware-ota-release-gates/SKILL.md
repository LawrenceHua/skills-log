---
name: firmware-ota-release-gates
description: Ship firmware to a physical device you cannot debug from a terminal: scripted build recipe, release manifest, one artifact-level marker, gate order as the only rollback, decoded panics, one-actor flashing, and a probe of the state you left behind.
---

# Firmware OTA release gates

The source is here, the device is elsewhere, and the installer usually refuses to go backwards, so every mistake is paid forward into the next version. Each rule carries the kind of incident that bought it.

This is the reusable release method, not permission to flash. A hold or freeze wins over a release date.

## 1. The build recipe is a script, never a remembered command

A remembered command drifts one flag at a time and every drift still exits 0. Typical incident: several consecutive builds reported zero errors and zero warnings but were configured for the wrong board, with the product's main feature compiled out of a passing build.

```sh
ls -l <fw-repo>/scripts/build.sh            # prove the recipe exists before quoting it
git -C <fw-repo> rev-parse --short HEAD     # the sha the recipe will stamp
```

## 2. Move the build output aside before a version-counter bump

If the counter is baked at configure time, an incremental build silently reproduces the previous version: same counter, same image, no error.

```sh
cd <fw-repo> && mv build build-$(date +%s)
strings -a <bin> | grep -c '<new-version>'   # expect 1: the counter is in the artifact
strings -a <bin> | grep -c '<old-version>'   # expect 0: the negative control
```

## 3. Every release carries a manifest

One file beside the binaries, written at build time: version, counter, git sha, **bin and elf sha256 and byte size**, the exact configure line and its exit code, resolved flags, board, and the **acceptance target** this release exists to change (the number, its expected value, who set it). The git sha is usually not inside the image, so the manifest is the only thing tying an artifact to a commit. Without it, when a build panics you cannot prove which ELF matches the crashed binary.

Bind with `shasum -a 256 -b <bin>` and `wc -c < <bin>`; repeat for the ELF.

## 4. Find one artifact-level marker only the correct configuration produces

Pick a marker present in the artifact only when the configuration is right (a symbol count, a string count, a version string), record its expected value in the manifest, and count it before every flash. Zero where you expect more than zero is the regression detector. Check both directions: present in the good image, absent in a known-bad one.

```sh
nm <elf> | grep -ci <feature-engine>        # N on every correct image; 0 = wrong configuration
strings -a <bin> | grep -c <new-symbol>     # 1 on the fixed build, 0 on the old one
```

A count is a location, not a behaviour; it narrows the question, it does not close it.

## 5. OTA is a one-way door, so gate order is the only rollback

If the installer refuses downgrades, and an installed-but-never-completed boot stays quarantined even while the server still advertises it, you cannot reinstall the old image. Gate order becomes the entire rollback.

Order, first to last: **boot sanity, then panic decode, then the one user-visible number the release exists to change, then everything it was forbidden to break.** Fix the target number in the manifest *before* the flash; a reference chosen after the result is known turns a gate into a report. A failed gate is repaired by building the next version, not by reflashing the same one.

## 6. A panic is decoded, never guessed

Map the faulting PC to `file:line` with the cross toolchain's `addr2line` against the ELF **from that same release**. If the ELF is missing or its identity is unproven, the answer is `BLOCKED`, not a plausible function name.

```sh
A2L="$(command ls -d <toolchain-root>/*/bin/*-addr2line 2>/dev/null | tail -1)"
[ -x "$A2L" ] || { echo "no addr2line found"; exit 1; }
"$A2L" -pfiaC -e <elf> 0x<pc>
```

Resolve the path once with `ls -d ... | tail -1` and guard it with `[ -x ]`. An unquoted glob stored in a variable and used as a command works in bash but not in zsh, and "it works in my shell" is not evidence.

Two traps: a frame recorded in an aliased address range may need a fixed offset subtracted before it resolves; and a path under someone else's home directory is a vendor blob, so report it `OPEN`, not fixed. One fixed address is one crash site, not a class: three addresses from one panic can decode to three unrelated causes.

## 7. Flashing is a scheduled operation, not a background one

Quiesce every other actor, take a **pre-flash baseline readout**, record the window, flash, re-read. A second actor, such as an auto-updater installing another image mid-gate, invalidates the measurement and the image.

```sh
curl -s "http://<device-host>/diag" > before.json    # version, state, panic flag, uptime
curl -s "http://<device-host>/diag" > after.json     # diff: the version must be the new one
```

## 8. Leave the device in the shipped state, and prove it with a probe

A device is shipped when the field says so, not when a neighbouring field looks plausible and not when the request was accepted. A `202` proves queuing, not pixels or installation. Read the boot and panic records and uptime **twice**, far enough apart to cross a reconnect.

## 9. Release checklist

1. `git status --short` in the firmware repo: know whose uncommitted work you are building.
2. Run the host test suite; record the count and any pre-existing failures you did not fix.
3. Move `build` aside; build through the script with counter and sha.
4. Prove the version string in the artifact: new = 1, old = 0.
5. Count the artifact marker against the manifest and the previous release.
6. Write the manifest (version, counter, sha, bin and elf sha256 and size, configure line, board).
7. Claim the device in whatever lease or lock registry you use, confirm no second actor, take the baseline.
8. Flash only through a guarded wrapper; never a raw flash tool or a full erase "to start clean".
9. Gate in order: boot sanity, panic decode, the target number, regressions.
10. Re-read post-flash state and diff it against the baseline.
11. Return the device to the shipped state and prove it with the field that says so.
12. Write the receipt, then label it: `CODE-SHIPPED-NOT-VERIFIED` until a probe you did not write agrees.

## 10. Receipt shape

A stranger must be able to re-run the release from the receipt alone: recipe path and environment, manifest path, bin and elf hashes, flash command and exit code, pre- and post-flash readouts, each gate as **number, reference, and the command that re-derives it**, residual risks, and the label (`CODE-SHIPPED-NOT-VERIFIED` with no device evidence, `INCONCLUSIVE` on a failed control, `BLOCKED` with the missing artifact named).

## Never

- Never raw-flash or erase to start clean; the guarded path exists because both can brick devices.
- Never flash while another job, script or schedule owns the device; queue it and name the owner.
- Never infer "shipped" from a build exit code, a publish exit 0, a `202`, or one answering request.
- Never quote a counter from a build log, or decode a panic against an ELF with no manifest.
- Never treat one device's result as a fleet result; the fleet step is inference.

## When to use

- Releasing firmware or a large image over the air to hardware you cannot attach a debugger to.
- A boot loop, a panic you need decoded, or a question of whether a build actually reached the device.
- Writing a release checklist or manifest format for an embedded project that has none.

## How to use

1. Copy this folder to `~/.claude/skills/firmware-ota-release-gates/` (personal) or `.claude/skills/firmware-ota-release-gates/` inside a project.
2. Ask Claude Code to use the `firmware-ota-release-gates` skill by name.

Example prompts:

- "Use the firmware-ota-release-gates skill to write a manifest format and a 12-step release checklist for our OTA pipeline, and tell me which marker to count in the image."
- "Use firmware-ota-release-gates: here is a panic log and an ELF. Decode it, and tell me whether the ELF's identity is proven or the answer is BLOCKED."
