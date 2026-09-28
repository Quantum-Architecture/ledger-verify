# Ledger format (normative for ledger_verify.py)

A ledger is a UTF-8 **JSON Lines** file: one JSON object per line, blank lines ignored.

Each record MUST contain:
- `prev_hash` — 64 lowercase hex characters. First record: `"0" * 64` (genesis). Then: the `hash` of the previous record.
- `hash` — 64 lowercase hex characters = SHA-256 of the **canonical JSON of the record without the `hash` field**.

Canonical JSON = `json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")`
where `payload` is every key of the record except `hash`, i.e. `prev_hash` **is** covered by the hash.

Any other keys are free (`seq`, `ts_utc`, `kind`, `payload`, …). Recommended: integers and strings only —
floats serialize differently across languages (`1.0` vs `1`) and break cross-implementation verification.

Verification (`ledger_verify.py file.jsonl`): for each record, `prev_hash` must equal the previous record's `hash`
(genesis for the first), and `hash` must equal the recomputed digest. Output `VALID` (exit 0) or `INVALID` with one
line per error (exit 1).

What a valid chain proves: no record was altered, inserted or removed after the chain was written, unless the whole
suffix was rewritten by someone holding the file. What it does not prove: who wrote it, when, or that the head was not
replaced — for that, anchor or sign the head (QEC Local Core does: Ed25519-signed anchors, ledger-attested state).

Reference implementations: Python (`ledger_verify.py`), JavaScript (`qe-journal.js`, browser, WebCrypto — same digests).
