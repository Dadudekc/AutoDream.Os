#!/usr/bin/env python3
"""
Utility Handler
===============

Handles utility CLI operations like status checking and history.
Extracted from messaging_cli_handlers_orchestrator.py for V2 compliance.

Author: Agent-8 (SSOT & System Integration Specialist)
License: MIT
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from ...utils.agent_registry import list_agents as registry_list_agents

try:
    from ...models.messaging_models import UnifiedMessage
    from ....core.unified_data_processing_system import read_json, write_json
except ImportError:
    # Fallback implementations
    class UnifiedMessage:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    
    def read_json(file_path: str) -> Dict[str, Any]:
        return {}
    
    def write_json(file_path: str, data: Dict[str, Any]) -> bool:
        return True


class UtilityHandler:
    """Handles utility operations for messaging CLI."""
    
    def __init__(self):
        """Initialize utility handler."""
        self.logger = logging.getLogger(__name__)
        self.message_history: List[Dict[str, Any]] = []
        
    def check_agent_status(self, agent_id: Optional[str] = None) -> Dict[str, Any]:
        """Check status of agents."""
        try:
            if agent_id:
                return self._check_single_agent_status(agent_id)
            else:
                return self._check_all_agents_status()
                
        except Exception as e:
            self.logger.error(f"Failed to check agent status: {e}")
            return {"status": "error", "message": str(e)}
    
    def _check_single_agent_status(self, agent_id: str) -> Dict[str, Any]:
        """Check status of a single agent."""
        try:
            # Try to read agent status file
            status_file = f"agent_workspaces/{agent_id}/status.json"
            status_data = read_json(status_file)
            
            if status_data:
                return {
                    "agent_id": agent_id,
                    "status": "active",
                    "data": status_data,
                    "last_updated": status_data.get("last_updated", "unknown")
                }
            else:
                return {
                    "agent_id": agent_id,
                    "status": "inactive",
                    "message": "No status file found"
                }
                
        except Exception as e:
            self.logger.error(f"Failed to check status for {agent_id}: {e}")
            return {
                "agent_id": agent_id,
                "status": "error",
                "message": str(e)
            }
    
    def _check_all_agents_status(self) -> Dict[str, Any]:
        """Check status of all agents."""
        try:
            agents = registry_list_agents()
            
            status_results = {}
            active_count = 0
            
            for agent_id in agents:
                agent_status = self._check_single_agent_status(agent_id)
                status_results[agent_id] = agent_status
                
                if agent_status.get("status") == "active":
                    active_count += 1
            
            return {
                "total_agents": len(agents),
                "active_agents": active_count,
                "inactive_agents": len(agents) - active_count,
                "agent_details": status_results,
                "checked_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to check all agents status: {e}")
            return {"status": "error", "message": str(e)}
    
    def add_to_history(self, message: UnifiedMessage, delivery_result: bool) -> None:
        """Add message to history."""
        try:
            history_entry = {
                "timestamp": datetime.now().isoformat(),
                "message_id": getattr(message, 'message_id', 'unknown'),
                "sender": getattr(message, 'sender', 'unknown'),
                "recipient": getattr(message, 'recipient', 'unknown'),
                "content": getattr(message, 'content', ''),
                "priority": getattr(message, 'priority', 'normal'),
                "delivery_successful": delivery_result
            }
            
            self.message_history.append(history_entry)
            
            # Keep only last 100 messages
            if len(self.message_history) > 100:
                self.message_history = self.message_history[-100:]
                
            self.logger.debug(f"Added message to history: {history_entry['message_id']}")
            
        except Exception as e:
            self.logger.error(f"Failed to add message to history: {e}")
    
    def get_message_history(self, limit: int = 10, agent_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get message history with optional filtering."""
        try:
            history = self.message_history.copy()
            
            # Filter by agent if specified
            if agent_id:
                history = [
                    msg for msg in history 
                    if msg.get('recipient') == agent_id or msg.get('sender') == agent_id
                ]
            
            # Return most recent messages first
            history.reverse()
            return history[:limit]
            
        except Exception as e:
            self.logger.error(f"Failed to get message history: {e}")
            return []
    
    def display_message_history(self, limit: int = 10, agent_id: Optional[str] = None) -> None:
        """Display message history in formatted output."""
        try:
            history = self.get_message_history(limit, agent_id)
            
            if not history:
                print("📜 No message history found")
                return
            
            title = f"📜 Message History"
            if agent_id:
                title += f" for {agent_id}"
            title += f" (Last {len(history)} messages)"
            
            print(f"\n{title}")
            print("=" * 60)
            
            for entry in history:
                timestamp = entry.get('timestamp', 'unknown')
                sender = entry.get('sender', 'unknown')
                recipient = entry.get('recipient', 'unknown')
                success = entry.get('delivery_successful', False)
                status_icon = "✅" if success else "❌"
                
                print(f"{status_icon} {timestamp}")
                print(f"   From: {sender} → To: {recipient}")
                print(f"   Content: {entry.get('content', '')[:50]}...")
                print(f"   Priority: {entry.get('priority', 'normal')}")
                print("-" * 60)
            
            print(f"Total messages shown: {len(history)}")
            
        except Exception as e:
            self.logger.error(f"Failed to display message history: {e}")
            print(f"❌ Error displaying history: {e}")
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information and statistics."""
        try:
            return {
                "history_size": len(self.message_history),
                "max_history_size": 100,
                "successful_deliveries": len([
                    msg for msg in self.message_history 
                    if msg.get('delivery_successful', False)
                ]),
                "failed_deliveries": len([
                    msg for msg in self.message_history 
                    if not msg.get('delivery_successful', True)
                ]),
                "unique_senders": len(set(
                    msg.get('sender', 'unknown') 
                    for msg in self.message_history
                )),
                "unique_recipients": len(set(
                    msg.get('recipient', 'unknown') 
                    for msg in self.message_history
                )),
                "system_status": "operational"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get system info: {e}")
            return {"status": "error", "message": str(e)}
    
    def clear_history(self) -> bool:
        """Clear message history."""
        try:
            history_size = len(self.message_history)
            self.message_history.clear()
            self.logger.info(f"Cleared message history ({history_size} entries)")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to clear history: {e}")
            return False
    
    def export_history(self, format_type: str = "json") -> Optional[str]:
        """Export message history in specified format."""
        try:
            if format_type.lower() == "json":
                import json
                return json.dumps(self.message_history, indent=2)
            elif format_type.lower() == "csv":
                lines = ["Timestamp,Sender,Recipient,Priority,Success,Content"]
                for msg in self.message_history:
                    content = msg.get('content', '').replace(',', ';').replace('\n', ' ')
                    lines.append(
                        f"{msg.get('timestamp', '')},{msg.get('sender', '')},"
                        f"{msg.get('recipient', '')},{msg.get('priority', '')},"
                        f"{msg.get('delivery_successful', False)},{content[:100]}"
                    )
                return "\n".join(lines)
            else:
                self.logger.warning(f"Unsupported export format: {format_type}")
                return None
                
        except Exception as e:
            self.logger.error(f"Failed to export history: {e}")
            return None
