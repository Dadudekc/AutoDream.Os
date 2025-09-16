#!/usr/bin/env python3
"""
Swarm Communication Core Module - V2 Compliant
Core communication functionality extracted from swarm_communication_coordinator.py
V2 Compliance: ≤400 lines for compliance

Author: Agent-7 (Web Development Specialist) - Swarm Coordination
License: MIT
"""

from __future__ import annotations

import asyncio
import json
import logging
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)


class SwarmDecisionType(Enum):
    """Types of swarm decisions that require democratic voting."""
    MISSION_ASSIGNMENT = "mission_assignment"
    ARCHITECTURE_CHANGE = "architecture_change"
    QUALITY_STANDARD_UPDATE = "quality_standard_update"
    RESOURCE_ALLOCATION = "resource_allocation"
    PHASE_TRANSITION = "phase_transition"
    EMERGENCY_RESPONSE = "emergency_response"


class SwarmAgentStatus(Enum):
    """Status of swarm agents."""
    ACTIVE = "active"
    IDLE = "idle"
    BUSY = "busy"
    OFFLINE = "offline"
    ERROR = "error"


@dataclass
class SwarmAgent:
    """Represents a swarm agent with its capabilities and status."""
    agent_id: str
    role: str
    status: SwarmAgentStatus = SwarmAgentStatus.IDLE
    capabilities: Set[str] = field(default_factory=set)
    current_mission: Optional[str] = None
    last_activity: datetime = field(default_factory=datetime.now)
    performance_metrics: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SwarmDecision:
    """Represents a democratic decision in the swarm."""
    decision_id: str
    decision_type: SwarmDecisionType
    description: str
    options: List[str]
    votes: Dict[str, str] = field(default_factory=dict)
    deadline: Optional[datetime] = None
    status: str = "pending"
    result: Optional[str] = None


