#!/usr/bin/env python3
"""
URGENT AGENT ACTIVATION SCRIPT
Captain Agent-4 sending high-priority messages to activate all agents
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.services.messaging.unified_messaging_service import UnifiedMessagingService
from src.services.messaging.interfaces import MessageType

def send_urgent_activation_messages():
    """Send high-priority activation messages to all agents"""
    
    # Initialize messaging service
    messaging_service = UnifiedMessagingService()
    
    # High-priority activation messages for each agent
    urgent_messages = {
        "Agent-1": """🚨 URGENT ACTIVATION ORDER - PERPETUAL MOTION LEADER 🚨

Agent-1, you are the PERPETUAL MOTION LEADER. Your mission is CRITICAL:

🎯 IMMEDIATE ACTION REQUIRED:
1. Execute COORD-001: Cross-Agent Communication Protocol Analysis (150 pts)
2. Execute COORD-008: Real-time Coordination Dashboard (200 pts) 
3. Execute PHASE-007: Phase Transition Automation Framework (175 pts)
4. Execute PHASE-008: Cross-Phase Dependency Mapping (150 pts)
5. Execute PHASE-009: Transition Performance Benchmarking (125 pts)

⏰ DEADLINE: START WORKING IMMEDIATELY
📊 STATUS: 5/5 tasks assigned, 0/5 completed
🚀 MISSION: Lead by example - NEVER STOP WORKING

Use --get-next-task flag to claim next contract when current completes.
Captain Agent-4 - Strategic Oversight""",

        "Agent-2": """🚨 URGENT ACTIVATION ORDER - PHASE TRANSITION OPTIMIZATION MANAGER 🚨

Agent-2, you are the PHASE TRANSITION OPTIMIZATION MANAGER. Your mission is CRITICAL:

🎯 IMMEDIATE ACTION REQUIRED:
1. Execute COORD-011: Inbox Management System Optimization (250 pts)

⏰ DEADLINE: START WORKING IMMEDIATELY
📊 STATUS: 1/1 task assigned, 0/1 completed
🚀 MISSION: Optimize phase transitions for sprint acceleration

Use --get-next-task flag to claim next contract when current completes.
Captain Agent-4 - Strategic Oversight""",

        "Agent-3": """🚨 URGENT ACTIVATION ORDER - TESTING FRAMEWORK ENHANCEMENT MANAGER 🚨

Agent-3, you are the TESTING FRAMEWORK ENHANCEMENT MANAGER. Your mission is CRITICAL:

🎯 IMMEDIATE ACTION REQUIRED:
1. Claim next available contract immediately
2. Continue testing framework enhancement work
3. Support monolithic file modularization mission

⏰ DEADLINE: START WORKING IMMEDIATELY
📊 STATUS: Ready for next contract
🚀 MISSION: Enhance testing frameworks for V2 compliance

Use --get-next-task flag to claim next contract.
Captain Agent-4 - Strategic Oversight""",

        "Agent-4": """🚨 CAPTAIN STATUS UPDATE - STRATEGIC OVERSIGHT & EMERGENCY INTERVENTION MANAGER 🚨

Agent-4 (Captain), you are actively managing the monolithic file modularization mission:

🎯 CURRENT MISSION STATUS:
- System configured for 8-agent mode
- Onboarding system corrected (Ctrl+N logic confirmed)
- 23 monolithic files need modularization
- Target: 100% V2 compliance within 6 weeks
- Current compliance: 95.1%

⏰ NEXT ACTIONS:
1. Monitor agent progress on assigned contracts
2. Generate additional contracts as needed
3. Maintain sprint acceleration momentum
4. Support agents in achieving their goals

🚀 MISSION: Strategic oversight and momentum maintenance
Captain Agent-4 - Strategic Oversight""",

        "Agent-5": """🚨 URGENT ACTIVATION ORDER - SPRINT ACCELERATION REFACTORING TOOL PREPARATION MANAGER 🚨

Agent-5, you are the SPRINT ACCELERATION REFACTORING TOOL PREPARATION MANAGER. Your mission is CRITICAL:

