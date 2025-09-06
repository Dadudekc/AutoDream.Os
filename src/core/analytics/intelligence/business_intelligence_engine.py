#!/usr/bin/env python3
"""
Business Intelligence Engine - KISS Compliant
=============================================

Backward compatibility wrapper for business intelligence engine.

Author: Agent-2 (Architecture & Design Specialist) - V2 Refactoring
License: MIT
"""

# Import all components from core and operations modules
from .business_intelligence_engine_core import BusinessIntelligenceEngineCore
from .business_intelligence_engine_operations import (
    BusinessIntelligenceEngineOperations,
)


# Create unified class
class BusinessIntelligenceEngine(
    BusinessIntelligenceEngineCore, BusinessIntelligenceEngineOperations
):
    """Unified business intelligence engine with core and operations functionality."""

    def __init__(self, config=None):
        """Initialize unified business intelligence engine."""
        BusinessIntelligenceEngineCore.__init__(self, config)
        BusinessIntelligenceEngineOperations.__init__(self, config)


# Re-export all components for backward compatibility
__all__ = ["BusinessIntelligenceEngine"]
