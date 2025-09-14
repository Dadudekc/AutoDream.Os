"""
Coordination CLI
================

Command-line interface for the coordination system.

Author: Agent-2 (Architecture & Design Specialist)
Mission: Large File Modularization and V2 Compliance
Contract: CONTRACT_Agent-2_1757826687
License: MIT
"""

import argparse
import logging
import sys
from typing import List, Optional

from .services.coordination_service import CoordinationService
from .models.agent_state import ContractType
from .factories.agent_factory import AgentFactory

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CoordinationCLI:
    """Command-line interface for coordination system."""
    
    def __init__(self):
        """Initialize CLI."""
        self.coordination_service = CoordinationService()
        
    def run_cli(self, args: Optional[List[str]] = None) -> None:
        """Run CLI with arguments."""
        parser = self._create_parser()
        
        if args is None:
            args = sys.argv[1:]
            
        parsed_args = parser.parse_args(args)
        
        try:
            if parsed_args.onboarding_status:
                self._show_onboarding_status()
            elif parsed_args.fsm_status:
                self._show_fsm_status()
            elif parsed_args.contract_status:
                self._show_contract_status()
            elif parsed_args.onboard_agent:
                self._onboard_agent(parsed_args.onboard_agent)
            elif parsed_args.onboard_all_agents:
                self._onboard_all_agents()
            elif parsed_args.start_enhanced_cycles:
                self._start_enhanced_cycles()
            elif parsed_args.stop_enhanced_cycles:
                self._stop_enhanced_cycles()
            elif parsed_args.create_contract:
                self._create_contract(parsed_args.create_contract)
            else:
                parser.print_help()
                
        except KeyboardInterrupt:
            logger.info("👋 CLI interrupted by user")
            self.coordination_service.stop_enhanced_cycles()
        except Exception as e:
            logger.error(f"❌ CLI error: {e}")
            sys.exit(1)
            
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser."""
        parser = argparse.ArgumentParser(
            description="Integrated Onboarding & Cycle Coordination System",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  python coordination_cli.py --onboarding-status
  python coordination_cli.py --fsm-status
  python coordination_cli.py --contract-status
  python coordination_cli.py --onboard-agent Agent-1
  python coordination_cli.py --onboard-all-agents
  python coordination_cli.py --start-enhanced-cycles
  python coordination_cli.py --create-contract Agent-2
            """
        )
        
        parser.add_argument(
            '--onboarding-status',
            action='store_true',
            help='Show onboarding status for all agents'
        )
        
        parser.add_argument(
            '--fsm-status',
            action='store_true',
            help='Show FSM status for all agents'
        )
        
        parser.add_argument(
            '--contract-status',
            action='store_true',
            help='Show contract status summary'
        )
        
        parser.add_argument(
            '--onboard-agent',
            type=str,
            metavar='AGENT_ID',
            help='Onboard specific agent'
        )
        
        parser.add_argument(
            '--onboard-all-agents',
            action='store_true',
            help='Onboard all agents'
        )
        
        parser.add_argument(
            '--start-enhanced-cycles',
            action='store_true',
            help='Start enhanced cycle coordination'
        )
        
        parser.add_argument(
            '--stop-enhanced-cycles',
            action='store_true',
            help='Stop enhanced cycle coordination'
        )
        
        parser.add_argument(
            '--create-contract',
            type=str,
            metavar='AGENT_ID',
            help='Create contract for specific agent'
        )
        
        return parser
        
    def _show_onboarding_status(self):
        """Show onboarding status."""
        print("🎯 ONBOARDING STATUS FOR ALL AGENTS:")
        print("=" * 60)
        
        onboarding_status = self.coordination_service.get_onboarding_status()
        agent_roles = AgentFactory.get_all_agent_roles()
        
        for agent_id in AgentFactory.get_swarm_agents():
            role = agent_roles.get(agent_id, "Unknown Specialist")
            status = "✅ ONBOARDED" if onboarding_status.get(agent_id, False) else "❌ PENDING"
            print(f"{agent_id}: {status} - {role}")
            
    def _show_fsm_status(self):
        """Show FSM status."""
        print("🔄 FSM STATUS FOR ALL AGENTS:")
        print("=" * 60)
        
        fsm_status = self.coordination_service.get_fsm_status()
        
        for agent_id, status_info in fsm_status.items():
            current_state = status_info.get('current_state', 'unknown')
            transition_count = status_info.get('transition_count', 0)
            print(f"{agent_id}: {current_state} (transitions: {transition_count})")
            
    def _show_contract_status(self):
        """Show contract status."""
        print("📋 CONTRACT STATUS SUMMARY:")
        print("=" * 60)
        
        summary = self.coordination_service.contract_service.get_contract_status_summary()
        print(f"Total Contracts: {summary['total_contracts']}")
        print(f"Pending: {summary['pending']}")
        print(f"Accepted: {summary['accepted']}")
        print(f"Completed: {summary['completed']}")
        
    def _onboard_agent(self, agent_id: str):
        """Onboard specific agent."""
        if agent_id not in AgentFactory.get_swarm_agents():
            logger.error(f"❌ Invalid agent ID: {agent_id}")
            return
            
        logger.info(f"🚀 Onboarding agent: {agent_id}")
        success = self.coordination_service.onboard_agent(agent_id)
        
        if success:
            logger.info(f"✅ Agent {agent_id} onboarded successfully")
        else:
            logger.error(f"❌ Failed to onboard agent {agent_id}")
            
    def _onboard_all_agents(self):
        """Onboard all agents."""
        logger.info("🚀 Onboarding all agents...")
        results = self.coordination_service.onboard_all_agents()
        
        successful = sum(1 for success in results.values() if success)
        total = len(results)
        
        logger.info(f"📊 Onboarding completed: {successful}/{total} agents successful")
        
        for agent_id, success in results.items():
            status = "✅ SUCCESS" if success else "❌ FAILED"
            logger.info(f"{agent_id}: {status}")
            
    def _start_enhanced_cycles(self):
        """Start enhanced cycles."""
        logger.info("🔄 Starting enhanced cycles...")
        success = self.coordination_service.start_enhanced_cycles()
        
        if success:
            logger.info("✅ Enhanced cycles started successfully")
            logger.info("Press Ctrl+C to stop")
            
            # Keep running until interrupted
            try:
                while True:
                    import time
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("👋 Stopping enhanced cycles...")
                self.coordination_service.stop_enhanced_cycles()
        else:
            logger.error("❌ Failed to start enhanced cycles")
            
    def _stop_enhanced_cycles(self):
        """Stop enhanced cycles."""
        logger.info("🛑 Stopping enhanced cycles...")
        self.coordination_service.stop_enhanced_cycles()
        logger.info("✅ Enhanced cycles stopped")
        
    def _create_contract(self, agent_id: str):
        """Create contract for agent."""
        if agent_id not in AgentFactory.get_swarm_agents():
            logger.error(f"❌ Invalid agent ID: {agent_id}")
            return
            
        logger.info(f"📋 Creating contract for agent: {agent_id}")
        
        # For Agent-2, create a modularization contract
        if agent_id == "Agent-2":
            contract_id = self.coordination_service.create_contract(
                agent_id=agent_id,
                contract_type=ContractType.V2_COMPLIANCE,
                task_description="Large File Modularization and V2 Compliance",
                priority="HIGH",
                deadline="2025-09-15 00:11:27"
            )
            
            if contract_id:
                logger.info(f"✅ Contract created: {contract_id}")
            else:
                logger.error(f"❌ Failed to create contract for {agent_id}")
        else:
            logger.info(f"ℹ️ Contract creation not implemented for {agent_id}")


def main():
    """Main entry point."""
    cli = CoordinationCLI()
    cli.run_cli()


if __name__ == "__main__":
    main()