#!/usr/bin/env python3
"""
Web Models - Data models for Discord Commander Web Controller
==========================================================

Data models extracted from web_controller.py for V2 compliance (≤400 lines).

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class AgentStatus:
    """Agent status data model."""

    agent_id: str
    status: str
    last_updated: str
    current_phase: str
    current_mission: str
    mission_priority: str
    current_tasks: list[str]
    completed_tasks: list[str]
    achievements: list[str]
    next_actions: list[str]
    coordinates: list[int]
    efficiency_score: float
    quality_score: float
    v2_compliance: bool


@dataclass
class SystemStatus:
    """System status data model."""

    timestamp: str
    total_agents: int
    active_agents: int
    inactive_agents: int
    total_tasks: int
    completed_tasks: int
    in_progress_tasks: int
    system_health: str
    messaging_service_status: str
    discord_bot_status: str
    quality_compliance_rate: float


@dataclass
class SocialMediaStatus:
    """Social media status data model."""

    platform: str
    status: str
    last_post: str | None
    posts_today: int
    engagement_rate: float
    followers_count: int
    is_active: bool


@dataclass
class MessageRequest:
    """Message request data model."""

    from_agent: str
    to_agent: str
    message: str
    priority: str
    message_type: str
    tags: list[str]
    timestamp: str


@dataclass
class SwarmCoordinateRequest:
    """Swarm coordinate request data model."""

    requesting_agent: str
    target_agents: list[str]
    action: str
    parameters: dict[str, Any]
    priority: str
    timestamp: str


@dataclass
class WebControllerConfig:
    """Web controller configuration data model."""

    host: str
    port: int
    debug: bool
    flask_available: bool
    socketio_enabled: bool
    auto_start: bool
    template_dir: str
    static_dir: str


@dataclass
class AgentWorkspaceInfo:
    """Agent workspace information data model."""

    agent_id: str
    workspace_path: str
    inbox_count: int
    outbox_count: int
    processed_count: int
    status_file_exists: bool
    working_tasks_count: int
    future_tasks_count: int
    last_status_update: str | None


@dataclass
class QualityMetrics:
    """Quality metrics data model."""

    total_files: int
    v2_compliant_files: int
    compliance_rate: float
    critical_violations: int
    file_size_violations: int
    function_count_violations: int
    class_count_violations: int
    last_quality_check: str


@dataclass
class CoordinationRequest:
    """Coordination request data model."""

    request_id: str
    from_agent: str
    to_agent: str
    request_type: str
    message: str
    priority: str
    timestamp: str
    acknowledged: bool
    responded: bool
    completed: bool
    response_time: float | None


@dataclass
class WebSocketEvent:
    """WebSocket event data model."""

    event_type: str
    data: dict[str, Any]
    timestamp: str
    source: str
    target: str | None


@dataclass
class TemplateData:
    """Template data model for web rendering."""

    title: str
    agents: list[AgentStatus]
    system_status: SystemStatus
    social_media_status: list[SocialMediaStatus]
    quality_metrics: QualityMetrics
    coordination_requests: list[CoordinationRequest]
    last_updated: str
