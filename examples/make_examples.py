#!/usr/bin/env python3
"""Regenerates examples/intact.jsonl and examples/tampered.jsonl deterministically (fixed timestamps)."""
import hashlib
import json
from pathlib import Path

GENESIS = "0" * 64
OUT = Path(__file__).parent


def canonical(o):
    return json.dumps(o, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def chain(events):
    prev, recs = GENESIS, []
    for i, (kind, payload) in enumerate(events, 1):
        rec = {"seq": i, "ts_utc": f"2026-09-26T00:00:{i:02d}Z", "kind": kind, "payload": payload, "prev_hash": prev}
        rec["hash"] = hashlib.sha256(canonical(rec)).hexdigest()
        recs.append(rec)
        prev = rec["hash"]
    return recs


recs = chain([("policy_loaded", {"rules": 3}), ("tool_allowed", {"tool": "lookup_vendor"}),
              ("tool_refused", {"tool": "schedule_payment", "code": "vendor_not_approved"}), ("session_end", {"refusals": 1})])
(OUT / "intact.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in recs), encoding="utf-8")
bad = json.loads(json.dumps(recs))
bad[2]["kind"] = "tool_allowed"          # a refusal rewritten as an allow, hash left unchanged
(OUT / "tampered.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in bad), encoding="utf-8")
print("examples regenerated")
