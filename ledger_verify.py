#!/usr/bin/env python3
"""Verify a UTF-8 JSONL hash chain using the public Quantum Excellium ledger format."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

GENESIS = "0" * 64
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def canonical(record: dict) -> bytes:
    payload = {k: v for k, v in record.items() if k != "hash"}
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def verify(path: Path) -> list[str]:
    errors: list[str] = []
    previous = GENESIS
    record_no = 0

    try:
        fh = path.open("r", encoding="utf-8")
    except OSError as exc:
        return [f"cannot read file: {exc}"]

    with fh:
        for physical_line, raw in enumerate(fh, 1):
            if not raw.strip():
                continue
            record_no += 1
            try:
                rec = json.loads(raw)
            except json.JSONDecodeError as exc:
                errors.append(f"line {physical_line}: invalid JSON ({exc.msg})")
                continue

            if not isinstance(rec, dict):
                errors.append(f"line {physical_line}: record is not a JSON object")
                continue

            prev_hash = rec.get("prev_hash")
            stored_hash = rec.get("hash")

            if not isinstance(prev_hash, str) or not HEX64.fullmatch(prev_hash):
                errors.append(f"line {physical_line}: invalid prev_hash")
            elif prev_hash != previous:
                errors.append(f"line {physical_line}: prev_hash mismatch")

            if not isinstance(stored_hash, str) or not HEX64.fullmatch(stored_hash):
                errors.append(f"line {physical_line}: invalid hash")
            else:
                computed = hashlib.sha256(canonical(rec)).hexdigest()
                if stored_hash != computed:
                    errors.append(f"line {physical_line}: hash mismatch")

            # Chain continuation uses the stored hash, which makes downstream link
            # errors visible even when the current record itself is tampered.
            if isinstance(stored_hash, str) and HEX64.fullmatch(stored_hash):
                previous = stored_hash

    if record_no == 0:
        errors.append("empty ledger")
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: ledger_verify.py FILE.jsonl")
        return 2
    errors = verify(Path(argv[1]))
    if errors:
        print("INVALID")
        for err in errors:
            print(err)
        return 1
    print("VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
