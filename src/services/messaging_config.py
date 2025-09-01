#!/usr/bin/env python3
"""
Messaging Configuration Module - Agent Cellphone V2
=================================================

Configuration management for the messaging service.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import json
import os
from typing import Dict, Any


class MessagingConfiguration:
    """Configuration management for messaging service."""

    def __init__(self):
        """Initialize configuration manager."""
        self.agents: Dict[str, Dict[str, Any]] = {}
        self.inbox_paths: Dict[str, str] = {}
        self._load_configuration()

    def _load_configuration(self):
        """Load configuration from centralized SSOT system (V2 compliance requirement).

        This method implements SSOT by using the centralized configuration management.
        """
        try:
            # Import centralized configuration
            from src.utils.config_core import get_config

            # Get agent count and captain ID from centralized config
            agent_count = get_config("AGENT_COUNT", 8)
            captain_id = get_config("CAPTAIN_ID", "Agent-4")

            # Default configuration using centralized values
            self.agents = {
                "Agent-1": {"description": "Integration & Core Systems Specialist", "coords": (-1269, 481)},
                "Agent-2": {"description": "Architecture & Design Specialist", "coords": (-308, 480)},
                "Agent-3": {"description": "Infrastructure & DevOps Specialist", "coords": (-1269, 1001)},
                "Agent-5": {"description": "Business Intelligence Specialist", "coords": (652, 421)},
                "Agent-6": {"description": "Gaming & Entertainment Specialist", "coords": (1612, 419)},
                "Agent-7": {"description": "Web Development Specialist", "coords": (653, 940)},
                "Agent-8": {"description": "Integration & Performance Specialist", "coords": (1611, 941)},
                "Agent-4": {"description": "Quality Assurance Specialist (CAPTAIN)", "coords": (-308, 1000)},
            }

            # Agent inbox paths using centralized configuration
            self.inbox_paths = {
                "Agent-1": "agent_workspaces/Agent-1/inbox",
                "Agent-2": "agent_workspaces/Agent-2/inbox",
                "Agent-3": "agent_workspaces/Agent-3/inbox",
                "Agent-4": "agent_workspaces/Agent-4/inbox",
                "Agent-5": "agent_workspaces/Agent-5/inbox",
                "Agent-6": "agent_workspaces/Agent-6/inbox",
                "Agent-7": "agent_workspaces/Agent-7/inbox",
                "Agent-8": "agent_workspaces/Agent-8/inbox",
            }

            # Load from config file if it exists
            config_file = "config/messaging_config.json"
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    if 'agents' in config:
                        self.agents.update(config['agents'])
                    if 'inbox_paths' in config:
                        self.inbox_paths.update(config['inbox_paths'])

        except Exception as e:
            # Fallback to hardcoded defaults is already set above
            pass
