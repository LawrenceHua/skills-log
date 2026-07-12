---
name: twilio-a2p-10dlc-compliance
description: Get a Twilio 10DLC A2P SMS campaign approved, or un-stick a rejected one — decodes the common rejection codes, gives the exact website compliance checklist, and covers the non-obvious resubmission mechanics (a FAILED campaign has no patch endpoint; you delete and re-POST).
---

# Twilio 10DLC A2P campaign compliance + resubmission

A 10DLC A2P campaign only passes carrier vetting when three things line up and are **publicly verifiable by a reviewer**: a compliant opt-in flow, a compliant Terms & Conditions page, and a compliant Privacy Policy page — and the campaign's `message_flow` text has to accurately *describe* that opt-in. Most rejections are a mismatch between what the campaign claims and what a reviewer can actually load and see.

> **Golden rule before you ever resubmit:** open the opt-in page, the Terms URL, and the Privacy URL in a private/incognito browser (no login) and confirm each one loads over HTTPS with every required element visible. If a reviewer can't see it, it fails — no exceptions.

## Step 0 — read the actual rejection first

`GET https://messaging.twilio.com/v1/Services/{MG}/Compliance/Usa2p/{QE}` and read the `errors[]` array (`error_code`, `fields`, `description`). Never guess the reason — the campaign object states it. Map the code with the table below.

## Rejection-code → fix map

| Code | Means | The fix that actually clears it |
|---|---|---|
| **30896** | Opt-in / message-flow description is inadequate | `message_flow` must state WHO opts in, WHERE (a real, live URL), and HOW (an unchecked checkbox + the exact disclosure text). Put the real opt-in page URL in the field. |
| **30923** | Consent is described as a *required* condition of service | Remove the word "required" from the consent description entirely. State the checkbox is optional and unchecked by default, and that the product works fine without SMS consent. (The single most common sole-proprietor trap.) |
| **30882** | Terms & Conditions URL missing, unreachable, or non-compliant | A public HTTPS Terms page on your own domain (not a generic terms-hosting service) containing: a program description, message frequency, "Msg & data rates may apply," STOP/HELP language, a carrier-liability disclaimer, and no bundling of SMS consent into general Terms acceptance. |
| **30908** | Privacy Policy URL missing, unreachable, or missing the SMS clause | A public HTTPS Privacy page containing the canonical SMS non-sharing clause (below) — this is the single most common privacy failure. |
| **30892** | A disallowed embedded link (a public URL shortener) | Use your own domain in message samples, not a public link shortener. |

> ⚠️ As of the current Twilio policy, `PrivacyPolicyUrl` **and** `TermsAndConditionsUrl` are mandatory API fields for every new campaign — including sole-proprietor campaigns. There's no carve-out; verify the current requirement against Twilio's own docs before submitting, since carrier rules do shift.

## The website compliance checklist

### 1. Opt-in form (clears 30896 / 30923)
Adjacent to the phone field, a separate, **optional, unchecked-by-default** SMS checkbox whose label contains all of:
- Your brand name, exactly as registered with the campaign.
- What messages are sent (a real program description).
- "Message frequency varies" (or a specific stated cadence).
- The canonical phrase **"Msg & data rates may apply."**
- "Reply STOP to unsubscribe" + "Reply HELP for help."
- Hyperlinked Privacy Policy and Terms links.

**Canonical opt-in disclosure (drop in verbatim, edit the brand/use-case):**
> ☐ I agree to receive text messages from **[Brand]** at the number provided, including [order/appointment/recap] updates. Message frequency varies. Msg & data rates may apply. Reply STOP to unsubscribe, HELP for help. See our [Privacy Policy] and [Terms].

The checkbox must not be `required` to submit the form, and SMS consent must not be bundled into general Terms acceptance. (Collecting the phone number for a *different* purpose — e.g. a phone call — is fine; the SMS consent has to be its own separate optional opt-in.)

### 2. SMS Terms page (clears 30882)
A public HTTPS page on your own domain containing: a program description, "Message frequency varies," "Msg & data rates may apply," "Reply STOP to cancel," "Reply HELP for help," **"Carriers are not liable for delayed or undelivered messages,"** no statement that opting in is required to use the service, and no statement that opt-in data is shared or sold.

### 3. Privacy Policy page (clears 30908)
A public HTTPS page containing the canonical SMS clause verbatim-ish (carriers search for this text specifically):
> **No mobile information will be shared with third parties or affiliates for marketing or promotional purposes. Text-messaging originator opt-in data and consent will not be shared with any third parties.**

Plus: what data is collected, how it's used, the opt-out mechanism, retention, a real contact method, and no conflicting second version of the policy living elsewhere on your site.

