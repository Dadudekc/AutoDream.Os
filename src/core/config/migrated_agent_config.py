"""
Migrated Configuration: agent_config.json

This file was automatically migrated from the original configuration
file to the centralized configuration system.

Original file: agent_workspaces\Agent-8\config\agent_config.json
Migration date: 2025-08-30T17:16:22.335169
"""

from src.core.config.centralized_config_manager import get_config_manager

# Configuration data from agent_config.json
CONFIG_DATA = {'agent_id': 'Agent-8', 'agent_name': 'Automation Agent', 'agent_type': 'automation', 'capabilities': ['process_automation', 'workflow_execution', 'optimization'], 'specializations': ['automation_operations', 'system_integration'], 'performance_metrics': {'task_completion_rate': 0.95, 'response_time_ms': 230, 'accuracy_score': 0.92, 'efficiency_rating': 0.88}, 'workflow_preferences': {'max_concurrent_tasks': 3, 'preferred_task_types': ['automation', 'basic_processing'], 'task_priority_strategy': 'fifo_with_priority'}, 'communication_settings': {'protocol': 'v2_messaging', 'message_format': 'json', 'response_timeout_ms': 5000, 'retry_attempts': 3}, 'resource_limits': {'max_memory_mb': 512, 'max_cpu_percent': 25, 'max_disk_mb': 100, 'max_network_mb': 50}, 'integration_config': {'messaging_system': 'v2_message_queue', 'task_manager': 'v2_task_manager', 'monitoring': 'v2_performance_monitor', 'logging': 'v2_logging_system'}, 'security_settings': {'authentication_required': True, 'encryption_level': 'standard', 'access_control': 'role_based', 'audit_logging': True}, 'last_updated': '2025-08-23T19:30:00Z', 'version': '2.0.0'}

def migrate_to_centralized():
    """Migrate configuration data to the centralized system."""
    config_manager = get_config_manager()
    
    for key, value in CONFIG_DATA.items():
        # Determine section based on key
        section = _determine_section(key)
        config_manager.set(key, value, section, description=f"Migrated from agent_config.json")
    
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
        logging.warning(f"Failed to auto-migrate agent_config.json: {e}")