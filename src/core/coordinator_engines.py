#!/usr/bin/env python3
"""
Coordinator Engines - V2 Compliant
=================================

Specialized engines for different aspects of coordination.

Author: Agent-2 - Architecture & Design Specialist
Created: 2025-01-27
Purpose: Modular coordinator system engines
"""

import time
from typing import Any, Dict, List, Optional, Callable
from datetime import datetime

from .coordinator_models import (
    CoordinationTarget, 
    CoordinationResult, 
    CoordinatorStatus,
    CoordinationStatus as Status,
    TargetType,
    Priority
)
from .coordinator_interfaces import (
    ICoordinatorTargetManager,
    ICoordinatorOperationEngine,
    ICoordinatorStatusTracker,
    ICoordinatorConfigManager,
    ICoordinatorLogger
)


class TargetManager(ICoordinatorTargetManager):
    """Manages coordination targets with enhanced functionality."""
    
    def __init__(self, logger: ICoordinatorLogger):
        self.targets: List[CoordinationTarget] = []
        self.logger = logger
    
    def add_target(self, target: CoordinationTarget) -> bool:
        """Add a coordination target."""
        try:
            # Check if target already exists
            existing = self.get_target(target.target_id)
            if existing:
                self.logger.warning(f"Target {target.target_id} already exists, updating")
                return self.update_target(target)
            
            self.targets.append(target)
            self.logger.info(f"Added coordination target: {target.target_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add coordination target {target.target_id}: {e}")
            return False
    
    def get_target(self, target_id: str) -> Optional[CoordinationTarget]:
        """Get coordination target by ID."""
        for target in self.targets:
            if target.target_id == target_id:
                return target
        return None
    
    def update_target(self, target: CoordinationTarget) -> bool:
        """Update coordination target."""
        try:
            for i, existing_target in enumerate(self.targets):
                if existing_target.target_id == target.target_id:
                    target.updated_at = datetime.now()
                    self.targets[i] = target
                    self.logger.info(f"Updated coordination target: {target.target_id}")
                    return True
            
            self.logger.warning(f"Target {target.target_id} not found for update")
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to update coordination target {target.target_id}: {e}")
            return False
    
    def remove_target(self, target_id: str) -> bool:
        """Remove coordination target."""
        try:
            for i, target in enumerate(self.targets):
                if target.target_id == target_id:
                    del self.targets[i]
                    self.logger.info(f"Removed coordination target: {target_id}")
                    return True
            
            self.logger.warning(f"Target {target_id} not found for removal")
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to remove coordination target {target_id}: {e}")
            return False
    
    def get_targets_by_type(self, target_type: str) -> List[CoordinationTarget]:
        """Get targets by type."""
        return [target for target in self.targets if target.target_type.value == target_type]
    
    def get_targets_by_priority(self, min_priority: int) -> List[CoordinationTarget]:
        """Get targets by minimum priority."""
        return [target for target in self.targets if target.priority.value >= min_priority]
    
    def get_all_targets(self) -> List[CoordinationTarget]:
        """Get all targets."""
        return self.targets.copy()
    
    def get_targets_count(self) -> int:
        """Get total targets count."""
        return len(self.targets)


class OperationEngine(ICoordinatorOperationEngine):
    """Executes coordination operations with enhanced error handling."""
    
    def __init__(self, logger: ICoordinatorLogger, status_tracker: ICoordinatorStatusTracker):
        self.logger = logger
        self.status_tracker = status_tracker
    
    def execute_operation(
        self, 
        operation_name: str, 
        operation_func: Callable, 
        *args, 
        **kwargs
    ) -> CoordinationResult:
        """Execute coordination operation."""
        self.status_tracker.update_operation_count()
        
        try:
            self.logger.info(f"Executing coordination operation: {operation_name}")
            
            start_time = time.time()
            result = operation_func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            self.logger.info(f"Coordination operation {operation_name} completed successfully in {execution_time:.2f}s")
            
            return CoordinationResult(
                success=True,
                operation=operation_name,
                result=result,
                timestamp=datetime.now(),
                metadata={"execution_time": execution_time}
            )
            
        except Exception as e:
            self.status_tracker.update_error_count()
            self.logger.error(f"Coordination operation {operation_name} failed: {e}")
            
            return CoordinationResult(
                success=False,
                operation=operation_name,
                error=str(e),
                timestamp=datetime.now()
            )
    
    def execute_with_retry(
        self, 
        operation_name: str, 
        operation_func: Callable, 
        max_retries: int = 3,
        *args, 
        **kwargs
    ) -> CoordinationResult:
        """Execute operation with retry logic."""
        last_error = None
        
        for attempt in range(max_retries + 1):
            result = self.execute_operation(operation_name, operation_func, *args, **kwargs)
            
            if result.success:
                if attempt > 0:
                    result.metadata["retry_attempts"] = attempt
                return result
            
            last_error = result.error
            if attempt < max_retries:
                self.logger.warning(f"Operation {operation_name} failed, retrying ({attempt + 1}/{max_retries})")
                time.sleep(0.1 * (2 ** attempt))  # Exponential backoff
        
        return CoordinationResult(
            success=False,
            operation=operation_name,
            error=f"Operation failed after {max_retries} retries. Last error: {last_error}",
            timestamp=datetime.now(),
            metadata={"retry_attempts": max_retries}
        )
    
    def execute_batch(self, operations: List[Dict[str, Any]]) -> List[CoordinationResult]:
        """Execute multiple operations in batch."""
        results = []
        
        for operation in operations:
            operation_name = operation.get("name", "unknown")
            operation_func = operation.get("func")
            args = operation.get("args", [])
            kwargs = operation.get("kwargs", {})
            
            if operation_func:
                result = self.execute_operation(operation_name, operation_func, *args, **kwargs)
                results.append(result)
            else:
                results.append(CoordinationResult(
                    success=False,
                    operation=operation_name,
                    error="No operation function provided",
                    timestamp=datetime.now()
                ))
        
        return results


