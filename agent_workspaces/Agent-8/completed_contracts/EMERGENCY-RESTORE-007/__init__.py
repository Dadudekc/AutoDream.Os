#!/usr/bin/env python3
"""
EMERGENCY-RESTORE-007 Package
=============================

Momentum acceleration and contract management system.
Follows V2 standards: modular, compliant architecture.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from .momentum_core import (
    MomentumCore, 
    MomentumStatus, 
    AccelerationPhase, 
    ContractMetrics,
    AccelerationMeasure,
    MomentumAccelerationConfig
)
from .contract_manager import (
    ContractManager,
    ContractTemplate,
    GeneratedContract
)
from .momentum_orchestrator import MomentumOrchestrator

__all__ = [
    'MomentumCore',
    'MomentumStatus',
    'AccelerationPhase', 
    'ContractMetrics',
    'AccelerationMeasure',
    'MomentumAccelerationConfig',
    'ContractManager',
    'ContractTemplate',
    'GeneratedContract',
    'MomentumOrchestrator'
]

__version__ = "1.0.0"
__author__ = "V2 SWARM CAPTAIN"
__license__ = "MIT"
