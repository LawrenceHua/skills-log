---
name: text-to-image-bakeoff
description: Wraps OpenAI gpt-image-1, Fal's Flux Pro, and Google Imagen text-to-image APIs behind one small script with a bake-off comparison mode, backend health tracking, and a reusable prompt template for a consistent web-ready visual system.
---

# text-to-image-bakeoff

When a task needs an AI-generated image and there's no image-generation MCP or tool wired in, the fastest path is a small standalone script that calls 2-3 providers' text-to-image APIs directly — no heavy SDK, just env-var keys and HTTP. Running the same prompt through every configured backend before picking one ("bake-off" mode) beats guessing which provider's style fits, and tracking backend health up front saves burning a call on a provider that's out of credit or misconfigured.

## Method

1. **One script, three backends.** Use any language with a built-in HTTP client (Python's `urllib`/`requests`, Node's `fetch`) — no provider SDK dependency. Read keys from environment variables only, never hardcoded: `OPENAI_API_KEY`, `FAL_KEY`, `GEMINI_API_KEY`.
2. **Bake-off mode.** Run one prompt through every backend that has a key set, write one image per backend into an output directory (`bakeoff/openai.png`, `bakeoff/fal.png`, `bakeoff/imagen.png`), and skip backends with no key instead of failing the whole run.
3. **One mode.** Generate a single image given an explicit backend, prompt, output path, and resolution — this is what you use once bake-off has told you which backend to default to.
4. **Health tracking.** Keep a small status file (e.g. `status.json`) recording which backend last succeeded vs failed, and why (bad key, out of credit, model retired). Before trusting a new backend or model id, make a lightweight "list models" call first rather than discovering it's dead on a real generation call.
5. **Prompt template + post-process for brand consistency.** For a set of images that need to feel like one visual system (e.g. backdrops sitting behind UI text), keep a short reusable prompt template capturing tone/color direction, composition rules (abstract/gradient, generous negative space, explicitly no text/logos/UI/faces), and run every output through a resize + compress step (e.g. a system image tool) so nothing needs manual web-readying afterward.

```bash
export OPENAI_API_KEY=sk-...
export FAL_KEY=...
export GEMINI_API_KEY=...

# compare all configured backends on one prompt
python3 image_gen.py bakeoff \
  --prompt "abstract teal-to-charcoal gradient, generous negative space, no text, no logos, no faces" \
  --out ./bakeoff/

# check which backends are healthy before spending a call
python3 image_gen.py status

# generate with the backend you picked
python3 image_gen.py one \
  --backend openai --model gpt-image-1 \
  --prompt "..." --size 1536x1024 --out ./assets/hero.png
```

## When to use

- A task needs hero art, a concept backdrop, or an illustration and no image-generation MCP/tool is available in the session.
- You're not sure which provider's style fits the task and want a side-by-side comparison before committing.
- You're generating a set of assets (multiple backdrops, a slide deck's images) that need to look like one consistent system rather than one-offs.
- A previously-working image backend starts failing and you need to know whether it's the key, the model id, or the account before retrying.

## How to use

**Install:** copy this folder into `~/.claude/skills/text-to-image-bakeoff/` for personal use, or `.claude/skills/text-to-image-bakeoff/` inside a project repo.

**Invoke:**
```
Generate 3 hero backdrop concepts for the landing page and bake-off compare them across providers
```
```
Check which image backend is currently healthy, then generate a single 1536x1024 hero image with it
```
