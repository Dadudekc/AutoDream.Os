#!/usr/bin/env python3
"""
Phase 3 Assignment Demo - Agent Cellphone V2
===========================================

Demonstrates Phase 3 contract assignment using the extended AgentCoordinator.
This script shows how to use the existing architecture for Phase 3 tasks.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import sys
import logging
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from autonomous_development.agents.agent_coordinator import AgentCoordinator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Main function to demonstrate Phase 3 contract assignment"""
    print("🚀 Phase 3 Contract Assignment Demo - Agent Cellphone V2")
    print("="*60)
    
    try:
        # Step 1: Initialize the existing AgentCoordinator
        print("📋 Step 1: Initializing AgentCoordinator...")
        coordinator = AgentCoordinator()
        
        # Show existing agents
        print(f"✅ Initialized with {len(coordinator.get_all_agents())} agents")
        print("\n🤖 Available Agents:")
        for agent in coordinator.get_all_agents():
            print(f"  • {agent.agent_id}: {agent.name} ({agent.role.value})")
            print(f"    Skills: {', '.join(agent.skills)}")
            print(f"    Max Tasks: {agent.max_concurrent_tasks}")
        
        # Step 2: Load Phase 3 contracts
        print("\n📋 Step 2: Loading Phase 3 contracts...")
        contracts_loaded = coordinator.load_phase3_contracts()
        
        if not contracts_loaded:
            print("❌ Failed to load Phase 3 contracts")
            return False
        
        print(f"✅ Loaded {len(coordinator.phase3_contracts)} Phase 3 contracts")
        
        # Step 3: Assign contracts to agents
        print("\n🎯 Step 3: Assigning Phase 3 contracts to agents...")
        assignments = coordinator.assign_phase3_contracts_to_agents()
        
        if not assignments:
            print("❌ No contracts were assigned to agents")
            return False
        
        print(f"✅ Assigned contracts to {len(assignments)} agents")
        
        # Step 4: Print assignment summary
        print("\n📊 Step 4: Assignment Summary")
        coordinator.print_phase3_assignment_summary()
        
        # Step 5: Show how to integrate with existing messaging
        print("\n💬 Step 5: Integration with Existing Systems")
        print("The AgentCoordinator is now ready to work with:")
        print("  • MessageCoordinator for task communication")
        print("  • WorkflowEngine for execution orchestration")
        print("  • Existing task management infrastructure")
        
        # Final summary
        print("\n" + "="*60)
        print("📋 FINAL SUMMARY")
        print("="*60)
        
        summary = coordinator.get_phase3_assignment_summary()
        print(f"Total Contracts: {summary['total_contracts']}")
        print(f"Total Assigned: {summary['total_assigned']}")
        
        print("\n🤖 Agent Workload Distribution:")
        for agent_id, agent_data in summary["agent_assignments"].items():
            print(f"  {agent_id}: {len(agent_data['contracts'])} contracts, {agent_data['effort']:.1f} hours")
        
        print("\n✅ Phase 3 contract assignment complete using existing architecture!")
        print("💡 The AgentCoordinator is now ready for Phase 3 execution!")
        
    except Exception as e:
        logger.error(f"Error during Phase 3 assignment: {e}")
        print(f"❌ Error: {e}")
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
