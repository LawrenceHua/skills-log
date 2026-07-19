---
name: safe-project-retirement
description: Enumerate every surface tied to a dead project (repos, scheduled jobs, dashboards, notes), get human confirmation, then archive everything reversibly with an undo manifest instead of deleting it.
---

# safe-project-retirement

Killing a project is never just one delete — it's scattered across a git repo, a cron job, a dashboard entry, and a dozen notes that still mention it. The core insight: treat retirement as an enumerate → confirm → archive-reversibly → log-undo-manifest pipeline, and ban hard-delete entirely, because "dead" and "gone forever" are different claims and only one of them is safe to get wrong.

## Method

1. **Enumerate every surface.** Given a project keyword/name, search all of:
   - Git repositories (local clones, matching directory names, remotes)
   - Scheduled jobs / background daemons (cron, launchd-style agents, any job whose name or command references the project)
   - Dashboards or status pages that list or link to it
   - Personal notes / memory entries that mention it (todo lists, journals, agent memory files)

   Don't stop at the first hit — grep by keyword across every category, not just the obvious one (a repo named `foo` might have a scheduler job named `foo-sync`).

2. **Present and confirm.** Print the full list of what was found, grouped by surface type, before touching anything. Require an explicit human go-ahead (a literal "yes" or a list of IDs to proceed with) — never auto-archive on a match. Let the human exclude items ("keep the dashboard entry, archive the rest").

3. **Archive reversibly, never hard-delete.**
   - Repos: move into an archive directory (e.g. `~/archive/projects/<name>-<date>/`), don't `rm -rf`.
   - Scheduled jobs: disable, don't delete the definition — unload it and rename the file with a `.disabled` suffix so it's inert but recoverable.
   - Dashboard/status entries: tag as archived/hidden, don't remove the row.
   - Notes/memory entries: tag matching entries `[archived]` in place, don't delete the text.

4. **Log an undo manifest.** Every move/disable action gets one line in a manifest file recording exactly what happened, so the whole retirement can be reversed by replaying it backwards. Example entries:

   ```json
   {
     "surface": "git-repo",
     "action": "moved",
     "from": "~/code/the-old-experiment",
     "to": "~/archive/projects/the-old-experiment-2026-07-19",
     "timestamp": "2026-07-19T14:02:11Z"
   }
   {
     "surface": "scheduled-job",
     "action": "disabled",
     "job": "the-old-experiment-nightly-sync",
     "from": "~/Library/LaunchAgents/com.user.the-old-experiment-sync.plist",
     "to": "~/Library/LaunchAgents/com.user.the-old-experiment-sync.plist.disabled",
     "unloaded": true,
     "timestamp": "2026-07-19T14:02:14Z"
   }
   ```

5. **Scrub before sharing.** If any archived artifact ends up in an external or shared location (a shared drive, a public repo, a team channel), strip private/internal names, paths, and credentials from it first — archiving reversibly for yourself doesn't mean the archive is safe to hand to someone else unmodified.

Hard-delete is banned throughout because retirement decisions are made on incomplete information — "dead" is a guess about the present, and the only cheap insurance against guessing wrong is keeping everything one move away from restoration.

## When to use

- A project, experiment, or prototype is confirmed dead or superseded and you want it out of your active working set
- You're doing periodic cleanup and don't want to hand-track every cron job, dashboard entry, or note tied to something
- Before deleting anything project-related by hand — this is the check that stops an accidental hard-delete
- Migrating or consolidating machines and deciding what to leave behind vs. carry forward

## How to use

**Install:** copy this folder into `~/.claude/skills/safe-project-retirement/` for personal use, or `.claude/skills/safe-project-retirement/` inside a project repo.

**Invoke:**
```
Retire the-old-experiment — find every repo, cron job, dashboard entry, and note tied to it, show me the list, and archive everything reversibly once I confirm.
```
```
I'm done with project-nightowl. Enumerate its surfaces and give me an undo manifest before you touch anything.
```
