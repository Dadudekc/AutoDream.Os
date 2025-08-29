from __future__ import annotations

import argparse
import logging

from .interfaces import MessagingMode
from .output_formatter import OutputFormatter
from .unified_messaging_service import UnifiedMessagingService
from .router import route_command
from .executor import CommandExecutor


logger = logging.getLogger(__name__)


class CommandHandler:
    """Wire together command parsing, routing and execution."""

    def __init__(self, formatter: OutputFormatter | None = None) -> None:
        service = UnifiedMessagingService()
        self.executor = CommandExecutor(service, formatter or OutputFormatter())
        logger.info("Messaging command handler initialized")

    def execute_command(self, args: argparse.Namespace) -> bool:
        """Route the command to the appropriate executor method."""
        try:
            mode = MessagingMode(args.mode)
            self.executor.service.set_mode(mode)
            action = route_command(args)
            if not action:
                return False
            handler = getattr(self.executor, action)
            return handler(args)
        except Exception as exc:  # pragma: no cover - defensive programming
            logger.error("Error executing command: %s", exc)
            return False
