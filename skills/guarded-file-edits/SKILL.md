---
name: guarded-file-edits
description: Edit files through an agent harness's read-before-write policy without burning turns on refusals — what each refusal message means and the single recovery each one needs.
---

# Guarded file edits

Most agent harnesses refuse to modify a file unless the current session has read it, and refuse again if the file changed after that read. In long sessions this is one of the most common tool-level failure families. This skill is not about editing syntax; it is about the *read receipt* the harness requires, and the two ways that receipt is lost.

## 1. A read is a receipt, not a copy

Before an in-place edit or whole-file overwrite, the runtime requires that this session has read that file. The receipt is per session and per file. It is invalidated by any change made outside the file tools — a shell redirect, a formatter, a code generator, another agent. It is not invalidated by your own successful edit through the file tools.

So there are exactly two ways to lose it: never having read the file, and the file moving under you. Every refusal below is one of those two.

## 2. The refusals and their one recovery each

Exact wording varies by harness; the meaning does not.

1. **"file has not been read"** (write to an existing file). Read it first. Do not route around this with a shell redirect — that writes blind, which is the state the policy exists to prevent.
2. **"file changed since it was read"** (edit). The receipt is stale; your cached `old_string` describes a file that no longer exists. Re-read, then apply the same intent to the current bytes.
3. **"file changed since it was read"** (whole-file write). The dangerous variant: the write would discard someone else's edit. Re-read and re-decide whether the overwrite is still right.
4. **"old_string was not found"**. The receipt was valid and the text genuinely is not there. Your copy is wrong (whitespace, a smart quote or dash, a line you already changed). Re-read the region and copy the exact bytes.
5. **"old_string matched N times"**. Ambiguous. Widen the match with surrounding context. A replace-all flag is the wrong default: it edits occurrences you never looked at.
6. **"not found" on read**. No receipt is possible. List the parent directory instead of guessing a second path; a path that "should" exist is as often a symlink or a mount as a typo.

## 3. Out-of-band writes void the receipt

Any write that bypasses the file tools — `sed -i`, `>>`, a heredoc, a code formatter, a generator, a checkout — leaves you holding a receipt for a file that changed. The next edit then fails with refusal 2, and it looks like a tool problem when it is bookkeeping.

Rule: **one writer per file per turn.** If a script must write the file, finish every script write, then re-read, then edit. In practice the out-of-band writer is usually your own previous command.

## 4. Recover by re-reading, never by re-issuing

After a refusal, the failure mode is retrying the identical call, or "fixing" it by writing the whole file from the copy in context. Both are wrong because your copy is what is out of date.

1. Read the file (bounded, if it is large).
2. Re-derive the smallest correct `old_string` from what is there now.
3. Apply, then re-read the changed region or `grep -n` the new text.
4. If a second refusal arrives, stop retrying and ask why the file is moving: another agent, a file watcher, a generator on a schedule. A file that changes between your read and your edit is evidence about a writer, not about your edit.

## 5. Whole-file writes and the path you did not mean

Write tools commonly create missing parent directories. A mistyped path therefore does not fail — it succeeds into a new tree nothing reads, and the failure surfaces later as "my change is not live". After a whole-file write to a path you have not written before:

```sh
ls -la "$(dirname <path>)" && wc -c <path>
```

If a running process serves the file, writing it *is* the deploy, and verifying the bytes you wrote is not verifying the bytes served. For a script a scheduler may execute mid-write, write `X.tmp` and rename; preserve the file mode, which a rename does not carry over.

**If the file is generated on a cadence, edit the generator.** A correct edit to a generated file is destroyed by design. Find the writer (`grep -rl '<filename>'` over the repo's scripts and scheduler configs) before touching the output. If the generator is read-only or vendor-owned, name the durable fix — a hook, an upstream patch, a change to what the generator reads — in the handoff.

## 6. Prove the edit landed

A success line is the tool's report about itself. Check the artifact, with two of these three (grep alone passes when the text landed twice or in the wrong copy):

```sh
grep -n '<new text>' <path>
shasum -a 256 <path>
git diff --stat -- <path>
```

When the change is behavioral, the proof is the test or a live probe, not the diff.

## 7. Reproduce the policy in a minute

Run this before trusting a new harness version. In a scratch directory create `f.txt` (two lines) and `dup.txt` (two identical lines), then as tool calls:

- write `f.txt` without reading it → refusal 1
- read `f.txt`, append a line from the shell, edit `f.txt` → refusal 2
- read `f.txt`, edit with an absent `old_string` → refusal 4
- read `dup.txt`, edit with `old_string="dup"` → refusal 5
- read a nonexistent file → refusal 6
- write into a nonexistent subdirectory → succeeds and creates it; list the directory to prove it

If any step succeeds differently, the policy moved. Record that before relying on this table.

## Never

- Never retry a refused edit unchanged.
- Never shell-edit a file you are also editing with the file tools without re-reading in between.
- Never use replace-all to resolve "matched N times" when you can widen the context.
- Never reconstruct a file from context after a stale-receipt refusal — you will drop whatever the other writer did.
- Never treat "Created file" as proof of the right path.
- Never edit a file another agent may be writing without first claiming it (a lock, a lease, or a separate worktree).

## When to use

- An edit or write is refused with any message above.
- A file must be touched by both a script and an edit tool in one session.
- Several agents may write the same file.
- A whole-file write may have landed somewhere you did not mean.

## How to use

1. Copy the `guarded-file-edits` folder into `~/.claude/skills/` (personal) or `.claude/skills/` inside a project, then ask Claude Code to use the skill by name.
2. Example prompts:
   - "Use the guarded-file-edits skill: my edit to `config.yaml` says the file changed since it was read. Recover without clobbering anything."
   - "Use guarded-file-edits to run the policy self-test in a scratch directory and tell me whether this harness's refusal behavior matches the table."
