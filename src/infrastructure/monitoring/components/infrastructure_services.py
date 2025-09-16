#!/usr/bin/env python3
"""
Infrastructure Services Monitoring

This module provides monitoring for infrastructure services including:
- File system monitoring
- Logging system monitoring
- Configuration management monitoring
"""

from __future__ import annotations

import logging
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

from ...logging.unified_logging_system import get_unified_logger
from ...utils.consolidated_config_management import UnifiedConfigurationManager
from ...utils.consolidated_file_operations import (
    DirectoryOperations,
    FileMetadataOperations,
    SerializationOperations,
)

logger = get_unified_logger(__name__)


class InfrastructureServices:
    """
    Infrastructure services monitoring and management.

    Monitors file system health, logging system performance,
    and configuration management status.
    """

    def __init__(self):
        """Initialize infrastructure services monitoring."""
        self.logger = logging.getLogger(__name__)
        self.config_manager = UnifiedConfigurationManager()
        self.file_ops = FileMetadataOperations()
        self.dir_ops = DirectoryOperations()
        self.serialization_ops = SerializationOperations()

    def monitor_file_system(self) -> dict[str, Any]:
        """Monitor file system health and usage."""
        try:
            # Get disk usage
            disk_usage = shutil.disk_usage("/")
            total_gb = disk_usage.total / (1024**3)
            used_gb = disk_usage.used / (1024**3)
            free_gb = disk_usage.free / (1024**3)
            usage_percent = (used_gb / total_gb) * 100

            # Check critical directories
            critical_dirs = ["src/", "config/", "runtime/", "agent_workspaces/", "logs/"]

            dir_status = {}
            for dir_path in critical_dirs:
                if os.path.exists(dir_path):
                    try:
                        dir_size = self._get_directory_size(dir_path)
                        dir_status[dir_path] = {
                            "exists": True,
                            "size_mb": dir_size / (1024**2),
                            "accessible": True,
                        }
                    except Exception as e:
                        dir_status[dir_path] = {
                            "exists": True,
                            "size_mb": 0,
                            "accessible": False,
                            "error": str(e),
                        }
                else:
                    dir_status[dir_path] = {"exists": False, "size_mb": 0, "accessible": False}

            return {
                "disk_usage": {
                    "total_gb": round(total_gb, 2),
                    "used_gb": round(used_gb, 2),
                    "free_gb": round(free_gb, 2),
                    "usage_percent": round(usage_percent, 2),
                },
                "directories": dir_status,
                "status": (
                    "healthy"
                    if usage_percent < 90
                    else "warning"
                    if usage_percent < 95
                    else "critical"
                ),
            }

        except Exception as e:
            self.logger.error(f"Failed to monitor file system: {e}")
            return {"status": "error", "error": str(e)}

    def monitor_logging_system(self) -> dict[str, Any]:
        """Monitor logging system performance."""
        try:
            # Check log directory
            log_dir = Path("runtime/agent_logs")
            log_files = []
            total_log_size = 0

            if log_dir.exists():
                for log_file in log_dir.glob("*.log*"):
                    try:
                        file_size = log_file.stat().st_size
                        total_log_size += file_size
                        log_files.append(
                            {
                                "name": log_file.name,
                                "size_mb": round(file_size / (1024**2), 2),
                                "modified": datetime.fromtimestamp(
                                    log_file.stat().st_mtime
                                ).isoformat(),
                            }
                        )
                    except Exception as e:
                        log_files.append({"name": log_file.name, "size_mb": 0, "error": str(e)})

            # Check for log rotation needs
            needs_rotation = any(
                file_info.get("size_mb", 0) > 100  # Files larger than 100MB
                for file_info in log_files
            )

            return {
                "log_directory": str(log_dir),
                "log_files": log_files,
                "total_size_mb": round(total_log_size / (1024**2), 2),
                "file_count": len(log_files),
                "needs_rotation": needs_rotation,
                "status": "healthy" if not needs_rotation else "warning",
            }

        except Exception as e:
            self.logger.error(f"Failed to monitor logging system: {e}")
            return {"status": "error", "error": str(e)}

    def monitor_configuration_system(self) -> dict[str, Any]:
        """Monitor configuration management system."""
        try:
            # Check configuration files
            config_files = []
            config_dir = Path("config")

            if config_dir.exists():
                for config_file in config_dir.glob("*.yaml"):
                    try:
                        file_size = config_file.stat().st_size
                        modified_time = datetime.fromtimestamp(config_file.stat().st_mtime)
                        config_files.append(
                            {
                                "name": config_file.name,
                                "size_kb": round(file_size / 1024, 2),
                                "modified": modified_time.isoformat(),
                                "age_hours": (datetime.now() - modified_time).total_seconds()
                                / 3600,
                            }
                        )
                    except Exception as e:
                        config_files.append({"name": config_file.name, "error": str(e)})

            # Check configuration validation
            validation_status = "unknown"
            try:
                # Attempt to load configuration
                self.config_manager.load_config()
                validation_status = "valid"
            except Exception as e:
                validation_status = f"invalid: {str(e)}"

            return {
                "config_directory": str(config_dir),
                "config_files": config_files,
                "file_count": len(config_files),
                "validation_status": validation_status,
                "status": "healthy" if validation_status == "valid" else "warning",
            }

        except Exception as e:
            self.logger.error(f"Failed to monitor configuration system: {e}")
            return {"status": "error", "error": str(e)}

    def _get_directory_size(self, directory: str) -> int:
        """Get total size of directory in bytes."""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    try:
                        total_size += os.path.getsize(filepath)
                    except (OSError, FileNotFoundError):
                        continue
        except Exception:
            pass
        return total_size

    def get_infrastructure_status(self) -> dict[str, Any]:
        """Get overall infrastructure status."""
        return {
            "file_system": self.monitor_file_system(),
            "logging_system": self.monitor_logging_system(),
            "configuration_system": self.monitor_configuration_system(),
            "timestamp": datetime.now().isoformat(),
        }

