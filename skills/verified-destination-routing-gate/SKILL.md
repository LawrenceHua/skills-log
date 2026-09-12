---
name: verified-destination-routing-gate
description: Before posting or mutating a single external destination, classify the payload into exactly one destination class and verify that destination against a freshly-read allowlist — never a cached ID — refusing on any ambiguity.
---

# verified-destination-routing-gate

Any automation that can send to one of several destinations (a set of chat channels, a set of deploy environments, a set of recipients) has one specific failure mode worth designing against: sending the right content to the wrong place. A cached channel ID goes stale when a channel gets renamed or recreated; a classifier that's forced to pick a destination even when the content is ambiguous will eventually guess wrong. Both are avoidable with the same pattern — classify strictly, verify live, and refuse rather than guess.

## The method

1. **Enumerate destination classes up front.** Define the finite set of valid destinations your system can ever target, each with one canonical identifier and a clear description of what belongs in it.
2. **Classify the outgoing payload into exactly one class.** If the content plausibly matches more than one class, or matches none confidently, refuse and surface the ambiguity to a human — don't default to "the most likely one." A wrong guess sent automatically is worse than a delay waiting for a human call.
3. **Re-read the destination's identifier live at send time**, from the provider itself (list channels, look up the recipient, query the deployment target), instead of trusting a cached ID from config or a previous run. A renamed or recreated destination silently invalidates any cached ID, and a cache doesn't know that happened.
4. **Compare the classified class's expected identifier against the freshly-read one, and only proceed on an exact match.** A partial or fuzzy match is a refusal, not a best-effort send.
5. **Version the class-to-identifier mapping and require review on every change to it.** This mapping is the single place a routing mistake would actually originate, so treat edits to it with the same scrutiny as a production config change.
6. **Fail closed on any mismatch, missing destination, or ambiguous classification.** Surface the specific reason the send was blocked rather than falling back to a default destination — a blocked send is recoverable; a message sent to the wrong audience often isn't.

## When to use

- Any bot or automation that posts to one of several possible external destinations (chat channels across different workspaces or teams, multiple deploy targets, multiple notification recipients), where sending to the wrong one would be embarrassing, unsafe, or hard to undo.
- Reviewing an existing notifier or deploy script that resolves its destination from a config file or cache — check whether it re-verifies that destination live, or trusts a value that could have gone stale.
- Building a new integration that fans a single event out to different destinations depending on content, where a misclassification is a realistic risk.

## How to use

**Install:** copy this folder into `~/.claude/skills/verified-destination-routing-gate/` for personal use, or `.claude/skills/verified-destination-routing-gate/` inside a project repo.

**Invoke:**

```
Add a verified-destination-routing-gate in front of this bot's send step — it should
classify the message, re-read the channel ID live, and refuse instead of guessing on
ambiguity.
```

```
Review this deploy script's target-selection logic against verified-destination-
routing-gate — does it trust a cached environment ID anywhere?
```
