"""Utilities for parsing contract files."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import List

from .contract_constants import DEFAULT_REQUIREMENT_TEMPLATES, REQUIREMENTS_HEADER
from .models import ContractRequirement

logger = logging.getLogger(__name__)


def parse_contract_requirements(contract_file: Path) -> List[ContractRequirement]:
    """Extract requirement entries from a contract Markdown file.

    Args:
        contract_file: Path to the contract Markdown file.

    Returns:
        A list of :class:`ContractRequirement` instances.
    """
    requirements: List[ContractRequirement] = []
    try:
        content = contract_file.read_text(encoding="utf-8")
        lines = content.split("\n")
        in_requirements = False
        for line in lines:
            if REQUIREMENTS_HEADER in line:
                in_requirements = True
                continue
            if in_requirements and line.startswith("### **"):
                if "Task Completion" in line:
                    requirements.append(
                        ContractRequirement(**DEFAULT_REQUIREMENT_TEMPLATES[0])
                    )
                elif "Progress Documentation" in line:
                    requirements.append(
                        ContractRequirement(**DEFAULT_REQUIREMENT_TEMPLATES[1])
                    )
                elif "Integration Verification" in line:
                    requirements.append(
                        ContractRequirement(**DEFAULT_REQUIREMENT_TEMPLATES[2])
                    )
            if in_requirements and line.startswith("---"):
                break
        if not requirements:
            requirements = [
                ContractRequirement(**template)
                for template in DEFAULT_REQUIREMENT_TEMPLATES
            ]
    except Exception as exc:  # pragma: no cover - log error path
        logger.error("Error parsing contract requirements: %s", exc)
        requirements = [
            ContractRequirement(**template)
            for template in DEFAULT_REQUIREMENT_TEMPLATES
        ]
    return requirements
