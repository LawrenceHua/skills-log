---
name: device-identity-proof-triage
description: Debug "the server ignores my device" by separating the identities a device presents, the proof mode behind a log line, the model string that selects its build, and probe identities that corrupt attribution.
---

# Device identity and proof triage

A connected device and its server disagree about "which device is this" in several separate ways, and each
drives a different outcome. Most "the server ignores my device" reports are one identity being wrong for
the question being asked, not a bug in the others.

## 1. Name the identities before theorising

| Identity | Typically | Decides |
|---|---|---|
| Hardware id (network address) | burned in, sent by firmware | registry lookup key |
| Install id (random uuid) | generated once, stored in device flash | registry lookup key and the pair proof |
| Model string | announced by the device | which build or feature set it is offered |

Shape check first: a real device request carries a hardware id plus a uuid install id. A request whose
install id is the hardware id was made by a script. That one fact separates device traffic from probe
traffic and is the first thing to read when something claims a device is online.

## 2. Read the registry before reasoning

The registry (an account file or table on the server's persistent volume, not in the image) answers: is the
device bound to an account, was its credential ever delivered, and which identity pair must a request
carry. Read it before inferring anything from logs. `credential_delivered: false` is a complete answer to
"could the device have authenticated with its credential?" No amount of log inference changes it.

## 3. Proof mode is not presence

- **Pair proof**: two header values matched a registry row. No secret, no signature, no challenge. Anyone
  who knows the pair can produce it with `curl`.
- **Secret proof**: a real credential was presented. This is evidence of the device; it cannot appear while
  the credential was never delivered.

A log line reading `proof=pair account=<owner>` is not evidence the device is present. Check the proof mode
before concluding anything is online.

## 4. The model string selects the build

Build lookup is usually a map keyed by the announced model string. Zero candidates for that key means "up
to date" to the device, forever.

| Announced model | Candidates | Offered |
|---|---|---|
| current name | many | latest build and URL |
| older alias after a rename | some | latest build and URL |
| legacy alias | 0 | nothing, "already latest" |

Publish every build under every model string the fleet can announce. After any rename, check the announced
string before blaming the device.

## 5. The stub that impersonates "you are up to date"

Many handlers return a default body, `{"firmware": {"version": "<what the device claimed>", "url": ""}}`,
when there is no newer build, when lookup found zero candidates, and when the version check raised and the
error was swallowed. It is not a verdict. Read the server's own branch lines (the "searching model X, found
N candidates" log) and confirm X is your model. If it is not, you have a probe defect, not an empty
registry.

## 6. Probe hygiene

A probe that presents the device's own identity corrupts every later log reading. Real consequence: a
monitoring script polling with a device's real id convinced another reviewer the device was alive, and a
correct diagnosis was retracted.

- Use an obviously synthetic identity such as `name-probe` and `name-probe-client`.
- Never reuse a fleet hardware id or real uuid, not even once "to see what it gets".
- Put the probe's own name in the identity so the log line explains itself later.
- Unattributable traffic: install-id shape decides it. Hardware id means script; uuid means device or an
  imitation; absent means neither.
- An unbound probe identity has per-account features suppressed by design; that suppression looks exactly
  like an outage.

## 7. Diagnosis order for "the device gets nothing"

1. Identity shapes in the log: is a real device talking at all?
2. Registry row for that pair: bound? credential delivered?
3. Announced model to candidate count: zero means the build is not published under that name.
4. Proof mode: pair proves nothing about presence; secret proves the credential.
5. Only then transport: rate times wall-clock arithmetic for a failing install.

## Never

- Never conclude a device is online from an authenticated log line without the proof mode.
- Never conclude a build is unavailable from one manifest; read the candidate line for the model.
- Never probe with a device identity, and never let a monitor script inherit one.

## When to use

- A device receives no update, or the server says "already latest" while it is clearly old.
- Telemetry or per-account features are silently missing.
- Telling a real device from a probe, or before publishing a build to a fleet.

## How to use

1. Copy this folder into `~/.claude/skills/` (personal use) or `.claude/skills/` inside a project.
2. Ask Claude Code to use the `device-identity-proof-triage` skill by name.

Example prompts:

- "Use device-identity-proof-triage on these OTA server logs: why does one device never get the new build?"
- "Use device-identity-proof-triage to review my monitoring script and tell me whether it can pollute the
  fleet's logs."
