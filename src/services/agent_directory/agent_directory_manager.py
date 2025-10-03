#!/usr/bin/env python3
"""
Agent Directory Manager - V2 Compliant
======================================

Manages agent directory, discovery, and registration for V2_SWARM system.
Provides centralized agent management and status tracking.

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
class AgentInfo:
    """Agent information structure."""
    
    agent_id: str
    name: str
    status: str
    coordinates: List[int]
    capabilities: List[str]
    current_role: Optional[str] = None
    last_seen: str = ""
    health_status: str = "unknown"
    
    def __post_init__(self):
        if not self.last_seen:
            self.last_seen = datetime.now().isoformat()


class AgentDirectoryManager:
    """Manages agent directory and registration."""
    
    def __init__(self, workspace_root: str = "agent_workspaces"):
        """Initialize agent directory manager."""
        self.workspace_root = Path(workspace_root)
        self.agents: Dict[str, AgentInfo] = {}
        self.registry_file = self.workspace_root / "agent_registry.json"
        
        # Load existing registry
        self._load_registry()
        
        logger.info(f"Agent Directory Manager initialized with {len(self.agents)} agents")
    
    def discover_agents(self) -> List[str]:
        """Discover all agents in workspace."""
        discovered_agents = []
        
        if not self.workspace_root.exists():
            logger.warning(f"Workspace root not found: {self.workspace_root}")
            return discovered_agents
        
        for agent_dir in self.workspace_root.iterdir():
            if agent_dir.is_dir() and agent_dir.name.startswith("Agent-"):
                discovered_agents.append(agent_dir.name)
        
        logger.info(f"Discovered {len(discovered_agents)} agents: {discovered_agents}")
        return discovered_agents
    
    def register_agent(self, agent_id: str) -> bool:
        """Register agent in directory."""
        try:
            # Load agent configuration
            agent_config = self._load_agent_config(agent_id)
            if not agent_config:
                logger.error(f"Failed to load config for {agent_id}")
                return False
            
            # Create agent info
            agent_info = AgentInfo(
                agent_id=agent_id,
                name=agent_config.get("name", f"{agent_id} Specialist"),
                status=agent_config.get("status", "UNKNOWN"),
                coordinates=agent_config.get("coordinates", [0, 0]),
                capabilities=agent_config.get("capabilities", []),
                current_role=agent_config.get("current_role"),
                health_status=self._check_agent_health(agent_id)
            )
            
            # Register agent
            self.agents[agent_id] = agent_info
            self._save_registry()
            
            logger.info(f"Registered agent: {agent_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error registering agent {agent_id}: {e}")
            return False
    
    def get_agent_status(self, agent_id: str) -> Dict[str, Any]:
        """Get agent status."""
        if agent_id not in self.agents:
            return {"error": f"Agent {agent_id} not found"}
        
        agent = self.agents[agent_id]
        return {
            "agent_id": agent.agent_id,
            "name": agent.name,
            "status": agent.status,
            "coordinates": agent.coordinates,
            "capabilities": agent.capabilities,
            "current_role": agent.current_role,
            "last_seen": agent.last_seen,
            "health_status": agent.health_status
        }
    
    def sync_agent_status(self, agent_id: str) -> bool:
        """Sync agent status across systems."""
        try:
            if agent_id not in self.agents:
                logger.warning(f"Agent {agent_id} not registered")
                return False
            
            # Load current status from workspace
            status_file = self.workspace_root / agent_id / "status.json"
            if status_file.exists():
                with open(status_file) as f:
                    status_data = json.load(f)
                
                # Update agent info
                agent = self.agents[agent_id]
                agent.status = status_data.get("status", agent.status)
                agent.current_role = status_data.get("current_role", agent.current_role)
                agent.last_seen = datetime.now().isoformat()
                agent.health_status = self._check_agent_health(agent_id)
                
                # Save updated registry
                self._save_registry()
                
                logger.info(f"Synced status for {agent_id}")
                return True
            else:
                logger.warning(f"Status file not found for {agent_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error syncing status for {agent_id}: {e}")
            return False
    
    def get_active_agents(self) -> List[str]:
        """Get list of active agents."""
        return [agent_id for agent_id, agent in self.agents.items() 
                if agent.status == "ACTIVE"]
    
    def get_all_agents(self) -> List[str]:
        """Get list of all registered agents."""
        return list(self.agents.keys())
    
    def update_agent_role(self, agent_id: str, role: str) -> bool:
        """Update agent's current role."""
        if agent_id not in self.agents:
            logger.warning(f"Agent {agent_id} not registered")
            return False
        
        self.agents[agent_id].current_role = role
        self.agents[agent_id].last_seen = datetime.now().isoformat()
        self._save_registry()
        
        logger.info(f"Updated role for {agent_id}: {role}")
        return True
    
    def _load_agent_config(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Load agent configuration from capabilities file."""
        try:
            capabilities_file = Path("config/agent_capabilities.json")
            if not capabilities_file.exists():
                logger.error("Agent capabilities file not found")
                return None
            
            with open(capabilities_file) as f:
                capabilities_data = json.load(f)
            
            agents_config = capabilities_data.get("agents", {})
            return agents_config.get(agent_id)
            
        except Exception as e:
            logger.error(f"Error loading agent config for {agent_id}: {e}")
            return None
    
    def _check_agent_health(self, agent_id: str) -> str:
        """Check agent health status."""
        try:
            workspace_dir = self.workspace_root / agent_id
            if not workspace_dir.exists():
                return "missing_workspace"
            
            status_file = workspace_dir / "status.json"
            if not status_file.exists():
                return "missing_status"
            
            with open(status_file) as f:
                status_data = json.load(f)
            
            # Check if status is recent (within last hour)
            last_update = status_data.get("last_update", "")
            if last_update:
                try:
                    last_update_time = datetime.fromisoformat(last_update)
                    time_diff = datetime.now() - last_update_time
                    if time_diff.total_seconds() > 3600:  # 1 hour
                        return "stale"
                except ValueError:
                    return "invalid_timestamp"
            
            return "healthy"
            
        except Exception as e:
            logger.error(f"Error checking health for {agent_id}: {e}")
            return "error"
    
    def _load_registry(self):
        """Load agent registry from file."""
        try:
            if self.registry_file.exists():
                with open(self.registry_file) as f:
                    registry_data = json.load(f)
                
                # Convert dict data back to AgentInfo objects
                for agent_id, agent_data in registry_data.get("agents", {}).items():
                    self.agents[agent_id] = AgentInfo(**agent_data)
                
                logger.info(f"Loaded registry with {len(self.agents)} agents")
            else:
                logger.info("No existing registry found, starting fresh")
                
        except Exception as e:
            logger.error(f"Error loading registry: {e}")
    
    def _save_registry(self):
        """Save agent registry to file."""
        try:
            registry_data = {
                "last_updated": datetime.now().isoformat(),
                "agents": {}
            }
            
            # Convert AgentInfo objects to dict
            for agent_id, agent in self.agents.items():
                registry_data["agents"][agent_id] = {
                    "agent_id": agent.agent_id,
                    "name": agent.name,
                    "status": agent.status,
                    "coordinates": agent.coordinates,
                    "capabilities": agent.capabilities,
                    "current_role": agent.current_role,
                    "last_seen": agent.last_seen,
                    "health_status": agent.health_status
                }
            
            with open(self.registry_file, "w") as f:
                json.dump(registry_data, f, indent=2)
            
            logger.info(f"Saved registry with {len(self.agents)} agents")
            
        except Exception as e:
            logger.error(f"Error saving registry: {e}")


def main():
    """CLI interface for agent directory manager."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Agent Directory Manager CLI")
    parser.add_argument("--discover", action="store_true", help="Discover all agents")
    parser.add_argument("--register", action="store_true", help="Register all discovered agents")
    parser.add_argument("--status", help="Get status for specific agent")
    parser.add_argument("--sync", help="Sync status for specific agent")
    parser.add_argument("--active", action="store_true", help="List active agents")
    parser.add_argument("--all", action="store_true", help="List all agents")
    parser.add_argument("--health", action="store_true", help="Check health of all agents")
    
    args = parser.parse_args()
    
    manager = AgentDirectoryManager()
    
    if args.discover:
        agents = manager.discover_agents()
        print("Discovered Agents:")
        for agent in agents:
            print(f"  - {agent}")
    
    elif args.register:
        agents = manager.discover_agents()
        print("Registering agents...")
        for agent in agents:
            success = manager.register_agent(agent)
            status = "✅" if success else "❌"
            print(f"  {status} {agent}")
    
    elif args.status:
        status = manager.get_agent_status(args.status)
        print(f"Status for {args.status}:")
        print(json.dumps(status, indent=2))
    
    elif args.sync:
        success = manager.sync_agent_status(args.sync)
        status = "✅" if success else "❌"
        print(f"  {status} Synced {args.sync}")
    
    elif args.active:
        agents = manager.get_active_agents()
        print("Active Agents:")
        for agent in agents:
            print(f"  - {agent}")
    
    elif args.all:
        agents = manager.get_all_agents()
        print("All Registered Agents:")
        for agent in agents:
            print(f"  - {agent}")
    
    elif args.health:
        print("Agent Health Status:")
        for agent_id in manager.get_all_agents():
            health = manager.agents[agent_id].health_status
            status_icon = "🟢" if health == "healthy" else "🔴"
            print(f"  {status_icon} {agent_id}: {health}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
