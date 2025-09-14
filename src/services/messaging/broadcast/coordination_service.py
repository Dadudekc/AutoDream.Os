#!/usr/bin/env python3
"""
Coordination Service - V2 Compliant Swarm Coordination
=====================================================

Service for managing swarm coordination, task distribution, and agent management.

V2 Compliance: <300 lines, single responsibility for coordination operations
Enterprise Ready: Task management, agent coordination, workflow orchestration

Author: Agent-4 (Captain) - V2_SWARM Consolidation
License: MIT
"""

import logging
import time
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from dataclasses import dataclass

try:
    from src.services.messaging.unified_service import get_unified_messaging_service
    from src.services.messaging.broadcast.broadcast_service import get_broadcast_service, BroadcastType, BroadcastPriority
    MESSAGING_AVAILABLE = True
except ImportError as e:
    logging.error(f"❌ Messaging service not available: {e}")
    MESSAGING_AVAILABLE = False

logger = logging.getLogger(__name__)

class CoordinationStatus(Enum):
    """Coordination status options."""
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskPriority(Enum):
    """Task priority levels."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

@dataclass
class CoordinationTask:
    """Coordination task data structure."""
    task_id: str
    agent_id: str
    description: str
    priority: TaskPriority
    status: CoordinationStatus
    created_at: str
    assigned_at: Optional[str] = None
    completed_at: Optional[str] = None
    results: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class CoordinationService:
    """V2 compliant coordination service for swarm management."""
    
    def __init__(self):
        """Initialize the coordination service."""
        self.messaging_service = get_unified_messaging_service() if MESSAGING_AVAILABLE else None
        self.broadcast_service = get_broadcast_service() if MESSAGING_AVAILABLE else None
        self.logger = logging.getLogger(__name__)
        
        # Coordination tracking
        self.active_tasks = {}
        self.task_history = []
        self.agent_status = {}
        
        # Agent definitions
        self.swarm_agents = [
            "Agent-1", "Agent-2", "Agent-3", "Agent-4",
            "Agent-5", "Agent-6", "Agent-7", "Agent-8"
        ]
        
        self.agent_roles = {
            "Agent-1": "Integration & Core Systems Specialist",
            "Agent-2": "Architecture & Design Specialist",
            "Agent-3": "Infrastructure & DevOps Specialist",
            "Agent-4": "Captain (Strategic Oversight & Emergency Intervention)",
            "Agent-5": "Business Intelligence Specialist",
            "Agent-6": "Coordination & Communication Specialist",
            "Agent-7": "Web Development Specialist",
            "Agent-8": "SSOT & System Integration Specialist"
        }
        
        # Initialize agent status
        for agent_id in self.swarm_agents:
            self.agent_status[agent_id] = {
                "status": "active",
                "last_activity": None,
                "current_task": None,
                "task_count": 0
            }
    
    def assign_task(self, agent_id: str, description: str, priority: TaskPriority = TaskPriority.NORMAL,
                   metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Assign task to specific agent."""
        if not self.messaging_service:
            self.logger.error("❌ Messaging service not available")
            return False
        
        if agent_id not in self.swarm_agents:
            self.logger.error(f"❌ Unknown agent: {agent_id}")
            return False
        
        try:
            # Create task
            task_id = f"task_{int(time.time())}_{agent_id}"
            task = CoordinationTask(
                task_id=task_id,
                agent_id=agent_id,
                description=description,
                priority=priority,
                status=CoordinationStatus.ACTIVE,
                created_at=time.strftime("%Y-%m-%d %H:%M:%S"),
                assigned_at=time.strftime("%Y-%m-%d %H:%M:%S"),
                metadata=metadata or {}
            )
            
            # Store task
            self.active_tasks[task_id] = task
            
            # Update agent status
            self.agent_status[agent_id]["current_task"] = task_id
            self.agent_status[agent_id]["task_count"] += 1
            self.agent_status[agent_id]["last_activity"] = time.strftime("%Y-%m-%d %H:%M:%S")
            
            # Send task assignment message
            message = self._format_task_assignment_message(task)
            success = self.messaging_service.send_message_to_agent(
                agent_id=agent_id,
                message=message,
                priority=priority.value.upper(),
                tag="TASK"
            )
            
            if success:
                self.logger.info(f"✅ Task {task_id} assigned to {agent_id}")
            else:
                self.logger.error(f"❌ Failed to send task assignment to {agent_id}")
                task.status = CoordinationStatus.FAILED
            
            return success
            
        except Exception as e:
            self.logger.error(f"❌ Error assigning task to {agent_id}: {e}")
            return False
    
    def complete_task(self, task_id: str, results: str) -> bool:
        """Mark task as completed."""
        if task_id not in self.active_tasks:
            self.logger.error(f"❌ Task not found: {task_id}")
            return False
        
        try:
            task = self.active_tasks[task_id]
            task.status = CoordinationStatus.COMPLETED
            task.completed_at = time.strftime("%Y-%m-%d %H:%M:%S")
            task.results = results
            
            # Update agent status
            agent_id = task.agent_id
            self.agent_status[agent_id]["current_task"] = None
            self.agent_status[agent_id]["last_activity"] = time.strftime("%Y-%m-%d %H:%M:%S")
            
            # Move to history
            self.task_history.append(task)
            del self.active_tasks[task_id]
            
            # Send completion acknowledgment
            message = self._format_task_completion_message(task)
            self.messaging_service.send_message_to_agent(
                agent_id=agent_id,
                message=message,
                priority="NORMAL",
                tag="TASK"
            )
            
            self.logger.info(f"✅ Task {task_id} completed by {agent_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error completing task {task_id}: {e}")
            return False
    
    def broadcast_coordination_update(self, message: str, priority: BroadcastPriority = BroadcastPriority.NORMAL) -> Dict[str, bool]:
        """Broadcast coordination update to all agents."""
        if not self.broadcast_service:
            self.logger.error("❌ Broadcast service not available")
            return dict.fromkeys(self.swarm_agents, False)
        
        return self.broadcast_service.broadcast_coordination_message(message, priority)
    
    def request_status_updates(self) -> Dict[str, bool]:
        """Request status updates from all agents."""
        message = """📊 STATUS UPDATE REQUEST

**From:** Captain Agent-4
**To:** ALL AGENTS
**Priority:** NORMAL

**Status Request:**
Please provide current status update including:
• Current task/project status
• Progress made since last update
• Any blockers or issues
• Next planned actions
• Estimated completion timeline

**Response Format:**
• Update your status.json file
• Create Discord devlog with status
• Send acknowledgment via messaging system

**Deadline:** Within 2 hours of receipt

🐝 WE ARE SWARM - Status update requested! ⚡️"""
        
        return self.broadcast_coordination_update(message)
    
    def get_agent_status(self, agent_id: Optional[str] = None) -> Dict[str, Any]:
        """Get status for specific agent or all agents."""
        if agent_id:
            if agent_id not in self.agent_status:
                return {"error": f"Unknown agent: {agent_id}"}
            
            status = self.agent_status[agent_id].copy()
            status["role"] = self.agent_roles.get(agent_id, "Unknown")
            
            # Add current task details if available
            if status["current_task"]:
                task_id = status["current_task"]
                if task_id in self.active_tasks:
                    task = self.active_tasks[task_id]
                    status["current_task_details"] = {
                        "task_id": task.task_id,
                        "description": task.description,
                        "priority": task.priority.value,
                        "assigned_at": task.assigned_at
                    }
            
            return status
        else:
            return {
                "total_agents": len(self.swarm_agents),
                "agent_status": self.agent_status.copy(),
                "agent_roles": self.agent_roles.copy(),
                "active_tasks": len(self.active_tasks),
                "completed_tasks": len(self.task_history)
            }
    
    def get_task_status(self, task_id: Optional[str] = None) -> Dict[str, Any]:
        """Get status for specific task or all tasks."""
        if task_id:
            if task_id in self.active_tasks:
                task = self.active_tasks[task_id]
                return {
                    "task_id": task.task_id,
                    "agent_id": task.agent_id,
                    "description": task.description,
                    "priority": task.priority.value,
                    "status": task.status.value,
                    "created_at": task.created_at,
                    "assigned_at": task.assigned_at,
                    "metadata": task.metadata
                }
            else:
                return {"error": f"Task not found: {task_id}"}
        else:
            return {
                "active_tasks": len(self.active_tasks),
                "completed_tasks": len(self.task_history),
                "task_list": list(self.active_tasks.keys())
            }
    
    def get_coordination_metrics(self) -> Dict[str, Any]:
        """Get coordination metrics."""
        total_tasks = len(self.active_tasks) + len(self.task_history)
        completed_tasks = len(self.task_history)
        
        return {
            "total_tasks": total_tasks,
            "active_tasks": len(self.active_tasks),
            "completed_tasks": completed_tasks,
            "completion_rate": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
            "active_agents": sum(1 for status in self.agent_status.values() if status["status"] == "active"),
            "total_agents": len(self.swarm_agents)
        }
    
    def _format_task_assignment_message(self, task: CoordinationTask) -> str:
        """Format task assignment message."""
        return f"""📋 TASK ASSIGNMENT - {task.agent_id}

**From:** Captain Agent-4
**To:** {task.agent_id}
**Priority:** {task.priority.value.upper()}
**Task ID:** {task.task_id}
**Timestamp:** {task.assigned_at}

**Task Description:**
{task.description}

**Assignment Instructions:**
1. Acknowledge receipt of this task
2. Update your status file with task details
3. Begin task execution
4. Report progress regularly
5. Create Discord devlog for task
6. Complete task and report results

**Task Metadata:**
{task.metadata if task.metadata else 'None'}

🐝 WE ARE SWARM - Task assigned and ready for execution! ⚡️"""
    
    def _format_task_completion_message(self, task: CoordinationTask) -> str:
        """Format task completion acknowledgment message."""
        return f"""✅ TASK COMPLETION ACKNOWLEDGED - {task.agent_id}

**From:** Captain Agent-4
**To:** {task.agent_id}
**Task ID:** {task.task_id}
**Completed At:** {task.completed_at}

**Task Completed:**
{task.description}

**Results:**
{task.results}

**Acknowledgment:**
Well done! Your task completion has been recorded.

**Next Steps:**
• Update your status file
• Create Discord devlog for completion
• Stand by for next assignment
• Maintain readiness for coordination

🐝 WE ARE SWARM - Task completed successfully! ⚡️"""

# Global service instance
coordination_service = CoordinationService()

# Public API functions
def get_coordination_service() -> CoordinationService:
    """Get the coordination service instance."""
    return coordination_service

def assign_task(agent_id: str, description: str, priority: TaskPriority = TaskPriority.NORMAL,
                metadata: Optional[Dict[str, Any]] = None) -> bool:
    """Assign task to agent."""
    return coordination_service.assign_task(agent_id, description, priority, metadata)

def complete_task(task_id: str, results: str) -> bool:
    """Complete task."""
    return coordination_service.complete_task(task_id, results)

def request_status_updates() -> Dict[str, bool]:
    """Request status updates from all agents."""
    return coordination_service.request_status_updates()

# Service exports
__all__ = [
    "CoordinationService",
    "CoordinationStatus",
    "TaskPriority",
    "CoordinationTask",
    "get_coordination_service",
    "assign_task",
    "complete_task",
    "request_status_updates",
    "coordination_service",
]