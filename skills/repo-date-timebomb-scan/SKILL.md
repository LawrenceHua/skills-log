---
name: repo-date-timebomb-scan
description: Find committed expiry dates that tests or runtime checks compare with the real clock, so a branch does not turn red or stop working on a day when nobody changed anything.
---

# Repository date time-bomb scan

A repository can hold dates that quietly arm themselves: a licence or claim record with an expiry, a lease file, a certificate fixture, a "review by" field in a policy that a test reads. On the day it passes, every pull request into the branch fails, and the diff offers no clue.

## 1. Scan the ref, without checking it out

```sh
REF=origin/<branch>        # fetch first if the ref may be old
git grep -nIE '20[0-9]{2}-[01][0-9]-[0-3][0-9]' "$REF" -- . ':!*.lock' ':!*lock.json' ':!*CHANGELOG*' |
python3 -I -c '
import re, sys, datetime as dt
WARN_DAYS = 30
today = dt.datetime.now(dt.timezone.utc).date()
key = re.compile(r"expir|valid[_ -]?(until|to|through)|not[_ -]?after|renew|review[_ -]?by|(?<![a-z])lease|deadline|sunset", re.I)
for line in sys.stdin:
    body = line.split(":", 3)[-1]  # skip the ref, path and line number
    if not key.search(body):
        continue
    for s in re.findall(r"20\d\d-\d\d-\d\d", body):
        try:
            d = dt.date.fromisoformat(s)
        except ValueError:
            continue
        days = (d - today).days
        if days <= WARN_DAYS:
            print(days, line.rstrip()[:200])
' | sort -n
```

Negative numbers have already passed.

This is a first pass, and its misses matter:
- The key word and the date may be on different lines. Open structured files that hold records (ledgers, registries, policy and contract files) and inspect their date fields.
- Dates may use other formats or epoch numbers.
- Encoded certificates carry their expiry inside the file; read each with `openssl x509 -noout -enddate`.
- Some expiries are computed from a start date plus a duration. Search for the comparison in code (current time against a stored value) and trace what feeds it.

An empty result means "nothing matched these patterns", not "no time bombs".

## 2. Decide which dates are live

For each hit, find the readers (`git grep -n '<file or field name>' "$REF"`) and classify it:

| Class | Sign | Action |
|---|---|---|
| Live-read | a test, build step or runtime check compares it with today | report with the days left |
| Frozen fixture | an input to a test that supplies its own clock, or a deliberately past value | ignore |
| Historical | release notes, migration names, dated records | ignore |
| Unclear | no reader found | list it for the owner |

Where practical, confirm a live-read date by running the relevant test in a scratch copy with an injected or faked clock set just past the date. It should fail there and pass the day before.

## 3. Report, do not bump

For every live date: file and line, date, days left, what breaks, and who owns the renewal.

Extending an expiry on a licence, legal claim, lease or certificate record asserts that something was re-verified. That is the owner's decision. Never move the date just to turn CI green.

## 4. Make it routine

Run it weekly on every release branch and file anything inside the warning window with the branch owner. Run it first whenever CI fails on a branch nobody changed.

## When to use

- CI suddenly fails with no related code change, especially on every branch at once.
- Before cutting a release.
- As a periodic sweep of long-lived branches.

## How to use

1. Copy the `repo-date-timebomb-scan` folder into `~/.claude/skills/` for personal use, or `.claude/skills/` inside a project.
2. Ask Claude Code to use the skill by name.
3. Example prompts:
   - "Use the repo-date-timebomb-scan skill on origin/main and list every live expiry inside 30 days with the test that reads it."
   - "CI went red overnight with no commits. Use repo-date-timebomb-scan to check whether a committed date passed."
