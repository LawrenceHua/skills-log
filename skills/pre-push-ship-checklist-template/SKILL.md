---
name: pre-push-ship-checklist-template
description: A six-gate checklist for shipping a change to any stateful service — ownership map, multi-source rule audit, structural gate, regression replay, safe restart, and one real end-to-end smoke test — run before every push.
---

# pre-push-ship-checklist-template

A green unit-test suite tells you the code you wrote does what you meant it to do in isolation. It does not tell you that you edited the right copy of a duplicated rule, that the service will restart cleanly with the new code, or that the live system actually behaves differently for a real interaction. For a long-running, stateful service (a voice or chat agent, a background daemon, an API gateway), the gap between "tests pass" and "shipped correctly" is exactly where the expensive bugs live. This is a fixed six-gate checklist to close that gap before every push, not just the risky ones.

## The method

Run these six gates, in order, before pushing a change to a stateful service:

1. **Consult the ownership map first.** Before editing, identify which module actually owns the behavior you're changing. Services accumulate near-duplicate logic over time; editing a downstream copy instead of the source of truth is a common way to "fix" a bug that then reappears.
2. **Audit every source-of-truth location for the changed rule.** Search the whole codebase for every place the same fact, prompt phrase, config value, or constant is duplicated, and update all of them. A fix that only touches one of three copies isn't a fix — it's a new inconsistency.
3. **Run the structural pre-push gate.** A scripted check — lint, schema validation, an import-graph check, a config-shape validator, whatever your project already has — that catches structural breakage mechanically, before a human or CI has to.
4. **Replay the regression suite.** Run your accumulated set of "bugs that already happened once" fixtures and require the pass count to stay at or above the current ceiling. A previously-fixed bug reopening silently is the single most avoidable class of regression.
5. **Restart the service via its documented state-preserving method — never a raw kill.** Use the graceful-restart path so in-flight requests, caches, or connections drain properly instead of getting force-terminated mid-transaction.
6. **Place one real end-to-end interaction before calling it shipped.** Actually exercise the live path — a real API call, a real test message, a real request through the deployed system — and check for the specific behavioral markers you expect. This is the gate that catches "the tests passed but the live system doesn't do what the tests assumed."

Treat all six as mandatory for every push to the service, not just large changes — the cost of running them is small and fixed; the cost of skipping one on the change that turns out to need it is not.

## When to use

- Shipping any change to a long-running, stateful service where a broken deploy is expensive or embarrassing to notice after the fact.
- Building a "ship checklist" for a project that doesn't have one yet — this is a reasonable default shape to start from.
- Reviewing why a bug reached production despite a passing test suite — check which of the six gates was skipped.

## How to use

**Install:** copy this folder into `~/.claude/skills/pre-push-ship-checklist-template/` for personal use, or `.claude/skills/pre-push-ship-checklist-template/` inside a project repo.

**Invoke:**

```
Run this change through the pre-push-ship-checklist-template before we push — start
with the ownership map and don't skip the live end-to-end check.
```

```
We shipped a bug last week despite green tests — use pre-push-ship-checklist-template
to figure out which gate would have caught it, and add it to our actual pipeline.
```
