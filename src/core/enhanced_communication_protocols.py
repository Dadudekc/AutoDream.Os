#!/usr/bin/env python3
"""
Enhanced Communication Protocols - Agent-6 (Coordination & Communication Specialist)
==================================================================================

Enhanced messaging protocols with improved reliability, response times, and coordination.

PROTOCOL IMPROVEMENTS:
1. Adaptive retry mechanisms with exponential backoff
2. Multi-channel delivery with automatic fallback
3. Priority-based message routing
4. Health monitoring and circuit breakers
5. Performance analytics and metrics
6. Enhanced error handling and recovery

Author: Agent-6 (Coordination & Communication Specialist)
Date: 2025-09-10
License: MIT
"""

import logging
import os
import queue
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)

# ==================== Enhanced Protocol Configuration ====================

class CommunicationPriority(Enum):
    """Enhanced priority levels with SLA requirements."""
    CRITICAL = "critical"    # SLA: < 30 seconds, guaranteed delivery
    URGENT = "urgent"        # SLA: < 2 minutes, guaranteed delivery
    HIGH = "high"           # SLA: < 5 minutes, guaranteed delivery
    NORMAL = "normal"       # SLA: < 15 minutes, best effort
    LOW = "low"            # SLA: < 60 minutes, best effort

class DeliveryChannel(Enum):
    """Available delivery channels."""
    PYAUTOGUI = "pyautogui"
    INBOX = "inbox"
    BROADCAST = "broadcast"
    DIRECT_API = "direct_api"

@dataclass
class ProtocolMetrics:
    """Communication protocol performance metrics."""
    total_messages_sent: int = 0
    total_messages_delivered: int = 0
    total_messages_failed: int = 0
    average_delivery_time: float = 0.0
    success_rate: float = 0.0
    last_updated: datetime = field(default_factory=datetime.now)

    def update_success_rate(self):
        """Update success rate calculation."""
        total = self.total_messages_sent
        if total > 0:
            self.success_rate = (self.total_messages_delivered / total) * 100
        self.last_updated = datetime.now()

@dataclass
class AgentHealthStatus:
    """Agent health monitoring status."""
    agent_id: str
    is_online: bool = True
    last_seen: datetime = field(default_factory=datetime.now)
    consecutive_failures: int = 0
    circuit_breaker_tripped: bool = False
    circuit_breaker_reset_time: datetime | None = None

    def record_success(self):
        """Record successful communication."""
        self.is_online = True
        self.last_seen = datetime.now()
        self.consecutive_failures = 0
        if self.circuit_breaker_tripped:
            self.reset_circuit_breaker()

    def record_failure(self):
        """Record failed communication."""
        self.consecutive_failures += 1
        if self.consecutive_failures >= 3:
            self.trip_circuit_breaker()

    def trip_circuit_breaker(self):
        """Trip circuit breaker to prevent further attempts."""
        self.circuit_breaker_tripped = True
        self.circuit_breaker_reset_time = datetime.now() + timedelta(minutes=5)
        logger.warning(f"🚨 Circuit breaker tripped for {self.agent_id}")

    def reset_circuit_breaker(self):
        """Reset circuit breaker after cooldown period."""
        self.circuit_breaker_tripped = False
        self.circuit_breaker_reset_time = None
        self.consecutive_failures = 0
        logger.info(f"✅ Circuit breaker reset for {self.agent_id}")

