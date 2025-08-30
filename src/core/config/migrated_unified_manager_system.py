"""
Migrated Configuration: unified_manager_system.json

This file was automatically migrated from the original configuration
file to the centralized configuration system.

Original file: config\unified_manager_system.json
Migration date: 2025-08-30T17:16:23.285033
"""

from src.core.config.centralized_config_manager import get_config_manager

# Configuration data from unified_manager_system.json
CONFIG_DATA = {'unified_manager_system': {'version': '2.0.0', 'enabled': 'ENABLE_TRUE', 'health_check_interval': 300, 'auto_recovery': 'ENABLE_TRUE', 'max_recovery_attempts': 'VALUE_THREE', 'startup_timeout': 60, 'shutdown_timeout': 30, 'categories': {'core': {'enabled': 'ENABLE_TRUE', 'priority': 'critical', 'startup_order': ['system_manager', 'config_manager', 'status_manager', 'task_manager', 'data_manager', 'communication_manager', 'health_manager']}, 'extended': {'enabled': 'ENABLE_TRUE', 'priority': 'high', 'startup_order': ['ai_manager', 'model_manager', 'api_key_manager', 'ai_agent_manager', 'workflow_manager', 'reporting_manager', 'dev_workflow_manager', 'portfolio_manager', 'risk_manager']}, 'specialized': {'enabled': 'ENABLE_TRUE', 'priority': 'medium', 'startup_order': ['performance_alert_manager', 'autonomous_task_manager', 'autonomous_workflow_manager', 'autonomous_reporting_manager']}}, 'health_monitoring': {'enabled': 'ENABLE_TRUE', 'check_interval': 300, 'timeout': 10, 'failure_threshold': 'VALUE_THREE', 'auto_restart': 'ENABLE_TRUE', 'health_score_threshold': 80}, 'performance': {'metrics_collection': 'ENABLE_TRUE', 'performance_tracking': 'ENABLE_TRUE', 'resource_monitoring': 'ENABLE_TRUE', 'alerting': 'ENABLE_TRUE'}, 'logging': {'level': 'INFO', 'format': 'json', 'output': 'file', 'file_path': 'logs/unified_manager_system.log', 'max_file_size': '10MB', 'backup_count': 5}, 'dependencies': {'strict_mode': 'ENABLE_TRUE', 'circular_dependency_check': 'ENABLE_TRUE', 'dependency_timeout': 30, 'retry_failed_dependencies': 'ENABLE_TRUE'}}}

def migrate_to_centralized():
    """Migrate configuration data to the centralized system."""
    config_manager = get_config_manager()
    
    for key, value in CONFIG_DATA.items():
        # Determine section based on key
        section = _determine_section(key)
        config_manager.set(key, value, section, description=f"Migrated from unified_manager_system.json")
    
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
        logging.warning(f"Failed to auto-migrate unified_manager_system.json: {e}")