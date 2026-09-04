---
name: gate-erosion-audit
description: Audit any existing safety gate, guard, or verifier for five specific ways enforcement silently stops working — failing open on error, opt-in enforcement that defaults off, a gate grading its own evidence, a guard with only one enforced entry point, and asymmetric normalization — each with a concrete pattern to grep for.
---

# gate-erosion-audit

A gate that was written correctly can still stop enforcing without anyone noticing, because the failure isn't a crash — it's the gate quietly returning "pass" when it should return "fail." The gate still exists, still runs, still looks like a safety measure in the code and in the docs. It just doesn't block anything anymore. This is a checklist for finding that specific class of defect in gates, guards, and verifiers you already have — as distinct from designing a new one correctly the first time.

## The five patterns

### 1. Fail-open on error

The gate's happy path correctly blocks, but its error-handling path doesn't. Grep for:

- `|| true` immediately after a command whose exit code the gate is supposed to check
- `set +e` inside a script whose whole job is to fail loudly on a bad exit code
- an `EXIT` trap that forces `exit 0` regardless of what happened before it
- an error/exception branch that returns or exits with the *success* value instead of propagating the failure
- a broad `except:` (or equivalent) around the check itself that swallows the exception and falls through to the allow path

**Why it happens:** someone added error handling to make the gate "more robust" against a flaky check, and the robust behavior they picked was "don't block on an error" — which is exactly backwards for a security/quality gate. An error in a gate should be treated as a failure to prove safety, not as evidence of safety.

### 2. Opt-in enforcement (defaults off)

The gate is real and correctly written, but it only runs when an environment variable or flag is explicitly set — and that variable defaults to off, or isn't set anywhere in your actual deployment. Grep for the flag the gate reads, then confirm: is it actually set to "on" everywhere this gate is supposed to run? An enforcement mechanism that's off by default in production isn't a gate, it's a feature nobody enabled.

### 3. Self-supplied evidence

The gate reads its own pass/fail verdict from an artifact that the same run wrote earlier — or compares a measured value against a threshold that was itself derived from that same measurement. Both versions produce a gate that can never fail, because it's checking its own homework. Look for: a check that reads a status file the current run wrote instead of independently re-deriving the answer; a bar/threshold computed *from* the data it's being used to judge.

### 4. Single, unenforced entry point

A refusing guard exists and works correctly, but there's exactly one call site invoking it in a file (or system) with several places that could take the guarded action. Every other write-site bypasses the guard entirely, not through a bug, but because nobody wired it there. This one is a heuristic, not a certain finding — flag it for a human to confirm the other write-sites are actually meant to go through the same guard, rather than auto-"fixing" it.

### 5. Asymmetric normalization

The gate compares two values, but only one side of the comparison gets normalized (case-folded, whitespace-trimmed, decoded) before the comparison runs. Or: a lossy parser sits upstream of an otherwise-correct fail-closed check, so by the time the check runs, the input it's judging has already been silently mangled into something that always passes. The check itself can be perfectly correct and still never fire, because what it's comparing against has been corrupted one step earlier.

## How to run the audit

1. **Find the gate-shaped files.** Look for files whose name or primary content is a guard, gate, verifier, or precondition — not every file in the repo.
2. **For each, check the five patterns above** against the actual code, not the docs describing it. A doc that says "mandatory, no opt-out" is a claim; the code is the evidence.
3. **Grade severity honestly.** Most findings here are "the gate is weaker than its doc claims," not "the whole system is compromised" — inflating severity to look thorough is its own failure mode. Note which of the five patterns applies and cite the exact line.
4. **Verify before fixing.** A gate that "looks" self-evidencing might actually be re-deriving the value from an independent source under a confusing name. Read the actual data flow before changing anything.
5. **Fix conservatively.** Flip the fail-open default, turn an opt-in flag into opt-out (or remove the flag), route the missing write-sites through the existing guard, or normalize both sides of the comparison the same way. Don't rewrite the whole gate when a one-line default flip is the actual fix.

## Worked example

```bash
# A gate meant to block on any nonzero exit — but "robustly":
result=$(risky_check.sh) || true      # pattern 1: swallows the real exit code
if [ "$result" = "PASS" ]; then
  deploy
fi
```

If `risky_check.sh` crashes before printing anything, `$result` is empty, the `if` is false, and deploy correctly doesn't run — this particular case is accidentally safe. But if the script's failure mode ever prints anything containing the literal string `PASS` before erroring (a common shape for scripts that print partial progress), the gate now deploys on a crashed check. The fix isn't a cosmetic rewrite — it's checking the actual exit code:

```bash
if risky_check.sh; then
  deploy
fi
```

## When to use

- Reviewing an existing safety gate, permission check, or verifier you didn't just write, especially one you're about to start trusting more (wiring it into an unattended pipeline, raising its blast radius).
- After a "the gate should have caught this" incident — before assuming the gate needs new logic, check whether it stopped enforcing for one of these five reasons.
- Periodically, on any gate whose enforcement claim ("mandatory," "fail-closed," "blocks on any failure") is load-bearing for how much you trust automation built on top of it.

## How to use

**Install:** copy this folder into `~/.claude/skills/gate-erosion-audit/` for personal use, or `.claude/skills/gate-erosion-audit/` inside a project repo.

**Invoke:**

```
Run gate-erosion-audit over the deploy gate in this repo — check all five
erosion patterns against the actual code and cite file:line for anything
you find.
```

```
This safety check is documented as "mandatory, no opt-out" — use
gate-erosion-audit to verify that claim is actually true in the code.
```
