#!/usr/bin/env python3
"""
Extended AI Agent Manager - inherits from BaseManager for unified functionality

This manager consolidates AI agent management functionality from:
- src/ai_ml/ai_agent_resource_manager.py
- src/ai_ml/ai_agent_skills.py  
- src/ai_ml/ai_agent_workload.py

into a V2-compliant system.
"""

import logging
from typing import Dict, List, Optional, Any, DefaultDict, Deque
from dataclasses import dataclass, field
from collections import defaultdict, deque
from datetime import datetime, timedelta

from src.core.base_manager import BaseManager
from src.utils.stability_improvements import stability_manager, safe_import

# Configure logging
logger = logging.getLogger(__name__)


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
            return int((self.completed_at - self.started_at).total_seconds() / 60)
        return None


class ExtendedAIAgentManager(BaseManager):
    """Extended AI Agent Manager - inherits from BaseManager for unified functionality"""
    
    def __init__(self, config_path: str = "config/ai_ml/ai_agent_manager.json"):
        super().__init__(
            manager_name="ExtendedAIAgentManager",
            config_path=config_path,
            enable_metrics=True,
            enable_events=True,
            enable_persistence=True
        )
        
        # AI Agent management state
        self.agents: Dict[str, Dict[str, Any]] = {}
        self.skills: Dict[str, Dict[str, Skill]] = defaultdict(dict)
        self.workloads: DefaultDict[str, Deque[AIAgentTask]] = defaultdict(deque)
        self.resource_usage: Dict[str, Dict[str, int]] = defaultdict(dict)
        self.task_history: List[AIAgentTask] = []
        
        # Resource management settings
        self.max_resources_per_agent = 100
        self.resource_types = ["cpu", "memory", "gpu", "network", "storage"]
        self.enable_auto_balancing = True
        self.balancing_threshold = 0.2  # 20% difference triggers rebalancing
        
        # Skill management settings
        self.max_skills_per_agent = 50
        self.skill_categories = ["general", "specialized", "domain", "technical", "soft"]
        self.enable_skill_decay = False
        self.skill_decay_rate = 0.1  # 10% per month
        
        # Workload management settings
        self.max_tasks_per_agent = 10
        self.task_priority_weights = {
            "priority": 0.4,
            "complexity": 0.3,
            "estimated_duration": 0.2,
            "agent_skill_match": 0.1
        }
        
        # Initialize AI agent management components
        self._initialize_ai_agent_components()
        
        logger.info(f"ExtendedAIAgentManager initialized successfully")
    
    def _initialize_ai_agent_components(self):
        """Initialize AI agent management components"""
        try:
            # Load configuration overrides
            if self.config:
                self.max_resources_per_agent = self.config.get("max_resources_per_agent", 100)
                self.resource_types = self.config.get("resource_types", self.resource_types)
                self.enable_auto_balancing = self.config.get("enable_auto_balancing", True)
                self.balancing_threshold = self.config.get("balancing_threshold", 0.2)
                
                self.max_skills_per_agent = self.config.get("max_skills_per_agent", 50)
                self.skill_categories = self.config.get("skill_categories", self.skill_categories)
                self.enable_skill_decay = self.config.get("enable_skill_decay", False)
                self.skill_decay_rate = self.config.get("skill_decay_rate", 0.1)
                
                self.max_tasks_per_agent = self.config.get("max_tasks_per_agent", 10)
                self.task_priority_weights = self.config.get("task_priority_weights", self.task_priority_weights)
            
            logger.info("✅ AI Agent management components initialized")
            
        except Exception as e:
            logger.error(f"❌ Error initializing AI agent components: {e}")
    
    # Resource Management Methods
    
    def register_agent(self, agent_id: str, agent_info: Optional[Dict[str, Any]] = None) -> bool:
        """Register a new AI agent"""
        try:
            if agent_id in self.agents:
                logger.warning(f"⚠️ Agent {agent_id} already registered")
                return False
            
            # Initialize agent data
            self.agents[agent_id] = {
                "registered_at": datetime.now(),
                "status": "active",
                "total_tasks_completed": 0,
                "total_skills_learned": 0,
                "current_resources": {rt: 0 for rt in self.resource_types},
                "max_resources": {rt: self.max_resources_per_agent for rt in self.resource_types},
                "last_activity": datetime.now()
            }
            
            if agent_info:
                self.agents[agent_id].update(agent_info)
            
            # Initialize workload queue
            self.workloads[agent_id] = deque()
            
            # Initialize resource usage tracking
            self.resource_usage[agent_id] = {rt: 0 for rt in self.resource_types}
            
            # Emit agent registered event
            self.emit_event("ai_agent_registered", {
                "agent_id": agent_id,
                "agent_info": agent_info or {},
                "timestamp": datetime.now().isoformat()
            })
            
            logger.info(f"✅ Agent {agent_id} registered successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error registering agent {agent_id}: {e}")
            return False
    
    def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an AI agent"""
        try:
            if agent_id not in self.agents:
                logger.warning(f"⚠️ Agent {agent_id} not found")
                return False
            
            # Release all resources
            self._release_all_resources(agent_id)
            
            # Reassign pending tasks
            pending_tasks = list(self.workloads[agent_id])
            for task in pending_tasks:
                self._reassign_task(task, agent_id)
            
            # Remove agent data
            del self.agents[agent_id]
            del self.workloads[agent_id]
            del self.resource_usage[agent_id]
            
            # Emit agent unregistered event
            self.emit_event("ai_agent_unregistered", {
                "agent_id": agent_id,
                "timestamp": datetime.now().isoformat()
            })
            
            logger.info(f"✅ Agent {agent_id} unregistered successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error unregistering agent {agent_id}: {e}")
            return False
    
    def allocate_resources(self, agent_id: str, resources: Dict[str, int]) -> bool:
        """Allocate resources for an agent"""
        try:
            if agent_id not in self.agents:
                logger.error(f"❌ Agent {agent_id} not registered")
                return False
            
            # Check resource availability
            for resource_type, amount in resources.items():
                if resource_type not in self.resource_types:
                    logger.warning(f"⚠️ Unknown resource type: {resource_type}")
                    continue
                
                current_usage = self.resource_usage[agent_id].get(resource_type, 0)
                max_available = self.agents[agent_id]["max_resources"].get(resource_type, self.max_resources_per_agent)
                
                if current_usage + amount > max_available:
                    logger.warning(f"⚠️ Insufficient {resource_type} resources for agent {agent_id}")
                    return False
            
            # Allocate resources
            for resource_type, amount in resources.items():
                if resource_type in self.resource_types:
                    self.resource_usage[agent_id][resource_type] += amount
            
            # Emit resource allocated event
            self.emit_event("resources_allocated", {
                "agent_id": agent_id,
                "resources": resources,
                "timestamp": datetime.now().isoformat()
            })
            
            logger.info(f"✅ Allocated {sum(resources.values())} resource units to agent {agent_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error allocating resources: {e}")
            return False
    
    def release_resources(self, agent_id: str, resources: Dict[str, int]) -> bool:
        """Release previously allocated resources"""
        try:
            if agent_id not in self.agents:
                logger.error(f"❌ Agent {agent_id} not registered")
                return False
            
            # Release resources
            for resource_type, amount in resources.items():
                if resource_type in self.resource_types:
                    current_usage = self.resource_usage[agent_id].get(resource_type, 0)
                    self.resource_usage[agent_id][resource_type] = max(0, current_usage - amount)
            
            # Emit resource released event
            self.emit_event("resources_released", {
                "agent_id": agent_id,
                "resources": resources,
                "timestamp": datetime.now().isoformat()
            })
            
            logger.info(f"✅ Released {sum(resources.values())} resource units from agent {agent_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error releasing resources: {e}")
            return False
    
    def _release_all_resources(self, agent_id: str):
        """Release all resources for an agent"""
        if agent_id in self.resource_usage:
            resources_to_release = self.resource_usage[agent_id].copy()
            self.release_resources(agent_id, resources_to_release)
    
    def get_resource_usage(self, agent_id: str) -> Dict[str, int]:
        """Get current resource usage for an agent"""
        return self.resource_usage.get(agent_id, {}).copy()
    
    def get_available_resources(self, agent_id: str) -> Dict[str, int]:
        """Get available resources for an agent"""
        if agent_id not in self.agents:
            return {}
        
        available = {}
        for resource_type in self.resource_types:
            current = self.resource_usage.get(agent_id, {}).get(resource_type, 0)
            max_available = self.agents[agent_id]["max_resources"].get(resource_type, self.max_resources_per_agent)
            available[resource_type] = max(0, max_available - current)
        
        return available
    
    # Skill Management Methods
    
    def add_skill(self, agent_id: str, skill_name: str, level: int = 0, category: str = "general") -> Optional[Skill]:
        """Add a skill to an agent"""
        try:
            if agent_id not in self.agents:
                logger.error(f"❌ Agent {agent_id} not registered")
                return None
            
            if len(self.skills[agent_id]) >= self.max_skills_per_agent:
                logger.warning(f"⚠️ Agent {agent_id} has reached maximum skills limit")
                return None
            
            skill = Skill(
                name=skill_name,
                level=max(0, min(100, level)),
                category=category
            )
            
            self.skills[agent_id][skill_name] = skill
            self.agents[agent_id]["total_skills_learned"] += 1
            
            # Emit skill added event
            self.emit_event("skill_added", {
                "agent_id": agent_id,
                "skill_name": skill_name,
                "level": level,
                "category": category,
                "timestamp": datetime.now().isoformat()
            })
            
            logger.info(f"✅ Added skill '{skill_name}' (level {level}) to agent {agent_id}")
            return skill
            
        except Exception as e:
            logger.error(f"❌ Error adding skill: {e}")
            return None
    
    def update_skill(self, agent_id: str, skill_name: str, delta: int) -> Optional[int]:
        """Update an agent's skill level"""
        try:
            if agent_id not in self.skills or skill_name not in self.skills[agent_id]:
                # Auto-create skill if it doesn't exist
                self.add_skill(agent_id, skill_name, 0)
            
            skill = self.skills[agent_id][skill_name]
            new_level = skill.adjust(delta)
            
            # Emit skill updated event
            self.emit_event("skill_updated", {
                "agent_id": agent_id,
                "skill_name": skill_name,
                "old_level": new_level - delta,
                "new_level": new_level,
                "delta": delta,
                "timestamp": datetime.now().isoformat()
            })
            
            logger.info(f"✅ Updated skill '{skill_name}' for agent {agent_id}: {new_level}")
            return new_level
            
        except Exception as e:
            logger.error(f"❌ Error updating skill: {e}")
            return None
    
    def get_skill_level(self, agent_id: str, skill_name: str) -> int:
        """Get an agent's skill level"""
        if agent_id in self.skills and skill_name in self.skills[agent_id]:
            return self.skills[agent_id][skill_name].level
        return 0
    
    def get_agent_skills(self, agent_id: str) -> Dict[str, Skill]:
        """Get all skills for an agent"""
        return self.skills.get(agent_id, {}).copy()
    
    def get_skills_by_category(self, agent_id: str, category: str) -> Dict[str, Skill]:
        """Get skills for an agent by category"""
        return {
            name: skill for name, skill in self.skills.get(agent_id, {}).items()
            if skill.category == category
        }
    
    def calculate_skill_match(self, agent_id: str, required_skills: Dict[str, int]) -> float:
        """Calculate how well an agent's skills match required skills"""
        try:
            if not required_skills:
                return 1.0
            
            total_match = 0.0
            total_weight = 0.0
            
            for skill_name, required_level in required_skills.items():
                agent_level = self.get_skill_level(agent_id, skill_name)
                match_score = min(1.0, agent_level / max(required_level, 1))
                total_match += match_score * required_level
                total_weight += required_level
            
            return total_match / total_weight if total_weight > 0 else 0.0
            
        except Exception as e:
            logger.error(f"❌ Error calculating skill match: {e}")
            return 0.0
    
    # Workload Management Methods
    
    def assign_task(self, agent_id: str, task: AIAgentTask) -> bool:
        """Assign a task to a specific agent"""
        try:
            if agent_id not in self.agents:
                logger.error(f"❌ Agent {agent_id} not registered")
                return False
            
            if len(self.workloads[agent_id]) >= self.max_tasks_per_agent:
                logger.warning(f"⚠️ Agent {agent_id} has reached maximum tasks limit")
                return False
            
            # Set agent ID
            task.agent_id = agent_id
            
            # Add to workload
            self.workloads[agent_id].append(task)
            
            # Emit task assigned event
            self.emit_event("task_assigned", {
                "agent_id": agent_id,
                "task_id": task.task_id,
                "task_type": task.task_type,
                "priority": task.priority,
                "timestamp": datetime.now().isoformat()
            })
            
            logger.info(f"✅ Task {task.task_id} assigned to agent {agent_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error assigning task: {e}")
            return False
    
    def get_workload(self, agent_id: str) -> List[AIAgentTask]:
        """Get workload for a specific agent"""
        return list(self.workloads.get(agent_id, []))
    
    def get_all_workloads(self) -> Dict[str, List[AIAgentTask]]:
        """Get workloads for all agents"""
        return {agent: list(tasks) for agent, tasks in self.workloads.items()}
    
    def start_task(self, agent_id: str, task_id: str) -> bool:
        """Start a specific task"""
        try:
            for task in self.workloads[agent_id]:
                if task.task_id == task_id and task.status == "pending":
                    task.start(agent_id)
                    
                    # Emit task started event
                    self.emit_event("task_started", {
                        "agent_id": agent_id,
                        "task_id": task_id,
                        "timestamp": datetime.now().isoformat()
                    })
                    
                    logger.info(f"✅ Task {task_id} started by agent {agent_id}")
                    return True
            
            logger.warning(f"⚠️ Task {task_id} not found or not pending")
            return False
            
        except Exception as e:
            logger.error(f"❌ Error starting task: {e}")
            return False
    
    def complete_task(self, agent_id: str, task_id: str) -> bool:
        """Complete a specific task"""
        try:
            for task in self.workloads[agent_id]:
                if task.task_id == task_id and task.status == "in_progress":
                    task.complete()
                    
                    # Update agent statistics
                    self.agents[agent_id]["total_tasks_completed"] += 1
                    self.agents[agent_id]["last_activity"] = datetime.now()
                    
                    # Move to history
                    self.task_history.append(task)
                    self.workloads[agent_id].remove(task)
                    
                    # Emit task completed event
                    self.emit_event("task_completed", {
                        "agent_id": agent_id,
                        "task_id": task_id,
                        "duration": task.get_duration(),
                        "timestamp": datetime.now().isoformat()
                    })
                    
                    logger.info(f"✅ Task {task_id} completed by agent {agent_id}")
                    return True
            
            logger.warning(f"⚠️ Task {task_id} not found or not in progress")
            return False
            
        except Exception as e:
            logger.error(f"❌ Error completing task: {e}")
            return False
    
    def balance_workloads(self) -> Dict[str, List[AIAgentTask]]:
        """Balance workloads across all agents"""
        try:
            if not self.enable_auto_balancing:
                return self.get_all_workloads()
            
            # Calculate current workload distribution
            workloads = self.get_all_workloads()
            total_tasks = sum(len(tasks) for tasks in workloads.values())
            agent_count = len(workloads)
            
            if agent_count == 0:
                return {}
            
            target_tasks_per_agent = total_tasks / agent_count
            
            # Check if rebalancing is needed
            max_deviation = max(
                abs(len(tasks) - target_tasks_per_agent) / max(target_tasks_per_agent, 1)
                for tasks in workloads.values()
            )
            
            if max_deviation <= self.balancing_threshold:
                logger.info("✅ Workloads are balanced, no rebalancing needed")
                return workloads
            
            # Pool all tasks
            all_tasks = []
            for tasks in workloads.values():
                all_tasks.extend(tasks)
                tasks.clear()
            
            # Redistribute tasks round-robin
            agent_ids = list(workloads.keys())
            for i, task in enumerate(all_tasks):
                agent_id = agent_ids[i % len(agent_ids)]
                self.workloads[agent_id].append(task)
            
            # Emit workload balanced event
            self.emit_event("workloads_balanced", {
                "total_tasks": total_tasks,
                "agent_count": agent_count,
                "target_per_agent": target_tasks_per_agent,
                "timestamp": datetime.now().isoformat()
            })
            
            logger.info(f"✅ Workloads rebalanced: {total_tasks} tasks across {agent_count} agents")
            return self.get_all_workloads()
            
        except Exception as e:
            logger.error(f"❌ Error balancing workloads: {e}")
            return self.get_all_workloads()
    
    def _reassign_task(self, task: AIAgentTask, old_agent_id: str):
        """Reassign a task to a different agent"""
        try:
            # Find best available agent
            best_agent = None
            best_score = -1
            
            for agent_id in self.agents:
                if agent_id != old_agent_id and len(self.workloads[agent_id]) < self.max_tasks_per_agent:
                    # Calculate assignment score
                    workload_score = 1.0 - (len(self.workloads[agent_id]) / self.max_tasks_per_agent)
                    skill_score = self.calculate_skill_match(agent_id, {task.task_type: 1})
                    
                    total_score = workload_score * 0.6 + skill_score * 0.4
                    
                    if total_score > best_score:
                        best_score = total_score
                        best_agent = agent_id
            
            if best_agent:
                self.assign_task(best_agent, task)
                logger.info(f"✅ Task {task.task_id} reassigned from {old_agent_id} to {best_agent}")
            else:
                logger.warning(f"⚠️ No suitable agent found for task {task.task_id}")
                
        except Exception as e:
            logger.error(f"❌ Error reassigning task: {e}")
    
    # Utility Methods
    
    def get_agent_status(self, agent_id: str) -> Dict[str, Any]:
        """Get comprehensive status for an agent"""
        if agent_id not in self.agents:
            return {}
        
        agent_data = self.agents[agent_id].copy()
        agent_data.update({
            "current_workload": len(self.workloads[agent_id]),
            "current_resources": self.get_resource_usage(agent_id),
            "available_resources": self.get_available_resources(agent_id),
            "total_skills": len(self.skills.get(agent_id, {})),
            "skill_summary": {
                skill.name: {
                    "level": skill.level,
                    "proficiency": skill.get_proficiency_label(),
                    "category": skill.category,
                    "experience_points": skill.experience_points
                } for skill in self.skills.get(agent_id, {}).values()
            }
        })
        
        return agent_data
    
    def get_system_summary(self) -> Dict[str, Any]:
        """Get comprehensive system summary"""
        try:
            total_agents = len(self.agents)
            total_tasks = sum(len(tasks) for tasks in self.workloads.values())
            total_skills = sum(len(skills) for skills in self.skills.values())
            total_completed_tasks = sum(agent["total_tasks_completed"] for agent in self.agents.values())
            
            # Calculate resource utilization
            total_resources = {}
            used_resources = {}
            for resource_type in self.resource_types:
                total_resources[resource_type] = sum(
                    agent["max_resources"].get(resource_type, self.max_resources_per_agent)
                    for agent in self.agents.values()
                )
                used_resources[resource_type] = sum(
                    usage.get(resource_type, 0) for usage in self.resource_usage.values()
                )
            
            resource_utilization = {}
            for resource_type in self.resource_types:
                total = total_resources.get(resource_type, 0)
                used = used_resources.get(resource_type, 0)
                resource_utilization[resource_type] = (used / total * 100) if total > 0 else 0
            
            summary = {
                "total_agents": total_agents,
                "active_agents": sum(1 for agent in self.agents.values() if agent["status"] == "active"),
                "total_tasks": total_tasks,
                "total_completed_tasks": total_completed_tasks,
                "total_skills": total_skills,
                "resource_utilization": resource_utilization,
                "workload_distribution": {
                    agent_id: len(tasks) for agent_id, tasks in self.workloads.items()
                },
                "last_updated": datetime.now().isoformat()
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"❌ Error generating system summary: {e}")
            return {}
    
    def get_ai_agent_metrics(self) -> Dict[str, Any]:
        """Get AI agent management performance metrics"""
        return {
            "total_agents_registered": len(self.agents),
            "total_skills_managed": sum(len(skills) for skills in self.skills.values()),
            "total_tasks_managed": sum(len(tasks) for tasks in self.workloads.values()),
            "total_tasks_completed": sum(agent["total_tasks_completed"] for agent in self.agents.values()),
            "average_workload": sum(len(tasks) for tasks in self.workloads.values()) / max(len(self.workloads), 1),
            "resource_utilization": sum(
                sum(usage.values()) for usage in self.resource_usage.values()
            ) / max(sum(
                sum(agent["max_resources"].values()) for agent in self.agents.values()
            ), 1) * 100,
            "uptime": self.get_uptime(),
            "last_activity": self.last_activity.isoformat() if self.last_activity else None
        }

