---
name: deepen-before-doing
description: Before any non-trivial task, brief, delegation, or unattended run, answer four questions (pro moves, raw material, methods, independent check) and rewrite the prompt to ask for exactly that - deeper, not bigger.
---

# Deepen before doing

Deeper, not bigger: the same deliverable and scope, with sharper inputs, methods, and proof. Run it once at the start of a task, state the four answers in a line or two each, rewrite the prompt, then work from the rewritten version.

## Choose a depth

- **Skip** (one silent check, no output): a lookup, one read-only command, a trivial edit that is already fully specified.
- **Standard** (any deliverable, state change, delegation, automation, or monitoring pass): the four answers plus the rewritten brief, then proceed. Do not wait for approval unless the rewrite changes scope, cost, or risk; then ask exactly one question.
- **High stakes** (money, auth, security, production, legal, irreversible, unattended): also write the falsifier for every claim, and have the independent check running or scheduled before the work starts.
- **Worker rule:** whoever writes the prompt deepens it. An agent that receives an already-deepened brief executes it and reports in the brief's reporting terms; it does not re-deepen or argue with it.

## The four questions

1. **What would a top professional in this field do here that I am not asking for?** Name the role (staff SRE, forensic accountant, security reviewer, editor). List two to four moves that would change the answer: challenge the premise; define done and the falsifier first; check what is absent (no data is not green); look for prior art (an open PR, an existing fix); reproduce before changing; bound the blast radius and the rollback. Tag each **IN** (cheap, same deliverable: fold into the rewrite) or **OFFER** (adds scope, cost, or risk: list it, do not do it). Drop decoration such as "be thorough".
2. **What is the rawest material they would start from, instead of what has already been digested for me?** Digests are summaries, dashboards, status lines, PR descriptions, notes, an earlier agent's report, a paraphrase of the request. Raw is what the digest was made from: the file, table rows, log lines in a time window, the API response, the diff, the CI log, the process table, the receipt, the original transcript, the primary spec. Name it exactly (path, table, endpoint, commit) and bound the read. If only digests exist, say so and treat each as a pointer to the raw, never as evidence.
3. **What specific methods and tools would they use?** Method, exact command, and the output that would be decisive. Prefer a method that can fail: a differential or property test, a mutation test, a read-only database query, a header-only HTTP probe, a bisect or `git log -S`, a held-out labelled set with a confusion matrix for any grader, breaking the thing on purpose and restoring it from version control.
4. **What, other than you or me, would show the result is right?** Something neither the doer nor the requester controls: CI on another machine; a deterministic oracle (compiler, schema validator, golden file, standard test vectors); the live system (HTTP status, database row, vendor API); a fresh-context verifier handed only the brief, the diff, and the command to re-run; a different model family grading the output; a primary source; a domain reviewer with no stake. State what result would prove the work wrong. If nothing independent can run, say so and report the weaker status below, never "verified".

## Rewrite the prompt

Replace vague nouns with the named things from the four answers. Same scope. Use these labels:

```
GOAL:                the original ask, one sentence
DONE WHEN:           observable criteria, each tied to the independent check
START FROM (raw):    exact paths, tables, endpoints, logs - bounded; digests listed as pointers only
PRO MOVES (in scope): the IN items
METHODS & TOOLS:     exact commands and the decisive output
INDEPENDENT CHECK:   who or what, how to run it, what would prove the work wrong
OFFERS (not done unless approved): the OFFER items, plus anything destructive, costly, or production-facing
REPORT AS:           VERIFIED | CODE-SHIPPED-NOT-VERIFIED | BLOCKED | INCONCLUSIVE + exact command or blocker
```

Rules for the rewrite:

