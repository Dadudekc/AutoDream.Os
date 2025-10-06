#!/usr/bin/env python3
"""
Discord Server Manager - Main Interface
=======================================

Main interface for Discord server management system.
V2 Compliant: ≤100 lines, imports from modular components.

Comprehensive Discord server management tool for AI assistant control.
Allows AI to manage Discord server, channels, permissions, members, roles, etc.

Features:
- Channel management (create, delete, modify)
- Role management (create, assign, modify permissions)
- Member management (kick, ban, mute, etc.)
- Permission management
- Server settings configuration
- Message management
- Webhook management
- Server audit and monitoring

Usage:
    python discord_server_manager.py --help
    python discord_server_manager.py server-info
    python discord_server_manager.py list-channels
    python discord_server_manager.py create-channel --name "new-channel" --type text
    python discord_server_manager.py manage-roles --action list

Author: Agent-7 (Implementation Specialist)
License: MIT
"""

# Import main components from modular files
from .server_manager_core import DiscordServerManager, main

# Re-export main class for backward compatibility
__all__ = [
    "DiscordServerManager",
    "main",
]


if __name__ == "__main__":
    import sys

    success = main()
    sys.exit(0 if success else 1)
