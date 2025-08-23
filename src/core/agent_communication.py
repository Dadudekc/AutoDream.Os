#!/usr/bin/env python3
"""
🔍 Agent Communication Protocol - Agent_Cellphone_V2

Cross-agent communication, message routing, and agent discovery system.
Following V2 coding standards: ≤300 LOC, OOP design, SRP.

Author: Communication & Coordination Specialist
License: MIT
"""

import logging
import threading
import time
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Callable, Set
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
import socket
import pickle

# Import V2 comprehensive messaging system
from .v2_comprehensive_messaging_system import (
    V2MessageType,
    V2MessagePriority,
    V2AgentStatus,
)

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class AgentInfo:
    """Agent registration information"""

    agent_id: str
    name: str
    capabilities: List[str]
    status: V2AgentStatus
    last_seen: datetime
    endpoint: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Message:
    """Inter-agent message structure"""

    message_id: str
    sender_id: str
    recipient_id: str
    message_type: V2MessageType
    priority: V2MessagePriority
    payload: Dict[str, Any]
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)


class AgentCommunicationProtocol:
    """
    Agent Communication Protocol - Single responsibility: Cross-agent communication and coordination.

    Follows V2 standards: ≤300 LOC, OOP design, SRP.
    """

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the agent communication protocol"""
        self.config = config or {}

        # Agent registry
        self.registered_agents: Dict[str, AgentInfo] = {}
        self.agent_capabilities: Dict[str, Set[str]] = defaultdict(set)

        # Message routing
        self.message_queue: deque = deque()
        self.message_history: List[Message] = []
        self.routing_table: Dict[str, str] = {}

        # Communication state
        self.communication_active = False
        self.communication_thread: Optional[threading.Thread] = None
        self.lock = threading.RLock()

        # Configuration
        self.heartbeat_interval = self.config.get("heartbeat_interval", 30)  # seconds
        self.message_timeout = self.config.get("message_timeout", 300)  # seconds
        self.max_message_history = self.config.get("max_message_history", 10000)

        # Callbacks
        self.message_callbacks: List[Callable] = []
        self.agent_status_callbacks: List[Callable] = []

        # Performance tracking integration
        self.performance_tracker = None

        logger.info("AgentCommunicationProtocol initialized")

    def register_agent(
        self,
        agent_id: str,
        name: str,
        capabilities: List[str],
        endpoint: str,
        metadata: Dict[str, Any] = None,
    ) -> bool:
        """Register a new agent"""
        with self.lock:
            if agent_id in self.registered_agents:
                logger.warning(f"Agent {agent_id} already registered, updating...")

            agent_info = AgentInfo(
                agent_id=agent_id,
                name=name,
                capabilities=capabilities,
                status=V2AgentStatus.ONLINE,
                last_seen=datetime.now(),
                endpoint=endpoint,
                metadata=metadata or {},
            )

            self.registered_agents[agent_id] = agent_info

            # Update capability index
            for capability in capabilities:
                self.agent_capabilities[capability].add(agent_id)

            # Update routing table
            self.routing_table[agent_id] = endpoint

            logger.info(
                f"Agent {agent_id} ({name}) registered with capabilities: {capabilities}"
            )
            return True

    def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent"""
        with self.lock:
            if agent_id not in self.registered_agents:
                logger.warning(f"Agent {agent_id} not found for unregistration")
                return False

            agent_info = self.registered_agents.pop(agent_id)

            # Remove from capability index
            for capability in agent_info.capabilities:
                if agent_id in self.agent_capabilities[capability]:
                    self.agent_capabilities[capability].remove(agent_id)
                    if not self.agent_capabilities[capability]:
                        del self.agent_capabilities[capability]

            # Remove from routing table
            if agent_id in self.routing_table:
                del self.routing_table[agent_id]

            logger.info(f"Agent {agent_id} unregistered")
            return True

    def update_agent_status(
        self, agent_id: str, status: V2AgentStatus, metadata: Dict[str, Any] = None
    ) -> bool:
        """Update agent status"""
        with self.lock:
            if agent_id not in self.registered_agents:
                logger.warning(f"Agent {agent_id} not found for status update")
                return False

            agent_info = self.registered_agents[agent_id]
            agent_info.status = status
            agent_info.last_seen = datetime.now()

            if metadata:
                agent_info.metadata.update(metadata)

            # Notify status callbacks
            self._notify_agent_status_callbacks(agent_id, status)

            logger.debug(f"Agent {agent_id} status updated to: {status.value}")
            return True

    def send_message(
        self,
        sender_id: str,
        recipient_id: str,
        message_type: V2MessageType,
        payload: Dict[str, Any],
        priority: V2MessagePriority = V2MessagePriority.NORMAL,
        metadata: Dict[str, Any] = None,
    ) -> str:
        """Send a message to another agent"""
        message = Message(
            message_id=str(uuid.uuid4()),
            sender_id=sender_id,
            recipient_id=recipient_id,
            message_type=message_type,
            priority=priority,
            payload=payload,
            timestamp=datetime.now(),
            metadata=metadata or {},
        )

        with self.lock:
            # Add to message queue
            self.message_queue.append(message)

            # Add to message history
            self.message_history.append(message)

            # Maintain history limits
            if len(self.message_history) > self.max_message_history:
                self.message_history = self.message_history[-self.max_message_history :]

        # Track message performance if tracker available
        if self.performance_tracker:
            self.performance_tracker.record_metric(
                "message_sent",
                1,
                "count",
                sender_id,
                {"message_type": message_type.value, "priority": priority.value},
            )

        logger.debug(
            f"Message queued: {message.message_id} from {sender_id} to {recipient_id}"
        )
        return message.message_id

    def broadcast_message(
        self,
        sender_id: str,
        message_type: V2MessageType,
        payload: Dict[str, Any],
        priority: V2MessagePriority = V2MessagePriority.NORMAL,
        metadata: Dict[str, Any] = None,
    ) -> List[str]:
        """Broadcast a message to all registered agents"""
        message_ids = []

        with self.lock:
            for agent_id in self.registered_agents:
                if agent_id != sender_id:
                    message_id = self.send_message(
                        sender_id, agent_id, message_type, payload, priority, metadata
                    )
                    message_ids.append(message_id)

        logger.info(f"Broadcast message sent to {len(message_ids)} agents")
        return message_ids

    def find_agents_by_capability(self, capability: str) -> List[AgentInfo]:
        """Find agents with a specific capability"""
        with self.lock:
            agent_ids = self.agent_capabilities.get(capability, set())
            return [
                self.registered_agents[aid]
                for aid in agent_ids
                if aid in self.registered_agents
            ]

    def get_agent_info(self, agent_id: str) -> Optional[AgentInfo]:
        """Get information about a specific agent"""
        with self.lock:
            return self.registered_agents.get(agent_id)

    def get_all_agents(self) -> List[AgentInfo]:
        """Get all registered agents"""
        with self.lock:
            return list(self.registered_agents.values())

    def get_agent_status(self, agent_id: str) -> Optional[V2AgentStatus]:
        """Get current status of an agent"""
        agent_info = self.get_agent_info(agent_id)
        return agent_info.status if agent_info else None

    def start_communication(self):
        """Start the communication protocol"""
        if self.communication_active:
            logger.warning("Communication protocol already active")
            return

        self.communication_active = True
        self.communication_thread = threading.Thread(
            target=self._communication_loop, daemon=True
        )
        self.communication_thread.start()
        logger.info("Agent communication protocol started")

    def stop_communication(self):
        """Stop the communication protocol"""
        self.communication_active = False
        if self.communication_thread:
            self.communication_thread.join(timeout=5)
        logger.info("Agent communication protocol stopped")

    def add_message_callback(self, callback: Callable):
        """Add callback for message processing"""
        if callback not in self.message_callbacks:
            self.message_callbacks.append(callback)

    def add_agent_status_callback(self, callback: Callable):
        """Add callback for agent status changes"""
        if callback not in self.agent_status_callbacks:
            self.agent_status_callbacks.append(callback)

    def set_performance_tracker(self, performance_tracker):
        """Set performance tracker for metrics collection"""
        self.performance_tracker = performance_tracker
        logger.info("Performance tracker integrated with communication protocol")

    def _communication_loop(self):
        """Main communication loop"""
        while self.communication_active:
            try:
                # Process message queue
                self._process_message_queue()

                # Send heartbeats
                self._send_heartbeats()

                # Cleanup old messages
                self._cleanup_old_messages()

                # Check agent health
                self._check_agent_health()

                time.sleep(1)  # Process every second

            except Exception as e:
                logger.error(f"Error in communication loop: {e}")
                time.sleep(10)

    def _process_message_queue(self):
        """Process messages in the queue"""
        with self.lock:
            while self.message_queue:
                message = self.message_queue.popleft()

                # Check if recipient is available
                recipient_info = self.registered_agents.get(message.recipient_id)
                if not recipient_info or recipient_info.status == V2AgentStatus.OFFLINE:
                    logger.warning(
                        f"Recipient {message.recipient_id} not available for message {message.message_id}"
                    )
                    continue

                # Process message based on type
                self._route_message(message)

                # Notify message callbacks
                self._notify_message_callbacks(message)

    def _route_message(self, message: Message):
        """Route a message to its destination"""
        try:
            # This would implement actual message routing logic
            # For now, we'll just log the routing
            logger.debug(
                f"Routing message {message.message_id} to {message.recipient_id}"
            )

            # Track message routing performance
            if self.performance_tracker:
                self.performance_tracker.record_metric(
                    "message_routed",
                    1,
                    "count",
                    message.sender_id,
                    {
                        "message_type": message.message_type.value,
                        "recipient": message.recipient_id,
                    },
                )

        except Exception as e:
            logger.error(f"Error routing message {message.message_id}: {e}")

    def _send_heartbeats(self):
        """Send heartbeat messages to all agents"""
        current_time = datetime.now()

        with self.lock:
            for agent_id, agent_info in self.registered_agents.items():
                if agent_info.status != V2AgentStatus.OFFLINE:
                    # Check if heartbeat is needed
                    time_since_last = current_time - agent_info.last_seen
                    if time_since_last.total_seconds() > self.heartbeat_interval:
                        # Send heartbeat
                        self.send_message(
                            "system",
                            agent_id,
                            V2MessageType.HEALTH_CHECK,
                            {"heartbeat": True, "timestamp": current_time.isoformat()},
                            V2MessagePriority.LOW,
                        )

    def _check_agent_health(self):
        """Check health of registered agents"""
        current_time = datetime.now()

        with self.lock:
            for agent_id, agent_info in list(self.registered_agents.items()):
                time_since_last = current_time - agent_info.last_seen

                # Mark agent as offline if no response for too long
                if time_since_last.total_seconds() > self.message_timeout:
                    if agent_info.status != V2AgentStatus.OFFLINE:
                        agent_info.status = V2AgentStatus.OFFLINE
                        self._notify_agent_status_callbacks(
                            agent_id, V2AgentStatus.OFFLINE
                        )
                        logger.warning(
                            f"Agent {agent_id} marked as offline due to timeout"
                        )

    def _cleanup_old_messages(self):
        """Clean up old messages from history"""
        current_time = datetime.now()
        cutoff_time = current_time - timedelta(seconds=self.message_timeout)

        with self.lock:
            self.message_history = [
                msg for msg in self.message_history if msg.timestamp >= cutoff_time
            ]

    def _notify_message_callbacks(self, message: Message):
        """Notify message processing callbacks"""
        for callback in self.message_callbacks:
            try:
                callback(message)
            except Exception as e:
                logger.error(f"Error in message callback: {e}")

    def _notify_agent_status_callbacks(self, agent_id: str, status: V2AgentStatus):
        """Notify agent status change callbacks"""
        for callback in self.agent_status_callbacks:
            try:
                callback(agent_id, status)
            except Exception as e:
                logger.error(f"Error in agent status callback: {e}")

    def export_communication_data(self, filepath: str):
        """Export communication data to JSON file"""
        with self.lock:
            export_data = {
                "export_timestamp": datetime.now().isoformat(),
                "registered_agents": {},
                "message_history": [],
                "routing_table": self.routing_table,
            }

            # Export agent information
            for agent_id, agent_info in self.registered_agents.items():
                export_data["registered_agents"][agent_id] = {
                    "name": agent_info.name,
                    "capabilities": agent_info.capabilities,
                    "status": agent_info.status.value,
                    "last_seen": agent_info.last_seen.isoformat(),
                    "endpoint": agent_info.endpoint,
                    "metadata": agent_info.metadata,
                }

            # Export recent messages
            for message in self.message_history[-1000:]:  # Last 1000 messages
                export_data["message_history"].append(
                    {
                        "message_id": message.message_id,
                        "sender_id": message.sender_id,
                        "recipient_id": message.recipient_id,
                        "message_type": message.message_type.value,
                        "priority": message.priority.value,
                        "payload": message.payload,
                        "timestamp": message.timestamp.isoformat(),
                        "metadata": message.metadata,
                    }
                )

            with open(filepath, "w") as f:
                json.dump(export_data, f, indent=2, default=str)

            logger.info(f"Exported communication data to {filepath}")

    def cleanup(self):
        """Cleanup communication protocol resources"""
        self.stop_communication()
        logger.info("AgentCommunicationProtocol cleaned up")
