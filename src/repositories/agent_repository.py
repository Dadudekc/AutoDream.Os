"""
Agent Repository - Data Access Layer
=====================================

Handles all agent-related data operations including status management,
workspace access, and agent information retrieval.

Author: Agent-7 - Repository Cloning Specialist
Mission: Quarantine Fix Phase 3 (Repository Pattern)
Date: 2025-10-16
Points: 300 pts
V2 Compliant: ≤400 lines, single responsibility

Architecture:
- Follows repository pattern (data access abstraction)
- No business logic (data operations only)
- Type hints for all methods
- Comprehensive error handling

Usage:
    from src.repositories import AgentRepository
    
    repo = AgentRepository()
    agent = repo.get_agent("Agent-7")
    agents = repo.get_all_agents()
    repo.update_agent_status("Agent-7", {"status": "ACTIVE"})
"""

from typing import List, Optional, Dict, Any
from pathlib import Path
import json
import logging

logger = logging.getLogger(__name__)


class AgentRepository:
    """
    Repository for agent data operations.
    
    Provides data access methods for agent workspaces, status files,
    and agent configuration data.
    """
    
    def __init__(self, workspace_root: str = "agent_workspaces"):
        """
        Initialize agent repository.
        
        Args:
            workspace_root: Root directory for agent workspaces
        """
        self.workspace_root = Path(workspace_root)
        self.agents = [
            "Agent-1", "Agent-2", "Agent-3", "Agent-4",
            "Agent-5", "Agent-6", "Agent-7", "Agent-8"
        ]
    
    def get_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """
        Get agent by ID.
        
        Args:
            agent_id: Agent identifier (e.g., "Agent-7")
            
        Returns:
            Agent data dictionary or None if not found
        """
        try:
            status_file = self.workspace_root / agent_id / "status.json"
            
            if not status_file.exists():
                logger.warning(f"Agent {agent_id} status file not found")
                return None
            
            with open(status_file, 'r', encoding='utf-8') as f:
                agent_data = json.load(f)
            
            return agent_data
            
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing status file for {agent_id}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error reading agent {agent_id}: {e}")
            return None
    
    def get_all_agents(self) -> List[Dict[str, Any]]:
        """
        Get all agents.
        
        Returns:
            List of agent data dictionaries
        """
        agents_data = []
        
        for agent_id in self.agents:
            agent_data = self.get_agent(agent_id)
            if agent_data:
                agents_data.append(agent_data)
        
        return agents_data
    
    def update_agent_status(
        self, 
        agent_id: str, 
        status_update: Dict[str, Any]
    ) -> bool:
        """
        Update agent status.
        
        Args:
            agent_id: Agent identifier
            status_update: Dictionary with status fields to update
            
        Returns:
            True if successful, False otherwise
        """
        try:
            status_file = self.workspace_root / agent_id / "status.json"
            
            if not status_file.exists():
                logger.error(f"Status file not found for {agent_id}")
                return False
            
            # Read current status
            with open(status_file, 'r', encoding='utf-8') as f:
                current_status = json.load(f)
            
            # Merge updates
            current_status.update(status_update)
            
            # Write updated status
            with open(status_file, 'w', encoding='utf-8') as f:
                json.dump(current_status, f, indent=2)
            
            logger.info(f"Updated status for {agent_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating status for {agent_id}: {e}")
            return False
    
    def get_agent_inbox(self, agent_id: str) -> List[Dict[str, Any]]:
        """
        Get agent inbox messages.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            List of message dictionaries
        """
        try:
            inbox_dir = self.workspace_root / agent_id / "inbox"
            
            if not inbox_dir.exists():
                logger.warning(f"Inbox directory not found for {agent_id}")
                return []
            
            messages = []
            
            # Read all message files
            for message_file in inbox_dir.glob("*.md"):
                try:
                    with open(message_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    messages.append({
                        "file": message_file.name,
                        "content": content,
                        "path": str(message_file)
                    })
                except Exception as e:
                    logger.warning(f"Error reading message {message_file}: {e}")
            
            return messages
            
        except Exception as e:
            logger.error(f"Error reading inbox for {agent_id}: {e}")
            return []
    
    def get_agent_workspace_path(self, agent_id: str) -> Optional[Path]:
        """
        Get agent workspace path.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            Path object or None if not found
        """
        workspace_path = self.workspace_root / agent_id
        
        if workspace_path.exists():
            return workspace_path
        
        logger.warning(f"Workspace not found for {agent_id}")
        return None
    
    def agent_exists(self, agent_id: str) -> bool:
        """
        Check if agent exists.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            True if agent workspace exists, False otherwise
        """
        return (self.workspace_root / agent_id).exists()
    
    def get_agent_count(self) -> int:
        """
        Get total agent count.
        
        Returns:
            Number of agents
        """
        return len(self.agents)
    
    def get_active_agents(self) -> List[Dict[str, Any]]:
        """
        Get all active agents.
        
        Returns:
            List of active agent data dictionaries
        """
        all_agents = self.get_all_agents()
        
        active_agents = [
            agent for agent in all_agents
            if agent.get('status') == 'ACTIVE_AGENT_MODE'
        ]
        
        return active_agents
    
    def create_agent_workspace(self, agent_id: str) -> bool:
        """
        Create agent workspace structure.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            True if successful, False otherwise
        """
        try:
            workspace_path = self.workspace_root / agent_id
            
            if workspace_path.exists():
                logger.info(f"Workspace already exists for {agent_id}")
                return True
            
            # Create workspace structure
            workspace_path.mkdir(parents=True, exist_ok=True)
            (workspace_path / "inbox").mkdir(exist_ok=True)
            
            # Create initial status file
            status_data = {
                "agent_id": agent_id,
                "status": "INITIALIZED",
                "workspace_created": True
            }
            
            status_file = workspace_path / "status.json"
            with open(status_file, 'w', encoding='utf-8') as f:
                json.dump(status_data, f, indent=2)
            
            logger.info(f"Created workspace for {agent_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating workspace for {agent_id}: {e}")
            return False

