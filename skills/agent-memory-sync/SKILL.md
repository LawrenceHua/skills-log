---
name: agent-memory-sync
description: A git-backed persistent memory layout for AI agents — one fact per file with typed frontmatter, a single always-loaded index file, and a scheduled commit/rebase/push sync job — so what an agent learned survives session boundaries, machine switches, and even switching to a different agent tool.
---

# agent-memory-sync

Agent sessions are amnesiac by default: the correction you gave on Tuesday is
gone by Thursday, and a second machine (or a second agent tool) knows none of
it. Vendor-native memory features help but lock the memory inside one tool.
Plain Markdown files in a git repo turn out to beat everything else: readable,
diffable, portable across every agent CLI, and synced with machinery you
already trust.

## The layout

```
memory/
  MEMORY.md                  # the index — one line per memory, always loaded
  feedback_never_trust_selfreports.md
  project_billing_migration.md
  reference_staging_dashboard.md
  user_prefers_typescript.md
```

**One fact per file**, with typed frontmatter:

```markdown
---
name: never-trust-selfreports
description: one-line summary used to decide relevance during recall
metadata:
  type: user | feedback | project | reference
---

The fact itself. For feedback/project memories, follow with:
**Why:** the incident or reason behind it.
**How to apply:** what to do differently next time.
Link related memories with [[their-name]].
```

The four types keep recall sharp: `user` (who the human is — role, expertise,
preferences), `feedback` (corrections and confirmed approaches, *with the
why*), `project` (ongoing goals/constraints not derivable from the code —
convert relative dates to absolute), `reference` (pointers to external
resources).

**`MEMORY.md` is an index, never a container.** One line per memory
(`- [Title](file.md) — hook`); it's the only file loaded into every session,
so it must stay small. The agent reads the index, then opens only the relevant
memory files.

## The hygiene rules

- **Update, don't duplicate.** Before writing, check for an existing file that
  covers the fact; edit it instead. Delete memories that turn out wrong — a
  false memory is worse than none, because it arrives wearing the authority of
  "we established this."
- **Don't store what's already recorded elsewhere.** Code structure, git
  history, and project docs are better sources than a memory that goes stale.
  Memory is for what *only the conversation knew*.
- **Recalled memories are hypotheses.** They reflect what was true when
  written; verify a remembered file/flag/URL still exists before acting on it.

## The sync

A scheduled job (every 5–15 min, plus session start/end) in the memory repo:

```bash
set -e
cd "$MEMORY_REPO"
# refuse to run over a half-finished rebase
if [ -d .git/rebase-merge ] || [ -d .git/rebase-apply ]; then
  echo "rebase in progress — needs a human" >&2; exit 1
fi
# cheap secret scan before anything is committed
! grep -rInE 'sk-[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]|xox[bp]-|AKIA[A-Z0-9]{8,}' . --exclude-dir=.git \
  || { echo "secret-shaped string found — refusing to sync" >&2; exit 1; }
if ! git diff --quiet || ! git diff --cached --quiet || [ -n "$(git status --porcelain)" ]; then
  git add -A && git commit -m "memory: sync from $(hostname -s)"
fi
git pull --rebase && git push
date +%s > "$MEMORY_REPO/.last-sync-receipt"   # the receipt your meta-monitor checks
```

Details that matter: commit *before* pulling (never stash agent writes —
that's how memories silently vanish on conflict); fail loudly — don't swallow
a failed commit with `|| true`, and write a receipt on success so a monitor
can detect a wedged sync (see `background-agent-roster`); give the repo a
`.gitignore` for anything env/credential-shaped and let the secret scan
fail-closed; on rebase conflict prefer the version with more information and
flag it for review; run the sync in a
dedicated clone or worktree so it never fights your interactive session. Every
machine — and every agent tool you point at the directory — now shares one
brain. For a team, the repo can be shared; keep personal memories in a
separate local-only directory.

## When to use

- You correct an agent for the second time about the same thing.
- You work across two machines, or two agent CLIs, and want one memory.
- A long-running project accumulates decisions no single session can hold.

**Skip it for:** one-off tasks and throwaway environments.

## How to use

**Install:** copy this folder into `~/.claude/skills/agent-memory-sync/`.
Create the memory repo, then tell your agent tool to load `MEMORY.md` every
session (most tools have a persistent-instructions or memory-directory hook)
and to write new memories in the format above.

**Invoke:**

```
Set up agent-memory-sync: create the memory repo layout, write the frontmatter
template, add the sync script, and schedule it every 10 minutes. Then record
today's two decisions as project memories.
```
