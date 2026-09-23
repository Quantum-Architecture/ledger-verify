import subprocess, sys

def run(path):
    return subprocess.run([sys.executable, "ledger_verify.py", path], capture_output=True, text=True)

def test_intact():
    r = run("examples/intact.jsonl")
    assert r.returncode == 0
    assert "VALID" in r.stdout

def test_tampered():
    r = run("examples/tampered.jsonl")
    assert r.returncode != 0
    assert "INVALID" in r.stdout
