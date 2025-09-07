"""
Migrated Configuration: agent_integration_config.json

This file was automatically migrated from the original configuration
file to the centralized configuration system.

Original file: config\agent_integration_config.json
Migration date: 2025-08-30T17:16:22.061922
"""

from src.core.config.centralized_config_manager import get_config_manager

# Configuration data from agent_integration_config.json
CONFIG_DATA = {'version': '2.0.0', 'last_updated': '2025-08-28T21:50:00Z', 'description': 'Centralized integration configuration for all agents - Single Source of Truth', 'integration_config': {'messaging_system': 'v2_message_queue', 'task_manager': 'v2_task_manager', 'monitoring': 'v2_performance_monitor', 'logging': 'v2_logging_system'}, 'validation_rules': {'required_fields': ['messaging_system', 'task_manager', 'monitoring', 'logging'], 'version_compatibility': ['2.0.0', '2.1.0'], 'field_types': {'messaging_system': 'string', 'task_manager': 'string', 'monitoring': 'string', 'logging': 'string'}}, 'metadata': {'created_by': 'Agent-8 (Integration Enhancement Manager)', 'contract': 'SSOT-001: SSOT Violation Analysis & Resolution', 'purpose': 'Eliminate configuration duplication across all 8 agents', 'benefits': ['Single source of truth for integration settings', 'Reduced configuration drift risk', 'Improved maintainability', 'Consistent agent behavior']}}

def migrate_to_centralized():
    """Migrate configuration data to the centralized system."""
    config_manager = get_config_manager()
    
    for key, value in CONFIG_DATA.items():
        # Determine section based on key
        section = _determine_section(key)
        config_manager.set(key, value, section, description=f"Migrated from agent_integration_config.json")
    
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
        logging.warning(f"Failed to auto-migrate agent_integration_config.json: {e}")