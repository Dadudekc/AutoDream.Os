#!/usr/bin/env python3
"""
Message Coordinator - V2 Standards Compliant
Core coordination logic for agent communication and task management
Follows V2 coding standards: ≤250 LOC, single responsibility
"""

import logging
import json
import time
import asyncio
import threading
from typing import Dict, Any, Optional, List, Callable, Union
from pathlib import Path
from datetime import datetime, timedelta
import uuid
import queue

try:
    from .coordinator_types import (
        CommunicationMode, TaskPriority, TaskStatus, CaptaincyTerm,
        CoordinationTask, CoordinationMessage, AgentCapability, CoordinationSession
    )
except ImportError:
    # Fallback for standalone usage
    from coordinator_types import (
        CommunicationMode, TaskPriority, TaskStatus, CaptaincyTerm,
        CoordinationTask, CoordinationMessage, AgentCapability, CoordinationSession
    )


class MessageCoordinator:
    """
    Core message coordination system for agent communication
    
    Responsibilities:
    - Task assignment and management
    - Message routing and delivery
    - Agent capability tracking
    - Coordination session management
    """

    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.MessageCoordinator")
        
        # Core data structures
        self.tasks: Dict[str, CoordinationTask] = {}
        self.agents: Dict[str, AgentCapability] = {}
        self.sessions: Dict[str, CoordinationSession] = {}
        self.message_queue = queue.Queue()
        
        # Configuration
        self.default_mode = CommunicationMode.COLLABORATIVE
        self.max_retries = 3
        self.retry_delay = 1.0
        
        # Threading
        self._running = False
        self._coordinator_thread = None
        self._lock = threading.Lock()

    def start_coordination(self):
        """Start the coordination system"""
        if self._running:
            self.logger.warning("Coordination system already running")
            return
        
        self._running = True
        self._coordinator_thread = threading.Thread(target=self._coordination_loop)
        self._coordinator_thread.daemon = True
        self._coordinator_thread.start()
        self.logger.info("Coordination system started")

    def stop_coordination(self):
        """Stop the coordination system"""
        self._running = False
        if self._coordinator_thread:
            self._coordinator_thread.join(timeout=5.0)
        self.logger.info("Coordination system stopped")

    def create_task(self, title: str, description: str, priority: TaskPriority,
                   assigned_agents: List[str], estimated_hours: float = 1.0,
                   tags: List[str] = None) -> str:
        """Create a new coordination task"""
        task_id = str(uuid.uuid4())
        task = CoordinationTask(
            task_id=task_id,
            title=title,
            description=description,
            priority=priority,
            status=TaskStatus.PENDING,
            assigned_agents=assigned_agents,
            dependencies=[],
            created_at=datetime.now(),
            due_date=None,
            estimated_hours=estimated_hours,
            actual_hours=0.0,
            progress_percentage=0.0,
            tags=tags or []
        )
        
        with self._lock:
            self.tasks[task_id] = task
        
        self.logger.info(f"Created task: {title} (ID: {task_id})")
        return task_id

    def assign_task(self, task_id: str, agent_id: str) -> bool:
        """Assign a task to an agent"""
        if task_id not in self.tasks:
            self.logger.error(f"Task {task_id} not found")
            return False
        
        if agent_id not in self.agents:
            self.logger.error(f"Agent {agent_id} not found")
            return False
        
        task = self.tasks[task_id]
        if agent_id not in task.assigned_agents:
            task.assigned_agents.append(agent_id)
        
        task.status = TaskStatus.ASSIGNED
        self.logger.info(f"Assigned task {task_id} to agent {agent_id}")
        return True

    def update_task_status(self, task_id: str, status: TaskStatus, 
                          progress_percentage: float = None) -> bool:
        """Update task status and progress"""
        if task_id not in self.tasks:
            self.logger.error(f"Task {task_id} not found")
            return False
        
        task = self.tasks[task_id]
        task.status = status
        
        if progress_percentage is not None:
            task.progress_percentage = max(0.0, min(100.0, progress_percentage))
        
        self.logger.info(f"Updated task {task_id} status to {status.value}")
        return True

    def register_agent(self, agent_id: str, capabilities: List[str],
                      specializations: List[str] = None) -> bool:
        """Register an agent with capabilities"""
        agent = AgentCapability(
            agent_id=agent_id,
            capabilities=capabilities,
            specializations=specializations or [],
            availability=True,
            current_load=0,
            max_capacity=10
        )
        
        with self._lock:
            self.agents[agent_id] = agent
        
        self.logger.info(f"Registered agent {agent_id} with {len(capabilities)} capabilities")
        return True

    def create_coordination_session(self, mode: CommunicationMode,
                                  participants: List[str], agenda: List[str] = None) -> str:
        """Create a new coordination session"""
        session_id = str(uuid.uuid4())
        session = CoordinationSession(
            session_id=session_id,
            mode=mode,
            participants=participants,
            start_time=datetime.now(),
            end_time=None,
            agenda=agenda or [],
            decisions=[]
        )
        
        with self._lock:
            self.sessions[session_id] = session
        
        self.logger.info(f"Created {mode.value} coordination session: {session_id}")
        return session_id

    def send_message(self, sender_id: str, recipient_ids: List[str],
                    message_type: str, content: str, priority: TaskPriority = TaskPriority.NORMAL) -> str:
        """Send a coordination message"""
        message_id = str(uuid.uuid4())
        message = CoordinationMessage(
            message_id=message_id,
            sender_id=sender_id,
            recipient_ids=recipient_ids,
            message_type=message_type,
            content=content,
            timestamp=datetime.now(),
            priority=priority,
            metadata={}
        )
        
        # Add to message queue for processing
        self.message_queue.put(message)
        self.logger.info(f"Queued message {message_id} from {sender_id} to {len(recipient_ids)} recipients")
        return message_id

    def get_agent_tasks(self, agent_id: str) -> List[CoordinationTask]:
        """Get all tasks assigned to an agent"""
        return [task for task in self.tasks.values() if agent_id in task.assigned_agents]

    def get_available_agents(self, required_capabilities: List[str] = None) -> List[str]:
        """Get available agents with required capabilities"""
        available = []
        for agent_id, agent in self.agents.items():
            if not agent.availability or agent.current_load >= agent.max_capacity:
                continue
            
            if required_capabilities:
                if not all(cap in agent.capabilities for cap in required_capabilities):
                    continue
            
            available.append(agent_id)
        
        return available

    def _coordination_loop(self):
        """Main coordination loop for processing messages"""
        while self._running:
            try:
                # Process messages from queue
                try:
                    message = self.message_queue.get(timeout=1.0)
                    self._process_message(message)
                except queue.Empty:
                    continue
                
                # Update task statuses
                self._update_task_statuses()
                
                # Clean up completed sessions
                self._cleanup_sessions()
                
            except Exception as e:
                self.logger.error(f"Error in coordination loop: {e}")
                time.sleep(self.retry_delay)

    def _process_message(self, message: CoordinationMessage):
        """Process a coordination message"""
        try:
            self.logger.debug(f"Processing message {message.message_id}")
            
            # Route message to recipients
            for recipient_id in message.recipient_ids:
                if recipient_id in self.agents:
                    self._deliver_message(message, recipient_id)
                else:
                    self.logger.warning(f"Recipient {recipient_id} not found")
                    
        except Exception as e:
            self.logger.error(f"Error processing message {message.message_id}: {e}")

    def _deliver_message(self, message: CoordinationMessage, recipient_id: str):
        """Deliver a message to a specific recipient"""
        # In a real implementation, this would integrate with the messaging system
        self.logger.info(f"Delivered message {message.message_id} to {recipient_id}")

    def _update_task_statuses(self):
        """Update task statuses based on progress"""
        current_time = datetime.now()
        for task in self.tasks.values():
            if task.status == TaskStatus.IN_PROGRESS:
                # Check if task is overdue
                if task.due_date and current_time > task.due_date:
                    task.status = TaskStatus.BLOCKED

    def _cleanup_sessions(self):
        """Clean up completed coordination sessions"""
        current_time = datetime.now()
        expired_sessions = []
        
        for session_id, session in self.sessions.items():
            if session.end_time and current_time > session.end_time:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            del self.sessions[session_id]
            self.logger.info(f"Cleaned up expired session: {session_id}")
