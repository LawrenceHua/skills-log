---
name: bounded-output
description: Bound every command result and file read by bytes before it enters an agent's context, keeping the full text on disk, so one noisy log or listing does not tax every later request in the session.
---

# Bounded output

Every tool result is inserted into the conversation once and then re-sent as
part of the context on every later request in the same session. A single
50 KB result with 400 requests still to go is paid for 400 times. The tool's own
cap (often around 50 KB) is a safety net, not a budget. Pick a budget (about
8 KB is a good default) and enforce it yourself.

## Rules

1. **Never dump a log.** Read it through a bounded reader: a short head, a longer
   tail, totals, and a note on how to widen.
2. **Wrap any command whose output size you cannot predict** (process listings,
   scheduler listings, recursive `ls`/`find`, `git log -p`, test and build
   output, JSON from an API or a receipt). The wrapper keeps the full output in a
   temp file and prints only a byte-bounded slice plus the file path.
3. **`| head -N` is a line bound, not a byte bound.** One line of minified JSON
   can be tens of KB. Bound by bytes first, then lines.
4. **Pick the end that holds the answer.** Build and test output: the tail.
   Listings and schemas: the head. Errors in a long log: a numbered pattern
   search with a match cap, not a read of the whole file.
5. **Truncation is never silent.** The footer must say how many bytes were shown
   out of how many, which end, and where the full text lives.
6. **Preserve the exit status** of the wrapped command, and merge stderr into the
   bounded stream (that is usually what the agent needs to see).
7. **Do not re-run to see more.** Search the saved file instead. Re-running a
   command can change its output or repeat a side effect.

## Helpers (POSIX shell)

Put these in a file you source from your shell profile, or in a small script
directory on your `PATH`.

```sh
# bo [-c BYTES] [-t] -- command args...   bounded command runner
bo() {
  budget=8192; mode=head
  while [ $# -gt 0 ]; do
    case "$1" in
      -c) budget=$2; shift 2 ;;
      -t) mode=tail; shift ;;
      --) shift; break ;;
      *) break ;;
    esac
  done
  out=$(mktemp "${TMPDIR:-/tmp}/bo.XXXXXX") || return 1
  "$@" >"$out" 2>&1; rc=$?
  total=$(wc -c <"$out" | tr -d ' ')
  if [ "$mode" = tail ]; then tail -c "$budget" "$out"; else head -c "$budget" "$out"; fi
  if [ "$total" -gt "$budget" ]; then
    printf '\n[bo: showed %s of %s bytes (%s); full output: %s]\n' "$budget" "$total" "$mode" "$out"
  fi
  return $rc
}

# rd FILE   bounded file/log reader: head + tail + totals
rd() {
  f=$1
  size=$(wc -c <"$f" | tr -d ' '); lines=$(wc -l <"$f" | tr -d ' ')
  if [ "$size" -le 8192 ]; then cat "$f"; return; fi
  head -n 30 "$f" | head -c 3000
  printf '\n[... %s lines / %s bytes total; middle omitted; use grep -n PATTERN "%s" ...]\n' "$lines" "$size" "$f"
  tail -n 90 "$f" | tail -c 5000
}
```

Usage:

```sh
bo -- ps aux                    # process table, bounded
bo -t -- npm test               # tail of a test run
bo -c 32768 -- jq . report.json # widen the budget explicitly, never drop it silently
rd build.log                    # head + tail of a big log
grep -nE 'Error|Traceback' build.log | head -40   # targeted search of a log
```

## Procedure

1. Before running a command, ask: could this print more than ~8 KB? If you
   cannot say no with confidence, wrap it.
2. Before reading a file, check its size (`wc -c`). Over ~8 KB: use the bounded
   reader, a pattern search, or a line range. In an editor tool, always pass a
   line limit for anything over ~200 lines.
3. When the bounded slice is not enough, widen on purpose: raise the byte budget
   or search the saved full-output file. State in your notes why you widened.
4. When the payload is itself the deliverable (a diff you must apply, a JSON
   document you must copy verbatim), size the budget to it and say so, rather
   than dropping the bound.
5. Never paste raw tool output into a prompt, handoff, or report. Quote the few
   lines that carry the finding and cite the file that holds the rest.

## When to use

- Running listings, build or test commands, or log tails whose size you cannot predict.
- Reading any log or data file over a few KB.
- A long agent session whose context keeps growing and whose cost or latency is climbing.
- Writing a brief or handoff that is tempted to paste command output.

## How to use

Install: copy this folder to `~/.claude/skills/bounded-output/` (personal use) or
`.claude/skills/bounded-output/` inside a project. Then source the helpers above
in your shell profile so the agent's shell can call `bo` and `rd`, and ask
Claude Code to use the `bounded-output` skill by name.

Example prompts:

- "Use the bounded-output skill. Run the full test suite and tell me which tests failed, without pasting the whole log."
- "Use the bounded-output skill to find why this 40 MB log has errors: search it, show me only the relevant lines, and tell me where the full file is."
