"""Central utilities package.

This module re-exports commonly used utilities to provide a single import
location. Only modules that are available in the repository are imported to
avoid runtime import errors.
"""

__version__ = "2.0.0"
__author__ = "Utilities & Support Team"
__status__ = "ACTIVE"

import argparse
import sys

from .config_loader import ConfigLoader
from .logging_setup import LoggingSetup
from .system_info import SystemInfo
from .dependency_checker import DependencyChecker
from .file_utils import FileUtils
from .config_utils_coordinator import ConfigUtilsCoordinator
from .system_utils_coordinator import SystemUtilsCoordinator
from .environment_overrides import EnvironmentOverrides
from .serializable import SerializableMixin
from .profiling import time_block
from .caching import generate_cache_key, calculate_file_hash

__all__ = [
    "ConfigLoader",
    "LoggingSetup",
    "SystemInfo",
    "DependencyChecker",
    "FileUtils",
    "ConfigUtilsCoordinator",
    "SystemUtilsCoordinator",
    "EnvironmentOverrides",
    "SerializableMixin",
    "time_block",
    "generate_cache_key",
    "calculate_file_hash",
]


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
