#!/usr/bin/env python3
"""
Agent Status Tracker - Agent Cellphone V2
=========================================

Simple status tracking using existing architecture.
Agents can report completion and status is tracked.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    print("📊 AGENT STATUS TRACKER - USING EXISTING ARCHITECTURE")
    print("="*60)
    
    # Import existing systems
    from src.autonomous_development.agents.agent_coordinator import AgentCoordinator
    
    print("✅ Successfully imported existing architecture")
    
    # Initialize existing system
    coordinator = AgentCoordinator()
    
    # Load contracts
    if coordinator.load_phase3_contracts():
        print(f"✅ Loaded {len(coordinator.phase3_contracts)} Phase 3 contracts")
        
        # Show current status
        print("\n📊 CURRENT PHASE 3 STATUS:")
        coordinator.print_phase3_assignment_summary()
        
        # Show agent workload
        print("\n🤖 AGENT WORKLOAD STATUS:")
        workload = coordinator.get_agent_workload_summary()
        for agent_id, data in workload.items():
            print(f"  {agent_id}: {data['current_tasks']}/{data['max_tasks']} tasks ({data['workload_percentage']:.1f}%)")
        
        # Show swarm status
        print("\n📊 SWARM STATUS:")
        print(coordinator.show_swarm_status())
        
    else:
        print("❌ Failed to load Phase 3 contracts")
    
    print("\n💡 STATUS TRACKING READY!")
    print("📱 Agents can report completion via messaging")
    print("🎯 Use existing coordinate system and messaging")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
