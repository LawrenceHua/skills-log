---
name: long-run-agent-job-supervision
description: Supervise a long-running background AI-agent job without killing healthy work or launching duplicates — one reconnectable launch with a private run directory, no reflexive wall-clock timeout, a repeated dead-versus-quiet evidence check, and defined stop conditions with cancellation limited to the recorded process group.
---

# long-run-agent-job-supervision

Long agent runs fail in two opposite ways, and both are supervision mistakes rather than model mistakes. Some supervisors give up too early: the log is quiet, a wrapper timed out, so they call the run hung, kill it, and relaunch — throwing away twenty minutes of good work and sometimes leaving two agents editing the same tree. Others never notice a run that is truly dead. This method gives you a repeatable way to tell **quiet** from **dead**, and a fixed set of reasons that justify stopping a run.

(For the launch itself — stdin, stderr, exit codes — see `headless-agent-launch-verification`. This skill starts once the job is running.)

## 1. Launch once, in a reconnectable, evidence-keeping way

- Start **one** job in a session you can reconnect to (a multiplexer session, a tracked background job, a supervised service) — not a fire-and-forget subshell.
- Create a **fresh private run directory** (mode 0700) and keep in it: stdout, stderr, the final result, the exit status, and the **exact process or process-group ID** (plus any tool-session ID the agent exposes). These are what you'll consult every time you wonder "is it alive?"
- Write a one-line manifest: job name, start time, launch command (with secrets redacted), brief path, and the run-directory path. A supervisor that loses its own context can resume from this.

## 2. Timeouts come from a real constraint, not a reflex

Don't stamp a 20-, 30-, or 60-minute cutoff on a run because that "feels like enough." An arbitrary deadline converts a healthy run that needs 70 minutes into a failure you'll misdiagnose as a model problem. Set a cap only when there's a genuine source for it:

- an explicit time or budget cap the requester gave you,
- a metered-cost ceiling,
- the provider's or subscription's native limits.

If your harness *requires* a deadline, treat that as a separate, explicitly bounded mode: label the run "deadline-bounded," size the deadline from a measured round-trip, and don't route an open-ended job through it silently.

## 3. Quiet is not dead — run the evidence check

Keep working on other things and check the run non-blockingly (a periodic look, not a sleep loop). Before you call a run dead or hung, check **all** of these, more than once, at intervals:

| Evidence | Alive looks like | Dead/hung looks like |
|---|---|---|
| **Process tree / group** | Root and children present; CPU time advancing between checks | Gone, zombie, or present with CPU time frozen |
| **Artifact size and mtime** | Output files, logs, or the working tree growing/changing | Nothing changed across several checks |
| **Exit status** | Not yet written | Written — the run is *finished*, not hung; read it |
| **Tool-session output** | New tool calls or messages appearing | Nothing new, and the session shows no active call |
| **Provider / usage metering** | Token or request counts rising | Flat across checks (only meaningful if metering is available) |

One flat reading is not a verdict; a **repeated** set of concrete flat readings is. A long run or a silent log alone is never failure.

## 4. Three misreadings to avoid

- **An outer timeout is not a model failure.** If a collector, UI, or wrapper gave up waiting, the *job may still be running*. Reconnect to or harvest the original run. **Never launch a duplicate** because a wrapper timed out.
- **A terminal authentication failure is not a timeout.** A run that ends immediately with a "not logged in" style result, zero tokens, and zero cost is a *terminal* failure — don't wait for it and don't blind-retry. Retry only after you've proven three things: the failed invocation is terminal, no live process from it remains, and its recorded usage/cost is zero. (A status command reporting "authenticated" doesn't override a terminal failure from the real invocation — some launch modes strip the auth context the status command sees.)
- **Exit 0 is not success** and **a confident summary is not a result** — verify what changed (see `headless-agent-launch-verification`).

## 5. Stop conditions — the complete list

Stop a run only for one of these:

1. An explicit user time or budget cap is reached.
2. The run reached a terminal exit (harvest it).
3. **Repeated** concrete dead/hung evidence from section 3.
4. A safety, out-of-scope, or destructive-action risk appears.
5. Metered cost is running away.
6. An external blocker (revoked access, exhausted quota, unavailable dependency).

"It's been a while" is not on the list.

## 6. Cancel narrowly, keep the wreckage

If you must stop it:

- Signal **only the recorded process group** (or the exact session ID). Never `pkill` by name — you may take out an unrelated sibling run.
- After signaling, confirm what is actually still alive.
- **Preserve partial artifacts**: don't clean the working tree or delete the run directory. A partial diff and a truncated log are the evidence you need to decide whether to resume, retry with a narrower brief, or hand off.
- Record why you stopped, in the manifest, using one of the six conditions above.

## When to use

- Handing a big review, migration, or build to a background agent and staying available.
- A run looks silent and you're tempted to kill and relaunch.
- A wrapper or UI timed out on a job that may still be working.
- Writing operating rules for a system that runs unattended agents, including what justifies stopping one.

## How to use

**Install:** copy this folder into `~/.claude/skills/long-run-agent-job-supervision/` for personal use, or `.claude/skills/long-run-agent-job-supervision/` inside a project repo. Then ask Claude Code to use the skill by name.

**Invoke:**

```
The background agent I started 40 minutes ago has printed nothing for 15. Use
long-run-agent-job-supervision to decide whether it's quiet or dead — run the
evidence check twice, five minutes apart, before recommending anything.
```

```
Write the operating rules for how we supervise long-running agent jobs, using
long-run-agent-job-supervision: launch layout, allowed stop conditions, and how to
cancel without touching sibling runs.
```
