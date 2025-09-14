"""
Agent Assignment Manager
========================

Manages agent assignments and principle allocations.
"""

import logging
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class AgentAssignment:
    """Represents an agent assignment."""
    agent_id: str
    principle: str
    priority: int
    status: str = "assigned"
    created_at: Optional[str] = None


class AgentAssignmentManager:
    """Manages agent assignments and principle allocations."""
    
    def __init__(self):
        """Initialize the assignment manager."""
        self.logger = logging.getLogger(__name__)
        self.assignments: Dict[str, List[AgentAssignment]] = {}
        self.principle_assignments: Dict[str, List[str]] = {}
    
    def assign_agent(self, agent_id: str, principle: str, priority: int = 1) -> bool:
        """Assign an agent to a principle."""
        try:
            assignment = AgentAssignment(
                agent_id=agent_id,
                principle=principle,
                priority=priority
            )
            
            # Track by agent
            if agent_id not in self.assignments:
                self.assignments[agent_id] = []
            self.assignments[agent_id].append(assignment)
            
            # Track by principle
            if principle not in self.principle_assignments:
                self.principle_assignments[principle] = []
            self.principle_assignments[principle].append(agent_id)
            
            self.logger.info(f"Assigned agent {agent_id} to principle {principle}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to assign agent {agent_id}: {e}")
            return False
    
    def get_agent_assignments(self, agent_id: str) -> List[AgentAssignment]:
        """Get assignments for a specific agent."""
        return self.assignments.get(agent_id, [])
    
    def get_principle_agents(self, principle: str) -> List[str]:
        """Get agents assigned to a specific principle."""
        return self.principle_assignments.get(principle, [])
    
    def remove_assignment(self, agent_id: str, principle: str) -> bool:
        """Remove an assignment."""
        try:
            # Remove from agent assignments
            if agent_id in self.assignments:
                self.assignments[agent_id] = [
                    a for a in self.assignments[agent_id]
                    if a.principle != principle
                ]
            
            # Remove from principle assignments
            if principle in self.principle_assignments:
                self.principle_assignments[principle] = [
                    a for a in self.principle_assignments[principle]
                    if a != agent_id
                ]
            
            self.logger.info(f"Removed assignment: agent {agent_id} from principle {principle}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to remove assignment: {e}")
            return False

