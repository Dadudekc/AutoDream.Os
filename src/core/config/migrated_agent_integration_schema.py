"""
Migrated Configuration: agent_integration_schema.json

This file was automatically migrated from the original configuration
file to the centralized configuration system.

Original file: config\agent_integration_schema.json
Migration date: 2025-08-30T17:16:23.316062
"""

from src.core.config.centralized_config_manager import get_config_manager

# Configuration data from agent_integration_schema.json
CONFIG_DATA = {'$schema': 'http://json-schema.org/draft-07/schema#', 'title': 'Agent Integration Configuration Schema', 'description': 'JSON Schema for validating agent integration configuration', 'type': 'object', 'required': ['version', 'last_updated', 'integration_config', 'validation_rules'], 'properties': {'version': {'type': 'string', 'pattern': '^\\d+\\.\\d+\\.\\d+$', 'description': 'Configuration version in semantic versioning format'}, 'last_updated': {'type': 'string', 'format': 'date-time', 'description': 'ISO 8601 timestamp of last configuration update'}, 'description': {'type': 'string', 'description': 'Human-readable description of the configuration'}, 'integration_config': {'type': 'object', 'required': ['messaging_system', 'task_manager', 'monitoring', 'logging'], 'properties': {'messaging_system': {'type': 'string', 'enum': ['v2_message_queue', 'v1_message_queue', 'legacy_messaging'], 'description': 'Messaging system implementation to use'}, 'task_manager': {'type': 'string', 'enum': ['v2_task_manager', 'v1_task_manager', 'legacy_task_manager'], 'description': 'Task management system implementation to use'}, 'monitoring': {'type': 'string', 'enum': ['v2_performance_monitor', 'v1_performance_monitor', 'basic_monitoring'], 'description': 'Performance monitoring system implementation to use'}, 'logging': {'type': 'string', 'enum': ['v2_logging_system', 'v1_logging_system', 'basic_logging'], 'description': 'Logging system implementation to use'}}, 'additionalProperties': 'ENABLE_FALSE'}, 'validation_rules': {'type': 'object', 'required': ['required_fields', 'version_compatibility'], 'properties': {'required_fields': {'type': 'array', 'items': {'type': 'string'}, 'description': 'List of required fields in integration_config'}, 'version_compatibility': {'type': 'array', 'items': {'type': 'string'}, 'description': 'List of compatible version strings'}, 'field_types': {'type': 'object', 'description': 'Expected data types for configuration fields'}}}, 'metadata': {'type': 'object', 'properties': {'created_by': {'type': 'string', 'description': 'Agent or user who created this configuration'}, 'contract': {'type': 'string', 'description': 'Associated contract or project identifier'}, 'purpose': {'type': 'string', 'description': 'Purpose of this configuration'}, 'benefits': {'type': 'array', 'items': {'type': 'string'}, 'description': 'List of benefits provided by this configuration'}}}}, 'additionalProperties': 'ENABLE_FALSE'}

def migrate_to_centralized():
    """Migrate configuration data to the centralized system."""
    config_manager = get_config_manager()
    
    for key, value in CONFIG_DATA.items():
        # Determine section based on key
        section = _determine_section(key)
        config_manager.set(key, value, section, description=f"Migrated from agent_integration_schema.json")
    
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
        logging.warning(f"Failed to auto-migrate agent_integration_schema.json: {e}")