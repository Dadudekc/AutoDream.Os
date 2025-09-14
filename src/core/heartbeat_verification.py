#!/usr/bin/env python3
"""
HEARTBEAT VERIFICATION SYSTEM - CRISIS RESPONSE
==============================================

Implements heartbeat verification between all agents and emergency broadcast system.
Part of THEA's emergency routing patch implementation.

Author: Agent-4 (Strategic Oversight & Emergency Intervention Manager)
License: MIT
"""

from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Set

from .messaging_core import (
    UnifiedMessage,
    UnifiedMessagePriority,
    UnifiedMessageType,
    UnifiedMessageTag,
    get_messaging_core
)
from .routing_tracer import get_routing_tracer

logger = logging.getLogger(__name__)

# SWARM AGENTS - Single source of truth
SWARM_AGENTS = [
    "Agent-1", "Agent-2", "Agent-3", "Agent-4",
    "Agent-5", "Agent-6", "Agent-7", "Agent-8"
]


@dataclass
class HeartbeatStatus:
    """Heartbeat status for an agent."""
    agent_id: str
    last_heartbeat: datetime
    is_online: bool
    response_time_ms: float
    consecutive_failures: int
    last_error: Optional[str] = None


@dataclass
class EmergencyBroadcast:
    """Emergency broadcast message."""
    broadcast_id: str
    sender: str
    content: str
    priority: UnifiedMessagePriority
    timestamp: datetime
    target_agents: List[str]
    delivery_status: Dict[str, bool]
    acknowledgment_required: bool = True


