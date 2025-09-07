# src/templates/onboarding_roles.py
from __future__ import annotations
from typing import Dict, List

ROLES = ["SOLID", "SSOT", "DRY", "KISS", "TDD"]

ROLE_TITLE = {
    "SOLID": "SOLID Sentinel",
    "SSOT": "SSOT Warden",
    "DRY": "DRY Hunter",
    "KISS": "KISS Guard",
    "TDD": "TDD Architect",
}

CHECKLIST: Dict[str, List[str]] = {
    "SOLID": [
        "SRP: No class/module with >1 reason to change",
        "OCP: No core class edited for new behavior (prefer extension)",
        "LSP: Subtypes honor base contracts (no widened preconditions)",
        "ISP: No 'god' interfaces; split where appropriate",
        "DIP: High-level depends on abstractions, not concretions",
    ],
    "SSOT": [
        "Identify SSOT files (e.g., README, CONFIG/*, SCHEMAS/*)",
        "Replace duplicated truth with references/links",
        "Introduce authoritative loaders (config/env/jsonschema)",
        "Add CI guard rejecting divergence from SSOT",
    ],
    "DRY": [
        "Detect duplicate logic (AST/hash/similarity) and consolidate",
        "Extract shared utilities; remove copy-paste variants",
        "Add tests covering consolidated paths",
    ],
    "KISS": [
        "Reduce function complexity (cyclomatic < 10 default)",
        "Cap file size (<=300 LOC rule) and split when needed",
        "Remove cleverness; prefer clear, linear flows",
        "Document one-liners when non-obvious",
    ],
    "TDD": [
        "Write failing unit test for each change (red)",
        "Implement minimal code to pass (green)",
        "Refactor with tests green (refactor)",
        "Ensure coverage threshold met (e.g., 80%+ key modules)",
    ],
}


def build_role_message(agent_id: str, role: str) -> str:
    title = ROLE_TITLE[role]
    checks = "\n".join(f"- [ ] {item}" for item in CHECKLIST[role])
    return (
        f"YOU ARE {agent_id} - {title}\n\n"
        f"🎯 ROLE: {role}\n"
        f"📋 PRIMARY RESPONSIBILITIES:\n"
        f"1) Enforce **{role}** across assigned scope\n"
        f"2) --get-next-task  3) Update status.json  4) Check inbox  5) Respond to agents\n"
        f"6) Maintain continuous workflow  7) Report with --captain  8) Use enhanced help\n\n"
        f"Checklist:\n{checks}\n\n"
        "Acceptance:\n"
        "- Submit a summary to captain with files touched & decisions.\n"
        "- Add/verify tests for affected modules (where applicable).\n"
        "- Report READY with timestamp.\n"
    )
