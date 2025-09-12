from __future__ import annotations

import logging

logger = logging.getLogger(__name__)
"""Text-based dashboard demo for AutoDream OS.

Shows how agent status might be displayed."""
from enum import Enum


class AgentStatus(Enum):
    """Represents the possible statuses of an agent."""
    ONLINE = 'online'
    IDLE = 'idle'
    OFFLINE = 'offline'


def get_agent_status() ->dict[str, AgentStatus]:
    """Return a mapping of agent names to their statuses."""
    return {'Agent-1': AgentStatus.ONLINE, 'Agent-2': AgentStatus.IDLE,
        'Agent-3': AgentStatus.OFFLINE}


def display_dashboard() ->None:
    """Display a simple dashboard of agent statuses."""
    status = get_agent_status()
    logger.info('Agent Status Dashboard')
    for name, state in status.items():
        logger.info(f'{name}: {state.value}')


if __name__ == '__main__':
    display_dashboard()