- **Specific or absent.** If you cannot name a real raw source or independent check, write `NONE FOUND: <why>` instead of inventing one, and lower the claim label.
- **Probe before you name.** `ls`, `command -v`, or a read-only query confirms a path or tool exists; otherwise mark it `(unverified)`.
- **Extensions go under OFFERS**, never into DONE WHEN. Destructive actions, spend, production changes, and credential changes stay the requester's call.
- **Shorter beats longer.** Cut any line that would not change what is done or how it is proved.

### Mini example

Original ask: "Find out why the nightly export is slow."

```
GOAL:               Identify what made last night's export slower than its usual runtime.
DONE WHEN:          A named stage accounts for at least 80% of the added time, shown by timestamps from two runs.
START FROM (raw):   The last 5 runs' log files (tail -n 200 each); the job's schedule definition. The dashboard summary is a pointer only.
PRO MOVES:          Compare slow vs. normal run side by side; check whether the input size changed before blaming code.
METHODS & TOOLS:    grep stage-start/stage-end lines, diff the per-stage durations; row counts via a read-only query.
INDEPENDENT CHECK:  Re-derive the per-stage durations from the raw timestamps with a separate script; the claim is wrong if any stage total differs by >5%.
OFFERS:             Adding an index or changing the schedule (not done unless approved).
REPORT AS:          VERIFIED | CODE-SHIPPED-NOT-VERIFIED | BLOCKED | INCONCLUSIVE + command
```

## Where it applies

| Surface | What to do |
|---|---|
| Interactive session | Run at task start, show the answers and the rewritten brief, proceed. |
| Delegating to an agent or another tool | Deepen while writing the brief; the rewritten form is the brief. Judge the returned work by the independent check, not by the worker's report. |
| Automation (cron, CI, headless runs, hooks) | Deepen once when the prompt is written and store the rewritten brief as the prompt. Do not prepend this preamble to a prompt whose output is machine-parsed (JSON-only, exit-code contracts); put the structure in the brief instead. |
| Monitoring or steering a running job | See below. |

## Monitoring and steering

The task is a true picture of the watched work plus the right nudge, so deepen the watch itself.

- **Pro moves:** read the no-data branch first (absence of evidence is not green); check liveness (heartbeat, file mtime, exit code) before content; ask whether each "done" has a receipt; steer with the restated brief (goal, done-when, evidence), never a bare "continue".
- **Raw:** the process table, file mtimes, bounded tails of the real log or receipt path, the worktree's `git status` and `git log`, CI run records - not the watched session's own status message or a handoff summary.
- **Tools:** bounded read-only probes; a check you repeat more than twice becomes a script; require two independent signals before declaring a stall.
- **Independent:** a signal the watched session did not produce (a receipt, a CI result, an mtime, a second observer). The watched session never grades itself.

## Guardrails

- Sensitive raw material (credentials, environment values, personal or customer data, private logs): do not open or print it. Use its least sensitive form (counts, hashes, headers, mtimes), check presence with `[ -n "${VAR+x}" ]`, or ask the owner.
- Bound every raw read (name the file, use `head`, `tail`, `-n`). The rewrite adds no whole-tree searches, background tasks, or deletes.
- A probe handed to a grader becomes its training set: give categories, keep the exact test strings private.
- Not independent: re-reading your own work, the requester's glance, a second instance fed the same digest. Independent means a different information path (tool, source, or model family).
- Say it once: show the analysis once per task and redo it only when the goal changes.

## When to use

- Starting any deliverable, state change, delegation, scheduled/headless prompt, or monitoring pass.
- A brief keeps producing plausible-but-unchecked results because it points at summaries instead of sources.
- You catch yourself writing "verify it works" with no named verifier.

Skip for one-shot lookups and fully specified trivial edits.

## How to use

1. Install: copy this folder into `~/.claude/skills/` for personal use, or into `.claude/skills/` inside a project. Then ask Claude Code to use the `deepen-before-doing` skill by name.
2. Example prompts:
   - "Use the deepen-before-doing skill, then fix the flaky checkout test."
   - "Use deepen-before-doing to rewrite this brief for a background agent before I launch it: <paste brief>."
