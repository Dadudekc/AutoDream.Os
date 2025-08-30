#!/usr/bin/env python3
"""
🚨 MOMENTUM SYSTEM ANALYTICS 🚨

Analytics and metrics analysis for the momentum acceleration system.

Author: Agent-8 (INTEGRATION ENHANCEMENT OPTIMIZATION MANAGER)
Contract: EMERGENCY-RESTORE-007
Status: MODULARIZED
"""

import logging
from typing import Dict, List
from datetime import datetime
from .models import ContractMetrics, MomentumAnalysis

logger = logging.getLogger(__name__)

class MomentumAnalytics:
    """Analytics engine for momentum system metrics and analysis"""
    
    @staticmethod
    def analyze_contract_completion_rates(task_list_data: Dict) -> ContractMetrics:
        """
        Analyze contract completion rates from task_list.json
        
        Args:
            task_list_data: Parsed task_list.json data
            
        Returns:
            ContractMetrics object with analysis results
        """
        try:
            total_contracts = task_list_data.get('total_contracts', 0)
            available_contracts = task_list_data.get('available_contracts', 0)
            claimed_contracts = task_list_data.get('claimed_contracts', 0)
            completed_contracts = task_list_data.get('completed_contracts', 0)
            
            # Calculate completion rate
            completion_rate = (completed_contracts / total_contracts * 100) if total_contracts > 0 else 0.0
            
            # Calculate total extra credit points
            total_extra_credit = 0
            if 'contracts' in task_list_data:
                for category, category_data in task_list_data['contracts'].items():
                    if 'contracts' in category_data:
                        for contract in category_data['contracts']:
                            if contract.get('status') == 'COMPLETED':
                                total_extra_credit += contract.get('extra_credit_points', 0)
            
            metrics = ContractMetrics(
                total_contracts=total_contracts,
                available_contracts=available_contracts,
                claimed_contracts=claimed_contracts,
                completed_contracts=completed_contracts,
                completion_rate=completion_rate,
                extra_credit_points=total_extra_credit
            )
            
            logger.info(f"📊 Contract Analysis Complete:")
            logger.info(f"   Total: {total_contracts}, Available: {available_contracts}")
            logger.info(f"   Claimed: {claimed_contracts}, Completed: {completed_contracts}")
            logger.info(f"   Completion Rate: {completion_rate:.1f}%")
            logger.info(f"   Productivity Score: {metrics.productivity_score:.2f}")
            
            return metrics
            
        except Exception as e:
            logger.error(f"❌ Error analyzing contract completion rates: {e}")
            return ContractMetrics(0, 0, 0, 0, 0.0, 0)
    
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
    def generate_productivity_report(contract_metrics: ContractMetrics, momentum_analysis: Dict) -> Dict:
        """
        Generate comprehensive productivity report
        
        Args:
            contract_metrics: Contract performance metrics
            momentum_analysis: Momentum analysis results
            
        Returns:
            Dictionary with productivity report
        """
        try:
            report = {
                'timestamp': datetime.now().isoformat(),
                'contract_performance': {
                    'total_contracts': contract_metrics.total_contracts,
                    'available_contracts': contract_metrics.available_contracts,
                    'claimed_contracts': contract_metrics.claimed_contracts,
                    'completed_contracts': contract_metrics.completed_contracts,
                    'completion_rate': contract_metrics.completion_rate,
                    'productivity_score': contract_metrics.productivity_score,
                    'extra_credit_points': contract_metrics.extra_credit_points
                },
                'momentum_status': momentum_analysis,
                'recommendations': []
            }
            
            # Generate recommendations based on metrics
            if contract_metrics.completion_rate < 50:
                report['recommendations'].append("Low completion rate detected - implement acceleration measures")
            
            if contract_metrics.available_contracts < 5:
                report['recommendations'].append("Low contract availability - generate new contracts")
            
            if 'CRITICAL' in str(momentum_analysis.values()):
                report['recommendations'].append("Critical system status - immediate intervention required")
            
            logger.info(f"📋 Productivity Report Generated with {len(report['recommendations'])} recommendations")
            return report
            
        except Exception as e:
            logger.error(f"❌ Error generating productivity report: {e}")
            return {'error': str(e)}
