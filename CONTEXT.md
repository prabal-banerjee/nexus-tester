# Context Handoff

## Repo

- GitHub: `https://github.com/prabal-banerjee/nexus-tester`
- Default branch: `main`
- Purpose: portable FastBridge / Nexus live test harness plus shareable static QA report bundles

## Current Main Script

- File: `ui_fastbridge_connect_test.py`
- Runs a live Playwright-based browser flow against `https://fastbridge.availproject.org/`
- Injects a wallet provider into the page
- Derives the wallet address from the provided private key at runtime
- Supports:
  - `personal_sign`
  - `eth_signTypedData_v4`
  - read RPC passthrough
  - route switching across supported chains
- Produces a report bundle under `fastbridge-report-artifacts/fastbridge-report-<RUN_ID>/`

## Current Report Bundle Output

Each run writes:

- `index.html`
- `expectations.html`
- `report.json`
- `report.md`
- `assets/`

Important implementation detail:

- `index.html` embeds screenshots directly as data URLs, so local browser image loading does not depend on relative file paths anymore.

## Current Helper Scripts

- `check_fastbridge_balances.py`
  - requires `FASTBRIDGE_TEST_ADDRESS`
- `check_fastbridge_tokens.py`
  - requires `FASTBRIDGE_TEST_ADDRESS`

## Key Reporting Decisions

### Expectations

- Expectation IDs are stable identifiers, not sequential numbering.
- Prefix meaning:
  - `EXP-Txx` = timing
  - `EXP-Dxx` = data correctness
  - `EXP-Uxx` = user experience
- The report should show the broader expectation catalog, even if some expectations are `NA`.

### `EXP-U03`

- `EXP-U03 Error messages are user-readable` should only evaluate user-facing journey failures.
- Background console / telemetry / network errors are valid issues, but they should not automatically fail `EXP-U03`.

### Static HTML

- HTML reports are preferred over plain Markdown because:
  - embedded screenshots
  - fullscreen image viewing
  - better visual structure
  - easier zip-and-share workflow

## Known Product Findings So Far

Observed repeatedly across live runs:

- Successful bridges can complete without any direct wallet `eth_sendTransaction`.
- Successful flows rely on a gasless permit-plus-relayer style path:
  - `personal_sign`
  - `eth_signTypedData_v4`
- Background production noise still appears:
  - recurring `400` console error
  - `401` from `https://otel.avail.so/v1/logs`
- These should remain separate from user-facing error quality.

## Known Harness / Reporting Fixes Already Made

- Removed machine-specific repo root dependency:
  - script uses `Path(__file__).resolve().parent`
- Removed hardcoded wallet dependency from the main runner:
  - wallet address comes from private key
- Fixed balance breakdown parsing:
  - blank lines between chain and balance no longer cause false failures
- Fixed HTML image loading:
  - screenshots embedded as data URLs
- Added expectation catalog page:
  - `expectations.html`
- Added portable export behavior:
  - report JSON / Markdown use bundle-relative paths where possible

## Current Sample Report Bundle

- Example bundle in repo:
  - `fastbridge-report-artifacts/fastbridge-report-20260419T202339Z/`
- This bundle was updated in place several times to fix:
  - breakdown parsing
  - image loading
  - expectation scoring

## Things Still Worth Improving

### 1. Recompute older bundles cleanly

Some older bundles were patched in place after generation.
It would be cleaner to add a small utility that:

- loads an old `report.json`
- reapplies the latest rendering / expectation logic
- rewrites `index.html`, `expectations.html`, and `report.md`

### 2. Broader expectation coverage

The current catalog now includes:

- `EXP-T01`
- `EXP-T02`
- `EXP-T03`
- `EXP-T04`
- `EXP-D01`
- `EXP-D02`
- `EXP-D03`
- `EXP-U01`
- `EXP-U02`
- `EXP-U03`

Potential next step:

- expand into a larger checklist / scenario library
- map expectations more explicitly per scenario

### 3. Multi-run dashboard

Right now each run creates one bundle.
Potential next step:

- aggregate multiple run bundles into one summary dashboard
- compare repeated route performance and issues over time

### 4. GitHub automation

Possible next improvement:

- add GitHub Actions workflow to run report generation on demand
- publish the generated HTML bundle as an artifact

## How To Continue Next Time

Recommended first steps:

1. Open `README.md`
2. Open `ui_fastbridge_connect_test.py`
3. Inspect the latest sample bundle under `fastbridge-report-artifacts/`
4. If needed, add a re-render utility for older `report.json` files
5. Then continue with either:
   - more route coverage
   - report UX improvements
   - GitHub Actions automation

## Safe Assumptions

- The repo is already public and pushed.
- A sample report bundle is intentionally committed.
- Private keys should never be committed.
- Wallet addresses may appear in sample reports because they are part of the observed run output.
