# FastBridge Report Style Guide

Reference used: `MegaETH QA Testing Dashboard.pdf`

## What To Capture

- Run metadata:
  run id, timestamp, tester, destination route, token, requested amount, final status
- Executive summary:
  3-5 bullets that say what worked, what failed, whether funds moved, and whether user-visible state was correct
- Scenario outcome:
  requested amount, source chain chosen by app, amount spent, amount received, total fees, explorer link
- Flow checkpoints:
  landing state, balance breakdown, quote visibility, allowance review, execution completion
- Expectations assessment:
  page load time, quote latency, unified balance visibility, source chain visibility, fee/spend/receive visibility, error readability, end-to-end completion timing
- Issues:
  stable issue id, severity, clear description, evidence artifact, suspected root cause, exact reconstruction steps
- Balance evidence:
  initial unified balance, final unified balance, per-chain balance rows shown in UI
- Wallet interaction:
  signature methods used, whether the app requested `eth_sendTransaction`, whether the flow was gasless
- Network and console anomalies:
  background `400` / `401` failures, page errors, other non-blocking signals
- Evidence:
  screenshots for each phase and generated JSON/Markdown artifacts

## How The Current Script Mirrors The Reference

The reusable script now outputs:

- `Executive Summary`
- `Scenario Outcome`
- `Flow Results`
- `Flow Checkpoints`
- `Expectations Assessment`
- `Issues Found`
- `Metrics`
- `Balance Evidence`
- `Wallet Interaction`
- `Network And Console Signals`
- `Transactions`
- `Artifacts`

## Reporting Rules

- If something fails, always include exact reconstruction steps.
- If something succeeds through a non-obvious path, explain the execution semantics.
  Example: a gasless permit-plus-relayer flow can be a success even when the wallet never receives `eth_sendTransaction`.
- Distinguish user-visible issues from backend-only or console-only issues.
- Prefer evidence-backed statements over inference.
- If data is unavailable, say `unknown` rather than guessing.
- Keep issue ids stable so repeated failures can be tracked across runs.

## Next Upgrades Worth Adding

- Multi-scenario aggregation into one dashboard file
- Stable checklist IDs per route and token combination
- Automatic explorer scraping for final intent details
- Cross-run pattern detection
- Balance delta verification against on-chain reads after completion
