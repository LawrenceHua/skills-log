---
name: signal-to-ticket-pipeline
description: Turn an ambient stream of unstructured signal (a chat channel, an inbox, voice notes) into scored, classified, ticketed work items automatically — with a cost cap, per-run rate limit, hash-based dedup, a sanitize pass on every external write, and a VERIFIED / CODE-SHIPPED-NOT-VERIFIED probe before any item is called done.
---

# Signal-to-Ticket Pipeline

Some sources of information are too high-volume to read by hand but too
valuable to ignore: a busy chat channel, a shared inbox, a stream of voice
notes. The temptation is to point an LLM at the whole feed and let it "handle
it," which either floods your issue tracker with noise or silently drops the
one message that mattered. This method turns raw signal into a small number
of well-formed, verified tickets, with hard limits so an automated run can
never overspend, double-process, or half-finish a write.

## The method

**1. Poll from a durable cursor, not from "everything."** Track the
last-seen position (a timestamp, a message ID, an offset) and only fetch
items newer than it. Persist the cursor immediately after a successful run,
not before, so a crashed run re-reads instead of silently skipping.

**2. Normalize every item to text before scoring.** If an item is audio,
transcribe it with a speech-to-text API; if it's already text, use it as-is.
Track the cost of every paid call (transcription, LLM scoring, LLM dispatch)
against a hard daily cap, and abort the run cleanly the moment you'd exceed
it — don't let a burst of audio messages blow the day's budget mid-run.

**3. Chunk and score against a written rubric, not a vibe.** Split each item
into paragraph-sized chunks and score each one (e.g. 0–3) against a rubric
you've actually written down and can point to — the set of things that make
a message worth turning into work for *this* project. Only chunks that clear
a minimum score proceed; the rest are read but never acted on.

**4. Classify into a small, fixed set of action types.** Map each
qualifying chunk to one of a handful of categories (e.g. research / design /
implementation / audit / test-case) rather than leaving the action open-ended
— a bounded category set is what makes step 5's dispatch and step 8's ticket
prefixing possible.

**5. Dispatch to a type-specific handler.** Each action type gets its own
tightly-scoped prompt or agent that returns a structured result: a short
summary, a longer description, what action it took (if any), what it
touched, and — critically — a concrete verification probe (a command whose
exit code proves the claimed action actually happened).

**6. Sanitize before any external write.** Run every outbound piece of text
(ticket title/body, chat reply, status post) through a scrub pass for
banned terms, secrets-shaped strings, and anything that shouldn't leave the
pipeline. Refuse the write and surface the block rather than posting a
redacted-looking guess.

**7. Create the ticket, then close the loop where the signal came from.**
File the tracked work item (issue tracker, task board) with a prefix
identifying its action type and a citation back to the source chunk. Reply
where the original signal appeared with the ticket link and a one-paragraph
summary, so a human skimming the source channel sees what happened without
opening the tracker.

**8. Run the probe before claiming anything.** Execute the handler's own
verification probe from step 5. Label the outcome `VERIFIED` only if the
probe exits clean; otherwise label it `CODE-SHIPPED-NOT-VERIFIED` and say so
in the same reply. Never let "a ticket got created" read as "the work is
done."

**9. Dedup by content hash, not by message ID.** Hash each processed chunk
and check it against an audit log before acting — this catches the case
where the same content reappears under a new message ID (an edit, a repost,
a retry) and stops it from generating a second ticket.

**10. Rate-limit per run, and let the backlog carry over.** Cap how many
items a single run will process; if more qualify, defer the rest to the next
cycle instead of trying to catch up all at once. A steady trickle of tickets
beats a burst that nobody can review.

**11. Fail closed on any external API error.** If the channel read, the
transcription call, the ticket creation, or the reply post fails partway
through, log it and stop — never leave a ticket half-created or a reply
posted without its ticket link because a later step in the same item failed.

## When to use

- You have a channel, inbox, or recording stream that generates real
  signal irregularly, and want it triaged into tracked work without a human
  reading every message.
- You've tried "just let the agent watch the channel" before and gotten
  either noise (too much gets ticketed) or silence (nothing gets acted on),
  and want the scoring/classification/verification structure that fixes
  both failure modes.

## How to use

**Install:** copy this folder into `~/.claude/skills/signal-to-ticket-pipeline/`
for personal use, or into `<project>/.claude/skills/` to share it via version
control. Implement the poll/transcribe/ticket/reply steps against whichever
chat platform, transcription API, and issue tracker you actually use — the
method is the same regardless of which ones you plug in.

**Invoke:**

```
Build a signal-to-ticket-pipeline that watches this channel every few
minutes, scores messages against our project's rubric, and files a ticket
with a verification probe for anything that clears the bar.
```

```
This channel-watcher keeps double-filing the same message and has no cost
cap. Use signal-to-ticket-pipeline to add hash-based dedup, a daily spend
ceiling, and a real VERIFIED/CODE-SHIPPED-NOT-VERIFIED check before it
replies.
```
