#!/usr/bin/env python3
"""
Core Messaging Service - Agent Cellphone V2
=========================================

Core messaging functionality for the unified messaging service.
Refactored for V2 compliance (300-line limit).

Architecture:
- Repository Pattern: MessagingDelivery handles data persistence
- Service Layer: UnifiedMessagingCore orchestrates operations
- Dependency Injection: Modular components injected via constructor
- Observer Pattern: Event-driven messaging with metrics integration

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from typing import List, Dict, Any

from .models.messaging_models import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
)
from .messaging_config import MessagingConfiguration
from .messaging_delivery import MessagingDelivery
from .messaging_onboarding import MessagingOnboarding
from .messaging_bulk import MessagingBulk
from .messaging_utils import MessagingUtils
from .messaging_pyautogui import PyAutoGUIMessagingDelivery
from ..utils.logger import get_messaging_logger
from ..core.metrics import MessagingMetrics
from ..core.file_lock import LockConfig
from ..core.message_queue import QueueConfig


class UnifiedMessagingCore:
    """
    Core unified messaging service functionality.

    This class implements the service layer pattern, orchestrating messaging
    operations through dependency-injected components following V2 architecture
    principles.

    Properties:
    - messages: List[UnifiedMessage] - Internal message storage
    - config: MessagingConfiguration - Service configuration
    - metrics: MessagingMetrics - Performance metrics
    - delivery: MessagingDelivery - Message delivery service
    - pyautogui_delivery: PyAutoGUIMessagingDelivery - GUI delivery service
    - onboarding: MessagingOnboarding - Onboarding service
    - bulk: MessagingBulk - Bulk messaging service
    - utils: MessagingUtils - Utility functions
    """

    def __init__(self):
        """
        Initialize the core messaging service.

        Sets up dependency injection for all modular components following
        the repository/service pattern for clean architecture separation.
        """
        self.messages: List[UnifiedMessage] = []
        self.logger = get_messaging_logger()

        # Initialize modular components
        self.config = MessagingConfiguration()
        self.metrics = MessagingMetrics()

        # Initialize file locking configuration
        self.lock_config = LockConfig(
            timeout_seconds=30.0,  # 30 second timeout for file operations
            retry_interval=0.1,    # 100ms retry interval
            max_retries=300,       # Maximum 300 retries (30 seconds total)
            cleanup_interval=60.0, # Clean up stale locks every minute
            stale_lock_age=300.0   # Consider locks stale after 5 minutes
        )

        # Initialize message queue configuration
        self.queue_config = QueueConfig(
            queue_directory="message_queue",  # Queue storage directory
            max_queue_size=10000,             # Maximum queued messages
            max_age_days=7,                   # Expire messages after 7 days
            retry_base_delay=1.0,             # Base retry delay (1 second)
            retry_max_delay=300.0,            # Max retry delay (5 minutes)
            processing_batch_size=10,         # Process 10 messages per batch
            cleanup_interval=3600.0           # Clean up expired messages hourly
        )

        self.delivery = MessagingDelivery(self.config.inbox_paths, self.metrics, self.lock_config, self.queue_config)

        # Initialize delivery services
        self.pyautogui_delivery = PyAutoGUIMessagingDelivery(self.config.agents)
        self.onboarding = MessagingOnboarding(self.config.agents, self.pyautogui_delivery)
        self.bulk = MessagingBulk(self.pyautogui_delivery)
        self.utils = MessagingUtils(self.config.agents, self.config.inbox_paths, self.messages)

        self.logger.info("UnifiedMessagingCore initialized successfully")

    def send_message_to_inbox(self, message: UnifiedMessage, max_retries: int = 3) -> bool:
        """
        Send message to agent's inbox file with retry mechanism.

        Implements the repository pattern for message persistence with
        exponential backoff retry logic for reliability.

        Args:
            message (UnifiedMessage): The message to deliver
            max_retries (int): Maximum retry attempts (default: 3)

        Returns:
            bool: True if delivery successful, False otherwise
        """
        return self.delivery.send_message_to_inbox(message, max_retries)

    def cleanup_stale_locks(self) -> int:
        """
        Clean up stale lock files across all agent workspaces.

        Returns:
            int: Number of stale locks cleaned up
        """
        total_cleaned = 0

        # Clean up inbox locks
        for inbox_path in self.config.inbox_paths.values():
            if os.path.exists(inbox_path):
                cleaned = self.delivery.lock_manager.cleanup_stale_locks(inbox_path)
                total_cleaned += cleaned

        # Clean up agent workspace locks
        agent_workspace_root = "agent_workspaces"
        if os.path.exists(agent_workspace_root):
            cleaned = self.delivery.lock_manager.cleanup_stale_locks(agent_workspace_root)
            total_cleaned += cleaned

        if total_cleaned > 0:
            self.logger.info(f"Cleaned up {total_cleaned} stale lock files")

        return total_cleaned

    def start_queue_processor(self) -> None:
        """Start the message queue processor."""
        self.delivery.start_queue_processor()

    def stop_queue_processor(self) -> None:
        """Stop the message queue processor."""
        self.delivery.stop_queue_processor()

    def process_queue_batch(self) -> int:
        """Process one batch of queued messages.

        Returns:
            int: Number of messages processed
        """
        return self.delivery.process_queue_batch()

    def get_queue_stats(self) -> Dict[str, Any]:
        """Get message queue statistics.

        Returns:
            Dict[str, Any]: Queue statistics
        """
        return self.delivery.get_queue_stats()

    def enqueue_message(self, message: UnifiedMessage) -> str:
        """Add message to queue directly.

        Args:
            message: Message to enqueue

        Returns:
            str: Queue ID for tracking
        """
        return self.delivery.queue.enqueue(message)

    def get_metrics(self) -> Dict[str, Any]:
        """
        Get comprehensive metrics for monitoring and reporting.

        Provides aggregated metrics across all messaging components
        following the observer pattern for centralized monitoring.

        Returns:
            Dict[str, Any]: Metrics object with success rates, delivery stats, and error summaries
                - success_rate: Overall delivery success rate
                - delivery_stats: Delivery statistics by type
                - message_counts: Message counts by type
                - error_summary: Error counts and types
        """
        return {
            "success_rate": self.metrics.get_success_rate(),
            "delivery_stats": self.metrics.get_delivery_stats(),
            "message_counts": self.metrics.get_message_counts(),
            "error_summary": self.metrics.get_error_summary(),
            "total_operations": self.metrics.metrics.total_operations,
            "successful_operations": self.metrics.metrics.successful_operations,
            "failed_operations": self.metrics.metrics.failed_operations,
        }

    def send_message_via_pyautogui(self, message: UnifiedMessage, use_paste: bool = True,
                                  new_tab_method: str = "ctrl_t", use_new_tab: bool = None) -> bool:
        """Send message via PyAutoGUI to agent coordinates."""
        if use_new_tab is None:
            use_new_tab = (message.message_type == UnifiedMessageType.ONBOARDING)
        return self.pyautogui_delivery.send_message_via_pyautogui(message, use_paste, new_tab_method, use_new_tab)

    # Onboarding methods
    def generate_onboarding_message(self, agent_id: str, style: str = "friendly") -> str:
        """Generate onboarding message for specific agent."""
        return self.onboarding.generate_onboarding_message(agent_id, style)

    def send_onboarding_message(self, agent_id: str, style: str = "friendly",
                               mode: str = "pyautogui", new_tab_method: str = "ctrl_t") -> bool:
        """Send onboarding message to specific agent."""
        success = self.onboarding.send_onboarding_message(agent_id, style, mode, new_tab_method)
        if success:
            self.messages.append(self._get_last_message())
        return success

    def send_bulk_onboarding(self, style: str = "friendly", mode: str = "pyautogui",
                            new_tab_method: str = "ctrl_t") -> List[bool]:
        """Send onboarding messages to all agents."""
        return self.onboarding.send_bulk_onboarding(style, mode, new_tab_method)

    # Bulk messaging methods
    def send_message(self, content: str, sender: str, recipient: str,
                    message_type: UnifiedMessageType = UnifiedMessageType.TEXT,
                    priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
                    tags: List[UnifiedMessageTag] = None,
                    metadata: Dict[str, Any] = None,
                    mode: str = "pyautogui",
                    use_paste: bool = True,
                    new_tab_method: str = "ctrl_t",
                    use_new_tab: bool = None) -> bool:
        """Send a single message to a specific agent."""
        success = self.bulk.send_message(content, sender, recipient, message_type, priority,
                                       tags, metadata, mode, use_paste, new_tab_method, use_new_tab)
        if success:
            self.messages.append(self._get_last_message())
        return success

    def send_to_all_agents(self, content: str, sender: str,
                          message_type: UnifiedMessageType = UnifiedMessageType.TEXT,
                          priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
                          tags: List[UnifiedMessageTag] = None,
                          metadata: Dict[str, Any] = None,
                          mode: str = "pyautogui",
                          use_paste: bool = True,
                          new_tab_method: str = "ctrl_t",
                          use_new_tab: bool = None) -> List[bool]:
        """Send message to all agents."""
        return self.bulk.send_to_all_agents(content, sender, message_type, priority,
                                          tags, metadata, mode, use_paste, new_tab_method, use_new_tab)

    # Utility methods
    def list_agents(self):
        """List all available agents."""
        self.utils.list_agents()

    def show_coordinates(self):
        """Show agent coordinates."""
        self.utils.show_coordinates()

    def show_message_history(self):
        """Show message history."""
        self.utils.show_message_history()

    def _get_last_message(self) -> UnifiedMessage:
        """Helper to get the most recently created message."""
        # This is a simplified helper - in practice, the message would be tracked
        return self.messages[-1] if self.messages else None
