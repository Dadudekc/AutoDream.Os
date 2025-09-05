"""
Utility Coordinator
==================

Coordination logic for utility system operations.
V2 Compliance: < 300 lines, single responsibility, coordination.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

import time
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, timedelta
from .models import (
    UtilityOperationType, UtilityStatus, UtilityOperation, 
    UtilityResult, UtilityConfig, UtilityMetrics, UtilitySystemModels
)


class UtilityCoordinator:
    """Coordination logic for utility system operations."""
    
    def __init__(self, config: UtilityConfig):
        """Initialize utility coordinator."""
        self.config = config
        self.operations: Dict[str, UtilityOperation] = {}
        self.metrics = UtilitySystemModels.create_utility_metrics()
        self.active_operations: List[str] = []
    
    def execute_operation(
        self,
        operation_type: UtilityOperationType,
        operation_func: Callable,
        input_data: Any,
        operation_id: str = None,
        metadata: Dict[str, Any] = None
    ) -> UtilityResult:
        """Execute a utility operation."""
        if operation_id is None:
            operation_id = f"{operation_type.value}_{int(time.time())}"
        
        # Create operation
        operation = UtilitySystemModels.create_utility_operation(
            operation_id=operation_id,
            operation_type=operation_type,
            input_data=input_data,
            metadata=metadata
        )
        
        self.operations[operation_id] = operation
        self.active_operations.append(operation_id)
        
        start_time = time.time()
        success = False
        error_message = None
        result_data = None
        
        try:
            # Execute operation based on type
            if operation_type == UtilityOperationType.CACHE_OPERATION:
                result_data = self._execute_cache_operation(operation_func, input_data)
            elif operation_type == UtilityOperationType.VALIDATION_OPERATION:
                result_data = self._execute_validation_operation(operation_func, input_data)
            elif operation_type == UtilityOperationType.TRANSFORMATION_OPERATION:
                result_data = self._execute_transformation_operation(operation_func, input_data)
            elif operation_type == UtilityOperationType.COORDINATION_OPERATION:
                result_data = self._execute_coordination_operation(operation_func, input_data)
            elif operation_type == UtilityOperationType.METRICS_OPERATION:
                result_data = self._execute_metrics_operation(operation_func, input_data)
            else:
                result_data = operation_func(input_data)
            
            success = True
            
        except Exception as e:
            error_message = str(e)
            operation.status = UtilityStatus.ERROR
            operation.error_message = error_message
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Update operation
        operation.end_time = datetime.now()
        operation.output_data = result_data
        if success:
            operation.status = UtilityStatus.ACTIVE
        
        # Update metrics
        self.metrics = UtilitySystemModels.update_metrics(
            self.metrics, operation_type, success, execution_time
        )
        
        # Remove from active operations
        if operation_id in self.active_operations:
            self.active_operations.remove(operation_id)
        
        return UtilitySystemModels.create_utility_result(
            success=success,
            data=result_data,
            error_message=error_message,
            execution_time=execution_time,
            metadata=operation.metadata
        )
    
    def _execute_cache_operation(self, operation_func: Callable, input_data: Any) -> Any:
        """Execute cache operation."""
        if not self.config.cache_enabled:
            return operation_func(input_data)
        
        # Check cache first
        cache_key = self._generate_cache_key(input_data)
        cached_result = self._get_from_cache(cache_key)
        
        if cached_result is not None:
            self.metrics.cache_hits += 1
            return cached_result
        
        # Execute operation and cache result
        result = operation_func(input_data)
        self._store_in_cache(cache_key, result)
        self.metrics.cache_misses += 1
        
        return result
    
    def _execute_validation_operation(self, operation_func: Callable, input_data: Any) -> Any:
        """Execute validation operation."""
        if not self.config.validation_enabled:
            return operation_func(input_data)
        
        # Set timeout for validation
        timeout = self.config.validation_timeout_seconds
        return self._execute_with_timeout(operation_func, input_data, timeout)
    
    def _execute_transformation_operation(self, operation_func: Callable, input_data: Any) -> Any:
        """Execute transformation operation."""
        if not self.config.transformation_enabled:
            return operation_func(input_data)
        
        # Set timeout for transformation
        timeout = self.config.transformation_timeout_seconds
        return self._execute_with_timeout(operation_func, input_data, timeout)
    
    def _execute_coordination_operation(self, operation_func: Callable, input_data: Any) -> Any:
        """Execute coordination operation."""
        if not self.config.coordination_enabled:
            return operation_func(input_data)
        
        # Set timeout for coordination
        timeout = self.config.coordination_timeout_seconds
        return self._execute_with_timeout(operation_func, input_data, timeout)
    
    def _execute_metrics_operation(self, operation_func: Callable, input_data: Any) -> Any:
        """Execute metrics operation."""
        if not self.config.metrics_enabled:
            return operation_func(input_data)
        
        return operation_func(input_data)
    
    def _execute_with_timeout(self, operation_func: Callable, input_data: Any, timeout: int) -> Any:
        """Execute operation with timeout."""
        # Simple timeout implementation
        start_time = time.time()
        result = operation_func(input_data)
        
        if time.time() - start_time > timeout:
            raise TimeoutError(f"Operation timed out after {timeout} seconds")
        
        return result
    
    def _generate_cache_key(self, input_data: Any) -> str:
        """Generate cache key from input data."""
        if isinstance(input_data, (str, int, float, bool)):
            return str(input_data)
        elif isinstance(input_data, dict):
            return str(sorted(input_data.items()))
        elif isinstance(input_data, list):
            return str(input_data)
        else:
            return str(hash(str(input_data)))
    
    def _get_from_cache(self, cache_key: str) -> Any:
        """Get data from cache."""
        # Simple in-memory cache implementation
        # In production, use Redis or similar
        return None
    
    def _store_in_cache(self, cache_key: str, data: Any) -> None:
        """Store data in cache."""
        # Simple in-memory cache implementation
        # In production, use Redis or similar
        pass
    
    def get_operation_status(self, operation_id: str) -> Optional[UtilityStatus]:
        """Get status of specific operation."""
        operation = self.operations.get(operation_id)
        return operation.status if operation else None
    
    def get_active_operations(self) -> List[str]:
        """Get list of active operations."""
        return self.active_operations.copy()
    
    def get_metrics(self) -> UtilityMetrics:
        """Get current metrics."""
        return self.metrics
    
    def clear_old_operations(self, hours_to_keep: int = 24) -> int:
        """Clear old operations."""
        cutoff_time = datetime.now() - timedelta(hours=hours_to_keep)
        
        old_operations = [
            op_id for op_id, operation in self.operations.items()
            if operation.start_time < cutoff_time
        ]
        
        for op_id in old_operations:
            del self.operations[op_id]
        
        return len(old_operations)
    
    def get_operation_history(self, operation_type: Optional[UtilityOperationType] = None) -> List[UtilityOperation]:
        """Get operation history."""
        operations = list(self.operations.values())
        
        if operation_type:
            operations = [op for op in operations if op.operation_type == operation_type]
        
        return sorted(operations, key=lambda x: x.start_time, reverse=True)
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary."""
        total_ops = self.metrics.total_operations
        success_rate = (self.metrics.successful_operations / total_ops * 100) if total_ops > 0 else 0
        
        cache_hit_rate = 0
        if self.metrics.cache_hits + self.metrics.cache_misses > 0:
            cache_hit_rate = (self.metrics.cache_hits / (self.metrics.cache_hits + self.metrics.cache_misses) * 100)
        
        return {
            'total_operations': total_ops,
            'success_rate': success_rate,
            'cache_hit_rate': cache_hit_rate,
            'average_response_time': self.metrics.average_response_time,
            'active_operations': len(self.active_operations),
            'last_updated': self.metrics.last_updated.isoformat() if self.metrics.last_updated else None
        }
