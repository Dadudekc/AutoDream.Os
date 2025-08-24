#!/usr/bin/env python3
"""
CLI Knowledge Database System - Agent Cellphone V2
==================================================

A comprehensive knowledge database system that agents can use via CLI to:
- Store and retrieve knowledge entries
- Search across multiple knowledge domains
- Maintain knowledge relationships and hierarchies
- Support agent learning and collaboration
- Provide intelligent querying and recommendations

Follows V2 coding standards: ≤300 LOC, OOP design, SRP
"""

import sqlite3
import json
import logging

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
import re

console = Console()


@dataclass
class KnowledgeEntry:
    """Represents a single knowledge entry"""

    id: str
    title: str
    content: str
    category: str
    tags: List[str]
    source: str
    confidence: float  # 0.0 to 1.0
    created_at: float
    updated_at: float
    agent_id: str
    related_entries: List[str]
    metadata: Dict[str, Any]


class KnowledgeDatabase:
    """Core knowledge database management system"""

    def __init__(self, db_path: str = "knowledge_base.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(f"{__name__}.KnowledgeDatabase")
        self.init_database()

    def init_database(self):
        """Initialize the knowledge database schema"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()

            # Main knowledge entries table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS knowledge_entries (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    category TEXT NOT NULL,
                    tags TEXT NOT NULL,
                    source TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    created_at REAL NOT NULL,
                    updated_at REAL NOT NULL,
                    agent_id TEXT NOT NULL,
                    related_entries TEXT NOT NULL,
                    metadata TEXT NOT NULL
                )
            """
            )

            # Knowledge relationships table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS knowledge_relationships (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entry_id TEXT NOT NULL,
                    related_id TEXT NOT NULL,
                    relationship_type TEXT NOT NULL,
                    strength REAL NOT NULL,
                    created_at REAL NOT NULL,
                    FOREIGN KEY (entry_id) REFERENCES knowledge_entries (id),
                    FOREIGN KEY (related_id) REFERENCES knowledge_entries (id)
                )
            """
            )

            # Search index table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS search_index (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entry_id TEXT NOT NULL,
                    search_text TEXT NOT NULL,
                    weight REAL NOT NULL,
                    FOREIGN KEY (entry_id) REFERENCES knowledge_entries (id)
                )
            """
            )

            # Create indexes for performance
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_category ON knowledge_entries (category)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_tags ON knowledge_entries (tags)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_agent ON knowledge_entries (agent_id)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_created ON knowledge_entries (created_at)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_search ON search_index (search_text)"
            )

            conn.commit()
            conn.close()
            self.logger.info(f"Knowledge database initialized: {self.db_path}")

        except Exception as e:
            self.logger.error(f"Database initialization failed: {e}")
            raise

    def store_knowledge(self, entry: KnowledgeEntry) -> bool:
        """Store a new knowledge entry"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT OR REPLACE INTO knowledge_entries
                (id, title, content, category, tags, source, confidence,
                 created_at, updated_at, agent_id, related_entries, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    entry.id,
                    entry.title,
                    entry.content,
                    entry.category,
                    json.dumps(entry.tags),
                    entry.source,
                    entry.confidence,
                    entry.created_at,
                    entry.updated_at,
                    entry.agent_id,
                    json.dumps(entry.related_entries),
                    json.dumps(entry.metadata),
                ),
            )

            # Update search index
            self._update_search_index(entry, cursor)

            conn.commit()
            conn.close()
            self.logger.info(f"Knowledge entry stored: {entry.id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to store knowledge entry: {e}")
            return False

    def _update_search_index(self, entry: KnowledgeEntry, cursor: sqlite3.Cursor):
        """Update search index for an entry"""
        # Remove old index entries
        cursor.execute("DELETE FROM search_index WHERE entry_id = ?", (entry.id,))

        # Create new index entries with weights
        search_texts = [
            (entry.title, 1.0),
            (entry.content, 0.8),
            (" ".join(entry.tags), 0.9),
            (entry.category, 0.7),
            (entry.source, 0.5),
        ]

        for text, weight in search_texts:
            if text:
                cursor.execute(
                    """
                    INSERT INTO search_index (entry_id, search_text, weight)
                    VALUES (?, ?, ?)
                """,
                    (entry.id, text.lower(), weight),
                )

    def search_knowledge(
        self, query: str, limit: int = 20
    ) -> List[Tuple[KnowledgeEntry, float]]:
        """Search knowledge base with relevance scoring"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()

            # Search across indexed content
            cursor.execute(
                """
                SELECT DISTINCT e.*, SUM(i.weight) as relevance
                FROM knowledge_entries e
                JOIN search_index i ON e.id = i.entry_id
                WHERE i.search_text LIKE ?
                GROUP BY e.id
                ORDER BY relevance DESC
                LIMIT ?
            """,
                (f"%{query.lower()}%", limit),
            )

            results = []
            for row in cursor.fetchall():
                entry = self._row_to_entry(row)
                relevance = row[-1] if row[-1] else 0.0
                results.append((entry, relevance))

            conn.close()
            return results

        except Exception as e:
            self.logger.error(f"Search failed: {e}")
            return []

    def get_knowledge_by_category(
        self, category: str, limit: int = 50
    ) -> List[KnowledgeEntry]:
        """Retrieve knowledge entries by category"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT * FROM knowledge_entries
                WHERE category = ?
                ORDER BY updated_at DESC
                LIMIT ?
            """,
                (category, limit),
            )

            entries = [self._row_to_entry(row) for row in cursor.fetchall()]
            conn.close()
            return entries

        except Exception as e:
            self.logger.error(f"Category retrieval failed: {e}")
            return []

    def get_knowledge_by_agent(
        self, agent_id: str, limit: int = 50
    ) -> List[KnowledgeEntry]:
        """Retrieve knowledge entries by agent"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT * FROM knowledge_entries
                WHERE agent_id = ?
                ORDER BY updated_at DESC
                LIMIT ?
            """,
                (agent_id, limit),
            )

            entries = [self._row_to_entry(row) for row in cursor.fetchall()]
            conn.close()
            return entries

        except Exception as e:
            self.logger.error(f"Agent retrieval failed: {e}")
            return []

    def _row_to_entry(self, row: Tuple) -> KnowledgeEntry:
        """Convert database row to KnowledgeEntry object"""
        return KnowledgeEntry(
            id=row[0],
            title=row[1],
            content=row[2],
            category=row[3],
            tags=json.loads(row[4]),
            source=row[5],
            confidence=row[6],
            created_at=row[7],
            updated_at=row[8],
            agent_id=row[9],
            related_entries=json.loads(row[10]),
            metadata=json.loads(row[11]),
        )

    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()

            # Total entries
            cursor.execute("SELECT COUNT(*) FROM knowledge_entries")
            total_entries = cursor.fetchone()[0]

            # Categories
            cursor.execute(
                "SELECT category, COUNT(*) FROM knowledge_entries GROUP BY category"
            )
            categories = dict(cursor.fetchall())

            # Agents
            cursor.execute(
                "SELECT agent_id, COUNT(*) FROM knowledge_entries GROUP BY agent_id"
            )
            agents = dict(cursor.fetchall())

            # Recent activity
            cursor.execute(
                """
                SELECT COUNT(*) FROM knowledge_entries
                WHERE updated_at > ?
            """,
                (datetime.now().timestamp() - 86400),
            )  # Last 24 hours
            recent_entries = cursor.fetchone()[0]

            conn.close()

            return {
                "total_entries": total_entries,
                "categories": categories,
                "agents": agents,
                "recent_entries": recent_entries,
            }

        except Exception as e:
            self.logger.error(f"Statistics retrieval failed: {e}")
            return {}


