#!/usr/bin/env python3
"""
Thea Conversation Manager - Persistent Conversation Link Management
================================================================

Manages conversation links for Thea strategic consultations, enabling agents
to continue existing conversations or start new ones as needed.

Features:
- Save conversation links when created
- Load existing conversations for continuation
- Track conversation metadata and history
- Enable agents to rejoin strategic consultations
- Automatic conversation link extraction from browser

Usage:
    from src.services.thea.thea_conversation_manager import TheaConversationManager
    
    manager = TheaConversationManager()
    link = manager.get_active_conversation_link()
    if link:
        # Continue existing conversation
        thea.load_conversation(link)
    else:
        # Start new conversation
        thea.start_new_conversation()
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class ConversationMetadata:
    """Metadata for a Thea conversation."""
    conversation_id: str
    conversation_link: str
    created_at: datetime
    last_accessed: datetime
    message_count: int
    participants: List[str]
    topic: str
    status: str  # active, archived, closed


class TheaConversationManager:
    """Manages persistent conversation links for Thea strategic consultations."""
    
    def __init__(self, conversations_file: str = "thea_conversations.json"):
        """
        Initialize the conversation manager.
        
        Args:
            conversations_file: Path to store conversation metadata
        """
        self.conversations_file = Path(conversations_file)
        self.conversations: Dict[str, ConversationMetadata] = {}
        self.active_conversation_id: Optional[str] = None
        self._load_conversations()
    
    def _load_conversations(self):
        """Load conversation metadata from file."""
        try:
            if self.conversations_file.exists():
                with open(self.conversations_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Convert back to ConversationMetadata objects
                for conv_id, conv_data in data.get('conversations', {}).items():
                    conv_data['created_at'] = datetime.fromisoformat(conv_data['created_at'])
                    conv_data['last_accessed'] = datetime.fromisoformat(conv_data['last_accessed'])
                    self.conversations[conv_id] = ConversationMetadata(**conv_data)
                
                self.active_conversation_id = data.get('active_conversation_id')
                logger.info(f"Loaded {len(self.conversations)} conversations")
            else:
                logger.info("No existing conversations file found")
                
        except Exception as e:
            logger.error(f"Failed to load conversations: {e}")
            self.conversations = {}
    
    def _save_conversations(self):
        """Save conversation metadata to file."""
        try:
            # Convert ConversationMetadata objects to dicts for JSON serialization
            conversations_data = {}
            for conv_id, conv_meta in self.conversations.items():
                conv_dict = asdict(conv_meta)
                conv_dict['created_at'] = conv_meta.created_at.isoformat()
                conv_dict['last_accessed'] = conv_meta.last_accessed.isoformat()
                conversations_data[conv_id] = conv_dict
            
            data = {
                'conversations': conversations_data,
                'active_conversation_id': self.active_conversation_id,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.conversations_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.debug(f"Saved {len(self.conversations)} conversations")
            
        except Exception as e:
            logger.error(f"Failed to save conversations: {e}")
    
    def extract_conversation_link(self, driver) -> Optional[str]:
        """
        Extract the current conversation link from the browser.
        
        Args:
            driver: Selenium WebDriver instance
            
        Returns:
            Conversation link URL, or None if not found
        """
        try:
            current_url = driver.current_url
            logger.info(f"Current URL: {current_url}")
            
            # Check if this is a conversation URL
            if "/c/" in current_url:
                logger.info(f"Found conversation link: {current_url}")
                return current_url
            else:
                logger.info("No conversation link found in current URL")
                return None
                
        except Exception as e:
            logger.error(f"Failed to extract conversation link: {e}")
            return None
    
    def create_new_conversation(self, driver, topic: str = "Strategic Consultation") -> str:
        """
        Create a new conversation and save its link.
        
        Args:
            driver: Selenium WebDriver instance
            topic: Topic/description of the conversation
            
        Returns:
            Conversation ID
        """
        try:
            # Extract conversation link from current page
            conversation_link = self.extract_conversation_link(driver)
            
            if not conversation_link:
                logger.warning("Could not extract conversation link, creating placeholder")
                conversation_link = f"https://chatgpt.com/c/placeholder-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            
            # Generate conversation ID
            conversation_id = f"thea_conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Create conversation metadata
            now = datetime.now()
            conversation_meta = ConversationMetadata(
                conversation_id=conversation_id,
                conversation_link=conversation_link,
                created_at=now,
                last_accessed=now,
                message_count=0,
                participants=["General Agent-4", "Commander Thea"],
                topic=topic,
                status="active"
            )
            
            # Save conversation
            self.conversations[conversation_id] = conversation_meta
            self.active_conversation_id = conversation_id
            self._save_conversations()
            
            logger.info(f"Created new conversation: {conversation_id}")
            logger.info(f"Conversation link: {conversation_link}")
            
            return conversation_id
            
        except Exception as e:
            logger.error(f"Failed to create new conversation: {e}")
            return f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def get_active_conversation_link(self) -> Optional[str]:
        """
        Get the link to the currently active conversation.
        
        Returns:
            Active conversation link, or None if no active conversation
        """
        if self.active_conversation_id and self.active_conversation_id in self.conversations:
            conv_meta = self.conversations[self.active_conversation_id]
            if conv_meta.status == "active":
                logger.info(f"Retrieved active conversation link: {conv_meta.conversation_link}")
                return conv_meta.conversation_link
        
        logger.info("No active conversation found")
        return None
    
    def load_conversation(self, conversation_link: str) -> bool:
        """
        Load an existing conversation by its link.
        
        Args:
            conversation_link: URL of the conversation to load
            
        Returns:
            True if conversation loaded successfully, False otherwise
        """
        try:
            # Find conversation by link
            for conv_id, conv_meta in self.conversations.items():
                if conv_meta.conversation_link == conversation_link:
                    self.active_conversation_id = conv_id
                    conv_meta.last_accessed = datetime.now()
                    conv_meta.status = "active"
                    self._save_conversations()
                    
                    logger.info(f"Loaded conversation: {conv_id}")
                    return True
            
            logger.warning(f"Conversation not found: {conversation_link}")
            return False
            
        except Exception as e:
            logger.error(f"Failed to load conversation: {e}")
            return False
    
    def update_conversation_activity(self, message_count: int = None):
        """
        Update the active conversation's activity metadata.
        
        Args:
            message_count: Optional message count to update
        """
        if self.active_conversation_id and self.active_conversation_id in self.conversations:
            conv_meta = self.conversations[self.active_conversation_id]
            conv_meta.last_accessed = datetime.now()
            
            if message_count is not None:
                conv_meta.message_count = message_count
            
            self._save_conversations()
            logger.debug(f"Updated conversation activity: {self.active_conversation_id}")
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """
        Get a list of all conversations with their metadata.
        
        Returns:
            List of conversation metadata dictionaries
        """
        history = []
        for conv_id, conv_meta in self.conversations.items():
            history.append({
                'conversation_id': conv_id,
                'topic': conv_meta.topic,
                'created_at': conv_meta.created_at.isoformat(),
                'last_accessed': conv_meta.last_accessed.isoformat(),
                'message_count': conv_meta.message_count,
                'status': conv_meta.status,
                'link': conv_meta.conversation_link
            })
        
        # Sort by last accessed (most recent first)
        history.sort(key=lambda x: x['last_accessed'], reverse=True)
        return history
    
    def archive_conversation(self, conversation_id: str = None):
        """
        Archive a conversation (set status to archived).
        
        Args:
            conversation_id: ID of conversation to archive (defaults to active)
        """
        if conversation_id is None:
            conversation_id = self.active_conversation_id
        
        if conversation_id and conversation_id in self.conversations:
            self.conversations[conversation_id].status = "archived"
            self._save_conversations()
            logger.info(f"Archived conversation: {conversation_id}")
            
            # Clear active conversation if it was archived
            if conversation_id == self.active_conversation_id:
                self.active_conversation_id = None
        else:
            logger.warning(f"Conversation not found for archiving: {conversation_id}")
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the conversation manager.
        
        Returns:
            Status dictionary with conversation counts and active conversation info
        """
        active_conv = None
        if self.active_conversation_id and self.active_conversation_id in self.conversations:
            conv_meta = self.conversations[self.active_conversation_id]
            active_conv = {
                'conversation_id': self.active_conversation_id,
                'topic': conv_meta.topic,
                'link': conv_meta.conversation_link,
                'message_count': conv_meta.message_count,
                'last_accessed': conv_meta.last_accessed.isoformat()
            }
        
        return {
            'total_conversations': len(self.conversations),
            'active_conversation': active_conv,
            'conversations_file': str(self.conversations_file),
            'last_updated': datetime.now().isoformat()
        }


# Convenience functions
def get_active_conversation_link() -> Optional[str]:
    """Get the currently active conversation link."""
    manager = TheaConversationManager()
    return manager.get_active_conversation_link()


def create_conversation_manager() -> TheaConversationManager:
    """Create a new conversation manager instance."""
    return TheaConversationManager()


if __name__ == "__main__":
    # Test the conversation manager
    print("🤖 Thea Conversation Manager Test")
    print("=" * 50)
    
    manager = TheaConversationManager()
    status = manager.get_status()
    
    print(f"📊 Status: {json.dumps(status, indent=2)}")
    
    history = manager.get_conversation_history()
    print(f"📚 Conversation History: {len(history)} conversations")
    
    for conv in history[:3]:  # Show first 3
        print(f"  • {conv['conversation_id']}: {conv['topic']} ({conv['status']})")




