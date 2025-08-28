"""Shared constants for the status monitor service."""

# Default agent IDs monitored by the service
DEFAULT_AGENT_IDS = [
    "Agent-1",
    "Agent-2",
    "Agent-3",
    "Agent-4",
    "Agent-5",
]

# Health score adjustments
ERROR_PENALTY = 10
WARNING_PENALTY = 5
MIN_ACTIVE_AGENTS = 2
LOW_ACTIVE_AGENT_PENALTY = 20

# Status display helpers
STATUS_EMOJIS = {
    "active": "🟢",
    "standby": "🟡",
    "offline": "🔴",
}
