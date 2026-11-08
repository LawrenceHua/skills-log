---
name: browser-profile-cache-reclaim
description: Reclaim disk from a retired automation's browser profile by deleting only the regenerable cache directories while keeping cookies, saved logins and profile state.
---

# Browser profile cache reclaim

A retired automation (scraping, QA, agent browsing) usually leaves a Chromium-style browser profile that is
mostly regenerable cache sitting next to a few irreplaceable identity files. The reclaim deletes the cache class
in place, keeps the identity class, and proves the result with a before/after disk reading.

This skill covers only the profile-anatomy split and its traps. Whether the directory is still referenced by a
scheduled job, and the general full-disk workflow, are separate questions: answer them first.

## Anatomy: cache vs identity

Delete in place (regenerable; the browser rebuilds them on next launch):

```sh
du -sm "<profile>"/{Cache,"Code Cache",GPUCache,"Service Worker/CacheStorage","Service Worker/ScriptCache",GrShaderCache,ShaderCache,"components/Crashpad"} 2>/dev/null
```

Keep (deleting these loses the logged-in session, sometimes the only copy):

- `Cookies`, `Login Data`, `History`, `Web Data`
- `Local State`, `Preferences`, `Secure Preferences` (profile structure and encryption keys)
- Anything the automation authored outside the profile (research outputs, receipts)

Never delete the profile root because an archive of it "would be smaller than the directory": the bytes you want
to remove are exactly the ones the archive does not need.

## The loop (run in this order)

1. **Prove it is not live.** Both probes must come back empty:
   ```sh
   ps aux | grep -i "<program name>" | grep -v grep | wc -l     # must be 0
   lsof -- "<profile>" 2>/dev/null | head -3                     # no output = nothing holds files open
   ```
   If either shows activity, stop. A cache that is being written is not regenerable.
2. **Measure.** Record `du -sm` of the whole profile and of each candidate directory, and `df -m <volume>` for
   the free-space baseline (MiB, not GiB).
3. **Back up first.** Archive the whole profile next to the original so the delete is reversible for one
   verification cycle:
   ```sh
   tar -c -C "<app-data-dir>" "<profile-dir-name>" | zstd -q -f -o "<archive>.tar.zst"
   shasum -a 256 "<archive>.tar.zst" > "<archive>.tar.zst.sha256"
   ```
4. **Delete only the cache class**:
   ```sh
   rm -rf "<profile>/Cache" "<profile>/Code Cache" "<profile>/GPUCache" "<profile>/Service Worker/CacheStorage"
   ```
5. **Verify.** `df -m` again (freed space on APFS can lag a few seconds; re-probe once), then confirm the identity
   files still exist.
6. **Retire the backup** after the delta lands and, if the program ever runs again, its next run still works.

## Negatives (each one cost something)

- Do not run while the owning program has a process. "It is retired" is a claim; `ps` and `lsof` are the probe.
- Do not trust `du -sm <dir>/*/` with a trailing slash to size candidates: if a subdirectory is a symlink into
  the profile, `du` follows it and counts the same bytes twice. Test for symlinks with `-L` first.
- Do not report the delta in `df -g`: a 2.8 GiB reclaim rounds to 0 or 1 in GiB columns. Use `df -m`.
- Do not delete `Service Worker/` wholesale; only its `CacheStorage` and `ScriptCache` children. The parent holds
  registration state some automations need to reattach.
- Do not keep the backup archive indefinitely; its job is one verification cycle.

## Verification

- `df -m` before and after in the same shell.
- If the browser has a headless mode, launch it once against the profile; a log line naming the profile (or a
  still-logged-in page) is the receipt.
- Record one ledger line: `<profile dir>: <MiB before> -> <MiB after>, df delta <x> MiB, archive sha <hash>`.

Example outcome: a retired research profile went from about 3.1 GiB to about 290 MiB, with about 2.8 GiB freed and
the identity files intact, confirmed by `df -m` and a clean `ps` probe.

## When to use

- A closed project's app-data folder holds gigabytes of browser cache and someone proposes deleting the whole
  profile.
- You need disk back but the logged-in session (or the only copy of an export) must survive.

## How to use

1. Copy this folder to `~/.claude/skills/browser-profile-cache-reclaim/` (personal) or
   `.claude/skills/browser-profile-cache-reclaim/` inside a project.
2. Ask Claude Code to use the `browser-profile-cache-reclaim` skill by name.

Example prompts:

- "Use browser-profile-cache-reclaim on `~/.old-scraper/chrome-profile`. Prove nothing is running, back it up, delete
  only the caches, and show the `df -m` delta."
- "Someone wants to `rm -rf` the whole profile of a retired QA bot. Use browser-profile-cache-reclaim to tell me what
  is safe to remove and what must stay."
