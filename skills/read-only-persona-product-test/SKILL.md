---
name: read-only-persona-product-test
description: Walk live web products read-only as a first-time visitor, buyer, returning user and developer, count clicks to first value, and produce a per-product scorecard with ranked fixes.
---

# Read-only persona product test

Uptime checks say a page loads. They do not say a stranger can find the product, see its price, try it, come back to it or integrate it. This skill walks those journeys on production without changing anything.

Test only products you own or are authorised to test.

## Safety rules (set these before the first request)

- Read-only toward production. Crawl with GET requests only.
- In the browser, abort every request that is not GET, HEAD or OPTIONS, and log what was aborted. A demo that needs a write is **not verified**, never "broken".
- Some GET links change state (sign out, unsubscribe, confirm, delete). Skip them by pattern and do not follow links from emails.
- No sign-ups, sign-ins, purchases, checkouts or form submissions. Never type real personal data.
- API or tool endpoints: only discovery calls, documented free calls with synthetic input, and one unauthenticated call to a protected operation to confirm it refuses. Never use a real token.
- Fixes go into draft pull requests. No merges or deploys.

A Playwright guard that covers pop-ups as well:

```js
const context = await browser.newContext({ serviceWorkers: 'block' });
await context.route('**/*', (route) => {
  const req = route.request();
  if (['GET', 'HEAD', 'OPTIONS'].includes(req.method())) return route.continue();
  console.log('aborted', req.method(), req.url().split('?')[0]);
  return route.abort();
});
```

This guard does not stop WebSocket messages, so do not interact with features that write over a socket.

## Steps

1. **Inventory.** Build the product list from the sitemap or catalogue, the repositories and any health endpoint. For each product record name, kind, detail page, gated app path, any API endpoint, a synthetic sample input and the expected result.
2. **Crawl from the homepage** breadth first. Depth equals clicks from home. Record broken internal links and slow pages against a stated budget.
3. **Walk each persona** for each product:

| Persona | Checks |
|---|---|
| Visitor | page loads; reachable within two clicks; no sign-in wall; a sample or demo before sign-up; title names the product; meta description and image alt text present; no console or 4xx errors; no horizontal scroll at a 390 px width |
| Buyer | price visible on the detail page; a clear buy, sign-in or connect action; pricing reachable in one click |
| Returning user | a signed-out deep link redirects to login and preserves the destination; the login heading and tab title name the product |
| Developer | integration docs reachable; a copy-paste install or call example; auth discovery metadata resolves; protected calls refuse without a token; a free call returns an accurate, cleanly formatted result |

Mark each check `pass`, `fail`, `not applicable` or `not verified`.

4. **Cross-check claims against live facts.** Compare counts and promises in the marketing copy with what the system reports (a page claiming five integrations while the live list shows eight, or a "try the sample" link with no sample).
5. **Score.** Weighted pass rate overall and per persona. Exclude "not applicable". Report "not verified" separately so it cannot inflate or hide the score.
6. **Rank fixes** by (check weight × products affected) ÷ effort.
7. **Save** the raw results and a scorecard for the run, and diff against the previous run.

## Probe artefacts that look like bugs

- Failed-request console errors caused by your own aborted writes. Filter them out.
- Intermittent hydration or timing errors. Reproduce across two runs before filing.
- Catalogue cards that link to a sign-in wall while a richer public page exists. Check both and report the link.

## Output

Per product: persona scores, clicks to first value, failed checks with evidence (URL, status, screenshot or excerpt), and the not-verified list. Then one ranked fix list across all products.

## When to use

- "Test every product end to end" or "use it like different kinds of users".
- Pre-launch usability passes.
- Reducing the number of clicks to first value.
- A deeper recurring check than uptime monitoring.

## How to use

1. Copy the `read-only-persona-product-test` folder into `~/.claude/skills/` for personal use, or `.claude/skills/` inside a project.
2. Ask Claude Code to use the skill by name.
3. Example prompts:
   - "Use the read-only-persona-product-test skill on https://<site> and give me a scorecard per product with the top five fixes."
   - "Use read-only-persona-product-test to count how many clicks a first-time visitor needs to see a price and try a sample."
