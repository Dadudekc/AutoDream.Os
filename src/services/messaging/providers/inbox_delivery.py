#!/usr/bin/env python3
"""
Inbox Message Delivery Provider - V2 Compliant Module
===================================================

File-based inbox delivery provider for messaging system.
V2 COMPLIANT: Focused delivery provider under 300 lines.

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

import os
from datetime import datetime
from pathlib import Path
from typing import List

try:
    from ..models.messaging_models import UnifiedMessage, MessageHistory
    from ..interfaces.messaging_interfaces import InboxDeliveryProvider, MessageHistoryProvider
except ImportError:
    # Fallback for direct execution
    from models.messaging_models import UnifiedMessage, MessageHistory
    from interfaces.messaging_interfaces import InboxDeliveryProvider, MessageHistoryProvider


class InboxMessageDelivery(InboxDeliveryProvider, MessageHistoryProvider):
    """File-based inbox message delivery provider."""

    def __init__(self, base_path: str = "agent_workspaces"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)

    def send_message(self, message: UnifiedMessage) -> bool:
        """Send message to agent's inbox file."""
        try:
            # Create agent workspace if it doesn't exist
            agent_dir = self.base_path / message.recipient
            agent_dir.mkdir(exist_ok=True)
            
            # Create inbox directory
            inbox_dir = agent_dir / "inbox"
            inbox_dir.mkdir(exist_ok=True)
            
            # Create message file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            message_file = inbox_dir / f"MESSAGE_{timestamp}_{message.message_id}.md"
            
            # Create message content
            message_content = self._create_message_content(message)
            
            # Write message file
            with open(message_file, 'w', encoding='utf-8') as f:
                f.write(message_content)
            
            # Save to history
            self.save_message(message)
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to send message to {message.recipient}: {e}")
            return False

    def _create_message_content(self, message: UnifiedMessage) -> str:
        """Create message content for inbox file."""
        priority_emoji = {
            "LOW": "🟢",
            "REGULAR": "🔵", 
            "HIGH": "🟡",
            "URGENT": "🔴"
        }
        
        emoji = priority_emoji.get(message.priority.value, "🔵")
        
        return f"""# {emoji} MESSAGE FROM {message.sender.upper()}

**From:** {message.sender}
**To:** {message.recipient}
**Type:** {message.message_type.value}
**Priority:** {message.priority.value}
**Timestamp:** {message.timestamp.isoformat()}
**Message ID:** {message.message_id}

---

{message.content}

---

**Delivered via Unified Messaging System**
**WE. ARE. SWARM. ⚡🐝**
"""

    def is_available(self) -> bool:
        """Check if file system is available."""
        try:
            # Test write access
            test_file = self.base_path / "test_write.tmp"
            test_file.write_text("test")
            test_file.unlink()
            return True
        except Exception:
            return False

    def get_inbox_messages(self, agent_id: str) -> List[UnifiedMessage]:
        """Get messages from agent's inbox."""
        try:
            inbox_dir = self.base_path / agent_id / "inbox"
            if not inbox_dir.exists():
                return []
            
            messages = []
            for message_file in inbox_dir.glob("MESSAGE_*.md"):
                # Parse message file to extract UnifiedMessage
                # This is a simplified implementation
                with open(message_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract basic info (simplified parsing)
                message = UnifiedMessage(
                    content=content,
                    recipient=agent_id,
                    sender="System",
                    message_id=message_file.stem
                )
                messages.append(message)
            
            return messages
            
        except Exception as e:
            print(f"❌ Failed to get inbox messages for {agent_id}: {e}")
            return []

    def save_message(self, message: UnifiedMessage) -> bool:
        """Save message to history."""
        try:
            # Create history directory
            history_dir = self.base_path / "history"
            history_dir.mkdir(exist_ok=True)
            
            # Create history file
            history_file = history_dir / f"{message.message_id}.json"
            
            # Save message as JSON
            import json
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(message.to_dict(), f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to save message to history: {e}")
            return False

    def get_message_history(self, agent_id: str, limit: int = 10) -> List[MessageHistory]:
        """Get message history for an agent."""
        try:
            history_dir = self.base_path / "history"
            if not history_dir.exists():
                return []
            
            history_entries = []
            history_files = sorted(history_dir.glob("*.json"), key=os.path.getmtime, reverse=True)
            
            for history_file in history_files[:limit]:
                try:
                    import json
                    with open(history_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    if data.get("recipient") == agent_id:
                        entry = MessageHistory(
                            message_id=data["message_id"],
                            content=data["content"],
                            sender=data["sender"],
                            recipient=data["recipient"],
                            timestamp=datetime.fromisoformat(data["timestamp"]),
                            status=data["status"],
                            delivery_method=data["delivery_method"]
                        )
                        history_entries.append(entry)
                        
                except Exception as e:
                    print(f"❌ Failed to parse history file {history_file}: {e}")
                    continue
            
            return history_entries
            
        except Exception as e:
            print(f"❌ Failed to get message history for {agent_id}: {e}")
            return []