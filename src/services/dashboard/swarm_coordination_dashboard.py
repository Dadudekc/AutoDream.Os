#!/usr/bin/env python3
"""
Swarm Coordination Dashboard
============================

Real-time dashboard for monitoring and coordinating Team Alpha agents.
Provides captain with comprehensive visibility into agent status, tasks, and performance.

Author: Agent-2 (Architecture & Design Specialist) + Agent-4 (Captain)
License: MIT
"""

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class AgentStatus(Enum):
    """Agent status enumeration"""
    ACTIVE = "active"
    IDLE = "idle"
    WORKING = "working"
    STALLED = "stalled"
    ERROR = "error"
    OFFLINE = "offline"

class TaskStatus(Enum):
    """Task status enumeration"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    BLOCKED = "blocked"

@dataclass
class AgentInfo:
    """Agent information data class"""
    agent_id: str
    status: AgentStatus
    current_task: Optional[str]
    last_activity: datetime
    coordinates: tuple
    performance_score: float
    message_count: int
    error_count: int

@dataclass
class TaskInfo:
    """Task information data class"""
    task_id: str
    title: str
    status: TaskStatus
    assigned_agent: str
    priority: str
    created_at: datetime
    updated_at: datetime
    progress: float

class SwarmCoordinationDashboard:
    """Main dashboard class for swarm coordination"""
    
    def __init__(self, config_path: str = "config/coordinates.json"):
        self.config_path = config_path
        self.agents: Dict[str, AgentInfo] = {}
        self.tasks: Dict[str, TaskInfo] = {}
        self.messages: List[Dict[str, Any]] = []
        self.alerts: List[Dict[str, Any]] = []
        self.last_update = datetime.now(timezone.utc)
        
    def initialize(self):
        """Initialize dashboard with agent data"""
        self._load_agent_coordinates()
        self._load_task_data()
        self._load_message_history()
        
    def _load_agent_coordinates(self):
        """Load agent coordinates from configuration"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                coords_data = json.load(f)
                
            for agent_id, agent_data in coords_data.get("agents", {}).items():
                coords = agent_data.get("chat_input_coordinates", [0, 0])
                self.agents[agent_id] = AgentInfo(
                    agent_id=agent_id,
                    status=AgentStatus.ACTIVE,
                    current_task=None,
                    last_activity=datetime.now(timezone.utc),
                    coordinates=tuple(coords),
                    performance_score=100.0,
                    message_count=0,
                    error_count=0
                )
        except Exception as e:
            print(f"Error loading agent coordinates: {e}")
            
    def _load_task_data(self):
        """Load task data from agent workspaces"""
        # This would integrate with the task management system
        # For now, create sample data
        sample_tasks = [
            TaskInfo(
                task_id="V3-005",
                title="Intelligent Alerting System",
                status=TaskStatus.COMPLETED,
                assigned_agent="Agent-2",
                priority="HIGH",
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
                progress=100.0
            ),
            TaskInfo(
                task_id="TESLA-001",
                title="Tesla Stock Forecast App Frontend",
                status=TaskStatus.COMPLETED,
                assigned_agent="Agent-2",
                priority="HIGH",
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
                progress=100.0
            )
        ]
        
        for task in sample_tasks:
            self.tasks[task.task_id] = task
            
    def _load_message_history(self):
        """Load recent message history"""
        # This would integrate with the messaging system
        # For now, create sample data
        self.messages = [
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "from": "Agent-2",
                "to": "Agent-4",
                "message": "Swarm Coordination Dashboard collaboration confirmed!",
                "priority": "NORMAL"
            }
        ]
        
    def get_agent_status(self, agent_id: str) -> Optional[AgentInfo]:
        """Get status for a specific agent"""
        return self.agents.get(agent_id)
        
    def get_all_agent_status(self) -> Dict[str, AgentInfo]:
        """Get status for all agents"""
        return self.agents.copy()
        
    def get_task_status(self, task_id: str) -> Optional[TaskInfo]:
        """Get status for a specific task"""
        return self.tasks.get(task_id)
        
    def get_all_task_status(self) -> Dict[str, TaskInfo]:
        """Get status for all tasks"""
        return self.tasks.copy()
        
    def get_recent_messages(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent messages"""
        return self.messages[-limit:] if self.messages else []
        
    def get_alerts(self) -> List[Dict[str, Any]]:
        """Get current alerts"""
        return self.alerts.copy()
        
    def add_alert(self, alert_type: str, message: str, agent_id: str = None):
        """Add a new alert"""
        alert = {
            "id": f"alert_{len(self.alerts) + 1}",
            "type": alert_type,
            "message": message,
            "agent_id": agent_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "acknowledged": False
        }
        self.alerts.append(alert)
        
    def acknowledge_alert(self, alert_id: str):
        """Acknowledge an alert"""
        for alert in self.alerts:
            if alert["id"] == alert_id:
                alert["acknowledged"] = True
                break
                
    def update_agent_status(self, agent_id: str, status: AgentStatus, 
                          current_task: str = None, performance_score: float = None):
        """Update agent status"""
        if agent_id in self.agents:
            agent = self.agents[agent_id]
            agent.status = status
            agent.last_activity = datetime.now(timezone.utc)
            if current_task:
                agent.current_task = current_task
            if performance_score is not None:
                agent.performance_score = performance_score
                
    def update_task_progress(self, task_id: str, progress: float, 
                           status: TaskStatus = None):
        """Update task progress"""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.progress = progress
            task.updated_at = datetime.now(timezone.utc)
            if status:
                task.status = status
                
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get complete dashboard data"""
        return {
            "timestamp": self.last_update.isoformat(),
            "agents": {
                agent_id: {
                    "agent_id": agent.agent_id,
                    "status": agent.status.value,
                    "current_task": agent.current_task,
                    "last_activity": agent.last_activity.isoformat(),
                    "coordinates": agent.coordinates,
                    "performance_score": agent.performance_score,
                    "message_count": agent.message_count,
                    "error_count": agent.error_count
                }
                for agent_id, agent in self.agents.items()
            },
            "tasks": {
                task_id: {
                    "task_id": task.task_id,
                    "title": task.title,
                    "status": task.status.value,
                    "assigned_agent": task.assigned_agent,
                    "priority": task.priority,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat(),
                    "progress": task.progress
                }
                for task_id, task in self.tasks.items()
            },
            "messages": self.get_recent_messages(20),
            "alerts": self.get_alerts(),
            "summary": self._get_summary_stats()
        }
        
    def _get_summary_stats(self) -> Dict[str, Any]:
        """Get summary statistics"""
        total_agents = len(self.agents)
        active_agents = sum(1 for agent in self.agents.values() 
                          if agent.status == AgentStatus.ACTIVE)
        total_tasks = len(self.tasks)
        completed_tasks = sum(1 for task in self.tasks.values() 
                            if task.status == TaskStatus.COMPLETED)
        pending_alerts = sum(1 for alert in self.alerts if not alert["acknowledged"])
        
        return {
            "total_agents": total_agents,
            "active_agents": active_agents,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "completion_rate": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
            "pending_alerts": pending_alerts,
            "last_update": self.last_update.isoformat()
        }
        
    def refresh(self):
        """Refresh dashboard data"""
        self.last_update = datetime.now(timezone.utc)
        # This would trigger data refresh from various sources
        # For now, just update the timestamp
        
    def export_data(self, format: str = "json") -> str:
        """Export dashboard data"""
        data = self.get_dashboard_data()
        if format.lower() == "json":
            return json.dumps(data, indent=2)
        else:
            return str(data)