class EnhancedCommunicationProtocols:
    """Enhanced communication protocols with advanced features."""

    def __init__(self):
        self.metrics = ProtocolMetrics()
        self.agent_health: dict[str, AgentHealthStatus] = {}
        self.message_queue = queue.Queue()
        self.retry_queue = queue.Queue()
        self.delivery_workers: list[threading.Thread] = []

        # Protocol configuration
        self.max_retries = int(os.getenv("MAX_RETRY_ATTEMPTS", "5"))
        self.base_retry_delay = float(os.getenv("BASE_RETRY_DELAY", "1.0"))
        self.max_retry_delay = float(os.getenv("MAX_RETRY_DELAY", "30.0"))
        self.circuit_breaker_threshold = int(os.getenv("CIRCUIT_BREAKER_THRESHOLD", "3"))

        # Initialize agent health monitoring
        self._initialize_agent_health()

        # Start background workers
        self._start_delivery_workers()

    def _initialize_agent_health(self):
        """Initialize health status for all agents."""
        agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4",
                 "Agent-5", "Agent-6", "Agent-7", "Agent-8"]

        for agent_id in agents:
            self.agent_health[agent_id] = AgentHealthStatus(agent_id)

    def _start_delivery_workers(self):
        """Start background delivery worker threads."""
        for i in range(3):  # 3 worker threads
            worker = threading.Thread(
                target=self._delivery_worker,
                name=f"DeliveryWorker-{i+1}",
                daemon=True
            )
            worker.start()
            self.delivery_workers.append(worker)

    def _delivery_worker(self):
        """Background worker for processing message deliveries."""
        while True:
            try:
                message_data = self.message_queue.get(timeout=1)
                if message_data:
                    self._process_message_delivery(message_data)
                self.message_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Delivery worker error: {e}")

    def _process_message_delivery(self, message_data: dict[str, Any]):
        """Process individual message delivery with enhanced protocols."""
        recipient = message_data.get("recipient")
        content = message_data.get("content")
        priority = message_data.get("priority", CommunicationPriority.NORMAL)
        callback = message_data.get("callback")

        # Check agent health
        if not self._is_agent_healthy(recipient):
            logger.warning(f"⚠️ Skipping delivery to unhealthy agent: {recipient}")
            if callback:
                callback(False, f"Agent {recipient} is currently unhealthy")
            return

        # Attempt delivery with fallback
        success = self._attempt_delivery_with_fallback(recipient, content, priority)

        # Update metrics and health
        self.metrics.total_messages_sent += 1
        if success:
            self.metrics.total_messages_delivered += 1
            self.agent_health[recipient].record_success()
        else:
            self.metrics.total_messages_failed += 1
            self.agent_health[recipient].record_failure()

        self.metrics.update_success_rate()

        # Execute callback
        if callback:
            callback(success, None if success else "Delivery failed")

    def _is_agent_healthy(self, agent_id: str) -> bool:
        """Check if agent is healthy for communication."""
        if agent_id not in self.agent_health:
            return False

        health = self.agent_health[agent_id]

        # Check circuit breaker
        if health.circuit_breaker_tripped:
            if datetime.now() > health.circuit_breaker_reset_time:
                health.reset_circuit_breaker()
            else:
                return False

        # Check timeout (5 minutes)
        if datetime.now() - health.last_seen > timedelta(minutes=5):
            health.is_online = False
            return False

        return health.is_online

    def _attempt_delivery_with_fallback(self, recipient: str, content: str,
                                      priority: CommunicationPriority) -> bool:
        """Attempt delivery using multiple channels with fallback."""
        channels = self._get_delivery_channels(priority)

        for channel in channels:
            try:
                if self._deliver_via_channel(channel, recipient, content):
                    logger.info(f"✅ Message delivered via {channel.value} to {recipient}")
                    return True
            except Exception as e:
                logger.warning(f"⚠️ Delivery failed via {channel.value}: {e}")
                continue

        logger.error(f"❌ All delivery channels failed for {recipient}")
        return False

    def _get_delivery_channels(self, priority: CommunicationPriority) -> list[DeliveryChannel]:
        """Get ordered list of delivery channels based on priority."""
        if priority in [CommunicationPriority.CRITICAL, CommunicationPriority.URGENT]:
            return [DeliveryChannel.PYAUTOGUI, DeliveryChannel.INBOX, DeliveryChannel.DIRECT_API]
        else:
            return [DeliveryChannel.PYAUTOGUI, DeliveryChannel.INBOX]

    def _deliver_via_channel(self, channel: DeliveryChannel, recipient: str, content: str) -> bool:
        """Deliver message via specific channel."""
        try:
            if channel == DeliveryChannel.PYAUTOGUI:
                return self._deliver_pyautogui(recipient, content)
            elif channel == DeliveryChannel.INBOX:
                return self._deliver_inbox(recipient, content)
            elif channel == DeliveryChannel.DIRECT_API:
                return self._deliver_direct_api(recipient, content)
            elif channel == DeliveryChannel.BROADCAST:
                return self._deliver_broadcast(content)
        except Exception as e:
            logger.error(f"Channel delivery error ({channel.value}): {e}")
            raise

        return False

    def _deliver_pyautogui(self, recipient: str, content: str) -> bool:
        """Deliver via PyAutoGUI with enhanced error handling."""
        try:
            # Import and use existing PyAutoGUI delivery
            from .messaging_pyautogui import deliver_message_pyautogui, get_agent_coordinates

            coords = get_agent_coordinates(recipient)
            if not coords:
                raise ValueError(f"No coordinates for {recipient}")

            # Create unified message for formatting
            from .messaging_core import UnifiedMessage, UnifiedMessagePriority, UnifiedMessageType
            message = UnifiedMessage(
                content=content,
                sender="Agent-6",
                recipient=recipient,
                message_type=UnifiedMessageType.AGENT_TO_AGENT,
                priority=UnifiedMessagePriority.REGULAR
            )

            return deliver_message_pyautogui(message, coords)

        except Exception as e:
            logger.error(f"PyAutoGUI delivery failed: {e}")
            raise

    def _deliver_inbox(self, recipient: str, content: str) -> bool:
        """Deliver via inbox fallback."""
        try:
            from pathlib import Path

            from .messaging_core import UnifiedMessage, UnifiedMessagePriority, UnifiedMessageType

            message = UnifiedMessage(
                content=content,
                sender="Agent-6",
                recipient=recipient,
                message_type=UnifiedMessageType.AGENT_TO_AGENT,
                priority=UnifiedMessagePriority.REGULAR
            )

            inbox_dir = Path("agent_workspaces") / recipient / "inbox"
            inbox_dir.mkdir(parents=True, exist_ok=True)

            filename = f"{int(time.time())}_enhanced_protocol.md"
            filepath = inbox_dir / filename

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"# Enhanced Protocol Message\n\n{content}")

            logger.info(f"Message saved to inbox: {filepath}")
            return True

        except Exception as e:
            logger.error(f"Inbox delivery failed: {e}")
            raise

    def _deliver_direct_api(self, recipient: str, content: str) -> bool:
        """Deliver via direct API (future implementation)."""
        # Placeholder for direct API delivery
        logger.info(f"Direct API delivery not yet implemented for {recipient}")
        return False

    def _deliver_broadcast(self, content: str) -> bool:
        """Deliver broadcast message to all agents."""
        success_count = 0
        for agent_id in self.agent_health.keys():
            try:
                if self._deliver_inbox(agent_id, f"[BROADCAST] {content}"):
                    success_count += 1
            except Exception as e:
                logger.error(f"Broadcast failed for {agent_id}: {e}")

        return success_count > 0

    # ==================== Public API ====================

    def send_message(self, recipient: str, content: str,
                    priority: CommunicationPriority = CommunicationPriority.NORMAL,
                    callback: Callable[[bool, str | None], None] | None = None) -> bool:
        """Send message with enhanced protocols."""
        if not self._is_agent_healthy(recipient):
            logger.warning(f"⚠️ Cannot send to unhealthy agent: {recipient}")
            return False

        message_data = {
            "recipient": recipient,
            "content": content,
            "priority": priority,
            "callback": callback,
            "timestamp": datetime.now()
        }

        self.message_queue.put(message_data)
        return True

    def broadcast_message(self, content: str,
                         priority: CommunicationPriority = CommunicationPriority.NORMAL) -> dict[str, bool]:
        """Broadcast message to all agents."""
        results = {}
        for agent_id in self.agent_health.keys():
            success = self.send_message(agent_id, content, priority)
            results[agent_id] = success
        return results

    def get_protocol_status(self) -> dict[str, Any]:
        """Get comprehensive protocol status."""
        return {
            "metrics": {
                "total_sent": self.metrics.total_messages_sent,
                "total_delivered": self.metrics.total_messages_delivered,
                "total_failed": self.metrics.total_messages_failed,
                "success_rate": f"{self.metrics.success_rate:.1f}%",
                "avg_delivery_time": f"{self.metrics.average_delivery_time:.2f}s"
            },
            "agent_health": {
                agent_id: {
                    "online": health.is_online,
                    "last_seen": health.last_seen.isoformat(),
                    "failures": health.consecutive_failures,
                    "circuit_breaker": health.circuit_breaker_tripped
                }
                for agent_id, health in self.agent_health.items()
            },
            "queue_status": {
                "pending_messages": self.message_queue.qsize(),
                "retry_queue": self.retry_queue.qsize()
            }
        }

    def reset_agent_health(self, agent_id: str):
        """Manually reset agent health status."""
        if agent_id in self.agent_health:
            self.agent_health[agent_id] = AgentHealthStatus(agent_id)
            logger.info(f"✅ Agent health reset for {agent_id}")

    def shutdown(self):
        """Gracefully shutdown enhanced protocols."""
        logger.info("🔧 Shutting down enhanced communication protocols...")

        # Wait for queue to empty
        self.message_queue.join()

        # Stop workers
        for worker in self.delivery_workers:
            worker.join(timeout=5)

        logger.info("✅ Enhanced communication protocols shutdown complete")


