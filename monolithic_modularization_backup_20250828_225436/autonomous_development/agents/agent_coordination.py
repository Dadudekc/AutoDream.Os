#!/usr/bin/env python3
"""
Agent Coordination - Agent Cellphone V2
======================================

Handles task assignment and coordination logic between agents.
Follows V2 standards: SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
from typing import Dict, List, Optional, Any
from pathlib import Path
import json

from ..core.models import DevelopmentTask
from .agent_management import AgentManager, AgentInfo


class AgentCoordinator:
    """Coordinates task assignment and coordination between agents"""
    
    def __init__(self, agent_manager: AgentManager):
        self.agent_manager = agent_manager
        self.logger = logging.getLogger(__name__)
        self.coordination_stats = {
            "total_task_assignments": 0,
            "successful_assignments": 0,
            "failed_assignments": 0,
        }
        
        # Phase 3 contract support
        self.phase3_contracts: Dict[str, Dict[str, Any]] = {}
        self.phase3_assignments: Dict[str, List[str]] = {}
    
    def assign_task_to_agent(self, task: DevelopmentTask, agent_id: str) -> bool:
        """Assign a task to an agent"""
        if agent_id not in self.agent_manager.agents:
            return False
        
        agent = self.agent_manager.agents[agent_id]
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
        if agent_id not in self.agent_manager.agents:
            return False
        
        agent = self.agent_manager.agents[agent_id]
        if task_id in agent.current_tasks:
            agent.current_tasks.remove(task_id)
            self.logger.info(f"Unassigned task {task_id} from agent {agent_id}")
            return True
        
        return False
    
    def find_best_agent_for_task(self, task: DevelopmentTask) -> Optional[AgentInfo]:
        """Find the best agent for a specific task"""
        available_agents = self.agent_manager.get_available_agents()
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
        available_agents = self.agent_manager.get_available_agents()
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
            
            agent = self.agent_manager.agents.get(agent_id)
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
