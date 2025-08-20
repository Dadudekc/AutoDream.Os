#!/usr/bin/env python3
"""
Scaling Package - Agent Cellphone V2
====================================

Refactored horizontal scaling system.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.
"""

from .scaling_types import (
    ScalingStrategy,
    ScalingStatus,
    LoadBalancerType,
    ScalingConfig,
    ScalingMetrics,
    ScalingDecision
)

from .scaling_core import HorizontalScalingEngine
from .scaling_distribution import LoadDistributor
from .scaling_monitoring import ScalingMonitor

# Backward compatibility
__all__ = [
    'ScalingStrategy',
    'ScalingStatus',
    'LoadBalancerType',
    'ScalingConfig',
    'ScalingMetrics',
    'ScalingDecision',
    'HorizontalScalingEngine',
    'LoadDistributor',
    'ScalingMonitor'
]
