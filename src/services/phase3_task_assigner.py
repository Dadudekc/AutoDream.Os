#!/usr/bin/env python3
"""
Phase 3 Task Assigner - Agent Cellphone V2
==========================================

Assigns Phase 3 modularization contracts to agents 1-4 via pyautogui messaging.
Single responsibility: Phase 3 contract assignment and messaging.
Follows V2 standards: OOP, SRP, clean production-grade code.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import json
import logging
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from ..utils.stability_improvements import stability_manager, safe_import
from .messaging.pyautogui_messaging import PyAutoGUIMessaging
from .messaging.coordinate_manager import CoordinateManager

logger = logging.getLogger(__name__)


@dataclass
class Phase3Contract:
    """Phase 3 contract data structure"""
    contract_id: str
    file_path: str
    current_lines: int
    target_lines: int
    priority: str
    category: str
    estimated_effort: float
    description: str
    refactoring_plan: List[str]
    dependencies: List[str]
    success_criteria: List[str]


@dataclass
class AgentAssignment:
    """Agent assignment data structure"""
    agent_id: str
    assigned_contracts: List[str]
    total_effort: float
    skills: List[str]
    availability: str  # "available", "busy", "unavailable"


class Phase3TaskAssigner:
    """
    Phase 3 Task Assigner - Single responsibility: Assign Phase 3 contracts to agents
    
    This class only handles:
    - Loading Phase 3 contracts
    - Assigning contracts to agents 1-4
    - Sending assignments via pyautogui messaging
    - Tracking assignment progress
    """
    
    def __init__(self, contracts_file: str = "contracts/phase3a_core_system_contracts.json"):
        """Initialize the Phase 3 task assigner"""
        self.contracts_file = Path(contracts_file)
        self.contracts: Dict[str, Phase3Contract] = {}
        self.agent_assignments: Dict[str, AgentAssignment] = {}
        self.messaging_system: Optional[PyAutoGUIMessaging] = None
        
        # Initialize agent assignments for agents 1-4
        self._initialize_agent_assignments()
        
        # Load contracts
        self._load_contracts()
        
        logger.info("Phase 3 Task Assigner initialized")
    
    def _initialize_agent_assignments(self):
        """Initialize agent assignments for agents 1-4"""
        self.agent_assignments = {
            "agent_001": AgentAssignment(
                agent_id="agent_001",
                assigned_contracts=[],
                total_effort=0.0,
                skills=["core_systems", "health_monitoring", "message_routing"],
                availability="available"
            ),
            "agent_002": AgentAssignment(
                agent_id="agent_002",
                assigned_contracts=[],
                total_effort=0.0,
                skills=["api_gateway", "agent_management", "performance_alerts"],
                availability="available"
            ),
            "agent_003": AgentAssignment(
                agent_id="agent_003",
                assigned_contracts=[],
                total_effort=0.0,
                skills=["financial_services", "portfolio_management", "risk_models"],
                availability="available"
            ),
            "agent_004": AgentAssignment(
                agent_id="agent_004",
                assigned_contracts=[],
                total_effort=0.0,
                skills=["testing_framework", "middleware", "integration_services"],
                availability="available"
            )
        }
    
    def _load_contracts(self):
        """Load Phase 3 contracts from JSON file"""
        try:
            if self.contracts_file.exists():
                with open(self.contracts_file, 'r') as f:
                    contracts_data = json.load(f)
                    
                # Handle the actual structure: contracts are in a "contracts" array
                if "contracts" in contracts_data:
                    contracts_array = contracts_data["contracts"]
                    for contract_data in contracts_array:
                        contract_id = contract_data.get("contract_id", "")
                        if contract_id:
                            # Extract refactoring plan steps
                            refactoring_plan = []
                            if "refactoring_plan" in contract_data:
                                plan_data = contract_data["refactoring_plan"]
                                if "extract_modules" in plan_data:
                                    refactoring_plan = plan_data["extract_modules"]
                            
                            contract = Phase3Contract(
                                contract_id=contract_id,
                                file_path=contract_data.get("file_path", ""),
                                current_lines=contract_data.get("current_lines", 0),
                                target_lines=contract_data.get("target_lines", 0),
                                priority=contract_data.get("priority", "MEDIUM"),
                                category=contract_data.get("category", ""),
                                estimated_effort=contract_data.get("estimated_hours", 0.0),
                                description=contract_data.get("category", ""),  # Use category as description
                                refactoring_plan=refactoring_plan,
                                dependencies=contract_data.get("dependencies", []),
                                success_criteria=contract_data.get("success_criteria", [])
                            )
                            self.contracts[contract_id] = contract
                else:
                    logger.error("No 'contracts' array found in file")
                
                logger.info(f"Loaded {len(self.contracts)} Phase 3 contracts")
            else:
                logger.error(f"Contracts file not found: {self.contracts_file}")
        except Exception as e:
            logger.error(f"Error loading contracts: {e}")
    
    def setup_messaging(self, coordinate_manager: CoordinateManager):
        """Setup the messaging system with coordinate manager"""
        try:
            self.messaging_system = PyAutoGUIMessaging(coordinate_manager)
            logger.info("Messaging system setup complete")
        except Exception as e:
            logger.error(f"Error setting up messaging system: {e}")
    
    def assign_contracts_to_agents(self) -> Dict[str, List[str]]:
        """Assign Phase 3 contracts to agents 1-4 based on skills and workload"""
        if not self.contracts:
            logger.warning("No contracts available for assignment")
            return {}
        
        # Sort contracts by priority and effort
        sorted_contracts = sorted(
            self.contracts.values(),
            key=lambda c: (self._priority_score(c.priority), c.estimated_effort),
            reverse=True
        )
        
        assignments = {}
        
        for contract in sorted_contracts:
            best_agent = self._find_best_agent_for_contract(contract)
            if best_agent:
                # Assign contract to agent
                self.agent_assignments[best_agent].assigned_contracts.append(contract.contract_id)
                self.agent_assignments[best_agent].total_effort += contract.estimated_effort
                
                if best_agent not in assignments:
                    assignments[best_agent] = []
                assignments[best_agent].append(contract.contract_id)
                
                logger.info(f"Assigned {contract.contract_id} to {best_agent}")
            else:
                logger.warning(f"No suitable agent found for {contract.contract_id}")
        
        return assignments
    
    def _find_best_agent_for_contract(self, contract: Phase3Contract) -> Optional[str]:
        """Find the best agent for a specific contract"""
        best_agent = None
        best_score = 0.0
        
        for agent_id, agent in self.agent_assignments.items():
            if agent.availability != "available":
                continue
            
            # Calculate compatibility score
            skill_score = self._calculate_skill_match(agent.skills, contract)
            workload_score = self._calculate_workload_score(agent.total_effort)
            total_score = skill_score * 0.7 + workload_score * 0.3
            
            if total_score > best_score:
                best_score = total_score
                best_agent = agent_id
        
        return best_agent
    
    def _calculate_skill_match(self, agent_skills: List[str], contract: Phase3Contract) -> float:
        """Calculate skill match between agent and contract"""
        # Simple skill matching based on category and description
        contract_text = f"{contract.category} {contract.description}".lower()
        
        skill_matches = 0
        for skill in agent_skills:
            if skill.lower() in contract_text:
                skill_matches += 1
        
        return min(skill_matches / len(agent_skills), 1.0) if agent_skills else 0.0
    
    def _calculate_workload_score(self, current_effort: float) -> float:
        """Calculate workload score (lower effort = higher score)"""
        # Prefer agents with lower current workload
        max_effort = 40.0  # Maximum expected effort per agent
        return max(0.0, 1.0 - (current_effort / max_effort))
    
    def _priority_score(self, priority: str) -> int:
        """Convert priority string to numeric score"""
        priority_map = {
            "CRITICAL": 4,
            "HIGH": 3,
            "MEDIUM": 2,
            "LOW": 1
        }
        return priority_map.get(priority, 2)
    
    def send_assignments_to_agents(self) -> bool:
        """Send contract assignments to agents via pyautogui messaging"""
        if not self.messaging_system:
            logger.error("Messaging system not setup")
            return False
        
        success_count = 0
        total_assignments = 0
        
        for agent_id, agent in self.agent_assignments.items():
            if not agent.assigned_contracts:
                continue
            
            total_assignments += 1
            message = self._format_assignment_message(agent)
            
            try:
                # Send assignment message to agent
                if self.messaging_system.send_message(
                    recipient=agent_id,
                    message_content=message,
                    message_type="task_assignment"
                ):
                    success_count += 1
                    logger.info(f"Assignment sent to {agent_id}")
                    
                    # Update agent availability
                    agent.availability = "busy"
                else:
                    logger.error(f"Failed to send assignment to {agent_id}")
                    
            except Exception as e:
                logger.error(f"Error sending assignment to {agent_id}: {e}")
        
        logger.info(f"Sent {success_count}/{total_assignments} assignments successfully")
        return success_count == total_assignments
    
    def _format_assignment_message(self, agent: AgentAssignment) -> str:
        """Format assignment message for an agent"""
        message_lines = [
            f"🎯 **PHASE 3 CONTRACT ASSIGNMENTS**",
            f"Agent: {agent.agent_id}",
            f"Total Contracts: {len(agent.assigned_contracts)}",
            f"Estimated Effort: {agent.total_effort:.1f} hours",
            "",
            "**ASSIGNED CONTRACTS:**"
        ]
        
        for contract_id in agent.assigned_contracts:
            contract = self.contracts.get(contract_id)
            if contract:
                message_lines.extend([
                    f"",
                    f"📋 **{contract_id}**",
                    f"File: {contract.file_path}",
                    f"Current: {contract.current_lines} lines → Target: {contract.target_lines} lines",
                    f"Priority: {contract.priority}",
                    f"Effort: {contract.estimated_effort:.1f} hours",
                    f"Description: {contract.description}",
                    "",
                    "**Refactoring Plan:**"
                ])
                
                for step in contract.refactoring_plan:
                    message_lines.append(f"• {step}")
                
                message_lines.extend([
                    "",
                    "**Success Criteria:**"
                ])
                
                for criterion in contract.success_criteria:
                    message_lines.append(f"✅ {criterion}")
        
        message_lines.extend([
            "",
            "🚀 **READY TO EXECUTE**",
            "Begin with the highest priority contract and work through systematically.",
            "Report progress and any issues encountered.",
            "",
            "Good luck with the modularization! 🎉"
        ])
        
        return "\n".join(message_lines)
    
    def get_assignment_summary(self) -> Dict[str, Any]:
        """Get summary of all assignments"""
        summary = {
            "total_contracts": len(self.contracts),
            "total_assigned": sum(len(agent.assigned_contracts) for agent in self.agent_assignments.values()),
            "total_effort": sum(agent.total_effort for agent in self.agent_assignments.values()),
            "agent_assignments": {}
        }
        
        for agent_id, agent in self.agent_assignments.items():
            summary["agent_assignments"][agent_id] = {
                "contracts": agent.assigned_contracts,
                "effort": agent.total_effort,
                "availability": agent.availability
            }
        
        return summary
    
    def print_assignment_summary(self):
        """Print a formatted summary of assignments"""
        summary = self.get_assignment_summary()
        
        print("\n" + "="*80)
        print("🎯 PHASE 3 CONTRACT ASSIGNMENT SUMMARY")
        print("="*80)
        print(f"Total Contracts: {summary['total_contracts']}")
        print(f"Total Assigned: {summary['total_assigned']}")
        print(f"Total Effort: {summary['total_effort']:.1f} hours")
        print()
        
        for agent_id, agent_data in summary["agent_assignments"].items():
            print(f"🤖 **{agent_id}**")
            print(f"   Contracts: {len(agent_data['contracts'])}")
            print(f"   Effort: {agent_data['effort']:.1f} hours")
            print(f"   Status: {agent_data['availability']}")
            
            if agent_data['contracts']:
                print("   Assigned Contracts:")
                for contract_id in agent_data['contracts']:
                    contract = self.contracts.get(contract_id)
                    if contract:
                        print(f"     • {contract_id}: {contract.file_path}")
            print()


def main():
    """Main function to demonstrate Phase 3 task assignment"""
    print("🚀 Phase 3 Task Assigner - Agent Cellphone V2")
    print("="*50)
    
    # Initialize task assigner
    task_assigner = Phase3TaskAssigner()
    
    # Print loaded contracts
    print(f"📋 Loaded {len(task_assigner.contracts)} Phase 3 contracts")
    
    # Assign contracts to agents
    print("\n🎯 Assigning contracts to agents...")
    assignments = task_assigner.assign_contracts_to_agents()
    
    # Print assignment summary
    task_assigner.print_assignment_summary()
    
    # Note: To actually send messages, you would need to:
    # 1. Setup coordinate manager
    # 2. Setup messaging system
    # 3. Call send_assignments_to_agents()
    
    print("\n✅ Phase 3 task assignment complete!")
    print("💡 To send assignments to agents, setup messaging system and call send_assignments_to_agents()")


if __name__ == "__main__":
    main()
