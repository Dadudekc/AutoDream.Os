#!/usr/bin/env python3
"""
Contract analytics module for momentum acceleration system
Extracted from momentum_acceleration_system.py for modularization
"""

import logging
from typing import Dict
from config_models import ContractMetrics

logger = logging.getLogger(__name__)

class ContractAnalytics:
    """Handles contract completion rate analysis and metrics"""
    
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
