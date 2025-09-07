"""
Migrated Configuration: centralized_config_manager.py

This file was automatically migrated from the original configuration
file to the centralized configuration system.

Original file: src\core\config\centralized_config_manager.py
Migration date: 2025-08-30T17:16:24.614243
"""

from src.core.config.centralized_config_manager import get_config_manager

# Configuration data from centralized_config_manager.py
CONFIG_DATA = {'ENVIRONMENT': 'environment', 'FILE': 'file', 'DATABASE': 'database', 'API': 'api', 'DEFAULT': 'default', 'CRITICAL': 0, 'HIGH': 1, 'NORMAL': 2, 'LOW': 3, 'DEBUG': 4, 'STRING': 'string', 'INTEGER': 'integer', 'FLOAT': 'float', 'BOOLEAN': 'boolean', 'LIST': 'list', 'DICT': 'dict', 'ENUM': 'enum'}

def migrate_to_centralized():
    """Migrate configuration data to the centralized system."""
    config_manager = get_config_manager()
    
    for key, value in CONFIG_DATA.items():
        # Determine section based on key
        section = _determine_section(key)
        config_manager.set(key, value, section, description=f"Migrated from centralized_config_manager.py")
    
    return len(CONFIG_DATA)

def _determine_section(key: str) -> str:
    """Determine which section a configuration key belongs to."""
    key_lower = key.lower()
    
    if any(word in key_lower for word in ["log", "logger", "logging"]):
        return "logging"
    elif any(word in key_lower for word in ["perf", "benchmark", "metric", "monitor"]):
        return "performance"
    elif any(word in key_lower for word in ["db", "database", "connection"]):
        return "database"
    elif any(word in key_lower for word in ["auth", "security", "encrypt", "token"]):
        return "security"
    elif any(word in key_lower for word in ["api", "endpoint", "url", "route"]):
        return "api"
    elif any(word in key_lower for word in ["test", "testing", "mock"]):
        return "testing"
    elif any(word in key_lower for word in ["dev", "development", "debug"]):
        return "development"
    elif any(word in key_lower for word in ["prod", "production", "deploy"]):
        return "production"
    else:
        return "general"

# Auto-migrate when module is imported
if __name__ != "__main__":
    try:
        migrate_to_centralized()
    except Exception as e:
        import logging
        logging.warning(f"Failed to auto-migrate centralized_config_manager.py: {e}")