### 4. Message samples
2-5 samples, 20-1024 characters each, each containing your brand name; at least one showing "Reply STOP to unsubscribe"; all matching your stated use-case; flag `has_embedded_links`/`has_embedded_phone` truthfully if any sample contains one; use `[Brackets]` for template variables. Sole-proprietor campaigns are limited to a single number on the campaign.

### 5. STOP / HELP
Twilio's carrier-level opt-out handling (enabled at the messaging-service level) auto-handles STOP/UNSTOP/HELP and satisfies the carrier requirement on its own. If you handle opt-out in your own application code instead, you must implement immediate STOP removal plus a HELP auto-reply yourself — either way, the carrier layer honors STOP regardless of what your app logic does.

## Resubmission mechanics (the non-obvious part)

- A **FAILED** campaign has **no PATCH endpoint and no resubmit sub-resource.** To correct it, you **delete the campaign and re-POST** a corrected one under the same messaging service. Deleting the campaign does **not** affect your Brand registration or Messaging Service — only the campaign itself needs re-registering.
- **Prefer editing the campaign in the Twilio Console** when the field you need to fix is edit-eligible: editing keeps the same campaign and is assessed the vetting fee only once. Deleting and re-POSTing via the API triggers a **new** vetting fee (typically a few dollars for a sole-proprietor campaign). There's no attempt limit and no cooldown either way.
- Fields you can usually change via edit: description, message_flow, samples, privacy URL, Terms URL. Fields that require delete + recreate: use-case, messaging-service SID, brand SID.

**API re-POST template** (pull credentials from environment variables — never hard-code them):
```bash
source ~/.twilio-creds.env   # sets TWILIO_ACCOUNT_SID / TWILIO_AUTH_TOKEN
curl -s -X POST \
  "https://messaging.twilio.com/v1/Services/{MG}/Compliance/Usa2p" \
  -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN" \
  --data-urlencode "BrandRegistrationSid={BN}" \
  --data-urlencode "UsAppToPersonUsecase=SOLE_PROPRIETOR" \
  --data-urlencode "Description=<specific: who sends, who receives, why>" \
  --data-urlencode "MessageFlow=<opt-in described: URL + unchecked optional checkbox + disclosure; state consent is NOT required to use the service>" \
  --data-urlencode "MessageSamples[0]=<brand + opt-out language>" \
  --data-urlencode "HasEmbeddedLinks=true" \
  --data-urlencode "HasEmbeddedPhone=false" \
  --data-urlencode "OptOutKeywords[0]=STOP" --data-urlencode "OptOutMessage=You're unsubscribed from {Brand}. Reply START to resubscribe." \
  --data-urlencode "HelpKeywords[0]=HELP" --data-urlencode "HelpMessage={Brand} help: <what it does>. Questions? <email/URL>. Reply STOP to unsubscribe."
```
Then poll `campaign_status` (`GET .../Usa2p/{newQE}`) until it reaches `VERIFIED` (sole-proprietor campaigns: hours to a few days).

## Pre-submit verification gate (run this every time)

1. Read `errors[]` and fix the *named* field — don't guess.
2. `curl -sI` the Privacy and Terms URLs — expect `200` over HTTPS, no redirect to a 404 or a login wall.
3. Grep the live Privacy page for the canonical non-sharing clause — it needs to be present near-verbatim.
4. Confirm the opt-in checkbox is optional and unchecked by default, and the disclosure has all six required elements.
5. Confirm `message_flow` states consent is **not required** to use the service (this specifically clears 30923).
6. Only then submit — a re-submission is billable, so get it right the first time.

## Operational safety when investigating a campaign via the API

Twilio's REST credentials are read+write+**delete** — there's no read-only scope on account-SID/auth-token basic auth. If you delegate an investigation to an agent or subagent, explicitly forbid POST/PUT/DELETE and have it print the commands it *would* run rather than executing them. "Read-only" as an instruction is not a real guardrail when the credential itself can execute anything — a real incident happened where an investigation agent deleted a live campaign while "demonstrating what a DELETE would return."

## How to use

**Install:** copy this folder into `~/.claude/skills/twilio-a2p-10dlc-compliance/` for personal use, or `.claude/skills/twilio-a2p-10dlc-compliance/` inside a project repo.

**Invoke:**

```
Our Twilio A2P campaign just got rejected with error 30908. Use
twilio-a2p-10dlc-compliance to tell me exactly what's wrong and what to fix.
```

```
Walk me through the full website compliance checklist from
twilio-a2p-10dlc-compliance before I submit a new sole-proprietor campaign.
```
