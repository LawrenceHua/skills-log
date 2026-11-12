---
name: agent-tool-integration-contract
description: Add a new command-line tool, skill or model lane to an agent setup so it is actually used: an eight-point tool contract (self-test with a failing arm, distinct refusal codes, bounded output, receipts, registry, ledger, discoverability) and the difference between installed, used and working.
---

# agent-tool-integration-contract

The dominant failure when you wire something new into an agent setup is not a broken component. It is a component that is installed, runs, reports success and changes nothing: the value it writes has no reader, the test never reaches the branch it claims to test, or the tool is on disk but no agent can find it. This skill is the contract to satisfy before you say "it's connected".

## Step 1: decide which of five things you are adding

They have different homes and different discovery paths. Confusing them is the first mistake.

| You are adding | It lives in | It is discovered by |
|---|---|---|
| a **tool** (a command an agent runs) | one file on your `PATH`, e.g. `~/.local/bin/<name>` | a registry file listing name, invocation, purpose |
| a **skill** (how an agent should behave) | `<skills-dir>/<name>/SKILL.md` | the skills index or directory listing your harness reads |
| a **model lane** (a way to run a model) | a launcher script plus a receipt | a `--list` command that shows last real call |
| a **recurring job** | your scheduler's definition file | a sweep or doctor command that lists loaded jobs |
| a **gate** (a refusal rule) | the tool or hook that enforces it | the negative test that triggers it |

A tool that needs judgement is also a skill. A skill that needs a deterministic check needs a tool. Write the tool first; then write the skill that says when to use it.

## Step 2: the eight-point tool contract

1. **One file, one purpose.** Executable, standard library or plain shell. A dependency needs a stated reason and a rollback.
2. **`--selftest` with negative controls.** The suite must prove the tool can fail. A self-test where every check passes shows the tool is quiet, not that it works. Label the failing arm "negative control" and check its premise: the control must actually reach the branch it is meant to trip.
3. **Refuse loudly with distinct exit codes.** Usage error gets one code; each refusal class gets its own nonzero code. Never degrade silently and never substitute a default the caller did not ask for. An unknown argument must never fall through to doing the real thing (a `--help` that starts a live job because the parser ignored argv is a real bug).
4. **Bound your own output.** Print a window, keep the full result on disk, and say where. One unbounded command result is paid for again on every later model request in the session.
5. **Write a receipt, not a log line.** Content-free, timestamped, in a state directory you name. Anyone must be able to re-run the check and get the same answer; if they cannot, it is a claim, not a result.
6. **Register it.** Add the registry entry (name, how to invoke, what it is for). If the registry reports both availability and last real call, keep them as two separate fields.
7. **Append a ledger row** naming what changed, why, the check that proves it, and the reference the check was compared against. Use a fixed vocabulary of verdicts (`VERIFIED`, `CODE-SHIPPED-NOT-VERIFIED`, `BLOCKED`, `INCONCLUSIVE`).
8. **Be discoverable.** If agents should find it, it must appear in the observed catalog. Regenerate the index, then search the index for your name. A skill that does not appear in the catalog does not exist; do not claim it is available until the search returns it.

## Step 3: installed is not used is not working

Measure the three claims separately and never let one stand for another.

- **Installed:** the file is on disk. Proves only disk state.
- **Used:** something invoked it. Check invocation history, not the binary.
- **Working:** a call returned success recently enough to matter, inside a stated tolerance.

A receipt proves a lane worked once, at its own timestamp. A list that prints "ok 9h ago" says nothing about whether the live call succeeds now (a quota message can be returned minutes later). Route only on a receipt inside your tolerance and probe when it is stale. A stale lane is `INCONCLUSIVE`, not green.

## Step 4: five ways an integration is silently useless

Check your own work against all five before reporting.

1. **The value you write has no reader.** Name the value, name its consumer, and prove the consumer visibly reacts. Typical shapes: a status column nobody reads, a check result computed and discarded so a failed check still reports done, a degraded reason dropped unless the result was empty.
2. **Your test never reaches the branch it tests.** A fixture missing the field a branch needs answers an earlier branch; a control with the wrong exit condition proves nothing; a filter narrow enough to bound output can hide the verdict.
3. **You measured a scope and reported a world.** A list command that reads one queue returns fewer rows than exist and nothing in its output says so. A result measures only the scope named in its own query; print the scope.
4. **You recorded your paraphrase instead of the observation.** "Not authenticated" can never equal the machine's own sentence. Record the raw value, the exit status or a stable extracted scalar.
5. **Your green is the artifact grading itself.** If you chose the reference, the claim is a report. Name an external reference: a live third party, a measurement you did not produce, or a reviewer whose default verdict is refuted.

## Step 5: prove you are connected

Connection is complete when you can paste the output of all four:

```sh
<tool> --selftest; echo rc=$?          # exits 0 and includes a failing arm
<tool>; echo rc=$?                     # bare usage: a distinct refusal code, not a silent run
<index-search> '<your-name>'           # discoverable in the catalog
<registry-show> <your-name>            # registered
```

Then label honestly. A self-test you wrote yourself is `CODE-SHIPPED-NOT-VERIFIED`. `VERIFIED` needs a reference you did not choose. In practice a large share of self-reviewed "done" items get overturned by an independent pass; assume yours is one of them until something other than you agrees.

## If you get stuck

- Decidable by a documented default? Take it, record the rollback, proceed.
- Needs a human's hands (a login, a signature)? Batch all such items into one list with exact steps.
- Waiting on another build? That is sequencing, not blocking.
- External outage or quota? Name the service and the date, route around it.

## When to use

- Connecting a new CLI, skill, model backend, hook or scheduled job to an agent setup.
- Reviewing a colleague's "I wired it up" report.
- Debugging "it's installed but agents never use it".

Skip it for a one-off script nobody else will call.

## How to use

**Install:** copy this folder into `~/.claude/skills/agent-tool-integration-contract/` for personal use, or `.claude/skills/agent-tool-integration-contract/` inside a project. Then ask Claude Code to use the skill by name.

**Example prompts:**

```
I just wrote a small CLI that agents should call. Walk it through the
agent-tool-integration-contract and tell me which of the eight points it fails.
```

```
Use agent-tool-integration-contract to audit this new model backend: is it
installed, used, or working, and what is the evidence for each?
```
