# ledger-verify

A small, runnable public verification utility from Quantum Excellium.

It demonstrates a general principle used throughout governed systems: **an append-only record should make later alteration detectable**.

This repository is deliberately non-enabling. It does **not** publish proprietary QEC, BTT, patent, orchestration or cryptographic implementation details.

## Quick start

```powershell
python .\ledger_verify.py .\examples\intact.jsonl
python .\ledger_verify.py .\examples\tampered.jsonl
```

Expected output:

```text
VALID
INVALID
```

## Test

```powershell
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

## Scope

This demonstrator uses a simple SHA-256 hash chain. It is an educational/public verifier, not a legal timestamping service and not a substitute for a security audit.

Website: https://quantumexcellium.com
