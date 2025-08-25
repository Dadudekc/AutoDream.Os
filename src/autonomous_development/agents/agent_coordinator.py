#!/usr/bin/env python3
"""
Agent Coordinator Orchestrator - Agent Cellphone V2
==================================================

Orchestrates agent coordination workflow using extracted modules.
Follows V2 standards: ≤400 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
from typing import Dict, List, Optional, Any

from .agent_management import AgentManager
from .agent_coordination import AgentCoordinator
from .agent_communication import AgentCommunication


class AgentCoordinatorOrchestrator:
    """Orchestrates agent coordination workflow using extracted modules"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize extracted modules
        self.agent_manager = AgentManager()
        self.agent_coordinator = AgentCoordinator(self.agent_manager)
        self.agent_communication = AgentCommunication(self.agent_manager)
        
        # Combined statistics
        self.orchestrator_stats = {
            "management_stats": self.agent_manager.management_stats,
            "coordination_stats": self.agent_coordinator.coordination_stats
        }
    
    # Agent Management Delegation
    def register_agent(self, agent_id: str, name: str, role, skills: List[str], max_concurrent_tasks: int) -> bool:
        """Register a new agent"""
        return self.agent_manager.register_agent(agent_id, name, role, skills, max_concurrent_tasks)
    
    def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent"""
        return self.agent_manager.unregister_agent(agent_id)
    
    def update_agent_heartbeat(self, agent_id: str) -> bool:
        """Update agent heartbeat"""
        return self.agent_manager.update_agent_heartbeat(agent_id)
    
    def deactivate_agent(self, agent_id: str) -> bool:
        """Deactivate an agent"""
        return self.agent_manager.deactivate_agent(agent_id)
    
    def get_agent(self, agent_id: str):
        """Get agent information"""
        return self.agent_manager.get_agent(agent_id)
    
    def get_active_agents(self) -> List:
        """Get all active agents"""
        return self.agent_manager.get_active_agents()
    
    def get_agents_by_role(self, role):
        """Get agents by role"""
        return self.agent_manager.get_agents_by_role(role)
    
    def get_agents_with_skill(self, skill: str) -> List:
        """Get agents with a specific skill"""
        return self.agent_manager.get_agents_with_skill(skill)
    
    def get_available_agents(self) -> List:
        """Get agents available for new tasks"""
        return self.agent_manager.get_available_agents()
    
    def get_all_agents(self) -> List:
        """Get all registered agents"""
        return self.agent_manager.get_all_agents()
    
    def cleanup_inactive_agents(self, max_inactive_time: int = 3600) -> int:
        """Remove inactive agents"""
        return self.agent_manager.cleanup_inactive_agents(max_inactive_time)
    
    def get_agent_statistics(self) -> Dict[str, any]:
        """Get comprehensive agent statistics"""
        return self.agent_manager.get_agent_statistics()
    
    def get_agent_workload_summary(self) -> Dict[str, any]:
        """Get summary of agent workloads"""
        return self.agent_manager.get_agent_workload_summary()
    
    # Task Coordination Delegation
    def assign_task_to_agent(self, task, agent_id: str) -> bool:
        """Assign a task to an agent"""
        return self.agent_coordinator.assign_task_to_agent(task, agent_id)
    
    def unassign_task_from_agent(self, task_id: str, agent_id: str) -> bool:
        """Unassign a task from an agent"""
        return self.agent_coordinator.unassign_task_from_agent(task_id, agent_id)
    
    def find_best_agent_for_task(self, task):
        """Find the best agent for a specific task"""
        return self.agent_coordinator.find_best_agent_for_task(task)
    
    # Phase 3 Contract Management Delegation
    def load_phase3_contracts(self, contracts_file: str = "contracts/phase3a_core_system_contracts.json") -> bool:
        """Load Phase 3 contracts from JSON file"""
        return self.agent_coordinator.load_phase3_contracts(contracts_file)
    
    def assign_phase3_contracts_to_agents(self) -> Dict[str, List[str]]:
        """Assign Phase 3 contracts to available agents"""
        return self.agent_coordinator.assign_phase3_contracts_to_agents()
    
    def get_phase3_assignment_summary(self) -> Dict[str, Any]:
        """Get summary of Phase 3 contract assignments"""
        return self.agent_coordinator.get_phase3_assignment_summary()
    
    def print_phase3_assignment_summary(self):
        """Print a formatted summary of Phase 3 assignments"""
        self.agent_coordinator.print_phase3_assignment_summary()
    
    # Communication Delegation
    def send_phase3_assignments_to_agents(self, message_coordinator=None) -> bool:
        """Send Phase 3 contract assignments to agents"""
        return self.agent_communication.send_phase3_assignments_to_agents(
            self.agent_coordinator.phase3_assignments,
            self.agent_coordinator.phase3_contracts,
            message_coordinator
        )
    
    # Swarm Command Delegation
    def take_command(self, agent_id: str) -> bool:
        """Allow any agent to take command of the swarm"""
        return self.agent_communication.take_command(agent_id)
    
    def get_command_capable_agents(self) -> List:
        """Get all agents capable of taking command"""
        return self.agent_communication.get_command_capable_agents()
    
    def execute_swarm_command(self, commander_id: str, command: str, target_agents: List[str] = None) -> bool:
        """Execute a swarm command from any capable agent"""
        return self.agent_communication.execute_swarm_command(commander_id, command, target_agents)
    
    def show_swarm_status(self, viewer_id: str = None) -> str:
        """Show current swarm status"""
        return self.agent_communication.show_swarm_status(viewer_id)
    
    # Orchestrator-specific methods
    def get_orchestrator_statistics(self) -> Dict[str, any]:
        """Get combined statistics from all modules"""
        return {
            "management": self.agent_manager.management_stats,
            "coordination": self.agent_coordinator.coordination_stats,
            "total_agents": len(self.agent_manager.agents),
            "active_agents": self.agent_manager.management_stats["active_agents"],
            "total_assignments": self.agent_coordinator.coordination_stats["total_task_assignments"]
        }
    
    def execute_phase3_workflow(self, message_coordinator=None) -> bool:
        """Execute complete Phase 3 workflow"""
        try:
            # Load contracts
            if not self.load_phase3_contracts():
                self.logger.error("Failed to load Phase 3 contracts")
                return False
            
            # Assign contracts to agents
            assignments = self.assign_phase3_contracts_to_agents()
            if not assignments:
                self.logger.warning("No Phase 3 contracts assigned")
                return False
            
            # Send assignments to agents
            if not self.send_phase3_assignments_to_agents(message_coordinator):
                self.logger.error("Failed to send Phase 3 assignments")
                return False
            
            # Print summary
            self.print_phase3_assignment_summary()
            
            self.logger.info("Phase 3 workflow executed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error executing Phase 3 workflow: {e}")
            return False


# Backward compatibility - maintain existing interface
class AgentCoordinator(AgentCoordinatorOrchestrator):
    """Backward compatibility alias for existing code"""
    pass