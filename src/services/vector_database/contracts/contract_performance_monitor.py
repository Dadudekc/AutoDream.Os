#!/usr/bin/env python3
"""
Contract Performance Monitor
============================

Monitors contract execution performance and statistics.
V2 Compliance: ≤150 lines, focused responsibility, KISS principle.
"""

import logging
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

from .contract_models import V3Contract, ContractStatus

logger = logging.getLogger(__name__)


class ContractPerformanceMonitor:
    """Monitors contract execution performance."""
    
    def __init__(self):
        """Initialize performance monitor."""
        self._execution_stats = {
            'contracts_processed': 0,
            'contracts_completed': 0,
            'execution_success_rate': 100.0,
            'quality_score': 100.0,
            'start_time': None,
            'last_update': None
        }
        
        self._performance_history = []
    
    def update_execution_stats(self, contracts: List[V3Contract]) -> Dict[str, Any]:
        """Update execution statistics."""
        try:
            # Calculate metrics
            total_contracts = len(contracts)
            completed_contracts = len([c for c in contracts if c.status == ContractStatus.COMPLETED])
            failed_contracts = len([c for c in contracts if c.status == ContractStatus.FAILED])
            
            # Calculate success rate
            if total_contracts > 0:
                success_rate = (completed_contracts / total_contracts) * 100
                self._execution_stats['execution_success_rate'] = success_rate
            
            # Update counters
            self._execution_stats['contracts_completed'] = completed_contracts
            self._execution_stats['contracts_processed'] += 1
            self._execution_stats['last_update'] = datetime.now(timezone.utc)
            
            # Initialize start time if not set
            if not self._execution_stats['start_time']:
                self._execution_stats['start_time'] = datetime.now(timezone.utc)
            
            # Store performance snapshot
            self._performance_history.append({
                'timestamp': datetime.now(timezone.utc),
                'metrics': self._execution_stats.copy()
            })
            
            # Keep only last 100 snapshots
            if len(self._performance_history) > 100:
                self._performance_history = self._performance_history[-100:]
            
            return self._execution_stats.copy()
            
        except Exception as e:
            logger.error(f"Failed to update execution stats: {e}")
            return self._execution_stats.copy()
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics."""
        try:
            current_time = datetime.now(timezone.utc)
            
            # Calculate uptime
            uptime = None
            if self._execution_stats['start_time']:
                uptime_seconds = (current_time - self._execution_stats['start_time']).total_seconds()
                uptime = {
                    'seconds': uptime_seconds,
                    'minutes': uptime_seconds / 60,
                    'hours': uptime_seconds / 3600
                }
            
            return {
                'execution_stats': self._execution_stats.copy(),
                'uptime': uptime,
                'performance_history_count': len(self._performance_history),
                'current_timestamp': current_time.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to get performance metrics: {e}")
            return {'error': str(e)}
    
    def get_performance_trend(self, hours: int = 1) -> Dict[str, Any]:
        """Get performance trend over specified hours."""
        try:
            cutoff_time = datetime.now(timezone.utc).timestamp() - (hours * 3600)
            
            recent_history = [
                snapshot for snapshot in self._performance_history
                if snapshot['timestamp'].timestamp() >= cutoff_time
            ]
            
            if not recent_history:
                return {'trend': 'no_data', 'data_points': 0}
            
            # Calculate trend
            first_success_rate = recent_history[0]['metrics']['execution_success_rate']
            last_success_rate = recent_history[-1]['metrics']['execution_success_rate']
            
            trend_direction = 'stable'
            if last_success_rate > first_success_rate + 5:
                trend_direction = 'improving'
            elif last_success_rate < first_success_rate - 5:
                trend_direction = 'declining'
            
            return {
                'trend': trend_direction,
                'data_points': len(recent_history),
                'first_success_rate': first_success_rate,
                'last_success_rate': last_success_rate,
                'change': last_success_rate - first_success_rate
            }
            
        except Exception as e:
            logger.error(f"Failed to get performance trend: {e}")
            return {'error': str(e)}
    
    def reset_stats(self) -> None:
        """Reset execution statistics."""
        try:
            self._execution_stats = {
                'contracts_processed': 0,
                'contracts_completed': 0,
                'execution_success_rate': 100.0,
                'quality_score': 100.0,
                'start_time': datetime.now(timezone.utc),
                'last_update': None
            }
            self._performance_history.clear()
            logger.info("Performance stats reset")
            
        except Exception as e:
            logger.error(f"Failed to reset stats: {e}")
