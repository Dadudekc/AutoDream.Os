#!/usr/bin/env python3
"""
Knowledge CLI - Agent Cellphone V2
==================================

Command-line interface for the knowledge database system.
Extracted from monolithic knowledge_database.py for better modularity.

Follows V2 coding standards: ≤300 LOC, OOP design, SRP
"""

import click
import logging
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from datetime import datetime
from typing import List, Optional

from .knowledge_models import KnowledgeEntry, KnowledgeEntryBuilder
from .knowledge_storage import KnowledgeStorage
from .knowledge_search import KnowledgeSearch


class KnowledgeCLI:
    """Command-line interface for knowledge database operations"""
    
    def __init__(self, db_path: str = "knowledge_base.db"):
        self.console = Console()
        self.storage = KnowledgeStorage(db_path)
        self.search = KnowledgeSearch(db_path)
        self.logger = logging.getLogger(f"{__name__}.KnowledgeCLI")
    
    def display_entry(self, entry: KnowledgeEntry):
        """Display a knowledge entry in a formatted way"""
        # Create a rich panel for the entry
        content = f"""
[bold blue]Title:[/bold blue] {entry.title}
[bold green]Category:[/bold green] {entry.category}
[bold yellow]Tags:[/bold yellow] {', '.join(entry.tags) if entry.tags else 'None'}
[bold cyan]Source:[/bold cyan] {entry.source}
[bold magenta]Confidence:[/bold magenta] {entry.get_confidence_level()} ({entry.confidence:.2f})
[bold white]Agent:[/bold white] {entry.agent_id}
[bold white]Created:[/bold white] {datetime.fromtimestamp(entry.created_at).strftime('%Y-%m-%d %H:%M:%S')}
[bold white]Updated:[/bold white] {datetime.fromtimestamp(entry.updated_at).strftime('%Y-%m-%d %H:%M:%S')}
[bold white]Age:[/bold white] {entry.get_age_days():.1f} days

[bold white]Content:[/bold white]
{entry.content}

[bold white]Related Entries:[/bold white] {', '.join(entry.related_entries) if entry.related_entries else 'None'}
[bold white]Metadata:[/bold white] {entry.metadata}
        """
        
        panel = Panel(content, title=f"Knowledge Entry: {entry.id}", border_style="blue")
        self.console.print(panel)
    
    def display_search_results(self, results: List[tuple]):
        """Display search results in a formatted table"""
        if not results:
            self.console.print("[yellow]No search results found[/yellow]")
            return
        
        # Create a rich table for results
        table = Table(title="Search Results", show_header=True, header_style="bold magenta")
        table.add_column("Title", style="cyan", width=40)
        table.add_column("Category", style="green", width=15)
        table.add_column("Tags", style="yellow", width=20)
        table.add_column("Confidence", style="magenta", width=10)
        table.add_column("Relevance", style="blue", width=10)
        table.add_column("Age (days)", style="white", width=10)
        
        for entry, relevance in results:
            table.add_row(
                entry.title[:37] + "..." if len(entry.title) > 40 else entry.title,
                entry.category,
                ", ".join(entry.tags[:2]) + ("..." if len(entry.tags) > 2 else ""),
                f"{entry.confidence:.2f}",
                f"{relevance:.2f}",
                f"{entry.get_age_days():.1f}"
            )
        
        self.console.print(table)
    
    def display_statistics(self):
        """Display database statistics"""
        stats = self.storage.get_statistics()
        
        if not stats:
            self.console.print("[red]Failed to retrieve statistics[/red]")
            return
        
        # Create statistics display
        content = f"""
[bold blue]Database Statistics[/bold blue]

[bold green]Total Entries:[/bold green] {stats.get('total_entries', 0)}

[bold yellow]Entries by Category:[/bold yellow]
"""
        
        for category, count in stats.get('category_counts', {}).items():
            content += f"  {category}: {count}\n"
        
        content += f"""
[bold cyan]Entries by Agent:[/bold cyan]
"""
        
        for agent, count in stats.get('agent_counts', {}).items():
            content += f"  {agent}: {count}\n"
        
        content += f"""
[bold magenta]Average Confidence:[/bold magenta] {stats.get('average_confidence', 0.0)}
        """
        
        panel = Panel(content, title="Knowledge Database Statistics", border_style="green")
        self.console.print(panel)
    
    def add_entry_interactive(self):
        """Interactive entry creation"""
        self.console.print("[bold blue]Creating New Knowledge Entry[/bold blue]")
        
        try:
            # Get entry details interactively
            title = click.prompt("Title", type=str)
            content = click.prompt("Content", type=str)
            category = click.prompt("Category", type=str)
            tags_input = click.prompt("Tags (comma-separated)", type=str, default="")
            source = click.prompt("Source", type=str)
            agent_id = click.prompt("Agent ID", type=str)
            confidence = click.prompt("Confidence (0.0-1.0)", type=float, default=1.0)
            
            # Parse tags
            tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
            
            # Create entry using builder pattern
            entry = (KnowledgeEntryBuilder()
                    .with_title(title)
                    .with_content(content)
                    .with_category(category)
                    .with_tags(tags)
                    .with_source(source)
                    .with_agent_id(agent_id)
                    .with_confidence(confidence)
                    .build())
            
            # Store entry
            if self.storage.store_knowledge(entry):
                self.console.print(f"[green]Knowledge entry added successfully: {entry.id}[/green]")
                self.display_entry(entry)
            else:
                self.console.print("[red]Failed to add knowledge entry[/red]")
                
        except click.Abort:
            self.console.print("[yellow]Entry creation cancelled[/yellow]")
        except Exception as e:
            self.console.print(f"[red]Error creating entry: {e}[/red]")


