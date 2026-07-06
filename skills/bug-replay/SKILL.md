---
name: bug-replay
description: Turn every fixed bug into a permanent regression fixture (input + expected behavior) in a JSONL/library, then replay the whole set before you ship anything. Use to verify "did we regress a bug we already fixed" and to keep a growing, runnable history of your project's known failure modes.
allowed-tools: [Read, Write, Bash]
---

# bug-replay

A discipline, not just a script: **every bug you fix becomes a fixture you
can replay forever.** Instead of trusting that a bug "stays fixed" because
nobody's complained lately, you keep a small library of concrete
reproductions and re-run all of them before anything ships. This turns bug
fixing from a one-off event into a permanently-growing regression suite.

## When to use

- Before shipping any change to a system that has a history of regressions
  ("did this touch the thing that broke last month?").
- Right after fixing a bug — capture it immediately, while the repro is
  fresh, rather than relying on memory.
- When someone asks "did we break BUG-044 again?" — replay that one fixture
  directly instead of re-deriving the repro from scratch.
- As a lightweight pre-flight gate before a release or deploy.

**Skip it for:** exploratory prototyping with no shipped surface yet, or
bugs so trivial/one-off that a fixture would never realistically fire again.

## The method

### 1. Capture every fixed bug as a fixture

When you fix a bug, write down (in a JSONL file, one line per bug):
- an ID (`BUG-001`, `BUG-002`, ...)
- the minimal input/scenario that reproduced it
- the expected correct behavior/output
- a **bucket** describing how it can be verified (see below)

Keep this file under version control next to the code it tests — it's your
project's memory of "things that have gone wrong before."

### 2. Bucket fixtures by how they're verified

Not every bug can be replayed the same way. Bucket each fixture so the
runner knows which check to apply:

| Bucket | Meaning |
|---|---|
| **synthetic** | Fully replayable through a mock/harness — feed the input, assert the exact output |
| **structural** | Checked by a deterministic gate (a lint rule, a schema check, a specific code path existing) rather than a full run |
| **graded** | Needs a rubric or LLM-judge pass rather than an exact-match (common for prompt/agent behavior, UX copy, tone) |

Most projects lean heavily "synthetic" early on and grow "graded" fixtures
as they add LLM- or judgment-driven behavior.

### 3. Build a small runner

A runner script that supports:
```bash
python3 run.py                 # full self-test: replay every fixture
python3 run.py --bug BUG-044   # replay a single fixture
python3 run.py --list          # show all fixtures + their bucket
python3 run.py --json          # machine-readable output for CI
```

For each fixture, the runner reports PASS/FAIL plus the observed vs.
expected diff. At the end it prints a summary line like `PASS: 41/44` in a
format your CI or a pre-flight gate script can parse.

### 4. Wire it into your ship gate

Run the full replay before anything meaningful ships — a deploy, a merge to
main, a prompt change. A single new failure in an old fixture is a
regression, full stop, even if the change under review looks unrelated: that
disconnect is exactly what the fixture caught.

### 5. Keep growing the library

Every new bug gets a new fixture, in the right bucket, added to the same
file. The value of this skill compounds — after a few months you have a
cheap, fast, ever-growing regression suite built entirely from real
incidents rather than hypothetical test cases.

## How to use

**Install:** copy this folder into `~/.claude/skills/bug-replay/` for
personal use, or `.claude/skills/bug-replay/` inside a project repo. Adapt
`run.py` to call into your own test harness/mocks — the fixture format and
bucket concept are the reusable part; the runner needs to know how to
actually exercise your system.

**Invoke:**

```
Run bug-replay against the full fixture set before we merge this — I want
to know if anything we already fixed has regressed.
```

```
We just fixed the double-charge bug in checkout — capture it as a new
bug-replay fixture (BUG-019) so it never silently comes back.
```
