"""
🔧 Utils Package - Agent_Cellphone_V2

This package contains utility components for the Agent_Cellphone_V2 system:
- Configuration utilities
- Logging utilities
- System utilities
- Validation utilities
- File utilities

Following V2 coding standards: ≤300 LOC per file, OOP design, SRP.
SSOT: Single Source of Truth for all utility functions.
"""

__version__ = "2.0.0"
__author__ = "Utilities & Support Team"
__status__ = "ACTIVE"

import argparse
import sys

# SSOT: Core utility imports - Single source of truth for all utility classes
try:
    from .config_loader import ConfigLoader
    from .logging_setup import LoggingSetup
    from .system_info import SystemInfo
    from src.core.performance.monitoring.performance_monitor import PerformanceMonitor
    from .dependency_checker import DependencyChecker
    from .cli_utils import CLIUtils
    from .message_builder import MessageBuilder
    from .onboarding_utils import OnboardingUtils
    from .onboarding_coordinator import OnboardingCoordinator
    from .onboarding_orchestrator import OnboardingOrchestrator
    from .config_utils_coordinator import ConfigUtilsCoordinator
    from .system_utils_coordinator import SystemUtilsCoordinator
    from .environment_overrides import EnvironmentOverrides
    from .serializable import SerializableMixin

    __all__ = [
        "ConfigLoader",
        "LoggingSetup",
        "SystemInfo",
        "PerformanceMonitor",
        "DependencyChecker",
        "CLIUtils",
        "MessageBuilder",
        "OnboardingUtils",
        "OnboardingCoordinator",
        "OnboardingOrchestrator",
        "ConfigUtilsCoordinator",
        "SystemUtilsCoordinator",
        "EnvironmentOverrides",
        "SerializableMixin",
    ]

except ImportError as e:
    print(f"⚠️ Warning: Some utils components not available: {e}")
    __all__ = []


def main():
    """CLI interface for utils module"""
    parser = argparse.ArgumentParser(description="Utils Package CLI")
    parser.add_argument("--version", action="store_true", help="Show version")
    parser.add_argument("--status", action="store_true", help="Show status")
    
    args = parser.parse_args()
    
    if args.version:
        print(f"Utils Package v{__version__}")
    elif args.status:
        print(f"Status: {__status__}")
        print(f"Available components: {len(__all__)}")
        for component in __all__:
            print(f"  - {component}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
