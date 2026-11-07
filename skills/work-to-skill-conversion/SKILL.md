---
name: work-to-skill-conversion
description: Turn a finished piece of work into a reusable agent skill by harvesting from artifacts instead of memory, executing every written command, writing the negative form, and proving the skill is discoverable.
---

# Work to skill conversion

A project spends days learning a dozen things the hard way; a skill is how the next agent gets them in about 140 lines instead of days. The conversion has one characteristic failure: you write down what you *remember* rather than what *happened*, and the result reads like advice instead of a record.

## 1. Harvest from the artifact, never from the conversation

Use the highest-truth source available for each claim:

1. **Live probe**: the thing itself answers right now (a command output, a repository log, a file's current bytes).
2. **File on disk**: the receipt, manifest, report or decision log, read directly.
3. **A summary of a file**: a handoff note or an agent's closing message. A pointer, not evidence.

The conversation you just had is not on the list. It is the most persuasive source and the least reliable: it is where the wrong claim felt obvious. Example: a team told a stakeholder "the menu is closed" for hours from memory of an earlier run while the device's own field said it was open. Read the field.

## 2. Run every command you intend to write down

A command that has not been executed is a hypothesis. Run each block (the read-only form is enough) and note the exit code. Then check what a reader will hit and the author will not: is the binary on `PATH`, is the flag spelled the way this platform spells it (`sha256sum` does not exist on macOS; `shasum -a 256` does), and is the path in the repository you think it is in.

## 3. Write the negative form

Positives describe the happy path the reader could have guessed. The negatives are the value: each one is a failure that already cost hours. Write them as imperatives with a one-clause reason ("Never flash directly; use the guarded publish path"). Keep six or seven, chosen by what the next agent would do by default.

## 4. Keep it a skill, not a manual

- **80 to 140 lines.** A loaded skill is context paid on every request. Deeper material goes in linked files.
- **`<name>/SKILL.md` at the top level** of the skills directory. Many loaders do not recurse into nested folders, so a deeper path is a skill nobody loads.
- **Frontmatter: `name` plus a one-sentence `description`** whose words are the words a future agent will search for (the words of the original ask), not your internal jargon.
- **Cite, do not restate.** If a neighboring skill owns a rule, name it in one clause and spend the lines on what only this work knows.
- **Placeholders for anything that moves or identifies**: `<host>`, `<repo>`, `<owner/repo>`. Never a credential, private address or customer name; skills get copied to machines you have not seen.

## 5. Do not duplicate what exists

Before writing, read the closest neighbor and state what your skill is *not*. Then cite it, narrow your scope around it, or drop the section. Search your skills directory for the topic word first.

## 6. Correct the record in the same pass

If the work proved a recorded fact wrong (an old note, a README, a memory file), fix the record now, dated, and say where the correction went. A skill that contradicts a stale note creates two sources of truth.

## 7. Prove discoverability

A skill nobody can find is not shipped. Start a fresh session (or list the catalog with your tool's skill listing) and confirm the skill appears with its description. Then give a fresh agent a prompt in the *original ask's* words and check it picks the skill. If it does not, rewrite the description, not the body.

## Never

- Never harvest from the conversation when a file or probe exists.
- Never include a command you did not run.
- Never ship positives without the negatives.
- Never paste a manual into the body; link it.
- Never put identifiers, hosts or credentials in the text.

## When to use

- You are asked to "skillify", "turn this into a skill", "codify what we learned", or "onboard the next agent".
- A project or incident just ended and its lessons would otherwise live only in a chat.

## How to use

1. Copy this folder into `~/.claude/skills/` (personal) or `.claude/skills/` inside a project, then ask Claude Code to use `work-to-skill-conversion` by name.
2. Point it at the artifacts (repo, receipts, logs), not the chat.

Example prompts:
- "Use work-to-skill-conversion to turn the migration we just finished into a skill, harvesting from the repo log and the receipts."
- "Use work-to-skill-conversion to review this draft SKILL.md: which commands were never run, and where are the negatives?"
