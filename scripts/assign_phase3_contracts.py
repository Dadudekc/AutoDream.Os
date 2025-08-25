#!/usr/bin/env python3
"""
Phase 3 Contract Assignment Script - Agent Cellphone V2
=====================================================

Script to assign Phase 3 contracts to agents 1-4 and send assignments via pyautogui.
This script demonstrates the complete workflow from contract loading to agent messaging.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import sys
import logging
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from services.phase3_task_assigner import Phase3TaskAssigner
from services.messaging.coordinate_manager import CoordinateManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Main function to execute Phase 3 contract assignment"""
    print("🚀 Phase 3 Contract Assignment - Agent Cellphone V2")
    print("="*60)
    
    try:
        # Step 1: Initialize task assigner
        print("📋 Step 1: Initializing Phase 3 Task Assigner...")
        task_assigner = Phase3TaskAssigner()
        
        if not task_assigner.contracts:
            print("❌ No contracts loaded. Please check the contracts file.")
            return
        
        print(f"✅ Loaded {len(task_assigner.contracts)} Phase 3 contracts")
        
        # Step 2: Assign contracts to agents
        print("\n🎯 Step 2: Assigning contracts to agents 1-4...")
        assignments = task_assigner.assign_contracts_to_agents()
        
        if not assignments:
            print("❌ No contracts were assigned to agents.")
            return
        
        print(f"✅ Assigned contracts to {len(assignments)} agents")
        
        # Step 3: Print assignment summary
        print("\n📊 Step 3: Assignment Summary")
        task_assigner.print_assignment_summary()
        
        # Step 4: Setup messaging system (if coordinates available)
        print("\n💬 Step 4: Setting up messaging system...")
        try:
            coordinate_manager = CoordinateManager()
            task_assigner.setup_messaging(coordinate_manager)
            print("✅ Messaging system setup complete")
            
            # Step 5: Send assignments to agents
            print("\n📤 Step 5: Sending assignments to agents...")
            success = task_assigner.send_assignments_to_agents()
            
            if success:
                print("✅ All assignments sent successfully!")
                print("\n🎉 Phase 3 contracts have been assigned and sent to agents 1-4!")
                print("🤖 Agents should now receive their contract assignments via pyautogui messaging.")
            else:
                print("⚠️ Some assignments failed to send. Check logs for details.")
                
        except Exception as e:
            print(f"⚠️ Messaging system setup failed: {e}")
            print("💡 This is expected if coordinate files are not configured.")
            print("📋 Contract assignments are still available for manual distribution.")
        
        # Final summary
        print("\n" + "="*60)
        print("📋 FINAL SUMMARY")
        print("="*60)
        
        summary = task_assigner.get_assignment_summary()
        print(f"Total Contracts: {summary['total_contracts']}")
        print(f"Total Assigned: {summary['total_assigned']}")
        print(f"Total Effort: {summary['total_effort']:.1f} hours")
        
        print("\n🤖 Agent Workload Distribution:")
        for agent_id, agent_data in summary["agent_assignments"].items():
            if agent_data['contracts']:
                print(f"  {agent_id}: {len(agent_data['contracts'])} contracts, {agent_data['effort']:.1f} hours")
        
        print("\n✅ Phase 3 contract assignment complete!")
        
    except Exception as e:
        logger.error(f"Error during contract assignment: {e}")
        print(f"❌ Error: {e}")
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
