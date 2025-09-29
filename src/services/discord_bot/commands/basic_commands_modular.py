"""
Basic Commands Module - Modular Architecture
============================================
Clean, modular command setup using focused components.
"""

import logging

from src.services.discord_bot.core.security_manager import SecurityManager

from .help_command import setup_help_command
from .ping_command import setup_ping_command

logger = logging.getLogger(__name__)


def setup(bot):
    """Setup all basic commands using modular components."""
    logger.info("Setting up modular basic commands...")

    # Initialize shared components
    security_manager = SecurityManager(bot)

    # Setup individual commands
    setup_help_command(bot, security_manager)
    setup_ping_command(bot, security_manager)

    logger.info("✅ Modular basic commands setup complete")
