#!/usr/bin/env python3
"""
Agent Configuration Loader - Agent Cellphone V2
==============================================

Loads and manages agent configurations for assessment.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from .agent_assessment_types import AgentConfiguration


class AgentConfigurationLoader:
    """Loads and manages agent configurations for assessment"""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.logger = logging.getLogger(__name__)
        self.agent_configs: Dict[str, Any] = {}
        self.agent_locations: Dict[str, str] = {}
        self.agent_roles: Dict[str, str] = {}
        
        # Load configurations
        self._load_agent_configs()
    
    def _load_agent_configs(self):
        """Load agent configurations and roles"""
        try:
            # Load agent roles
            roles_file = self.repo_root / "config" / "agents" / "agent_roles.json"
            if roles_file.exists():
                with open(roles_file, "r") as f:
                    self.agent_roles = json.load(f)
                self.logger.info("Agent roles loaded successfully")
            else:
                self.logger.warning("Agent roles file not found")
                self.agent_roles = {}

            # Load agent locations
            locations_file = self.repo_root / "agent_complete_locations.json"
            if locations_file.exists():
                with open(locations_file, "r") as f:
                    self.agent_locations = json.load(f)
                self.logger.info("Agent locations loaded successfully")
            else:
                self.logger.warning("Agent locations file not found")
                self.agent_locations = {}

        except Exception as e:
            self.logger.error(f"Error loading agent configs: {e}")
            self.agent_configs = {}
    
    def get_agent_configuration(self, agent_id: str) -> Optional[AgentConfiguration]:
        """Get configuration for a specific agent"""
        try:
            # Get agent role
            agent_role = self.agent_roles.get(agent_id, "unknown")
            
            # Get agent location
            agent_location = self.agent_locations.get(agent_id, "unknown")
            
            # Create agent configuration
            config = AgentConfiguration(
                agent_id=agent_id,
                agent_name=f"Agent-{agent_id.split('-')[-1]}" if '-' in agent_id else agent_id,
                agent_type=agent_role,
                current_location=agent_location,
                capabilities=self._get_default_capabilities(agent_role),
                limitations=self._get_default_limitations(agent_role),
                integration_status="pending",
                last_updated=Path().stat().st_mtime
            )
            
            return config
            
        except Exception as e:
            self.logger.error(f"Error getting agent configuration for {agent_id}: {e}")
            return None
    
    def _get_default_capabilities(self, agent_role: str) -> List[str]:
        """Get default capabilities based on agent role"""
        default_capabilities = {
            "foundation": ["basic_communication", "task_execution", "status_reporting"],
            "testing": ["test_execution", "result_validation", "bug_reporting"],
            "development": ["code_generation", "debugging", "optimization"],
            "coordination": ["task_assignment", "workflow_management", "resource_allocation"],
            "monitoring": ["health_checking", "performance_tracking", "alert_generation"],
            "integration": ["api_communication", "data_transformation", "protocol_handling"]
        }
        
        return default_capabilities.get(agent_role.lower(), ["basic_functionality"])
    
    def _get_default_limitations(self, agent_role: str) -> List[str]:
        """Get default limitations based on agent role"""
        default_limitations = {
            "foundation": ["limited_autonomy", "basic_decision_making"],
            "testing": ["test_creation_limitations", "complex_scenario_handling"],
            "development": ["code_review_limitations", "architecture_planning"],
            "coordination": ["conflict_resolution", "priority_optimization"],
            "monitoring": ["predictive_analysis", "anomaly_detection"],
            "integration": ["protocol_adaptation", "error_recovery"]
        }
        
        return default_limitations.get(agent_role.lower(), ["general_limitations"])
    
    def get_all_agent_ids(self) -> List[str]:
        """Get list of all available agent IDs"""
        agent_ids = set()
        
        # Add agents from roles
        agent_ids.update(self.agent_roles.keys())
        
        # Add agents from locations
        agent_ids.update(self.agent_locations.keys())
        
        return sorted(list(agent_ids))
    
    def get_agent_role(self, agent_id: str) -> str:
        """Get role for a specific agent"""
        return self.agent_roles.get(agent_id, "unknown")
    
    def get_agent_location(self, agent_id: str) -> str:
        """Get location for a specific agent"""
        return self.agent_locations.get(agent_id, "unknown")
    
    def update_agent_configuration(self, agent_id: str, updates: Dict[str, Any]) -> bool:
        """Update agent configuration"""
        try:
            if agent_id in self.agent_roles:
                self.agent_roles[agent_id].update(updates)
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error updating agent configuration for {agent_id}: {e}")
            return False
    
    def save_configurations(self) -> bool:
        """Save current configurations to files"""
        try:
            # Save agent roles
            roles_file = self.repo_root / "config" / "agents" / "agent_roles.json"
            roles_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(roles_file, "w") as f:
                json.dump(self.agent_roles, f, indent=2)
            
            # Save agent locations
            locations_file = self.repo_root / "agent_complete_locations.json"
            with open(locations_file, "w") as f:
                json.dump(self.agent_locations, f, indent=2)
            
            self.logger.info("Agent configurations saved successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving agent configurations: {e}")
            return False
