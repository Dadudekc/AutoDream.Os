#!/usr/bin/env python3
"""
SSOT Package - V2 Compliant
===========================

Single Source of Truth system with modular architecture.

Author: Agent-4 - Strategic Oversight & Emergency Intervention Manager
Created: 2025-01-27
Purpose: V2 compliant SSOT package
"""

from .ssot_orchestrator import (
    UnifiedSSOTOrchestrator,
    get_unified_ssot_orchestrator
)
from .ssot_models import (
    SSOTComponent,
    SSOTExecutionTask,
    SSOTIntegrationResult,
    SSOTValidationReport,
    SSOTComponentType,
    SSOTExecutionPhase,
    SSOTValidationLevel,
    SSOTMetrics
)

# Export main interfaces
__all__ = [
    'UnifiedSSOTOrchestrator',
    'get_unified_ssot_orchestrator',
    'SSOTComponent',
    'SSOTExecutionTask',
    'SSOTIntegrationResult',
    'SSOTValidationReport',
    'SSOTComponentType',
    'SSOTExecutionPhase',
    'SSOTValidationLevel',
    'SSOTMetrics'
]
