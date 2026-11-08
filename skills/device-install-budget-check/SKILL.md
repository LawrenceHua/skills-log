---
name: device-install-budget-check
description: Decide whether a firmware or large-image update can physically reach a device over its network, using measured rate times wall-clock, and separate server fault from device fault with a slow-client control.
---

# Device install budget check

A device that cannot receive an image is usually not a build problem and often not a server problem. It is
arithmetic: the image has to arrive inside the time the device is willing to keep reading. Compute that budget
before changing any code. Every round spent on a fix before this arithmetic is a round spent on an untested
hypothesis.

## 1. Measure both numbers, then divide

- **Image size:** `ls -l <artifact> | awk '{print $5" bytes"}'`
- **Device rate:** read it from the device's own update counters (bytes read, bytes written, elapsed seconds),
  not from a speed test on your laptop. Bytes per second as the device experienced it is the only rate that counts.
- **Wall:** the elapsed time at which the device stops reading. It is empirical; take it from the elapsed time at
  which earlier attempts ended.

> installable if `image_bytes / device_rate < device_wall`

Worked example: a 3.6 MB image at 6.4 kB/s needs about 560 s against a wall near 400 s. The transfer cannot
finish, so every retry is a lottery ticket and each costs several minutes.

If the quotient is close, options are a faster path (position, region, another host), a smaller image, a wired
route, or resume support in a build the device can already receive. If it is far over, no server fix helps.

## 2. Three checks that look like proof and are not

- **"Connection not cut" in the server log.** That is the application's view. It says nothing about whether the
  client received the bytes.
- **A tiny handler time on a multi-megabyte file.** The handler handed bytes to a buffer; that is not delivery.
- **Several attempts stopping at similar byte counts.** That looks like a byte cap, but if the runs also had similar
  rates, similar rate times similar wall gives a similar stop byte. Compare rates before naming a cap.

## 3. The control that separates server from device

Run a client at the device's own rate and let it finish:

```sh
curl -s -o /tmp/img.bin --limit-rate 6k \
  -w 'bytes=%{size_download} time=%{time_total}s speed=%{speed_download}B/s\n' "<download url>"
shasum -a 256 /tmp/img.bin     # must equal the built artifact's sha256
```

If a client slower than the device receives every byte with the right hash, the server is exonerated. Publish that
control next to the failure; it turns "we think the server is fine" into a statement with a receipt. The remaining
questions are rate and wall.

## 4. The manifest stub that impersonates "you are up to date"

An update-check response that echoes the version the device claimed, with an empty download URL, is the default
stub. The same shape comes back when:

- there is genuinely no newer build,
- the lookup used the wrong model or channel and found zero candidates,
- the version check raised an exception that the handler swallowed.

You cannot tell which from the response. Read the branch in the server log (candidate counts are usually logged).
An empty-candidate line names what was searched; if that is not the model your build is published under, you have a
probe defect, not an empty registry.

## 5. Probe with the identity the device actually uses

Manifest responses are often scoped by identity. A synthetic id silently changes the answer: per-account features
are suppressed for an unbound identity, which reads exactly like "the feature is not deployed".

1. Read the registered identifiers from the registry, read-only (print ids, never tokens).
2. Replay the request with every identifier the device sends (device id, client id, model or board type in the body).
3. Run a control: the same request with the model omitted must be worse. If both answers are identical, the model
   field does nothing and your probe is inert.

A probe missing one of the three identifiers is a probe of a different device.

## 6. What proves the build reached the hardware

Only the device's own report: the version string read from the device after it boots, plus a state that is not the
update state. An advertised manifest, a server log that served the file, and a published artifact are each necessary
and none is sufficient. Quote the version from the device or report the install as unproven.

## 7. Aftermath

An aborted update can be followed, minutes later, by a device that stops answering network requests while still
powered. Recovery may need a physical power cycle. So: do not retry an install whose arithmetic does not close, warn
the owner that a power cycle may be needed, and leave the device idle rather than mid-upgrade.

## Never

- Never quote a device rate from your own host's request to the same server.
- Never call a server fix "the unblock" until the slow-client control has failed to receive the file.
- Never treat a repeated stop byte count as a cap without comparing rates.
- Never probe a per-account endpoint with a synthetic identity and conclude the feature is missing.
- Never report an install as done from the server side.

## When this is wrong

It assumes one download attempt with no resume. A build that supports HTTP range resume (`accept-ranges: bytes`) can
survive a wall because each attempt is small; the arithmetic then becomes a per-chunk budget. Check whether the
device's current build has resume before declaring an install impossible.

## When to use

- An over-the-air update keeps failing, or the server shows a successful download while the device stays on the old
  version.
- A manifest says "up to date" and you suspect the probe.
- Someone proposes a server fix for a device-side symptom.

## How to use

1. Copy this folder to `~/.claude/skills/device-install-budget-check/` (personal) or
   `.claude/skills/device-install-budget-check/` inside a project.
2. Ask Claude Code to use the `device-install-budget-check` skill by name.

Example prompts:

- "Our sensor firmware update downloads on the server but the unit never upgrades. Use device-install-budget-check:
  compute the rate-times-wall budget from its counters and run the slow-client control."
- "The update endpoint returns an empty URL for my test device. Use device-install-budget-check to tell me whether
  that is a real 'up to date' or a probe defect."
