---
name: device-handover-saga
description: Hand a working bound device and its account to another person without a terminal: five owned legs, a one-tap owner approval, a re-runnable mover that never needs the device, and checks that come from outside the tool doing the move.
---

# Device handover saga

Handing hardware to a person is not a file copy. It is a saga with one owner act and five legs, and the
usual failure is that every leg reports success while the recipient receives nothing. This skill is the
shape that survives: who owns each leg, which invariants keep the mover re-runnable, and which checks do
not come from the tool grading itself.

## 1. The five legs, each with an owner

| Leg | Owner | Must be provable by something outside the producer |
|---|---|---|
| Recipient self-registers | recipient | The signup page answers 200 from outside your deployment, with no invitation required |
| The system notifies | server | The notification exists in the channel (read its timestamp) and the mail server's own accept reply is logged |
| Owner approves | owner, once | The approval link works only when authorised: admin surface returns 401, token surface returns 404/410 after use |
| Binding and account row move | automation | Registry owner id and the account row's foreign key agree, read live |
| Device reaches the recipient's network | recipient | The device's own documented setup path, or a long-press fallback |

Rule: the owner's act is one tap. If a step needs a terminal, a printout or a command, it is not part of
the handover; it is a workaround for a missing leg.

## 2. Invariants that make it re-runnable

1. **The mover must not need the device.** Compute the transfer from server-side state only. On a real
   handover the device is in transit or on someone else's network; a reachability gate turns a working
   transfer into a failure in exactly the window that matters.
2. **Derive the target id, never type it.** Hash a stable subject (a normalised address) into the target
   identifier, with an explicit allowlist for adopted accounts. A guessed id hands the device to a stranger.
3. **One write gate.** A single flag performs writes. A separate read-only `--verify` mode is what every
   proof step calls. Do not put a revert in the same tool.
4. **Attach is idempotent.** A second run finds the binding already moved and re-proves it instead of
   moving twice.
5. **Arm by timestamp, not boolean.** Record `armed_at`. An empty value is disarmed and must be reported as
   such; `armed: null` in a state file proves nothing.
6. **Watch the watcher.** The job that fires the transfer exits 0 whether it worked or sat idle. Pair it
   with an independent observer that alerts on stale or never-armed state.
7. **Data does not follow the device row.** Before promising a clean slate, read the foreign keys: rows
   keyed by account stay with the old owner; rows keyed by device travel with the hardware. One query
   decides which promise is honest.

## 3. Never

- Never unbind by deleting the binding row to "reset" it if the reconciler only updates. You would be
  deleting the only copy. Confirm an insert path exists before trusting a reversible-sounding word.
- Never fire the real path as a test when the only registered subject is the owner. It resolves to the
  owner's own account and moves the device back, a silent revert that looks like success.
- Never gate the transfer on the device answering.
- Never quote the tool's exit 0 as proof. Read the channel, the database row, or the vendor receipt.
- Never hand-write SQL to repair a row when a tested repair script exists.
- Never test the failure notification by deliberately failing a real handover.

## 4. Pre-flight before the recipient touches it

Write one read-only script, exit 0 meaning ready, that prints one line per leg: device answering and in a
sane state; the health flag that silently dies (not only power); binding agrees on both sides; watcher
armed, not yet fired, last exit 0; account list unchanged. Run it minutes before the handover and paste
its output block into your work log. Make each check overridable by environment variable so the script is
testable without the device.

## 5. Verify from three independent sides

```sh
./pre-handover-check.sh        # exit 0 = READY; one line per leg
./verify-handover.sh           # registry + account row + device; prints the owner line
./mover.sh --verify            # read-only, server-side only (no device)
```

Require the owner line to name both identities and agree, for example
`owner: device-registry=<target-id> console=<account-email>`. Then check the data direction you promised:

```sh
sqlite3 -readonly <db-file> "SELECT COUNT(*) FROM <table> WHERE account_id = <recipient-id>;"
sqlite3 -readonly <db-file> "SELECT COUNT(*) FROM <table> WHERE account_id = <old-owner-id>;"
```

Expect the recipient at 0 and the old owner unchanged. Quote that pair, not a narrative.

## 6. The message that says it worked

One message, four fields: who it went to, what moved (registry entry and account row), when, and the one
sentence that removes doubt ("you did not have to run anything"). Add exactly one recovery line for the
predictable failure, such as a power cycle. Print the address it moved to and invite a correction; a
mistyped address is the one failure that locks the recipient out, so the handover must be re-runnable.

## 7. After

Leave a recovery page beside the handover doc: what each alert means, what to do for each, and the exact
command that restarts each job. A handover without one is finished work that still wakes someone at the
wrong hour.

## When to use

- Giving a device, assistant appliance or any account-bound hardware to another person.
- An approval must trigger a move automatically, with no operator at a keyboard.
- Someone asks "is the handover really ready?" and you need more than a green script.

## How to use

1. Copy this folder into `~/.claude/skills/` (personal use) or `.claude/skills/` inside a project.
2. Ask Claude Code to use the `device-handover-saga` skill by name.

Example prompts:

- "Use device-handover-saga to review my plan for transferring a bound smart speaker to a friend, and list
  which of the five legs has no outside proof yet."
- "Use device-handover-saga to write the read-only pre-flight script for my handover, one line per leg."
