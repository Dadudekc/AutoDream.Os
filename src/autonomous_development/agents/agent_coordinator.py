#!/usr/bin/env python3
"""
Agent Coordinator - Agent Cellphone V2
=====================================

Coordinates autonomous agents for development tasks.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
import time
import json
from pathlib import Path

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, List, Optional, Set, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
from ..core.enums import AgentRole, TaskStatus
from ..core.models import DevelopmentTask


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


class AgentCoordinator:
    """Coordinates autonomous agents for development tasks"""
    
    def __init__(self):
        self.agents: Dict[str, AgentInfo] = {}
        self.logger = logging.getLogger(__name__)
        self.coordination_stats = {
            "total_agents_registered": 0,
            "active_agents": 0,
            "total_task_assignments": 0,
            "successful_assignments": 0,
            "failed_assignments": 0,
        }
        
        # Initialize with sample agents
        self._initialize_sample_agents()
        
        # Phase 3 contract support
        self.phase3_contracts: Dict[str, Dict[str, Any]] = {}
        self.phase3_assignments: Dict[str, List[str]] = {}
    
    def _initialize_sample_agents(self):
        """Initialize with sample development agents"""
        sample_agents = [
            {
                "agent_id": "agent_1",
                "name": "Agent-1 (Coordinator)",
                "role": AgentRole.COORDINATOR,
                "skills": ["coordination", "planning", "monitoring"],
                "max_concurrent_tasks": 1
            },
            {
                "agent_id": "agent_2",
                "name": "Agent-2 (Worker)",
                "role": AgentRole.WORKER,
                "skills": ["git", "code_analysis", "optimization", "testing"],
                "max_concurrent_tasks": 3
            },
            {
                "agent_id": "agent_3",
                "name": "Agent-3 (Worker)",
                "role": AgentRole.WORKER,
                "skills": ["documentation", "markdown", "api_design", "security"],
                "max_concurrent_tasks": 2
            },
            {
                "agent_id": "agent_4",
                "name": "Agent-4 (Monitor)",
                "role": AgentRole.MONITOR,
                "skills": ["monitoring", "reporting", "quality_assurance"],
                "max_concurrent_tasks": 1
            },
            {
                "agent_id": "agent_5",
                "name": "Agent-5 (Validator)",
                "role": AgentRole.VALIDATOR,
                "skills": ["code_review", "testing", "validation"],
                "max_concurrent_tasks": 2
            }
        ]
        
        for agent_data in sample_agents:
            self.register_agent(**agent_data)
    
    def register_agent(self, agent_id: str, name: str, role: AgentRole,
                      skills: List[str], max_concurrent_tasks: int) -> bool:
        """Register a new agent"""
        if agent_id in self.agents:
            self.logger.warning(f"Agent {agent_id} already registered")
            return False
        
        agent = AgentInfo(
            agent_id=agent_id,
            name=name,
            role=role,
            skills=skills,
            max_concurrent_tasks=max_concurrent_tasks
        )
        
        self.agents[agent_id] = agent
        self.coordination_stats["total_agents_registered"] += 1
        self.coordination_stats["active_agents"] += 1
        
        self.logger.info(f"Registered agent {agent_id}: {name} ({role.value})")
        return True
    
    def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent"""
        if agent_id not in self.agents:
            return False
        
        agent = self.agents[agent_id]
        if agent.is_active:
            self.coordination_stats["active_agents"] -= 1
        
        del self.agents[agent_id]
        self.logger.info(f"Unregistered agent {agent_id}")
        return True
    
    def update_agent_heartbeat(self, agent_id: str) -> bool:
        """Update agent heartbeat"""
        if agent_id not in self.agents:
            return False
        
        agent = self.agents[agent_id]
        agent.last_heartbeat = datetime.now()
        
        # Reactivate if was inactive
        if not agent.is_active:
            agent.is_active = True
            self.coordination_stats["active_agents"] += 1
            self.logger.info(f"Agent {agent_id} reactivated")
        
        return True
    
    def deactivate_agent(self, agent_id: str) -> bool:
        """Deactivate an agent"""
        if agent_id not in self.agents:
            return False
        
        agent = self.agents[agent_id]
        if agent.is_active:
            agent.is_active = False
            self.coordination_stats["active_agents"] -= 1
            self.logger.info(f"Agent {agent_id} deactivated")
            return True
        
        return False
    
    def get_agent(self, agent_id: str) -> Optional[AgentInfo]:
        """Get agent information"""
        return self.agents.get(agent_id)
    
    def get_active_agents(self) -> List[AgentInfo]:
        """Get all active agents"""
        return [agent for agent in self.agents.values() if agent.is_active]
    
    def get_agents_by_role(self, role: AgentRole) -> List[AgentInfo]:
        """Get agents by role"""
        return [agent for agent in self.agents.values() if agent.role == role]
    
    def get_agents_with_skill(self, skill: str) -> List[AgentInfo]:
        """Get agents with a specific skill"""
        return [agent for agent in self.agents.values() if skill in agent.skills]
    
    def get_available_agents(self) -> List[AgentInfo]:
        """Get agents available for new tasks"""
        return [
            agent for agent in self.agents.values()
            if (agent.is_active and 
                len(agent.current_tasks) < agent.max_concurrent_tasks)
        ]
    
    def assign_task_to_agent(self, task: DevelopmentTask, agent_id: str) -> bool:
        """Assign a task to an agent"""
        if agent_id not in self.agents:
            return False
        
        agent = self.agents[agent_id]
        if not agent.is_active:
            return False
        
        if len(agent.current_tasks) >= agent.max_concurrent_tasks:
            return False
        
        # Check if agent has required skills
        required_skills = set(task.required_skills)
        agent_skills = set(agent.skills)
        if not required_skills.issubset(agent_skills):
            missing_skills = required_skills - agent_skills
            self.logger.warning(f"Agent {agent_id} missing skills: {missing_skills}")
            return False
        
        # Assign the task
        if task.claim(agent_id):
            agent.current_tasks.append(task.task_id)
            self.coordination_stats["total_task_assignments"] += 1
            self.coordination_stats["successful_assignments"] += 1
            
            self.logger.info(f"Assigned task {task.task_id} to agent {agent_id}")
            return True
        
        self.coordination_stats["failed_assignments"] += 1
        return False
    
    def unassign_task_from_agent(self, task_id: str, agent_id: str) -> bool:
        """Unassign a task from an agent"""
        if agent_id not in self.agents:
            return False
        
        agent = self.agents[agent_id]
        if task_id in agent.current_tasks:
            agent.current_tasks.remove(task_id)
            self.logger.info(f"Unassigned task {task_id} from agent {agent_id}")
            return True
        
        return False
    
    def find_best_agent_for_task(self, task: DevelopmentTask) -> Optional[AgentInfo]:
        """Find the best agent for a specific task"""
        available_agents = self.get_available_agents()
        if not available_agents:
            return None
        
        # Score agents based on skills match and current workload
        best_agent = None
        best_score = -1
        
        for agent in available_agents:
            # Calculate skills match score
            required_skills = set(task.required_skills)
            agent_skills = set(agent.skills)
            skills_match = len(required_skills.intersection(agent_skills))
            
            # Calculate workload score (lower is better)
            workload_ratio = len(agent.current_tasks) / agent.max_concurrent_tasks
            
            # Combined score (skills match weighted more than workload)
            score = (skills_match * 10) - (workload_ratio * 5)
            
            if score > best_score:
                best_score = score
                best_agent = agent
        
        return best_agent if best_score > 0 else None
    
    def get_agent_statistics(self) -> Dict[str, Any]:
        """Get comprehensive agent statistics."""
        active_agents = [agent for agent in self.agents.values() if agent.is_active]
        inactive_agents = [agent for agent in self.agents.values() if not agent.is_active]
        
        return {
            "total_agents": len(self.agents),
            "active_agents": len(active_agents),
            "inactive_agents": len(inactive_agents),
            "total_skills": sum(len(agent.skills) for agent in self.agents.values()),
            "avg_skills_per_agent": sum(len(agent.skills) for agent in self.agents.values()) / len(self.agents) if self.agents else 0,
            "total_tasks_assigned": sum(len(agent.current_tasks) for agent in self.agents.values()),
            "avg_tasks_per_agent": sum(len(agent.current_tasks) for agent in self.agents.values()) / len(self.agents) if self.agents else 0
        }
    
    def get_all_agents(self) -> List[AgentInfo]:
        """Get all registered agents."""
        return list(self.agents.values())
    
    def cleanup_inactive_agents(self, max_inactive_time: int = 3600) -> int:
        """Remove agents that haven't sent heartbeat for specified time"""
        timeout = timedelta(minutes=max_inactive_time)
        cutoff_time = datetime.now() - timeout
        removed_count = 0
        
        agent_ids_to_remove = []
        for agent_id, agent in self.agents.items():
            if (agent.last_heartbeat and 
                agent.last_heartbeat < cutoff_time and
                agent.role != AgentRole.COORDINATOR):  # Don't remove coordinator
                agent_ids_to_remove.append(agent_id)
        
        for agent_id in agent_ids_to_remove:
            self.unregister_agent(agent_id)
            removed_count += 1
        
        self.logger.info(f"Removed {removed_count} inactive agents")
        return removed_count
    
    def get_agent_workload_summary(self) -> Dict[str, any]:
        """Get summary of agent workloads"""
        workload_summary = {}
        
        for agent_id, agent in self.agents.items():
            workload_summary[agent_id] = {
                "name": agent.name,
                "role": agent.role.value,
                "current_tasks": len(agent.current_tasks),
                "max_tasks": agent.max_concurrent_tasks,
                "workload_percentage": (len(agent.current_tasks) / agent.max_concurrent_tasks) * 100,
                "is_active": agent.is_active,
                "last_heartbeat": agent.last_heartbeat.isoformat() if agent.last_heartbeat else None
            }
        
        return workload_summary
    
    # Phase 3 Contract Management Methods
    
    def load_phase3_contracts(self, contracts_file: str = "contracts/phase3a_core_system_contracts.json") -> bool:
        """Load Phase 3 contracts from JSON file"""
        try:
            contracts_path = Path(contracts_file)
            if not contracts_path.exists():
                self.logger.error(f"Phase 3 contracts file not found: {contracts_file}")
                return False
            
            with open(contracts_path, 'r') as f:
                contracts_data = json.load(f)
            
            # Handle the actual structure: contracts are in a "contracts" array
            if "contracts" in contracts_data:
                contracts_array = contracts_data["contracts"]
                for contract_data in contracts_array:
                    contract_id = contract_data.get("contract_id", "")
                    if contract_id:
                        self.phase3_contracts[contract_id] = contract_data
                
                self.logger.info(f"Loaded {len(self.phase3_contracts)} Phase 3 contracts")
                return True
            else:
                self.logger.error("No 'contracts' array found in Phase 3 file")
                return False
                
        except Exception as e:
            self.logger.error(f"Error loading Phase 3 contracts: {e}")
            return False
    
    def assign_phase3_contracts_to_agents(self) -> Dict[str, List[str]]:
        """Assign Phase 3 contracts to available agents based on skills and workload"""
        if not self.phase3_contracts:
            self.logger.warning("No Phase 3 contracts loaded")
            return {}
        
        # Reset assignments
        self.phase3_assignments = {}
        
        # Sort contracts by priority and effort
        sorted_contracts = sorted(
            self.phase3_contracts.values(),
            key=lambda c: (self._phase3_priority_score(c.get("priority", "MEDIUM")), 
                          c.get("estimated_hours", 0.0)),
            reverse=True
        )
        
        assignments = {}
        
        for contract in sorted_contracts:
            contract_id = contract.get("contract_id", "")
            best_agent = self._find_best_agent_for_phase3_contract(contract)
            
            if best_agent:
                # Assign contract to agent
                if best_agent not in self.phase3_assignments:
                    self.phase3_assignments[best_agent] = []
                self.phase3_assignments[best_agent].append(contract_id)
                
                if best_agent not in assignments:
                    assignments[best_agent] = []
                assignments[best_agent].append(contract_id)
                
                self.logger.info(f"Assigned Phase 3 contract {contract_id} to {best_agent}")
            else:
                self.logger.warning(f"No suitable agent found for Phase 3 contract {contract_id}")
        
        return assignments
    
    def _find_best_agent_for_phase3_contract(self, contract: Dict[str, Any]) -> Optional[str]:
        """Find the best agent for a specific Phase 3 contract"""
        available_agents = self.get_available_agents()
        if not available_agents:
            return None
        
        best_agent = None
        best_score = -1
        
        for agent in available_agents:
            # Calculate skills match score
            contract_category = contract.get("category", "").lower()
            contract_description = contract.get("description", "").lower()
            contract_text = f"{contract_category} {contract_description}"
            
            skills_match = 0
            for skill in agent.skills:
                if skill.lower() in contract_text:
                    skills_match += 1
            
            # Calculate workload score (lower is better)
            workload_ratio = len(agent.current_tasks) / agent.max_concurrent_tasks
            
            # Combined score (skills match weighted more than workload)
            score = (skills_match * 10) - (workload_ratio * 5)
            
            if score > best_score:
                best_score = score
                best_agent = agent.agent_id
        
        return best_agent if best_score > 0 else None
    
    def _phase3_priority_score(self, priority: str) -> int:
        """Convert Phase 3 priority string to numeric score"""
        priority_map = {
            "CRITICAL": 4,
            "HIGH": 3,
            "MEDIUM": 2,
            "LOW": 1
        }
        return priority_map.get(priority, 2)
    
    def get_phase3_assignment_summary(self) -> Dict[str, Any]:
        """Get summary of Phase 3 contract assignments"""
        summary = {
            "total_contracts": len(self.phase3_contracts),
            "total_assigned": sum(len(contracts) for contracts in self.phase3_assignments.values()),
            "agent_assignments": {}
        }
        
        for agent_id, contracts in self.phase3_assignments.items():
            total_effort = 0.0
            for contract_id in contracts:
                contract = self.phase3_contracts.get(contract_id, {})
                total_effort += contract.get("estimated_hours", 0.0)
            
            agent = self.agents.get(agent_id)
            agent_name = agent.name if agent else "Unknown"
            summary["agent_assignments"][agent_id] = {
                "contracts": contracts,
                "effort": total_effort,
                "agent_name": agent_name
            }
        
        return summary
    
    def print_phase3_assignment_summary(self):
        """Print a formatted summary of Phase 3 assignments"""
        summary = self.get_phase3_assignment_summary()
        
        print("\n" + "="*80)
        print("🎯 PHASE 3 CONTRACT ASSIGNMENT SUMMARY")
        print("="*80)
        print(f"Total Contracts: {summary['total_contracts']}")
        print(f"Total Assigned: {summary['total_assigned']}")
        print()
        
        for agent_id, agent_data in summary["agent_assignments"].items():
            print(f"🤖 **{agent_id}** ({agent_data['agent_name']})")
            print(f"   Contracts: {len(agent_data['contracts'])}")
            print(f"   Effort: {agent_data['effort']:.1f} hours")
            
            if agent_data['contracts']:
                print("   Assigned Contracts:")
                for contract_id in agent_data['contracts']:
                    contract = self.phase3_contracts.get(contract_id, {})
                    file_path = contract.get("file_path", "Unknown")
                    print(f"     • {contract_id}: {file_path}")
            print()
    
    def send_phase3_assignments_to_agents(self, message_coordinator=None) -> bool:
        """Send Phase 3 contract assignments to agents using existing messaging system"""
        if not self.phase3_assignments:
            self.logger.warning("No Phase 3 assignments to send")
            return False
        
        success_count = 0
        total_assignments = 0
        
        for agent_id, contracts in self.phase3_assignments.items():
            if not contracts:
                continue
            
            total_assignments += 1
            message = self._format_phase3_assignment_message(agent_id, contracts)
            
            try:
                if message_coordinator:
                    # Use existing MessageCoordinator if available
                    task_id = message_coordinator.create_task(
                        title=f"Phase 3 Contract Assignment - {agent_id}",
                        description=message,
                        priority="HIGH",
                        assigned_agents=[agent_id],
                        estimated_hours=sum(
                            self.phase3_contracts.get(c, {}).get("estimated_hours", 0.0) 
                            for c in contracts
                        )
                    )
                    self.logger.info(f"Created task {task_id} for {agent_id}")
                    success_count += 1
                else:
                    # Fallback to direct logging
                    self.logger.info(f"Phase 3 assignment for {agent_id}: {message}")
                    success_count += 1
                    
            except Exception as e:
                self.logger.error(f"Error sending Phase 3 assignment to {agent_id}: {e}")
        
        self.logger.info(f"Sent {success_count}/{total_assignments} Phase 3 assignments")
        return success_count == total_assignments
    
    def _format_phase3_assignment_message(self, agent_id: str, contracts: List[str]) -> str:
        """Format Phase 3 assignment message for an agent"""
        agent = self.agents.get(agent_id)
        agent_name = agent.name if agent else agent_id
        
        message_lines = [
            f"🎯 **PHASE 3 CONTRACT ASSIGNMENTS - CAPTAIN'S ORDERS**",
            f"Agent: {agent_id} ({agent_name})",
            f"Total Contracts: {len(contracts)}",
            f"Priority: CRITICAL - Phase 3 Modularization",
            "",
            "**MISSION BRIEFING:**",
            "You have been assigned Phase 3 modularization contracts.",
            "These are critical for achieving V2 compliance standards.",
            "Execute with precision and report progress immediately.",
            "",
            "**ASSIGNED CONTRACTS:**"
        ]
        
        total_effort = 0.0
        for contract_id in contracts:
            contract = self.phase3_contracts.get(contract_id, {})
            if contract:
                effort = contract.get("estimated_hours", 0.0)
                total_effort += effort
                
                message_lines.extend([
                    f"",
                    f"📋 **{contract_id}**",
                    f"File: {contract.get('file_path', 'Unknown')}",
                    f"Current: {contract.get('current_lines', 0)} lines → Target: {contract.get('target_lines', 0)} lines",
                    f"Priority: {contract.get('priority', 'MEDIUM')}",
                    f"Effort: {effort:.1f} hours",
                    f"Category: {contract.get('category', 'Unknown')}",
                    "",
                    "**Refactoring Plan:**"
                ])
                
                refactoring_plan = contract.get("refactoring_plan", {})
                if isinstance(refactoring_plan, dict) and "extract_modules" in refactoring_plan:
                    for module in refactoring_plan["extract_modules"]:
                        message_lines.append(f"• Extract: {module}")
                else:
                    message_lines.append("• Modularize according to V2 standards")
                
                message_lines.extend([
                    "",
                    "**Success Criteria:**"
                ])
                
                success_criteria = contract.get("success_criteria", [])
                for criterion in success_criteria:
                    message_lines.append(f"✅ {criterion}")
        
        message_lines.extend([
            "",
            "**EXECUTION ORDERS:**",
            "1. Begin with highest priority contract",
            "2. Follow V2 modularization standards",
            "3. Maintain single responsibility principle",
            "4. Report progress every 2 hours",
            "5. Flag any blockers immediately",
            "",
            "**CAPTAIN'S EXPECTATIONS:**",
            f"Total Effort: {total_effort:.1f} hours",
            "Timeline: Execute with urgency",
            "Quality: Maintain V2 standards",
            "Communication: Keep team informed",
            "",
            "🚀 **READY TO EXECUTE - MAKE US PROUD!** 🚀",
            "",
            "Captain Agent-1 out. Over and out."
        ])
        
        return "\n".join(message_lines)
