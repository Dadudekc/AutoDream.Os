#!/usr/bin/env python3
"""
Tests for Autonomous Development Agents Module
=============================================

Tests the agent coordination and management functionality for autonomous development.
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from src.autonomous_development.agents.coordinator import AgentCoordinator
# Use type hints with strings to avoid circular imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.autonomous_development.core import DevelopmentTask


class TestAgentCoordinator:
    """Test cases for AgentCoordinator"""

    @pytest.fixture
    def agent_coordinator(self):
        """Create an agent coordinator instance for testing"""
        return AgentCoordinator()

    @pytest.fixture
    def mock_task(self):
        """Create a mock development task"""
        task = Mock(spec=DevelopmentTask)
        task.task_id = "TASK-001"
        task.title = "Test Task"
        task.priority = 8
        task.complexity = "high"
        task.estimated_hours = 4.0
        task.required_skills = ["python", "testing", "debugging"]
        return task

    def test_init(self, agent_coordinator):
        """Test agent coordinator initialization"""
        assert agent_coordinator.agent_workloads is not None
        assert agent_coordinator.agent_skills is not None
        
        # Verify agents 2-8 were initialized
        for i in range(2, 9):
            agent_id = f"Agent-{i}"
            assert agent_id in agent_coordinator.agent_workloads
            assert agent_id in agent_coordinator.agent_skills

    def test_generate_agent_skills(self, agent_coordinator):
        """Test agent skill generation"""
        agent_id = "Agent-2"
        skills = agent_coordinator._generate_agent_skills(agent_id)
        
        # Verify skills were generated
        assert isinstance(skills, list)
        assert 5 <= len(skills) <= 8
        
        # Verify all skills are from the allowed list
        all_skills = [
            "git", "code_analysis", "optimization", "documentation", "markdown",
            "api_docs", "debugging", "testing", "feature_development",
            "performance_analysis", "profiling", "test_automation",
            "coverage_analysis", "code_review", "refactoring", "architecture",
            "dependency_management", "compatibility_testing", "security_analysis",
            "vulnerability_assessment", "security_fixes"
        ]
        
        for skill in skills:
            assert skill in all_skills

    def test_find_best_task_for_agent(self, agent_coordinator, mock_task):
        """Test finding best task for an agent"""
        available_tasks = [mock_task]
        
        # Test with Agent-2
        best_task = agent_coordinator.find_best_task_for_agent("Agent-2", available_tasks)
        
        # Should return the task since it's the only one available
        assert best_task is not None
        assert best_task.task_id == "TASK-001"

    def test_find_best_task_for_agent_no_match(self, agent_coordinator):
        """Test finding best task when no skills match"""
        # Create a task with skills that no agent has
        mock_task = Mock(spec=DevelopmentTask)
        mock_task.required_skills = ["nonexistent_skill"]
        mock_task.priority = 10
        mock_task.complexity = "high"
        
        available_tasks = [mock_task]
        
        # Test with Agent-2
        best_task = agent_coordinator.find_best_task_for_agent("Agent-2", available_tasks)
        
        # Should return None since no skills match
        assert best_task is None

    def test_find_best_task_for_agent_unknown_agent(self, agent_coordinator, mock_task):
        """Test finding best task for unknown agent"""
        available_tasks = [mock_task]
        
        # Test with unknown agent
        best_task = agent_coordinator.find_best_task_for_agent("Unknown-Agent", available_tasks)
        
        # Should return None for unknown agent
        assert best_task is None

    def test_get_agent_skills(self, agent_coordinator):
        """Test getting agent skills"""
        agent_id = "Agent-2"
        skills = agent_coordinator.get_agent_skills(agent_id)
        
        assert isinstance(skills, list)
        assert len(skills) > 0

    def test_get_agent_skills_unknown_agent(self, agent_coordinator):
        """Test getting skills for unknown agent"""
        skills = agent_coordinator.get_agent_skills("Unknown-Agent")
        assert skills == []

    def test_update_agent_workload_claim(self, agent_coordinator):
        """Test updating agent workload when claiming a task"""
        agent_id = "Agent-2"
        task_id = "TASK-001"
        
        # Initial state
        assert agent_coordinator.agent_workloads[agent_id]["current_task"] is None
        assert agent_coordinator.agent_workloads[agent_id]["availability"] == "available"
        
        # Claim task
        agent_coordinator.update_agent_workload(agent_id, task_id, "claim")
        
        # Verify state updated
        assert agent_coordinator.agent_workloads[agent_id]["current_task"] == task_id
        assert agent_coordinator.agent_workloads[agent_id]["availability"] == "busy"

    def test_update_agent_workload_complete(self, agent_coordinator):
        """Test updating agent workload when completing a task"""
        agent_id = "Agent-2"
        task_id = "TASK-001"
        
        # Set initial state
        agent_coordinator.agent_workloads[agent_id]["current_task"] = task_id
        agent_coordinator.agent_workloads[agent_id]["availability"] = "busy"
        
        # Complete task
        agent_coordinator.update_agent_workload(agent_id, task_id, "complete")
        
        # Verify state updated
        assert agent_coordinator.agent_workloads[agent_id]["current_task"] is None
        assert agent_coordinator.agent_workloads[agent_id]["availability"] == "available"
        assert task_id in agent_coordinator.agent_workloads[agent_id]["completed_tasks"]

    def test_update_agent_workload_release(self, agent_coordinator):
        """Test updating agent workload when releasing a task"""
        agent_id = "Agent-2"
        task_id = "TASK-001"
        
        # Set initial state
        agent_coordinator.agent_workloads[agent_id]["current_task"] = task_id
        agent_coordinator.agent_workloads[agent_id]["availability"] = "busy"
        
        # Release task
        agent_coordinator.update_agent_workload(agent_id, task_id, "release")
        
        # Verify state updated
        assert agent_coordinator.agent_workloads[agent_id]["current_task"] is None
        assert agent_coordinator.agent_workloads[agent_id]["availability"] == "available"

    def test_update_agent_workload_unknown_agent(self, agent_coordinator):
        """Test updating workload for unknown agent"""
        # Should not raise an error, just log warning
        agent_coordinator.update_agent_workload("Unknown-Agent", "TASK-001", "claim")

    def test_get_agent_availability(self, agent_coordinator):
        """Test getting agent availability"""
        agent_id = "Agent-2"
        availability = agent_coordinator.get_agent_availability(agent_id)
        
        assert availability == "available"

    def test_get_agent_availability_unknown_agent(self, agent_coordinator):
        """Test getting availability for unknown agent"""
        availability = agent_coordinator.get_agent_availability("Unknown-Agent")
        assert availability == "unknown"

    def test_get_agent_workload_summary(self, agent_coordinator):
        """Test getting agent workload summary"""
        agent_id = "Agent-2"
        summary = agent_coordinator.get_agent_workload_summary(agent_id)
        
        assert isinstance(summary, dict)
        assert "current_task" in summary
        assert "completed_tasks_count" in summary
        assert "total_hours_worked" in summary
        assert "availability" in summary
        assert "skills" in summary

    def test_get_agent_workload_summary_unknown_agent(self, agent_coordinator):
        """Test getting workload summary for unknown agent"""
        summary = agent_coordinator.get_agent_workload_summary("Unknown-Agent")
        assert summary == {}

    def test_get_all_agents_summary(self, agent_coordinator):
        """Test getting workload summary for all agents"""
        summary = agent_coordinator.get_all_agents_summary()
        
        assert isinstance(summary, dict)
        # Should have 7 agents (Agent-2 through Agent-8)
        assert len(summary) == 7
        
        for agent_id in summary:
            assert agent_id.startswith("Agent-")
            assert isinstance(summary[agent_id], dict)

    def test_add_agent_skill(self, agent_coordinator):
        """Test adding a skill to an agent"""
        agent_id = "Agent-2"
        new_skill = "new_skill"
        
        # Add skill
        agent_coordinator.add_agent_skill(agent_id, new_skill)
        
        # Verify skill was added
        assert new_skill in agent_coordinator.agent_skills[agent_id]

    def test_add_agent_skill_existing(self, agent_coordinator):
        """Test adding a skill that already exists"""
        agent_id = "Agent-2"
        existing_skill = agent_coordinator.agent_skills[agent_id][0]
        
        # Add existing skill
        agent_coordinator.add_agent_skill(agent_id, existing_skill)
        
        # Verify skill count didn't change
        original_count = len(agent_coordinator.agent_skills[agent_id])
        agent_coordinator.add_agent_skill(agent_id, existing_skill)
        assert len(agent_coordinator.agent_skills[agent_id]) == original_count

    def test_remove_agent_skill(self, agent_coordinator):
        """Test removing a skill from an agent"""
        agent_id = "Agent-2"
        existing_skill = agent_coordinator.agent_skills[agent_id][0]
        
        # Remove skill
        agent_coordinator.remove_agent_skill(agent_id, existing_skill)
        
        # Verify skill was removed
        assert existing_skill not in agent_coordinator.agent_skills[agent_id]

    def test_remove_agent_skill_nonexistent(self, agent_coordinator):
        """Test removing a skill that doesn't exist"""
        agent_id = "Agent-2"
        nonexistent_skill = "nonexistent_skill"
        
        # Remove nonexistent skill
        agent_coordinator.remove_agent_skill(agent_id, nonexistent_skill)
        
        # Should not raise error

    def test_get_agents_by_skill(self, agent_coordinator):
        """Test getting agents by skill"""
        # Get a skill that exists
        existing_skill = agent_coordinator.agent_skills["Agent-2"][0]
        
        agents_with_skill = agent_coordinator.get_agents_by_skill(existing_skill)
        
        assert isinstance(agents_with_skill, list)
        assert len(agents_with_skill) > 0
        assert "Agent-2" in agents_with_skill

    def test_get_agents_by_skill_nonexistent(self, agent_coordinator):
        """Test getting agents by nonexistent skill"""
        agents_with_skill = agent_coordinator.get_agents_by_skill("nonexistent_skill")
        
        assert isinstance(agents_with_skill, list)
        assert len(agents_with_skill) == 0

    def test_get_agent_task_compatibility_score(self, agent_coordinator, mock_task):
        """Test calculating agent-task compatibility score"""
        agent_id = "Agent-2"
        
        score = agent_coordinator.get_agent_task_compatibility_score(agent_id, mock_task)
        
        # Score should be between 0.0 and 1.0
        assert 0.0 <= score <= 1.0
        
        # Since Agent-2 has some skills that match the task, score should be > 0
        assert score > 0.0

    def test_get_agent_task_compatibility_score_no_skills(self, agent_coordinator):
        """Test compatibility score when task has no required skills"""
        agent_id = "Agent-2"
        mock_task = Mock(spec=DevelopmentTask)
        mock_task.required_skills = []
        
        score = agent_coordinator.get_agent_task_compatibility_score(agent_id, mock_task)
        
        # Should return 1.0 when no skills required
        assert score == 1.0

    def test_get_agent_task_compatibility_score_unknown_agent(self, agent_coordinator, mock_task):
        """Test compatibility score for unknown agent"""
        score = agent_coordinator.get_agent_task_compatibility_score("Unknown-Agent", mock_task)
        
        # Should return 0.0 for unknown agent
        assert score == 0.0

    def test_get_optimal_task_assignment(self, agent_coordinator):
        """Test optimal task assignment"""
        # Create mock tasks
        mock_tasks = [
            Mock(spec=DevelopmentTask, task_id="TASK-001", priority=8, complexity="high"),
            Mock(spec=DevelopmentTask, task_id="TASK-002", priority=5, complexity="medium"),
        ]
        
        # Mock the compatibility score method
        with patch.object(agent_coordinator, 'get_agent_task_compatibility_score') as mock_score:
            mock_score.return_value = 0.8  # High compatibility
            
            assignments = agent_coordinator.get_optimal_task_assignment(mock_tasks)
            
            # Should return assignments
            assert isinstance(assignments, dict)
            # Since all agents are available and have high compatibility, should get assignments
            assert len(assignments) > 0

    def test_get_optimal_task_assignment_no_available_agents(self, agent_coordinator):
        """Test optimal task assignment when no agents are available"""
        # Create mock tasks
        mock_tasks = [
            Mock(spec=DevelopmentTask, task_id="TASK-001", priority=8, complexity="high"),
        ]
        
        # Make all agents busy
        for agent_id in agent_coordinator.agent_workloads:
            agent_coordinator.agent_workloads[agent_id]["availability"] = "busy"
        
        assignments = agent_coordinator.get_optimal_task_assignment(mock_tasks)
        
        # Should return empty assignments
        assert assignments == {}


if __name__ == "__main__":
    pytest.main([__file__])
