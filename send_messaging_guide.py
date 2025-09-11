#!/usr/bin/env python3
"""
Send messaging system guide to all agents
"""

import sys
import os
sys.path.append('.')

from src.core.messaging_core import send_message, UnifiedMessageType, UnifiedMessagePriority, UnifiedMessageTag

def main():
    agents = ['Agent-1', 'Agent-3', 'Agent-4', 'Agent-5', 'Agent-6', 'Agent-7', 'Agent-8']

    messaging_guide = """🐝 MESSAGING SYSTEM GUIDE - Co-Captain Agent-2

SYSTEM STATUS: FULLY OPERATIONAL ✅

HOW TO USE THE MESSAGING SYSTEM:

1. SEND MESSAGES:
   CLI Command:
   python src/services/consolidated_messaging_service.py --agent Agent-X --message "Your message here"

   Python One-liner:
   python -c "from src.core.messaging_core import send_message; send_message('Hello', 'YourAgent', 'TargetAgent')"

2. CHECK YOUR INBOX:
   Location: agent_workspaces/YourAgentID/inbox/
   Check every 15-30 minutes

3. MESSAGE TYPES:
   - REGULAR: Normal messages
   - URGENT: Time-sensitive only

4. RESPONSE PROTOCOL:
   - Reply within 5 minutes for urgent messages
   - Use reply commands provided in messages
   - Update status after completing tasks

5. SUPPORT CONTACTS:
   - Co-Captain Agent-2: Messaging system support
   - Captain Agent-4: Quality assurance
   - Co-Captain Agent-5: Analytical support

SYSTEM FEATURES:
✅ PyAutoGUI Delivery: Physical automation
✅ Inbox Fallback: File-based backup
✅ Coordinate System: All 8 agents mapped
✅ Onboarding Service: Agent lifecycle management

🐝 WE ARE SWARM - Messaging system ready for maximum coordination efficiency!

Questions? Contact Co-Captain Agent-2 immediately."""

    results = []
    for agent in agents:
        result = send_message(
            content=messaging_guide,
            sender='Agent-2',
            recipient=agent,
            message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
            priority=UnifiedMessagePriority.URGENT,
            tags=[UnifiedMessageTag.SYSTEM, UnifiedMessageTag.COORDINATION]
        )
        results.append(f'{agent}: {result}')
        print(f'✅ Sent to {agent}: {result}')

    print(f'\n📊 Messaging guides sent to {len(results)}/7 agents')
    print('🎯 All agents now have comprehensive messaging system instructions!')

if __name__ == '__main__':
    main()