# Click CLI commands
@click.group()
@click.option('--db-path', default='knowledge_base.db', help='Database file path')
@click.pass_context
def cli(ctx, db_path):
    """Knowledge Database CLI - Manage and search knowledge entries"""
    ctx.obj = {'cli': KnowledgeCLI(db_path)}


@cli.command()
@click.argument('title')
@click.argument('content')
@click.argument('category')
@click.argument('source')
@click.argument('agent_id')
@click.option('--tags', help='Comma-separated tags')
@click.option('--confidence', default=1.0, help='Confidence level (0.0-1.0)')
@click.option('--related', help='Comma-separated related entry IDs')
@click.pass_context
def add(ctx, title, content, category, source, agent_id, tags, confidence, related):
    """Add a new knowledge entry"""
    cli_obj = ctx.obj['cli']
    
    # Parse tags and related entries
    tag_list = [tag.strip() for tag in tags.split(',')] if tags else []
    related_list = [rel.strip() for rel in related.split(',')] if related else []
    
    # Create entry using builder pattern
    entry = (KnowledgeEntryBuilder()
            .with_title(title)
            .with_content(content)
            .with_category(category)
            .with_tags(tag_list)
            .with_source(source)
            .with_agent_id(agent_id)
            .with_confidence(confidence)
            .build())
    
    # Add related entries if specified
    for rel_id in related_list:
        entry.add_related_entry(rel_id)
    
    # Store entry
    if cli_obj.storage.store_knowledge(entry):
        cli_obj.console.print(f"[green]Knowledge entry added successfully: {entry.id}[/green]")
        cli_obj.display_entry(entry)
    else:
        cli_obj.console.print("[red]Failed to add knowledge entry[/red]")


@cli.command()
@click.argument('query')
@click.option('--limit', default=20, help='Maximum number of results')
@click.pass_context
def search(ctx, query, limit):
    """Search knowledge base"""
    cli_obj = ctx.obj['cli']
    results = cli_obj.search.search_knowledge(query, limit)
    cli_obj.display_search_results(results)


@cli.command()
@click.argument('category')
@click.option('--limit', default=50, help='Maximum number of results')
@click.pass_context
def category(ctx, category, limit):
    """Show knowledge entries by category"""
    cli_obj = ctx.obj['cli']
    entries = cli_obj.storage.get_knowledge_by_category(category, limit)
    
    if entries:
        cli_obj.console.print(f"[blue]Found {len(entries)} entries in category '{category}':[/blue]")
        for entry in entries:
            cli_obj.display_entry(entry)
    else:
        cli_obj.console.print(f"[yellow]No entries found in category '{category}'[/yellow]")


@cli.command()
@click.argument('agent_id')
@click.option('--limit', default=50, help='Maximum number of results')
@click.pass_context
def agent(ctx, agent_id, limit):
    """Show knowledge entries by agent"""
    cli_obj = ctx.obj['cli']
    entries = cli_obj.storage.get_knowledge_by_agent(agent_id, limit)
    
    if entries:
        cli_obj.console.print(f"[blue]Found {len(entries)} entries from agent '{agent_id}':[/blue]")
        for entry in entries:
            cli_obj.display_entry(entry)
    else:
        cli_obj.console.print(f"[yellow]No entries found from agent '{agent_id}'[/yellow]")


@cli.command()
@click.pass_context
def stats(ctx):
    """Show database statistics"""
    cli_obj = ctx.obj['cli']
    cli_obj.display_statistics()


@cli.command()
@click.argument('entry_id')
@click.pass_context
def show(ctx, entry_id):
    """Show a specific knowledge entry"""
    cli_obj = ctx.obj['cli']
    entry = cli_obj.storage.get_knowledge_by_id(entry_id)
    
    if entry:
        cli_obj.display_entry(entry)
    else:
        cli_obj.console.print(f"[yellow]Entry not found: {entry_id}[/yellow]")


@cli.command()
@click.pass_context
def interactive(ctx):
    """Interactive entry creation mode"""
    cli_obj = ctx.obj['cli']
    cli_obj.add_entry_interactive()


if __name__ == '__main__':
    cli()
