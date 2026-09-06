---
name: runbook-generator
description: Generate a standardized operational runbook for a service — start/stop/health-check/maintenance/incident-response/rollback/escalation sections, each critical step paired with an expected-output verification check, so a runbook is provably correct at write time rather than only trusted during a real incident.
---

# runbook-generator

A runbook that's a free-form paragraph of notes is only as good as whoever wrote it remembers to keep it updated. A runbook with a fixed shape and a verification check on every critical step can be validated at write time — you find out the start command is stale before an incident, not during one.

## The method

**1. Fixed section shape, every time.** Every runbook for every service gets the same eight sections, so anyone on-call can navigate any service's runbook without relearning its structure:

1. **Overview** — what the service does, one paragraph
2. **Start** — exact commands to start it
3. **Stop** — exact commands to stop it
4. **Health check** — how to verify it's actually healthy (a probe command, a log pattern, a status endpoint)
5. **Maintenance** — periodic tasks (log rotation, credential rotation, cleanup)
6. **Incident response** — a symptoms → likely causes → fixes table
7. **Rollback triggers** — when to revert, and the exact command to do it
8. **Escalation** — who to contact if the primary owner is unavailable

**2. Every critical step gets a verification check, not just a command.** A runbook step isn't "run this command" — it's "run this command, then confirm this specific expected output." For example:

```bash
# Step: start the service
launchctl load ~/Library/LaunchAgents/com.example.service.plist

# Verify (exit code reflects whether the service is actually listed)
launchctl list | grep -q com.example.service
```

Every command in the runbook should be literally copy-pasteable, and every critical one should be paired with a way to confirm it actually worked — a runbook step with no verification is a guess dressed up as an instruction.

**3. Dry-run before trusting it.** Run the health-check command (read-only, non-destructive) against a real instance of the service and confirm it returns the expected output and exit code before considering the runbook done — an untested runbook is a hypothesis, not documentation.

**4. Version-controlled, indexed, and reviewed on a cadence.** Store each runbook alongside the code it documents, keep an index file linking every runbook, and set an explicit review cadence (quarterly is a reasonable default) so runbooks don't silently drift from the service they describe the way ad hoc docs do.

**5. Documented commands, not executed ones.** The generator writes the runbook; it doesn't run the start/stop/rollback commands itself outside of the dry-run health check. Those commands are for a human (or an on-call responder) to execute deliberately during an actual incident.

## When to use

- Before any new service, scheduled job, or agent goes live.
- When existing runbooks have drifted and no longer match what a service actually needs to start/stop/recover.
- Onboarding someone new to on-call rotation for a service.

Not needed for a one-off script or a trivial change with no operational surface — inline comments cover that case better than a full runbook.

## How to use

**Install:** copy this folder into `~/.claude/skills/runbook-generator/` for personal use, or `.claude/skills/runbook-generator/` inside a project repo.

**Invoke:**

```
Generate a runbook-generator scaffold for this new service — fill in the
start/stop/health-check commands from how it's actually deployed, and
dry-run the health check before you call it done.
```

```
Our runbooks haven't been touched in months. Audit them against
runbook-generator's structure and flag anything that's drifted from
how the service actually runs today.
```
