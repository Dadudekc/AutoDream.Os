"""
Unified Integration Coordinator - V2 Compliant Module
====================================================

Main coordinator for integration operations.
Coordinates all coordinator components and provides unified interface.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import asyncio
import time
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime

from ..models import (
    IntegrationType, IntegrationConfig, IntegrationTask,
    IntegrationStatus, IntegrationModels
)
from ..optimizer import IntegrationOptimizer
from ..monitor import IntegrationMonitor
from .task_manager import TaskManager
from .health_monitor import HealthMonitor
from .config_manager import ConfigManager


class UnifiedIntegrationCoordinator:
    """
    Main coordinator for integration operations.
    
    Coordinates task management, health monitoring, and configuration
    for integration operations.
    """
    
    def __init__(self, config: IntegrationConfig = None):
        """Initialize integration coordinator."""
        self.config = config or IntegrationModels.create_integration_config()
        self.optimizer = IntegrationOptimizer()
        self.monitor = IntegrationMonitor(self.config)
        
        # Initialize component managers
        self.task_manager = TaskManager(self.config)
        self.health_monitor = HealthMonitor(self.config)
        self.config_manager = ConfigManager(self.config)
        
        self.coordination_active = False
    
    def start_coordination(self) -> None:
        """Start integration coordination."""
        self.coordination_active = True
        self.monitor.start_monitoring()
        
        # Register default optimization configs
        self._register_default_configs()
    
    def stop_coordination(self) -> None:
        """Stop integration coordination."""
        self.coordination_active = False
        self.monitor.stop_monitoring()
    
    def register_integration_handler(
        self, 
        integration_type: IntegrationType, 
        handler: Callable
    ) -> None:
        """Register integration handler."""
        self.task_manager.register_integration_handler(integration_type, handler)
    
    def execute_integration(
        self,
        integration_type: IntegrationType,
        operation: str,
        data: Any,
        priority: int = 1,
        timeout: int = 30
    ) -> Dict[str, Any]:
        """Execute integration operation."""
        # Create task
        task = self.task_manager.create_task(
            integration_type, operation, data, priority, timeout
        )
        
        # Execute task
        result = self.task_manager.execute_task(task)
        
        # Record metrics
        self.monitor.record_request(
            integration_type, 
            result['execution_time'], 
            result['success']
        )
        
        # Auto-optimize if enabled
        if self.config.auto_optimize:
            self._auto_optimize(integration_type)
        
        # Clean up task
        self.task_manager.cleanup_completed_tasks()
        
        return result
    
    async def execute_integration_async(
        self,
        integration_type: IntegrationType,
        operation: str,
        data: Any,
        priority: int = 1,
        timeout: int = 30
    ) -> Dict[str, Any]:
        """Execute integration operation asynchronously."""
        # Create task
        task = self.task_manager.create_task(
            integration_type, operation, data, priority, timeout
        )
        
        # Execute task asynchronously
        result = await self.task_manager.execute_task_async(task)
        
        # Record metrics
        self.monitor.record_request(
            integration_type, 
            result['execution_time'], 
            result['success']
        )
        
        # Auto-optimize if enabled
        if self.config.auto_optimize:
            self._auto_optimize(integration_type)
        
        # Clean up task
        self.task_manager.cleanup_completed_tasks()
        
        return result
    
    def get_integration_status(self, integration_type: IntegrationType) -> Dict[str, Any]:
        """Get status of specific integration."""
        metrics = self.monitor.get_metrics(integration_type)
        
        if not metrics:
            return {
                'integration_type': integration_type.value,
                'status': 'not_registered',
                'message': 'Integration not registered'
            }
        
        return {
            'integration_type': integration_type.value,
            'status': 'active',
            'metrics': metrics,
            'health': self.monitor._is_integration_healthy(integration_type, metrics)
        }
    
    def get_coordination_status(self) -> Dict[str, Any]:
        """Get overall coordination status."""
        return {
            'coordination_active': self.coordination_active,
            'task_manager': self.task_manager.get_manager_status(),
            'health_monitor': self.health_monitor.get_monitor_status(),
            'config_manager': self.config_manager.get_manager_status(),
            'monitoring_active': self.monitor.monitoring_active,
            'optimization_status': self.optimizer.get_optimization_status(),
            'health_status': self.monitor.get_health_status()
        }
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary."""
        return self.monitor.get_performance_summary()
    
    def get_optimization_recommendations(
        self, 
        integration_type: Optional[IntegrationType] = None
    ) -> List[Dict[str, Any]]:
        """Get optimization recommendations."""
        if integration_type:
            metrics = self.monitor.get_metrics(integration_type)
            if metrics:
                return self.optimizer.get_optimization_recommendations(metrics)
            return []
        
        # Get recommendations for all integrations
        all_recommendations = []
        for itype in IntegrationType:
            metrics = self.monitor.get_metrics(itype)
            if metrics:
                recommendations = self.optimizer.get_optimization_recommendations(metrics)
                all_recommendations.extend(recommendations)
        
        return all_recommendations
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health."""
        return self.health_monitor.get_system_health(self.monitor, self.optimizer)
    
    def export_configuration(self) -> Dict[str, Any]:
        """Export coordination configuration."""
        return self.config_manager.export_configuration(
            self.task_manager.integration_handlers,
            self.health_monitor.get_alert_thresholds(),
            self.optimizer.get_optimization_status()
        )
    
    def _register_default_configs(self) -> None:
        """Register default optimization configurations."""
        # This would register default optimization configs
        # Implementation depends on specific requirements
        pass
    
    def _auto_optimize(self, integration_type: IntegrationType) -> None:
        """Auto-optimize integration if needed."""
        metrics = self.monitor.get_metrics(integration_type)
        if metrics:
            self.optimizer.optimize_integration(integration_type, metrics)
    
    def add_monitoring_callback(self, callback: Callable) -> None:
        """Add monitoring callback."""
        self.health_monitor.add_monitoring_callback(callback)
    
    def set_alert_threshold(self, metric: str, threshold: float) -> None:
        """Set alert threshold."""
        self.health_monitor.set_alert_threshold(metric, threshold)
    
    def get_alert_thresholds(self) -> Dict[str, float]:
        """Get alert thresholds."""
        return self.health_monitor.get_alert_thresholds()
