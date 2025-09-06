#!/usr/bin/env python3
"""
Messaging Agent Coordination Module - V2 Compliant
=================================================

Modular component for cross-agent coordination and swarm communication.
Handles agent-to-agent messaging and coordination protocols.

Author: Agent-7 - Web Development Specialist
License: MIT
"""


# Import unified logger with fallback
try:

    unified_logger = get_logger("messaging_coordination")
except ImportError:
    unified_logger = None


class MessagingAgentCoordination:
    """Handles cross-agent coordination and swarm communication."""

    def __init__(self, logger=None, unified_logger=None):
        """Initialize agent coordination handler."""
        self.logger = logger
        self.unified_logger = unified_logger
        self.delivery_orchestrator = MessagingDeliveryOrchestrator(logger)

    async def coordinate_with_agent(
        self,
        target_agent: str,
        coordination_type: str,
        message: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Enhanced cross-agent coordination with optional unified logging.

        Args:
            target_agent: The agent to coordinate with
            coordination_type: Type of coordination (task_handover, status_sync, etc.)
            message: Coordination message
            context: Additional context for coordination

        Returns:
            bool: True if coordination successful, False otherwise
        """
        operation_id = f"cross_agent_coordination_{target_agent}"

        try:
            # Log coordination attempt (if unified logging available)
            if self.unified_logger:
                self.unified_logger.start_operation(
                    operation_id,
                    "Agent-6",
                    operation_type="agent_coordination",
                    metadata={
                        "target_agent": target_agent,
                        "coordination_type": coordination_type,
                        "swarm_coordination": True,
                        "pattern_elimination": "unified_coordination_applied",
                        "context": context or {},
                    },
                )

            if self.logger:
                self.get_logger(__name__).info(
                    f"🤝 Coordinating with {target_agent} for {coordination_type}"
                )

            # Create coordination message
            coord_message = Message(
                id=f"coord_{coordination_type}_{target_agent}_{asyncio.get_event_loop().time()}",
                timestamp=str(asyncio.get_event_loop().time()),
                sender="Agent-6",  # Coordination agent
                recipient=target_agent,
                type=MessageType.agent_to_agent,
                priority=(
                    "urgent" if "urgent" in coordination_type.lower() else "normal"
                ),
                content=message,
                tags=["coordination", coordination_type, "swarm"],
                metadata={
                    "coordination_type": coordination_type,
                    "coordination_context": context or {},
                    "swarm_coordination": True,
                    "coordination_initiator": "Agent-6",
                },
            )

            # Send coordination message
            success = await self.delivery_orchestrator.deliver_message(coord_message)

            # Log coordination result (if unified logging available)
            if self.unified_logger:
                if success:
                    self.unified_logger.log_agent_coordination(
                        operation_id,
                        target_agent,
                        message=f"Cross-agent coordination successful with {target_agent}",
                        metadata={
                            "coordination_type": coordination_type,
                            "coordination_success": True,
                            "swarm_coordination": True,
                            "message_delivered": True,
                        },
                        parent_operation="cross_agent_coordination",
                    )
                else:
                    self.unified_logger.log_agent_coordination(
                        operation_id,
                        target_agent,
                        message=f"Cross-agent coordination failed with {target_agent}",
                        metadata={
                            "coordination_type": coordination_type,
                            "coordination_success": False,
                            "swarm_coordination": True,
                            "message_delivered": False,
                        },
                        parent_operation="cross_agent_coordination",
                    )

                self.unified_logger.end_operation(
                    "cross_agent_coordination", "Agent-6", success=success
                )

            if self.logger:
                if success:
                    self.get_logger(__name__).info(
                        f"✅ Coordination successful with {target_agent}"
                    )
                else:
                    self.get_logger(__name__).error(
                        f"❌ Coordination failed with {target_agent}"
                    )

            return success

        except Exception as e:
            # Log coordination exception
            if self.unified_logger:
                self.unified_logger.log_agent_coordination(
                    operation_id,
                    target_agent,
                    message=f"Cross-agent coordination exception with {target_agent}: {str(e)}",
                    metadata={
                        "coordination_type": coordination_type,
                        "exception": str(e),
                        "coordination_success": False,
                    },
                    parent_operation="cross_agent_coordination",
                )
                self.unified_logger.end_operation(
                    "cross_agent_coordination", "Agent-6", success=False
                )

            if self.logger:
                self.get_logger(__name__).error(
                    f"❌ Cross-agent coordination exception with {target_agent}: {e}"
                )

            return False

    async def report_status_to_captain(
        self, status_message: str, context: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Report status update to Captain Agent-4 with enhanced coordination tracking.

        Args:
            status_message: Status message to report
            context: Additional context for the status report

        Returns:
            bool: True if status report successful, False otherwise
        """
        return await self.coordinate_with_agent(
            target_agent="Agent-4",
            coordination_type="status_report",
            message=status_message,
            context={
                "captain_coordination": True,
                "status_report": True,
                "report_context": context or {},
            },
        )

    async def broadcast_to_swarm(
        self, message: str, exclude_agents: Optional[list] = None
    ) -> Dict[str, bool]:
        """Broadcast message to all swarm agents.

        Args:
            message: Message to broadcast
            exclude_agents: List of agents to exclude from broadcast

        Returns:
            Dict mapping agent names to delivery success status
        """
        agents = [
            "Agent-1",
            "Agent-2",
            "Agent-3",
            "Agent-4",
            "Agent-5",
            "Agent-6",
            "Agent-7",
            "Agent-8",
        ]
        exclude_agents = exclude_agents or []

        results = {}
        for agent in agents:
            if agent not in exclude_agents:
                success = await self.coordinate_with_agent(
                    target_agent=agent,
                    coordination_type="swarm_broadcast",
                    message=message,
                    context={"broadcast": True, "swarm_wide": True},
                )
                results[agent] = success

        return results
