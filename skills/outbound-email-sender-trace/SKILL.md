---
name: outbound-email-sender-trace
description: Work out read-only which path and client sent an email from your own mailbox, using provider-added headers, send receipts and recorded approvals, and rule whether it was cleared, bypassed a gate or looks like compromise.
---

# Outbound email sender trace

When scripts and agents can send from your mailbox, an unexplained message in Sent needs an evidence-based answer: which path carried it, which of your senders used that path, and whether it was allowed.

This skill is for mailboxes you own or are authorised to investigate. It reads only.

## 1. Collect the message

Use read tools only. Fetch the raw message or all headers. Record the message id, the `Date` header, the provider's own timestamp if available, and your local time.

## 2. Identify the submission path

Read `Received:` headers from the top down and find the **earliest hop added by your mail provider**, where the message entered its systems. Anything below that line arrived with the message and can be forged by whatever submitted it.

Patterns commonly seen on Gmail (other providers differ):

| Entry hop | Likely path |
|---|---|
| `from <number> named unknown by gmailapi.google.com with HTTPREST` | HTTP API; the number usually identifies the API client's cloud project |
| `by smtp.gmail.com with ESMTPSA`, from an external address | authenticated SMTP, using an app password or an OAuth token; this line alone does not say which |
| no API or SMTP submission hop | possibly the web or mobile app; confirm with a known sample |

These are observed formats, not a guarantee. Before relying on them, compare against one message you know came from each path. If you have no such sample, label the path `probable`.

Supporting signals only: `Message-ID` format, client or mailer headers, MIME boundary style, mailbox labels, whether it started a new thread. The `Date` offset is stamped by the sender and proves nothing about location.

## 3. Check account access

Search the same mailbox, read-only, for security notices since your last review: app password created, new app access granted, new sign-in. If SMTP was used from an outside address, compare that address with the public addresses of your own machines, read live.

## 4. Match a sender

1. Map the API client number or submission address to your **known-sender table**. Anything absent from the table is unknown.
2. Search action logs and send ledgers in a window of a few minutes around the send. A strong match ties message id or body hash, recipient and time.
3. With no receipt, write "sending process not identified". Do not guess from writing style.

## 5. Check clearance

Look for a recorded approval that names this message or campaign, in the approver's own words, dated before the send. An agent saying it was approved is not an approval. If two records conflict, apply the stricter one.

## Ruling

| Ruling | When |
|---|---|
| `CLEARED` | known sender, matching receipt, approval covers it |
| `CLEARANCE-UNPROVEN` | known sender and receipt; approval is cited but the original words are not on record |
| `GATE-BYPASS` | known sender, no approval covering it |
| `COMPROMISE-SUSPECTED` | unknown client or address, or content outside every known workflow |
| `UNDETERMINED` | headers, logs or approvals could not be read |

Escalate `COMPROMISE-SUSPECTED` immediately and recommend the account owner review access from the provider's security page. Escalate `GATE-BYPASS` to whoever owns the sender.

For marketing mail, also note missing legal basics that apply to you, such as a postal address and a working opt-out.

## Report line

`<ruling> | mailbox <alias> | message <id> <time> | path <API client / SMTP / app, certain or probable> | sender <name or not identified> | approval <reference or none>`

## Never

- Never send, reply, forward, label, archive or delete anything during the trace.
- Never copy body text or personal addresses into reports; use ids, times and business domains.
- Never revoke access, change passwords or disable jobs yourself. Recommend it to the owner.
- Never contact the recipient.

## When to use

- An email appears in Sent that no person or agent admits sending.
- A send hold may have been bypassed.
- Auditing which automations sent a campaign.

## How to use

1. Copy the `outbound-email-sender-trace` folder into `~/.claude/skills/` for personal use, or `.claude/skills/` inside a project.
2. Ask Claude Code to use the skill by name.
3. Example prompts:
   - "Use the outbound-email-sender-trace skill on message <id> in my sent folder. My send logs are in `<folder>`."
   - "Use outbound-email-sender-trace to check whether yesterday's batch went through an approved sender."
