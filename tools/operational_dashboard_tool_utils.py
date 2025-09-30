#!/usr/bin/env python3
"""
Operational Dashboard Tool Utils
===============================

Utility functions and helper methods for operational dashboard.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

import json
import logging
from pathlib import Path
from typing import Any

from .operational_dashboard_tool_core import (
    AgentPerformance,
    AlertLevel,
    OperationalAlert,
    ProjectProgress,
    QualityGateResult,
)

logger = logging.getLogger(__name__)


def calculate_quality_score(numbers: list[int]) -> float:
    """Calculate quality score from a list of numbers."""
    if not numbers:
        return 0.0
    
    # Simple quality score calculation
    total = sum(numbers)
    if total == 0:
        return 100.0
    
    # Higher numbers = better quality
    max_possible = len(numbers) * 100
    return min(100.0, (total / max_possible) * 100)


def extract_metric(data: dict, key: str, default: float) -> float:
    """Extract metric value from data dictionary."""
    try:
        value = data.get(key, default)
        if isinstance(value, (int, float)):
            return float(value)
        elif isinstance(value, str):
            return float(value)
        else:
            return default
    except (ValueError, TypeError):
        logger.warning(f"Could not extract metric {key} from data")
        return default


def count_completed_tasks() -> int:
    """Count completed tasks from agent workspaces."""
    try:
        completed_count = 0
        agent_workspaces = Path("agent_workspaces")
        
        if not agent_workspaces.exists():
            return 0
        
        for agent_dir in agent_workspaces.iterdir():
            if agent_dir.is_dir():
                status_file = agent_dir / "status.json"
                if status_file.exists():
                    try:
                        with open(status_file, "r") as f:
                            status_data = json.load(f)
                            if "tasks_completed" in status_data:
                                completed_count += status_data["tasks_completed"]
                    except (json.JSONDecodeError, KeyError):
                        continue
        
        return completed_count
    except Exception as e:
        logger.warning(f"Could not count completed tasks: {e}")
        return 0


def count_total_tasks() -> int:
    """Count total tasks from agent workspaces."""
    try:
        total_count = 0
        agent_workspaces = Path("agent_workspaces")
        
        if not agent_workspaces.exists():
            return 0
        
        for agent_dir in agent_workspaces.iterdir():
            if agent_dir.is_dir():
                status_file = agent_dir / "status.json"
                if status_file.exists():
                    try:
                        with open(status_file, "r") as f:
                            status_data = json.load(f)
                            if "tasks_total" in status_data:
                                total_count += status_data["tasks_total"]
                    except (json.JSONDecodeError, KeyError):
                        continue
        
        return total_count
    except Exception as e:
        logger.warning(f"Could not count total tasks: {e}")
        return 0


def generate_recommendations(
    quality_score: float,
    violations: int,
    critical_issues: int,
    agent_performance: list[AgentPerformance],
) -> list[str]:
    """Generate operational recommendations."""
    recommendations = []
    
    if quality_score < 70:
        recommendations.append("Improve code quality - focus on V2 compliance")
    
    if violations > 50:
        recommendations.append("Address V2 compliance violations")
    
    if critical_issues > 0:
        recommendations.append("Resolve critical issues immediately")
    
    # Check agent performance
    inactive_agents = [agent for agent in agent_performance if agent.current_status == "inactive"]
    if len(inactive_agents) > 0:
        recommendations.append(f"Reactivate {len(inactive_agents)} inactive agents")
    
    # Check task completion rates
    total_tasks = sum(agent.tasks_completed + agent.tasks_failed for agent in agent_performance)
    if total_tasks > 0:
        completion_rate = sum(agent.tasks_completed for agent in agent_performance) / total_tasks
        if completion_rate < 0.8:
            recommendations.append("Improve task completion rates")
    
    if not recommendations:
        recommendations.append("System operating optimally")
    
    return recommendations


def load_v3_coordination_data() -> dict[str, Any]:
    """Load V3 coordination data from various sources."""
    try:
        data = {
            "timestamp": datetime.now().isoformat(),
            "v3_status": "active",
            "coordination_mode": "5-agent",
            "active_agents": ["Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"],
        }
        
        # Load from project analysis if available
        project_analysis = Path("project_analysis.json")
        if project_analysis.exists():
            try:
                with open(project_analysis, "r") as f:
                    analysis_data = json.load(f)
                    data.update(analysis_data)
            except (json.JSONDecodeError, KeyError):
                pass
        
        return data
    except Exception as e:
        logger.warning(f"Could not load V3 coordination data: {e}")
        return {"timestamp": datetime.now().isoformat(), "v3_status": "unknown"}


def load_quality_gate_data() -> QualityGateResult:
    """Load quality gate data."""
    try:
        # Try to load from quality gates output
        quality_file = Path("quality_gates_results.json")
        if quality_file.exists():
            with open(quality_file, "r") as f:
                quality_data = json.load(f)
                return QualityGateResult(
                    timestamp=quality_data.get("timestamp", datetime.now().isoformat()),
                    total_files=quality_data.get("total_files", 0),
                    compliant_files=quality_data.get("compliant_files", 0),
                    violations=quality_data.get("violations", 0),
                    quality_score=quality_data.get("quality_score", 0.0),
                    critical_issues=quality_data.get("critical_issues", 0),
                    recommendations=quality_data.get("recommendations", []),
                )
        
        # Fallback to default values
        return QualityGateResult(
            timestamp=datetime.now().isoformat(),
            total_files=0,
            compliant_files=0,
            violations=0,
            quality_score=0.0,
            critical_issues=0,
            recommendations=["Run quality gates to get current data"],
        )
    except Exception as e:
        logger.warning(f"Could not load quality gate data: {e}")
        return QualityGateResult(
            timestamp=datetime.now().isoformat(),
            total_files=0,
            compliant_files=0,
            violations=0,
            quality_score=0.0,
            critical_issues=0,
            recommendations=["Quality gate data unavailable"],
        )


def load_agent_performance_data() -> list[AgentPerformance]:
    """Load agent performance data."""
    try:
        performance_data = []
        agent_workspaces = Path("agent_workspaces")
        
        if not agent_workspaces.exists():
            return []
        
        for agent_dir in agent_workspaces.iterdir():
            if agent_dir.is_dir():
                agent_id = agent_dir.name
                status_file = agent_dir / "status.json"
                
                if status_file.exists():
                    try:
                        with open(status_file, "r") as f:
                            status_data = json.load(f)
                            
                        performance_data.append(AgentPerformance(
                            agent_id=agent_id,
                            tasks_completed=status_data.get("tasks_completed", 0),
                            tasks_failed=status_data.get("tasks_failed", 0),
                            average_cycle_time=status_data.get("average_cycle_time", 0.0),
                            quality_score=status_data.get("quality_score", 0.0),
                            last_active=status_data.get("last_active", "unknown"),
                            current_status=status_data.get("current_status", "unknown"),
                        ))
                    except (json.JSONDecodeError, KeyError):
                        # Create default performance data
                        performance_data.append(AgentPerformance(
                            agent_id=agent_id,
                            tasks_completed=0,
                            tasks_failed=0,
                            average_cycle_time=0.0,
                            quality_score=0.0,
                            last_active="unknown",
                            current_status="unknown",
                        ))
        
        return performance_data
    except Exception as e:
        logger.warning(f"Could not load agent performance data: {e}")
        return []


def load_project_progress_data() -> list[ProjectProgress]:
    """Load project progress data."""
    try:
        progress_data = []
        
        # Load from project analysis
        project_analysis = Path("project_analysis.json")
        if project_analysis.exists():
            try:
                with open(project_analysis, "r") as f:
                    analysis_data = json.load(f)
                    
                # Extract project information
                total_files = analysis_data.get("total_files", 0)
                compliant_files = analysis_data.get("compliant_files", 0)
                completion_percentage = (compliant_files / total_files * 100) if total_files > 0 else 0
                
                progress_data.append(ProjectProgress(
                    project_name="V2_SWARM",
                    completion_percentage=completion_percentage,
                    tasks_completed=compliant_files,
                    tasks_total=total_files,
                    last_update=analysis_data.get("timestamp", datetime.now().isoformat()),
                    status="active",
                ))
            except (json.JSONDecodeError, KeyError):
                pass
        
        # Add default project if none found
        if not progress_data:
            progress_data.append(ProjectProgress(
                project_name="V2_SWARM",
                completion_percentage=0.0,
                tasks_completed=0,
                tasks_total=0,
                last_update=datetime.now().isoformat(),
                status="unknown",
            ))
        
        return progress_data
    except Exception as e:
        logger.warning(f"Could not load project progress data: {e}")
        return []
