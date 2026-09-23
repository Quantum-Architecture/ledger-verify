#!/usr/bin/env python3
import hashlib, json
from pathlib import Path

GENESIS = "0" * 64

def canon(r):
    payload = {k:r[k] for k in sorted(r) if k != "hash"}
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()

def seal(r):
    r["hash"] = hashlib.sha256(canon(r)).hexdigest()
    return r

Path("examples").mkdir(exist_ok=True)
prev = GENESIS
rows = []
for seq, event in [(1,"created"),(2,"evaluated"),(3,"closed")]:
    r = {"seq":seq,"event":event,"prev_hash":prev}
    seal(r)
    rows.append(r)
    prev = r["hash"]

Path("examples/intact.jsonl").write_text(
    "\n".join(json.dumps(x, sort_keys=True) for x in rows) + "\n", encoding="utf-8"
)
tampered = [dict(x) for x in rows]
tampered[1]["event"] = "altered"
Path("examples/tampered.jsonl").write_text(
    "\n".join(json.dumps(x, sort_keys=True) for x in tampered) + "\n", encoding="utf-8"
)
print("samples written")
