#!/usr/bin/env python3
"""
Web Utils - Utility functions for Discord Commander Web Controller
===============================================================

Utility functions extracted from web_controller.py for V2 compliance (≤400 lines).

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from .web_models import (
    AgentStatus,
    AgentWorkspaceInfo,
    QualityMetrics,
    SocialMediaStatus,
    SystemStatus,
    TemplateData,
)

logger = logging.getLogger(__name__)


def load_agent_status(agent_id: str) -> AgentStatus | None:
    """Load agent status from workspace."""
    try:
        status_path = Path(f"agent_workspaces/{agent_id}/status.json")
        if not status_path.exists():
            return None

        with open(status_path) as f:
            data = json.load(f)

        return AgentStatus(
            agent_id=data.get("agent_id", agent_id),
            status=data.get("status", "UNKNOWN"),
            last_updated=data.get("last_updated", ""),
            current_phase=data.get("current_phase", ""),
            current_mission=data.get("current_mission", ""),
            mission_priority=data.get("mission_priority", "NORMAL"),
            current_tasks=data.get("current_tasks", []),
            completed_tasks=data.get("completed_tasks", []),
            achievements=data.get("achievements", []),
            next_actions=data.get("next_actions", []),
            coordinates=data.get("coordinates", [0, 0]),
            efficiency_score=data.get("efficiency_score", 0.0),
            quality_score=data.get("quality_score", 0.0),
            v2_compliance=data.get("v2_compliance", False),
        )
    except Exception as e:
        logger.error(f"Error loading agent status for {agent_id}: {e}")
        return None


def load_all_agents() -> list[AgentStatus]:
    """Load status for all agents."""
    agents = []
    workspace_dir = Path("agent_workspaces")

    if not workspace_dir.exists():
        return agents

    for agent_dir in workspace_dir.iterdir():
        if agent_dir.is_dir() and agent_dir.name.startswith("Agent-"):
            agent_status = load_agent_status(agent_dir.name)
            if agent_status:
                agents.append(agent_status)

    return agents


def calculate_system_status(agents: list[AgentStatus]) -> SystemStatus:
    """Calculate overall system status."""
    active_agents = len([a for a in agents if a.status == "ACTIVE_AGENT_MODE"])
    inactive_agents = len(agents) - active_agents

    total_tasks = sum(len(a.current_tasks) for a in agents)
    completed_tasks = sum(len(a.completed_tasks) for a in agents)
    in_progress_tasks = total_tasks - completed_tasks

    # Calculate system health
    if active_agents == len(agents) and active_agents > 0:
        system_health = "EXCELLENT"
    elif active_agents >= len(agents) * 0.8:
        system_health = "GOOD"
    elif active_agents >= len(agents) * 0.5:
        system_health = "FAIR"
    else:
        system_health = "POOR"

    return SystemStatus(
        timestamp=datetime.now().isoformat(),
        total_agents=len(agents),
        active_agents=active_agents,
        inactive_agents=inactive_agents,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        in_progress_tasks=in_progress_tasks,
        system_health=system_health,
        messaging_service_status="Active",
        discord_bot_status="Active",
        quality_compliance_rate=0.895,  # From previous analysis
    )


def load_social_media_status() -> list[SocialMediaStatus]:
    """Load social media status information."""
    platforms = [
        SocialMediaStatus(
            platform="Discord",
            status="Active",
            last_post=datetime.now().isoformat(),
            posts_today=5,
            engagement_rate=0.85,
            followers_count=100,
            is_active=True,
        ),
        SocialMediaStatus(
            platform="Twitter",
            status="Inactive",
            last_post=None,
            posts_today=0,
            engagement_rate=0.0,
            followers_count=0,
            is_active=False,
        ),
    ]
    return platforms


def load_quality_metrics() -> QualityMetrics:
    """Load quality metrics from analysis."""
    return QualityMetrics(
        total_files=772,
        v2_compliant_files=691,
        compliance_rate=0.895,
        critical_violations=81,
        file_size_violations=6,
        function_count_violations=45,
        class_count_violations=12,
        last_quality_check=datetime.now().isoformat(),
    )


def get_agent_workspace_info(agent_id: str) -> AgentWorkspaceInfo:
    """Get agent workspace information."""
    workspace_path = f"agent_workspaces/{agent_id}"
    workspace_dir = Path(workspace_path)

    inbox_count = 0
    outbox_count = 0
    processed_count = 0
    working_tasks_count = 0
    future_tasks_count = 0

    if workspace_dir.exists():
        inbox_dir = workspace_dir / "inbox"
        outbox_dir = workspace_dir / "outbox"
        processed_dir = workspace_dir / "processed"

        if inbox_dir.exists():
            inbox_count = len(list(inbox_dir.glob("*")))
        if outbox_dir.exists():
            outbox_count = len(list(outbox_dir.glob("*")))
        if processed_dir.exists():
            processed_count = len(list(processed_dir.glob("*")))

        # Load task counts
        working_tasks_file = workspace_dir / "working_tasks.json"
        future_tasks_file = workspace_dir / "future_tasks.json"

        if working_tasks_file.exists():
            try:
                with open(working_tasks_file) as f:
                    data = json.load(f)
                    working_tasks_count = len(data.get("current_task", {}))
            except:
                pass

        if future_tasks_file.exists():
            try:
                with open(future_tasks_file) as f:
                    data = json.load(f)
                    future_tasks_count = len(data.get("available_tasks", []))
            except:
                pass

    status_file_exists = (workspace_dir / "status.json").exists()
    last_status_update = None

    if status_file_exists:
        try:
            with open(workspace_dir / "status.json") as f:
                data = json.load(f)
                last_status_update = data.get("last_updated")
        except:
            pass

    return AgentWorkspaceInfo(
        agent_id=agent_id,
        workspace_path=workspace_path,
        inbox_count=inbox_count,
        outbox_count=outbox_count,
        processed_count=processed_count,
        status_file_exists=status_file_exists,
        working_tasks_count=working_tasks_count,
        future_tasks_count=future_tasks_count,
        last_status_update=last_status_update,
    )


def create_template_data() -> TemplateData:
    """Create template data for web rendering."""
    agents = load_all_agents()
    system_status = calculate_system_status(agents)
    social_media_status = load_social_media_status()
    quality_metrics = load_quality_metrics()

    return TemplateData(
        title="Discord Commander Dashboard",
        agents=agents,
        system_status=system_status,
        social_media_status=social_media_status,
        quality_metrics=quality_metrics,
        coordination_requests=[],  # TODO: Load from coordination tracker
        last_updated=datetime.now().isoformat(),
    )


def validate_message_request(data: dict[str, Any]) -> bool:
    """Validate message request data."""
    required_fields = ["from_agent", "to_agent", "message"]
    return all(field in data for field in required_fields)


def format_agent_response(agent_status: AgentStatus) -> dict[str, Any]:
    """Format agent status for JSON response."""
    return {
        "agent_id": agent_status.agent_id,
        "status": agent_status.status,
        "last_updated": agent_status.last_updated,
        "current_phase": agent_status.current_phase,
        "current_mission": agent_status.current_mission,
        "mission_priority": agent_status.mission_priority,
        "current_tasks": agent_status.current_tasks,
        "completed_tasks": agent_status.completed_tasks,
        "achievements": agent_status.achievements,
        "next_actions": agent_status.next_actions,
        "coordinates": agent_status.coordinates,
        "efficiency_score": agent_status.efficiency_score,
        "quality_score": agent_status.quality_score,
        "v2_compliance": agent_status.v2_compliance,
    }
