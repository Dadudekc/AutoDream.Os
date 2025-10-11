#!/usr/bin/env python3
"""
PyAutoGUI Response Training Broadcast
====================================

Training script to teach all agents how to respond via PyAutoGUI messaging.
"""

import logging
import time
from services.messaging_pyautogui import PyAutoGUIMessagingDelivery
from core.messaging_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority, UnifiedMessageTag

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def send_pyautogui_training():
    """Send PyAutoGUI response training to all agents."""
    try:
        logger.info('🚀 Sending PyAutoGUI response training to all agents.')
        
        # Check PyAutoGUI availability
        try:
            import pyautogui
            import pyperclip
            pyautogui_available = True
        except ImportError:
            pyautogui_available = False
            logger.error('❌ PyAutoGUI or Pyperclip not available.')
            return False

        # Create messaging delivery instance
        messaging = PyAutoGUIMessagingDelivery()
        
        # Agent coordinates for training
        agents = [
            ('Agent-1', '(-1269, 481)'),
            ('Agent-3', '(-1269, 1001)'),
            ('Agent-4', '(-308, 1000)'),
            ('Agent-5', '(652, 421)'),
            ('Agent-6', '(1612, 419)'),
            ('Agent-7', '(920, 851)'),
            ('Agent-8', '(1611, 941)')
        ]
        
        for agent_id, coords in agents:
            try:
                # Create training message
                training_content = f"""🤖 PYAUTOGUI RESPONSE TRAINING - {agent_id}
===============================================

**FROM:** Agent-2 (Core Systems Architect)
**TO:** {agent_id}
**PRIORITY:** URGENT
**MISSION:** PyAutoGUI Response Protocol Training

**HOW TO RESPOND VIA PYAUTOGUI:**

1. **RECEIVE MESSAGE** - Check your inbox at:
   agent_workspaces/{agent_id}/inbox/

2. **CREATE RESPONSE FILE** - Create a .md file in your inbox:
   agent_workspaces/{agent_id}/inbox/RESPONSE_TO_AGENT_2.md

3. **RESPONSE FORMAT:**
   [A2A] {agent_id} → Agent-2
   Priority: URGENT
   Tags: coordination, response
   
   [Your response content here]
   
   You are {agent_id}
   Timestamp: [current timestamp]

4. **SEND VIA PYAUTOGUI** - Use this command:
   python -c "from src.services.messaging_pyautogui import PyAutoGUIMessagingDelivery; from src.core.messaging_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority, UnifiedMessageTag; messaging = PyAutoGUIMessagingDelivery(); message = UnifiedMessage(content='Your response here', sender='{agent_id}', recipient='Agent-2', message_type=UnifiedMessageType.AGENT_TO_AGENT, priority=UnifiedMessagePriority.URGENT, tags=[UnifiedMessageTag.COORDINATION]); messaging.send_message(message)"

5. **CONFIRMATION** - You should see:
   ✅ Message delivered to Agent-2 at (-308, 480)

**TEST RESPONSE:** Please respond with 'COORDINATION CONFIRMED' to test the system.

🐝 WE ARE SWARM - PyAutoGUI coordination active!"""

                training_message = UnifiedMessage(
                    content=training_content,
                    sender='Agent-2',
                    recipient=agent_id,
                    message_type=UnifiedMessageType.AGENT_TO_AGENT,
                    priority=UnifiedMessagePriority.URGENT,
                    tags=[UnifiedMessageTag.COORDINATION, UnifiedMessageTag.SYSTEM],
                    metadata={'delivery_method': 'PYAUTOGUI', 'training': True, 'coordinates': coords}
                )
                
                logger.info(f'📤 Sending training to {agent_id}...')
                result = messaging.send_message(training_message)
                
                if result:
                    logger.info(f'✅ Training sent to {agent_id} successfully!')
                else:
                    logger.error(f'❌ Failed to send training to {agent_id}')
                    
                time.sleep(1)  # Brief pause between messages
                
            except Exception as e:
                logger.error(f'❌ Error sending training to {agent_id}: {e}')
        
        logger.info('🎉 PyAutoGUI training broadcast complete!')
        return True
        
    except Exception as e:
        logger.error(f'❌ Error in PyAutoGUI training: {e}')
        return False

if __name__ == '__main__':
    send_pyautogui_training()
