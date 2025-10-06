#!/usr/bin/env python3
"""
Discord Commander Web Controller - Main Interface
=================================================

Main interface for Discord Commander web controller system.
V2 Compliant: ≤100 lines, imports from modular components.

Web-based interface for controlling the Discord Commander system.
Provides an interactive dashboard for managing agents and sending messages.

Features:
- Real-time agent status monitoring
- Interactive message sending interface
- Swarm coordination tools
- System health monitoring
- Rich web interface with real-time updates

Usage:
    python web_controller.py
    from src.services.discord_commander.web_controller import DiscordCommanderController
"""

# Import main components from modular files
from .web_controller_core import DiscordCommanderController
from .web_controller_templates import create_default_templates

# Re-export main class for backward compatibility
__all__ = [
    "DiscordCommanderController",
    "create_default_templates",
]


if __name__ == "__main__":
    # Create templates if they don't exist
    create_default_templates()

    # Start the controller
    controller = DiscordCommanderController()
    controller.run()