class HeartbeatVerificationSystem:
    """Heartbeat verification system for agent monitoring."""
    
    def __init__(self, heartbeat_interval: int = 15, timeout_seconds: int = 30):
        self.logger = logging.getLogger(__name__)
        self.heartbeat_interval = heartbeat_interval
        self.timeout_seconds = timeout_seconds
        
        # Initialize agent status
        self.agent_status: Dict[str, HeartbeatStatus] = {}
        for agent in SWARM_AGENTS:
            self.agent_status[agent] = HeartbeatStatus(
                agent_id=agent,
                last_heartbeat=datetime.now(),
                is_online=True,
                response_time_ms=0.0,
                consecutive_failures=0
            )
        
        self.messaging_core = get_messaging_core()
        self.routing_tracer = get_routing_tracer()
        self.emergency_broadcasts: List[EmergencyBroadcast] = []
        
        # Start heartbeat monitoring
        self._start_heartbeat_monitoring()
    
    def _start_heartbeat_monitoring(self):
        """Start heartbeat monitoring in background."""
        import threading
        
        def heartbeat_loop():
            while True:
                try:
                    asyncio.run(self._check_all_agent_heartbeats())
                    time.sleep(self.heartbeat_interval)
                except Exception as e:
                    self.logger.error(f"Heartbeat monitoring error: {e}")
                    time.sleep(60)  # Wait longer on error
        
        heartbeat_thread = threading.Thread(target=heartbeat_loop, daemon=True)
        heartbeat_thread.start()
        self.logger.info("Heartbeat monitoring started")
    
    async def _check_all_agent_heartbeats(self):
        """Check heartbeats for all agents."""
        for agent in SWARM_AGENTS:
            try:
                await self._check_agent_heartbeat(agent)
            except Exception as e:
                self.logger.error(f"Heartbeat check failed for {agent}: {e}")
                self._mark_agent_offline(agent, str(e))
    
    async def _check_agent_heartbeat(self, agent_id: str):
        """Check heartbeat for specific agent."""
        start_time = time.time()
        
        try:
            # Send heartbeat message
            heartbeat_message = UnifiedMessage(
                content=f"HEARTBEAT_CHECK_{int(time.time())}",
                sender="SYSTEM",
                recipient=agent_id,
                message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
                priority=UnifiedMessagePriority.REGULAR,
                tags=[UnifiedMessageTag.SYSTEM]
            )
            
            # Start trace
            trace_id = self.routing_tracer.start_trace(heartbeat_message)
            
            # Send message
            success = self.messaging_core.send_message_object(heartbeat_message)
            
            # Calculate response time
            response_time = (time.time() - start_time) * 1000
            
            # Complete trace
            self.routing_tracer.complete_trace(
                trace_id,
                "delivered" if success else "failed",
                verification_passed=success,
                processing_time_ms=response_time
            )
            
            # Update agent status
            if success:
                self._mark_agent_online(agent_id, response_time)
            else:
                self._mark_agent_offline(agent_id, "Message delivery failed")
                
        except Exception as e:
            self._mark_agent_offline(agent_id, str(e))
    
    def _mark_agent_online(self, agent_id: str, response_time_ms: float):
        """Mark agent as online."""
        if agent_id in self.agent_status:
            self.agent_status[agent_id].last_heartbeat = datetime.now()
            self.agent_status[agent_id].is_online = True
            self.agent_status[agent_id].response_time_ms = response_time_ms
            self.agent_status[agent_id].consecutive_failures = 0
            self.agent_status[agent_id].last_error = None
            
            self.logger.debug(f"Agent {agent_id} is online (response time: {response_time_ms:.1f}ms)")
    
    def _mark_agent_offline(self, agent_id: str, error_message: str):
        """Mark agent as offline."""
        if agent_id in self.agent_status:
            self.agent_status[agent_id].is_online = False
            self.agent_status[agent_id].consecutive_failures += 1
            self.agent_status[agent_id].last_error = error_message
            
            self.logger.warning(f"Agent {agent_id} is offline: {error_message} (failures: {self.agent_status[agent_id].consecutive_failures})")
            
            # Trigger emergency response for critical agents
            if agent_id == "Agent-8" and self.agent_status[agent_id].consecutive_failures >= 3:
                self._trigger_emergency_response(agent_id)
    
    def _trigger_emergency_response(self, agent_id: str):
        """Trigger emergency response for critical agent failure."""
        self.logger.critical(f"EMERGENCY: Critical agent {agent_id} is offline!")
        
        # Send emergency broadcast
        emergency_content = f"🚨 EMERGENCY ALERT: {agent_id} is offline and requires immediate attention!"
        
        self.send_emergency_broadcast(
            content=emergency_content,
            sender="SYSTEM",
            priority=UnifiedMessagePriority.URGENT,
            target_agents=["Agent-4"]  # Notify Captain
        )
    
    def get_agent_status(self, agent_id: str) -> Optional[HeartbeatStatus]:
        """Get status for specific agent."""
        return self.agent_status.get(agent_id)
    
    def get_all_agent_status(self) -> Dict[str, HeartbeatStatus]:
        """Get status for all agents."""
        return self.agent_status.copy()
    
    def get_online_agents(self) -> List[str]:
        """Get list of online agents."""
        return [agent for agent, status in self.agent_status.items() if status.is_online]
    
    def get_offline_agents(self) -> List[str]:
        """Get list of offline agents."""
        return [agent for agent, status in self.agent_status.items() if not status.is_online]
    
    def send_emergency_broadcast(self, content: str, sender: str, 
                               priority: UnifiedMessagePriority = UnifiedMessagePriority.URGENT,
                               target_agents: Optional[List[str]] = None) -> str:
        """Send emergency broadcast message."""
        try:
            broadcast_id = f"EMERGENCY_{int(time.time())}"
            target_agents = target_agents or SWARM_AGENTS
            
            # Create emergency broadcast
            emergency_broadcast = EmergencyBroadcast(
                broadcast_id=broadcast_id,
                sender=sender,
                content=content,
                priority=priority,
                timestamp=datetime.now(),
                target_agents=target_agents,
                delivery_status={},
                acknowledgment_required=True
            )
            
            # Send to all target agents
            for agent in target_agents:
                try:
                    message = UnifiedMessage(
                        content=content,
                        sender=sender,
                        recipient=agent,
                        message_type=UnifiedMessageType.BROADCAST,
                        priority=priority,
                        tags=[UnifiedMessageTag.SYSTEM]
                    )
                    
                    success = self.messaging_core.send_message_object(message)
                    emergency_broadcast.delivery_status[agent] = success
                    
                    if success:
                        self.logger.info(f"Emergency broadcast sent to {agent}")
                    else:
                        self.logger.error(f"Failed to send emergency broadcast to {agent}")
                        
                except Exception as e:
                    self.logger.error(f"Emergency broadcast error for {agent}: {e}")
                    emergency_broadcast.delivery_status[agent] = False
            
            # Store broadcast
            self.emergency_broadcasts.append(emergency_broadcast)
            
            self.logger.critical(f"Emergency broadcast {broadcast_id} sent to {len(target_agents)} agents")
            return broadcast_id
            
        except Exception as e:
            self.logger.error(f"Emergency broadcast failed: {e}")
            return ""
    
    def get_system_health_summary(self) -> Dict[str, Any]:
        """Get comprehensive system health summary."""
        try:
            online_agents = self.get_online_agents()
            offline_agents = self.get_offline_agents()
            
            # Calculate average response time
            response_times = [status.response_time_ms for status in self.agent_status.values() if status.is_online]
            avg_response_time = sum(response_times) / len(response_times) if response_times else 0.0
            
            # Get recent emergency broadcasts
            recent_broadcasts = [
                broadcast for broadcast in self.emergency_broadcasts
                if broadcast.timestamp > datetime.now() - timedelta(hours=1)
            ]
            
            return {
                "total_agents": len(SWARM_AGENTS),
                "online_agents": len(online_agents),
                "offline_agents": len(offline_agents),
                "online_agent_list": online_agents,
                "offline_agent_list": offline_agents,
                "average_response_time_ms": avg_response_time,
                "system_health": "HEALTHY" if len(offline_agents) == 0 else "DEGRADED" if len(offline_agents) <= 2 else "CRITICAL",
                "recent_emergency_broadcasts": len(recent_broadcasts),
                "last_health_check": datetime.now().isoformat(),
                "agent_details": {
                    agent: {
                        "is_online": status.is_online,
                        "last_heartbeat": status.last_heartbeat.isoformat(),
                        "response_time_ms": status.response_time_ms,
                        "consecutive_failures": status.consecutive_failures,
                        "last_error": status.last_error
                    }
                    for agent, status in self.agent_status.items()
                }
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get system health summary: {e}")
            return {"error": str(e)}


# Global heartbeat verification system instance
_heartbeat_system = None


def get_heartbeat_system() -> HeartbeatVerificationSystem:
    """Get global heartbeat verification system instance."""
    global _heartbeat_system
    if _heartbeat_system is None:
        _heartbeat_system = HeartbeatVerificationSystem()
    return _heartbeat_system


# Convenience functions
def check_agent_health(agent_id: str) -> Optional[HeartbeatStatus]:
    """Check health status of specific agent."""
    system = get_heartbeat_system()
    return system.get_agent_status(agent_id)


def get_system_health() -> Dict[str, Any]:
    """Get comprehensive system health status."""
    system = get_heartbeat_system()
    return system.get_system_health_summary()


def send_emergency_alert(content: str, target_agents: Optional[List[str]] = None) -> str:
    """Send emergency alert to specified agents."""
    system = get_heartbeat_system()
    return system.send_emergency_broadcast(
        content=content,
        sender="SYSTEM",
        priority=UnifiedMessagePriority.URGENT,
        target_agents=target_agents
    )