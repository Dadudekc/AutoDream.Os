"""
Migrated Configuration: branch_protection.json

This file was automatically migrated from the original configuration
file to the centralized configuration system.

Original file: config\branch_protection.json
Migration date: 2025-08-30T17:16:21.714606
"""

from src.core.config.centralized_config_manager import get_config_manager

# Configuration data from branch_protection.json
CONFIG_DATA = {'branch_protection': {'main_branch': 'agent', 'protected_branches': ['agent', 'main', 'master'], 'rules': {'require_reviews': 'ENABLE_TRUE', 'min_reviews': 'VALUE_TWO', 'require_status_checks': 'ENABLE_TRUE', 'require_branch_up_to_date': 'ENABLE_TRUE', 'restrict_pushes': 'ENABLE_TRUE', 'allow_force_pushes': 'ENABLE_FALSE', 'allow_deletions': 'ENABLE_FALSE'}}, 'pr_limits': {'max_file_size_lines': 400, 'max_pr_size_lines': 500, 'max_files_per_pr': 20}, 'automated_checks': ['file_size_validation', 'code_style_checking', 'basic_syntax_validation', 'security_scanning']}

def migrate_to_centralized():
    """Migrate configuration data to the centralized system."""
    config_manager = get_config_manager()
    
    for key, value in CONFIG_DATA.items():
        # Determine section based on key
        section = _determine_section(key)
        config_manager.set(key, value, section, description=f"Migrated from branch_protection.json")
    
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
        logging.warning(f"Failed to auto-migrate branch_protection.json: {e}")