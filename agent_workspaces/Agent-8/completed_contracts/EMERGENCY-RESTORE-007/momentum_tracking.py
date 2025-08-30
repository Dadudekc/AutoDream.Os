#!/usr/bin/env python3
"""
Momentum tracking module for momentum acceleration system
Extracted from momentum_acceleration_system.py for modularization
"""

import logging
from typing import Dict
from config_models import MomentumStatus, AccelerationPhase

logger = logging.getLogger(__name__)

class MomentumTracker:
    """Handles momentum status tracking and metrics analysis"""
    
    @staticmethod
    def check_momentum_metrics(meeting_data: Dict) -> Dict:
        """
        Check momentum metrics from meeting.json
        
        Args:
            meeting_data: Parsed meeting.json data
            
        Returns:
            Dictionary with momentum analysis results
        """
        try:
            momentum_analysis = {
                'system_health': meeting_data.get('current_status', {}).get('system_health', 'UNKNOWN'),
                'perpetual_motion': meeting_data.get('current_status', {}).get('perpetual_motion', 'UNKNOWN'),
                'sprint_momentum': meeting_data.get('current_status', {}).get('sprint_momentum', 'UNKNOWN'),
                'contract_system': meeting_data.get('current_status', {}).get('contract_system', 'UNKNOWN'),
                'momentum_sustainment': meeting_data.get('current_status', {}).get('momentum_sustainment', 'UNKNOWN')
            }
            
            # Analyze momentum status
            if 'STALLED' in str(momentum_analysis.values()) or 'EMERGENCY' in str(momentum_analysis.values()):
                momentum_status = "CRITICAL - Emergency intervention required"
            elif 'ACTIVE' in str(momentum_analysis.values()) and 'OPERATIONAL' in str(momentum_analysis.values()):
                momentum_status = "HEALTHY - Momentum sustained"
            else:
                momentum_status = "MIXED - Some systems operational, others need attention"
            
            momentum_analysis['overall_status'] = momentum_status
            
            logger.info(f"📈 Momentum Metrics Analysis:")
            logger.info(f"   System Health: {momentum_analysis['system_health']}")
            logger.info(f"   Perpetual Motion: {momentum_analysis['perpetual_motion']}")
            logger.info(f"   Sprint Momentum: {momentum_analysis['sprint_momentum']}")
            logger.info(f"   Overall Status: {momentum_status}")
            
            return momentum_analysis
            
        except Exception as e:
            logger.error(f"❌ Error checking momentum metrics: {e}")
            return {'error': str(e)}
    
    @staticmethod
    def get_next_actions(current_phase: AccelerationPhase) -> list:
        """Get next actions for momentum sustainment"""
        actions = []
        
        if current_phase == AccelerationPhase.EMERGENCY_RESPONSE:
            actions.extend([
                "Complete emergency response implementation",
                "Transition to system recovery phase",
                "Validate emergency contract system functionality"
            ])
        elif current_phase == AccelerationPhase.SYSTEM_RECOVERY:
            actions.extend([
                "Complete system recovery implementation",
                "Transition to momentum sustainment phase",
                "Validate perpetual motion system operation"
            ])
        elif current_phase == AccelerationPhase.MOMENTUM_SUSTAINMENT:
            actions.extend([
                "Complete momentum sustainment implementation",
                "Transition to continuous optimization phase",
                "Validate momentum sustainment protocols"
            ])
        elif current_phase == AccelerationPhase.CONTINUOUS_OPTIMIZATION:
            actions.extend([
                "Monitor system performance continuously",
                "Optimize acceleration algorithms",
                "Maintain momentum sustainment"
            ])
        
        return actions
