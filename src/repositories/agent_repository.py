"""
Agent Repository - Data Access Layer
====================================

Handles all agent-related data operations following the repository pattern.
This repository provides data access abstraction for agent workspaces, status,
and inbox operations.

Author: Agent-7 (Quarantine Mission Phase 3)
Date: 2025-10-16
Points: 300
"""

from typing import List, Optional, Dict, Any
from pathlib import Path
import json
from datetime import datetime


class AgentRepository:
    """
    Repository for agent data operations.
    
    Provides data access layer for agent workspaces, status files,
    and inbox messages. No business logic - pure data operations.
    
    Attributes:
        workspace_root: Root directory for agent workspaces
    """
    
    def __init__(self, workspace_root: str = "agent_workspaces"):
        """
        Initialize agent repository.
        
        Args:
            workspace_root: Root directory for agent workspaces (default: "agent_workspaces")
        """
        self.workspace_root = Path(workspace_root)
        
    def get_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """
        Get agent data by ID.
        
        Args:
            agent_id: Agent identifier (e.g., "Agent-7")
            
        Returns:
            Agent data dictionary if found, None otherwise
        """
        status_file = self.workspace_root / agent_id / "status.json"
        
        if not status_file.exists():
            return None
            
        try:
            with open(status_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    
    def get_all_agents(self) -> List[Dict[str, Any]]:
        """
        Get all agents from workspace.
        
        Returns:
            List of agent data dictionaries
        """
        agents = []
        
        if not self.workspace_root.exists():
            return agents
            
        for agent_dir in self.workspace_root.iterdir():
            if agent_dir.is_dir() and agent_dir.name.startswith('Agent-'):
                agent_data = self.get_agent(agent_dir.name)
                if agent_data:
                    agents.append(agent_data)
                    
        return agents
    
    def update_agent_status(self, agent_id: str, status_data: Dict[str, Any]) -> bool:
        """
        Update agent status file.
        
        Args:
            agent_id: Agent identifier (e.g., "Agent-7")
            status_data: Status data dictionary to save
            
        Returns:
            True if update successful, False otherwise
        """
        agent_dir = self.workspace_root / agent_id
        status_file = agent_dir / "status.json"
        
        # Create directory if doesn't exist
        agent_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(status_file, 'w', encoding='utf-8') as f:
                json.dump(status_data, f, indent=2, ensure_ascii=False)
            return True
        except IOError:
            return False
    
    def get_agent_inbox(self, agent_id: str) -> List[Dict[str, Any]]:
        """
        Get agent inbox messages.
        
        Args:
            agent_id: Agent identifier (e.g., "Agent-7")
            
        Returns:
            List of message file paths and metadata
        """
        inbox_dir = self.workspace_root / agent_id / "inbox"
        
        if not inbox_dir.exists():
            return []
            
        messages = []
        for msg_file in inbox_dir.glob("*.md"):
            messages.append({
                'filename': msg_file.name,
                'path': str(msg_file),
                'modified': datetime.fromtimestamp(msg_file.stat().st_mtime).isoformat(),
                'size': msg_file.stat().st_size
            })
            
        # Sort by modification time (newest first)
        messages.sort(key=lambda x: x['modified'], reverse=True)
        return messages
    
    def get_agent_workspace_path(self, agent_id: str) -> Path:
        """
        Get agent workspace directory path.
        
        Args:
            agent_id: Agent identifier (e.g., "Agent-7")
            
        Returns:
            Path object for agent workspace
        """
        return self.workspace_root / agent_id
    
    def agent_exists(self, agent_id: str) -> bool:
        """
        Check if agent workspace exists.
        
        Args:
            agent_id: Agent identifier (e.g., "Agent-7")
            
        Returns:
            True if agent workspace exists, False otherwise
        """
        return (self.workspace_root / agent_id).exists()
    
    def get_agent_notes(self, agent_id: str) -> List[Dict[str, Any]]:
        """
        Get agent notes from workspace.
        
        Args:
            agent_id: Agent identifier (e.g., "Agent-7")
            
        Returns:
            List of note file metadata
        """
        notes_dir = self.workspace_root / agent_id / "notes"
        
        if not notes_dir.exists():
            return []
            
        notes = []
        for note_file in notes_dir.glob("*.md"):
            notes.append({
                'filename': note_file.name,
                'path': str(note_file),
                'modified': datetime.fromtimestamp(note_file.stat().st_mtime).isoformat()
            })
            
        notes.sort(key=lambda x: x['modified'], reverse=True)
        return notes
