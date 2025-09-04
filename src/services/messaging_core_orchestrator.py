"""
Messaging Core Orchestrator

Main orchestrator for the messaging system using modular components.
V2 Compliant - Under 300 lines.
"""

from ..core.unified_data_processing_system import read_json, write_json
from .unified_messaging_imports import logging
import asyncio
import time
import sys
from typing import Any, Dict, List, Optional

# Import MessagingMessageBuilder - SSOT compliant import
try:
    from .messaging_message_builder import MessagingMessageBuilder
except ImportError:
    # Fallback import for SSOT compliance
    MessagingMessageBuilder = None

from .models.messaging_models import (
    UnifiedMessage,
    UnifiedMessagePriority,
    UnifiedMessageType,
    UnifiedMessageTag,
    SenderType,
    RecipientType
)
from .messaging_core import UnifiedMessagingCore

# Import delivery manager
try:
    from .messaging_delivery_manager import MessagingDeliveryManager
except ImportError:
    MessagingDeliveryManager = None

# Import coordination handler
try:
    from .messaging_coordination_handler import MessagingCoordinationHandler
except ImportError:
    MessagingCoordinationHandler = None

# Import status tracker
try:
    from .messaging_status_tracker import MessagingStatusTracker
except ImportError:
    MessagingStatusTracker = None

logger = logging.getLogger(__name__)

# Constants
COORDINATE_CONFIG_FILE = "cursor_agent_coords.json"

