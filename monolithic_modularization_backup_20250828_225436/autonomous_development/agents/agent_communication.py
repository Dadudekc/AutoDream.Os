#!/usr/bin/env python3
"""
Agent Communication - Agent Cellphone V2
=======================================

Handles messaging, swarm commands, and communication between agents.
Follows V2 standards: SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
from typing import Dict, List, Optional, Any

from .agent_management import AgentManager, AgentInfo


class AgentCommunication:
    """Handles messaging, swarm commands, and communication between agents"""
    
    def __init__(self, agent_manager: AgentManager):
        self.agent_manager = agent_manager
        self.logger = logging.getLogger(__name__)
    
    def send_phase3_assignments_to_agents(self, phase3_assignments: Dict[str, List[str]], 
                                        phase3_contracts: Dict[str, Dict[str, Any]], 
                                        message_coordinator=None) -> bool:
        """Send Phase 3 contract assignments to agents using existing messaging system"""
        if not phase3_assignments:
            self.logger.warning("No Phase 3 assignments to send")
            return False
        
        success_count = 0
        total_assignments = 0
        
        for agent_id, contracts in phase3_assignments.items():
            if not contracts:
                continue
            
            total_assignments += 1
            message = self._format_phase3_assignment_message(agent_id, contracts, phase3_contracts)
            
            try:
                if message_coordinator:
                    # Use existing MessageCoordinator if available
                    task_id = message_coordinator.create_task(
                        title=f"Phase 3 Contract Assignment - {agent_id}",
                        description=message,
                        priority="HIGH",
                        assigned_agents=[agent_id],
                        estimated_hours=sum(
                            phase3_contracts.get(c, {}).get("estimated_hours", 0.0) 
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
    
    def _format_phase3_assignment_message(self, agent_id: str, contracts: List[str], 
                                        phase3_contracts: Dict[str, Dict[str, Any]]) -> str:
        """Format Phase 3 assignment message for an agent"""
        agent = self.agent_manager.agents.get(agent_id)
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
            contract = phase3_contracts.get(contract_id, {})
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
    
    # Swarm Command Methods - Any Agent Can Take Command
    
    def take_command(self, agent_id: str) -> bool:
        """Allow any agent to take command of the swarm"""
        if agent_id not in self.agent_manager.agents:
            self.logger.error(f"Agent {agent_id} not found - cannot take command")
            return False
        
        agent = self.agent_manager.agents[agent_id]
        if "swarm_command" not in agent.skills:
            self.logger.warning(f"Agent {agent_id} lacks swarm_command skill")
            return False
        
        # Update agent role to COORDINATOR if not already
        if agent.role.value != "COORDINATOR":
            old_role = agent.role.value
            agent.role.value = "COORDINATOR"
            self.logger.info(f"Agent {agent_id} promoted from {old_role} to COORDINATOR")
        
        self.logger.info(f"🎖️  Agent {agent_id} ({agent.name}) has taken command of the swarm!")
        return True
    
    def get_command_capable_agents(self) -> List[AgentInfo]:
        """Get all agents capable of taking command"""
        return [agent for agent in self.agent_manager.agents.values() if "swarm_command" in agent.skills]
    
    def execute_swarm_command(self, commander_id: str, command: str, target_agents: List[str] = None) -> bool:
        """Execute a swarm command from any capable agent"""
        if not self.take_command(commander_id):
            return False
        
        commander = self.agent_manager.agents[commander_id]
        self.logger.info(f"🎖️  Commander {commander_id} executing: {command}")
        
        if target_agents:
            for target_id in target_agents:
                if target_id in self.agent_manager.agents:
                    target = self.agent_manager.agents[target_id]
                    self.logger.info(f"📡 Command transmitted to {target_id}: {command}")
                else:
                    self.logger.warning(f"Target agent {target_id} not found")
        else:
            # Broadcast to all agents
            for agent_id in self.agent_manager.agents:
                if agent_id != commander_id:
                    self.logger.info(f"📡 Command broadcast to {agent_id}: {command}")
        
        return True
    
    def show_swarm_status(self, viewer_id: str = None) -> str:
        """Show current swarm status - any agent can view"""
        status_lines = [
            "🤖 **SWARM STATUS REPORT**",
            f"Total Agents: {len(self.agent_manager.agents)}",
            f"Active Agents: {len([a for a in self.agent_manager.agents.values() if a.is_active])}",
            f"Command Capable: {len(self.get_command_capable_agents())}",
            "",
            "**AGENT STATUS:**"
        ]
        
        for agent_id, agent in self.agent_manager.agents.items():
            role_icon = "🎖️" if agent.role.value == "COORDINATOR" else "🤖"
            status_icon = "🟢" if agent.is_active else "🔴"
            command_icon = "⚡" if "swarm_command" in agent.skills else "  "
            
            status_lines.append(
                f"{role_icon} {command_icon} **{agent_id}** ({agent.name})"
            )
            status_lines.append(
                f"   Role: {agent.role.value} | Status: {status_icon} {'Active' if agent.is_active else 'Inactive'}"
            )
            status_lines.append(
                f"   Skills: {', '.join(agent.skills)}"
            )
            status_lines.append(
                f"   Tasks: {len(agent.current_tasks)}/{agent.max_concurrent_tasks}"
            )
            status_lines.append("")
        
        if viewer_id:
            viewer = self.agent_manager.agents.get(viewer_id)
            if viewer:
                status_lines.append(f"👁️  Report generated by: {viewer_id} ({viewer.name})")
        
        return "\n".join(status_lines)
