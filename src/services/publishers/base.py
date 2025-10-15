"""
Base Publisher Interface - Multi-Platform Devlog Publishing
Extracted from Auto_Blogger repository and adapted for agent devlogs

Pattern Source: Auto_Blogger/autoblogger/services/publishing/base.py
Extraction Date: 2025-10-15
Extracted By: Agent-8
Value: 200 points (extensible architecture pattern)
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class DevlogPublisher(ABC):
    """
    Abstract base class for all platform-specific devlog publishers.
    
    Enables extensible multi-platform devlog posting:
    - Discord (current)
    - Slack (future)
    - GitHub Issues/Discussions (future)
    - Custom platforms (extensible)
    
    Pattern: Strategy pattern for publishing
    Benefit: Easy to add new platforms without changing client code
    """

    @abstractmethod
    def publish_devlog(
        self,
        agent_id: str,
        title: str,
        content: str,
        cycle: str = None,
        tags: list[str] = None,
        metadata: Dict[str, Any] = None
    ) -> bool:
        """
        Publish agent devlog to target platform.
        
        Args:
            agent_id: Agent identifier (e.g., "Agent-8")
            title: Devlog title
            content: Main devlog content
            cycle: Cycle identifier (e.g., "C-047")
            tags: List of hashtags for categorization
            metadata: Additional metadata (points, discoveries, etc.)
            
        Returns:
            bool: True if publish successful, False otherwise
        """
        pass

    @abstractmethod
    def validate_credentials(self) -> bool:
        """
        Validate publisher credentials/configuration.
        
        Returns:
            bool: True if credentials valid and ready to publish
        """
        pass

    @abstractmethod
    def get_publish_status(self, message_id: str) -> Optional[Dict[str, Any]]:
        """
        Get status of a published devlog.
        
        Args:
            message_id: Platform-specific message identifier
            
        Returns:
            Optional[Dict[str, Any]]: Status info or None if not found
        """
        pass


class DevlogPublishingHistory:
    """
    Track publishing history to prevent duplicates and enable analytics.
    
    Pattern extracted from Auto_Blogger's DevlogHarvester
    """
    
    def __init__(self, history_file: str = "devlog_history.json"):
        """Initialize history tracker."""
        self.history_file = history_file
        self.history = []
    
    def record_publish(
        self,
        devlog_id: str,
        platform: str,
        message_id: str,
        agent_id: str,
        title: str,
        timestamp: str = None
    ) -> None:
        """
        Record a devlog publication.
        
        Args:
            devlog_id: Unique devlog identifier
            platform: Platform name (discord, slack, etc.)
            message_id: Platform-specific message ID
            agent_id: Agent who posted
            title: Devlog title
            timestamp: Publication timestamp
        """
        entry = {
            "devlog_id": devlog_id,
            "platform": platform,
            "message_id": message_id,
            "agent_id": agent_id,
            "title": title,
            "timestamp": timestamp or self._current_timestamp()
        }
        self.history.append(entry)
        self._save_history()
    
    def was_published(self, devlog_id: str, platform: str = None) -> bool:
        """
        Check if devlog already published.
        
        Args:
            devlog_id: Devlog identifier to check
            platform: Optional platform filter
            
        Returns:
            bool: True if already published
        """
        for entry in self.history:
            if entry["devlog_id"] == devlog_id:
                if platform is None or entry["platform"] == platform:
                    return True
        return False
    
    def _save_history(self):
        """Save history to file (implement based on storage preference)."""
        # TODO: Implement JSON persistence
        pass
    
    def _current_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()

