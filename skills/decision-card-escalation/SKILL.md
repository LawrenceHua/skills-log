---
name: decision-card-escalation
description: Decide when an agent should take a decision itself versus escalate it, and write the escalation as a durable single-decision card with a recommendation, a default and a deadline, proven delivered from the channel's own state rather than the sender's exit code.
---

# Decision card escalation

Decisions that need a human should reach them as a durable **card**, not as a question typed into a chat window. A chat question is answered by whoever is looking, evaporates when the session ends, and cannot be resumed. A card is durable, carries options and a default, and leaves a receipt.

## 1. Decide or escalate: the four-part test

An agent may take a decision itself, record it with its rollback, and proceed only when **all four** hold:

1. **Executable**: an agent can actually do it. A signature, a login, a payment or a physical action cannot be "decided" by an agent; it can only be pretended.
2. **Reversible**: it can be undone locally by the same agent without asking anyone.
3. **Bounded**: the downside of being wrong is known and small enough to accept.
4. **Unruled**: the human has not already decided it. An existing clearance, grant or recorded decision satisfies this, so a cleared action is executed, never re-asked. Reading this as "have they spoken recently?" turns every clearance into a loop.

If any one fails, it is the human's and gets a card. No decision under this test overrides a hold, a freeze or a standing rule; those are the human having already ruled. "It has consequences" is not the test; every decision has consequences.

Never send a card to re-ask something already answered; it is the most expensive kind of noise and teaches the reader to skim. Never send a decidable decision as a card; it turns a zero-second default into human latency.

## 2. The card contract

- **One decision per card.** Two decisions in one card get one answer and a half. (A single list card holding several pending *chores* is fine; several *decisions* are not.)
- A **recommended option** and a **default if no answer**. If silence would leave the matter ambiguous, the card is incomplete.
- A **deadline** (keep it short, a few days at most) and what happens at it.
- **Evidence rows that carry proof**, not narrative. The card must stand alone for someone with no session context.
- Respect field length caps. Labels are the usual casualty: an option label one character over the cap may be dropped silently, so the option vanishes with no error.
- An option's label must be at least as broad as the code that implements it. A narrow label on a broad change asks for the wrong consent.

## 3. Prove the premise before sending

A card that authorizes an action must first prove the action's input exists, and the proof belongs in the card's evidence rows. A card built on a false premise is worse than none: it spends trust and yields a decision about nothing.

If a premise turns out false after posting: withdraw the source, then post a **second card under a new request id** that states plainly what was wrong. Withdrawal does not retract the delivered message and typically blocks a repost under the *old* id, so a correction that reuses the id is silently suppressed and looks exactly like a correction nobody sent. A correction is a second card; it is never an edit.

## 4. Prove a card is live

A card is live only when the channel's own state says so. The producer's exit code is not evidence, and an attempt counter is not delivery.

- Read three things from the channel's state: the source record's status, a non-null delivery timestamp, and the message identity.
- **Validator failures often exit 0.** Unpostable content shows up in a skipped-items list, not a non-zero exit. Read the skip list every time.
- A dry-run mode that reports "posted: N" usually skips the channel's intake validation. It is not evidence a card will post.
- A stale request artifact can suppress delivery permanently for that request id. Deleting it may be a fenced action; re-issue under a new id instead.
- A card written to the consumer's directory was never written. Know which directory is the source and which is the output.
- Pin the interpreter explicitly when the producer bakes it into a handler path. A shim interpreter whose resolved path differs from the configured prefix can make the intake refuse the card, and the refusal then pins itself to that id.

## 5. The fallback ladder

When the channel is broken, in order:

1. Say the channel is broken, and exactly what is broken, in the same breath as the decision. Never let the human believe a card is coming when it is not.
2. Deliver the same content through a surface they will actually see, keeping options, recommendation, default and deadline intact.
3. Record where it went and what would prove it was answered, so the next agent resumes instead of re-asking.

## 6. Noise gates

1. **Check open cards before writing a new one.** Extend, supersede or withdraw instead of adding a second card about the same decision.
2. **Batch human-hands chores** (logins, signatures, physical steps) into one list card with the exact URL and expected duration per item.
3. **Cap open cards per producer** (two is a good number). At the cap the producer holds new cards and sends nothing until the open count drops; it does not route around the cap by renaming itself.
4. **Defaults close the card.** Past the deadline, the producer, not the display layer, applies the card's own default and records that answer.

## Anti-patterns

- Evidence rows that describe the work instead of proving the premise.
- No default, so the card silently becomes a stall.
- Calling a card sent because the producer printed success.
- Answering in chat about a decision that also needs a card, so the durable record and the conversation diverge.
- Writing the card from session context it will not have.

## When to use

- Work needs a human's act: a login, an approval, a signature, a clearance, a judgment call.
- Building or reviewing an approval or escalation channel (Slack cards, tickets, email, an approvals queue).
- A producer claimed success but nothing reached the human.

## How to use

1. Copy this folder to `~/.claude/skills/decision-card-escalation/` (personal) or `.claude/skills/decision-card-escalation/` inside a project.
2. Ask Claude Code to use the `decision-card-escalation` skill by name.

Example prompts:

- "Use the decision-card-escalation skill on these five open questions: apply the four-part test, decide the ones I would not need to see, and draft cards for the rest with a default and a deadline."
- "Use decision-card-escalation to check whether the card our bot says it sent actually reached the channel, reading the channel's own state rather than the bot's output."
