---
name: graph-engineering
description: Design multi-agent work as a real directed graph instead of a chain — bounded nodes with explicit input/output contracts, edges only for genuine data dependencies, a fan-out/reduce/synthesize pattern, and isolated verifiers that never share context with the work they're checking.
---

# graph-engineering

A methodology for orchestrating agent work as a directed graph, not a chain of vibes. Most multi-step agent workflows default to a long sequential chain because that's the easiest thing to write — but a 40-step chain is the worst possible shape: 40 sequential failure points and zero parallelism, when most of those steps don't actually depend on each other.

## Nodes and edges

- **A node is one bounded job with an explicit input/output contract.** Declare exactly what it receives and exactly what it must return — specific fields, `file:line` references, an exit status — never a wall of free text passed between nodes with no contract on either end.
- **An edge is a real data dependency, and only that.** Apply the fake-edge test: if step B doesn't actually consume step A's output, there is no edge between them — run them in parallel instead. Most chains have far fewer real edges than their author assumed.

## The diamond pattern

1. **Fan out** — one worker per independent angle or subsystem, breadth-first.
2. **Reduce with plain code** — merge, dedupe, count, and filter the intermediate results with a script or deterministic logic. This step is free: it costs no model context and introduces no judgment error.
3. **Synthesize once** — a single node consumes the reduced results and produces the final artifact.

Intermediate fan-out results stay in the orchestration layer — files, tool outputs, scratch state — never dumped raw into the orchestrator's own context. The orchestrator should see digests and pointers, not the full output of every worker.

## The verifier rule

A worker and its verifier must never share a context. A verifier that read the worker's own reasoning inherits the worker's blind spots along with it — a graph where every node shares one context is just a single loop wearing a costume. Give every checker a fresh context and three questions to answer:

1. **Correct?** — does the claim actually hold against the artifact itself?
2. **Current?** — does it hold against live state right now, not a stale snapshot?
3. **Source real?** — is the cited evidence (a file, a line, a command's actual output, a URL) genuine and checkable?

Default stance for any verifier: refute first — treat the claim as broken until it survives a real check, not the other way around.

## Failure modes and fixes

| Failure mode | What happens | Fix |
|---|---|---|
| Context collapse | The orchestrator drowns in raw fan-out output | Batch-summarize at fan-in; keep raw results in the orchestration layer, pass only digests onward |
| False independence | "Parallel" nodes secretly share mutable state (same working directory, same DB row, same lock) and corrupt each other | Isolate each node's workspace; audit shared *resources*, not just data flow |
| Silent node failure | A node dies or returns empty and the merge step quietly proceeds with fewer inputs than expected | Have the merge step count expected vs. received inputs and fail loudly on any gap |

## Anchors

Goals and plans should terminate on non-arguable signals — a named test that actually ran and passed, a command that exited 0, a file that exists with the expected content — never on "looks done." Some things stay frozen off-limits from optimization entirely: safety gates, permission boundaries, and any cost/scope guard are not knobs a node is allowed to tune just to reach its anchor faster.

## When NOT to graph

- Small or isolated tasks — a graph is pure orchestration overhead when there's no real breadth to buy.
- Approval-heavy work with a human gate between most steps.
- Exploratory work where the next step genuinely depends on a human's read of the last one.
- Truly sequential work where every step really does consume the previous step's output — that's an honest chain, not a graph in disguise.

A graph buys breadth, not better judgment: parallel nodes trade tokens for wall-clock time, and adding more agents never fixes a wrong goal. Right-size the fan-out to the actual blast radius of the task — a handful of readers for a local change, one node per subsystem for a migration, never a fleet for a one-file edit.

## When to use

- Orchestrating any fan-out of agents, subagents, or automated multi-step work.
- Designing a review, audit, or verification pipeline where independent checks shouldn't contaminate each other.
- Reviewing an existing agent pipeline that's slow or unreliable — check it for hidden fake edges and shared-context verifiers first.

## How to use

**Install:** copy this folder into `~/.claude/skills/graph-engineering/` for personal use, or `.claude/skills/graph-engineering/` inside a project repo.

**Invoke:**

```
Before you build this multi-agent pipeline, apply graph-engineering — map
the real edges first and tell me which steps can actually run in parallel.
```

```
Review this agent workflow against graph-engineering's verifier rule — is
any checker sharing context with the work it's supposed to be checking?
```