class StatusTracker(ICoordinatorStatusTracker):
    """Tracks coordinator status and metrics."""
    
    def __init__(self, name: str, config: Dict[str, Any], logger: ICoordinatorLogger):
        self.name = name
        self.config = config
        self.logger = logger
        self.start_time = datetime.now()
        self.operations_count = 0
        self.error_count = 0
        self.initialized = False
        self.coordination_status = Status.INITIALIZING
    
    def get_status(self) -> CoordinatorStatus:
        """Get comprehensive coordinator status."""
        uptime = (datetime.now() - self.start_time).total_seconds()
        success_rate = self._calculate_success_rate()
        
        return CoordinatorStatus(
            name=self.name,
            initialized=self.initialized,
            coordination_status=self.coordination_status,
            config=self.config,
            start_time=self.start_time,
            uptime_seconds=uptime,
            operations_count=self.operations_count,
            error_count=self.error_count,
            success_rate=success_rate,
            targets_count=0,  # Will be set by coordinator
            targets_by_type={},  # Will be set by coordinator
            status="OPERATIONAL" if self.initialized else "INITIALIZING"
        )
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get coordinator metrics."""
        uptime = (datetime.now() - self.start_time).total_seconds()
        
        return {
            "uptime_seconds": uptime,
            "operations_count": self.operations_count,
            "error_count": self.error_count,
            "success_rate": self._calculate_success_rate(),
            "operations_per_second": self.operations_count / max(uptime, 1),
            "error_rate": self.error_count / max(self.operations_count, 1)
        }
    
    def reset_statistics(self) -> None:
        """Reset coordinator statistics."""
        self.operations_count = 0
        self.error_count = 0
        self.start_time = datetime.now()
        self.logger.info(f"Statistics reset for {self.name}")
    
    def update_operation_count(self) -> None:
        """Update operation count."""
        self.operations_count += 1
    
    def update_error_count(self) -> None:
        """Update error count."""
        self.error_count += 1
    
    def set_initialized(self, initialized: bool) -> None:
        """Set initialization status."""
        self.initialized = initialized
        self.coordination_status = Status.OPERATIONAL if initialized else Status.INITIALIZING
    
    def set_status(self, status: Status) -> None:
        """Set coordination status."""
        self.coordination_status = status
    
    def _calculate_success_rate(self) -> float:
        """Calculate success rate."""
        if self.operations_count == 0:
            return 100.0
        
        successful_operations = self.operations_count - self.error_count
        return (successful_operations / self.operations_count) * 100.0


class ConfigManager(ICoordinatorConfigManager):
    """Manages coordinator configuration."""
    
    def __init__(self, config: Dict[str, Any], logger: ICoordinatorLogger):
        self.config = config.copy()
        self.logger = logger
    
    def get_config_value(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config.get(key, default)
    
    def update_config(self, updates: Dict[str, Any]) -> bool:
        """Update configuration."""
        try:
            self.config.update(updates)
            self.logger.info("Configuration updated successfully")
            return True
        except Exception as e:
            self.logger.error(f"Configuration update failed: {e}")
            return False
    
    def validate_config(self) -> bool:
        """Validate configuration."""
        try:
            # Basic validation - can be extended
            return isinstance(self.config, dict)
        except Exception as e:
            self.logger.error(f"Configuration validation failed: {e}")
            return False
    
    def reload_config(self) -> bool:
        """Reload configuration from source."""
        # This would typically reload from a file or external source
        # For now, just validate current config
        return self.validate_config()
