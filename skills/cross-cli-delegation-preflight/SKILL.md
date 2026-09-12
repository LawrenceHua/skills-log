---
name: cross-cli-delegation-preflight
description: Operational hygiene rules for delegating work across multiple local AI CLIs or backends — a secretless read-only probe before any cross-tool call, a free-tier-first default, opaque aliases instead of real identifiers, and scoped, idempotent grants for any mutation triggered from a secondary surface.
---

# cross-cli-delegation-preflight

Once you're routing work across more than one AI CLI or backend — a paid frontier model plus a local/free model, a phone-triggered automation plus your main session — the failure modes stop being "which model is smarter" and start being operational: a misconfigured secondary backend silently eats real work, real usernames leak across a tool boundary that assumes they're private, or a mutation triggered from a phone gets executed twice. These are a fixed set of hygiene rules that apply regardless of which backends you're actually using.

## The method

1. **Probe before you commit.** Before routing real work to a secondary CLI or backend, send a cheap, secretless, read-only request first — a trivial status check or a simple question — to confirm the backend is actually reachable and correctly configured. Discovering a broken connection *after* handing off real work wastes the work.
2. **Default to the free or already-funded lane.** Unless the task's complexity clearly needs a paid or higher-capability backend, route to the free/local lane by default and escalate only when the task genuinely warrants it. This keeps routing decisions from silently drifting toward the most expensive option out of habit.
3. **Keep subscription-bound work in its native tool.** If a backend's capability comes from a personal subscription or license tied to its own CLI, don't try to proxy that work through a different tool just because it's more convenient to call from there — run it natively where the entitlement actually lives.
4. **Never pass real identifiers across a tool boundary.** When one tool's output references an account, username, or internal ID, translate it to an opaque alias before handing it to a different tool or surface. A leak in one system shouldn't expose identifying detail that originated in another.
5. **Gate mutations from secondary surfaces behind scoped, idempotent grants.** If a mutation (not just a read) can be triggered from a secondary surface — a phone-triggered command, a delegated agent acting on your behalf — require an explicit, scoped permission grant for that specific action, and make the action idempotent so a duplicate trigger (a retried request, a double-tap) can't execute it twice.

## When to use

- Any setup that routes tasks across more than one AI CLI or backend and needs consistent safety hygiene regardless of which one ends up doing the work.
- Adding a second CLI or a remote/mobile trigger surface to an existing single-agent setup.
- Reviewing an existing multi-backend routing setup for the specific gaps above — an unverified connection, identifier leakage, or a non-idempotent remote-triggered mutation.

## How to use

**Install:** copy this folder into `~/.claude/skills/cross-cli-delegation-preflight/` for personal use, or `.claude/skills/cross-cli-delegation-preflight/` inside a project repo.

**Invoke:**

```
Before delegating this to the other backend, run cross-cli-delegation-preflight — a
cheap connectivity probe first, and make sure my real username isn't passed across.
```

```
Review our phone-triggered automation against cross-cli-delegation-preflight — is
the mutation it triggers actually idempotent and scoped?
```
