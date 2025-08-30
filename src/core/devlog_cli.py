"""Command-line interface for project devlogs.

This module exposes :class:`DevlogCLI` which provides an entry point for
managing project devlogs from the command line.  The class delegates business
logic to :class:`~src.core.devlog_service.DevlogService` keeping this file
focused on argument parsing and high level orchestration.  Splitting the
implementation allows each module to remain well under the 300 line limit
mandated by V2 standards.
"""

from __future__ import annotations

from pathlib import Path
from typing import List
import argparse
import logging
import sys

# Ensure project root is on ``sys.path`` when executed directly.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from .devlog_service import DevlogService  # noqa: E402  (import after path fix)


class DevlogCLI:
    """High level command line interface for devlogs.

    The CLI is intentionally lightweight; it builds the argument parser and
    forwards execution to :class:`DevlogService`.  All side effects (database
    writes, Discord posts, etc.) are handled by the service to keep concerns
    separated and the codebase maintainable.
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.service = DevlogService()
        self.parser = self._create_parser()

    # ------------------------------------------------------------------
    # Parser construction
    # ------------------------------------------------------------------
    def _create_parser(self) -> argparse.ArgumentParser:
        """Build the top level argument parser and sub‑commands."""

        parser = argparse.ArgumentParser(
            description="Devlog CLI - SINGLE SOURCE OF TRUTH for team communication",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=(
                "Examples:\n"
                "  python -m src.core.devlog_cli create --title 'Phase 3 Complete' --content 'All systems integrated'\n"
                "  python -m src.core.devlog_cli search --query 'Phase 3'\n"
                "  python -m src.core.devlog_cli recent --limit 5\n"
                "  python -m src.core.devlog_cli status"
            ),
        )

        subparsers = parser.add_subparsers(dest="command", help="Available commands")

        # create -----------------------------------------------------------------
        create_p = subparsers.add_parser("create", help="Create a new devlog entry")
        create_p.add_argument("--title", "-t", required=True, help="Devlog title")
        create_p.add_argument("--content", "-c", required=True, help="Devlog content")
        create_p.add_argument("--agent", "-a", default="unknown", help="Agent ID")
        create_p.add_argument(
            "--category",
            "-cat",
            choices=["project_update", "milestone", "issue", "idea", "review"],
            default="project_update",
            help="Devlog category",
        )
        create_p.add_argument("--tags", "-tags", help="Comma separated tags")
        create_p.add_argument(
            "--priority",
            "-p",
            choices=["low", "normal", "high", "critical"],
            default="normal",
            help="Entry priority",
        )
        create_p.add_argument("--no-discord", action="store_true", help="Don't post to Discord")
        create_p.set_defaults(func=self.service.create_entry)

        # search -----------------------------------------------------------------
        search_p = subparsers.add_parser("search", help="Search devlog entries")
        search_p.add_argument("--query", "-q", required=True, help="Search query")
        search_p.add_argument("--category", "-cat", help="Filter by category")
        search_p.add_argument("--agent", "-a", help="Filter by agent")
        search_p.add_argument("--limit", "-l", type=int, default=10, help="Maximum results")
        search_p.set_defaults(func=self.service.search_entries)

        # recent -----------------------------------------------------------------
        recent_p = subparsers.add_parser("recent", help="Show recent devlog entries")
        recent_p.add_argument("--limit", "-l", type=int, default=5, help="Number of entries")
        recent_p.add_argument("--category", "-cat", help="Filter by category")
        recent_p.set_defaults(func=self.service.show_recent)

        # discord ----------------------------------------------------------------
        discord_p = subparsers.add_parser("discord", help="Post an entry to Discord")
        discord_p.add_argument("--id", "-i", required=True, help="Devlog entry ID")
        discord_p.add_argument("--channel", "-ch", help="Discord channel (default: devlog)")
        discord_p.set_defaults(func=self.service.post_to_discord)

        # status -----------------------------------------------------------------
        status_p = subparsers.add_parser("status", help="Show devlog system status")
        status_p.set_defaults(func=self.service.show_status)

        return parser

    # ------------------------------------------------------------------
    # Entry point
    # ------------------------------------------------------------------
    def run(self, args: List[str] | None = None) -> int:
        """Parse arguments and execute the requested command."""

        try:
            parsed = self.parser.parse_args(args)
            if not parsed.command:
                self.parser.print_help()
                return 0
            success = parsed.func(parsed)
            return 0 if success else 1
        except KeyboardInterrupt:
            print("\n❌ Operation cancelled by user")
            return 1
        except Exception as exc:  # pragma: no cover - defensive logging
            self.logger.error("CLI error: %s", exc)
            print(f"❌ CLI error: {exc}")
            return 1


def main() -> int:
    """Module entry point used by ``python -m src.core.devlog_cli``."""

    cli = DevlogCLI()
    return cli.run()


if __name__ == "__main__":  # pragma: no cover - manual execution
    raise SystemExit(main())

