"""Data service layer for portal API."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .portal_core import UnifiedPortal
from .enums import PortalSection


def get_status(portal: UnifiedPortal) -> Dict[str, Any]:
    """Return portal status information."""
    return portal.get_portal_status()


def get_agents(portal: UnifiedPortal) -> List[Dict[str, Any]]:
    """Return all agents as a list of dictionaries."""
    return [agent.to_dict() for agent in portal.agents.values()]


def get_agent(portal: UnifiedPortal, agent_id: str) -> Optional[Dict[str, Any]]:
    """Return a specific agent or None if not found."""
    agent = portal.get_agent_info(agent_id)
    return agent.to_dict() if agent else None


def get_navigation(portal: UnifiedPortal) -> Dict[str, Any]:
    """Return navigation state."""
    return portal.get_navigation_state()


def navigate_to(portal: UnifiedPortal, section: str) -> bool:
    """Navigate to a portal section."""
    try:
        portal_section = PortalSection(section)
        portal.navigate_to_section(portal_section)
        return True
    except ValueError:
        return False


def create_session(
    portal: UnifiedPortal, user_id: str, metadata: Dict[str, Any]
) -> str:
    """Create a new session and return its ID."""
    return portal.create_session(user_id, metadata)


def validate_session(portal: UnifiedPortal, session_id: str) -> bool:
    """Validate a session ID."""
    return portal.validate_session(session_id)


def terminate_session(portal: UnifiedPortal, session_id: str) -> bool:
    """Terminate a session by ID."""
    return portal.terminate_session(session_id)


def get_statistics(portal: UnifiedPortal) -> Dict[str, Any]:
    """Return portal statistics."""
    return portal.get_agent_statistics()
