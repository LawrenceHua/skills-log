---
name: recurring-automation-audit
description: Decide whether a recurring automation (cron, timer, scheduled agent pass) earns its cadence, audit it from its own ledger, and retire it reversibly when it does not.
---

# Recurring automation audit

A schedule is a promise to spend an hour every hour, forever, with nobody obliged to read the output. A cadence that stops being useful does not stop, because the evidence of its uselessness is buried inside the volume it produces. This skill is the audit that finds it and the procedure that ends it.

It owns the *cadence*: should it exist, is it working, how does it die. It does not label a single claim or deepen a single brief.

## 1. Five gates before you write the schedule

1. **Name the artifact a stranger can open, and the person who opens it.** Missing either makes the loop a metronome. This gate fails silently, because a pass that writes notes always has an artifact.
2. **Name one exit number** — published, installed, answered by a human. "Rows written" is not an exit number.
3. **Name the external reference that judges it.** If the pass chooses its own scope and certifies its own result, its verdicts measure its confidence, not the world. A claim whose reference the builder chose is a report, not a verification.
4. **Write the kill criterion at creation:** "if N consecutive passes produce nothing a human opened, stop and escalate." Nobody adds it later, which is why loops outlive their usefulness.
5. **Price the hour** — what it touches unattended and what it can break while nobody looks (a loose pattern-based "remove job" command can delete a live job that is not yours).

**Never put a mandatory research step in a recurring pass.** It makes the report the deliverable. Research serves a build; in a loop with no build it becomes the product, and the hour ends before the hard part starts.

## 2. Audit a live loop from its own ledger

Count from the loop's ledger, never its summaries. Adapt the field names:

```sh
L=<ledger-file>   # append-only record the loop writes
R=<reports-dir>   # where its pass writes notes (may not be next to the ledger)
echo "rows        $(wc -l < "$L" | tr -d ' ')"
echo "changes     $(jq -c 'select(.event=="change")'     "$L" | wc -l | tr -d ' ')"
echo "verified    $(jq -c 'select(.label=="VERIFIED")'   "$L" | wc -l | tr -d ' ')"
echo "corrections $(jq -c 'select(.event=="correction")' "$L" | wc -l | tr -d ' ')"
echo "notes       $(ls "$R"/*.md 2>/dev/null | wc -l | tr -d ' ')"
```

Traps when you write the audit down:
- The reports directory is often *not* adjacent to the ledger. A guessed relative path answers `0`, which reads as "the loop wrote no notes".
- Some `wc` implementations pad with spaces; strip them.
- **Date the snapshot and expect it to move.** A live ledger grows while you read it — including with your own audit's rows. Quote numbers with a timestamp and say which rows arrived after your snapshot before calling a mismatch a defect.

Then answer one question in one line: **what did a person outside the loop get?** If the answer is nothing, the ratio of rows to outcomes is the whole finding. `verified` exceeding `changes` means the same work was re-certified repeatedly by its own author — a rehearsal mistaken for a job.

A loop that picks its own gap always finds one that fits the hour. Self-chosen scope plus self-graded result is a closed system; it converges on whatever is cheap and always has something to report.

## 3. Four ways a cadence manufactures activity

- **The pass grades itself.** If the checker is the builder, the label measures the builder's confidence.
- **The mandatory research step.** Every note is an hour that felt finished.
- **The report as deliverable.** A status card saying the loop is running is the loop's report about itself.
- **A closed gate nobody names.** Before blaming effort, check *why* nothing shipped: a resource guard may be killing the work, or publishing may be on hold. A loop cannot ship through a closed gate and will not report that as its finding unless you ask.

## 4. Retire it, reversibly

Do all six; skipping the last costs the next agent an hour of archaeology.

1. **Delete the job** with the scheduler's own delete, naming the **exact** job label — never a pattern.
2. **Restore anything you removed by mistake**, then confirm it is listed again.
3. **Prove nothing is in flight** — job list, reminder list, process table. "Stopped" means no schedule *and* no running pass.
4. **Write the stop record** beside the work: why it stopped (with measured counts), what was worth keeping, and the exact recipe to recreate it. A stop with no recipe is a decision the next agent will re-litigate.
5. **Append a decision row to the ledger** naming the rollback, not just the action.
6. **Tell the owner in one line, with the ship count first.** Do not send a card announcing that reporting will continue.

When told "just stop it", stop all of it — schedule, reports, cards, renders — and say so plainly. A paused loop that keeps posting is the defect it was meant to fix.

## 5. Instrument rules a self-graded loop breaks

- **One instrument per threshold, borrowed from the gate.** If your measurement disagrees with the gate's tool on the same file, call the gate's implementation, and show both agree on one real control file first.
- **A check that cannot fail will pass.** If a probe returns an empty string for both sides, "unchanged" compares two blanks. Test every check against a known-different input.
- **Never re-implement a chain you were handed.** If the project's own tool already produces the result, wrap it instead of rebuilding it from parts.
- **A cleaning step can eat the output.** A "shortest stream" flag can trim real content on a tiny mismatch; pad the shorter input instead and re-hash.
- **A child process that reads stdin eats the loop that called it.** Give loop-driven commands no stdin (`-nostdin`, `< /dev/null`).
- **A guard's own numbers are often the whole explanation.** If a worker keeps dying with the same signal, read the watchdog's thresholds before blaming the worker.

## 6. Where a lesson has to live to survive

Prose appended to the end of a shared instruction file is the first thing a size cut removes. If your loader truncates a file at a byte limit, a lesson past the limit is invisible while sitting correctly on disk. Check headroom with `wc -c <file>` against the documented limit, and put durable lessons in a discoverable skill whose description is what triggers it; keep the shared file for short pointers.

## Never

- Never recreate a stopped automation without the owner saying so.
- Never add "research first" to a recurring pass.
- Never let a pass certify its own work or choose its own reference.
- Never quote a row count as a ship count.
- Never remove a job by pattern; name the exact label.
- Never move a threshold to make a pass succeed — escalate it.
- Never say "paused" when the instruction was "stop".

## When to use

- Someone asks "is this automation actually helping?" or "why is this loop not shipping?"
- Before creating an hourly, cron, timer, or babysitting pass.
- A scheduled pass has produced hundreds of records and nothing a person used.

## How to use

1. Copy the `recurring-automation-audit` folder into `~/.claude/skills/` (personal) or `.claude/skills/` inside a project, then ask Claude Code to use the skill by name.
2. Example prompts:
   - "Use the recurring-automation-audit skill on my nightly agent pass. Here is its ledger path; give me the ship count and a keep-or-retire recommendation."
   - "Before I schedule an hourly research agent, run the five gates from recurring-automation-audit and tell me which one it fails."
