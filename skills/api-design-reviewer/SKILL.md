---
name: api-design-reviewer
description: A static REST API design review — lints naming/method/status-code/error-format conventions, diffs two spec versions to classify breaking vs. non-breaking changes, audits the versioning strategy, and produces a weighted design scorecard (consistency, docs, security, usability, performance).
---

# api-design-reviewer

Convention drift in a REST API — kebab-case here, camelCase there, one endpoint returning a bare error string while another returns a structured object — is easy for any single PR review to miss and expensive to fix once clients depend on the inconsistency. This is a static, read-only review pass that catches it before the API ships, plus a breaking-change diff for anyone bumping a spec version.

## The method

**1. Lint conventions.** Check, and flag any inconsistency within the same project:
   - Resource naming (commonly kebab-case for resource paths, camelCase for JSON fields, snake_case for query params — the exact convention matters less than *consistency* within one project)
   - HTTP method usage (`GET` safe and idempotent, `POST` create, `PUT` full replace and idempotent, `PATCH` partial update, `DELETE` idempotent)
   - URL structure (`/api/v1/{resource}/{id}/{sub-resource}` and similar predictable nesting)
   - Status code usage (2xx success, 4xx client error, 5xx server error, used consistently for the same situation across endpoints)
   - Error response shape (one consistent structured format across every endpoint — RFC 9457 Problem Details is a reasonable default if there's no existing convention)
   - Documentation coverage (every endpoint has a description, every parameter has a type and description, every response code has an example)

**2. Detect breaking changes between two spec versions.** Given an old and a new API spec (or two commits of the source route definitions), classify every difference as BREAKING, NON-BREAKING, or DEPRECATED:
   - Endpoint removal → BREAKING
   - Response field renamed or removed → BREAKING
   - Field type changed (e.g. string → number) → BREAKING
   - New required field added to a request → BREAKING
   - Status code changed for the same situation (e.g. 200 → 204) → BREAKING
   - Auth scheme changed → BREAKING
   - New optional field, new endpoint, or a field marked deprecated but still present → NON-BREAKING / DEPRECATED

**3. Audit the versioning strategy.** Detect which mechanism is in use — URL versioning (`/api/v1/`), header versioning, media-type versioning, or query-param versioning — and flag it explicitly if none is in use at all. URL versioning is generally the easiest for API consumers to discover and reason about, but the specific choice matters far less than having *a* consistent, discoverable one.

**4. Score a weighted scorecard.** Produce a 0–100 score across five weighted axes: Consistency (30%, naming and structural patterns), Documentation (20%, completeness and clarity), Security (20%, auth/authz, security headers, input validation), Usability (15%, discoverability and developer experience), Performance (15%, caching, pagination, and other efficiency patterns). The weighting matters more than the exact number — it forces "we have great docs but inconsistent auth" to actually move the score down, instead of averaging out.

**5. Report as advisory, not authoritative.** This is design-time static analysis only — it says nothing about runtime correctness, which still needs integration tests. Output findings by severity (critical / major / minor) with a suggested fix per finding, plus the breaking-change list with migration notes for anyone bumping a version.

## When to use

- Reviewing a new or changed REST API before it ships.
- After any PR that adds or modifies endpoints.
- Planning a v2 migration and needing an explicit breaking-change list with migration notes.

Not for GraphQL or gRPC APIs (different conventions entirely) and not a substitute for integration tests — this checks the design, not the runtime behavior.

## How to use

**Install:** copy this folder into `~/.claude/skills/api-design-reviewer/` for personal use, or `.claude/skills/api-design-reviewer/` inside a project repo.

**Invoke:**

```
Run api-design-reviewer against this OpenAPI spec and give me the
scorecard plus the top critical findings.
```

```
Diff these two spec versions with api-design-reviewer and list every
breaking change with its migration note before we bump to v2.
```
