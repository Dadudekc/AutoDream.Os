"""
Migrated Configuration: automation_orchestrator_config.py

This file was automatically migrated from the original configuration
file to the centralized configuration system.

Original file: src\web\automation\automation_orchestrator_config.py
Migration date: 2025-08-30T17:16:18.131787
"""

from src.core.config.centralized_config_manager import get_config_manager

# Configuration data from automation_orchestrator_config.py
CONFIG_DATA = {'EXAMPLE_PIPELINES': {'basic_website': {'website_generation': {'name': 'example_site', 'title': 'Example Website', 'description': 'A basic example website', 'pages': [{'name': 'home', 'title': 'Home', 'route': '/', 'content': {'heading': 'Welcome', 'description': 'Welcome to our site'}}]}, 'testing': {}}, 'automation_demo': {'web_automation': {'headless': True, 'browser_type': 'chrome', 'tasks': [{'type': 'navigation', 'url': 'https://example.com'}, {'type': 'screenshot', 'filename': 'example_site'}]}, 'testing': {}}}}

def migrate_to_centralized():
    """Migrate configuration data to the centralized system."""
    config_manager = get_config_manager()
    
    for key, value in CONFIG_DATA.items():
        # Determine section based on key
        section = _determine_section(key)
        config_manager.set(key, value, section, description=f"Migrated from automation_orchestrator_config.py")
    
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
        logging.warning(f"Failed to auto-migrate automation_orchestrator_config.py: {e}")