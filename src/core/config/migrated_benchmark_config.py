"""
Migrated Configuration: benchmark_config.py

This file was automatically migrated from the original configuration
file to the centralized configuration system.

Original file: src\core\performance\config\benchmark_config.py
Migration date: 2025-08-30T17:16:23.055826
"""

from src.core.config.centralized_config_manager import get_config_manager

# Configuration data from benchmark_config.py
CONFIG_DATA = {'LOAD_TEST': 'load_test', 'STRESS_TEST': 'stress_test', 'ENDURANCE_TEST': 'endurance_test', 'SPIKE_TEST': 'spike_test', 'SCALABILITY_TEST': 'scalability_test', 'PENDING': 'pending', 'RUNNING': 'running', 'COMPLETED': 'completed', 'FAILED': 'failed', 'CANCELLED': 'cancelled'}

def migrate_to_centralized():
    """Migrate configuration data to the centralized system."""
    config_manager = get_config_manager()
    
    for key, value in CONFIG_DATA.items():
        # Determine section based on key
        section = _determine_section(key)
        config_manager.set(key, value, section, description=f"Migrated from benchmark_config.py")
    
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
        logging.warning(f"Failed to auto-migrate benchmark_config.py: {e}")