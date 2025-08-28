#!/usr/bin/env python3
"""
Message Queue System - Agent Cellphone V2
========================================

Coordinates 8 agents to prevent keyboard conflicts and ensure orderly execution.
Single responsibility: Message queue management and agent coordination.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
import time
import threading
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
from queue import Queue, PriorityQueue

# Import existing priority system to avoid duplication
from .models.unified_message import UnifiedMessagePriority

logger = logging.getLogger(__name__)


class AgentStatus(Enum):
    """Agent status states"""
    IDLE = "idle"
    WORKING = "working"
    WAITING = "waiting"
    COMPLETED = "completed"
    ERROR = "error"


@dataclass
class QueuedMessage:
    """Message in the queue"""
    priority: UnifiedMessagePriority
    timestamp: float
    agent_id: str
    message: str
    message_type: str
    requires_response: bool
    response_timeout: float = 30.0  # seconds


@dataclass
class AgentState:
    """Current state of an agent"""
    status: AgentStatus
    current_task: Optional[str]
    last_activity: float
    response_count: int
    compliance_score: float = 1.0


class MessageQueueSystem:
    """
    Message Queue System - Single responsibility: Coordinate 8 agents
    
    This class only handles:
    - Message queuing and prioritization
    - Agent state tracking
    - Keyboard conflict prevention
    - Response monitoring
    """
    
    def __init__(self):
        """Initialize the message queue system"""
        self.message_queue = PriorityQueue()
        self.agent_states: Dict[str, AgentState] = {}
        self.response_queue = Queue()
        self.coordination_lock = threading.Lock()
        self.system_active = True
        
        # Initialize agent states
        for i in range(1, 9):
            agent_id = f"Agent-{i}"
            self.agent_states[agent_id] = AgentState(
                status=AgentStatus.IDLE,
                current_task=None,
                last_activity=time.time(),
                response_count=0
            )
        
        # Start coordination thread
        self.coordination_thread = threading.Thread(target=self._coordination_loop, daemon=True)
        self.coordination_thread.start()
        
        logger.info("Message Queue System initialized with 8 agents")
    
    def queue_message(self, agent_id: str, message: str, message_type: str = "text", 
                     priority: UnifiedMessagePriority = UnifiedMessagePriority.NORMAL, 
                     requires_response: bool = True) -> bool:
        """Queue a message for an agent"""
        try:
            queued_msg = QueuedMessage(
                priority=priority,
                timestamp=time.time(),
                agent_id=agent_id,
                message=message,
                message_type=message_type,
                requires_response=requires_response
            )
            
            # Calculate priority score (lower = higher priority)
            priority_score = priority.value
            
            self.message_queue.put((priority_score, queued_msg))
            logger.info(f"Message queued for {agent_id} with priority {priority.value}")
            return True
            
        except Exception as e:
            logger.error(f"Error queuing message: {e}")
            return False
    
    def get_next_message(self) -> Optional[QueuedMessage]:
        """Get the next message from the queue"""
        try:
            if not self.message_queue.empty():
                priority_score, queued_msg = self.message_queue.get()
                return queued_msg
            return None
        except Exception as e:
            logger.error(f"Error getting next message: {e}")
            return None
    
    def update_agent_state(self, agent_id: str, status: AgentStatus, 
                          task: Optional[str] = None) -> None:
        """Update agent state"""
        with self.coordination_lock:
            if agent_id in self.agent_states:
                self.agent_states[agent_id].status = status
                self.agent_states[agent_id].current_task = task
                self.agent_states[agent_id].last_activity = time.time()
                
                if status == AgentStatus.COMPLETED:
                    self.agent_states[agent_id].response_count += 1
                    self.agent_states[agent_id].compliance_score = min(1.0, 
                        self.agent_states[agent_id].compliance_score + 0.1)
                
                logger.info(f"Agent {agent_id} state updated: {status.value}")
    
    def record_response(self, agent_id: str, response: str) -> None:
        """Record agent response"""
        with self.coordination_lock:
            if agent_id in self.agent_states:
                self.agent_states[agent_id].last_activity = time.time()
                self.agent_states[agent_id].response_count += 1
                self.agent_states[agent_id].compliance_score = min(1.0, 
                    self.agent_states[agent_id].compliance_score + 0.05)
                
                # Add to response queue for processing
                self.response_queue.put((agent_id, response, time.time()))
                
                logger.info(f"Response recorded from {agent_id}")
    
    def get_agent_status(self, agent_id: str) -> Optional[AgentState]:
        """Get current status of an agent"""
        return self.agent_states.get(agent_id)
    
    def get_all_agent_statuses(self) -> Dict[str, AgentState]:
        """Get status of all agents"""
        return self.agent_states.copy()
    
    def check_keyboard_conflicts(self) -> List[str]:
        """Check for potential keyboard conflicts between agents"""
        conflicts = []
        working_agents = []
        
        with self.coordination_lock:
            for agent_id, state in self.agent_states.items():
                if state.status == AgentStatus.WORKING:
                    working_agents.append(agent_id)
            
            # If more than 1 agent is working, potential conflict
            if len(working_agents) > 1:
                conflicts = working_agents
                logger.warning(f"Keyboard conflict detected: {conflicts}")
        
        return conflicts
    
    def enforce_agent_priority(self) -> None:
        """Enforce agent priority to prevent conflicts"""
        with self.coordination_lock:
            # Only allow 1 agent to work at a time
            working_count = sum(1 for state in self.agent_states.values() 
                              if state.status == AgentStatus.WORKING)
            
            if working_count > 1:
                # Force all but highest priority agent to wait
                highest_priority = None
                for agent_id, state in self.agent_states.items():
                    if state.status == AgentStatus.WORKING:
                        if highest_priority is None or state.compliance_score > self.agent_states[highest_priority].compliance_score:
                            highest_priority = agent_id
                
                for agent_id, state in self.agent_states.items():
                    if state.status == AgentStatus.WORKING and agent_id != highest_priority:
                        state.status = AgentStatus.WAITING
                        logger.info(f"Agent {agent_id} forced to wait to prevent keyboard conflict")
    
    def _coordination_loop(self) -> None:
        """Main coordination loop"""
        while self.system_active:
            try:
                # Check for keyboard conflicts
                conflicts = self.check_keyboard_conflicts()
                if conflicts:
                    self.enforce_agent_priority()
                
                # Process response queue
                while not self.response_queue.empty():
                    agent_id, response, timestamp = self.response_queue.get()
                    logger.info(f"Processing response from {agent_id}: {response[:50]}...")
                
                # Sleep to prevent excessive CPU usage
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error in coordination loop: {e}")
                time.sleep(1.0)
    
    def shutdown(self) -> None:
        """Shutdown the message queue system"""
        self.system_active = False
        logger.info("Message Queue System shutdown")


# Global instance
message_queue_system = MessageQueueSystem()
