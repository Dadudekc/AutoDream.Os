#!/usr/bin/env python3
"""
Utility Coordinator - V2 Compliance Module
=========================================

Main coordinator for utility system operations.

Author: Agent-5 - Business Intelligence Specialist
License: MIT
"""

import time
from typing import Any, Dict, List, Optional, Union
from pathlib import Path

from ..managers.file_manager import FileManager, FileOperationConfig
from ..managers.string_manager import StringManager, StringOperationConfig
from ..managers.path_manager import PathManager, PathOperationConfig
from ..utility_system_models import UtilityConfig, UtilityMetrics, UtilityOperationType


class UtilityCoordinator:
    """Main coordinator for utility system operations."""

    def __init__(self, config: UtilityConfig = None):
        """Initialize utility coordinator."""
        self.config = config or UtilityConfig()
        
        # Initialize managers
        self.file_manager = FileManager(FileOperationConfig(
            enable_caching=self.config.cache_enabled,
            cache_ttl_seconds=300,
            max_file_size_mb=self.config.max_file_size_mb,
            backup_before_write=self.config.backup_enabled
        ))
        
        self.string_manager = StringManager(StringOperationConfig(
            enable_caching=self.config.cache_enabled,
            cache_ttl_seconds=300,
            max_string_length=10000,
            enable_validation=self.config.validation_enabled
        ))
        
        self.path_manager = PathManager(PathOperationConfig(
            enable_validation=self.config.validation_enabled,
            cross_platform=True,
            max_path_length=260
        ))
        
        self.metrics = UtilityMetrics()

    def execute_file_operation(self, operation_type: str, **kwargs) -> Any:
        """Execute file operation through coordinator."""
        start_time = time.time()
        
        try:
            if operation_type == "read":
                result = self.file_manager.read_file(kwargs["file_path"], kwargs.get("encoding", "utf-8"))
            elif operation_type == "write":
                result = self.file_manager.write_file(kwargs["file_path"], kwargs["content"], kwargs.get("encoding", "utf-8"))
            elif operation_type == "copy":
                result = self.file_manager.copy_file(kwargs["source"], kwargs["destination"])
            elif operation_type == "move":
                result = self.file_manager.move_file(kwargs["source"], kwargs["destination"])
            elif operation_type == "delete":
                result = self.file_manager.delete_file(kwargs["file_path"])
            elif operation_type == "backup":
                result = self.file_manager.backup_file(kwargs["file_path"])
            elif operation_type == "restore":
                result = self.file_manager.restore_file(kwargs["backup_path"], kwargs["target_path"])
            else:
                raise ValueError(f"Unknown file operation: {operation_type}")
            
            execution_time = (time.time() - start_time) * 1000
            self._update_metrics(UtilityOperationType.FILE_OPERATION, True, execution_time)
            return result
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            self._update_metrics(UtilityOperationType.FILE_OPERATION, False, execution_time)
            raise e

    def execute_string_operation(self, operation_type: str, **kwargs) -> Any:
        """Execute string operation through coordinator."""
        start_time = time.time()
        
        try:
            if operation_type == "format":
                result = self.string_manager.format_string(kwargs["template"], **kwargs.get("kwargs", {}))
            elif operation_type == "sanitize":
                result = self.string_manager.sanitize_string(
                    kwargs["text"], 
                    kwargs.get("remove_special", True), 
                    kwargs.get("normalize_whitespace", True)
                )
            elif operation_type == "validate":
                result = self.string_manager.validate_string(
                    kwargs["text"],
                    kwargs.get("min_length", 0),
                    kwargs.get("max_length", 1000),
                    kwargs.get("allow_empty", True)
                )
            elif operation_type == "transform":
                result = self.string_manager.transform_data(
                    kwargs["data"], 
                    kwargs["transformation_type"], 
                    **kwargs.get("kwargs", {})
                )
            elif operation_type == "parse_json":
                result = self.string_manager.parse_json(kwargs["json_string"], **kwargs.get("kwargs", {}))
            elif operation_type == "stringify_json":
                result = self.string_manager.stringify_json(kwargs["data"], **kwargs.get("kwargs", {}))
            else:
                raise ValueError(f"Unknown string operation: {operation_type}")
            
            execution_time = (time.time() - start_time) * 1000
            self._update_metrics(UtilityOperationType.STRING_MANIPULATION, True, execution_time)
            return result
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            self._update_metrics(UtilityOperationType.STRING_MANIPULATION, False, execution_time)
            raise e

    def execute_path_operation(self, operation_type: str, **kwargs) -> Any:
        """Execute path operation through coordinator."""
        start_time = time.time()
        
        try:
            if operation_type == "resolve":
                result = self.path_manager.resolve_path(kwargs["path"])
            elif operation_type == "normalize":
                result = self.path_manager.normalize_path(kwargs["path"])
            elif operation_type == "relative":
                result = self.path_manager.get_relative_path(kwargs["file_path"], kwargs.get("base_path"))
            elif operation_type == "extension":
                result = self.path_manager.get_file_extension(kwargs["file_path"])
            elif operation_type == "exists":
                result = self.path_manager.path_exists(kwargs["path"])
            elif operation_type == "create":
                result = self.path_manager.create_directory(kwargs["dir_path"])
            else:
                raise ValueError(f"Unknown path operation: {operation_type}")
            
            execution_time = (time.time() - start_time) * 1000
            self._update_metrics(UtilityOperationType.PATH_RESOLUTION, True, execution_time)
            return result
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            self._update_metrics(UtilityOperationType.PATH_RESOLUTION, False, execution_time)
            raise e

    def execute_batch_operations(self, operations: List[Dict[str, Any]]) -> List[Any]:
        """Execute batch operations across all managers."""
        results = []
        
        for operation in operations:
            try:
                op_type = operation.get("type")
                manager_type = operation.get("manager", "file")
                
                if manager_type == "file":
                    result = self.execute_file_operation(op_type, **operation.get("params", {}))
                elif manager_type == "string":
                    result = self.execute_string_operation(op_type, **operation.get("params", {}))
                elif manager_type == "path":
                    result = self.execute_path_operation(op_type, **operation.get("params", {}))
                else:
                    result = None
                
                results.append(result)
                
            except Exception as e:
                results.append(f"Error: {str(e)}")
        
        return results

    def get_metrics(self) -> UtilityMetrics:
        """Get utility system metrics."""
        return self.metrics

    def reset_metrics(self) -> None:
        """Reset metrics."""
        self.metrics = UtilityMetrics()

    def _update_metrics(self, operation_type: UtilityOperationType, success: bool, execution_time: float) -> None:
        """Update metrics."""
        self.metrics.total_operations += 1
        
        if success:
            self.metrics.successful_operations += 1
        else:
            self.metrics.failed_operations += 1
        
        self.metrics.total_execution_time_ms += execution_time
        self.metrics.average_execution_time_ms = (
            self.metrics.total_execution_time_ms / self.metrics.total_operations
        )
        
        op_type_str = operation_type.value
        if op_type_str not in self.metrics.operations_by_type:
            self.metrics.operations_by_type[op_type_str] = 0
        self.metrics.operations_by_type[op_type_str] += 1
        
        if not success:
            if op_type_str not in self.metrics.error_count_by_type:
                self.metrics.error_count_by_type[op_type_str] = 0
            self.metrics.error_count_by_type[op_type_str] += 1
