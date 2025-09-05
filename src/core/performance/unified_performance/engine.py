"""
Performance Engine
=================

Core engine for performance optimization operations.
V2 Compliance: < 300 lines, single responsibility, engine logic.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

import asyncio
import time
import gc
import threading
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging
import psutil
from .models import (
    OptimizationRule, OptimizationResult, PerformanceMetrics,
    OptimizationType, OptimizationStatus, OptimizationPriority
)


class PerformanceEngine:
    """Performance optimization engine."""
    
    def __init__(self):
        """Initialize performance engine."""
        self.rules: Dict[str, OptimizationRule] = {}
        self.results: Dict[str, OptimizationResult] = {}
        self.metrics_history: List[PerformanceMetrics] = []
        self.active_optimizations: Dict[str, OptimizationResult] = {}
        self.logger = logging.getLogger(__name__)
        self.is_running = False
        self.monitoring_thread = None
    
    async def start_monitoring(self, interval: int = 60):
        """Start performance monitoring."""
        if self.is_running:
            return
        
        self.is_running = True
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            args=(interval,),
            daemon=True
        )
        self.monitoring_thread.start()
        self.logger.info("Performance monitoring started")
    
    def stop_monitoring(self):
        """Stop performance monitoring."""
        self.is_running = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        self.logger.info("Performance monitoring stopped")
    
    def _monitoring_loop(self, interval: int):
        """Performance monitoring loop."""
        while self.is_running:
            try:
                metrics = self._collect_metrics()
                self.metrics_history.append(metrics)
                
                # Keep only last 1000 metrics
                if len(self.metrics_history) > 1000:
                    self.metrics_history = self.metrics_history[-1000:]
                
                # Check optimization rules
                self._check_optimization_rules(metrics)
                
                time.sleep(interval)
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(interval)
    
    def _collect_metrics(self) -> PerformanceMetrics:
        """Collect current performance metrics."""
        try:
            # Get system metrics
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            network = psutil.net_io_counters()
            
            # Calculate network usage (simplified)
            network_usage = 0.0
            if hasattr(network, 'bytes_sent') and hasattr(network, 'bytes_recv'):
                network_usage = (network.bytes_sent + network.bytes_recv) / (1024 * 1024)  # MB
            
            return PerformanceMetrics(
                timestamp=datetime.now(),
                cpu_usage=cpu_usage,
                memory_usage=memory.percent,
                disk_usage=disk.percent,
                network_usage=network_usage,
                response_time=0.0,  # Mock value
                throughput=0.0,     # Mock value
                error_rate=0.0,    # Mock value
                active_connections=0,  # Mock value
                queue_size=0       # Mock value
            )
        except Exception as e:
            self.logger.error(f"Error collecting metrics: {e}")
            return PerformanceMetrics(
                timestamp=datetime.now(),
                cpu_usage=0.0,
                memory_usage=0.0,
                disk_usage=0.0,
                network_usage=0.0,
                response_time=0.0,
                throughput=0.0,
                error_rate=0.0,
                active_connections=0,
                queue_size=0
            )
    
    def _check_optimization_rules(self, metrics: PerformanceMetrics):
        """Check optimization rules against current metrics."""
        metrics_dict = metrics.to_dict()
        
        for rule in self.rules.values():
            if not rule.enabled:
                continue
            
            try:
                if rule.condition(metrics_dict):
                    self._execute_optimization(rule, metrics)
            except Exception as e:
                self.logger.error(f"Error checking rule {rule.name}: {e}")
    
    def _execute_optimization(self, rule: OptimizationRule, metrics: PerformanceMetrics):
        """Execute optimization rule."""
        result = OptimizationResult(
            result_id=f"opt_{int(time.time())}",
            rule_id=rule.rule_id,
            status=OptimizationStatus.RUNNING,
            start_time=datetime.now(),
            metrics_before=metrics.to_dict()
        )
        
        self.active_optimizations[result.result_id] = result
        
        try:
            # Execute optimization action
            success = rule.action(metrics.to_dict())
            
            result.status = OptimizationStatus.COMPLETED if success else OptimizationStatus.FAILED
            result.success = success
            result.end_time = datetime.now()
            
            # Collect metrics after optimization
            new_metrics = self._collect_metrics()
            result.metrics_after = new_metrics.to_dict()
            
            self.logger.info(f"Optimization {rule.name} {'completed' if success else 'failed'}")
            
        except Exception as e:
            result.status = OptimizationStatus.FAILED
            result.error_message = str(e)
            result.end_time = datetime.now()
            self.logger.error(f"Optimization {rule.name} failed: {e}")
        
        finally:
            self.results[result.result_id] = result
            if result.result_id in self.active_optimizations:
                del self.active_optimizations[result.result_id]
    
    async def add_optimization_rule(self, rule: OptimizationRule) -> bool:
        """Add optimization rule."""
        try:
            validation = self._validate_rule(rule)
            if not validation['is_valid']:
                self.logger.error(f"Invalid rule: {validation['errors']}")
                return False
            
            self.rules[rule.rule_id] = rule
            self.logger.info(f"Added optimization rule: {rule.name}")
            return True
        except Exception as e:
            self.logger.error(f"Error adding rule: {e}")
            return False
    
    def _validate_rule(self, rule: OptimizationRule) -> Dict[str, Any]:
        """Validate optimization rule."""
        validation = {
            'is_valid': True,
            'warnings': [],
            'errors': []
        }
        
        if not rule.name:
            validation['errors'].append("Rule name is required")
            validation['is_valid'] = False
        
        if not callable(rule.condition):
            validation['errors'].append("Rule condition must be callable")
            validation['is_valid'] = False
        
        if not callable(rule.action):
            validation['errors'].append("Rule action must be callable")
            validation['is_valid'] = False
        
        return validation
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary."""
        if not self.metrics_history:
            return {
                'status': 'no_data',
                'message': 'No performance data available'
            }
        
        latest_metrics = self.metrics_history[-1]
        total_optimizations = len(self.results)
        successful_optimizations = sum(1 for r in self.results.values() if r.success)
        
        return {
            'status': 'active',
            'latest_metrics': latest_metrics.to_dict(),
            'total_optimizations': total_optimizations,
            'successful_optimizations': successful_optimizations,
            'success_rate': successful_optimizations / total_optimizations if total_optimizations > 0 else 0.0,
            'active_optimizations': len(self.active_optimizations),
            'rules_count': len(self.rules),
            'metrics_count': len(self.metrics_history)
        }
    
    def get_optimization_results(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get optimization results."""
        results = list(self.results.values())
        results.sort(key=lambda x: x.start_time, reverse=True)
        
        return [
            {
                'result_id': r.result_id,
                'rule_id': r.rule_id,
                'status': r.status.value,
                'start_time': r.start_time.isoformat(),
                'end_time': r.end_time.isoformat() if r.end_time else None,
                'duration': r.duration,
                'success': r.success,
                'error_message': r.error_message,
                'improvement_percentage': r.improvement_percentage
            }
            for r in results[:limit]
        ]
    
    def clear_old_data(self, days: int = 7):
        """Clear old performance data."""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Clear old metrics
        self.metrics_history = [
            m for m in self.metrics_history 
            if m.timestamp > cutoff_date
        ]
        
        # Clear old results
        old_results = [
            r_id for r_id, result in self.results.items()
            if result.start_time < cutoff_date
        ]
        for r_id in old_results:
            del self.results[r_id]
        
        self.logger.info(f"Cleared data older than {days} days")
