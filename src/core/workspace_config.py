from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
import json
import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from .base_manager import BaseManager


class WorkspaceType(Enum):
    """Types of agent workspaces."""

    AGENT = "agent"
    COORDINATION = "coordination"
    SHARED = "shared"
    ISOLATED = "isolated"
    TEMPORARY = "temporary"


class WorkspaceStatus(Enum):
    """Workspace lifecycle states."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    ARCHIVED = "archived"
    ERROR = "error"


@dataclass
class WorkspaceConfig:
    """Configuration persisted for a workspace."""

    name: str
    workspace_type: WorkspaceType
    base_path: str
    permissions: List[str]
    isolation_level: str
    max_size_mb: int
    auto_cleanup: bool
    backup_enabled: bool


@dataclass
class WorkspaceInfo:
    """Runtime information about a workspace."""

    name: str
    workspace_type: WorkspaceType
    status: WorkspaceStatus
    path: str
    size_mb: float
    created_at: str
    last_accessed: str
    agent_count: int
    resource_usage: Dict[str, Any]
    # Agent specific paths for backwards compatibility
    inbox_path: Optional[str] = None
    tasks_path: Optional[str] = None
    responses_path: Optional[str] = None
    agent_id: Optional[str] = None


class WorkspaceConfigManager(BaseManager):
    """Handles persistence of workspace configuration.
    
    Now inherits from BaseManager for unified functionality
    """

    def __init__(self, base_workspace_dir: Path):
        super().__init__(
            manager_id="workspace_config_manager",
            name="Workspace Config Manager",
            description="Handles persistence of workspace configuration"
        )
        
        self.base_workspace_dir = base_workspace_dir
        
        # Workspace configuration tracking
        self.config_operations: List[Dict[str, Any]] = []
        self.saved_configs_count = 0
        self.loaded_configs_count = 0
        self.failed_operations: List[Dict[str, Any]] = []
        
        self.logger.info("Workspace Config Manager initialized")

    def save_workspace_config(self, name: str, config: WorkspaceConfig) -> bool:
        """Persist workspace configuration to disk."""
        start_time = time.time()
        try:
            config_file = self.base_workspace_dir / name / "workspace_config.json"
            with open(config_file, "w") as f:
                json.dump(asdict(config), f, indent=2, default=str)
            
            # Record successful operation
            self.saved_configs_count += 1
            self.record_operation("save_workspace_config", True, time.time() - start_time)
            
            return True
        except Exception as e:  # pragma: no cover - logging protection
            self.logger.error(f"Failed to save workspace config for {name}: {e}")
            self.record_operation("save_workspace_config", False, time.time() - start_time)
            self.failed_operations.append({
                "operation": "save_workspace_config",
                "workspace_name": name,
                "error": str(e),
                "timestamp": time.time()
            })
            return False

    def load_workspace_config(self, name: str) -> Optional[WorkspaceConfig]:
        """Load configuration from disk if available."""
        start_time = time.time()
        try:
            config_file = self.base_workspace_dir / name / "workspace_config.json"
            if config_file.exists():
                with open(config_file, "r") as f:
                    data = json.load(f)
                data["workspace_type"] = WorkspaceType(data["workspace_type"])
                config = WorkspaceConfig(**data)
                
                # Record successful operation
                self.loaded_configs_count += 1
                self.record_operation("load_workspace_config", True, time.time() - start_time)
                
                return config
            
            # Record failed operation (config not found)
            self.record_operation("load_workspace_config", False, time.time() - start_time)
            return None
        except Exception as e:  # pragma: no cover - logging protection
            self.logger.error(f"Failed to load workspace config for {name}: {e}")
            self.record_operation("load_workspace_config", False, time.time() - start_time)
            self.failed_operations.append({
                "operation": "load_workspace_config",
                "workspace_name": name,
                "error": str(e),
                "timestamp": time.time()
            })
            return None

    @staticmethod
    def get_current_timestamp() -> str:
        """Return current timestamp string."""
        from datetime import datetime

        return datetime.now().isoformat()

    # ============================================================================
    # BaseManager Abstract Method Implementations
    # ============================================================================
    
    def _on_start(self) -> bool:
        """Initialize workspace configuration system"""
        try:
            self.logger.info("Starting Workspace Config Manager...")
            
            # Clear tracking data
            self.config_operations.clear()
            self.saved_configs_count = 0
            self.loaded_configs_count = 0
            self.failed_operations.clear()
            
            self.logger.info("Workspace Config Manager started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start Workspace Config Manager: {e}")
            return False
    
    def _on_stop(self) -> bool:
        """Cleanup workspace configuration system"""
        try:
            self.logger.info("Stopping Workspace Config Manager...")
            
            # Save workspace configuration data
            self._save_workspace_config_data()
            
            self.logger.info("Workspace Config Manager stopped successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to stop Workspace Config Manager: {e}")
            return False
    
    def _on_heartbeat(self) -> bool:
        """Workspace configuration health check"""
        try:
            # Check workspace configuration health
            health_status = self._check_workspace_config_health()
            
            # Update metrics
            self.metrics.update(
                operations_count=len(self.config_operations),
                success_rate=self._calculate_success_rate(),
                average_response_time=self._calculate_average_response_time(),
                health_status=health_status
            )
            
            return health_status == "healthy"
            
        except Exception as e:
            self.logger.error(f"Workspace Config Manager heartbeat failed: {e}")
            return False
    
    def _on_initialize_resources(self) -> bool:
        """Initialize workspace configuration resources"""
        try:
            # Ensure base workspace directory exists
            self.base_workspace_dir.mkdir(parents=True, exist_ok=True)
            
            # Initialize configuration tracking
            self.config_operations = []
            self.saved_configs_count = 0
            self.loaded_configs_count = 0
            self.failed_operations = []
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Workspace Config Manager resources: {e}")
            return False
    
    def _on_cleanup_resources(self) -> bool:
        """Cleanup workspace configuration resources"""
        try:
            # Save workspace configuration data
            self._save_workspace_config_data()
            
            # Clear tracking data
            self.config_operations.clear()
            self.saved_configs_count = 0
            self.loaded_configs_count = 0
            self.failed_operations.clear()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup Workspace Config Manager resources: {e}")
            return False
    
    def _on_recovery_attempt(self) -> bool:
        """Attempt to recover from errors"""
        try:
            self.logger.info("Attempting Workspace Config Manager recovery...")
            
            # Reinitialize base workspace directory
            try:
                self.base_workspace_dir.mkdir(parents=True, exist_ok=True)
                self.logger.info("Workspace Config Manager recovery successful")
                return True
            except Exception as e:
                self.logger.error(f"Failed to recreate base workspace directory: {e}")
                return False
                
        except Exception as e:
            self.logger.error(f"Workspace Config Manager recovery attempt failed: {e}")
            return False
    
    # ============================================================================
    # Private Helper Methods
    # ============================================================================
    
    def _save_workspace_config_data(self):
        """Save workspace configuration data for persistence"""
        try:
            data = {
                "saved_configs_count": self.saved_configs_count,
                "loaded_configs_count": self.loaded_configs_count,
                "failed_operations": self.failed_operations,
                "timestamp": time.time()
            }
            
            # Save to file or database as needed
            # For now, just log the data
            self.logger.info(f"Workspace configuration data: {data}")
            
        except Exception as e:
            self.logger.error(f"Failed to save workspace configuration data: {e}")
    
    def _check_workspace_config_health(self) -> str:
        """Check workspace configuration system health"""
        try:
            # Check if base workspace directory is accessible
            if self.base_workspace_dir.exists() and self.base_workspace_dir.is_dir():
                # Check if we have recent operations
                if len(self.config_operations) > 0:
                    return "healthy"
                else:
                    return "idle"
            else:
                return "unhealthy"
                
        except Exception as e:
            self.logger.error(f"Workspace configuration health check failed: {e}")
            return "unhealthy"
    
    def _calculate_success_rate(self) -> float:
        """Calculate operation success rate"""
        try:
            if len(self.config_operations) == 0:
                return 1.0
            
            successful_ops = sum(1 for op in self.config_operations if op.get("success", False))
            return successful_ops / len(self.config_operations)
            
        except Exception as e:
            self.logger.error(f"Failed to calculate success rate: {e}")
            return 0.0
    
    def _calculate_average_response_time(self) -> float:
        """Calculate average operation response time"""
        try:
            if len(self.config_operations) == 0:
                return 0.0
            
            total_time = sum(op.get("duration", 0.0) for op in self.config_operations)
            return total_time / len(self.config_operations)
            
        except Exception as e:
            self.logger.error(f"Failed to calculate average response time: {e}")
            return 0.0


__all__ = [
    "WorkspaceType",
    "WorkspaceStatus",
    "WorkspaceConfig",
    "WorkspaceInfo",
    "WorkspaceConfigManager",
]
