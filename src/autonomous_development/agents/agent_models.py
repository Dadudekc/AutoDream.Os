#!/usr/bin/env python3
"""
Agent Models - Agent Cellphone V2
=================================

Data models and structures for agent management.
Follows V2 standards: SRP, clean data structures.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from datetime import datetime
from typing import List
from dataclasses import dataclass

from src.core.enums import AgentRole


@dataclass
class AgentInfo:
    """Agent information and capabilities"""
    agent_id: str
    name: str
    role: AgentRole
    skills: List[str]
    max_concurrent_tasks: int
    is_active: bool = True
    last_heartbeat: datetime = None
    current_tasks: List[str] = None
    
    def __post_init__(self):
        if self.current_tasks is None:
            self.current_tasks = []
        if self.last_heartbeat is None:
            self.last_heartbeat = datetime.now()


@dataclass
class AgentStats:
    """Agent management statistics"""
    total_agents_registered: int = 0
    active_agents: int = 0
