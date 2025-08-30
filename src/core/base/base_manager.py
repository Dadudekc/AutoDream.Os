"""
Unified Base Manager Class

This class consolidates functionality from 8 duplicate manager.py files:
- Task management
- Workflow management  
- Performance management
- Validation management
- Resource management
- Status management

Eliminates duplication and provides unified patterns for all manager classes.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
import logging
import time
from pathlib import Path


class ManagerState(Enum):
    """Unified manager state enumeration."""
    INITIALIZING = "initializing"
    ACTIVE = "active"
    PAUSED = "paused"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"
    MAINTENANCE = "maintenance"


class ManagerType(Enum):
    """Unified manager type enumeration."""
    TASK = "task"
    WORKFLOW = "workflow"
    PERFORMANCE = "performance"
    VALIDATION = "validation"
    RESOURCE = "resource"
    STATUS = "status"
    CUSTOM = "custom"


@dataclass
class ManagerConfig:
    """Unified configuration for all manager types."""
    name: str
    manager_type: ManagerType
    enabled: bool = True
    max_workers: int = 4
    timeout: float = 30.0
    retry_attempts: int = 3
    log_level: str = "INFO"
    config_path: Optional[Path] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ManagerMetrics:
    """Unified metrics for all manager types."""
    start_time: float = field(default_factory=time.time)
    total_operations: int = 0
    successful_operations: int = 0
    failed_operations: int = 0
    active_workers: int = 0
    memory_usage: float = 0.0
    cpu_usage: float = 0.0
    last_operation_time: float = 0.0


class BaseManager(ABC):
    """
    Unified base class for all manager types.
    
    Consolidates functionality from duplicate manager implementations:
    - src/core/performance/alerts/manager.py
    - src/core/smooth_handoff/manager.py
    - src/core/data_sources/manager.py
    - src/autonomous_development/tasks/manager.py
    - src/autonomous_development/workflow/manager.py
    - src/autonomous_development/reporting/manager.py
    - config/manager.py
    - config_backup/manager.py
    """
    
    def __init__(self, config: ManagerConfig):
        """
        Initialize the unified base manager.
        
        Args:
            config: Manager configuration object
        """
        self.config = config
        self.state = ManagerState.INITIALIZING
        self.metrics = ManagerMetrics()
        self.logger = self._setup_logging()
        self.workers: List[Any] = []
        self._initialize()
    
    def _setup_logging(self) -> logging.Logger:
        """Set up unified logging for all manager types."""
        logger = logging.getLogger(f"{self.__class__.__name__}.{self.config.name}")
        logger.setLevel(getattr(logging, self.config.log_level.upper()))
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _initialize(self) -> None:
        """Initialize manager-specific components."""
        try:
            self.logger.info(f"Initializing {self.config.manager_type.value} manager: {self.config.name}")
            
            # Load configuration if path provided
            if self.config.config_path and self.config.config_path.exists():
                self._load_config()
            
            # Initialize manager-specific resources
            self._initialize_resources()
            
            # Validate configuration
            self._validate_config()
            
            self.state = ManagerState.ACTIVE
            self.logger.info(f"Manager {self.config.name} initialized successfully")
            
        except Exception as e:
            self.state = ManagerState.ERROR
            self.logger.error(f"Failed to initialize manager {self.config.name}: {e}")
            raise
    
    @abstractmethod
    def _initialize_resources(self) -> None:
        """Initialize manager-specific resources. Must be implemented by subclasses."""
        pass
    
    def _load_config(self) -> None:
        """Load configuration from file if specified."""
        try:
            # This would be implemented based on config file format
            self.logger.debug(f"Loading configuration from {self.config.config_path}")
            # Implementation depends on config format (JSON, YAML, etc.)
        except Exception as e:
            self.logger.warning(f"Failed to load config from {self.config.config_path}: {e}")
    
    def _validate_config(self) -> None:
        """Validate manager configuration."""
        if not self.config.name:
            raise ValueError("Manager name is required")
        
        if self.config.max_workers < 1:
            raise ValueError("max_workers must be at least 1")
        
        if self.config.timeout <= 0:
            raise ValueError("timeout must be positive")
        
        if self.config.retry_attempts < 0:
            raise ValueError("retry_attempts must be non-negative")
    
    def start(self) -> bool:
        """Start the manager."""
        if self.state != ManagerState.ACTIVE:
            try:
                self.logger.info(f"Starting manager {self.config.name}")
                self._start_workers()
                self.state = ManagerState.ACTIVE
                self.logger.info(f"Manager {self.config.name} started successfully")
                return True
            except Exception as e:
                self.state = ManagerState.ERROR
                self.logger.error(f"Failed to start manager {self.config.name}: {e}")
                return False
        return True
    
    def stop(self) -> bool:
        """Stop the manager."""
        if self.state != ManagerState.STOPPED:
            try:
                self.logger.info(f"Stopping manager {self.config.name}")
                self.state = ManagerState.STOPPING
                self._stop_workers()
                self.state = ManagerState.STOPPED
                self.logger.info(f"Manager {self.config.name} stopped successfully")
                return True
            except Exception as e:
                self.state = ManagerState.ERROR
                self.logger.error(f"Failed to stop manager {self.config.name}: {e}")
                return False
        return True
    
    def pause(self) -> bool:
        """Pause the manager."""
        if self.state == ManagerState.ACTIVE:
            try:
                self.logger.info(f"Pausing manager {self.config.name}")
                self.state = ManagerState.PAUSED
                self._pause_workers()
                self.logger.info(f"Manager {self.config.name} paused successfully")
                return True
            except Exception as e:
                self.logger.error(f"Failed to pause manager {self.config.name}: {e}")
                return False
        return False
    
    def resume(self) -> bool:
        """Resume the manager."""
        if self.state == ManagerState.PAUSED:
            try:
                self.logger.info(f"Resuming manager {self.config.name}")
                self.state = ManagerState.ACTIVE
                self._resume_workers()
                self.logger.info(f"Manager {self.config.name} resumed successfully")
                return True
            except Exception as e:
                self.logger.error(f"Failed to resume manager {self.config.name}: {e}")
                return False
        return False
    
    def _start_workers(self) -> None:
        """Start manager workers."""
        self.logger.debug(f"Starting {self.config.max_workers} workers")
        # Implementation depends on manager type
    
    def _stop_workers(self) -> None:
        """Stop manager workers."""
        self.logger.debug("Stopping all workers")
        # Implementation depends on manager type
    
    def _pause_workers(self) -> None:
        """Pause manager workers."""
        self.logger.debug("Pausing all workers")
        # Implementation depends on manager type
    
    def _resume_workers(self) -> None:
        """Resume manager workers."""
        self.logger.debug("Resuming all workers")
        # Implementation depends on manager type
    
    def get_status(self) -> Dict[str, Any]:
        """Get unified manager status."""
        return {
            'name': self.config.name,
            'type': self.config.manager_type.value,
            'state': self.state.value,
            'enabled': self.config.enabled,
            'metrics': {
                'uptime': time.time() - self.metrics.start_time,
                'total_operations': self.metrics.total_operations,
                'successful_operations': self.metrics.successful_operations,
                'failed_operations': self.metrics.failed_operations,
                'active_workers': self.metrics.active_workers,
                'memory_usage': self.metrics.memory_usage,
                'cpu_usage': self.metrics.cpu_usage,
                'last_operation_time': self.metrics.last_operation_time
            },
            'config': {
                'max_workers': self.config.max_workers,
                'timeout': self.config.timeout,
                'retry_attempts': self.config.retry_attempts,
                'log_level': self.config.log_level
            }
        }
    
    def update_metrics(self, operation_success: bool = True) -> None:
        """Update manager metrics."""
        self.metrics.total_operations += 1
        if operation_success:
            self.metrics.successful_operations += 1
        else:
            self.metrics.failed_operations += 1
        self.metrics.last_operation_time = time.time()
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get manager health status."""
        return {
            'healthy': self.state in [ManagerState.ACTIVE, ManagerState.PAUSED],
            'state': self.state.value,
            'error_count': self.metrics.failed_operations,
            'success_rate': (
                self.metrics.successful_operations / max(self.metrics.total_operations, 1)
            ),
            'uptime': time.time() - self.metrics.start_time
        }
    
    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()
    
    def __repr__(self) -> str:
        """String representation."""
        return f"{self.__class__.__name__}(name='{self.config.name}', type='{self.config.manager_type.value}', state='{self.state.value}')"
