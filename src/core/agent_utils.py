from __future__ import annotations

"""Shared agent utilities and constants."""

from dataclasses import dataclass
from typing import List

# Type alias for agent capability identifiers
AgentCapability = str


@dataclass
class AgentInfo:
    """Basic information about a registered agent."""

    capabilities: List[AgentCapability]
