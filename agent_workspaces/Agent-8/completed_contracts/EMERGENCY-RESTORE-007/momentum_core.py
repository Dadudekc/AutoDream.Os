#!/usr/bin/env python3
"""
Momentum Core Module
====================

Core momentum acceleration functionality.
Follows V2 standards: ≤400 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
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


class MomentumCore:
    """Core momentum acceleration functionality"""
    
    def __init__(self, config: Optional[MomentumAccelerationConfig] = None):
        self.config = config or MomentumAccelerationConfig()
        self.logger = self._setup_logging()
        self.current_status = MomentumStatus.STALLED
        self.current_phase = AccelerationPhase.EMERGENCY_RESPONSE
        self.momentum_history: List[Dict[str, Any]] = []
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for momentum operations"""
        logger = logging.getLogger("MomentumCore")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '[MOMENTUM] %(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    def assess_momentum_status(self, metrics: ContractMetrics) -> MomentumStatus:
        """Assess current momentum status based on metrics"""
        try:
            if metrics.productivity_score >= 0.8:
                return MomentumStatus.FULLY_OPERATIONAL
            elif metrics.productivity_score >= 0.6:
                return MomentumStatus.SUSTAINED
            elif metrics.productivity_score >= 0.4:
                return MomentumStatus.ACCELERATING
            elif metrics.productivity_score >= 0.2:
                return MomentumStatus.RECOVERING
            else:
                return MomentumStatus.STALLED
                
        except Exception as e:
            self.logger.error(f"Error assessing momentum status: {e}")
            return MomentumStatus.STALLED
    
    def determine_acceleration_phase(self, status: MomentumStatus) -> AccelerationPhase:
        """Determine appropriate acceleration phase based on status"""
        try:
            if status == MomentumStatus.STALLED:
                return AccelerationPhase.EMERGENCY_RESPONSE
            elif status == MomentumStatus.RECOVERING:
                return AccelerationPhase.SYSTEM_RECOVERY
            elif status == MomentumStatus.ACCELERATING:
                return AccelerationPhase.MOMENTUM_SUSTAINMENT
            else:
                return AccelerationPhase.CONTINUOUS_OPTIMIZATION
                
        except Exception as e:
            self.logger.error(f"Error determining acceleration phase: {e}")
            return AccelerationPhase.EMERGENCY_RESPONSE
    
    def calculate_momentum_score(self, metrics: ContractMetrics) -> float:
        """Calculate comprehensive momentum score"""
        try:
            base_score = metrics.productivity_score * 100
            
            # Bonus for high completion rates
            if metrics.completion_rate > 0.8:
                base_score += 20
            
            # Bonus for available contracts
            if metrics.available_contracts > 5:
                base_score += 15
            
            # Bonus for extra credit points
            if metrics.extra_credit_points > 1000:
                base_score += 10
            
            return min(base_score, 100.0)
            
        except Exception as e:
            self.logger.error(f"Error calculating momentum score: {e}")
            return 0.0
    
    def update_momentum_history(self, status: MomentumStatus, phase: AccelerationPhase, 
                               metrics: ContractMetrics, score: float) -> None:
        """Update momentum history with current state"""
        try:
            history_entry = {
                "timestamp": datetime.now().isoformat(),
                "status": status.value,
                "phase": phase.value,
                "metrics": asdict(metrics),
                "momentum_score": score,
                "config": asdict(self.config)
            }
            
            self.momentum_history.append(history_entry)
            
            # Keep only last 100 entries
            if len(self.momentum_history) > 100:
                self.momentum_history = self.momentum_history[-100:]
                
        except Exception as e:
            self.logger.error(f"Error updating momentum history: {e}")
    
    def get_momentum_summary(self) -> Dict[str, Any]:
        """Get summary of momentum system status"""
        try:
            if not self.momentum_history:
                return {
                    "current_status": self.current_status.value,
                    "current_phase": self.current_phase.value,
                    "momentum_score": 0.0,
                    "history_count": 0,
                    "trend": "no_data"
                }
            
            latest = self.momentum_history[-1]
            previous = self.momentum_history[-2] if len(self.momentum_history) > 1 else None
            
            # Calculate trend
            if previous:
                if latest["momentum_score"] > previous["momentum_score"]:
                    trend = "improving"
                elif latest["momentum_score"] < previous["momentum_score"]:
                    trend = "declining"
                else:
                    trend = "stable"
            else:
                trend = "no_trend_data"
            
            return {
                "current_status": self.current_status.value,
                "current_phase": self.current_phase.value,
                "momentum_score": latest["momentum_score"],
                "history_count": len(self.momentum_history),
                "trend": trend,
                "last_update": latest["timestamp"]
            }
            
        except Exception as e:
            self.logger.error(f"Error getting momentum summary: {e}")
            return {
                "error": str(e),
                "current_status": "unknown",
                "momentum_score": 0.0
            }
    
    def reset_momentum_system(self) -> bool:
        """Reset momentum system to initial state"""
        try:
            self.current_status = MomentumStatus.STALLED
            self.current_phase = AccelerationPhase.EMERGENCY_RESPONSE
            self.momentum_history.clear()
            
            self.logger.info("Momentum system reset successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error resetting momentum system: {e}")
            return False
