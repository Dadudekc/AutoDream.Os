#!/usr/bin/env python3
"""
Main orchestration module for momentum acceleration system
Modularized version of momentum_acceleration_system.py
"""

import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import asdict

# Import modularized components
from config_models import (
    MomentumStatus, AccelerationPhase, MomentumAccelerationConfig,
    ContractMetrics, AccelerationMeasure
)
from contract_analytics import ContractAnalytics
from momentum_tracking import MomentumTracker
from acceleration_strategies import AccelerationStrategies
from system_health import SystemHealthMonitor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('momentum_acceleration.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MomentumAccelerationSystem:
    """
    🚀 MOMENTUM ACCELERATION SYSTEM 🚀
    
    Modularized version that orchestrates all acceleration components
    """
    
    def __init__(self, config: MomentumAccelerationConfig):
        self.config = config
        self.current_status = MomentumStatus.STALLED
        self.current_phase = AccelerationPhase.EMERGENCY_RESPONSE
        self.acceleration_measures: List[AccelerationMeasure] = []
        self.contract_metrics: Optional[ContractMetrics] = None
        self.last_acceleration_time = datetime.now()
        self.emergency_contracts_generated = 0
        self.perpetual_motion_contracts_generated = 0
        self.momentum_sustainment_contracts_generated = 0
        
        # Initialize acceleration measures
        self._initialize_acceleration_measures()
        
        logger.info("🚀 Momentum Acceleration System initialized successfully")
    
    def _initialize_acceleration_measures(self):
        """Initialize all acceleration measures using the strategies module"""
        self.acceleration_measures = AccelerationStrategies.initialize_acceleration_measures()
    
    def analyze_contract_completion_rates(self, task_list_data: Dict) -> ContractMetrics:
        """Analyze contract completion rates using the analytics module"""
        self.contract_metrics = ContractAnalytics.analyze_contract_completion_rates(task_list_data)
        return self.contract_metrics
    
    def check_momentum_metrics(self, meeting_data: Dict) -> Dict:
        """Check momentum metrics using the tracking module"""
        return MomentumTracker.check_momentum_metrics(meeting_data)
    
    def implement_momentum_acceleration_measures(self) -> Dict:
        """Implement acceleration measures using the strategies module"""
        return AccelerationStrategies.implement_momentum_acceleration_measures(
            self.current_phase, self.acceleration_measures
        )
    
    def _assess_system_health(self) -> Dict:
        """Assess system health using the health monitor"""
        return SystemHealthMonitor.assess_system_health(
            self.current_status, self.current_phase, 
            asdict(self.contract_metrics) if self.contract_metrics else None
        )
    
    def ensure_continuous_task_flow(self) -> Dict:
        """Ensure continuous task flow using the health monitor"""
        return SystemHealthMonitor.ensure_continuous_task_flow()
    
    def get_system_status_report(self) -> Dict:
        """Generate comprehensive system status report"""
        try:
            report = {
                'timestamp': datetime.now().isoformat(),
                'system_status': {
                    'momentum_status': self.current_status.value,
                    'acceleration_phase': self.current_phase.value,
                    'health_score': self._assess_system_health().get('health_score', 0),
                    'health_status': self._assess_system_health().get('health_status', 'UNKNOWN')
                },
                'contract_metrics': asdict(self.contract_metrics) if self.contract_metrics else None,
                'acceleration_measures': {
                    'total_implemented': len([m for m in self.acceleration_measures if m.status != 'PENDING']),
                    'total_pending': len([m for m in self.acceleration_measures if m.status == 'PENDING']),
                    'measures': [asdict(m) for m in self.acceleration_measures]
                },
                'contract_generation': {
                    'emergency_contracts': self.emergency_contracts_generated,
                    'perpetual_motion_contracts': self.perpetual_motion_contracts_generated,
                    'momentum_sustainment_contracts': self.momentum_sustainment_contracts_generated,
                    'total_contracts_generated': (
                        self.emergency_contracts_generated +
                        self.perpetual_motion_contracts_generated +
                        self.momentum_sustainment_contracts_generated
                    )
                },
                'continuous_task_flow': self.ensure_continuous_task_flow(),
                'last_acceleration': self.last_acceleration_time.isoformat(),
                'next_actions': MomentumTracker.get_next_actions(self.current_phase)
            }
            
            return report
            
        except Exception as e:
            logger.error(f"❌ Error generating system status report: {e}")
            return {'error': str(e)}

def main():
    """Main execution function"""
    try:
        logger.info("🚨 EMERGENCY-RESTORE-007: MOMENTUM ACCELERATION SYSTEM STARTING 🚨")
        
        # Initialize configuration
        config = MomentumAccelerationConfig()
        
        # Initialize momentum acceleration system
        momentum_system = MomentumAccelerationSystem(config)
        
        # Get system status report
        status_report = momentum_system.get_system_status_report()
        
        # Log system status
        logger.info("📊 SYSTEM STATUS REPORT:")
        logger.info(f"   Momentum Status: {status_report['system_status']['momentum_status']}")
        logger.info(f"   Acceleration Phase: {status_report['system_status']['acceleration_phase']}")
        logger.info(f"   Health Score: {status_report['system_status']['health_score']}")
        logger.info(f"   Health Status: {status_report['system_status']['health_status']}")
        
        # Ensure continuous task flow
        task_flow_status = momentum_system.ensure_continuous_task_flow()
        logger.info(f"   Continuous Task Flow: {task_flow_status['status']}")
        
        logger.info("✅ MOMENTUM ACCELERATION SYSTEM OPERATIONAL")
        
        return status_report
        
    except Exception as e:
        logger.error(f"❌ CRITICAL ERROR in momentum acceleration system: {e}")
        return {'error': str(e), 'status': 'CRITICAL_FAILURE'}

if __name__ == "__main__":
    main()
