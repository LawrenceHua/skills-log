---
name: paid-mcp-server-billing
description: Design and verify billing for a paid MCP server, with paid access that fails closed, atomic per-tool quotas, safe payment webhooks, negative-control tests and human approval before live billing changes.
---

# Paid MCP server billing

Charging for an MCP server adds three ways to fail: paid tools run for people who have not paid, paying users are locked out or charged twice, and a looping client runs up a large bill. This skill designs against all three. Check current MCP and payment-provider documentation for exact names and fields, because both change.

## 1. Write the tier contract first

| Tier | Access and limits | Billing | At the limit or after lapse |
|---|---|---|---|
| Free | key or sign-in, daily and monthly caps, low-cost tools | none | refuse with the reset time and an upgrade link |
| Subscription | scoped key or token, larger allowance | recurring plan with a self-service billing page | refuse paid tools; allow a grace period only if you defined one |
| Usage-based | account-scoped keys and usage counters | metered billing | stop at a hard spend ceiling |

Let a new user get a real result before paying. For each tool, write down its tier and usage weight.

Prevent double subscriptions. Keep one provider customer per account, and do not assume that checkout blocks a second purchase. If a subscription is active, trialing, past due or incomplete, send the user to manage it. Also guard against two checkouts open at once, for example by reusing one pending checkout session per account.

## 2. Check access on every tool call

- Decide access on the server. Never trust a tier or customer id sent by the client.
- API keys: generate long random values, store only a hash, show the raw key once, and support rotation and immediate revocation. Compare secrets in constant time.
- Tokens: validate signature, issuer, audience, expiry and scope.
- On remote servers, follow the current MCP authorization specification for missing or invalid credentials (normally HTTP 401) and for insufficient scope (normally 403).
- Allow only listed subscription states. An unknown state, a lookup error or a database timeout refuses paid access.
- If you cache access decisions, set a short lifetime and clear the entry on revocation and billing changes.

## 3. Reserve quota before doing costly work

- Reserve the tool's weight in one atomic operation that succeeds only if usage stays within the limit, such as a single conditional update. A separate read then write lets parallel calls overspend.
- Give each call an idempotency key scoped to the account. A JSON-RPC request id alone is not unique across sessions. Insert the key under a unique constraint **in the same transaction** as the quota update, so two simultaneous retries cannot both reserve. If either step fails, roll back both.
- Store the tool name and a hash of the arguments with the key, and reject a key reused for a different request.
- A duplicate of a call still in progress gets an in-progress conflict. A repeat of a finished call returns the stored result or a clear conflict. Neither runs the costly work or charges again.
- Decide in advance whether a failed or timed-out upstream call is refunded, kept or reconciled later.
- Return a quota or plan refusal as a tool result marked `isError: true`, so the model can see and act on it. Include a code such as `QUOTA_EXCEEDED`, the retry or reset time and the upgrade link. Keep JSON-RPC protocol errors, whose codes are integers, for protocol problems such as an unknown tool or a malformed request. Authentication failures and transport-level rate limits (HTTP 429) are handled at the HTTP layer. Confirm this against the specification version you target.
- Do not include stack traces, keys or internal host details in errors.

## 4. Treat webhooks as unordered and repeatable

1. Verify the provider's signature against the raw request body, using the provider's library and its timestamp tolerance. Keep the signing secret in a secret store.
2. Record the event id under a unique constraint **in the same transaction** as the resulting change. If you record it first and then crash, the retry is skipped and the change is lost.
3. Do not assume arrival order. For subscription state, read the current object from the provider, or reject updates that are older than what you hold. An old "active" event must not restore a cancelled account.
4. If processing fails, return a failure status so the provider retries.
5. Handle checkout completion, delayed payment success and failure, invoice paid and failed, and subscription updated and deleted. A completed checkout does not always mean money was received, so check the payment status.
6. Reconcile on a schedule against the provider's records to catch missed events.

For usage billing, use the provider's current metering interface. Send each usage record with a stable unique identifier, queue and retry failed sends, learn the provider's deduplication window, and compare your ledger with the invoiced usage.

## 5. Verify with negative controls

Run in the provider's test mode. Replay or trigger webhooks with its command-line tool where available.

| Case | Required result |
|---|---|
| no key, bad key, revoked key | refused |
| free key calls a paid tool | refused |
| parallel calls with different keys at one unit below the limit | exactly one succeeds (unit-weight tool) |
| the same key sent twice in parallel | one reservation and one run |
| the same key reused with different arguments | rejected |
| checkout completed with payment still pending | no paid access until payment succeeds |
| two upgrade attempts at once | at most one subscription |
| tampered or unsigned webhook | rejected with no state change |
| same event delivered twice | one change |
| older event after cancellation | stays cancelled |
| crash during webhook handling | retry applies the change once |
| database or provider lookup fails | paid tools refused |

Then probe the deployed endpoint without spending: tool listing, one free call and the refusal paths. A live paid call is run by a person. Report test-mode results as test-mode results.

## 6. Human gate

Get explicit approval before changing live prices, products, payouts or webhook endpoints, switching to live mode or spending on promotion.

## Never

- Never grant paid access because a check failed or a signing secret is missing.
- Never log payment keys, signing secrets, customer keys or bearer tokens.
- Never mix data or credentials from unrelated projects or organizations.

## When to use

- You are adding paid tiers or usage limits to an MCP server.
- You are reviewing entitlement, metering or webhook code before launch.
- Customers report wrong access or doubled usage.

## How to use

1. Copy the `paid-mcp-server-billing` folder into `~/.claude/skills/` for personal use, or `.claude/skills/` inside a project.
2. Ask Claude Code to use the skill by name.
3. Example prompts:
   - "Use the paid-mcp-server-billing skill to add a free tier and one subscription tier to my MCP server. Use test mode only."
   - "Use paid-mcp-server-billing to review my webhook handler for lost, repeated and out-of-order events."
