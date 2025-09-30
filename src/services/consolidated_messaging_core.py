"""
Consolidated Messaging Service Core
V2 Compliant core messaging functionality
"""

import logging
import time
from datetime import datetime
from typing import Dict, List, Optional

try:
    import pyautogui
    import pyperclip
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    pyautogui = None
    pyperclip = None
    PYAUTOGUI_AVAILABLE = False

from .messaging_models import Message, MessagePriority, MessageStatus, MessageType, AgentStatus


class ConsolidatedMessagingService:
    """Consolidated messaging service - V2 Compliant"""
    
    def __init__(self):
        """Initialize messaging service"""
        self.messages: List[Message] = []
        self.agent_status: Dict[str, AgentStatus] = {}
        self.logger = logging.getLogger(__name__)
        
    def send_message(self, sender: str, recipient: str, content: str, 
                    priority: MessagePriority = MessagePriority.NORMAL) -> bool:
        """Send a message"""
        if not PYAUTOGUI_AVAILABLE:
            self.logger.error("PyAutoGUI not available")
            return False
            
        message = Message(
            message_id=f"msg_{len(self.messages) + 1}",
            sender=sender,
            recipient=recipient,
            content=content,
            message_type=MessageType.TEXT,
            priority=priority,
            status=MessageStatus.PENDING,
            timestamp=datetime.now(),
            metadata={}
        )
        
        try:
            # Copy message to clipboard
            pyperclip.copy(content)
            
            # Send via PyAutoGUI (simplified)
            success = self._send_via_pyautogui(recipient, content)
            
            if success:
                message.status = MessageStatus.SENT
                self.logger.info(f"Message sent from {sender} to {recipient}")
            else:
                message.status = MessageStatus.FAILED
                self.logger.error(f"Failed to send message from {sender} to {recipient}")
                
        except Exception as e:
            message.status = MessageStatus.FAILED
            self.logger.error(f"Error sending message: {e}")
            
        self.messages.append(message)
        return message.status == MessageStatus.SENT
        
    def _send_via_pyautogui(self, recipient: str, content: str) -> bool:
        """Send message via PyAutoGUI"""
        try:
            # Simplified PyAutoGUI sending
            # In a real implementation, this would use agent coordinates
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.1)
            pyautogui.press('enter')
            return True
        except Exception as e:
            self.logger.error(f"PyAutoGUI error: {e}")
            return False
            
    def get_agent_status(self, agent_id: str) -> Optional[AgentStatus]:
        """Get agent status"""
        return self.agent_status.get(agent_id)
        
    def update_agent_status(self, agent_id: str, status: str, 
                          coordinates: tuple[int, int], current_task: Optional[str] = None):
        """Update agent status"""
        self.agent_status[agent_id] = AgentStatus(
            agent_id=agent_id,
            status=status,
            last_seen=datetime.now(),
            coordinates=coordinates,
            current_task=current_task,
            performance_score=95.0  # Placeholder
        )
        
    def get_messaging_metrics(self) -> Dict[str, int]:
        """Get messaging metrics"""
        total = len(self.messages)
        successful = sum(1 for msg in self.messages if msg.status == MessageStatus.SENT)
        failed = sum(1 for msg in self.messages if msg.status == MessageStatus.FAILED)
        
        return {
            "total_messages": total,
            "successful_messages": successful,
            "failed_messages": failed,
            "active_agents": len(self.agent_status)
        }
        
    def stall_agent(self, agent_id: str) -> bool:
        """Stall an agent"""
        if agent_id in self.agent_status:
            self.agent_status[agent_id].status = "stalled"
            self.logger.info(f"Agent {agent_id} stalled")
            return True
        return False
        
    def unstall_agent(self, agent_id: str) -> bool:
        """Unstall an agent"""
        if agent_id in self.agent_status:
            self.agent_status[agent_id].status = "active"
            self.logger.info(f"Agent {agent_id} unstalled")
            return True
        return False
