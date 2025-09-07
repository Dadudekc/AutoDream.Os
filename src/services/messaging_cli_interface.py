"""Command-line interface entry for messaging service."""

from __future__ import annotations

import logging
from typing import Optional

from .parser import create_parser
from .command_handler import CommandHandler
from .output_formatter import OutputFormatter

logger = logging.getLogger(__name__)


class MessagingCLI:
    """Parse arguments and delegate execution to the command handler."""

    def __init__(self, formatter: Optional[OutputFormatter] = None) -> None:
        self.parser = create_parser(None)
        self.handler = CommandHandler(formatter or OutputFormatter())
        self.service = self.handler.executor.service

    def run(self, argv: Optional[list[str]] = None) -> bool:
        try:
            args = self.parser.parse_args(argv)
            return self.handler.execute_command(args)
        except Exception as exc:  # pragma: no cover - defensive programming
            logger.error("Error running CLI: %s", exc)
            return False

    # The smoke tests expect a private helper for displaying help
    def _show_help(self) -> bool:
        """Display help information for the CLI."""
        self.parser.print_help()
        return True


if __name__ == "__main__":
    cli = MessagingCLI()
    cli.run()