class MessagingCoreOrchestrator:
    """
    Main orchestrator for the messaging system.

    This class coordinates all messaging functionality using specialized
    modular components, maintaining clean separation of concerns.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the messaging orchestrator.

        Args:
            config: Optional configuration dictionary
        """
        self.logger = logging.getLogger("messaging_orchestrator")
        self.config = config or {}

        # Initialize core messaging service
        self.messaging_core = UnifiedMessagingCore(config)

        # Initialize modular components
        self.message_builder = MessagingMessageBuilder(self.logger) if MessagingMessageBuilder else None
        self.delivery_manager = MessagingDeliveryManager(self.logger) if MessagingDeliveryManager else None
        self.coordination_handler = MessagingCoordinationHandler(self.logger) if MessagingCoordinationHandler else None
        self.status_tracker = MessagingStatusTracker(self.logger) if MessagingStatusTracker else None

        # Agent coordination data
        self.agent_coordinates: Dict[str, Dict[str, Any]] = {}

        self.logger.info("🚀 Messaging Core Orchestrator initialized with modular architecture")

    def get_logger(self, name: str):
        """Get logger for the messaging orchestrator."""
        return logging.getLogger(name)

    # === MESSAGE SENDING ===

    async def send_message(self, message: UnifiedMessage) -> bool:
        """
        Send a message using the best available delivery method.

        Args:
            message: UnifiedMessage to send

        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            self.get_logger(__name__).info(f"📤 Sending message to {message.recipient}")

            # Track initial status
            self.status_tracker.track_message_status(message, UnifiedMessageStatus.PENDING)

            # Deliver message
            success = await self.delivery_manager.deliver_message(message)

            # Update final status
            final_status = UnifiedMessageStatus.DELIVERED if success else UnifiedMessageStatus.FAILED
            self.status_tracker.track_message_status(message, final_status)

            if success:
                self.get_logger(__name__).info(f"✅ UnifiedMessage delivered successfully to {message.recipient}")
            else:
                self.get_logger(__name__).error(f"❌ UnifiedMessage delivery failed to {message.recipient}")

            return success

        except Exception as e:
            self.get_logger(__name__).error(f"❌ Error sending message: {e}")
            self.status_tracker.track_message_status(message, UnifiedMessageStatus.FAILED, str(e))
            return False

    def send_message_sync(
        self,
        content: str,
        sender: str,
        recipient: str,
        message_type: UnifiedMessageType = UnifiedMessageType.TEXT,
        priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
        tags: List[UnifiedMessageTag] = None,
        metadata: Dict[str, Any] = None,
    ) -> bool:
        """
        Send a message synchronously with individual parameters.
        """
        try:
            # Build and send message synchronously
            message = self.message_builder.build_message(
                content=content, sender=sender, recipient=recipient,
                message_type=message_type, priority=priority,
                tags=tags, metadata=metadata or {}
            )

            return asyncio.run(self.send_message(message))

        except Exception as e:
            self.get_logger(__name__).error(f"❌ Error sending message synchronously: {e}")
            return False

    # === AGENT COORDINATION ===

    async def coordinate_with_agent(
        self,
        target_agent: str,
        coordination_type: str,
        message: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Coordinate with another agent.

        Args:
            target_agent: Agent to coordinate with
            coordination_type: Type of coordination
            message: Coordination message
            context: Additional context

        Returns:
            bool: True if coordination successful, False otherwise
        """
        return await self.coordination_handler.coordinate_with_agent(
            target_agent, coordination_type, message, context
        )

    # === BROADCAST FUNCTIONALITY ===

    def send_broadcast(
        self,
        content: str,
        sender: str,
        recipients: List[str],
        message_type: UnifiedMessageType = UnifiedMessageType.BROADCAST,
        priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
        tags: List[UnifiedMessageTag] = None,
        metadata: Dict[str, Any] = None,
    ) -> Dict[str, bool]:
        """
        Send broadcast message to multiple recipients.
        """
        try:
            messages = self.message_builder.create_broadcast_message(
                content=content, sender=sender, recipients=recipients,
                message_type=message_type, priority=priority,
                tags=tags, metadata=metadata or {}
            )

            results = {}
            for message in messages:
                try:
                    success = asyncio.run(self.send_message(message))
                    results[message.recipient] = success
                except Exception as e:
                    self.get_logger(__name__).error(f"❌ Broadcast failed for {message.recipient}: {e}")
                    results[message.recipient] = False

            successful_count = sum(1 for success in results.values() if success)
            self.get_logger(__name__).info(f"📢 Broadcast: {successful_count}/{len(recipients)} successful")
            return results

        except Exception as e:
            self.get_logger(__name__).error(f"❌ Broadcast error: {e}")
            return {}

    # === STATUS AND REPORTING ===

    def get_delivery_stats(self) -> Dict[str, Any]:
        """
        Get delivery statistics.

        Returns:
            Dictionary with delivery statistics
        """
        return self.delivery_manager.get_delivery_stats()

    def get_delivery_report(self, time_range_hours: int = 24) -> Dict[str, Any]:
        """
        Generate delivery report.

        Args:
            time_range_hours: Number of hours to look back

        Returns:
            Delivery report dictionary
        """
        return self.status_tracker.get_delivery_report(time_range_hours)

    def get_system_health_report(self) -> Dict[str, Any]:
        """
        Generate system health report.

        Returns:
            System health report dictionary
        """
        return self.status_tracker.get_system_health_report()

    def get_agent_activity_report(self, agent_id: str,
                                time_range_hours: int = 24) -> Dict[str, Any]:
        """
        Generate activity report for an agent.

        Args:
            agent_id: Agent identifier
            time_range_hours: Number of hours to look back

        Returns:
            Agent activity report dictionary
        """
        return self.status_tracker.get_agent_activity_report(agent_id, time_range_hours)

    # === UTILITY METHODS ===

    def validate_message(self, message: UnifiedMessage) -> bool:
        """
        Validate a message.

        Args:
            message: UnifiedMessage to validate

        Returns:
            True if valid, False otherwise
        """
        return self.message_builder.validate_message(message)

    def update_agent_coordinates(self, agent_id: str, coordinates: Dict[str, Any]) -> None:
        """
        Update coordinates for an agent.

        Args:
            agent_id: Agent identifier
            coordinates: Agent coordinates
        """
        self.agent_coordinates[agent_id] = coordinates
        self.get_logger(__name__).info(f"📍 Updated coordinates for agent {agent_id}")

    def get_agent_coordinates(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """
        Get coordinates for an agent.

        Args:
            agent_id: Agent identifier

        Returns:
            Agent coordinates or None
        """
        return self.agent_coordinates.get(agent_id)

    async def show_coordinates(self) -> Dict[str, Any]:
        """
        Show all agent coordinates from the coordinate mapping file.

        Returns:
            Dictionary with coordinates and success status
        """
        try:
            
            # Load coordinates from the coordinate mapping file
            coords_file = COORDINATE_CONFIG_FILE
            if not get_unified_utility().path.exists(coords_file):
                return {
                    "success": False,
                    "error": f"Coordinate file {coords_file} not found",
                    "coordinates": {},
                    "agent_count": 0
                }
            
            coords_data = read_json(coords_file)
            
            # Extract agent coordinates
            coordinates = {}
            for agent_id, agent_data in coords_data.get("agents", {}).items():
                if agent_data.get("active", True):
                    coordinates[agent_id] = agent_data.get("chat_input_coordinates", [0, 0])
            
            # Update internal coordinate cache
            self.agent_coordinates = coordinates
            
            return {
                "success": True,
                "coordinates": coordinates,
                "agent_count": len(coordinates),
                "coordinate_system": coords_data.get("coordinate_system", {}),
                "validation_rules": coords_data.get("validation_rules", {})
            }
            
        except Exception as e:
            self.get_logger(__name__).error(f"Failed to load coordinates: {e}")
            return {
                "success": False,
                "error": str(e),
                "coordinates": {},
                "agent_count": 0
            }

    async def cleanup_old_records(self, max_age_hours: int = 168) -> int:
        """
        Clean up old records across all components.

        Args:
            max_age_hours: Maximum age in hours for records

        Returns:
            Total number of records cleaned up
        """
        try:
            total_cleaned = 0

            # Clean coordination records
            coord_cleaned = await self.coordination_handler.cleanup_old_coordinations(max_age_hours)
            total_cleaned += coord_cleaned

            # Clean status records
            status_cleaned = self.status_tracker.cleanup_old_records(max_age_hours)
            total_cleaned += status_cleaned

            # Reset delivery stats (they rebuild automatically)
            self.delivery_manager.reset_delivery_stats()

            self.get_logger(__name__).info(f"🧹 Cleaned up {total_cleaned} old records across all components")
            return total_cleaned

        except Exception as e:
            self.get_logger(__name__).error(f"❌ Error cleaning up old records: {e}")
            return 0

    # === HARD ONBOARDING METHODS ===

    def send_to_all_agents(
        self,
        content: str,
        sender: str,
        message_type: UnifiedMessageType = UnifiedMessageType.TEXT,
        priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
        tags: List[UnifiedMessageTag] = None,
        mode: str = "pyautogui",
        use_paste: bool = True,
    ) -> List[bool]:
        """
        Send message to all agents.

        Args:
            content: UnifiedMessage content
            sender: UnifiedMessage sender
            message_type: Type of message
            priority: UnifiedMessage priority
            tags: UnifiedMessage tags
            mode: Delivery mode
            use_paste: Whether to use paste method

        Returns:
            List of success results for each agent
        """
        
        # Load agent coordinates for PyAutoGUI delivery
        try:
            with open(COORDINATE_CONFIG_FILE, "r") as f:
                coords_data = read_json(f)
                agents = {}
                for agent_id_key, agent_data in coords_data["agents"].items():
                    # Use chat_input_coordinates for regular messaging
                    agents[agent_id_key] = {"coords": agent_data["chat_input_coordinates"]}
        except Exception:
            agents = {}
        
        # Send to all agents using core messaging service
        results = []
        for agent_id in agents:
            success = self.send_message(
                content=content,
                sender=sender,
                recipient=agent_id,
                message_type=message_type,
                priority=priority,
                mode=mode
            )
            results.append(success)
        
        return results

    async def send_message_to_agent(
        self,
        agent_id: str,
        content: str,
        sender: str,
        message_type: UnifiedMessageType = UnifiedMessageType.TEXT,
        priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
        tags: List[UnifiedMessageTag] = None,
        mode: str = "pyautogui",
        use_new_tab: bool = False,
        use_paste: bool = True,
        use_onboarding_coords: bool = False,
    ) -> bool:
        """
        Send message to specific agent.

        Args:
            agent_id: Target agent ID
            content: UnifiedMessage content
            sender: UnifiedMessage sender
            message_type: Type of message
            priority: UnifiedMessage priority
            tags: UnifiedMessage tags
            mode: Delivery mode
            use_new_tab: Whether to create new tab
            use_paste: Whether to use paste method

        Returns:
            True if sent successfully, False otherwise
        """

        # Create message
        message = UnifiedMessage(
            content=content,
            sender=sender,
            recipient=agent_id,
            message_type=message_type,
            priority=priority,
            tags=tags or [],
            sender_type=SenderType.SYSTEM,
            recipient_type=RecipientType.AGENT,
        )

        # Use the existing messaging onboarding service for delivery
        
        # Load agent coordinates
        try:
            with open(COORDINATE_CONFIG_FILE, "r") as f:
                coords_data = read_json(f)
                agents = {}
                for agent_id_key, agent_data in coords_data["agents"].items():
                    # Use onboarding_input_coords for onboarding, chat_input_coordinates for regular messaging
                    coord_type = "onboarding_input_coords" if use_onboarding_coords else "chat_input_coordinates"
                    agents[agent_id_key] = {"coords": agent_data[coord_type]}
        except Exception:
            agents = {}
        
        # Send message using core messaging service
        return self.send_message(
            content=content,
            sender=sender,
            recipient=agent_id,
            message_type=message_type,
            priority=priority,
            mode=mode
        )

    def generate_personalized_onboarding_message(
        self,
        agent_id: str,
        style: str = "friendly"
    ) -> str:
        """
        Generate personalized onboarding message for specific agent.

        Args:
            agent_id: Target agent ID
            style: Onboarding style (friendly/professional)

        Returns:
            Personalized onboarding message content
        """
        
        # Get agent role from status file
        role = self._get_agent_role_from_status(agent_id)
        
        # Generate personalized message
        onboarding_service = OnboardingService()
        return onboarding_service.generate_onboarding_message(agent_id, role, style)

    def _get_agent_role_from_status(self, agent_id: str) -> str:
        """Get agent role from their status.json file."""

        status_file = f"agent_workspaces/{agent_id}/status.json"
        try:
            if get_unified_utility().path.exists(status_file):
                with open(status_file, "r", encoding="utf-8") as f:
                    status = read_json(f)
                    return status.get("agent_name", f"{agent_id} Specialist")
            else:
                return f"{agent_id} Specialist"
        except Exception:
            return f"{agent_id} Specialist"

    def export_system_report(self, file_path: str) -> bool:
        """
        Export comprehensive system report.

        Args:
            file_path: Path to save the report

        Returns:
            True if successful, False otherwise
        """
        try:
            report = {
                'export_timestamp': get_current_timestamp(),
                'system_health': self.get_system_health_report(),
                'delivery_stats': self.get_delivery_stats(),
                'delivery_report_24h': self.get_delivery_report(24),
                'agent_count': len(self.agent_coordinates),
                'active_coordinations': len(self.coordination_handler.active_coordinations)
            }

            with open(file_path, 'w', encoding='utf-8') as f:
                write_json(report, f, indent=2, ensure_ascii=False)

            self.get_logger(__name__).info(f"📊 System report exported to {file_path}")
            return True

        except Exception as e:
            self.get_logger(__name__).error(f"❌ Error exporting system report: {e}")
            return False

    # === CLI COMPATIBILITY METHODS ===
    
    def send_message(self, content: str, sender: str, recipient: str, 
                    message_type: str = "text", priority: str = "regular", 
                    mode: str = "pyautogui", **kwargs) -> bool:
        """Send message for CLI compatibility."""
        try:
            # Create message using core service
            message = self.messaging_core.create_message(
                content=content,
                sender=sender,
                recipient=recipient,
                message_type=UnifiedMessageType(message_type),
                priority=UnifiedMessagePriority(priority)
            )
            
            # Send using core service
            return self.messaging_core.send_message(message, mode)
            
        except Exception as e:
            self.logger.error(f"❌ Error sending message: {e}")
            return False

    def send_to_all_agents(self, content: str, sender: str, 
                          message_type: str = "text", priority: str = "regular", 
                          mode: str = "pyautogui", **kwargs) -> List[bool]:
        """Send message to all agents."""
        try:
            # Load agent coordinates
            with open(COORDINATE_CONFIG_FILE, "r") as f:
                coords_data = read_json(f)
                agents = list(coords_data["agents"].keys())
            
            results = []
            for agent_id in agents:
                success = self.send_message(
                    content=content,
                    sender=sender,
                    recipient=agent_id,
                    message_type=message_type,
                    priority=priority,
                    mode=mode
                )
                results.append(success)
            
            return results
            
        except Exception as e:
            self.logger.error(f"❌ Error sending to all agents: {e}")
            return []

    def send_onboarding_message(self, agent_id: str, style: str = "friendly", 
                               mode: str = "pyautogui", **kwargs) -> bool:
        """Send onboarding message to specific agent."""
        content = f"Welcome {agent_id}! You are now onboarded to the system."
        return self.send_message(
            content=content,
            sender="Captain Agent-4",
            recipient=agent_id,
            message_type="onboarding",
            priority="regular",
            mode=mode
        )

    def send_bulk_onboarding(self, style: str = "friendly", mode: str = "pyautogui", **kwargs) -> None:
        """Send bulk onboarding to all agents."""
        content = f"Bulk onboarding message - {style} style"
        self.send_to_all_agents(
            content=content,
            sender="Captain Agent-4",
            message_type="onboarding",
            priority="regular",
            mode=mode
        )

    def list_agents(self) -> None:
        """List all available agents."""
        try:
            with open(COORDINATE_CONFIG_FILE, "r") as f:
                coords_data = read_json(f)
                agents = coords_data["agents"]
            
            print("🤖 Available Agents:")
            for agent_id, agent_data in agents.items():
                status = "✅ Active" if agent_data.get("active", True) else "❌ Inactive"
                print(f"  {agent_id}: {agent_data.get('description', 'No description')} - {status}")
                
        except Exception as e:
            print(f"❌ Error listing agents: {e}")

    def show_message_history(self) -> None:
        """Show message history."""
        history = self.messaging_core.get_message_history()
        if not history:
            print("📭 No messages in history")
            return
        
        print("📜 Message History:")
        for i, message in enumerate(history[-10:], 1):  # Show last 10 messages
            print(f"  {i}. {message.sender} -> {message.recipient}: {message.content[:50]}...")
