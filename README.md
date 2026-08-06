# Draven Biotech Event Engine

A reproducible, evidence-first system for underwriting binary and path-dependent biotechnology equity events.

The repository converts a catalyst dossier into a publication-ready investment-committee report using deterministic calculations, typed evidence records, explicit assumptions, falsifiers, and instrument-selection gates. The first reference case is Zymeworks (`ZYME`) ahead of the August 25, 2026 Ziihera PDUFA and the subsequent HERIZON-GEA-01 doublet overall-survival analysis.

## Why this is stronger than a conventional narrative report

Every material conclusion must be traceable to one of four objects:

1. **Evidence**: an atomic, dated claim with a source tier and confidence.
2. **Assumption**: an explicit model input that is not directly observed.
3. **Calculation**: deterministic output generated from disclosed inputs.
4. **Judgment**: an investment conclusion that identifies its supporting evidence and falsifiers.

The engine rejects reports that contain unsupported probabilities, terminal values that do not reconcile, stale catalyst dates, inconsistent share counts, or option structures that fail liquidity and breakeven gates.

## Workflow

```text
source intake
  -> evidence ledger
  -> clinical/statistical agent
  -> regulatory/CMC agent
  -> commercial/competitive agent
  -> capital structure and valuation engine
  -> ownership/positioning agent
  -> options/instrument gate
  -> red-team and falsifier pass
  -> investment committee report
  -> post-event scorecard
```

## Repository structure

```text
cases/                  structured event dossiers
schemas/                JSON Schema contracts
prompts/                agent handoff and rejection rules
src/draven_engine.py    deterministic validation and valuation logic
tests/                  reproducibility and integrity tests
main.py                 Streamlit review interface
```

## Run locally

```bash
python -m pip install -r requirements.txt
pytest -q
streamlit run main.py
```

## Core quality gates

A case cannot be marked publication-ready unless:

- the official catalyst date is sourced and freshness-checked;
- each clinical endpoint includes population, arm, estimand, denominator, effect estimate, interval, and analysis timing when available;
- regulatory probability is decomposed into efficacy, safety, CMC, inspection, and label-shape components;
- scenario probabilities sum to 1.00;
- terminal values reconcile to a disclosed valuation bridge;
- probability-weighted value and expected return are calculated, not hand-entered;
- option trades pass expiry, spread-width, liquidity, breakeven, and event-coverage tests;
- every load-bearing claim has at least one falsifier;
- the report preserves known conflicts rather than silently resolving them;
- the evidence cutoff and version hash are displayed.

## ZYME reference thesis

The reference dossier frames ZYME as a two-stage event rather than a single PDUFA binary:

- high-probability FDA conversion and a $250 million milestone;
- lower-probability but higher-information-value doublet OS readout;
- common equity preferred because listed expiries do not isolate the PDUFA and quoted options fail liquidity and price gates.

The case file is an analytical example, not investment advice. Inputs must be refreshed before publication or trading.

## Security

Never commit API keys or credentials. Use environment variables or repository secrets. A previously committed key was removed from the current tree, but any exposed credential must also be revoked and rotated because Git history can retain it.
