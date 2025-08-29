from typing import List

from __future__ import annotations
from dataclasses import dataclass


"""Shared agent utilities and constants."""


# Type alias for agent capability identifiers
AgentCapability = str


@dataclass
class AgentInfo:
    """Basic information about a registered agent."""

    capabilities: List[AgentCapability]
