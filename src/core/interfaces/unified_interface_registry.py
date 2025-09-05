#!/usr/bin/env python3
"""
Unified Interface Registry - V2 Compliant Redirect
=================================================

V2 compliance redirect to modular interface registry system.
Original monolithic implementation refactored into focused modules.

Author: Agent-3 - Infrastructure & DevOps Specialist (V2 Refactoring)
Created: 2025-01-28
Purpose: V2 compliant modular interface registry
"""

# V2 COMPLIANCE REDIRECT - Import from modular system
from .unified_interface import (
    UnifiedInterfaceRegistryOrchestrator,
    InterfaceModels,
    InterfaceRegistry,
    InterfaceValidator
)

# Re-export for backward compatibility
__all__ = [
    'UnifiedInterfaceRegistryOrchestrator',
    'InterfaceModels',
    'InterfaceRegistry',
    'InterfaceValidator'
]