class KnowledgeCLI:
    """CLI interface for the knowledge database"""

    def __init__(self, db_path: str = "knowledge_base.db"):
        self.db = KnowledgeDatabase(db_path)
        self.console = Console()

    def display_entry(self, entry: KnowledgeEntry, show_metadata: bool = False):
        """Display a knowledge entry in a formatted way"""
        panel = Panel(
            f"[bold blue]{entry.title}[/bold blue]\n\n"
            f"[green]Category:[/green] {entry.category}\n"
            f"[green]Tags:[/green] {', '.join(entry.tags)}\n"
            f"[green]Source:[/green] {entry.source}\n"
            f"[green]Confidence:[/green] {entry.confidence:.2f}\n"
            f"[green]Agent:[/green] {entry.agent_id}\n"
            f"[green]Created:[/green] {datetime.fromtimestamp(entry.created_at).strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"[green]Updated:[/green] {datetime.fromtimestamp(entry.updated_at).strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"[yellow]Content:[/yellow]\n{entry.content}",
            title=f"Knowledge Entry: {entry.id}",
            border_style="blue",
        )
        self.console.print(panel)

        if show_metadata and entry.metadata:
            meta_panel = Panel(
                json.dumps(entry.metadata, indent=2),
                title="Metadata",
                border_style="green",
            )
            self.console.print(meta_panel)

    def display_search_results(self, results: List[Tuple[KnowledgeEntry, float]]):
        """Display search results in a table"""
        if not results:
            self.console.print("[yellow]No results found.[/yellow]")
            return

        table = Table(title="Search Results")
        table.add_column("ID", style="cyan")
        table.add_column("Title", style="blue")
        table.add_column("Category", style="green")
        table.add_column("Agent", style="yellow")
        table.add_column("Relevance", style="red")
        table.add_column("Updated", style="magenta")

        for entry, relevance in results:
            table.add_row(
                entry.id[:8],
                entry.title[:40] + "..." if len(entry.title) > 40 else entry.title,
                entry.category,
                entry.agent_id,
                f"{relevance:.2f}",
                datetime.fromtimestamp(entry.updated_at).strftime("%m-%d %H:%M"),
            )

        self.console.print(table)

    def display_statistics(self):
        """Display database statistics"""
        stats = self.db.get_statistics()

        # Main stats
        stats_panel = Panel(
            f"[bold blue]Knowledge Base Statistics[/bold blue]\n\n"
            f"[green]Total Entries:[/green] {stats.get('total_entries', 0)}\n"
            f"[green]Recent Entries (24h):[/green] {stats.get('recent_entries', 0)}\n\n"
            f"[yellow]Categories:[/yellow]\n"
            + "\n".join(
                [
                    f"  {cat}: {count}"
                    for cat, count in stats.get("categories", {}).items()
                ]
            )
            + "\n\n"
            f"[yellow]Agents:[/yellow]\n"
            + "\n".join(
                [
                    f"  {agent}: {count}"
                    for agent, count in stats.get("agents", {}).items()
                ]
            ),
            title="Database Statistics",
            border_style="blue",
        )
        self.console.print(stats_panel)


# CLI Commands
@click.group()
@click.option(
    "--db-path", default="knowledge_base.db", help="Path to knowledge database"
)
@click.pass_context
def cli(ctx, db_path):
    """CLI Knowledge Database for Agents"""
    ctx.ensure_object(dict)
    ctx.obj["cli"] = KnowledgeCLI(db_path)


@cli.command()
@click.option("--title", required=True, help="Knowledge entry title")
@click.option("--content", required=True, help="Knowledge entry content")
@click.option("--category", required=True, help="Knowledge category")
@click.option("--tags", help="Comma-separated tags")
@click.option("--source", required=True, help="Knowledge source")
@click.option(
    "--confidence", type=float, default=0.8, help="Confidence level (0.0-1.0)"
)
@click.option("--agent-id", required=True, help="Agent ID")
@click.option("--related", help="Comma-separated related entry IDs")
@click.pass_context
def add(ctx, title, content, category, tags, source, confidence, agent_id, related):
    """Add a new knowledge entry"""
    cli_obj = ctx.obj["cli"]

    # Generate unique ID
    entry_id = hashlib.sha256(f"{title}{content}{agent_id}".encode()).hexdigest()[:16]

    # Parse tags and related entries
    tag_list = [t.strip() for t in tags.split(",")] if tags else []
    related_list = [r.strip() for r in related.split(",")] if related else []

    # Create entry
    entry = KnowledgeEntry(
        id=entry_id,
        title=title,
        content=content,
        category=category,
        tags=tag_list,
        source=source,
        confidence=confidence,
        created_at=datetime.now().timestamp(),
        updated_at=datetime.now().timestamp(),
        agent_id=agent_id,
        related_entries=related_list,
        metadata={"cli_created": True},
    )

    if cli_obj.db.store_knowledge(entry):
        cli_obj.console.print(
            f"[green]Knowledge entry added successfully: {entry_id}[/green]"
        )
        cli_obj.display_entry(entry)
    else:
        cli_obj.console.print("[red]Failed to add knowledge entry[/red]")


@cli.command()
@click.argument("query")
@click.option("--limit", default=20, help="Maximum number of results")
@click.pass_context
def search(ctx, query, limit):
    """Search knowledge base"""
    cli_obj = ctx.obj["cli"]
    results = cli_obj.db.search_knowledge(query, limit)
    cli_obj.display_search_results(results)


@cli.command()
@click.argument("category")
@click.option("--limit", default=50, help="Maximum number of results")
@click.pass_context
def category(ctx, category, limit):
    """Show knowledge entries by category"""
    cli_obj = ctx.obj["cli"]
    entries = cli_obj.db.get_knowledge_by_category(category, limit)

    if entries:
        cli_obj.console.print(
            f"[blue]Found {len(entries)} entries in category '{category}':[/blue]"
        )
        for entry in entries:
            cli_obj.display_entry(entry)
    else:
        cli_obj.console.print(
            f"[yellow]No entries found in category '{category}'[/yellow]"
        )


@cli.command()
@click.argument("agent_id")
@click.option("--limit", default=50, help="Maximum number of results")
@click.pass_context
def agent(ctx, agent_id, limit):
    """Show knowledge entries by agent"""
    cli_obj = ctx.obj["cli"]
    entries = cli_obj.db.get_knowledge_by_agent(agent_id, limit)

    if entries:
        cli_obj.console.print(
            f"[blue]Found {len(entries)} entries from agent '{agent_id}':[/blue]"
        )
        for entry in entries:
            cli_obj.display_entry(entry)
    else:
        cli_obj.console.print(
            f"[yellow]No entries found from agent '{agent_id}'[/yellow]"
        )


@cli.command()
@click.pass_context
def stats(ctx):
    """Show database statistics"""
    cli_obj = ctx.obj["cli"]
    cli_obj.display_statistics()


@cli.command()
@click.argument("entry_id")
@click.pass_context
def show(ctx, entry_id):
    """Show a specific knowledge entry"""
    cli_obj = ctx.obj["cli"]
    # This would need a get_by_id method in the database class
    cli_obj.console.print(
        f"[yellow]Show command not yet implemented for ID: {entry_id}[/yellow]"
    )


if __name__ == "__main__":
    cli()
