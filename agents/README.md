# Agents — drop-in verifier bench

Five single-purpose subagent definitions in the
[Claude Code custom-agent format](https://docs.claude.com/en/docs/claude-code)
(Markdown with YAML frontmatter). Other tools can use the body text as a system
prompt for an equivalent role.

| Agent | Role | Tools | Model tier |
|---|---|---|---|
| [`adversarial-verifier.md`](adversarial-verifier.md) | Refute-by-default checker for "done/fixed/shipped" claims — the claim is false until it personally reproduces the evidence | Read, Grep, Glob, Bash | strong |
| [`hostile-reviewer.md`](hostile-reviewer.md) | Adversarial PR reviewer with domain drills (security, correctness, ML/data, process, perf, a11y) and an "attacked and survived" proof-of-work section | Read, Grep, Glob, Bash | strong |
| [`completeness-critic.md`](completeness-critic.md) | End-of-run gap-finder — walks the spec line-by-line against the artifact to find what was never checked at all | Read, Grep, Glob, Bash | strong |
| [`cheap-grader.md`](cheap-grader.md) | Mechanical rubric scoring with per-criterion evidence pointers; structured output only, never essays | Read, Grep, Bash | cheapest |
| [`researcher.md`](researcher.md) | Multi-query web sweep with source-quality ratings and falsifiable quoted claims | WebSearch, WebFetch, Read, Bash | mid |

## Design rules (why these work)

- **Fresh context.** A verifier must never share context with the work it
  checks. Spawn it as a subagent, hand it only the claim + artifact paths.
- **Read-only by contract — enforce it if your runs are unattended.** No agent
  here gets Edit or Write, and each prompt forbids mutating commands. But be
  honest about the limit: **Bash can mutate** (`sed -i`, `>`, `git push`), and
  the tool list alone doesn't stop that — the read-only property is
  prompt-level. For interactive use with permission prompts that's fine; for
  unattended or auto-approve sessions, add hard enforcement: deny rules in your
  tool's permission settings (e.g. deny `Edit`, `Write`, `Bash(git push:*)`,
  `Bash(rm:*)` for these agents), or remove Bash entirely from the graders and
  accept weaker evidence. An agent that can edit can "fix" its way to a
  passing verdict.
- **Evidence or nothing.** Every verdict line requires quoted command output or
  `file:line` evidence. "Looks good" is not a finding.
- **Pin the model.** Each file pins its model tier explicitly — subagents
  otherwise silently inherit your (expensive) main-loop model. Adjust the
  `model:` values to your setup; the tier logic is what matters: grading is
  cheap-tier work, adversarial verification is strong-tier work.

## Install

Copy into your user-level agents directory (the glob skips this README):

```bash
cp agents/[a-z]*.md ~/.claude/agents/
```

Then invoke from any session, e.g.:

```
Spawn the adversarial-verifier agent on this claim: "the migration is complete
and all tests pass". Give it the repo path and the test command.
```
