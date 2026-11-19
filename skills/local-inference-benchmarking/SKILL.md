---
name: local-inference-benchmarking
description: Tunes a local model server with measured performance ceilings, paired benchmark controls, and full-context stability checks.
---

# Local inference benchmarking

## When to use

Use this skill when an agent needs to tune a local language model server, compare serving configurations on the same hardware, or verify that a cleaned-up configuration reproduces a benchmark result.

## Method

### 1. Define the workload and record a baseline

- Pick a primary metric and write down the constraints before running the benchmark. Record the concurrency target, prompt and output lengths, required context length, memory budget, and allowed output quality changes. Set regression tolerances for the other metrics that matter.
- Record the hardware, driver, server build, model and tokenizer revisions, precision, quantization, and launch settings. Use an isolated server and synthetic or approved local prompts. Save the baseline configuration so it can be run again.
- Use the same tokenized fixtures, sampling settings, output budget, and load pattern across runs. Keep warm and cold runs separate and explicitly control prefix-cache reuse. Keep the host and performance profile stable, warm up before timed runs, and serialize benchmarks on shared hardware.
- Measure time to first token (TTFT) from request submission to the first generated token. Measure steady decode using generated tokens after the first token divided by the remaining generation time. Use server token counts or the model tokenizer. Measure aggregate throughput over the same request window at the target concurrency. If the server exposes prefill timing, report prompt tokens per prefill second at each test length and state which timings include queueing. For latency-sensitive workloads, report the median and 95th percentile for TTFT and end-to-end latency, with the sample count. Keep startup timing separate.
- Record failed requests, unexpectedly short or degenerate output, and peak memory. On a unified-memory machine, use the platform's memory accounting and check which counters overlap before combining them. Monitor the memory cap during testing. Stop admitting requests and drain the isolated server when ending a run.

### 2. Estimate the headroom

- Measure sustained device memory bandwidth and matrix throughput on the target machine using representative workloads and the relevant precision.
- For single-stream decode that is limited by memory bandwidth, estimate tokens per second as sustained bytes per second divided by estimated bytes transferred per generated token. Include active weights, the output projection if counted separately, and attention cache reads at the test context length. State cache and expert-routing assumptions. For speculative decoding, record both emitted tokens per verification step and elapsed time per step, including draft cost.
- For compute-limited prefill, divide sustained operations per second by estimated operations per prompt token. Include attention work at the tested length. Cross-check memory feasibility by estimating weights, runtime workspace, and key/value cache for the requested number of full-length sequences. Use these estimates to rank experiments and explain measured bottlenecks.

### 3. Change one setting and bracket the measurement

1. Pick a setting that addresses the measured bottleneck. Try warm compilation caches for startup, graph execution for decode overhead, draft length for speculative decoding, cache or batch sizing for concurrency, or prefill chunk size for contention between input processing and generation.
2. Run the current best configuration, the candidate, then the current best again. Collect at least six valid decode samples per configuration when decode is the target. Compare medians and record the spread. If conditions drift or the controls disagree enough to change the verdict, repeat the comparison under stable conditions.
3. Keep a change only when it beats both controls by more than ordinary variation, passes the memory and output checks, and stays within the declared regression tolerances. Repeat surprising wins. If the controls vary widely, gather more samples before choosing a winner.
4. Record each trial in a table with the baseline and candidate settings, workload, sample counts, control and candidate results, memory peak, output checks, verdict, and reason. Keep rejected changes in the log so a later run can avoid repeating them. If several plausible changes land within noise, report the plateau and the measured limit.

### 4. Qualify the winner from a clean restart

- Recreate the winning configuration with pinned model, tokenizer, server, and runtime revisions. Rerun the baseline and winner using the same fixtures and conditions. Confirm that the clean winner matches the exploratory winner within measured variation.
- Check retrieval of known strings at several positions in prompts around half the target context length and near the usable limit. Leave room for generation and verify the server received the full prompt. Sustain concurrent full-length requests at the target concurrency and confirm error rates and memory stay within budget.
- For a change intended to preserve outputs, compare greedy token sequences against the baseline on representative fixtures and investigate divergences. For an allowed precision or quality trade-off, run the agreed quality checks and report the change. Exercise tool calls if the intended workload uses them.
- Hand back the pinned configuration and a table with baseline, winner, estimated ceiling where applicable, and how each number was measured. Include discarded runs, observed regressions, and any untested workload. Restore temporary host settings and record the final server state.

## How to use

1. Copy the `local-inference-benchmarking` folder into `~/.claude/skills/` for personal use or into a project's `.claude/skills/` directory.
2. Ask Claude Code to use the skill by name in that project.

Example prompts:

- “Use local-inference-benchmarking to improve single-user decode on my local model server. Keep the memory budget and context length in my benchmark notes fixed.”
- “Use local-inference-benchmarking to compare two prefill chunk sizes at four concurrent requests. Check tail latency and full-context stability before selecting one.”
