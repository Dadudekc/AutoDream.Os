<<<<<<< HEAD
"""
Core Managers - Phase-2 Manager Consolidation
============================================

Exports all core manager interfaces and implementations.
Consolidates 16+ managers into 5 core managers following SOLID principles.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

from .contracts import (
    Manager,
    ManagerContext,
    ManagerResult,
    ResourceManager,
    ConfigurationManager,
    ExecutionManager,
    MonitoringManager,
    ServiceManager,
    MANAGER_TYPES,
)

from .registry import ManagerRegistry, get_manager_registry, create_manager_registry

from .core_resource_manager import CoreResourceManager
from .core_configuration_manager import CoreConfigurationManager
from .core_execution_manager import CoreExecutionManager
from .execution import (
    BaseExecutionManager,
    TaskManager,
    ProtocolManager,
    ExecutionCoordinator,
)
from .core_monitoring_manager import CoreMonitoringManager
from .core_service_manager import CoreServiceManager
from .core_onboarding_manager import CoreOnboardingManager
from .core_recovery_manager import CoreRecoveryManager
from .core_results_manager import CoreResultsManager
from .results import (
    BaseResultsManager,
    ValidationResultsProcessor,
    AnalysisResultsProcessor,
    IntegrationResultsProcessor,
    PerformanceResultsProcessor,
    GeneralResultsProcessor,
    ResultsArchiveManager,
)
from .core_service_coordinator import CoreServiceCoordinator

from .adapters.legacy_manager_adapter import (
    LegacyManagerAdapter,
    create_legacy_manager_adapter,
)

__all__ = [
    # Contracts
    "Manager",
    "ManagerContext",
    "ManagerResult",
    "ResourceManager",
    "ConfigurationManager",
    "ExecutionManager",
    "MonitoringManager",
    "ServiceManager",
    "MANAGER_TYPES",
    # Registry
    "ManagerRegistry",
    "get_manager_registry",
    "create_manager_registry",
    # Core Managers
    "CoreResourceManager",
    "CoreConfigurationManager",
    "CoreExecutionManager",
    # Execution Components
    "BaseExecutionManager",
    "TaskManager",
    "ProtocolManager",
    "ExecutionCoordinator",
    "CoreMonitoringManager",
    "CoreServiceManager",
    # Specialized Service Managers
    "CoreOnboardingManager",
    "CoreRecoveryManager",
    "CoreResultsManager",
    # Results Processors
    "BaseResultsManager",
    "ValidationResultsProcessor",
    "AnalysisResultsProcessor",
    "IntegrationResultsProcessor",
    "PerformanceResultsProcessor",
    "GeneralResultsProcessor",
    "ResultsArchiveManager",
    "CoreServiceCoordinator",
    # Legacy Adapters
    "LegacyManagerAdapter",
    "create_legacy_manager_adapter",
=======
#!/usr/bin/env python3
"""Base Manager Package - Agent Cellphone V2"""

from .base_manager_types import (
    ManagerStatus, ManagerPriority, ManagerMetrics, ManagerConfig
)
from .base_manager_interface import BaseManagerInterface
from .base_manager_lifecycle import BaseManagerLifecycle
from .base_manager_monitoring import BaseManagerMonitoring
from .base_manager_config import BaseManagerConfiguration
from .base_manager_utils import BaseManagerUtils
from .manager_utils import current_timestamp, ensure_directory
from .user_manager import (
    AgentStatus,
    AgentCapability,
    AgentInfo,
    UserManager,
)
from .resource_manager import WorkspaceInfo, ResourceManager
from .process_manager import ProcessManager

__all__ = [
    "ManagerStatus",
    "ManagerPriority",
    "ManagerMetrics",
    "ManagerConfig",
    "BaseManagerInterface",
    "BaseManagerLifecycle",
    "BaseManagerMonitoring",
    "BaseManagerConfiguration",
    "BaseManagerUtils",
    "current_timestamp",
    "ensure_directory",
    "AgentStatus",
    "AgentCapability",
    "AgentInfo",
    "WorkspaceInfo",
    "UserManager",
    "ResourceManager",
    "ProcessManager",
>>>>>>> origin/codex/catalog-functions-in-utils-directories
]
