#!/usr/bin/env python3
"""Constants Consolidation System - Agent-8 Autonomous Cleanup.

Automated system to consolidate scattered constants.py files into the unified
constants system. Part of Agent-8's autonomous cleanup mission to achieve
maximum efficiency.
"""

from .definitions import ConstantDefinition
from .consolidator import ConstantsConsolidator

__all__ = ["ConstantDefinition", "ConstantsConsolidator", "main"]


def main() -> dict:
    """Run the constants consolidation process and return the results."""
    consolidator = ConstantsConsolidator()
    results = consolidator.consolidate_constants()
    consolidator.create_migration_guide(results)
    return results
