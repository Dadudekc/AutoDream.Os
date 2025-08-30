#!/usr/bin/env python3
"""
Configuration models for momentum acceleration system
Extracted from momentum_acceleration_system.py for modularization
"""

from dataclasses import dataclass
from enum import Enum

class MomentumStatus(Enum):
    """Momentum status enumeration"""
    STALLED = "STALLED"
    RECOVERING = "RECOVERING"
    ACCELERATING = "ACCELERATING"
    SUSTAINED = "SUSTAINED"
    FULLY_OPERATIONAL = "FULLY_OPERATIONAL"

class AccelerationPhase(Enum):
    """Acceleration phase enumeration"""
    EMERGENCY_RESPONSE = "EMERGENCY_RESPONSE"
    SYSTEM_RECOVERY = "SYSTEM_RECOVERY"
    MOMENTUM_SUSTAINMENT = "MOMENTUM_SUSTAINMENT"
    CONTINUOUS_OPTIMIZATION = "CONTINUOUS_OPTIMIZATION"

@dataclass
class ContractMetrics:
    """Contract performance metrics"""
    total_contracts: int
    available_contracts: int
    claimed_contracts: int
    completed_contracts: int
    completion_rate: float
    extra_credit_points: int
    
    @property
    def productivity_score(self) -> float:
        """Calculate productivity score based on completion rate and available contracts"""
        if self.total_contracts == 0:
            return 0.0
        completion_weight = 0.6
        availability_weight = 0.4
        return (self.completion_rate * completion_weight) + \
               (min(self.available_contracts / 10, 1.0) * availability_weight)

@dataclass
class AccelerationMeasure:
    """Individual acceleration measure configuration"""
    measure_id: str
    name: str
    description: str
    implementation_time: int  # minutes
    contracts_generated: int
    extra_credit_points: int
    system_impact: str
    status: str
    priority: int

@dataclass
class MomentumAccelerationConfig:
    """Momentum acceleration system configuration"""
    emergency_response_threshold: int = 5  # minutes
    perpetual_motion_threshold: int = 10   # minutes
    momentum_sustainment_threshold: int = 15  # minutes
    priority_management_threshold: int = 5  # minutes
    contract_generation_rate: int = 25     # contracts per cycle
    points_generation_rate: int = 7975     # points per cycle
    system_recovery_timeout: int = 60      # minutes
