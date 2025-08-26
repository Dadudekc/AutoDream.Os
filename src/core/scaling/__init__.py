#!/usr/bin/env python3
"""
Scaling Package - Agent Cellphone V2
====================================

CONSOLIDATED scaling system - replaces 4 separate scaling files with unified manager.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

CONSOLIDATION STATUS:
- ✅ ScalingManager: Unified scaling management (managers/scaling_manager.py)
- ❌ REMOVED: scaling_core.py (consolidated into ScalingManager)
- ❌ REMOVED: scaling_distribution.py (consolidated into ScalingManager)
- ❌ REMOVED: scaling_monitoring.py (consolidated into ScalingManager)
- ❌ REMOVED: scaling_types.py (consolidated into ScalingManager)
"""

# ARCHITECTURE CORRECTED: Using unified scaling manager
from ..managers.scaling_manager import (
    ScalingManager,
    ScalingStrategy,
    ScalingStatus,
    LoadBalancerType,
    ScalingConfig,
    ScalingMetrics,
    ScalingDecision
)

# Backward compatibility
__all__ = [
    "ScalingManager",
    "ScalingStrategy",
    "ScalingStatus",
    "LoadBalancerType",
    "ScalingConfig",
    "ScalingMetrics",
    "ScalingDecision"
]
