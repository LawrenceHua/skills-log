---
name: skill-miner
description: Periodically scan your own AI-assistant session transcripts for repeated workflow patterns, cluster them, draft candidate reusable skills via a cheap LLM, self-grade the drafts, and queue them for manual human approval — never auto-promoting anything.
allowed-tools: [Bash, Read, Write, Edit, Grep, Glob]
---

# skill-miner

If you use an AI coding assistant heavily, you end up repeating the same
multi-step workflows over and over across sessions — the same kind of
review, the same kind of investigation, the same kind of report. Most of
those repeated patterns would make good reusable skills, but nobody has
time to notice them by hand. This skill mines your own session history for
those patterns, drafts candidate skill files, and — critically — queues
them for a human to approve or reject. It never promotes a skill on its
own.

## When to use

- Run it on a schedule (weekly is a reasonable cadence) to surface what
  you've been repeating.
- Run it manually whenever you want to ask "what am I repeating lately?" or
  "what skills should I add?"
- Skip promotion (dry-run mode) whenever you just want the analysis without
  generating candidate files.

## Trigger phrasing

Treat these as semantic triggers, not exact strings: "mine skills," "what
skills should we add," "what patterns am I repeating," "audit my workflow
patterns," "look at this week's sessions," "scan transcripts for skills."

Suppress the run if you've flagged your own system with an emergency-stop
condition, if the user explicitly asked for analysis only (no drafting), or
if there simply isn't enough new session data since the last run to be
worth clustering.

## The phases

Before doing anything, write a one-line act-or-observe note to your own
log: what triggered this run, what it's about to touch, whether it's
reversible (it is — deleting the candidate files undoes everything), and
whether you're actually executing or just observing this time.

### 1. Discover

Walk your session-transcript directory for whatever coding assistant you
use. Exclude sessions you've already processed (keep a small "seen
sessions" list so re-runs don't reprocess old data). Default to a rolling
window (e.g. the last 7 days).

### 2. Parse and filter

Parse each transcript into turns. Drop sessions with too few real user
turns to contain a repeatable pattern (a floor of ~3 is reasonable). Add a
recursion guard: skip any session that is itself about mining/promoting
skills, or whose working directory is your own automation/state directory
— otherwise the miner starts mining itself.

### 3. Scrub PII and secrets (layered defense — don't skip this)

Before any of this data touches an LLM or a stored candidate file, run it
through multiple layers of scrubbing:

1. **Specific credential patterns** — API keys, OAuth tokens, cloud
   provider keys, bearer/JWT tokens, private-key blocks, anything
   key-shaped.
2. **General PII patterns** — phone numbers, emails, physical addresses,
   government/account IDs, anything else specific to your domain.
3. **An entropy-based catch-all** — flag any remaining high-entropy token
   over a length threshold that didn't match a known pattern; when in
   doubt, redact it rather than let it through.

Keep a small golden-fixture test suite for this scrubber and run it before
trusting any given version — a scrubbing regression is exactly the kind of
bug you want to catch before it ships a secret into a candidate skill file.

### 4. Embed and cluster

Turn each session's request pattern into a vector (a local, free embedding
model is enough — no need to call out to a paid API for this step) and
cluster similar sessions together (a density-based clustering algorithm
like HDBSCAN works well because it doesn't force every session into a
cluster). Weight the embedding toward the actual request text, with a
smaller weight on the sequence of tools used, since two sessions can use
the same tools for very different reasons.

### 5. Draft, validate, and self-grade

For each cluster that's big enough and spans more than one distinct day
(a one-off isn't a pattern yet):

1. Ask a cheap LLM to draft a `SKILL.md` from the cluster's representative
   sessions.
2. Run a small validator: valid frontmatter, required fields present, no
   PII/secret leakage, a unique kebab-case name, and a real methodology
   section (not just a description).
3. Self-grade the draft with a second LLM call and require a minimum score
   before it's queued — low-quality drafts get discarded, not queued for a
   human to wade through.
4. Cap how many candidates you generate per run, sorted by cluster size, so
   review stays manageable.

### 6. Persist and queue for human approval

Write each accepted candidate to a candidates directory and append a row to
a candidates log. Queue it for approval through whatever channel you
actually check — a chat message, an email, a pull request — with a short
promote/reject action a human can trigger. Give queued candidates an
expiry so stale ones don't linger forever.

### 7. Notify

Post one short digest message: how many candidates are ready, one line per
candidate (cluster size, days spanned, self-grade, how to approve or
reject it).

## Output and verification

- **On success:** the run exits cleanly, an audit log has one row per
  phase with counts, and the candidates log has any new rows.
- **On failure:** the run exits non-zero so your scheduler retries; after
  repeated consecutive failures, escalate a notification rather than
  failing silently forever.
- **Dry-run:** parse and cluster only — no LLM calls, no writes — useful
  for "just show me the patterns, don't draft anything yet."

## Failure modes

| Symptom | Likely cause | Fix |
|---|---|---|
| Self-test fails on a PII check | A scrubbing pattern regressed or a new secret shape appeared | Add the new pattern to the scrubber and bump its version |
| Self-grade is consistently low | The drafting prompt has drifted | Revise the drafting prompt |
| No clusters ever surface | Clustering threshold too strict | Lower the minimum cluster size |
| It's mining itself | Recursion guard missed a path/keyword | Add the missing exclusion pattern |
| Scheduled run silently stops firing | The scheduler lost its registration after an environment change | Re-register it, and add a periodic health check that does so automatically |

## How to use

**Install:** copy this folder into `~/.claude/skills/skill-miner/` for
personal use. This is inherently a personal-workflow tool — it reads your
own session history, so it doesn't make sense to share verbatim across a
team the way a stateless methodology skill does. Wire the "discover" step
to wherever your coding assistant stores session transcripts, and the
"notify" step to whatever channel you actually check.

**Invoke:**

```
Run skill-miner in dry-run mode over my last two weeks of sessions — just
show me the clusters, don't draft anything yet.
```

```
Mine my sessions for repeated patterns and draft candidate skills for
anything that shows up on at least 2 different days — queue them for my
approval, don't auto-promote.
```
