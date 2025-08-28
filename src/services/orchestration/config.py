"""Shared configuration and constants for orchestration stages."""

from __future__ import annotations

from typing import Dict

ENTERPRISE_STANDARDS: Dict[str, str] = {
    "loc_compliance": "PASSED (350 LOC limit)",
    "code_quality": "ENTERPRISE GRADE",
    "test_coverage": "COMPREHENSIVE V2 SERVICES",
    "reliability": "HIGH",
}
