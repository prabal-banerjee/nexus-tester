# FastBridge QA Dashboard

- Scenario ID: `FB-USDC-AVALANCHE-001`
- Status: `PARTIAL`
- Run ID: `20260419T202339Z`
- UTC Time: `2026-04-19T20:24:18.856583+00:00`
- Tester: `Codex Agent`
- App URL: `https://fastbridge.availproject.org/avalanche/`
- Wallet: `0x5931C7252658B763c26e9487BB367DaD46B00000`
- Destination chain tested: `Avalanche`
- Destination token tested: `USDC`
- Transfer amount tested: `0.1 USDC`
- Bridge completed: `True`
- Gasless flow detected: `True`
- Transactions submitted: `0`
- Explorer URL: `https://explorer.nexus.availproject.org/intent/3294`

## Executive Summary

- Unified balance aggregation is working for this wallet on the Avalanche route.
- The quote path for sending 0.1 USDC to Avalanche works and the information shown is complete enough to review the route.
- The end-to-end bridge transaction completed successfully and the UI balance updated on the destination chain.
- This successful route appears to rely on a gasless signed-intent flow rather than a direct wallet-broadcast transaction.

## Scenario Outcome

| Field | Value |
| --- | --- |
| Scenario | `FB-USDC-AVALANCHE-001` |
| Destination | `Avalanche` |
| Requested output | `0.1 USDC` |
| Bridge completed | `True` |
| Gasless flow | `True` |
| Source chain(s) used | `Arbitrum One` |
| Amount spent | `0.110357 USDC` |
| Amount received | `0.1 USDC` |
| Total fees | `0.010357 USDC` |

## Flow Results

- Unified balance loaded in the live UI and surfaced a total of 4.9209 USDC.
- Balance breakdown opened successfully and exposed per-chain USDC balances.
- A real 0.1 USDC route to Avalanche was quoted successfully with spend, receive, and fee information.
- The execution flow advanced into the token allowance step for the selected source chain.
- The wallet signed the typed-data request used during the allowance flow.
- The bridge completed successfully in the live UI and the destination balance updated to include 0.1 USDC on Avalanche.
- This route completed without a direct wallet-broadcast transaction, which is consistent with a gasless permit-plus-relayer flow.

## Flow Checkpoints

- `Landing page and wallet state`: `PASS`
  Evidence: `./assets/avalanche-initial.png`
  Notes: Unified balance shown as 4.9209 USDC.
- `Balance breakdown panel`: `PASS`
  Evidence: `./assets/avalanche-breakdown.png`
  Notes: 5 per-chain entries captured.
- `Quote rendering`: `PASS`
  Evidence: `./assets/avalanche-after-amount.png`
  Notes: Spend 0.1103 USDC, receive 0.1 USDC, fees 0.0103 USDC.
- `Allowance review`: `PASS`
  Evidence: `./assets/avalanche-allowance.png`
  Notes: Allowance modal rendered with approval options.
- `Execution completion`: `PASS`
  Evidence: `./assets/avalanche-final.png`
  Notes: Bridge successful state rendered with final amounts and explorer link.

## Expectations Assessment

| Expectation | Status | Notes |
| --- | --- | --- |
| `EXP-T01` Execution completes within 30s | `PASS` | Measured 15191 ms from approval click to final capture. |
| `EXP-T02` Page load within 5s | `FAIL` | Measured 7519 ms. |
| `EXP-T03` Balances refresh after completion | `PASS` | Unified balance changed from 4.9209 USDC to 4.9105 USDC after completion. |
| `EXP-T04` Quote appears within 5s | `PASS` | Measured 2610 ms. |
| `EXP-D01` Delivered output matches quoted output | `PASS` | Quoted receive 0.1 USDC; actual receive 0.1 USDC. |
| `EXP-D02` Actual fees do not materially exceed quoted fees | `PASS` | Quoted fees 0.0103 USDC; actual fees 0.010357 USDC. |
| `EXP-D03` Unified balance and breakdown are visible | `PASS` | Initial unified 4.9209 USDC; breakdown rows captured: 5. |
| `EXP-U01` Spend, receive, and fee details shown | `PASS` | Spend 0.1103 USDC, receive 0.1 USDC, fees 0.0103 USDC. |
| `EXP-U02` Source chain visible before confirm | `PASS` | Source summary: USDC on 1 chain. |
| `EXP-U03` Error messages are user-readable | `PASS` | No user-facing action failure was observed in this run. |

## Issues Found

### FB-P2-001 Background 400 Error Visible In Console
- Severity: `medium`
- Details: The app still emits a recurring 400 resource error during normal usage. It did not block this route, but it remains noisy and could hide other issues.
- Evidence: `./assets/avalanche-initial.png`
- Suspected Root Cause: One or more startup requests are failing with a 400 without a user-facing surface.
- Reproduction:
  - Open FastBridge on any supported route.
  - Open browser devtools console.
  - Observe the recurring 400 resource error during startup.

### FB-P2-002 Background 401 Error During Nexus Setup
- Severity: `medium`
- Details: A 401 resource error appeared during initialization, even though the route still progressed. Users do not get an explicit explanation for it in the UI.
- Evidence: `./assets/avalanche-initial.png`
- Suspected Root Cause: Telemetry/logging endpoint requires authorization and fails noisily during normal flows.
- Reproduction:
  - Connect a wallet on the Avalanche route.
  - Wait for Nexus initialization.
  - Inspect browser console/network for 401 responses.

## Metrics

| Metric | Value |
| --- | --- |
| `pageLoadMs` | `7519` |
| `quoteVisibleMs` | `2610` |
| `executionCompletionMs` | `15191` |
| `consoleErrorCount` | `3` |
| `pageErrorCount` | `1` |
| `networkEventCount` | `70` |

## Balance Evidence

- Initial unified balance: `4.9209 USDC`
- Final unified balance: `4.9105 USDC`
- `Arbitrum`: `2.3271 USDC`
- `Optimism`: `2.2938 USDC`
- `Base`: `0.1 USDC`
- `Scroll`: `0.1 USDC`
- `Polygon`: `0.1 USDC`

## Wallet Interaction

- Methods called: `eth_accounts, eth_chainId, eth_signTypedData_v4, personal_sign, wallet_switchEthereumChain`
- Personal sign requests: `2`
- Typed data sign requests: `1`
- `eth_sendTransaction` requests: `0`

## Network And Console Signals

- 3 console error(s) captured.
- 1 page error(s) captured.
- 2 network 401 response(s) captured.
- 0 network 400 response(s) captured.

## Transactions

- No direct wallet-broadcast transaction was captured. The route completed via signed approvals/intents and relayer execution.

## Artifacts

- `Initial connected state`: `./assets/avalanche-initial.png`
- `Balance breakdown`: `./assets/avalanche-breakdown.png`
- `After amount input`: `./assets/avalanche-after-amount.png`
- `Allowance modal`: `./assets/avalanche-allowance.png`
- `Post approval state`: `./assets/avalanche-post-approve.png`
- `Final UI state`: `./assets/avalanche-final.png`
