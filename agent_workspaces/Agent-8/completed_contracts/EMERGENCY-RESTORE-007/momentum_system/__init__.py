#!/usr/bin/env python3
"""
🚨 MOMENTUM ACCELERATION SYSTEM PACKAGE 🚨

Modularized momentum acceleration system package.

Author: Agent-8 (INTEGRATION ENHANCEMENT OPTIMIZATION MANAGER)
Contract: EMERGENCY-RESTORE-007
Status: MODULARIZED
"""

from .models import (
    MomentumStatus,
    AccelerationPhase,
    ContractMetrics,
    AccelerationMeasure,
    MomentumAccelerationConfig,
    MomentumAnalysis,
    ImplementationResult
)

from .analytics import MomentumAnalytics
from .implementation import MomentumImplementationEngine
from .acceleration_measures import AccelerationMeasuresManager
from .main import MomentumAccelerationSystem

__version__ = "2.0.0"
__author__ = "Agent-8 (INTEGRATION ENHANCEMENT OPTIMIZATION MANAGER)"
__status__ = "MODULARIZED"

__all__ = [
    'MomentumStatus',
    'AccelerationPhase',
    'ContractMetrics',
    'AccelerationMeasure',
    'MomentumAccelerationConfig',
    'MomentumAnalysis',
    'ImplementationResult',
    'MomentumAnalytics',
    'MomentumImplementationEngine',
    'AccelerationMeasuresManager',
    'MomentumAccelerationSystem'
]
