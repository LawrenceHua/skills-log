---
name: code-graph-blast-radius
description: Before editing a shared symbol, class, file, or module, query a code-dependency-graph tool for its actual upstream callers/importers instead of relying on grep alone, then compare what you actually changed against the predicted blast radius afterward.
---

# code-graph-blast-radius

Grep tells you where a name appears as text. It doesn't tell you which of those appearances are load-bearing callers versus comments, string literals, or unrelated shadowed names, and it can't rank them by how directly they depend on what you're about to change. A code-dependency-graph tool — several exist as MCP servers, IDE plugins, or standalone CLIs — answers a different, more useful question: "if I change this, what actually breaks, and how directly?"

## The method

**1. Before a risky edit to a shared symbol, class, file, or module, query the graph for its dependents (upstream impact), not just its definition.** Prefer a live query tool (an MCP server or equivalent) exposed in your current session over a raw CLI invocation when both are available — it's faster and keeps the query in context.

**2. Read the result by depth, not as an undifferentiated list:**
- **Depth 1** — direct callers/importers. Plan an update or at least a review for every one of these before you finalize the edit.
- **Depth 2** — likely affected. Identify which tests or manual smoke-checks would catch a regression here.
- **Depth 3+** — the broad regression surface. Sample rather than exhaustively review, but don't ignore it entirely for a genuinely shared utility.

**3. Treat "risk unknown" as unsafe, not as "probably fine."** If the graph tool can't prove low risk for a given edit (a dynamic call site, a stale or partial index, an unindexed language feature), that's a signal to fall back to a manual, more conservative review of that specific spot — not to proceed as if grep-level confidence were sufficient.

**4. Keep the index current before trusting it.** A stale index gives you a confident, wrong answer. If the tool supports a refresh/re-index command, run it (respecting any project convention for when that's safe to do) before relying on a query for a genuinely risky change.

**5. After the edit, close the loop.** Compare the files you actually changed against the blast radius the graph predicted. If files outside the predicted set changed, or if direct (depth-1) dependents were never touched by your test run, say so explicitly before calling the change finished — that mismatch is itself a finding, not a footnote.

## When to use

- Before refactors, renames, or signature changes to anything used outside its own file.
- Before editing a shared utility, base class, or config schema whose consumers you don't have memorized.
- Debugging an unfamiliar codebase's data/control flow, where "grep and guess" would take much longer than a graph query.
- Any time someone asks "what could break if I change this" and the honest answer requires more than a text search.

## How to use

**Install:** this pattern applies to whatever code-graph tool you already have available — an MCP server exposing query/impact/context tools, or a CLI that builds and queries a dependency index for your repo. If you don't have one yet, most language ecosystems have at least one open-source option (call-graph generators, LSP-based reference finders, or dedicated code-intelligence indexers).

**Invoke:**

```
I'm about to rename this shared function. Use code-graph-blast-radius to find
every direct and indirect caller before I touch it, and flag anything the graph
can't prove is low-risk.
```

```
I just finished this refactor — run code-graph-blast-radius's after-edit check:
did the files I actually changed match the predicted blast radius, and did my
tests cover the depth-1 callers?
```
