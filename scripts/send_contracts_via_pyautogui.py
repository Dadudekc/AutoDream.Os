#!/usr/bin/env python3
"""
PyAutoGUI Contract Sender - Agent Cellphone V2
==============================================

ACTUALLY SENDS contracts to agents via PyAutoGUI using existing architecture.
This is the real implementation that will send messages to agents.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import sys
import json
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    print("🚀 PYAUTOGUI CONTRACT SENDER - ACTUALLY SENDING CONTRACTS!")
    print("="*70)
    
    # Import existing systems
    from services.messaging.coordinate_manager import CoordinateManager
    from services.messaging import UnifiedPyAutoGUIMessaging
    from autonomous_development.agents.agent_coordinator import AgentCoordinator
    
    print("✅ Successfully imported existing architecture")
    
    # Initialize existing systems
    print("\n📋 Initializing existing systems...")
    coordinate_manager = CoordinateManager()
    messaging = PyAutoGUIMessaging(coordinate_manager)
    coordinator = AgentCoordinator()
    
    print(f"✅ Coordinate Manager: {len(coordinate_manager.coordinates)} modes loaded")
    print(f"✅ PyAutoGUI Messaging: Ready")
    print(f"✅ Agent Coordinator: {len(coordinator.get_all_agents())} agents ready")
    
    # Load Phase 3 contracts using existing system
    print("\n📋 Loading Phase 3 contracts...")
    if coordinator.load_phase3_contracts():
        print(f"✅ Loaded {len(coordinator.phase3_contracts)} Phase 3 contracts")
        
        # Get available agent modes from coordinates
        available_modes = list(coordinate_manager.coordinates.keys())
        print(f"📱 Available agent modes: {available_modes}")
        
        # Use 4-agent mode (most common)
        target_mode = "4-agent" if "4-agent" in available_modes else available_modes[0]
        print(f"🎯 Using mode: {target_mode}")
        
        # Get agents in this mode
        mode_agents = list(coordinate_manager.coordinates[target_mode].keys())
        print(f"🤖 Agents in {target_mode}: {mode_agents}")
        
        # Confirm before sending
        print(f"\n⚠️  READY TO SEND {len(coordinator.phase3_contracts)} CONTRACTS VIA PYAUTOGUI!")
        print(f"📱 Target agents: {mode_agents}")
        print(f"🎯 Mode: {target_mode}")
        
        confirm = input("\n🚨 Type 'SEND' to proceed with PyAutoGUI messaging: ")
        if confirm != "SEND":
            print("❌ Contract sending cancelled")
            sys.exit(0)
        
        # Distribute contracts in round-robin
        print("\n📡 DISTRIBUTING CONTRACTS VIA PYAUTOGUI...")
        
        contract_list = list(coordinator.phase3_contracts.values())
        agent_index = 0
        success_count = 0
        
        for i, contract in enumerate(contract_list):
            # Get next agent in round-robin
            target_agent = mode_agents[agent_index % len(mode_agents)]
            agent_index += 1
            
            # Format contract message
            contract_message = f"""🎯 PHASE 3 CONTRACT ASSIGNMENT

Contract ID: {contract.get('contract_id', 'Unknown')}
File: {contract.get('file_path', 'Unknown')}
Priority: {contract.get('priority', 'MEDIUM')}
Effort: {contract.get('estimated_hours', 0.0)} hours

DESCRIPTION:
{contract.get('description', 'Modularize according to V2 standards')}

REFACTORING PLAN:
{contract.get('refactoring_plan', {}).get('extract_modules', ['Modularize according to V2 standards'])}

SUCCESS CRITERIA:
{chr(10).join([f"✅ {criterion}" for criterion in contract.get('success_criteria', ['File under 200 lines', 'Single responsibility principle', 'Clean imports'])])}

INSTRUCTIONS:
1. Review the file and understand current structure
2. Extract modules following V2 standards
3. Maintain functionality while reducing line count
4. Test your changes
5. Commit and push your work
6. Reply with "CONTRACT COMPLETE: [filename]"

🎖️  Captain Agent-1 out. Over and out."""
            
            print(f"\n📤 Sending contract {contract.get('contract_id', 'Unknown')} to {target_agent}...")
            
            # Send via existing PyAutoGUI system
            success = messaging.send_message(
                recipient=target_agent,
                message_content=contract_message,
                message_type="high_priority"
            )
            
            if success:
                print(f"✅ Contract sent to {target_agent}")
                success_count += 1
            else:
                print(f"❌ Failed to send contract to {target_agent}")
            
            # Small delay between messages to avoid overwhelming
            time.sleep(3)
        
        print(f"\n🎯 CONTRACT DISTRIBUTION COMPLETE!")
        print(f"📊 Total contracts: {len(contract_list)}")
        print(f"✅ Successfully sent: {success_count}")
        print(f"❌ Failed: {len(contract_list) - success_count}")
        print(f"🤖 Agents involved: {mode_agents}")
        print(f"📱 Mode used: {target_mode}")
        
        # Show final status
        print("\n📊 FINAL ASSIGNMENT STATUS:")
        coordinator.print_phase3_assignment_summary()
        
    else:
        print("❌ Failed to load Phase 3 contracts")
    
    print("\n🚀 PyAutoGUI contract distribution complete!")
    print("💡 Agents should now receive contracts via messaging")
    print("📱 Use existing coordinate system and messaging infrastructure")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
