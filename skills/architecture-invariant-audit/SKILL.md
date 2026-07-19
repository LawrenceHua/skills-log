---
name: architecture-invariant-audit
description: A read-only, dependency-free script that checks a layered codebase against documented architecture rules (layer crossings, legacy reuse, anti-pattern regressions, doc drift) and fails CI when they're violated.
---

# architecture-invariant-audit

Architecture decisions rot the moment nobody re-checks them — "core never imports adapters" survives exactly until someone under deadline pressure adds the import. A small, deterministic, standard-library-only script that encodes your team's actual rules as executable checks turns "we agreed not to do that" into a merge gate instead of a hope, and it runs in under a second on every commit because it never calls an LLM.

## Method

1. **Pick your layers.** Name the directories that form your dependency order (e.g. `core/` → `adapters/` → `pipelines/`) and write down, in one sentence each, which direction imports are allowed to flow.
2. **Encode each rule as an independent, single-purpose check function.** Each check returns a list of findings (severity, file:line evidence, one-line suggested fix) and nothing else — no shared mutable state, no repo mutation.
3. **Rank and print findings**, most severe first, then emit a PASS/FAIL summary line.
4. **Set the exit code from severity only**: 0 if zero ERROR-level findings, 1 otherwise. WARNING findings never fail the build on their own.

| Rule | Severity | Catches |
|---|---|---|
| `no_layer_crossing` | ERROR | inner layer (`core/`) importing from an outer layer (`adapters/`, `pipelines/`) |
| `no_legacy_reuse` | ERROR | new adapter code importing the legacy module it's supposed to be replacing |
| `legacy_shrinking` | WARNING then ERROR | the file(s) being strangled out growing instead of shrinking, checked against a stored watermark |
| `no_regressed_anti_pattern` | ERROR | a previously-fixed anti-pattern (e.g. inline multi-line string building outside its one helper) reappearing elsewhere |
| `missing_tests_dir` | WARNING | a top-level package with no `tests/` dir or no real test file in it |
| `policy_prompt_drift` | WARNING | a prompt/instructions file that no longer mentions constants a policy module enforces |

**Implementation notes per check type:**

- **Layer crossing / legacy reuse (import-graph scanning):** parse each file with your language's AST module, walk import statements, map each import's module path to a layer via the directory prefix, and flag any edge that violates your allowed-direction table. No need for a full dependency graph — a flat "importer layer → imported layer" lookup is enough.
- **Legacy shrinking (LOC watermark):** store the last-known-good line count for the target file(s) (a small JSON/text file checked into the repo). On each run, count current LOC; if it's above the watermark, WARN at a lower threshold and ERROR at a higher one, and never let the watermark move upward silently — only ratchet it down when the file actually shrinks.
- **Anti-pattern regression (AST/regex pattern-matching):** write a narrow predicate that matches the exact shape of the bug you already fixed once (e.g. "assignment built from 3+ concatenated string literals outside the one designated helper function"), scan every file except the canonical helper, and flag matches.
- **Policy/prompt drift (cross-reference):** extract the identifiers or values a policy/constants module defines, then check the prompt or instructions file it's supposed to mirror still references each one by name; flag any that are missing.

**Output contract:** human-readable text by default; `--json` for machine consumption in CI; `--errors-only` filters output to ERROR severity for use as a merge gate. A self-test mode exercises the tool's own check functions against fixture inputs so you can verify the auditor works independent of what it currently finds in the real repo. The tool is read-only — it never edits the audited codebase.

```
$ audit_invariants.py --errors-only
[ERROR] no_layer_crossing  core/pipeline.py:14  imports adapters.http_client — inner layer cannot import outer layer
[ERROR] legacy_shrinking   legacy/parser.py: 812 LOC (watermark 780, hard limit 800)
FAIL — 2 error(s), 1 warning(s)
```

## When to use

- Migrating a monolith into layered core/adapter/pipeline modules and want the boundary to hold under pressure, not just at design time.
- Running a strangler-pattern migration off a legacy module and need proof the legacy file is actually shrinking, not just "mostly not growing."
- You already fixed one specific bug class once and don't trust that nobody reintroduces it in a different file.
- Wiring a merge/CI gate that must stay fast (sub-second, no network, no LLM calls) and fully deterministic.
- A policy or constants module and its paired natural-language prompt/instructions file need to stay in sync over time.

## How to use

**Install:** copy this folder into `~/.claude/skills/architecture-invariant-audit/` for personal use, or `.claude/skills/architecture-invariant-audit/` inside a project repo.

**Invoke:**
```
Set up an architecture invariant audit for this repo — core/ can't import from adapters/ or pipelines/, and legacy/parser.py needs to keep shrinking. Wire it into the merge gate.
```
```
Run the architecture audit in --json --errors-only mode and tell me if the build should fail.
```