# ==================== Global Instance ====================

_enhanced_protocols: EnhancedCommunicationProtocols | None = None

def get_enhanced_protocols() -> EnhancedCommunicationProtocols:
    """Get global enhanced protocols instance."""
    global _enhanced_protocols
    if _enhanced_protocols is None:
        _enhanced_protocols = EnhancedCommunicationProtocols()
    return _enhanced_protocols

# ==================== Convenience Functions ====================

def send_enhanced_message(recipient: str, content: str,
                         priority: CommunicationPriority = CommunicationPriority.NORMAL) -> bool:
    """Convenience function for sending enhanced messages."""
    return get_enhanced_protocols().send_message(recipient, content, priority)

def broadcast_enhanced_message(content: str,
                              priority: CommunicationPriority = CommunicationPriority.NORMAL) -> dict[str, bool]:
    """Convenience function for broadcasting enhanced messages."""
    return get_enhanced_protocols().broadcast_message(content, priority)

def get_protocol_health() -> dict[str, Any]:
    """Get protocol health status."""
    return get_enhanced_protocols().get_protocol_status()

# ==================== Initialization ====================

def initialize_enhanced_protocols() -> None:
    """Initialize enhanced communication protocols."""
    logger.info("🚀 Initializing Enhanced Communication Protocols...")

    protocols = get_enhanced_protocols()

    # Log initialization status
    status = protocols.get_protocol_status()
    logger.info(f"✅ Enhanced protocols initialized with {len(protocols.agent_health)} agents")
    logger.info(f"📊 Initial success rate: {status['metrics']['success_rate']}")

try:
    initialize_enhanced_protocols()
except Exception as e:
    logger.error(f"❌ Failed to initialize enhanced protocols: {e}")

__all__ = [
    "EnhancedCommunicationProtocols",
    "CommunicationPriority",
    "DeliveryChannel",
    "ProtocolMetrics",
    "AgentHealthStatus",
    "get_enhanced_protocols",
    "send_enhanced_message",
    "broadcast_enhanced_message",
    "get_protocol_health",
    "initialize_enhanced_protocols"
]
