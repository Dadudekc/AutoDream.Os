#!/usr/bin/env python3
"""
Scanner Registry - Autonomous Plugin System
===========================================

Self-registering scanner system for config pattern detection.
Scanners auto-discover and auto-register themselves.

AUTONOMY FEATURES:
- Auto-discovery of scanner classes
- Auto-registration via decorators
- Dynamic scanner loading
- Self-organizing plugin architecture

V2 Compliance: <300 lines
Author: Agent-4 (Captain) - Autonomous Systems
"""

import importlib
import inspect
import logging

logger = logging.getLogger(__name__)


class ScannerRegistry:
    """Autonomous scanner registry with auto-discovery."""

    _instance = None
    _scanners: dict[str, type] = {}

    def __new__(cls):
        """Singleton pattern for registry."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def register(cls, scanner_class: type) -> type:
        """Register a scanner class."""
        scanner_name = scanner_class.__name__
        cls._scanners[scanner_name] = scanner_class
        logger.info(f"✅ Auto-registered scanner: {scanner_name}")
        return scanner_class

    @classmethod
    def get_scanner(cls, name: str) -> type:
        """Get a registered scanner by name."""
        return cls._scanners.get(name)

    @classmethod
    def get_all_scanners(cls) -> list[type]:
        """Get all registered scanners."""
        return list(cls._scanners.values())

    @classmethod
    def auto_discover_scanners(cls, module_path: str = "src.utils") -> None:
        """Auto-discover and register scanners in a module."""
        try:
            # Import the module
            module = importlib.import_module(module_path)

            # Find all scanner classes
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if name.endswith("Scanner") and hasattr(obj, "scan_file"):
                    if name not in cls._scanners:
                        cls.register(obj)

            logger.info(f"✅ Auto-discovery complete: {len(cls._scanners)} scanners")

        except Exception as e:
            logger.error(f"Error auto-discovering scanners: {e}")

    @classmethod
    def list_scanners(cls) -> str:
        """List all registered scanners."""
        output = "📋 Registered Scanners:\n"
        for name, scanner in cls._scanners.items():
            output += f"  - {name}\n"
        return output


def auto_register(scanner_class: type) -> type:
    """Decorator for auto-registering scanners."""
    ScannerRegistry.register(scanner_class)
    return scanner_class


# Example usage in unified_config_utils.py:
# @auto_register
# class EnvironmentVariableScanner(ConfigurationScanner):
#     ...

if __name__ == "__main__":
    # Demo auto-discovery
    registry = ScannerRegistry()
    registry.auto_discover_scanners("src.utils.unified_config_utils")
    print(registry.list_scanners())
