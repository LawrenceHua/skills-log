---
name: fail-closed-guards
description: When a guard/gate/precondition depends on data that might be missing, make the missing-data fallback REFUSE the action, not allow it — and confirm every write-site actually populates the field the guard reads.
---

# fail-closed-guards

Any guard of the shape `if predicate(value): allow_action()` has a hidden failure mode: what does it do when `value` was never set? If the chosen default makes the predicate evaluate to "allow," the guard is dead code from the moment it's written — it will never actually block anything, and nobody will notice until the exact scenario it was supposed to prevent happens in production.

## When to use

- You're writing or reviewing any guard, gate, permission check, or precondition that reads a field which might be missing, unset, or not-yet-written (a race condition, an optional field, a field only some code paths populate).
- You see a pattern like `dict.get(key, DEFAULT)`, `value or DEFAULT`, or `getattr(obj, "x", DEFAULT)` feeding directly into an `if` that gates a sensitive action.
- A guard "isn't firing" and you can't tell why — check the default first.

## The rule

For any guard of the form `if predicate(value): allow_action()`:

1. **Identify what `value` is when the data is missing** — not stamped, not set, a race condition, never initialized, an optional field nobody filled in.
2. **Choose the default so `predicate(missing) == False`** — never `True`.
3. **Confirm every write-site actually stamps `value`.** A fail-closed default doesn't help if nothing ever writes the field in the first place — the guard will "always fire closed," which just masks the real bug of a field never being populated.

## The canonical anti-pattern

```python
# BEFORE — fail-OPEN default
last_action_time = state.get("t", 999.0)
if (now - last_action_time) > 4.0:
    allow_action()  # 999.0 reads as "a long time ago" -> ALWAYS fires
```

The fallback `999.0` was picked to mean "the last action was a long time ago, so it's safe to proceed." But if none of the code paths that build `state` actually stamp `"t"`, the guard's predicate sees `999.0` on every single call — it always evaluates true, so the guard never actually blocks anything. This is dead code wearing a guard's clothing.

```python
# AFTER — fail-CLOSED default, plus the write-sites fixed
last_action_time = state.get("t", 0.0)
if (now - last_action_time) > 4.0:
    allow_action()  # 0.0 reads as "never stamped" -> predicate is False -> REFUSED

# every site that builds `state` must now actually stamp it:
state["t"] = time.time()
```

## Checklist for any new guard

1. What's the data the guard depends on? (a variable, a dict key, a DB row, a field on an object)
2. What does that data look like when it's MISSING? (`None`, `""`, `0`, `False`, key absent, row not yet inserted)
3. What does the guard's predicate return on that missing value?
4. **If the answer to #3 is "allow" → stop and flip the default or invert the predicate.**
5. Who writes the field? Grep for every write-site and confirm each one actually writes it — a fail-closed default is worthless if the field is never populated at all.
6. Add a log line on the "guard fired because the field was missing" path, so the next person debugging knows the safe-fail kicked in rather than a real denial.

## Worked examples

**Reject-if-recent guard** — read your predicate carefully; the safe default depends on what it's testing, not just "pick a small/large number":

```python
# Refuse the action if something else JUST happened (need to wait it out)
last_t = state.get("t", now)   # default = "just now" = the safe REFUSE branch
if (now - last_t) < 1.5:
    return refuse("too soon — wait for the in-flight action to finish")
```
A naive `state.get("t", 0.0)` default would be fail-*open* here — `now - 0.0` is huge, so the "too soon" check would never trigger on a missing timestamp. The safe default flips depending on which direction the predicate refuses in.

**Permission default:**
```python
# FAIL-CLOSED: default = guest, which never matches "admin"
if user.get("role", "guest") == "admin":
    return allow()

# ANTI-PATTERN — FAIL-OPEN: default = admin
if user.get("role", "admin") != "guest":
    return allow()
```

**Feature-flag default:**
```python
# New/incomplete features default OFF, not ON
if flags.get("new_path_enabled", False):
    new_path()
else:
    old_path()
```
If the flag is missing from config (new environment, partial deploy), the safe default is the old, proven path.

## When NOT to apply this

- **Performance-tuning defaults** (`cache_size: int = 256`) — no safety concern, just pick something reasonable.
- **Display/UI defaults** (`theme: str = "light"`) — a UI fallback, not a guard.
- **Backward-compat shims for legacy data** — the default IS the intended legacy behavior, by design.

This applies specifically to guards, gates, and preconditions that decide whether a *sensitive* action proceeds.

## How to use

**Install:** copy this folder into `~/.claude/skills/fail-closed-guards/` for personal use, or `.claude/skills/fail-closed-guards/` inside a project repo.

**Invoke:**

```
Review the hangup/cancel guard in this file with fail-closed-guards — walk the
checklist and tell me what the predicate does when its input field is missing.
```

```
I added a permission check but I'm not sure the default is safe. Apply
fail-closed-guards to it before I merge.
```
