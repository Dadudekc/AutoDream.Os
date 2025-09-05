#!/usr/bin/env python3
"""
Utility Factory - V2 Compliance Module
=====================================

Factory pattern for creating utility instances.

Author: Agent-5 - Business Intelligence Specialist
License: MIT
"""

from typing import Any, Dict, Optional, Type
from enum import Enum

from ..utility_system_models import UtilityConfig
from ..managers.file_manager import FileManager, FileOperationConfig
from ..managers.string_manager import StringManager, StringOperationConfig
from ..managers.path_manager import PathManager, PathOperationConfig
from ..coordinators.utility_coordinator import UtilityCoordinator


class UtilityType(Enum):
    """Types of utility instances."""
    FILE_MANAGER = "file_manager"
    STRING_MANAGER = "string_manager"
    PATH_MANAGER = "path_manager"
    COORDINATOR = "coordinator"


class UtilityFactory:
    """Factory for creating utility instances."""

    _instances: Dict[str, Any] = {}
    _config: Optional[UtilityConfig] = None

    @classmethod
    def set_config(cls, config: UtilityConfig) -> None:
        """Set global configuration."""
        cls._config = config

    @classmethod
    def get_file_manager(cls, config: FileOperationConfig = None) -> FileManager:
        """Get file manager instance."""
        key = "file_manager"
        if key not in cls._instances:
            cls._instances[key] = FileManager(config)
        return cls._instances[key]

    @classmethod
    def get_string_manager(cls, config: StringOperationConfig = None) -> StringManager:
        """Get string manager instance."""
        key = "string_manager"
        if key not in cls._instances:
            cls._instances[key] = StringManager(config)
        return cls._instances[key]

    @classmethod
    def get_path_manager(cls, config: PathOperationConfig = None) -> PathManager:
        """Get path manager instance."""
        key = "path_manager"
        if key not in cls._instances:
            cls._instances[key] = PathManager(config)
        return cls._instances[key]

    @classmethod
    def get_coordinator(cls, config: UtilityConfig = None) -> UtilityCoordinator:
        """Get coordinator instance."""
        key = "coordinator"
        if key not in cls._instances:
            cls._instances[key] = UtilityCoordinator(config or cls._config)
        return cls._instances[key]

    @classmethod
    def create_manager(cls, manager_type: UtilityType, **kwargs) -> Any:
        """Create manager instance by type."""
        if manager_type == UtilityType.FILE_MANAGER:
            return cls.get_file_manager(kwargs.get("config"))
        elif manager_type == UtilityType.STRING_MANAGER:
            return cls.get_string_manager(kwargs.get("config"))
        elif manager_type == UtilityType.PATH_MANAGER:
            return cls.get_path_manager(kwargs.get("config"))
        elif manager_type == UtilityType.COORDINATOR:
            return cls.get_coordinator(kwargs.get("config"))
        else:
            raise ValueError(f"Unknown manager type: {manager_type}")

    @classmethod
    def reset_instances(cls) -> None:
        """Reset all instances."""
        cls._instances.clear()

    @classmethod
    def get_instance_count(cls) -> int:
        """Get number of created instances."""
        return len(cls._instances)

    @classmethod
    def get_instance_info(cls) -> Dict[str, str]:
        """Get information about created instances."""
        return {
            key: type(instance).__name__ 
            for key, instance in cls._instances.items()
        }
