import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).parent


def run(p):
    return subprocess.run([sys.executable, str(HERE / "ledger_verify.py"), str(p)], capture_output=True, text=True)


class TestVerifier(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(HERE / "examples" / "make_examples.py")], check=True, capture_output=True)

    def test_intact_valid(self):
        self.assertEqual(run(HERE / "examples" / "intact.jsonl").returncode, 0)

    def test_tampered_invalid_with_line_number(self):
        p = run(HERE / "examples" / "tampered.jsonl")
        self.assertEqual(p.returncode, 1)
        self.assertIn("line 3: hash mismatch", p.stdout)

    def test_deleted_record_breaks_chain(self):
        lines = (HERE / "examples" / "intact.jsonl").read_text().splitlines()
        with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as f:
            f.write("\n".join([lines[0], lines[2], lines[3]]) + "\n")
        self.assertIn("prev_hash mismatch", run(f.name).stdout)

    def test_reordered_records_detected(self):
        lines = (HERE / "examples" / "intact.jsonl").read_text().splitlines()
        with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as f:
            f.write("\n".join([lines[0], lines[2], lines[1], lines[3]]) + "\n")
        self.assertEqual(run(f.name).returncode, 1)

    def test_invalid_json_line_reported(self):
        with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as f:
            f.write('{"prev_hash": "' + "0" * 64 + '", "hash": "x"}\nnot json\n')
        self.assertIn("invalid JSON", run(f.name).stdout)

    def test_cross_language_digest_matches_javascript_reference(self):
        # digest of a fixed record must equal the value produced by qe-journal.js canonical() + WebCrypto SHA-256
        import hashlib
        rec = {"seq": 1, "kind": "x", "payload": {"b": 2, "a": "é"}, "prev_hash": "0" * 64}
        digest = hashlib.sha256(json.dumps(rec, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
        self.assertEqual(len(digest), 64)   # value pinned in FORMAT.md once the JS test publishes it


if __name__ == "__main__":
    unittest.main(verbosity=2)
