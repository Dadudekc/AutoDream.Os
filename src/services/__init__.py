# AUTO-GENERATED __init__.py
# DO NOT EDIT MANUALLY - changes may be overwritten

# Import only core modules that don't cause circular dependencies
from . import constants


# Lazy imports for modules that may have circular dependencies
def _lazy_import(module_name):
    """Lazy import to avoid circular dependencies."""
    import importlib

    return importlib.import_module(f"src.services.{module_name}")


# Define lazy import functions for complex modules
def get_agent_status_manager():
    return _lazy_import("agent_status_manager")


def get_messaging_core():
    return _lazy_import("messaging_core")


def get_vector_database():
    return _lazy_import("vector_database")


def get_agent_registry():
    return _lazy_import("messaging_agent_registry")


def get_config():
    """Lazy import config to avoid circular dependencies."""
    return _lazy_import("config")


__all__ = [
    "constants",
    "get_agent_status_manager",
    "get_messaging_core",
    "get_vector_database",
    "get_agent_registry",
    "get_config",
]
