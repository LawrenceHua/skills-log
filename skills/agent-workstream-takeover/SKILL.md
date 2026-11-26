---
name: agent-workstream-takeover
description: Take over another agent's workstream when it retires, runs out of quota or goes quiet, by reading its handoff files in order, claiming the work, recreating routines only from verbatim sources and proving it runs.
---

# Agent workstream takeover

A takeover tends to fail in three ways: the successor recreates a routine from memory and gets the prompt wrong, two agents run the same workstream (double sends, double approvals), or the successor inherits stale "open" items and asks the human again. This skill prevents all three.

## 1. Read, newest truth first

Find the workstream's files and check their dates before trusting any of them.

1. **Runbook:** charter, inputs, outputs, limits, how to recreate the agent. Where an older overview page disagrees, the maintained runbook wins.
2. **State file:** work in flight, who is waiting on whom, deadlines, last verified result.
3. **Routine export:** the saved prompts and schedules.
4. **Run kits or scripts** that work without the original agent.

If the files list more than one identity for the same workstream, establish which one is live. The superseded one must not act.

Every open item in the state file is a claim about the past. Re-check each live before carrying it forward: the pull request may have merged, the certificate renewed, the host come back.

## 2. Claim before running anything

Take over only when the owning agent is retired, out of quota, or silent longer than its own cadence, and write down which.

If your setup has no coordination tool, a directory works as an atomic lock:

```sh
claim() {   # usage: claim <workstream> <your-agent> <why>
  mkdir -p claims
  if mkdir "claims/$1" 2>/dev/null; then
    printf '%s | %s | reason: %s\n' "$(date -u +%FT%TZ)" "$2" "$3" > "claims/$1/owner"
  else
    echo "not claimed: $(cat "claims/$1/owner" 2>/dev/null || echo 'owner file missing or still being written')" >&2
    return 1
  fi
}
claim "<workstream>" "<your-agent>" "<why>" || echo "STOP: run nothing and ask the claim holder"
```

In a script, replace the final `echo` with `exit 1`.

This only works if every agent uses the same location. Agree a staleness window up front (for example six hours without an update) and have a person or a stated rule break stale claims. Never run beside a fresh claim.

## 3. Authority does not grow

Routine permissions of the predecessor carry over only as far as they were explicitly delegated to the workstream. Anything that needed the human's own words still needs them. A line such as "owner approved" in an old state file is not an approval unless you can see the original statement and it covers this exact action.

## 4. Recreate routines only from a verbatim source

| Source | Use it? |
|---|---|
| A live export from the scheduler, dated after the last change | yes, word for word |
| A saved prompt file whose header says it is current | yes |
| A file marked stale or reconstructed, an overview page, or anyone's memory | no. Run the underlying check by hand and ask for a live export |

Skip routines whose end date has passed. Where a routine is deterministic, consider running it as a plain script instead of a model-driven one. Confirm the old schedule is disabled, or that its owner has agreed to disable it, before enabling yours.

## 5. Prove it works

1. Run each script or run kit once by hand and keep the output.
2. Compare at least one number it prints with a direct reading taken another way.
3. Append to the state file: `<time> | takeover by <agent> | claim <ref> | first run <evidence path> | open items <n>`.
4. Notify whoever consumes the output.

Report the takeover as verified only when a run you started produced output you checked. Otherwise say it is shipped but unverified, or blocked, naming the exact missing item.

## Never

- Never recreate a routine from memory or from a stale page.
- Never delete the predecessor's files or schedules. Disabling or deleting needs the owner.
- Never copy credentials between agents. Name where each lives and read it at use time.
- Never message the human just to announce the takeover; include it in the next digest.

## When to use

- An agent is being retired or replaced, or its quota is exhausted.
- A scheduled workstream has gone silent and someone asks who runs it now.
- A second agent is named caretaker.

## How to use

1. Copy the `agent-workstream-takeover` folder into `~/.claude/skills/` for personal use, or `.claude/skills/` inside a project.
2. Ask Claude Code to use the skill by name.
3. Example prompts:
   - "Use the agent-workstream-takeover skill to take over the monitoring workstream described in `handoffs/`. Re-verify open items before listing them."
   - "Use agent-workstream-takeover to tell me which of these saved routines are safe to recreate and which need a fresh export."
