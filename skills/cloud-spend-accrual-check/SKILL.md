---
name: cloud-spend-accrual-check
description: Watch cloud and API spend read-only against caps, prove with two timed readings whether a cost is still accruing before calling it a leak, and hand the owner one decision with a safe default.
---

# Cloud spend accrual check

Agents reviewing bills tend to raise two kinds of false alarm: a total that is large but no longer growing, and a "nothing is running" report while storage keeps billing. This skill finds money that is leaking, proves it, and proposes one action.

## Authority

Default to read-only. If the owner has given standing permission to stop clearly idle compute, confirm no job depends on it, stop it, and report at once. Deleting is not covered by that permission. Note that on many providers a stopped machine still bills for its disks or reserved addresses, and some offer no stop at all, only termination.

## 1. Inventory

List resources with each provider's read-only commands: applications, machines or instances, GPUs, volumes, snapshots, reserved addresses, managed databases and API usage. Record the command and the time beside every result. An empty instance list says nothing about storage.

If a command fails or a login has expired, the provider is `UNKNOWN`, not zero.

## 2. Billing truth

Invoices, receipts and the provider's billing page are the record of what was charged. CLI listings and usage counters are leading indicators. Add up only documents you actually opened, and write each figure with its source date. Note credits that offset charges.

## 3. Caps

Keep the owner's caps in one table and re-read it before quoting any of them.

| Bucket | Cap | Alert at |
|---|---|---|
| Always-on services | <amount per month> | <percent> |
| API usage | <amount per month> | <percent> |
| GPU or burst compute | <amount per day and per period> | <percent> |

If two sources disagree about a cap, apply the stricter one and flag the conflict.

## 4. Frozen or accruing

Do this before any "it is still billing" claim.

1. Take reading A of the usage counter for the specific resource (running seconds, byte-hours, accumulated cost), with a timestamp.
2. Wait long enough for the counter to move visibly given how often the provider updates it. Several hours at least; 24 hours is far more convincing.
3. Take reading B the same way.
4. Judge it:
   - **Accruing** when the counter grew roughly in line with elapsed time or use.
   - **Frozen** when it did not move over a window longer than the provider's reporting delay. Report "not accruing in this window, recheck at <time>".
   - **Inconclusive** when the window is shorter than the reporting delay or a read failed.
5. Reconcile with receipts and credits. A counter is not an invoice.

A deleted resource can leave a non-zero lifetime total behind. That total looks alarming and may never grow again, which only the second reading shows.

## 5. Output

One line per finding:

```
<provider> | <resource> | <figure per day or month> | source <receipt date or command + time> | cap <x> | under/over | state accruing/frozen/inconclusive | proposed action, default if silent: <safe default>
```

Put the safe default on every decision ("keep, recheck on <date>"). Batch non-urgent items into one list. Raise immediately only what is accruing and near or over a cap.

## Never

- Never delete a machine, volume, snapshot, bucket or domain. Stopping clearly idle compute, only with standing permission, is the limit.
- Never deploy, scale up, change plans or buy credits.
- Never open credential files or print API keys; use the CLIs' existing logins.
- Never call a cost a leak from a single reading.
- Never quote a cap from memory.

## When to use

- A daily or weekly cost check.
- "What am I spending?" or "Am I over a cap?"
- A GPU, volume or deleted resource may still be billing.
- Before asking anyone to delete or stop something to save money.

## How to use

1. Copy the `cloud-spend-accrual-check` folder into `~/.claude/skills/` for personal use, or `.claude/skills/` inside a project.
2. Ask Claude Code to use the skill by name.
3. Example prompts:
   - "Use the cloud-spend-accrual-check skill to inventory my cloud accounts read-only and list anything that is still accruing. My caps are <caps>."
   - "I deleted two volumes yesterday and still see a cost. Use cloud-spend-accrual-check to find out whether it is growing."
