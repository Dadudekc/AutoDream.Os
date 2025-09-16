import logging
logger = logging.getLogger(__name__)
"""
Agent-8 Coordination Interface
==============================
Operations & Support Specialist coordination interface
"""
import sys
sys.path.append('.')
from datetime import datetime
from src.core.messaging_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority, UnifiedMessageTag
from src.core.messaging_pyautogui import deliver_message_pyautogui, format_message_for_delivery


def send_coordination_message(agent_id: str, message: str, priority: str=
    'NORMAL', tag: str='COORDINATION'):
    """Send coordination message to specified agent."""
    try:
        unified_message = UnifiedMessage(content=message, sender='Agent-8',
            recipient=agent_id, message_type=UnifiedMessageType.
            AGENT_TO_AGENT, priority=UnifiedMessagePriority(priority), tags
            =[UnifiedMessageTag(tag)], timestamp=datetime.now())
        formatted_message = format_message_for_delivery(unified_message)
        success = deliver_message_pyautogui(unified_message)
        logger.info(f'✅ Message sent to {agent_id}: {success}')
        return success
    except Exception as e:
        logger.info(f'❌ Failed to send message to {agent_id}: {e}')
        return False


def broadcast_coordination_message(message: str, priority: str='NORMAL',
    tag: str='COORDINATION'):
    """Broadcast coordination message to all agents."""
    try:
        unified_message = UnifiedMessage(content=message, sender='Agent-8',
            recipient='ALL_AGENTS', message_type=UnifiedMessageType.
            BROADCAST, priority=UnifiedMessagePriority(priority), tags=[
            UnifiedMessageTag(tag)], timestamp=datetime.now())
        formatted_message = format_message_for_delivery(unified_message)
        success = deliver_message_pyautogui(unified_message)
        logger.info(f'✅ Broadcast message sent: {success}')
        return success
    except Exception as e:
        logger.info(f'❌ Failed to send broadcast message: {e}')
        return False


if __name__ == '__main__':
    logger.info('🛠️ Agent-8 Coordination Interface Active')
    send_coordination_message('Agent-4',
        'AGENT-8 OPERATIONS SPECIALIST: Enhanced cycle coordination active. FSM State: IDLE → ACTIVE. Contract system operational. Operations tools available. Multi-agent coordination active. Consolidation opportunities: 70+ files identified. Requesting Captain coordination for operations mission execution. WE ARE SWARM!'
        , 'NORMAL', 'COORDINATION')
