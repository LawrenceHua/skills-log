---
name: headless-agent-launch-verification
description: Launch a headless/background CLI coding-agent run so it can't silently hang or lie about completing, and verify what it actually did instead of trusting its self-report.
---

# headless-agent-launch-verification

Delegating a task to a second CLI-based coding agent running in the background fails in a small number of very specific, very repeatable ways — almost never because the model was wrong, but because the launch or the verification was sloppy. This method is the checklist that catches them, learned the expensive way (dead runs, doubled-up concurrent edits, and false "it did nothing" verdicts).

## Invocation shape

Whatever the specific CLI, the safe launch pattern is the same:

```bash
your-agent-cli exec "$(cat /path/to/brief.md)" \
  < /dev/null \
  > run.out 2> run.err
echo "RC=$?" > run.rc
```

Every one of these pieces exists because skipping it has caused a real failure:

- **`< /dev/null` is not optional.** Launched from a non-interactive context (a background shell, a nested subshell, a scheduler), many CLI agents will print something like "reading additional input from stdin..." and block forever waiting for EOF that never arrives. The prompt argument alone doesn't prevent this. The process looks healthy in `ps`, CPU sits near zero, and the log has one line — that line means "hung waiting for stdin," not "the model is thinking."
- **Redirect stdout and stderr separately.** Many agents put their actual work (file reads, tool calls) on stderr and reserve stdout for the final summary. A 0-byte stdout is not evidence the agent found or did nothing — check stderr before concluding that.
- **Write the exit code to a file, on its own line, immediately after the command.** If you chain `; echo "done"` or similar after the launch, a naive automation reading "the last command's exit code" will read the echo's exit code, not the agent's. A `timeout`-based kill typically reports 124 — treat that specifically as "timed out," not as a generic failure.
- **Pass long briefs via `"$(cat brief.md)"`, not inline.** A multi-paragraph brief typed or interpolated directly into a shell command gets mangled by quoting long before it reaches the agent.

## The four traps

**1. A background-launch wrapper reporting success while the agent is still working.** `nohup your-agent-cli exec … &` returns exit 0 immediately — that's the *shell's* exit code for backgrounding successfully, not the agent's for finishing. A harness that treats early "exit 0" as "done" will read a truncated, half-written log and conclude the agent did nothing — then relaunch, leaving two instances editing the same files concurrently. Confirm the agent is actually still running by process, not by exit code:

```bash
ps -eo pid,etime,args | grep "your-agent-cli exec" | grep -v grep
```

If you must background it, track the process yourself (record its PID at launch) and always check for an existing live run before relaunching.

**2. Exit 0 is not evidence of work.** An agent can finish cleanly having changed nothing. Fingerprint the target files before and after and compare:

```bash
md5sum target/**/*.py | md5sum       # before
# … run the agent …
md5sum target/**/*.py | md5sum       # after — identical means it wrote nothing
```

Don't rely on a self-written report file as your only signal either — a run killed mid-flight never gets to write one. Check both the report and the actual diff.

**3. Brief size and shape matter more than brief length.** A large, unstructured brief can cause some agents to print a plan and exit having done no work, even at high reasoning-effort settings — while a well-structured brief of similar or larger size runs fine. Keep briefs tight and explicit: numbered questions or steps, a named output location, and a closing template the agent must fill in. If a run exits cleanly with no work done, don't just shorten it — check the log for what it actually spent its effort on before concluding it needs a smaller task.

**4. Concurrent runs on the same tree corrupt each other.** Two background agent runs editing one working tree will interleave edits into a broken mix. Always check for a live run before launching a new one (trap 1), and when you kill a stray process, confirm what's actually still alive afterward — you may take out an unrelated sibling run by mistake.

## Safe scoping — put this in every brief

State hard constraints explicitly; agents generally follow them well when stated as rules, not implied:

```
- Edit ONLY files under <exact path>. Nothing else.
- NEVER run destructive git commands (add -A, checkout ., stash, clean -f).
- Do NOT print, echo, or copy any secret VALUE — names and paths only.
- Do NOT edit shared config files outside the scoped path.
- Do not install packages or restart services unless explicitly told to.
- Do not commit.
```

If the target directory isn't cleanly reversible via git (an unmanaged state directory, for example), snapshot it first with a plain recursive copy before granting write access.

## Verifying what it did — non-negotiable

Treat everything the agent reports as a claim, not a result:

1. Diff every file it touched yourself — read the actual change, don't take the summary's word for it.
2. Re-run your test suite yourself and assert on the actual count of tests run and passed — not on the presence of a word like "OK" in the output.
3. **Mutation-test the claimed fix**: revert just that change, confirm the relevant test now fails, restore it, confirm the test passes again. A change whose test passes either way isn't actually tested.
4. Confirm it didn't widen a guard, weaken a fail-closed check, or delete a test to make something pass.
5. If the change needs to go live, restart/redeploy yourself — "edited on disk" is not "running."

Before trusting a *finding* (not just an edit) from the agent, confirm it actually read the relevant code rather than pattern-matching on filenames or its own config files:

```bash
grep -cE "sed -n|nl -ba|cat |rg |grep " run.log     # did it read anything at all?
```

If that count is near zero, the run's verdict is void regardless of how confident it sounds — a "verdict" line from these agents tends to run more confident than the evidence behind it supports.

## When NOT to delegate this way

- Trivial mechanical edits — launch/verification overhead exceeds the work itself.
- Anything requiring live credentials, production deploys, or outward-facing actions without a human in the loop.
- Work you already know the answer to and just need to type — delegating it adds a verification step for no benefit.

## When to use

- Any time you hand a substantial coding, review, or research task to a second CLI-based agent running unattended in the background.
- Debugging a delegated run that "came back empty" — walk the four traps in order before assuming the model failed.

## How to use

**Install:** copy this folder into `~/.claude/skills/headless-agent-launch-verification/` for personal use, or `.claude/skills/headless-agent-launch-verification/` inside a project.

**Invoke:**

```
Launch this task on the background CLI agent using headless-agent-launch-verification
— I don't want another silent hang, and I want the diff mutation-tested before you
tell me it's done.
```

```
The last background agent run came back with no changes and a confident summary.
Walk through headless-agent-launch-verification's four traps and tell me which one
this actually was.
```
