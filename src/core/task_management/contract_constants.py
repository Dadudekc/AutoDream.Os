"""Shared constants and requirement templates for contract management."""

from __future__ import annotations

from typing import Any, Dict, List

REQUIREMENTS_HEADER = "## 📋 **DELIVERABLES REQUIRED**"

DEFAULT_REQUIREMENT_TEMPLATES: List[Dict[str, Any]] = [
    {
        "requirement_id": "task_completion",
        "description": "Complete the specified task",
        "required": True,
    },
    {
        "requirement_id": "progress_documentation",
        "description": "Document current progress and completion",
        "required": True,
    },
    {
        "requirement_id": "integration_verification",
        "description": "Verify system integration",
        "required": True,
    },
]
