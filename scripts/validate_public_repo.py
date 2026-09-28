#!/usr/bin/env python3
"""Public-surface self-check: required files present, README not empty, no obvious secret-like markers.
This is repository hygiene, not technical validation of the licensed runtime."""
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
required = ["README.md", "SECURITY.md", "LICENSE"]
errors = [f"missing {x}" for x in required if not (root / x).exists()]
readme = (root / "README.md").read_text(encoding="utf-8", errors="replace") if (root / "README.md").exists() else ""
if len(readme.strip()) < 500:
    errors.append("README.md is unexpectedly short")
bad_names = [".env", "id_rsa", "private_key", "client_secret"]
bad_text = ["BEGIN " + "PRIVATE KEY", "api_key" + "=", "password" + "="]      # split so this file never matches itself
for p in root.rglob("*"):
    if not p.is_file() or ".git" in p.parts or p.resolve() == SELF:
        continue
    rel = str(p.relative_to(root))
    low = rel.lower()
    for token in bad_names:
        if token in low:
            errors.append(f"suspicious filename: {rel}")
    if p.stat().st_size <= 1000000 and p.suffix.lower() in {".md", ".txt", ".json", ".yml", ".yaml", ".py", ".ps1", ".js"}:
        txt = p.read_text(encoding="utf-8", errors="ignore").lower()
        for token in bad_text:
            if token.lower() in txt:
                errors.append(f"suspicious secret-like token in: {rel}")
if errors:
    print("PUBLIC-REPO SELF-CHECK: FAIL")
    for e in errors:
        print("-", e)
    sys.exit(1)
print("PUBLIC-REPO SELF-CHECK: PASS")
print("Required public-surface files present; no obvious secret-like markers detected.")