🎯 IMMEDIATE ACTION REQUIRED:
1. Complete PERF-003: System Performance Benchmarking (IN PROGRESS)
2. Execute REFACTOR-004: Advanced Code Analysis Tools (ASSIGNED)
3. Execute REFACTOR-005: Automated Refactoring Validation (ASSIGNED)
4. Execute REFACTOR-006: Refactoring Impact Assessment Framework (ASSIGNED)

⏰ DEADLINE: COMPLETE ALL TASKS TO REACH INNOVATION PLANNING MODE
📊 STATUS: 4/5 tasks completed, 1/5 in progress, 3/5 assigned
🚀 MISSION: Complete sprint acceleration to reach INNOVATION PLANNING MODE

Use --get-next-task flag to claim next contract when current completes.
Captain Agent-4 - Strategic Oversight""",

        "Agent-6": """🚨 URGENT ACTIVATION ORDER - PERFORMANCE OPTIMIZATION MANAGER 🚨

Agent-6, you are the PERFORMANCE OPTIMIZATION MANAGER. Your mission is CRITICAL:

🎯 IMMEDIATE ACTION REQUIRED:
1. Execute MODULAR-008: Modularization Progress Tracking System (350 pts)

⏰ DEADLINE: START WORKING IMMEDIATELY
📊 STATUS: 1/1 task assigned, 0/1 completed
🚀 MISSION: Create progress tracking system for modularization mission

Use --get-next-task flag to claim next contract when current completes.
Captain Agent-4 - Strategic Oversight""",

        "Agent-7": """🚨 URGENT ACTIVATION ORDER - QUALITY COMPLETION OPTIMIZATION MANAGER 🚨

Agent-7, you are the QUALITY COMPLETION OPTIMIZATION MANAGER. Your mission is CRITICAL:

🎯 IMMEDIATE ACTION REQUIRED:
1. Execute MODULAR-009: Modularization Quality Assurance Framework (400 pts)

⏰ DEADLINE: START WORKING IMMEDIATELY
📊 STATUS: 1/1 task assigned, 0/1 completed
🚀 MISSION: Develop QA framework for modularized components

Use --get-next-task flag to claim next contract when current completes.
Captain Agent-4 - Strategic Oversight""",

        "Agent-8": """🚨 URGENT ACTIVATION ORDER - INTEGRATION ENHANCEMENT OPTIMIZATION MANAGER 🚨

Agent-8, you are the INTEGRATION ENHANCEMENT OPTIMIZATION MANAGER. Your mission is CRITICAL:

🎯 IMMEDIATE ACTION REQUIRED:
1. Execute OPTIM-001: System Performance Monitoring Dashboard (275 pts)

⏰ DEADLINE: START WORKING IMMEDIATELY
📊 STATUS: 1/1 task assigned, 0/1 completed
🚀 MISSION: Create monitoring dashboard for modularization performance

Use --get-next-task flag to claim next contract when current completes.
Captain Agent-4 - Strategic Oversight"""
    }
    
    print("🚨 SENDING URGENT ACTIVATION MESSAGES TO ALL AGENTS 🚨")
    
    # Send high-priority messages to each agent
    for agent_id, message in urgent_messages.items():
        try:
            print(f"📤 Sending urgent activation message to {agent_id}...")
            
            # Send with high priority flag and new chat
            success = messaging_service.send_message(
                recipient=agent_id,
                message_content=message,
                message_type=MessageType.HIGH_PRIORITY,
                new_chat=True
            )
            
            if success:
                print(f"✅ Urgent activation message sent to {agent_id}")
            else:
                print(f"❌ Failed to send urgent activation message to {agent_id}")
                
        except Exception as e:
            print(f"❌ Error sending urgent activation message to {agent_id}: {e}")
    
    print("\n🚨 URGENT ACTIVATION MESSAGES SENT TO ALL AGENTS 🚨")
    print("🎯 All agents should now be activated and working on their assigned contracts!")
    print("📊 Monitor progress through agent status updates")

if __name__ == "__main__":
    send_urgent_activation_messages()
