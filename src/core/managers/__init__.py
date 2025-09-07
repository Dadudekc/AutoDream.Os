"""Core managers package exporting specialized managers."""

from .core_onboarding_manager import CoreOnboardingManager
from .core_recovery_manager import CoreRecoveryManager
from .core_results_manager import CoreResultsManager
from .core_service_coordinator import CoreServiceCoordinator
from .core_service_manager import CoreServiceManager
from .core_resource_manager import CoreResourceManager
from .core_configuration_manager import CoreConfigurationManager
from .core_execution_manager import CoreExecutionManager
from .core_monitoring_manager import CoreMonitoringManager

__all__ = [
    "CoreOnboardingManager",
    "CoreRecoveryManager",
    "CoreResultsManager",
    "CoreServiceCoordinator",
    "CoreServiceManager",
    "CoreResourceManager",
    "CoreConfigurationManager",
    "CoreExecutionManager",
    "CoreMonitoringManager",
]

# Optional export of UnifiedConfigurationManager to avoid import-time errors
try:  # pragma: no cover - defensive
    from .unified_configuration_manager import UnifiedConfigurationManager

    __all__.append("UnifiedConfigurationManager")
except Exception:  # Missing dependencies
    UnifiedConfigurationManager = None
