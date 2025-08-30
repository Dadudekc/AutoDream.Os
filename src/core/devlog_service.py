"""Business logic for the devlog system.

The :class:`DevlogService` class encapsulates all operations for creating,
searching and publishing devlog entries.  It acts as the execution layer for
``DevlogCLI`` and can be reused programmatically by other modules.  Splitting
this code from the CLI keeps each module concise and easier to maintain.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import List
import argparse
import logging
import os

from .devlog_reporting import post_entry_to_discord, show_status

try:  # Optional integrations -------------------------------------------------
    from src.core.knowledge_database import KnowledgeDatabase, KnowledgeEntry
    from simple_discord import SimpleDiscordIntegration
    FSMDiscordBridge = None  # Not available, set to None
except Exception:  # pragma: no cover - fallback placeholders
    FSMDiscordBridge = None
    SimpleDiscordIntegration = None
    KnowledgeDatabase = None

    class KnowledgeEntry:  # minimal placeholder used for offline operation
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)


class DevlogService:
    """Core operations for devlog management."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

        db_path = Path("devlog_knowledge.db")
        if KnowledgeDatabase is not None:
            self.knowledge_db = KnowledgeDatabase(str(db_path))
            self.systems_available = True
        else:
            self.knowledge_db = self._create_placeholder_database(db_path)
            self.systems_available = False

        if SimpleDiscordIntegration is not None:
            try:
                self.discord_service = SimpleDiscordIntegration()
                self.discord_available = True
            except Exception:
                self.discord_service = None
                self.discord_available = False
        else:
            self.discord_service = None
            self.discord_available = False

        self.discord_bridge = FSMDiscordBridge() if FSMDiscordBridge else None

        self.devlog_config = {
            "default_channel": "devlog",
            "auto_discord": True,
            "knowledge_categories": ["project_update", "milestone", "issue", "idea", "review"],
            "ssot_enforced": True,
            "required_for_updates": True,
        }

    # ------------------------------------------------------------------
    def _create_placeholder_database(self, db_path: Path):
        class PlaceholderDatabase:
            def __init__(self, db_path: Path):
                self.db_path = Path(db_path)
                self.entries: List[KnowledgeEntry] = []
                self.entry_id = 0

            def store_knowledge(self, entry: KnowledgeEntry) -> bool:
                entry.id = f"devlog_{self.entry_id}"
                self.entry_id += 1
                self.entries.append(entry)
                return True

            def search_knowledge(self, query: str, limit: int = 10):
                results = []
                for entry in self.entries:
                    if query.lower() in entry.title.lower() or query.lower() in entry.content.lower():
                        results.append((entry, 0.8))
                return results[:limit]

        return PlaceholderDatabase(db_path)

    # ------------------------------------------------------------------
    def create_entry(self, args: argparse.Namespace) -> bool:
        """Create a new devlog entry."""

        try:
            timestamp = datetime.now().timestamp()
            entry_id = f"devlog_{int(timestamp)}_{args.agent}"
            tags = [t.strip() for t in args.tags.split(",")] if args.tags else []
            entry = KnowledgeEntry(
                id=entry_id,
                title=args.title,
                content=args.content,
                category=args.category,
                tags=tags,
                source=f"agent:{args.agent}",
                confidence=1.0,
                created_at=timestamp,
                updated_at=timestamp,
                agent_id=args.agent,
                related_entries=[],
                metadata={
                    "priority": args.priority,
                    "cli_created": True,
                    "discord_posted": False,
                    "ssot_enforced": True,
                },
            )

            if not self.knowledge_db.store_knowledge(entry):
                print("❌ Failed to add entry to knowledge database")
                return False

            if not args.no_discord and self.devlog_config["auto_discord"]:
                if post_entry_to_discord(entry, self.discord_service, self.devlog_config):
                    entry.metadata["discord_posted"] = True
                    self.knowledge_db.store_knowledge(entry)
                    print("📱 Posted to Discord")
                else:
                    print("⚠️  Failed to post to Discord")

            print(f"✅ Devlog entry created: {entry_id}")
            return True
        except Exception as exc:
            self.logger.error("Failed to create devlog entry: %s", exc)
            print(f"❌ Error creating entry: {exc}")
            return False

    # ------------------------------------------------------------------
    def search_entries(self, args: argparse.Namespace) -> bool:
        """Search stored devlog entries."""

        try:
            results = self.knowledge_db.search_knowledge(args.query, limit=args.limit)
            if not results:
                print("❌ No entries found")
                return True

            for entry, relevance in results[: args.limit]:
                print(f"🆔 {entry.id}")
                print(f"📝 {entry.title}")
                print(f"🏷️  {entry.category}")
                print(f"🤖 {entry.agent_id}")
                print(f"📅 {datetime.fromtimestamp(entry.created_at).strftime('%Y-%m-%d %H:%M:%S')}")
                preview = entry.content[:100] + ("..." if len(entry.content) > 100 else "")
                print(f"📋 {preview}")
                print(f"📊 Relevance: {relevance:.2f}")
                print("-" * 80)
            return True
        except Exception as exc:
            self.logger.error("Failed to search entries: %s", exc)
            print(f"❌ Error searching entries: {exc}")
            return False

    # ------------------------------------------------------------------
    def show_recent(self, args: argparse.Namespace) -> bool:
        """Display recent entries."""

        try:
            query = f"created_at:{datetime.now().strftime('%Y-%m-%d')}"
            results = self.knowledge_db.search_knowledge(query, limit=args.limit)
            if not results:
                print("❌ No recent entries found")
                return True

            for entry, relevance in sorted(results, key=lambda x: x[0].created_at, reverse=True)[: args.limit]:
                print(f"🆔 {entry.id}")
                print(f"📝 {entry.title}")
                print(f"🏷️  Category: {entry.category}")
                print(f"🤖 Agent: {entry.agent_id}")
                print(f"📅 {datetime.fromtimestamp(entry.created_at).strftime('%Y-%m-%d %H:%M:%S')}")
                preview = entry.content[:100] + ("..." if len(entry.content) > 100 else "")
                print(f"📋 {preview}")
                print(f"📊 Relevance: {relevance:.2f}")
                print("-" * 80)
            return True
        except Exception as exc:
            self.logger.error("Failed to show recent entries: %s", exc)
            print(f"❌ Error showing recent entries: {exc}")
            return False

    # ------------------------------------------------------------------
    def post_to_discord(self, args: argparse.Namespace) -> bool:
        """Post an existing entry to Discord."""

        try:
            results = self.knowledge_db.search_knowledge(args.id, limit=1)
            if not results:
                print(f"❌ Entry not found: {args.id}")
                return False

            entry, _ = results[0]
            channel = args.channel or self.devlog_config["default_channel"]
            if post_entry_to_discord(entry, self.discord_service, self.devlog_config, channel):
                print(f"✅ Entry posted to Discord channel: {channel}")
                return True
            print("❌ Failed to post to Discord")
            return False
        except Exception as exc:
            self.logger.error("Failed to post to Discord: %s", exc)
            print(f"❌ Error posting to Discord: {exc}")
            return False

    # ------------------------------------------------------------------
    def show_status(self, _: argparse.Namespace) -> bool:
        """Proxy to :func:`devlog_reporting.show_status`.``"""

        return show_status(
            self.knowledge_db,
            self.discord_service,
            self.devlog_config,
            self.systems_available,
            self.discord_available,
        )

