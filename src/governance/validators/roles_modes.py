#!/usr/bin/env python3
"""
Governance Validators - Roles & Modes
====================================

Runtime invariants for mode switching and role projections.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class ValidationReport:
    ok: bool
    errors: List[str]
    warnings: List[str]

    def to_dict(self) -> Dict:
        return asdict(self)


def _normalize_mode_value(mode_value: object) -> Optional[int]:
    if isinstance(mode_value, int):
        return mode_value if mode_value in {2, 4, 5, 6, 8} else None
    if isinstance(mode_value, str) and len(mode_value) >= 2 and mode_value.upper().startswith("A"):
        try:
            num = int(mode_value[1:])
            return num if num in {2, 4, 5, 6, 8} else None
        except ValueError:
            return None
    return None


def validate_projection(canonical: Dict, active: Dict) -> ValidationReport:
    errors: List[str] = []
    warnings: List[str] = []

    # Active must define include and mapping
    include = active.get("include", [])
    mapping = active.get("mapping", {})

    # Count invariant
    mode_sz = _normalize_mode_value(active.get("mode")) or len(include)
    if len(include) != mode_sz:
        errors.append(f"projection_size_mismatch: include={len(include)} expected={mode_sz}")

    # Coordinates exist for each canonical agent used
    canonical_keys = {str(k) for k in canonical.keys()}
    for src in mapping.keys():
        if str(int(src)) not in canonical_keys:
            errors.append(f"missing_canonical_coordinates_for_agent_{src}")

    # Ensure unique role per agent in active assignments (if provided)
    assignments = active.get("assignments", {})
    if assignments:
        seen_roles: Dict[str, str] = {}
        for agent_idx_str, role_name in assignments.items():
            if not role_name or role_name == "unassigned":
                continue
            if role_name in seen_roles:
                errors.append(f"role_uniqueness_conflict:{role_name} on Agent-{seen_roles[role_name]} and Agent-{agent_idx_str}")
            else:
                seen_roles[role_name] = agent_idx_str

    return ValidationReport(ok=len(errors) == 0, errors=errors, warnings=warnings)


def validate_no_running_work(state: Dict) -> ValidationReport:
    errors: List[str] = []
    warnings: List[str] = []
    running = state.get("running_agents", [])
    blockers = state.get("blockers", [])
    if running:
        errors.append("running_work_detected")
    if blockers:
        errors.append("open_blockers_present")
    return ValidationReport(ok=len(errors) == 0, errors=errors, warnings=warnings)


def validate_switch_request(request: Dict, state: Dict) -> ValidationReport:
    errors: List[str] = []
    warnings: List[str] = []

    # Captain-only
    owner = (request.get("owner") or "").lower()
    if owner not in {"captain", "co_captain"}:  # allow co_captain per policy
        errors.append("owner_not_authorized")

    # Mode value
    if _normalize_mode_value(request.get("target_mode")) is None:
        errors.append("invalid_target_mode")

    # Signed intent (presence check)
    sign_path = request.get("signature_path")
    if not sign_path or not Path(sign_path).exists():
        errors.append("missing_signed_intent")

    # No running work
    nrw = validate_no_running_work(state)
    if not nrw.ok:
        errors.extend(nrw.errors)

    return ValidationReport(ok=len(errors) == 0, errors=errors, warnings=warnings)


def emit_report(report: ValidationReport, base: Path, filename: str = "validation_report.json") -> Path:
    out_dir = base / "runtime" / "governance"
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = report.to_dict()
    payload["timestamp"] = time.time()
    out_path = out_dir / filename
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return out_path

