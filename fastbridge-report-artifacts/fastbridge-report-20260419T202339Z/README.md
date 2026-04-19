# FastBridge Report Bundle

This folder contains a shareable static QA report for one FastBridge test run.

## Open The Report

- Open [index.html](./index.html) in a browser.
- Open [expectations.html](./expectations.html) for the expectation catalog.

## Re-Run The Generator

Run these commands from the repository root.

Script:

- `ui_fastbridge_connect_test.py`

Basic run:

```bash
python3 ui_fastbridge_connect_test.py
```

Run a specific destination route:

```bash
FASTBRIDGE_DEST_SLUG=avalanche python3 ui_fastbridge_connect_test.py
```

Set the amount:

```bash
FASTBRIDGE_DEST_SLUG=avalanche FASTBRIDGE_BRIDGE_AMOUNT=0.1 python3 ui_fastbridge_connect_test.py
```

Provide the private key by prompt or environment variable:

```bash
FASTBRIDGE_TEST_PRIVATE_KEY=your_key_here python3 ui_fastbridge_connect_test.py
```

## Supported Environment Variables

- `FASTBRIDGE_DEST_SLUG`
  Example: `base`, `polygon`, `scroll`, `avalanche`
- `FASTBRIDGE_BRIDGE_AMOUNT`
  Example: `0.1`
- `FASTBRIDGE_TEST_PRIVATE_KEY`
  If omitted, the script prompts for it securely.

## Output

Each run creates a new folder under:

- `fastbridge-report-artifacts/`

That folder includes:

- `index.html`
- `expectations.html`
- `report.json`
- `report.md`
- `assets/`

## Notes

- The script runs a live browser flow against `https://fastbridge.availproject.org/`.
- Successful routes may be gasless from the wallet perspective and use signatures instead of `eth_sendTransaction`.
- The generated HTML embeds screenshots directly, so the bundle can be zipped and shared as-is.
