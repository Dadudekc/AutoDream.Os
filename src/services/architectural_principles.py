"""
Architectural Principles - V2 Compliance Module
================================================

Centralized architectural principles registry.
REFACTORED: Extracted principle data to separate module for V2 compliance.

Author: Agent-2 - Architecture & Design Specialist (V2 Refactor)
License: MIT
"""

from .architectural_models import ArchitecturalGuidance, ArchitecturalPrinciple
from .architectural_principles_data import get_ocp_guidance, get_srp_guidance


class PrincipleDefinitions:
    """Centralized definitions for all architectural principles."""

    @staticmethod
    def get_all_principles() -> dict[ArchitecturalPrinciple, ArchitecturalGuidance]:
        """Get all architectural principle definitions (refactored for V2)."""
        # NOTE: Only SRP and OCP implemented in data module currently
        # TODO: Add remaining 6 principles (LSP, ISP, DIP, SSOT, DRY, KISS, TDD)
        return {
            ArchitecturalPrinciple.SINGLE_RESPONSIBILITY: get_srp_guidance(),
            ArchitecturalPrinciple.OPEN_CLOSED: get_ocp_guidance(),
        }

    @staticmethod
    def get_principle(principle: ArchitecturalPrinciple) -> ArchitecturalGuidance:
        """Get a specific architectural principle."""
        all_principles = PrincipleDefinitions.get_all_principles()
        return all_principles.get(principle)
