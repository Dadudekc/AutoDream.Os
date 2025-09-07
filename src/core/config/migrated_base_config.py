"""
Migrated Configuration: base_config.py

This file was automatically migrated from the original configuration
file to the centralized configuration system.

Original file: src\core\base\base_config.py
Migration date: 2025-08-30T17:16:24.550184
"""

from src.core.config.centralized_config_manager import get_config_manager

# Configuration data from base_config.py
CONFIG_DATA = {'PERFORMANCE': 'performance', 'REFACTORING': 'refactoring', 'TESTING': 'testing', 'SERVICE': 'service', 'AI_ML': 'ai_ml', 'FSM': 'fsm', 'WORKFLOW': 'workflow', 'VALIDATION': 'validation', 'SECURITY': 'security', 'DATABASE': 'database', 'CUSTOM': 'custom', 'JSON': 'json', 'YAML': 'yaml', 'INI': 'ini', 'ENV': 'env', 'PYTHON': 'python', 'FILE': 'file', 'ENVIRONMENT': 'environment', 'API': 'api', 'DEFAULT': 'default'}

def migrate_to_centralized():
    """Migrate configuration data to the centralized system."""
    config_manager = get_config_manager()
    
    for key, value in CONFIG_DATA.items():
        # Determine section based on key
        section = _determine_section(key)
        config_manager.set(key, value, section, description=f"Migrated from base_config.py")
    
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
        logging.warning(f"Failed to auto-migrate base_config.py: {e}")