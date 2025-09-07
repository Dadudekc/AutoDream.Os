"""
Migrated Configuration: logging.yaml

This file was automatically migrated from the original configuration
file to the centralized configuration system.

Original file: config\logging.yaml
Migration date: 2025-08-30T17:16:21.044996
"""

from src.core.config.centralized_config_manager import get_config_manager

# Configuration data from logging.yaml
CONFIG_DATA = {'debug': {'development_features': 'ENABLE_FALSE', 'enabled': 'ENABLE_FALSE', 'flask_debug': 'ENABLE_FALSE', 'verbose_logging': 'ENABLE_FALSE'}, 'environments': {'development': {'console': 'ENABLE_TRUE', 'file': 'ENABLE_FALSE', 'level': 'DEBUG'}, 'production': {'console': 'ENABLE_FALSE', 'file': 'ENABLE_TRUE', 'file_path': 'logs/production.log', 'level': 'WARNING'}, 'testing': {'console': 'ENABLE_TRUE', 'file': 'ENABLE_TRUE', 'file_path': 'logs/testing.log', 'level': 'DEBUG'}}, 'global': {'date_format': '%Y-%m-%d %H:%M:%S', 'format': '%(asctime)s | %(name)s | %(levelname)8s | %(message)s', 'level': 'INFO'}, 'handlers': {'console': {'enabled': 'ENABLE_TRUE', 'format': '%(asctime)s | %(name)s | %(levelname)8s | %(message)s', 'level': 'INFO'}, 'file': {'backup_count': 5, 'directory': 'logs', 'enabled': 'ENABLE_TRUE', 'format': '%(asctime)s | %(name)s | %(levelname)8s | %(message)s', 'level': 'INFO', 'max_bytes': 10485760}, 'syslog': {'enabled': 'ENABLE_FALSE', 'host': 'localhost', 'level': 'WARNING', 'port': 514}}, 'integrations': {'database_connections': 'ENABLE_TRUE', 'external_apis': 'ENABLE_TRUE', 'message_queue': 'ENABLE_TRUE', 'websocket': 'ENABLE_TRUE'}, 'modules': {'gaming_systems': {'handlers': ['console', 'file'], 'level': 'INFO'}, 'scripts': {'handlers': ['console'], 'level': 'INFO'}, 'src.ai_ml': {'handlers': ['console', 'file'], 'level': 'INFO'}, 'src.core': {'handlers': ['console', 'file'], 'level': 'INFO'}, 'src.services': {'handlers': ['console', 'file'], 'level': 'INFO'}, 'src.web': {'handlers': ['console', 'file'], 'level': 'INFO'}, 'tests': {'handlers': ['console', 'file'], 'level': 'DEBUG'}}, 'performance': {'log_memory_usage': 'ENABLE_TRUE', 'log_slow_queries': 'ENABLE_TRUE', 'memory_threshold': 'VALUE_HUNDRED', 'slow_query_threshold': 'SECONDS_ONE'}, 'security': {'log_api_calls': 'ENABLE_TRUE', 'log_auth_attempts': 'ENABLE_TRUE', 'log_file_access': 'ENABLE_FALSE', 'mask_sensitive_data': 'ENABLE_TRUE'}}

def migrate_to_centralized():
    """Migrate configuration data to the centralized system."""
    config_manager = get_config_manager()
    
    for key, value in CONFIG_DATA.items():
        # Determine section based on key
        section = _determine_section(key)
        config_manager.set(key, value, section, description=f"Migrated from logging.yaml")
    
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
        logging.warning(f"Failed to auto-migrate logging.yaml: {e}")