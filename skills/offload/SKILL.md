---
name: offload
description: A cost-optimization router for offloading self-contained work off your primary AI assistant's metered quota and onto a secondary backend you already have (a flat-rate CLI coding agent, a local/free model, or a trusted automation you run yourself) — then verifying the result yourself instead of trusting the self-report.
allowed-tools: [Bash, Read, Write, Edit, Grep, Glob]
---

# offload

Most people run more than one AI backend: a primary metered assistant, plus
often a flat-rate subscription CLI tool, a local/free model, or an
automation you've already built and trust for narrow, recurring tasks. When a
piece of work is genuinely self-contained, route it to whichever backend is
cheapest *while still clearing the task's quality bar* — and keep the
conclusion, not the token cost, on your primary assistant's budget.

**Quality is the hard constraint.** The goal is not "always pick the
cheapest option" — it's "pick the cheapest backend that can actually do
this job well," and then verify its output yourself regardless of which
backend produced it.

## When to use

- You're low on your primary assistant's usage/credits, or spend is capped,
  and a piece of work doesn't need this exact conversation's full context.
- A **self-contained sub-task** can run on its own: a focused fix, a
  scaffold, a refactor, a research question, a forensic investigation, a
  code review.
- You want an **independent second opinion** — a different model family or
  a fresh context is genuinely useful, not just cheaper.
- You want to **parallelize** — offload one piece while you keep working on
  another.

**Skip it for:** tiny edits you'd finish faster doing yourself inline, work
that genuinely needs this conversation's accumulated context, or any
outward-facing/irreversible action without an explicit human approval gate.

## Decision matrix — which backend for which job

| Backend type | Best for | Typical cost model |
|---|---|---|
| **A flat-rate CLI coding agent** (e.g. a subscription-based coding CLI you already pay for) | Hard, code-heavy, or investigative work: forensic repo analysis, deep code review, multi-step autonomous refactors, research that needs shell access. Usually the strongest reasoning of the three. | Flat subscription — verify you're authenticated via the subscription, not an API key that bills per-token |
| **A local or free-tier agent tool** (an MCP-connected local model, a cheap-API coworker) | General self-contained sub-tasks: a fix, a scaffold, a focused refactor, a research question. Fastest to fire — usually a single tool call. Good default when the task is well-scoped and not maximally hard. | Free or near-free |
| **A trusted recurring automation** you've built for a narrow task family (health checks, cleanup, data refresh, research digests) | Internal, repetitive task families where you've already earned trust through a track record of correct, verifiable output | Whatever compute it runs on — usually the cheapest per-run |

Rule of thumb: **investigation or the hardest code → the flat-rate CLI
agent; a general scoped task → the cheapest agent tool you have; a proven,
narrow, recurring family → your own trusted automation.** When unsure
between the first two, try the cheaper one first and escalate only if it
needs more horsepower or shell-driven investigation.

## How to invoke a backend

The exact mechanics depend on what you've set up, but the shape is always
the same:

1. Write the task/prompt to a file (or pass it directly if your tool
   supports inline prompts).
2. Point the backend at the right working directory and, if it can write
   files, the right sandbox/permission mode — read-only for delicate or
   shared state, write-enabled only for an isolated workspace you're
   comfortable with it touching.
3. For long-running jobs, kick them off in the background and come back to
   read the report when it's done, rather than blocking on it.

**Safety note on any backend with a "bypass guardrails" mode:** if a
backend supports a full-bypass/no-sandbox mode, that mode removes its own
safety net — the *prompt* becomes the only guard. Reserve it for isolated
environments, and always open the prompt with an explicit forbidden-action
list (no destructive git operations, no edits outside the intended
directory, no reading secrets) when running read-only investigation against
anything shared or delicate.

## Always — verify, don't trust the self-report

Offloaded agents self-attest success, and self-attestation is exactly the
thing that can quietly go wrong (an automated agent can report "done"
without having actually done it correctly). After any offload:

1. **Read the actual artifact** the backend produced — the report file, the
   diff, the return value — don't relay a summary you didn't open yourself.
2. **Re-verify the checkable claims** with your own tools: run the test,
   grep the file, diff against the base, hit the endpoint — whatever
   applies.
3. If it touched files, confirm the diff is what you expected and nothing
   unexpected leaked in.

## Report-back pattern

Offload → the backend writes to a file (or returns a result) → **you** read
it, independently verify the key claims, and only then relay the verified
conclusion plus a recommended next action. The offloaded output is input to
your judgment — never the final word on its own.

## How to use

**Install:** copy this folder into `~/.claude/skills/offload/` for personal
use, or `.claude/skills/offload/` inside a project repo. This skill
describes a decision process, not a specific vendor integration — adapt the
"how to invoke" mechanics to whichever secondary backend(s) you actually
have configured (a CLI tool, an MCP server, a local script).

**Invoke:**

```
I'm low on quota this month — offload the forensic investigation of why
this endpoint intermittently times out to my flat-rate coding CLI, then
read its report back and verify the root cause yourself before we act on it.
```

```
This refactor is well-scoped and not that hard — offload it to whatever
local/cheap agent I have configured, then diff the result and confirm the
tests still pass before you tell me it's done.
```
