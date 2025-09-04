"""
Messaging Coordination Handler

Handles agent coordination, status tracking, and inter-agent communication.
"""

from .unified_messaging_imports import logging
from typing import Any, Dict, List, Optional

from .models.messaging_models import (
    UnifiedMessage as Message,
    UnifiedMessageType as MessageType,
    UnifiedMessagePriority as MessagePriority,
    UnifiedMessageTag as MessageTag,
    SenderType,
    RecipientType
)

logger = logging.getLogger(__name__)

class MessagingCoordinationHandler:
    """
    Handles agent coordination and inter-agent communication.
    """

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

        # Coordination tracking
        self.active_coordinations = {}
        self.coordination_history = []

        # Agent status tracking
        self.agent_status = {}
        self.last_heartbeat = {}

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
            True if coordination successful, False otherwise
        """
        try:
            self.get_logger(__name__).info(f"🤝 Coordinating with {target_agent}: {coordination_type}")

            # Create coordination record
            coordination_id = self._generate_coordination_id(target_agent, coordination_type)

            coordination_record = {
                'id': coordination_id,
                'target_agent': target_agent,
                'type': coordination_type,
                'message': message,
                'context': context or {},
                'status': 'initiated',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }

            self.active_coordinations[coordination_id] = coordination_record

            # Send coordination message
            success = await self._send_coordination_message(
                target_agent, coordination_type, message, context
            )

            if success:
                coordination_record['status'] = 'sent'
                self.get_logger(__name__).info(f"✅ Coordination message sent to {target_agent}")
            else:
                coordination_record['status'] = 'failed'
                self.get_logger(__name__).error(f"❌ Coordination message failed to {target_agent}")

            coordination_record['updated_at'] = datetime.now().isoformat()
            self.coordination_history.append(coordination_record)

            return success

        except Exception as e:
            self.get_logger(__name__).error(f"❌ Error coordinating with {target_agent}: {e}")
            return False

    async def _send_coordination_message(
        self,
        target_agent: str,
        coordination_type: str,
        message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Send coordination message to target agent.

        Args:
            target_agent: Target agent
            coordination_type: Type of coordination
            message: Message content
            context: Additional context

        Returns:
            True if sent successfully, False otherwise
        """
        try:
            # Import here to avoid circular imports

            # Build coordination message
            builder = MessagingMessageBuilder(self.logger)

            # Add coordination metadata
            metadata = {
                'coordination_type': coordination_type,
                'coordination_context': context or {},
                'coordination_timestamp': datetime.now().isoformat()
            }

            # Create coordination message
            coord_message = builder.build_message(
                content=message,
                sender="MessagingCoordinator",
                recipient=target_agent,
                message_type=MessageType.COORDINATION,
                priority=MessagePriority.HIGH,
                tags=[MessageTag.COORDINATION],
                metadata=metadata,
                sender_type=SenderType.SYSTEM,
                recipient_type=RecipientType.AGENT
            )

            # Import delivery manager here to avoid circular imports

            delivery_manager = MessagingDeliveryManager(self.logger)
            success = await delivery_manager.deliver_message(coord_message)

            return success

        except Exception as e:
            self.get_logger(__name__).error(f"❌ Error sending coordination message: {e}")
            return False

    async def update_agent_status(self, agent_id: str, status: str,
                                details: Optional[Dict[str, Any]] = None) -> None:
        """
        Update status of an agent.

        Args:
            agent_id: Agent identifier
            status: New status
            details: Additional status details
        """
        try:
            self.agent_status[agent_id] = {
                'status': status,
                'details': details or {},
                'updated_at': datetime.now().isoformat()
            }

            self.last_heartbeat[agent_id] = datetime.now().isoformat()

            self.get_logger(__name__).info(f"📊 Agent {agent_id} status updated: {status}")

        except Exception as e:
            self.get_logger(__name__).error(f"❌ Error updating agent status: {e}")

    async def get_agent_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """
        Get status of an agent.

        Args:
            agent_id: Agent identifier

        Returns:
            Agent status information or None
        """
        try:
            status = self.agent_status.get(agent_id)
            if status:
                # Check if agent is still active (heartbeat within last 5 minutes)
                last_heartbeat = self.last_heartbeat.get(agent_id)
                if last_heartbeat:
                    last_heartbeat_time = datetime.fromisoformat(last_heartbeat)
                    time_diff = datetime.now() - last_heartbeat_time

                    if time_diff.total_seconds() > 300:  # 5 minutes
                        status['status'] = 'inactive'

            return status

        except Exception as e:
            self.get_logger(__name__).error(f"❌ Error getting agent status: {e}")
            return None

    async def broadcast_coordination(
        self,
        target_agents: List[str],
        coordination_type: str,
        message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, bool]:
        """
        Broadcast coordination message to multiple agents.

        Args:
            target_agents: List of target agents
            coordination_type: Type of coordination
            message: Coordination message
            context: Additional context

        Returns:
            Dictionary mapping agent IDs to success status
        """
        try:
            results = {}

            for agent_id in target_agents:
                success = await self.coordinate_with_agent(
                    agent_id, coordination_type, message, context
                )
                results[agent_id] = success

            successful_count = sum(1 for success in results.values() if success)
            self.get_logger(__name__).info(f"📢 Broadcast coordination: {successful_count}/{len(target_agents)} successful")

            return results

        except Exception as e:
            self.get_logger(__name__).error(f"❌ Error broadcasting coordination: {e}")
            return {}

    async def get_coordination_history(self, agent_id: Optional[str] = None,
                                     limit: int = 20) -> List[Dict[str, Any]]:
        """
        Get coordination history.

        Args:
            agent_id: Optional agent to filter by
            limit: Maximum number of records to return

        Returns:
            List of coordination records
        """
        try:
            if agent_id:
                history = [
                    record for record in self.coordination_history
                    if record['target_agent'] == agent_id
                ]
            else:
                history = self.coordination_history

            # Sort by creation time (newest first)
            history.sort(key=lambda x: x['created_at'], reverse=True)

            return history[:limit]

        except Exception as e:
            self.get_logger(__name__).error(f"❌ Error getting coordination history: {e}")
            return []

    async def acknowledge_coordination(self, coordination_id: str,
                                     agent_id: str, response: str) -> bool:
        """
        Acknowledge a coordination request.

        Args:
            coordination_id: Coordination identifier
            agent_id: Agent acknowledging
            response: Response message

        Returns:
            True if acknowledged successfully, False otherwise
        """
        try:
            if coordination_id not in self.active_coordinations:
                self.get_logger(__name__).warning(f"⚠️ Coordination {coordination_id} not found")
                return False

            coordination = self.active_coordinations[coordination_id]

            # Update coordination record
            coordination['acknowledged_by'] = agent_id
            coordination['acknowledged_at'] = datetime.now().isoformat()
            coordination['response'] = response
            coordination['status'] = 'acknowledged'
            coordination['updated_at'] = datetime.now().isoformat()

            self.get_logger(__name__).info(f"✅ Coordination {coordination_id} acknowledged by {agent_id}")
            return True

        except Exception as e:
            self.get_logger(__name__).error(f"❌ Error acknowledging coordination: {e}")
            return False

    def _generate_coordination_id(self, target_agent: str, coordination_type: str) -> str:
        """
        Generate unique coordination identifier.

        Args:
            target_agent: Target agent
            coordination_type: Type of coordination

        Returns:
            Unique coordination ID
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"coord_{target_agent}_{coordination_type}_{timestamp}"

    async def get_active_coordinations(self, agent_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get active coordinations.

        Args:
            agent_id: Optional agent to filter by

        Returns:
            List of active coordination records
        """
        try:
            if agent_id:
                active = [
                    coord for coord in self.active_coordinations.values()
                    if coord['target_agent'] == agent_id and coord['status'] == 'sent'
                ]
            else:
                active = [
                    coord for coord in self.active_coordinations.values()
                    if coord['status'] == 'sent'
                ]

            return active

        except Exception as e:
            self.get_logger(__name__).error(f"❌ Error getting active coordinations: {e}")
            return []

    async def cleanup_old_coordinations(self, max_age_hours: int = 24) -> int:
        """
        Clean up old coordination records.

        Args:
            max_age_hours: Maximum age in hours for coordination records

        Returns:
            Number of records cleaned up
        """
        try:
            cutoff_time = datetime.now().timestamp() - (max_age_hours * 3600)
            cleaned_count = 0

            # Clean active coordinations
            to_remove = []
            for coord_id, coordination in self.active_coordinations.items():
                created_time = datetime.fromisoformat(coordination['created_at']).timestamp()
                if created_time < cutoff_time:
                    to_remove.append(coord_id)

            for coord_id in to_remove:
                del self.active_coordinations[coord_id]
                cleaned_count += 1

            # Clean coordination history
            self.coordination_history = [
                record for record in self.coordination_history
                if datetime.fromisoformat(record['created_at']).timestamp() >= cutoff_time
            ]

            if cleaned_count > 0:
                self.get_logger(__name__).info(f"🧹 Cleaned up {cleaned_count} old coordination records")

            return cleaned_count

        except Exception as e:
            self.get_logger(__name__).error(f"❌ Error cleaning up coordinations: {e}")
            return 0

