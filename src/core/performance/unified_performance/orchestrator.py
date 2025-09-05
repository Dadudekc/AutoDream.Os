"""
Performance Optimization Orchestrator
=====================================

Main orchestrator for performance optimization operations.
V2 Compliance: < 300 lines, single responsibility, orchestration logic.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging
from .models import (
    OptimizationRule, OptimizationResult, PerformanceMetrics,
    OptimizationConfig, OptimizationType, OptimizationPriority
)
from .engine import PerformanceEngine
from .optimizer import PerformanceOptimizer


class PerformanceOptimizationOrchestrator:
    """Main orchestrator for performance optimization operations."""
    
    def __init__(self):
        """Initialize performance optimization orchestrator."""
        self.engine = PerformanceEngine()
        self.optimizer = PerformanceOptimizer()
        self.logger = logging.getLogger(__name__)
        self.is_initialized = False
        self.config: Optional[OptimizationConfig] = None
    
    async def initialize(self, config: OptimizationConfig = None) -> bool:
        """Initialize the orchestrator."""
        try:
            self.logger.info("Initializing Performance Optimization Orchestrator")
            
            # Set default config if not provided
            if config is None:
                config = OptimizationConfig(
                    config_id="default",
                    name="Default Performance Config",
                    description="Default performance optimization configuration"
                )
            
            self.config = config
            
            # Load default optimization rules
            default_rules = self.optimizer.create_default_rules()
            for rule in default_rules:
                await self.engine.add_optimization_rule(rule)
            
            # Start monitoring if auto-optimization is enabled
            if config.auto_optimization_enabled:
                await self.engine.start_monitoring(config.metrics_collection_interval)
            
            self.is_initialized = True
            self.logger.info("Performance Optimization Orchestrator initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Performance Optimization Orchestrator: {e}")
            return False
    
    async def add_optimization_rule(self, rule: OptimizationRule) -> bool:
        """Add optimization rule."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return await self.engine.add_optimization_rule(rule)
    
    async def remove_optimization_rule(self, rule_id: str) -> bool:
        """Remove optimization rule."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        try:
            if rule_id in self.engine.rules:
                del self.engine.rules[rule_id]
                self.logger.info(f"Removed optimization rule: {rule_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error removing rule {rule_id}: {e}")
            return False
    
    async def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.engine.get_performance_summary()
    
    async def get_optimization_results(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get optimization results."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.engine.get_optimization_results(limit)
    
    async def get_active_optimizations(self) -> List[Dict[str, Any]]:
        """Get active optimizations."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return [
            {
                'result_id': result.result_id,
                'rule_id': result.rule_id,
                'status': result.status.value,
                'start_time': result.start_time.isoformat(),
                'duration': (datetime.now() - result.start_time).total_seconds()
            }
            for result in self.engine.active_optimizations.values()
        ]
    
    async def trigger_optimization(self, rule_id: str) -> bool:
        """Manually trigger optimization for a specific rule."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        try:
            if rule_id not in self.engine.rules:
                self.logger.error(f"Rule {rule_id} not found")
                return False
            
            rule = self.engine.rules[rule_id]
            current_metrics = self.engine._collect_metrics()
            
            # Execute optimization
            self.engine._execute_optimization(rule, current_metrics)
            self.logger.info(f"Triggered optimization for rule: {rule.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error triggering optimization for rule {rule_id}: {e}")
            return False
    
    async def get_optimization_rules(self) -> List[Dict[str, Any]]:
        """Get all optimization rules."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return [
            {
                'rule_id': rule.rule_id,
                'name': rule.name,
                'description': rule.description,
                'optimization_type': rule.optimization_type.value,
                'priority': rule.priority.value,
                'enabled': rule.enabled,
                'created_at': rule.created_at.isoformat()
            }
            for rule in self.engine.rules.values()
        ]
    
    async def update_rule_status(self, rule_id: str, enabled: bool) -> bool:
        """Update rule enabled status."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        try:
            if rule_id in self.engine.rules:
                self.engine.rules[rule_id].enabled = enabled
                self.logger.info(f"Updated rule {rule_id} status to {enabled}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error updating rule {rule_id} status: {e}")
            return False
    
    async def get_performance_metrics(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get performance metrics history."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        metrics = self.engine.metrics_history[-limit:] if limit > 0 else self.engine.metrics_history
        return [metric.to_dict() for metric in metrics]
    
    async def analyze_bottlenecks(self) -> List[str]:
        """Analyze current performance bottlenecks."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        if not self.engine.metrics_history:
            return ["No performance data available"]
        
        latest_metrics = self.engine.metrics_history[-1]
        return self.optimizer.analyze_performance_bottlenecks(latest_metrics)
    
    async def clear_old_data(self, days: int = 7):
        """Clear old performance data."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        self.engine.clear_old_data(days)
        self.logger.info(f"Cleared performance data older than {days} days")
    
    def shutdown(self):
        """Shutdown orchestrator."""
        if not self.is_initialized:
            return
        
        self.logger.info("Shutting down Performance Optimization Orchestrator")
        self.engine.stop_monitoring()
        self.is_initialized = False
    
    def get_config(self) -> Optional[OptimizationConfig]:
        """Get current configuration."""
        return self.config
    
    async def update_config(self, config: OptimizationConfig) -> bool:
        """Update configuration."""
        try:
            self.config = config
            
            # Restart monitoring if needed
            if config.auto_optimization_enabled and not self.engine.is_running:
                await self.engine.start_monitoring(config.metrics_collection_interval)
            elif not config.auto_optimization_enabled and self.engine.is_running:
                self.engine.stop_monitoring()
            
            self.logger.info("Configuration updated successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error updating configuration: {e}")
            return False
