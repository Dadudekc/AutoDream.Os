#!/usr/bin/env python3
"""
Agent Metrics - Clean OOP Design
================================

Agent metrics following clean object-oriented principles.
Single responsibility: Track agent performance metrics.

Author: Agent-1 (Integration Specialist)
License: MIT
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any


@dataclass
class AgentMetrics:
    """Agent performance metrics."""
    
    # Performance metrics
    tasks_completed: int = 0
    tasks_failed: int = 0
    average_response_time: float = 0.0
    uptime_percentage: float = 100.0
    
    # Resource usage
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    disk_usage: float = 0.0
    
    # Communication metrics
    messages_sent: int = 0
    messages_received: int = 0
    commands_executed: int = 0
    
    # Timestamps
    last_activity: datetime = field(default_factory=datetime.now)
    last_error: datetime = field(default_factory=datetime.now)
    
    # Custom metrics
    custom_metrics: Dict[str, Any] = field(default_factory=dict)
    
    def get_success_rate(self) -> float:
        """Calculate task success rate."""
        total_tasks = self.tasks_completed + self.tasks_failed
        if total_tasks == 0:
            return 100.0
        return (self.tasks_completed / total_tasks) * 100
    
    def get_uptime_hours(self) -> float:
        """Get uptime in hours."""
        return self.uptime_percentage * 24 / 100
    
    def update_activity(self):
        """Update last activity timestamp."""
        self.last_activity = datetime.now()
    
    def record_task_completion(self, success: bool, response_time: float):
        """Record task completion."""
        if success:
            self.tasks_completed += 1
        else:
            self.tasks_failed += 1
            self.last_error = datetime.now()
        
        # Update average response time
        total_tasks = self.tasks_completed + self.tasks_failed
        self.average_response_time = (
            (self.average_response_time * (total_tasks - 1) + response_time) / total_tasks
        )
        self.update_activity()
    
    def record_message(self, sent: bool):
        """Record message activity."""
        if sent:
            self.messages_sent += 1
        else:
            self.messages_received += 1
        self.update_activity()
    
    def record_command(self):
        """Record command execution."""
        self.commands_executed += 1
        self.update_activity()
    
    def set_custom_metric(self, key: str, value: Any):
        """Set custom metric."""
        self.custom_metrics[key] = value
        self.update_activity()
    
    def get_custom_metric(self, key: str, default: Any = None) -> Any:
        """Get custom metric."""
        return self.custom_metrics.get(key, default)