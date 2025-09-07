#!/usr/bin/env python3
"""
AI Agent Manager Models
=======================

Data models for AI agent management system.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any


@dataclass
class Skill:
    """Represents a skill and its proficiency level"""
    name: str
    level: int = 0  # 0-100 scale
    last_updated: datetime = field(default_factory=datetime.now)
    experience_points: int = 0
    category: str = "general"
    
    def adjust(self, delta: int) -> int:
        """Adjust the skill level by delta clamped to 0-100"""
        old_level = self.level
        self.level = max(0, min(100, self.level + delta))
        self.last_updated = datetime.now()
        
        # Award experience points for skill increases
        if self.level > old_level:
            self.experience_points += (self.level - old_level) * 10
        
        return self.level
    
    def get_proficiency_label(self) -> str:
        """Get human-readable proficiency label"""
        if self.level >= 90:
            return "Expert"
        elif self.level >= 75:
            return "Advanced"
        elif self.level >= 50:
            return "Intermediate"
        elif self.level >= 25:
            return "Beginner"
        else:
            return "Novice"


@dataclass
class AIAgentTask:
    """Represents a task assigned to an AI agent"""
    task_id: str
    task_type: str
    priority: int = 1  # 1-10 scale
    complexity: int = 1  # 1-10 scale
    estimated_duration: int = 0  # minutes
    assigned_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    status: str = "pending"  # pending, in_progress, completed, failed
    progress: float = 0.0  # 0.0-100.0
    agent_id: Optional[str] = None
    
    def start(self, agent_id: str):
        """Start the task"""
        self.agent_id = agent_id
        self.started_at = datetime.now()
        self.status = "in_progress"
    
    def update_progress(self, progress: float):
        """Update task progress"""
        self.progress = max(0.0, min(100.0, progress))
        if self.progress >= 100.0:
            self.complete()
    
    def complete(self):
        """Mark task as completed"""
        self.completed_at = datetime.now()
        self.status = "completed"
        self.progress = 100.0
    
    def fail(self):
        """Mark task as failed"""
        self.status = "failed"
    
    def get_duration(self) -> Optional[int]:
        """Get actual task duration in minutes"""
        if self.started_at and self.completed_at:
            duration = self.completed_at - self.started_at
            return int(duration.total_seconds() / 60)
        return None


@dataclass
class AIAgent:
    """Represents an AI agent with its capabilities and status"""
    agent_id: str
    name: str
    agent_type: str = "general"
    status: str = "active"  # active, inactive, busy, offline
    max_resources: Dict[str, float] = field(default_factory=dict)
    skills: Dict[str, Skill] = field(default_factory=dict)
    total_tasks_completed: int = 0
    total_tasks_failed: int = 0
    average_task_duration: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    last_activity: Optional[datetime] = None
    
    def update_activity(self):
        """Update last activity timestamp"""
        self.last_activity = datetime.now()
    
    def add_skill(self, skill_name: str, initial_level: int = 0, category: str = "general"):
        """Add a new skill to the agent"""
        if skill_name not in self.skills:
            self.skills[skill_name] = Skill(
                name=skill_name,
                level=initial_level,
                category=category
            )
    
    def improve_skill(self, skill_name: str, improvement: int):
        """Improve a skill by the specified amount"""
        if skill_name in self.skills:
            self.skills[skill_name].adjust(improvement)
    
    def get_skill_level(self, skill_name: str) -> int:
        """Get the level of a specific skill"""
        return self.skills.get(skill_name, Skill(skill_name)).level
    
    def get_skill_summary(self) -> Dict[str, Dict[str, Any]]:
        """Get summary of all skills"""
        return {
            skill_name: {
                "level": skill.level,
                "proficiency": skill.get_proficiency_label(),
                "category": skill.category,
                "experience_points": skill.experience_points
            }
            for skill_name, skill in self.skills.items()
        }
