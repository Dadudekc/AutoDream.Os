
# MIGRATED: This file has been migrated to the centralized configuration system
#!/usr/bin/env python3
"""
Agent Integration Configuration Manager

This module provides centralized configuration management for agent integration settings,
eliminating SSOT violations and ensuring configuration consistency across all agents.

Author: Agent-8 (Integration Enhancement Manager)
Contract: SSOT-001: SSOT Violation Analysis & Resolution
License: MIT
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConfigValidationStatus(Enum):
    """Configuration validation status enumeration"""
    VALID = "VALID"
    INVALID = "INVALID"
    WARNING = "WARNING"
    ERROR = "ERROR"


@dataclass
class ValidationResult:
    """Configuration validation result"""
    status: ConfigValidationStatus
    message: str
    errors: List[str]
    warnings: List[str]
    timestamp: datetime


@dataclass
class AgentConfig:
    """Agent configuration data structure"""
    agent_id: str
    integration_config: Dict[str, str]
    version: str
    last_updated: datetime
    source: str


class AgentIntegrationConfigManager:
    """
    Centralized configuration manager for agent integration settings.
    
    This class eliminates SSOT violations by providing a single source of truth
    for all agent integration configurations.
    """
    
    def __init__(self, config_path: str = "config/agent_integration_config.json"):
        """
        Initialize the configuration manager.
        
        Args:
            config_path: Path to the central configuration file
        """
        self.config_path = Path(config_path)
        self.central_config = None
        self.validation_schema = None
        self.agent_configs: Dict[str, AgentConfig] = {}
        self._load_central_config()
    
    def _load_central_config(self) -> None:
        """Load the central integration configuration file."""
        try:
            if not self.config_path.exists():
                logger.error(f"Central configuration file not found: {self.config_path}")
                self._create_default_config()
                return
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.central_config = json.load(f)
            
            logger.info(f"Central configuration loaded from {self.config_path}")
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in configuration file: {e}")
            self._create_default_config()
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            self._create_default_config()
    
    def _create_default_config(self) -> None:
        """Create a default configuration if loading fails."""
        logger.warning("Creating default configuration due to loading failure")
        self.central_config = {
            "version": "2.0.0",
            "last_updated": datetime.now().isoformat(),
            "description": "Default configuration - SSOT resolution in progress",
            "integration_config": {
                "messaging_system": "v2_message_queue",
                "task_manager": "v2_task_manager",
                "monitoring": "v2_performance_monitor",
                "logging": "v2_logging_system"
            },
            "validation_rules": {
                "required_fields": ["messaging_system", "task_manager", "monitoring", "logging"],
                "version_compatibility": ["2.0.0", "2.1.0"]
            }
        }
    
    def validate_config(self, config: Dict[str, Any]) -> ValidationResult:
        """
        Validate configuration against schema and rules.
        
        Args:
            config: Configuration dictionary to validate
            
        Returns:
            ValidationResult with validation status and details
        """
        errors = []
        warnings = []
        
        # Check required fields
        required_fields = config.get("validation_rules", {}).get("required_fields", [])
        for field in required_fields:
            if field not in config.get("integration_config", {}):
                errors.append(f"Required field '{field}' missing from integration_config")
        
        # Check version compatibility
        version = config.get("version", "unknown")
        compatible_versions = config.get("validation_rules", {}).get("version_compatibility", [])
        if version not in compatible_versions:
            warnings.append(f"Version {version} not in compatible versions list")
        
        # Determine status
        if errors:
            status = ConfigValidationStatus.INVALID
        elif warnings:
            status = ConfigValidationStatus.WARNING
        else:
            status = ConfigValidationStatus.VALID
        
        return ValidationResult(
            status=status,
            message=f"Configuration validation completed with {len(errors)} errors, {len(warnings)} warnings",
            errors=errors,
            warnings=warnings,
            timestamp=datetime.now()
        )
    
    def get_agent_config(self, agent_id: str) -> Optional[AgentConfig]:
        """
        Get integration configuration for a specific agent.
        
        Args:
            agent_id: ID of the agent (e.g., "Agent-1", "Agent-8")
            
        Returns:
            AgentConfig object or None if not found
        """
        if agent_id in self.agent_configs:
            return self.agent_configs[agent_id]
        
        # Create new agent config from central source
        if self.central_config:
            agent_config = AgentConfig(
                agent_id=agent_id,
                integration_config=self.central_config["integration_config"].copy(),
                version=self.central_config["version"],
                last_updated=datetime.fromisoformat(self.central_config["last_updated"]),
                source="central_config"
            )
            self.agent_configs[agent_id] = agent_config
            return agent_config
        
        return None
    
    def update_config(self, new_config: Dict[str, Any]) -> bool:
        """
        Update central configuration and propagate to all agents.
        
        Args:
            new_config: New configuration dictionary
            
        Returns:
            True if update successful, False otherwise
        """
        try:
            # Validate new configuration
            validation_result = self.validate_config(new_config)
            if validation_result.status == ConfigValidationStatus.INVALID:
                logger.error(f"Configuration validation failed: {validation_result.errors}")
                return False
            
            # Update central configuration
            self.central_config = new_config
            self.central_config["last_updated"] = datetime.now().isoformat()
            
            # Save to file
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.central_config, f, indent=2, default=str)
            
            # Propagate to all agents
            self._propagate_config_to_agents()
            
            logger.info("Central configuration updated and propagated to all agents")
            return True
            
        except Exception as e:
            logger.error(f"Error updating configuration: {e}")
            return False
    
    def _propagate_config_to_agents(self) -> None:
        """Propagate configuration changes to all registered agents."""
        for agent_id, agent_config in self.agent_configs.items():
            agent_config.integration_config = self.central_config["integration_config"].copy()
            agent_config.version = self.central_config["version"]
            agent_config.last_updated = datetime.now()
            agent_config.source = "central_config_propagated"
            
            logger.debug(f"Configuration propagated to {agent_id}")
    
    def get_all_agent_configs(self) -> Dict[str, AgentConfig]:
        """Get configurations for all registered agents."""
        return self.agent_configs.copy()
    
    def register_agent(self, agent_id: str) -> bool:
        """
        Register a new agent for configuration management.
        
        Args:
            agent_id: ID of the agent to register
            
        Returns:
            True if registration successful, False otherwise
        """
        if agent_id in self.agent_configs:
            logger.warning(f"Agent {agent_id} already registered")
            return False
        
        agent_config = self.get_agent_config(agent_id)
        if agent_config:
            logger.info(f"Agent {agent_id} registered successfully")
            return True
        
        return False
    
    def unregister_agent(self, agent_id: str) -> bool:
        """
        Unregister an agent from configuration management.
        
        Args:
            agent_id: ID of the agent to unregister
            
        Returns:
            True if unregistration successful, False otherwise
        """
        if agent_id in self.agent_configs:
            del self.agent_configs[agent_id]
            logger.info(f"Agent {agent_id} unregistered successfully")
            return True
        
        logger.warning(f"Agent {agent_id} not found in registered agents")
        return False
    
    def get_config_health_status(self) -> Dict[str, Any]:
        """
        Get overall configuration system health status.
        
        Returns:
            Dictionary containing health metrics and status
        """
        total_agents = len(self.agent_configs)
        config_validation = self.validate_config(self.central_config)
        
        health_status = {
            "timestamp": datetime.now().isoformat(),
            "total_agents": total_agents,
            "central_config_status": config_validation.status.value,
            "central_config_errors": len(config_validation.errors),
            "central_config_warnings": len(config_validation.warnings),
            "config_file_exists": self.config_path.exists(),
            "last_config_update": self.central_config.get("last_updated") if self.central_config else None,
            "system_health": "HEALTHY" if config_validation.status == ConfigValidationStatus.VALID else "DEGRADED"
        }
        
        return health_status
    
    def export_agent_config(self, agent_id: str, output_path: str) -> bool:
        """
        Export agent configuration to a file.
        
        Args:
            agent_id: ID of the agent
            output_path: Path to save the exported configuration
            
        Returns:
            True if export successful, False otherwise
        """
        try:
            agent_config = self.get_agent_config(agent_id)
            if not agent_config:
                logger.error(f"Agent {agent_id} not found")
                return False
            
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(agent_config), f, indent=2, default=str)
            
            logger.info(f"Agent {agent_id} configuration exported to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting agent configuration: {e}")
            return False


def create_agent_integration_manager(config_path: str = None) -> AgentIntegrationConfigManager:
    """
    Factory function to create an AgentIntegrationConfigManager instance.
    
    Args:
        config_path: Optional path to configuration file
        
    Returns:
        Configured AgentIntegrationConfigManager instance
    """
    if config_path is None:
        config_path = "config/agent_integration_config.json"
    
    return AgentIntegrationConfigManager(config_path)


# Example usage and testing
if __name__ == "__main__":
    # Create configuration manager
    manager = create_agent_integration_manager()
    
    # Register some agents
    manager.register_agent("Agent-1")
    manager.register_agent("Agent-8")
    
    # Get agent configurations
    agent1_config = manager.get_agent_config("Agent-1")
    agent8_config = manager.get_agent_config("Agent-8")
    
    print(f"Agent-1 config: {agent1_config}")
    print(f"Agent-8 config: {agent8_config}")
    
    # Get system health
    health = manager.get_config_health_status()
    print(f"System health: {health}")
