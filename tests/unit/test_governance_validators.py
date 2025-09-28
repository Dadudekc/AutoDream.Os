#!/usr/bin/env python3
from pathlib import Path

from src.governance.validators.roles_modes import (
    validate_projection,
    validate_no_running_work,
    validate_switch_request,
    ValidationReport,
)


def test_validate_projection_ok():
    canonical = {"1": [0, 0], "2": [1, 1], "3": [2, 2], "4": [3, 3]}
    active = {"mode": 4, "include": [1, 2, 3, 4], "mapping": {"1": 1, "2": 2, "3": 3, "4": 4}}
    rep = validate_projection(canonical, active)
    assert rep.ok
    assert rep.errors == []


def test_validate_projection_size_mismatch():
    canonical = {"1": [0, 0], "2": [1, 1]}
    active = {"mode": 4, "include": [1, 2], "mapping": {"1": 1, "2": 2}}
    rep = validate_projection(canonical, active)
    assert not rep.ok
    assert any("projection_size_mismatch" in e for e in rep.errors)


def test_validate_no_running_work_blocked():
    rep = validate_no_running_work({"running_agents": [1], "blockers": []})
    assert not rep.ok
    assert "running_work_detected" in rep.errors


def test_validate_switch_request_requires_signature(tmp_path: Path):
    req = {"owner": "captain", "target_mode": "A4", "signature_path": str(tmp_path / "missing.pem")}
    rep = validate_switch_request(req, state={"running_agents": [], "blockers": []})
    assert not rep.ok
    assert "missing_signed_intent" in rep.errors

