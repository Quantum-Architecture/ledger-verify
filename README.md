# ledger-verify

[![verify](https://github.com/Quantum-Architecture/ledger-verify/actions/workflows/verify.yml/badge.svg)](https://github.com/Quantum-Architecture/ledger-verify/actions/workflows/verify.yml)

**Independent verification for hash-chained AI-agent audit ledgers.**

This repository answers one public question:

> Has this JSONL audit ledger been altered after it was written?

It does **not** prove who produced an event, when it happened, or that the underlying action was correct.

## Published format

Each line is one UTF-8 JSON object.

- `prev_hash` — previous record hash.
- `hash` — SHA-256 of the current canonical record.
- Genesis `prev_hash` — exactly 64 zeroes.
- Canonical JSON — keys sorted, separators `(",", ":")`, UTF-8 bytes.
- `hash` itself is excluded from the hash calculation.

## Expected behaviour

```bash
python ledger_verify.py examples/intact.jsonl
# VALID ; exit 0

python ledger_verify.py examples/tampered.jsonl
# INVALID ; exit 1
```

## What this proves

A `VALID` result means the chain is internally consistent under the published format.

## What it does not prove

- signer identity;
- trusted time;
- external anchoring;
- policy correctness;
- physical execution of the logged action;
- SOC 2 / ISO 27001 / regulatory certification.

## Related public proof

Governed-agent demo:
https://github.com/Quantum-Architecture/qec-governed-agent-demo

Proof page:
https://quantumexcellium.com/en/proof.html

## Security

See `SECURITY.md`.

## License

Apache-2.0.


## Format and tests
Format specification: [FORMAT.md](FORMAT.md) · `python -m unittest -v test_ledger_verify` · CI regenerates the examples and requires `intact` to pass and `tampered` to fail.
