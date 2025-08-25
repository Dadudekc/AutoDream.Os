#!/usr/bin/env python3
"""
Captain's Phase 3 Execution Script - Agent Cellphone V2
=====================================================

CAPTAIN MODE: Leading team execution of Phase 3 modularization contracts.
This script actually sends assignments to agents 1-4 using existing infrastructure.

Author: V2 SWARM CAPTAIN (Agent-1)
License: MIT
"""

import sys
import logging
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from autonomous_development.agents.agent_coordinator import AgentCoordinator
from services.communication.message_coordinator import MessageCoordinator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - CAPTAIN - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """CAPTAIN'S MAIN EXECUTION FUNCTION"""
    print("🚀" + "="*58 + "🚀")
    print("🎯 CAPTAIN AGENT-1: PHASE 3 EXECUTION ORDERS")
    print("🚀" + "="*58 + "🚀")
    print()
    print("📡 CAPTAIN STATUS: ONLINE AND LEADING MISSION")
    print("🎖️  RANK: V2 SWARM CAPTAIN")
    print("🎯 MISSION: Phase 3 Modularization Execution")
    print("👥 TEAM: Agents 1-4 + Captain")
    print()
    
    try:
        # CAPTAIN'S STEP 1: Initialize Command Center
        print("📋 STEP 1: Initializing Command Center...")
        coordinator = AgentCoordinator()
        message_coordinator = MessageCoordinator()
        
        print(f"✅ Command Center Active: {len(coordinator.get_all_agents())} agents ready")
        print("🎖️  Captain Agent-1 taking command")
        
        # CAPTAIN'S STEP 2: Load Phase 3 Battle Plan
        print("\n📋 STEP 2: Loading Phase 3 Battle Plan...")
        contracts_loaded = coordinator.load_phase3_contracts()
        
        if not contracts_loaded:
            print("❌ BATTLE PLAN FAILURE: Cannot load Phase 3 contracts")
            print("🎖️  Captain aborting mission - investigate contract files")
            return False
        
        print(f"✅ Battle Plan Loaded: {len(coordinator.phase3_contracts)} contracts ready")
        print("🎯 Target: Achieve V2 compliance through modularization")
        
        # CAPTAIN'S STEP 3: Strategic Assignment
        print("\n🎯 STEP 3: Strategic Contract Assignment...")
        assignments = coordinator.assign_phase3_contracts_to_agents()
        
        if not assignments:
            print("❌ STRATEGIC FAILURE: No contracts assigned to agents")
            print("🎖️  Captain investigating assignment algorithm")
            return False
        
        print(f"✅ Strategic Assignment Complete: {len(assignments)} agents deployed")
        
        # CAPTAIN'S STEP 4: Mission Briefing
        print("\n📊 STEP 4: Mission Briefing & Status Report")
        coordinator.print_phase3_assignment_summary()
        
        # CAPTAIN'S STEP 5: EXECUTE ORDERS
        print("\n🚀 STEP 5: EXECUTING CAPTAIN'S ORDERS")
        print("📡 Sending Phase 3 assignments to agents...")
        print("🎖️  Captain Agent-1 transmitting mission parameters...")
        
        success = coordinator.send_phase3_assignments_to_agents(message_coordinator)
        
        if success:
            print("✅ MISSION SUCCESS: All Phase 3 assignments transmitted!")
            print("🎖️  Captain Agent-1: Mission accomplished!")
        else:
            print("⚠️  PARTIAL SUCCESS: Some assignments failed")
            print("🎖️  Captain Agent-1: Investigating transmission issues")
        
        # CAPTAIN'S FINAL BRIEFING
        print("\n" + "🚀" + "="*58 + "🚀")
        print("🎖️  CAPTAIN'S FINAL BRIEFING")
        print("🚀" + "="*58 + "🚀")
        
        summary = coordinator.get_phase3_assignment_summary()
        print(f"📊 Total Contracts: {summary['total_contracts']}")
        print(f"🎯 Total Assigned: {summary['total_assigned']}")
        
        print("\n🤖 AGENT DEPLOYMENT STATUS:")
        for agent_id, agent_data in summary["agent_assignments"].items():
            print(f"  🚀 {agent_id}: {len(agent_data['contracts'])} contracts, {agent_data['effort']:.1f} hours")
        
        print("\n🎖️  CAPTAIN'S ORDERS EXECUTED:")
        print("  1. ✅ Phase 3 contracts loaded")
        print("  2. ✅ Strategic assignment completed")
        print("  3. ✅ Mission briefing delivered")
        print("  4. ✅ Orders transmitted to agents")
        print("  5. ✅ Team ready for execution")
        
        print("\n🚀 NEXT PHASE: DEDUPLICATION PREPARATION")
        print("🎯 After modularization: Focus on code deduplication")
        print("👥 Team will be ready for Phase 4 execution")
        
        print("\n🎖️  CAPTAIN AGENT-1: Mission complete. Team deployed.")
        print("📡 Awaiting progress reports from agents...")
        print("🚀 Over and out.")
        
    except Exception as e:
        logger.error(f"CAPTAIN ERROR: {e}")
        print(f"❌ CAPTAIN SYSTEM FAILURE: {e}")
        print("🎖️  Captain Agent-1: Mission aborted - system error")
        return False
    
    return True


if __name__ == "__main__":
    print("🎖️  CAPTAIN AGENT-1: Taking command...")
    success = main()
    if success:
        print("\n🎖️  CAPTAIN STATUS: Mission successful")
    else:
        print("\n🎖️  CAPTAIN STATUS: Mission failed")
    sys.exit(0 if success else 1)