class SwarmCommunicationCore:
    """
    Core swarm communication functionality.
    
    V2 Compliance: Extracted from monolithic 762-line file.
    """

    def __init__(self):
        self.agents: Dict[str, SwarmAgent] = {}
        self.decisions: Dict[str, SwarmDecision] = {}
        self.communication_threads: Dict[str, threading.Thread] = {}
        self.is_running = False
        self.executor = ThreadPoolExecutor(max_workers=8)
        
        # Web interface integration
        self.web_interface = None
        self.ui_callbacks = []

    async def initialize(self) -> bool:
        """Initialize the swarm communication core."""
        try:
            logger.info("🐝 Initializing Swarm Communication Core...")
            
            # Initialize web interface integration
            await self._initialize_web_interface()
            
            # Start communication monitoring
            self.is_running = True
            await self._start_communication_monitoring()
            
            logger.info("✅ Swarm Communication Core initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize Swarm Communication Core: {e}")
            return False

    async def _initialize_web_interface(self):
        """Initialize web interface integration."""
        try:
            # Web interface integration for real-time monitoring
            self.web_interface = {
                "agents": {},
                "decisions": {},
                "metrics": {},
                "last_updated": datetime.now().isoformat()
            }
            logger.info("🌐 Web interface integration initialized")
        except Exception as e:
            logger.error(f"❌ Web interface initialization failed: {e}")

    async def _start_communication_monitoring(self):
        """Start monitoring swarm communication."""
        try:
            # Start background monitoring thread
            monitor_thread = threading.Thread(
                target=self._monitor_swarm_communication,
                daemon=True
            )
            monitor_thread.start()
            self.communication_threads["monitor"] = monitor_thread
            logger.info("📡 Swarm communication monitoring started")
        except Exception as e:
            logger.error(f"❌ Failed to start communication monitoring: {e}")

    def _monitor_swarm_communication(self):
        """Monitor swarm communication in background thread."""
        while self.is_running:
            try:
                # Update agent statuses
                self._update_agent_statuses()
                
                # Process pending decisions
                self._process_pending_decisions()
                
                # Update web interface
                self._update_web_interface()
                
                time.sleep(1)  # Monitor every second
                
            except Exception as e:
                logger.error(f"❌ Communication monitoring error: {e}")
                time.sleep(5)  # Wait longer on error

    def _update_agent_statuses(self):
        """Update agent statuses based on activity."""
        current_time = datetime.now()
        
        for agent_id, agent in self.agents.items():
            # Check if agent is inactive
            time_since_activity = (current_time - agent.last_activity).total_seconds()
            
            if time_since_activity > 300:  # 5 minutes
                if agent.status != SwarmAgentStatus.OFFLINE:
                    agent.status = SwarmAgentStatus.OFFLINE
                    logger.warning(f"⚠️ Agent {agent_id} marked as offline")

    def _process_pending_decisions(self):
        """Process pending democratic decisions."""
        current_time = datetime.now()
        
        for decision_id, decision in self.decisions.items():
            if decision.status == "pending" and decision.deadline:
                if current_time > decision.deadline:
                    # Deadline reached, finalize decision
                    self._finalize_decision(decision_id)

    def _finalize_decision(self, decision_id: str):
        """Finalize a democratic decision."""
        decision = self.decisions.get(decision_id)
        if not decision:
            return

        # Count votes
        vote_counts = {}
        for option in decision.options:
            vote_counts[option] = sum(1 for vote in decision.votes.values() if vote == option)

        # Determine winner
        if vote_counts:
            winner = max(vote_counts, key=vote_counts.get)
            decision.result = winner
            decision.status = "completed"
            
            logger.info(f"🗳️ Decision {decision_id} finalized: {winner}")
            
            # Notify web interface
            self._notify_web_interface("decision_completed", {
                "decision_id": decision_id,
                "result": winner,
                "vote_counts": vote_counts
            })

    def _update_web_interface(self):
        """Update web interface data."""
        try:
            self.web_interface.update({
                "agents": {
                    agent_id: {
                        "role": agent.role,
                        "status": agent.status.value,
                        "current_mission": agent.current_mission,
                        "last_activity": agent.last_activity.isoformat(),
                        "capabilities": list(agent.capabilities)
                    }
                    for agent_id, agent in self.agents.items()
                },
                "decisions": {
                    decision_id: {
                        "type": decision.decision_type.value,
                        "description": decision.description,
                        "status": decision.status,
                        "result": decision.result,
                        "vote_count": len(decision.votes)
                    }
                    for decision_id, decision in self.decisions.items()
                },
                "metrics": {
                    "total_agents": len(self.agents),
                    "active_agents": len([a for a in self.agents.values() if a.status == SwarmAgentStatus.ACTIVE]),
                    "pending_decisions": len([d for d in self.decisions.values() if d.status == "pending"]),
                    "completed_decisions": len([d for d in self.decisions.values() if d.status == "completed"])
                },
                "last_updated": datetime.now().isoformat()
            })
        except Exception as e:
            logger.error(f"❌ Web interface update failed: {e}")

    def _notify_web_interface(self, event_type: str, data: Dict[str, Any]):
        """Notify web interface of events."""
        try:
            for callback in self.ui_callbacks:
                try:
                    callback(event_type, data)
                except Exception as e:
                    logger.error(f"❌ Web interface callback error: {e}")
        except Exception as e:
            logger.error(f"❌ Web interface notification failed: {e}")

    def register_agent(self, agent_id: str, role: str, capabilities: Set[str]) -> bool:
        """Register a new agent in the swarm."""
        try:
            agent = SwarmAgent(
                agent_id=agent_id,
                role=role,
                capabilities=capabilities,
                status=SwarmAgentStatus.ACTIVE
            )
            
            self.agents[agent_id] = agent
            logger.info(f"✅ Agent {agent_id} registered as {role}")
            
            # Notify web interface
            self._notify_web_interface("agent_registered", {
                "agent_id": agent_id,
                "role": role,
                "capabilities": list(capabilities)
            })
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to register agent {agent_id}: {e}")
            return False

    def update_agent_status(self, agent_id: str, status: SwarmAgentStatus, mission: Optional[str] = None) -> bool:
        """Update agent status and current mission."""
        try:
            agent = self.agents.get(agent_id)
            if not agent:
                logger.warning(f"⚠️ Agent {agent_id} not found")
                return False

            agent.status = status
            agent.current_mission = mission
            agent.last_activity = datetime.now()
            
            logger.info(f"🔄 Agent {agent_id} status updated: {status.value}")
            
            # Notify web interface
            self._notify_web_interface("agent_status_updated", {
                "agent_id": agent_id,
                "status": status.value,
                "mission": mission
            })
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to update agent {agent_id} status: {e}")
            return False

    def create_decision(self, decision_type: SwarmDecisionType, description: str, options: List[str], deadline_minutes: int = 10) -> str:
        """Create a new democratic decision."""
        try:
            decision_id = f"decision_{int(time.time())}"
            deadline = datetime.now().timestamp() + (deadline_minutes * 60)
            
            decision = SwarmDecision(
                decision_id=decision_id,
                decision_type=decision_type,
                description=description,
                options=options,
                deadline=datetime.fromtimestamp(deadline)
            )
            
            self.decisions[decision_id] = decision
            logger.info(f"🗳️ Decision {decision_id} created: {description}")
            
            # Notify web interface
            self._notify_web_interface("decision_created", {
                "decision_id": decision_id,
                "type": decision_type.value,
                "description": description,
                "options": options,
                "deadline": deadline
            })
            
            return decision_id
            
        except Exception as e:
            logger.error(f"❌ Failed to create decision: {e}")
            return ""

    def cast_vote(self, agent_id: str, decision_id: str, option: str) -> bool:
        """Cast a vote in a democratic decision."""
        try:
            decision = self.decisions.get(decision_id)
            if not decision:
                logger.warning(f"⚠️ Decision {decision_id} not found")
                return False

            if decision.status != "pending":
                logger.warning(f"⚠️ Decision {decision_id} is not pending")
                return False

            if option not in decision.options:
                logger.warning(f"⚠️ Invalid option {option} for decision {decision_id}")
                return False

            decision.votes[agent_id] = option
            logger.info(f"🗳️ Agent {agent_id} voted for {option} in decision {decision_id}")
            
            # Notify web interface
            self._notify_web_interface("vote_cast", {
                "agent_id": agent_id,
                "decision_id": decision_id,
                "option": option,
                "total_votes": len(decision.votes)
            })
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to cast vote: {e}")
            return False

    def get_swarm_status(self) -> Dict[str, Any]:
        """Get current swarm status for web interface."""
        return {
            "agents": self.agents,
            "decisions": self.decisions,
            "web_interface": self.web_interface,
            "is_running": self.is_running
        }

    def add_web_interface_callback(self, callback):
        """Add web interface callback for real-time updates."""
        self.ui_callbacks.append(callback)

    async def shutdown(self):
        """Shutdown the swarm communication core."""
        try:
            logger.info("🛑 Shutting down Swarm Communication Core...")
            
            self.is_running = False
            
            # Stop all communication threads
            for thread in self.communication_threads.values():
                thread.join(timeout=5)
            
            # Shutdown executor
            self.executor.shutdown(wait=True)
            
            logger.info("✅ Swarm Communication Core shutdown complete")
            
        except Exception as e:
            logger.error(f"❌ Error during shutdown: {e}")


# Global instance for web interface integration
_swarm_communication_core = None


def get_swarm_communication_core() -> SwarmCommunicationCore:
    """Get the global swarm communication core instance."""
    global _swarm_communication_core
    if _swarm_communication_core is None:
        _swarm_communication_core = SwarmCommunicationCore()
    return _swarm_communication_core

