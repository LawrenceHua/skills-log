---
name: tool-refusal-and-timeout-handling
description: Tell a deliberate tool refusal from an outage, and never blindly retry a mutating call that timed out — read the state first, probe a surface before routing around it, and date every recorded limit.
---

# Tool refusal and timeout handling

A refusal is not an outage and not a bug in your prompt: it is the deployment telling you which door is locked. The cost of not knowing is one wasted turn per incident, plus — in the timeout case — a duplicated mutation. This is the short list of rules.

## 1. Read a refusal once, and date it

Call the surface once, quote the exact error string, record the date. A refusal you have written down is knowledge; one you re-discover every session is a tax. A recorded refusal is true only for the deployment that produced it, so keep the date and re-probe before citing it.

## 2. Arguments that fail before execution

- Missing a required field (a shell tool that wants both a command and a description, say) fails before anything runs. Schema errors are free to retry — fix the field and resend.
- Read tool arguments from session logs as the type they were stored in: some are JSON strings that must be parsed before keys can be read, or every argument looks absent.

## 3. The dangerous class: it may already have run

Three results look alike and are not the same:

| result | what you know |
|---|---|
| "timed out after N ms" | the call was cut off; **the command may have completed** |
| "aborted" | cut off by the session; same uncertainty |
| "interrupted, no result durably recorded" | the call was recorded; the outcome was not |

Before retrying a *mutating* command after any of these, **read the state it would have changed, where the effect would show**. For outward effects that is not the working tree: a deploy is proven by the version the service reports (`curl -s <service>/health`), a post by the channel's newest id, a push by the remote ref. One cheap read, then retry only what is actually missing. A blind retry of an append, post, deploy, or payment is a duplicate, and the duplicate is silent.

If the effect has no readable state at all, you cannot verify the retry is safe: label the outcome `UNKNOWN`, retry only through an idempotency key or a documented reconciliation, and say so.

A *read-only* call is the counter-case: retry freely, and make it cheaper (smaller output, narrower query) so it does not time out again. Distinguishing the two is the whole rule.

## 4. Structure, not permission

- **Subagent or teammate caps are intentional.** At the cap, use fewer, better-briefed workers or a batch workflow that does not consume team slots; do not spawn around it.
- **Some operations require a human turn** (editing or pausing a goal, for example). From an agent turn they return a refusal. Do not try to fix state programmatically — it is a contract, not a permission you can route around.
- **Explicit-request-only features stay explicit.** An agent that fans out dozens of subagents on its own initiative has replaced the owner's judgment with its own.

## 5. Dead addresses after a compaction or restart

Messaging a teammate that was listed as inactive often fails because the target's session is gone, not because of the message.

- "Inactive" means no turn is executing — not finished, not failed, and not reachable.
- List agents first and treat a target as addressable only if the list returned it this turn.
- A dead target is not a blocker: do the work, or spawn one fresh member with a complete brief. Do not resend the same message to three names hoping one lands.

## 6. A gap in history is not a current absence

A fetch tool may have failed for a stretch because of a misconfigured endpoint and work fine now. An agent that read only the failures would route around an available tool; one that read only the successes would use an unavailable one. **Probe a surface once before routing around it**, and re-probe before citing its state. Anything you write down about a surface is a snapshot.

```sh
curl -sI https://example.com | head -1     # a fetch-capable surface should return a 200
```

When a probe disagrees with a written note, the probe wins and the note gets a dated correction.

## Never

- Never retry a timed-out mutation without reading the state first.
- Never conclude a capability is missing from a transcript, including a transcript of your own failures; probe it.
- Never route around a required argument or a structural cap with a workaround (a heredoc to simulate an edit, a third-party post to simulate a team message). The cap encodes an intent someone had.
- Never resend to a target the current agent list did not return.
- Never write "the tool is broken" without the error string, the date, and the one command that reproduces it.

## When to use

- A tool call returns "disabled in this deployment", "missing required property", "limit reached", "requires a direct human turn", "timed out", "aborted", or "unavailable".
- Before retrying anything that timed out.
- Before writing a note about what a tool can or cannot do.

## How to use

1. Copy the `tool-refusal-and-timeout-handling` folder into `~/.claude/skills/` (personal) or `.claude/skills/` inside a project, then ask Claude Code to use the skill by name.
2. Example prompts:
   - "My deploy command timed out. Use tool-refusal-and-timeout-handling to check whether it actually ran before I retry."
   - "Use tool-refusal-and-timeout-handling to write a dated list of the tool limits we hit this session, with the exact error strings and a probe command for each."
