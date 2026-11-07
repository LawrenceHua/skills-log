---
name: held-out-gated-skill-patching
description: Evolve an agent's skill/prompt package after repeated failures by tracing each failure to one component, patching only that component, and admitting the patch only if it beats the prior version on held-out instances.
---

# Held-out gated skill patching

When an agent keeps failing at long multi-step work, the tempting fix is to rewrite the whole prompt or skill package. That hides which change helped and which hurt, and often regresses something else. This method evolves the package like code: small versioned patches, each admitted by a mechanical check on evidence the patch was not written against.

## The pattern, in order

1. **Freeze the agent, version the memory.** The agent's base prompt and policy stay fixed. The skill package (rules, checklists, examples, tool guidance) is a separate, versioned artifact. Every change gets a version number and a one-step rollback to the prior version. Never change both at once.
2. **Trace the failure to one component.** Read the execution trace and name the single component that failed (retrieval, planning, tool use, verification, formatting). If two components failed, that is two patches, sequenced, not one combined rewrite.
3. **Patch only that component.** Make the smallest change that addresses the traced failure. A patch that rewrites the whole package in response to one failure is rejected on sight.
4. **Gate admission on paired held-out evidence.** Collect instances of the same task family that were *not* used to write the patch. Run the prior version and the patched version on them. Admit the patch only if the patched version wins by a deterministic comparison (pass/fail checks, exact-match, tests), not a self-grade. If it does not beat the prior version, reject it and keep the old one.
5. **Record the admission.** Version, what failed, what changed, the held-out result (before and after counts), and the rollback command. A change with no held-out result is not admitted, however good it looks in the trace.

## Transfer caution

A package evolved for one model or task family can transfer negatively to another. Treat a pass as local. On any transfer (new model, new task family, new product), re-run the held-out gate before trusting the package there.

## Worked shape

- Failure: a multi-step agent keeps misreading tool output at step 3 of 8.
- Trace: the tool-use component, not planning or retrieval.
- Patch: one added rule in the tool-use section, nothing else.
- Gate: 10 held-out instances of the same task family, before and after.
- Admit only if the patched package wins; otherwise revert and re-trace.

## Refusals

- Do not use this for a one-off failure: fix the instance, do not evolve the package.
- Do not use it when no held-out evidence exists: collect evidence first, then evolve.
- Do not admit a patch because the trace "looks fixed". The trace is where the patch came from; it cannot also be the test.
- Do not stack patches before the previous one is admitted or reverted.

## When to use

- The same component fails repeatedly across runs while the rest of the package works.
- A prompt or skill package is drifting through ad hoc edits and needs a disciplined change rule.
- Multi-step work where a fix in one place quietly breaks another.

## How to use

1. Copy this folder into `~/.claude/skills/` (personal) or `.claude/skills/` inside a project, then ask Claude Code to use `held-out-gated-skill-patching` by name.
2. Give it the failing trace, the current package version, and (if you have them) held-out instances. If you have none, ask it to help build the held-out set first.

Example prompts:
- "Use held-out-gated-skill-patching on this failing trace: name the one component that failed and propose the smallest patch."
- "Use held-out-gated-skill-patching to decide whether v7 of my review skill should replace v6, using these 12 unseen tasks."
