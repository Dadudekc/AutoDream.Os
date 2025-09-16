#!/usr/bin/env python3
"""
Coordination Factory Module
===========================

Factory for creating and orchestrating the integrated coordination system.
Handles main system orchestration and component creation.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import argparse
import logging
from pathlib import Path
from typing import Dict, List

from .coordination_service import CoordinationService
from .onboarding_coordinator import OnboardingCoordinator
from .agent_instructions import AgentInstructions

logger = logging.getLogger(__name__)

class CoordinationFactory:
    """Factory for creating coordination system components."""
    
    def __init__(self):
        self.coordination_service = None
        self.onboarding_coordinator = None
        self.agent_instructions = None
        self.swarm_agents = [
            "Agent-1", "Agent-2", "Agent-3", "Agent-4",
            "Agent-5", "Agent-6", "Agent-7", "Agent-8"
        ]
    
    def create_coordination_service(self) -> CoordinationService:
        """Create coordination service instance."""
        if not self.coordination_service:
            self.coordination_service = CoordinationService()
            logger.info("✅ CoordinationService created")
        return self.coordination_service
    
    def create_onboarding_coordinator(self) -> OnboardingCoordinator:
        """Create onboarding coordinator instance."""
        if not self.onboarding_coordinator:
            coordination_service = self.create_coordination_service()
            self.onboarding_coordinator = OnboardingCoordinator(coordination_service)
            logger.info("✅ OnboardingCoordinator created")
        return self.onboarding_coordinator
    
    def create_agent_instructions(self) -> AgentInstructions:
        """Create agent instructions instance."""
        if not self.agent_instructions:
            self.agent_instructions = AgentInstructions()
            logger.info("✅ AgentInstructions created")
        return self.agent_instructions
    
    def create_integrated_system(self):
        """Create the complete integrated system."""
        coordination_service = self.create_coordination_service()
        onboarding_coordinator = self.create_onboarding_coordinator()
        agent_instructions = self.create_agent_instructions()
        
        return IntegratedOnboardingCoordinationSystem(
            coordination_service,
            onboarding_coordinator,
            agent_instructions
        )

class IntegratedOnboardingCoordinationSystem:
    """Main integrated system orchestrator."""
    
    def __init__(self, coordination_service, onboarding_coordinator, agent_instructions):
        self.coordination_service = coordination_service
        self.onboarding_coordinator = onboarding_coordinator
        self.agent_instructions = agent_instructions
        self.swarm_agents = [
            "Agent-1", "Agent-2", "Agent-3", "Agent-4",
            "Agent-5", "Agent-6", "Agent-7", "Agent-8"
        ]
        
        logger.info("🚀 IntegratedOnboardingCoordinationSystem initialized")
    
    def onboard_all_agents(self) -> Dict[str, bool]:
        """Onboard all agents in the swarm."""
        logger.info("🚀 Starting onboarding for all agents...")
        results = self.onboarding_coordinator.onboard_all_agents()
        
        # Update FSM states for successfully onboarded agents
        for agent_id, success in results.items():
            if success:
                from .onboarding_coordinator import AgentState
                self.coordination_service.transition_agent_state(agent_id, AgentState.ONBOARDING)
        
        return results
    
    def start_enhanced_cycles(self):
        """Start enhanced coordination cycles."""
        logger.info("🚀 Starting enhanced coordination cycles...")
        
        # Get all onboarded agents
        onboarded_agents = self.coordination_service.get_onboarded_agents()
        logger.info(f"📋 Onboarded agents: {onboarded_agents}")
        
        # Start coordination cycles for each agent
        for agent_id in onboarded_agents:
            self._start_agent_cycle(agent_id)
        
        logger.info("✅ Enhanced coordination cycles started")
    
    def _start_agent_cycle(self, agent_id: str):
        """Start coordination cycle for a specific agent."""
        try:
            # Get agent state and contract
            state = self.coordination_service.get_agent_state(agent_id)
            contract = self.coordination_service.get_contract(agent_id)
            is_onboarded = self.coordination_service.is_agent_onboarded(agent_id)
            
            # Get agent-specific instructions
            instructions = self.agent_instructions.get_agent_instructions(
                agent_id, state, contract, is_onboarded
            )
            
            logger.info(f"🔄 Started coordination cycle for {agent_id}")
            logger.info(f"📋 Instructions: {instructions[:100]}...")
            
        except Exception as e:
            logger.error(f"❌ Failed to start cycle for {agent_id}: {e}")
    
    def get_contract_status(self):
        """Get current contract status."""
        return self.coordination_service.get_contract_status()
    
    def get_system_status(self):
        """Get comprehensive system status."""
        return self.coordination_service.get_system_status()
    
    def get_agent_statistics(self):
        """Get statistics about agent states and transitions."""
        return self.coordination_service.get_agent_statistics()
    
    def cleanup_expired_contracts(self):
        """Clean up expired or completed contracts."""
        self.coordination_service.cleanup_expired_contracts()
    
    def reset_agent_state(self, agent_id: str):
        """Reset agent state to uninitialized."""
        self.coordination_service.reset_agent_state(agent_id)
    
    def validate_system(self) -> Dict[str, bool]:
        """Validate system configuration and state."""
        validation_results = {
            "coordinates_valid": True,
            "fsm_initialized": True,
            "contracts_valid": True,
            "system_ready": True
        }
        
        try:
            # Validate coordinates
            coord_validation = self.coordination_service.validate_coordinates()
            validation_results["coordinates_valid"] = all(coord_validation.values())
            
            # Validate FSM initialization
            validation_results["fsm_initialized"] = len(self.coordination_service.agent_fsms) == len(self.swarm_agents)
            
            # Validate contracts
            validation_results["contracts_valid"] = len(self.coordination_service.contracts) >= 0
            
            # Overall system readiness
            validation_results["system_ready"] = all(validation_results.values())
            
        except Exception as e:
            logger.error(f"❌ System validation failed: {e}")
            validation_results["system_ready"] = False
        
        return validation_results
    
    def run(self, args):
        """Main execution method."""
        try:
            if args.onboard_all_agents:
                logger.info("🚀 Starting agent onboarding...")
                results = self.onboard_all_agents()
                successful = sum(1 for success in results.values() if success)
                logger.info(f"✅ Onboarding complete: {successful}/{len(results)} agents onboarded")
                
            elif args.start_enhanced_cycles:
                logger.info("🚀 Starting enhanced cycles...")
                self.start_enhanced_cycles()
                
            elif args.contract_status:
                logger.info("📋 Contract status:")
                status = self.get_contract_status()
                for agent_id, contract in status.items():
                    logger.info(f"  {agent_id}: {contract['status']} ({contract['progress_percentage']}%)")
                    
            elif args.system_status:
                logger.info("📊 System status:")
                status = self.get_system_status()
                logger.info(f"  Total agents: {status['total_agents']}")
                logger.info(f"  Onboarded agents: {status['onboarded_agents']}")
                logger.info(f"  Active contracts: {status['active_contracts']}")
                
            elif args.validate_system:
                logger.info("🔍 Validating system...")
                validation = self.validate_system()
                for check, result in validation.items():
                    status = "✅" if result else "❌"
                    logger.info(f"  {check}: {status}")
                    
            else:
                logger.info("❓ No action specified. Use --help for available options.")
                
        except Exception as e:
            logger.error(f"❌ Execution failed: {e}")
            raise

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Integrated Onboarding & Cycle Coordination System")
    parser.add_argument("--onboard-all-agents", action="store_true", help="Onboard all agents")
    parser.add_argument("--start-enhanced-cycles", action="store_true", help="Start enhanced cycles")
    parser.add_argument("--contract-status", action="store_true", help="Show contract status")
    parser.add_argument("--system-status", action="store_true", help="Show system status")
    parser.add_argument("--validate-system", action="store_true", help="Validate system configuration")
    
    args = parser.parse_args()
    
    try:
        factory = CoordinationFactory()
        system = factory.create_integrated_system()
        system.run(args)
    except Exception as e:
        logger.error(f"❌ System execution failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
