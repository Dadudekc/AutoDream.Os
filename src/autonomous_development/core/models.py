#!/usr/bin/env python3
"""
Autonomous Development Models - Agent Cellphone V2
================================================

Data models for autonomous development system.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
from .enums import TaskPriority, TaskComplexity, TaskStatus


@dataclass
class DevelopmentTask:
    """Development task definition"""
    
    task_id: str
    title: str
    description: str
    complexity: TaskComplexity
    priority: TaskPriority
    estimated_hours: float
    required_skills: List[str]
    status: TaskStatus = TaskStatus.AVAILABLE
    claimed_by: Optional[str] = None
    claimed_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    progress_percentage: float = 0.0
    blockers: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Post-initialization validation"""
        if self.progress_percentage < 0.0:
            self.progress_percentage = 0.0
        elif self.progress_percentage > 100.0:
            self.progress_percentage = 100.0
    
    def claim(self, agent_id: str) -> bool:
        """Claim the task for an agent"""
        if self.status != TaskStatus.AVAILABLE:
            return False
        
        self.claimed_by = agent_id
        self.claimed_at = datetime.now()
        self.status = TaskStatus.CLAIMED
        self.updated_at = datetime.now()
        return True
    
    def start_work(self) -> bool:
        """Start working on the task"""
        if self.status != TaskStatus.CLAIMED:
            return False
        
        self.started_at = datetime.now()
        self.status = TaskStatus.IN_PROGRESS
        self.updated_at = datetime.now()
        return True
    
    def update_progress(self, percentage: float) -> bool:
        """Update task progress"""
        if self.status != TaskStatus.IN_PROGRESS:
            return False
        
        self.progress_percentage = max(0.0, min(100.0, percentage))
        self.updated_at = datetime.now()
        
        if self.progress_percentage >= 100.0:
            self.complete()
        
        return True
    
    def complete(self) -> bool:
        """Mark task as completed"""
        if self.status != TaskStatus.IN_PROGRESS:
            return False
        
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now()
        self.progress_percentage = 100.0
        self.updated_at = datetime.now()
        return True
    
    def block(self, reason: str) -> bool:
        """Block the task with a reason"""
        if self.status not in [TaskStatus.CLAIMED, TaskStatus.IN_PROGRESS]:
            return False
        
        self.status = TaskStatus.BLOCKED
        self.blockers.append(reason)
        self.updated_at = datetime.now()
        return True
    
    def unblock(self) -> bool:
        """Unblock the task"""
        if self.status != TaskStatus.BLOCKED:
            return False
        
        # Return to previous state
        if self.started_at:
            self.status = TaskStatus.IN_PROGRESS
        else:
            self.status = TaskStatus.CLAIMED
        
        self.updated_at = datetime.now()
        return True
    
    def cancel(self) -> bool:
        """Cancel the task"""
        if self.status in [TaskStatus.COMPLETED, TaskStatus.CANCELLED]:
            return False
        
        self.status = TaskStatus.CANCELLED
        self.updated_at = datetime.now()
        return True
    
    def add_dependency(self, task_id: str) -> bool:
        """Add a dependency to this task"""
        if task_id not in self.dependencies:
            self.dependencies.append(task_id)
            self.updated_at = datetime.now()
            return True
        return False
    
    def remove_dependency(self, task_id: str) -> bool:
        """Remove a dependency from this task"""
        if task_id in self.dependencies:
            self.dependencies.remove(task_id)
            self.updated_at = datetime.now()
            return True
        return False
    
    def add_tag(self, tag: str) -> bool:
        """Add a tag to the task"""
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now()
            return True
        return False
    
    def remove_tag(self, tag: str) -> bool:
        """Remove a tag from the task"""
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.now()
            return True
        return False
    
    def get_elapsed_time(self) -> Optional[float]:
        """Get elapsed time since task was claimed (in hours)"""
        if not self.claimed_at:
            return None
        
        end_time = self.completed_at or datetime.now()
        elapsed = end_time - self.claimed_at
        return elapsed.total_seconds() / 3600.0
    
    def get_remaining_time(self) -> Optional[float]:
        """Get estimated remaining time (in hours)"""
        if self.status == TaskStatus.COMPLETED:
            return 0.0
        
        if self.progress_percentage <= 0:
            return self.estimated_hours
        
        # Estimate based on progress
        elapsed = self.get_elapsed_time() or 0.0
        if elapsed <= 0:
            return self.estimated_hours
        
        # Calculate remaining based on progress rate
        progress_rate = self.progress_percentage / elapsed
        if progress_rate <= 0:
            return self.estimated_hours
        
        remaining_percentage = 100.0 - self.progress_percentage
        return remaining_percentage / progress_rate
    
    def is_blocked(self) -> bool:
        """Check if task is blocked"""
        return self.status == TaskStatus.BLOCKED
    
    def is_available(self) -> bool:
        """Check if task is available for claiming"""
        return self.status == TaskStatus.AVAILABLE
    
    def is_in_progress(self) -> bool:
        """Check if task is in progress"""
        return self.status == TaskStatus.IN_PROGRESS
    
    def is_completed(self) -> bool:
        """Check if task is completed"""
        return self.status == TaskStatus.COMPLETED
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary for serialization"""
        return {
            'task_id': self.task_id,
            'title': self.title,
            'description': self.description,
            'complexity': self.complexity.value,
            'priority': self.priority.value,
            'estimated_hours': self.estimated_hours,
            'required_skills': self.required_skills,
            'status': self.status.value,
            'claimed_by': self.claimed_by,
            'claimed_at': self.claimed_at.isoformat() if self.claimed_at else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'progress_percentage': self.progress_percentage,
            'blockers': self.blockers,
            'dependencies': self.dependencies,
            'tags': self.tags,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DevelopmentTask':
        """Create task from dictionary"""
        # Convert enum values back to enum objects
        data['complexity'] = TaskComplexity(data['complexity'])
        data['priority'] = TaskPriority(data['priority'])
        data['status'] = TaskStatus(data['status'])
        
        # Convert datetime strings back to datetime objects
        for field in ['claimed_at', 'started_at', 'completed_at', 'created_at', 'updated_at']:
            if data.get(field):
                data[field] = datetime.fromisoformat(data[field])
        
        return cls(**data)
