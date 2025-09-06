# tests/test_proof_ledger.py
import os, json
from src.quality.proof_ledger import run_tdd_proof

def test_proof_file_written(tmp_path, monkeypatch):
    # run in temp dir to avoid touching real repo
    cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        path = run_tdd_proof(mode="quality-suite", role_map={"Agent-1":"SOLID"})
        assert os.path.exists(path)
        data = json.load(open(path, "r", encoding="utf-8"))
        assert data["schema"] == "tdd_proof/v1"
        assert "mode" in data and "roles" in data
        assert "duration_sec" in data
    finally:
        os.chdir(cwd)
