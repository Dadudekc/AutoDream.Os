"""
Unified Utility System Orchestrator
===================================

Main orchestrator for utility system operations.
V2 Compliance: < 300 lines, single responsibility, orchestration.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

from typing import Any, Dict, List, Optional, Callable
from .models import (
    UtilityConfig, UtilityMetrics, UtilityOperationType, 
    UtilityStatus, UtilityOperation, UtilityResult, UtilitySystemModels
)
from .coordinator import UtilityCoordinator
from .factory import UtilityFactory


class UnifiedUtilitySystem:
    """Main orchestrator for utility system operations."""
    
    def __init__(self, config: UtilityConfig = None):
        """Initialize unified utility system."""
        self.factory = UtilityFactory()
        self.config = config or self.factory.create_default_config()
        self.coordinator = self.factory.create_coordinator(self.config)
        self.status = UtilityStatus.ACTIVE
    
    def execute_operation(
        self,
        operation_type: UtilityOperationType,
        operation_func: Callable,
        input_data: Any,
        operation_id: str = None,
        metadata: Dict[str, Any] = None
    ) -> UtilityResult:
        """Execute a utility operation."""
        if self.status != UtilityStatus.ACTIVE:
            return UtilitySystemModels.create_utility_result(
                success=False,
                error_message=f"System is not active. Current status: {self.status.value}"
            )
        
        return self.coordinator.execute_operation(
            operation_type=operation_type,
            operation_func=operation_func,
            input_data=input_data,
            operation_id=operation_id,
            metadata=metadata
        )
    
    def execute_cache_operation(
        self,
        operation_func: Callable,
        input_data: Any,
        operation_id: str = None,
        metadata: Dict[str, Any] = None
    ) -> UtilityResult:
        """Execute cache operation."""
        return self.execute_operation(
            UtilityOperationType.CACHE_OPERATION,
            operation_func,
            input_data,
            operation_id,
            metadata
        )
    
    def execute_validation_operation(
        self,
        operation_func: Callable,
        input_data: Any,
        operation_id: str = None,
        metadata: Dict[str, Any] = None
    ) -> UtilityResult:
        """Execute validation operation."""
        return self.execute_operation(
            UtilityOperationType.VALIDATION_OPERATION,
            operation_func,
            input_data,
            operation_id,
            metadata
        )
    
    def execute_transformation_operation(
        self,
        operation_func: Callable,
        input_data: Any,
        operation_id: str = None,
        metadata: Dict[str, Any] = None
    ) -> UtilityResult:
        """Execute transformation operation."""
        return self.execute_operation(
            UtilityOperationType.TRANSFORMATION_OPERATION,
            operation_func,
            input_data,
            operation_id,
            metadata
        )
    
    def execute_coordination_operation(
        self,
        operation_func: Callable,
        input_data: Any,
        operation_id: str = None,
        metadata: Dict[str, Any] = None
    ) -> UtilityResult:
        """Execute coordination operation."""
        return self.execute_operation(
            UtilityOperationType.COORDINATION_OPERATION,
            operation_func,
            input_data,
            operation_id,
            metadata
        )
    
    def execute_metrics_operation(
        self,
        operation_func: Callable,
        input_data: Any,
        operation_id: str = None,
        metadata: Dict[str, Any] = None
    ) -> UtilityResult:
        """Execute metrics operation."""
        return self.execute_operation(
            UtilityOperationType.METRICS_OPERATION,
            operation_func,
            input_data,
            operation_id,
            metadata
        )
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status."""
        return {
            'status': self.status.value,
            'config': {
                'cache_enabled': self.config.cache_enabled,
                'validation_enabled': self.config.validation_enabled,
                'transformation_enabled': self.config.transformation_enabled,
                'coordination_enabled': self.config.coordination_enabled,
                'metrics_enabled': self.config.metrics_enabled
            },
            'metrics': self.coordinator.get_metrics().__dict__,
            'active_operations': len(self.coordinator.get_active_operations())
        }
    
    def get_metrics(self) -> UtilityMetrics:
        """Get current metrics."""
        return self.coordinator.get_metrics()
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary."""
        return self.coordinator.get_performance_summary()
    
    def get_operation_history(
        self, 
        operation_type: Optional[UtilityOperationType] = None
    ) -> List[UtilityOperation]:
        """Get operation history."""
        return self.coordinator.get_operation_history(operation_type)
    
    def get_operation_status(self, operation_id: str) -> Optional[UtilityStatus]:
        """Get status of specific operation."""
        return self.coordinator.get_operation_status(operation_id)
    
    def clear_old_operations(self, hours_to_keep: int = 24) -> int:
        """Clear old operations."""
        return self.coordinator.clear_old_operations(hours_to_keep)
    
    def update_config(self, new_config: UtilityConfig) -> bool:
        """Update system configuration."""
        try:
            # Validate new configuration
            validation_results = self.factory.validate_config(new_config)
            
            if not validation_results['is_valid']:
                return False
            
            # Update configuration
            self.config = new_config
            self.coordinator = self.factory.create_coordinator(new_config)
            
            return True
            
        except Exception:
            return False
    
    def set_status(self, status: UtilityStatus) -> None:
        """Set system status."""
        self.status = status
    
    def start_system(self) -> bool:
        """Start the utility system."""
        try:
            self.status = UtilityStatus.ACTIVE
            return True
        except Exception:
            return False
    
    def stop_system(self) -> bool:
        """Stop the utility system."""
        try:
            self.status = UtilityStatus.INACTIVE
            return True
        except Exception:
            return False
    
    def restart_system(self) -> bool:
        """Restart the utility system."""
        try:
            self.stop_system()
            return self.start_system()
        except Exception:
            return False
    
    def get_config_presets(self) -> Dict[str, UtilityConfig]:
        """Get available configuration presets."""
        return self.factory.get_config_presets()
    
    def apply_config_preset(self, preset_name: str) -> bool:
        """Apply configuration preset."""
        presets = self.get_config_presets()
        
        if preset_name not in presets:
            return False
        
        return self.update_config(presets[preset_name])
    
    def register_operation(
        self, 
        operation_type: UtilityOperationType, 
        operation_class: type
    ) -> None:
        """Register operation class."""
        self.factory.register_operation(operation_type, operation_class)
    
    def get_registered_operations(self) -> Dict[UtilityOperationType, type]:
        """Get registered operations."""
        return self.factory.get_registered_operations()
    
    def validate_configuration(self) -> Dict[str, Any]:
        """Validate current configuration."""
        return self.factory.validate_config(self.config)
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get system health status."""
        metrics = self.get_metrics()
        performance = self.get_performance_summary()
        
        health_score = 100
        issues = []
        
        # Check success rate
        if performance['success_rate'] < 95:
            health_score -= 20
            issues.append(f"Low success rate: {performance['success_rate']:.1f}%")
        
        # Check response time
        if performance['average_response_time'] > 1000:  # > 1 second
            health_score -= 15
            issues.append(f"High response time: {performance['average_response_time']:.1f}ms")
        
        # Check cache hit rate
        if performance['cache_hit_rate'] < 50:
            health_score -= 10
            issues.append(f"Low cache hit rate: {performance['cache_hit_rate']:.1f}%")
        
        # Check active operations
        if performance['active_operations'] > 100:
            health_score -= 10
            issues.append(f"High active operations: {performance['active_operations']}")
        
        health_status = 'excellent' if health_score >= 90 else 'good' if health_score >= 70 else 'fair' if health_score >= 50 else 'poor'
        
        return {
            'health_score': health_score,
            'health_status': health_status,
            'issues': issues,
            'metrics': performance,
            'system_status': self.status.value
        }
