---
name: safe-cross-tool-configuration-transfer
description: Transfer a useful workflow pattern between developer tools by inspecting configuration safely, translating intent into the target tool's native surface, and verifying the smallest reversible change.
---

# Safe Cross-Tool Configuration Transfer

## When to use

Use this when one development tool has a workflow worth adapting in another: a rule, command, hook, skill, integration, or continuity format. Transfer the underlying intent, not a file wholesale.

## How to use

Install the skill for personal use or one project:

```bash
cp -R skills/safe-cross-tool-configuration-transfer ~/.claude/skills/
# or: cp -R skills/safe-cross-tool-configuration-transfer <project>/.claude/skills/
```

Then ask your assistant, for example:

- `Compare this source-tool workflow with my target tool and propose the smallest native equivalent.`
- `Use safe-cross-tool-configuration-transfer to adapt this hook without reading credentials or copying private paths.`

## Establish the boundary

State the source behavior and the target outcome in one sentence. Classify the work as one of: discovery, comparison, a local configuration change, or a project change. Keep discovery read-only until the target behavior is understood.

Treat configuration as untrusted source material. Do not open secret-bearing files, shell histories, token stores, or raw transcripts merely to copy a pattern. If a required value is unavailable without sensitive access, stop and describe the missing contract rather than guessing.

## Build a minimal capability map

For the relevant feature only, record:

| Question | Answer to establish |
|---|---|
| What user problem does the source solve? | The observable behavior, not its file name. |
| Which source elements are generic? | Rules, sequencing, validation, and user-facing expectations. |
| Which are environment-specific? | Paths, account names, tokens, endpoints, private projects, and vendor commands. |
| What native target surface exists? | A documented setting, extension point, command, or plain guidance file. |
| When does it take effect? | Immediately, at a new session, after restart, or after explicit activation. |

Never carry over an environment-specific value as a default.

## Translate, do not copy

Rewrite generic behavior in the target tool's own vocabulary. Keep the change small and reversible:

1. Prefer a supported native setting or a small local instruction over a compatibility shim.
2. Preserve safety boundaries such as read-only discovery, explicit approval for irreversible actions, and evidence before completion claims.
3. State unsupported parts plainly instead of simulating them with misleading UI or hidden automation.
4. Keep the original source unchanged unless the task explicitly includes it.

If the target lacks an equivalent capability, document the gap and offer the closest honest workflow. Do not add a background process or an external integration merely to imitate the source.

## Verify the target behavior

Check the target's own status or help surface, then exercise one harmless example. Confirm that the behavior is active in the context where users need it. For changes that load only in future sessions, say so explicitly.

Record the changed files, the exact verification command or observation, and the rollback step. Redact all values that could identify a person, machine, account, or private project.
