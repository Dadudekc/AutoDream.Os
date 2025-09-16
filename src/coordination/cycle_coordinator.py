"""
Cycle Coordinator - Main Coordination System
===========================================

Main coordination system integrating contracts and FSM.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""
import argparse
import logging
import time
from typing import Dict, List, Optional
from .contract_system import ContractManager, ContractStatus
from .fsm_system import FSMManager, AgentState
logger = logging.getLogger(__name__)


class CycleCoordinator:
    """Main cycle coordination system."""

    def __init__(self):
        self.contract_manager = ContractManager()
        self.fsm_manager = FSMManager()
        self.agent_roles = {'Agent-1':
            'Integration & System Architecture Specialist', 'Agent-2':
            'Architecture & Design Specialist', 'Agent-3':
            'Code Quality & Optimization Specialist', 'Agent-4':
            'Strategic Oversight & Emergency Intervention Manager',
            'Agent-5': 'Business Intelligence & Analytics Specialist',
            'Agent-6': 'Documentation & Knowledge Management Specialist',
            'Agent-7': 'Testing & Quality Assurance Specialist', 'Agent-8':
            'Operations & Swarm Coordinator'}

    def get_agent_specific_prompt(self, agent_id: str, cycle_number: int=1
        ) ->str:
        """Generate agent-specific cycle prompt."""
        role = self.agent_roles.get(agent_id, 'Specialist')
        fsm = self.fsm_manager.get_or_create_fsm(agent_id)
        contracts = self.contract_manager.get_agent_contracts(agent_id)
        active_contracts = [c for c in contracts if c.status ==
            ContractStatus.ACTIVE]
        prompt = f"""🚀 ENHANCED CYCLE COORDINATION - {agent_id}
Role: {role}
FSM State: {fsm.current_state.value.upper()}
Cycle: #{cycle_number}

📋 CURRENT STATUS:
• State: {fsm.current_state.value}
• Transitions: {len(fsm.transitions)}
• Previous State: {fsm.previous_state.value if fsm.previous_state else 'None'}

🎯 {role.upper()} - GENERAL:
• Focus on {self._get_role_focus(agent_id)}
• Coordinate with other agents as needed
• Maintain high code quality and V2 compliance
• Report progress regularly

🛠️ CONTRACT & FSM TOOLS:
• Contract Status: Check current contract commitments
• FSM Transitions: Manage state transitions
• Collaboration: Coordinate with dependent agents
• Progress Reporting: Update contract progress"""
        if active_contracts:
            prompt += f'\n\n📋 ACTIVE CONTRACTS ({len(active_contracts)}):'
            for contract in active_contracts:
                prompt += (
                    f'\n• {contract.task} (Progress: {contract.progress}%)')
        prompt += f"""

🔧 COORDINATION COMMANDS:
• Message Captain: python unified_resume_coordination_tool.py --agent Agent-4 --message "Contract: [status]"
• Update FSM: Report state transitions to coordination system
• Broadcast Progress: python unified_resume_coordination_tool.py --broadcast --message "Contract: [progress]"

🐝 WE ARE SWARM - Enhanced cycle coordination with contracts and FSM active!

📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory

You are {agent_id}
Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}"""
        return prompt

    def _get_role_focus(self, agent_id: str) ->str:
        """Get role-specific focus areas."""
        focus_map = {'Agent-1':
            'system integration and architectural design', 'Agent-2':
            'architectural design and system consolidation', 'Agent-3':
            'code quality improvements and optimization', 'Agent-4':
            'strategic oversight and emergency intervention', 'Agent-5':
            'business intelligence and analytics initiatives', 'Agent-6':
            'documentation and knowledge management', 'Agent-7':
            'testing and quality assurance initiatives', 'Agent-8':
            'operations and swarm coordination'}
        return focus_map.get(agent_id, 'general project tasks')

    def start_cycles(self, duration_minutes: int=60) ->None:
        """Start cycle coordination for specified duration."""
        logger.info(
            f'Starting cycle coordination for {duration_minutes} minutes')
        pass

    def resume_agent_cycle(self, agent_id: str) ->bool:
        """Resume cycle for specific agent."""
        try:
            fsm = self.fsm_manager.get_or_create_fsm(agent_id)
            fsm.transition_to(AgentState.WORKING, 'Cycle resumed')
            prompt = self.get_agent_specific_prompt(agent_id)
            logger.info(f'Resumed cycle for {agent_id}')
            return True
        except Exception as e:
            logger.error(f'Error resuming cycle for {agent_id}: {e}')
            return False

    def get_contract_status(self) ->Dict:
        """Get overall contract status."""
        all_contracts = list(self.contract_manager.contracts.values())
        status_counts = {}
        for status in ContractStatus:
            status_counts[status.value] = sum(1 for c in all_contracts if c
                .status == status)
        return {'total_contracts': len(all_contracts), 'status_breakdown':
            status_counts, 'active_contracts': [c.to_dict() for c in
            all_contracts if c.status == ContractStatus.ACTIVE]}

    def run_cli(self) ->None:
        """Run command line interface."""
        parser = argparse.ArgumentParser(description=
            'Cycle Coordination System')
        parser.add_argument('--start-cycles', action='store_true', help=
            'Start cycle coordination')
        parser.add_argument('--agent', help='Target agent ID')
        parser.add_argument('--resume-cycle', action='store_true', help=
            'Resume agent cycle')
        parser.add_argument('--contract-status', action='store_true', help=
            'Show contract status')
        parser.add_argument('--duration', type=int, default=60, help=
            'Cycle duration in minutes')
        args = parser.parse_args()
        if args.start_cycles:
            self.start_cycles(args.duration)
        elif args.agent and args.resume_cycle:
            self.resume_agent_cycle(args.agent)
        elif args.contract_status:
            status = self.get_contract_status()
            logger.info(f'Contract Status: {status}')
        else:
            parser.print_help()


def main():
    """Main entry point."""
    coordinator = CycleCoordinator()
    coordinator.run_cli()


if __name__ == '__main__':
    main()
