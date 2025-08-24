#!/usr/bin/env python3
"""
Autonomous Development Agent Coordinator
=======================================

This module handles agent coordination and task matching for autonomous development.
Follows SRP by focusing solely on agent management and coordination.
"""

import random
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

from src.utils.stability_improvements import stability_manager, safe_import
# Use type hints with strings to avoid circular imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.autonomous_development.core import DevelopmentTask


class AgentCoordinator:
    """Coordinates agents and manages their skills and workloads"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.agent_workloads = {}
        self.agent_skills = {}

        # Initialize agent workloads and skills
        self._initialize_agents()

    def _initialize_agents(self):
        """Initialize agent workloads and skills"""
        for i in range(2, 9):  # Agents 2-8
            agent_id = f"Agent-{i}"
            self.agent_workloads[agent_id] = {
                "current_task": None,
                "completed_tasks": [],
                "total_hours_worked": 0.0,
                "availability": "available",
            }
            self.agent_skills[agent_id] = self._generate_agent_skills(agent_id)

    def _generate_agent_skills(self, agent_id: str) -> List[str]:
        """Generate skills for each agent"""
        all_skills = [
            "git",
            "code_analysis",
            "optimization",
            "documentation",
            "markdown",
            "api_docs",
            "debugging",
            "testing",
            "feature_development",
            "performance_analysis",
            "profiling",
            "test_automation",
            "coverage_analysis",
            "code_review",
            "refactoring",
            "architecture",
            "dependency_management",
            "compatibility_testing",
            "security_analysis",
            "vulnerability_assessment",
            "security_fixes",
        ]

        # Each agent gets 5-8 random skills
        num_skills = random.randint(5, 8)
        return random.sample(all_skills, num_skills)

    def find_best_task_for_agent(
        self, agent_id: str, available_tasks: List["DevelopmentTask"]
    ) -> Optional["DevelopmentTask"]:
        """Find the best matching task for an agent based on skills and preferences"""
        if agent_id not in self.agent_skills:
            self.logger.warning(f"Agent {agent_id} not found in skills registry")
            return None

        agent_skills = self.agent_skills[agent_id]

        # Score tasks based on skill match and priority
        scored_tasks = []
        for task in available_tasks:
            skill_match = len(set(agent_skills) & set(task.required_skills))
            priority_score = task.priority
            complexity_bonus = (
                2
                if task.complexity == "medium"
                else 3
                if task.complexity == "high"
                else 1
            )

            total_score = (skill_match * 10) + priority_score + complexity_bonus
            scored_tasks.append((task, total_score))

        # Return highest scoring task
        if scored_tasks:
            scored_tasks.sort(key=lambda x: x[1], reverse=True)
            return scored_tasks[0][0]

        return None

    def get_agent_skills(self, agent_id: str) -> List[str]:
        """Get skills for a specific agent"""
        return self.agent_skills.get(agent_id, [])

    def update_agent_workload(self, agent_id: str, task_id: str, action: str):
        """Update agent workload when tasks are claimed, started, or completed"""
        if agent_id not in self.agent_workloads:
            self.logger.warning(f"Agent {agent_id} not found in workload registry")
            return

        if action == "claim":
            self.agent_workloads[agent_id]["current_task"] = task_id
            self.agent_workloads[agent_id]["availability"] = "busy"
        elif action == "start":
            # Task started, workload remains the same
            pass
        elif action == "complete":
            completed_task = self.agent_workloads[agent_id]["current_task"]
            if completed_task:
                self.agent_workloads[agent_id]["completed_tasks"].append(completed_task)
                self.agent_workloads[agent_id]["current_task"] = None
                self.agent_workloads[agent_id]["availability"] = "available"
        elif action == "release":
            self.agent_workloads[agent_id]["current_task"] = None
            self.agent_workloads[agent_id]["availability"] = "available"

    def get_agent_availability(self, agent_id: str) -> str:
        """Get current availability status of an agent"""
        return self.agent_workloads.get(agent_id, {}).get("availability", "unknown")

    def get_agent_workload_summary(self, agent_id: str) -> Dict[str, Any]:
        """Get workload summary for a specific agent"""
        if agent_id not in self.agent_workloads:
            return {}

        workload = self.agent_workloads[agent_id]
        return {
            "current_task": workload["current_task"],
            "completed_tasks_count": len(workload["completed_tasks"]),
            "total_hours_worked": workload["total_hours_worked"],
            "availability": workload["availability"],
            "skills": self.agent_skills.get(agent_id, []),
        }

    def get_all_agents_summary(self) -> Dict[str, Dict[str, Any]]:
        """Get workload summary for all agents"""
        summary = {}
        for agent_id in self.agent_workloads:
            summary[agent_id] = self.get_agent_workload_summary(agent_id)
        return summary

    def add_agent_skill(self, agent_id: str, skill: str):
        """Add a new skill to an agent"""
        if agent_id not in self.agent_skills:
            self.agent_skills[agent_id] = []
        
        if skill not in self.agent_skills[agent_id]:
            self.agent_skills[agent_id].append(skill)
            self.logger.info(f"Added skill '{skill}' to {agent_id}")

    def remove_agent_skill(self, agent_id: str, skill: str):
        """Remove a skill from an agent"""
        if agent_id in self.agent_skills and skill in self.agent_skills[agent_id]:
            self.agent_skills[agent_id].remove(skill)
            self.logger.info(f"Removed skill '{skill}' from {agent_id}")

    def get_agents_by_skill(self, skill: str) -> List[str]:
        """Get list of agents that have a specific skill"""
        agents_with_skill = []
        for agent_id, skills in self.agent_skills.items():
            if skill in skills:
                agents_with_skill.append(agent_id)
        return agents_with_skill

    def get_agent_task_compatibility_score(
        self, agent_id: str, task: "DevelopmentTask"
    ) -> float:
        """Calculate compatibility score between agent and task (0.0 to 1.0)"""
        if agent_id not in self.agent_skills:
            return 0.0

        agent_skills = set(self.agent_skills[agent_id])
        required_skills = set(task.required_skills)
        
        if not required_skills:
            return 1.0

        skill_match = len(agent_skills & required_skills)
        total_required = len(required_skills)
        
        return skill_match / total_required if total_required > 0 else 0.0

    def get_optimal_task_assignment(
        self, available_tasks: List["DevelopmentTask"]
    ) -> Dict[str, str]:
        """Get optimal task assignment for all available agents"""
        assignments = {}
        available_agents = [
            agent_id for agent_id in self.agent_workloads 
            if self.agent_workloads[agent_id]["availability"] == "available"
        ]

        # Sort tasks by priority (highest first)
        sorted_tasks = sorted(available_tasks, key=lambda t: t.priority, reverse=True)
        
        # Sort agents by skill diversity (most skills first)
        sorted_agents = sorted(
            available_agents, 
            key=lambda a: len(self.agent_skills.get(a, [])), 
            reverse=True
        )

        for task in sorted_tasks:
            best_agent = None
            best_score = 0.0

            for agent_id in sorted_agents:
                if agent_id in assignments.values():
                    continue  # Agent already assigned

                score = self.get_agent_task_compatibility_score(agent_id, task)
                if score > best_score:
                    best_score = score
                    best_agent = agent_id

            if best_agent and best_score > 0.3:  # Minimum compatibility threshold
                assignments[task.task_id] = best_agent

        return assignments
