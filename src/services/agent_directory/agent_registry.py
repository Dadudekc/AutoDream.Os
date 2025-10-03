#!/usr/bin/env python3
"""
Agent Registry - V2 Compliant
=============================

Central registry for all agents in V2_SWARM system.
Provides agent lookup, capability mapping, and role tracking.

Author: Agent-4 (Captain)
License: MIT
"""

import json
import logging
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

logger = logging.getLogger(__name__)


@dataclass
class AgentCapability:
    """Agent capability definition."""
    
    capability_id: str
    name: str
    description: str
    category: str
    required_for_roles: List[str]


@dataclass
class AgentRole:
    """Agent role definition."""
    
    role_id: str
    name: str
    description: str
    required_capabilities: List[str]
    priority_level: int


class AgentRegistry:
    """Central registry for all agents."""
    
    def __init__(self, registry_file: str = "agent_workspaces/agent_registry.json"):
        """Initialize agent registry."""
        self.registry_file = Path(registry_file)
        self.agents: Dict[str, Dict[str, Any]] = {}
        self.capabilities: Dict[str, AgentCapability] = {}
        self.roles: Dict[str, AgentRole] = {}
        
        # Load registry data
        self._load_registry()
        
        logger.info(f"Agent Registry initialized with {len(self.agents)} agents")
    
    def register_agent(self, agent_info: Dict[str, Any]) -> bool:
        """Register agent in registry."""
        try:
            agent_id = agent_info.get("agent_id")
            if not agent_id:
                logger.error("Agent ID is required")
                return False
            
            # Validate agent info
            required_fields = ["name", "status", "coordinates", "capabilities"]
            for field in required_fields:
                if field not in agent_info:
                    logger.error(f"Missing required field: {field}")
                    return False
            
            # Register agent
            self.agents[agent_id] = agent_info
            self._save_registry()
            
            logger.info(f"Registered agent: {agent_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error registering agent: {e}")
            return False
    
    def get_active_agents(self) -> List[str]:
        """Get list of active agents."""
        return [agent_id for agent_id, agent in self.agents.items() 
                if agent.get("status") == "ACTIVE"]
    
    def get_agent_capabilities(self, agent_id: str) -> List[str]:
        """Get agent capabilities."""
        if agent_id not in self.agents:
            logger.warning(f"Agent {agent_id} not found in registry")
            return []
        
        return self.agents[agent_id].get("capabilities", [])
    
    def get_agents_by_capability(self, capability: str) -> List[str]:
        """Get agents that have specific capability."""
        agents_with_capability = []
        
        for agent_id, agent in self.agents.items():
            capabilities = agent.get("capabilities", [])
            if capability in capabilities:
                agents_with_capability.append(agent_id)
        
        return agents_with_capability
    
    def get_agents_by_role(self, role: str) -> List[str]:
        """Get agents currently assigned to specific role."""
        agents_with_role = []
        
        for agent_id, agent in self.agents.items():
            current_role = agent.get("current_role")
            if current_role == role:
                agents_with_role.append(agent_id)
        
        return agents_with_role
    
    def assign_role(self, agent_id: str, role: str) -> bool:
        """Assign role to agent."""
        if agent_id not in self.agents:
            logger.error(f"Agent {agent_id} not found in registry")
            return False
        
        # Check if agent has required capabilities for role
        if not self._can_agent_perform_role(agent_id, role):
            logger.error(f"Agent {agent_id} cannot perform role {role}")
            return False
        
        # Assign role
        self.agents[agent_id]["current_role"] = role
        self.agents[agent_id]["last_role_update"] = datetime.now().isoformat()
        self._save_registry()
        
        logger.info(f"Assigned role {role} to {agent_id}")
        return True
    
    def remove_role(self, agent_id: str) -> bool:
        """Remove current role from agent."""
        if agent_id not in self.agents:
            logger.error(f"Agent {agent_id} not found in registry")
            return False
        
        # Remove role
        self.agents[agent_id]["current_role"] = None
        self.agents[agent_id]["last_role_update"] = datetime.now().isoformat()
        self._save_registry()
        
        logger.info(f"Removed role from {agent_id}")
        return True
    
    def get_agent_info(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get complete agent information."""
        return self.agents.get(agent_id)
    
    def update_agent_status(self, agent_id: str, status: str) -> bool:
        """Update agent status."""
        if agent_id not in self.agents:
            logger.error(f"Agent {agent_id} not found in registry")
            return False
        
        self.agents[agent_id]["status"] = status
        self.agents[agent_id]["last_status_update"] = datetime.now().isoformat()
        self._save_registry()
        
        logger.info(f"Updated status for {agent_id}: {status}")
        return True
    
    def get_registry_summary(self) -> Dict[str, Any]:
        """Get registry summary statistics."""
        total_agents = len(self.agents)
        active_agents = len(self.get_active_agents())
        
        # Count agents by status
        status_counts = {}
        for agent in self.agents.values():
            status = agent.get("status", "UNKNOWN")
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # Count agents by role
        role_counts = {}
        for agent in self.agents.values():
            role = agent.get("current_role", "NO_ROLE")
            role_counts[role] = role_counts.get(role, 0) + 1
        
        return {
            "total_agents": total_agents,
            "active_agents": active_agents,
            "status_distribution": status_counts,
            "role_distribution": role_counts,
            "last_updated": datetime.now().isoformat()
        }
    
    def _can_agent_perform_role(self, agent_id: str, role: str) -> bool:
        """Check if agent can perform the specified role."""
        if agent_id not in self.agents:
            return False
        
        agent_capabilities = self.agents[agent_id].get("capabilities", [])
        
        # Load role requirements from capabilities file
        try:
            capabilities_file = Path("config/agent_capabilities.json")
            if capabilities_file.exists():
                with open(capabilities_file) as f:
                    capabilities_data = json.load(f)
                
                agents_config = capabilities_data.get("agents", {})
                agent_config = agents_config.get(agent_id, {})
                
                # Check if role is in agent's available roles
                default_roles = agent_config.get("default_roles", [])
                specialized_roles = agent_config.get("specialized_roles", [])
                all_available_roles = default_roles + specialized_roles
                
                return role in all_available_roles
            
        except Exception as e:
            logger.error(f"Error checking role capability: {e}")
        
        return False
    
    def _load_registry(self):
        """Load registry data from file."""
        try:
            if self.registry_file.exists():
                with open(self.registry_file) as f:
                    registry_data = json.load(f)
                
                self.agents = registry_data.get("agents", {})
                logger.info(f"Loaded registry with {len(self.agents)} agents")
            else:
                logger.info("No existing registry found, starting fresh")
                
        except Exception as e:
            logger.error(f"Error loading registry: {e}")
    
    def _save_registry(self):
        """Save registry data to file."""
        try:
            registry_data = {
                "last_updated": datetime.now().isoformat(),
                "agents": self.agents
            }
            
            with open(self.registry_file, "w") as f:
                json.dump(registry_data, f, indent=2)
            
            logger.info(f"Saved registry with {len(self.agents)} agents")
            
        except Exception as e:
            logger.error(f"Error saving registry: {e}")


def main():
    """CLI interface for agent registry."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Agent Registry CLI")
    parser.add_argument("--active", action="store_true", help="List active agents")
    parser.add_argument("--capabilities", help="Get capabilities for specific agent")
    parser.add_argument("--by-capability", help="Get agents with specific capability")
    parser.add_argument("--by-role", help="Get agents with specific role")
    parser.add_argument("--assign-role", nargs=2, metavar=("AGENT", "ROLE"), 
                       help="Assign role to agent")
    parser.add_argument("--remove-role", help="Remove role from agent")
    parser.add_argument("--summary", action="store_true", help="Show registry summary")
    
    args = parser.parse_args()
    
    registry = AgentRegistry()
    
    if args.active:
        agents = registry.get_active_agents()
        print("Active Agents:")
        for agent in agents:
            print(f"  - {agent}")
    
    elif args.capabilities:
        capabilities = registry.get_agent_capabilities(args.capabilities)
        print(f"Capabilities for {args.capabilities}:")
        for capability in capabilities:
            print(f"  - {capability}")
    
    elif args.by_capability:
        agents = registry.get_agents_by_capability(args.by_capability)
        print(f"Agents with capability '{args.by_capability}':")
        for agent in agents:
            print(f"  - {agent}")
    
    elif args.by_role:
        agents = registry.get_agents_by_role(args.by_role)
        print(f"Agents with role '{args.by_role}':")
        for agent in agents:
            print(f"  - {agent}")
    
    elif args.assign_role:
        agent_id, role = args.assign_role
        success = registry.assign_role(agent_id, role)
        status = "✅" if success else "❌"
        print(f"  {status} Assigned role {role} to {agent_id}")
    
    elif args.remove_role:
        success = registry.remove_role(args.remove_role)
        status = "✅" if success else "❌"
        print(f"  {status} Removed role from {args.remove_role}")
    
    elif args.summary:
        summary = registry.get_registry_summary()
        print("Registry Summary:")
        print(json.dumps(summary, indent=2))
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
