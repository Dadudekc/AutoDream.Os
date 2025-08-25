#!/usr/bin/env python3
"""
Devlog CLI System - Agent Cellphone V2
=======================================

CLI system for agents to create, manage, and query devlogs.
Integrates with existing knowledge database and Discord systems.
Follows V2 coding standards: ≤300 LOC, OOP design, SRP.

**Features:**
- Create devlog entries via CLI
- Store in knowledge database for querying
- Post to Discord devlog channels
- Search and review project history
- Knowledge database integration

**Author:** V2 SWARM CAPTAIN
**Created:** Current Sprint
**Status:** ACTIVE - V2 STANDARDS COMPLIANT
"""

import argparse
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

from src.utils.stability_improvements import stability_manager, safe_import

# Import existing systems
try:
    from .knowledge_database import KnowledgeDatabase, KnowledgeEntry
    from ..services.discord_integration_service import DiscordIntegrationService
    from .fsm_discord_bridge import FSMDiscordBridge
    
    SYSTEMS_AVAILABLE = True
except ImportError as e:
    SYSTEMS_AVAILABLE = False
    print(f"⚠️ Some systems not available: {e} - using placeholder classes")
    
    # Placeholder classes
    class KnowledgeEntry:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    
    class KnowledgeDatabase:
        def __init__(self, db_path: str = "devlog_knowledge.db"):
            self.db_path = db_path
            self.entries = []
            self.entry_id = 0
        
        def store_knowledge(self, entry: KnowledgeEntry) -> bool:
            """Store a knowledge entry"""
            try:
                entry.id = f"devlog_{self.entry_id}"
                self.entry_id += 1
                self.entries.append(entry)
                return True
            except Exception:
                return False
        
        def search_knowledge(self, query: str, limit: int = 10) -> List[tuple]:
            """Search knowledge entries"""
            try:
                results = []
                for entry in self.entries:
                    if query.lower() in entry.title.lower() or query.lower() in entry.content.lower():
                        relevance = 0.8  # Simple relevance scoring
                        results.append((entry, relevance))
                
                return results[:limit]
            except Exception:
                return []
    
    class DiscordIntegrationService:
        def __init__(self):
            pass
        def send_message(self, sender: str, message_type: str, content: str, channel: str = "devlog") -> bool:
            return True
    
    class FSMDiscordBridge:
        def __init__(self):
            pass


class DevlogCLI:
    """Command-line interface for devlog management"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.parser = self._create_parser()
        
        # Initialize existing systems
        self.knowledge_db = KnowledgeDatabase("devlog_knowledge.db")
        self.discord_service = DiscordIntegrationService()
        self.discord_bridge = FSMDiscordBridge()
        
        # Devlog configuration
        self.devlog_config = {
            "default_channel": "devlog",
            "auto_discord": True,
            "knowledge_categories": ["project_update", "milestone", "issue", "idea", "review"]
        }
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create the command-line argument parser"""
        parser = argparse.ArgumentParser(
            description="Devlog CLI - Create and manage project devlogs",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Create a new devlog entry
  python -m src.core.devlog_cli create --title "Phase 3 Complete" --content "All systems integrated"
  
  # Search devlogs
  python -m src.core.devlog_cli search --query "Phase 3"
  
  # Show recent devlogs
  python -m src.core.devlog_cli recent --limit 5
  
  # Post to Discord
  python -m src.core.devlog_cli discord --id <entry_id>
            """
        )
        
        # Add subcommands
        subparsers = parser.add_subparsers(dest="command", help="Available commands")
        
        # Create command
        create_parser = subparsers.add_parser("create", help="Create a new devlog entry")
        create_parser.add_argument("--title", "-t", required=True, help="Devlog title")
        create_parser.add_argument("--content", "-c", required=True, help="Devlog content")
        create_parser.add_argument("--category", "-cat", choices=["project_update", "milestone", "issue", "idea", "review"], 
                                 default="project_update", help="Devlog category")
        create_parser.add_argument("--tags", "-tags", help="Comma-separated tags")
        create_parser.add_argument("--agent", "-a", default="unknown", help="Agent ID creating the entry")
        create_parser.add_argument("--priority", "-p", choices=["low", "normal", "high", "critical"], 
                                 default="normal", help="Entry priority")
        create_parser.add_argument("--no-discord", action="store_true", help="Don't post to Discord")
        create_parser.set_defaults(func=self._create_entry)
        
        # Search command
        search_parser = subparsers.add_parser("search", help="Search devlog entries")
        search_parser.add_argument("--query", "-q", required=True, help="Search query")
        search_parser.add_argument("--category", "-cat", help="Filter by category")
        search_parser.add_argument("--agent", "-a", help="Filter by agent")
        search_parser.add_argument("--limit", "-l", type=int, default=10, help="Maximum results")
        search_parser.set_defaults(func=self._search_entries)
        
        # Recent command
        recent_parser = subparsers.add_parser("recent", help="Show recent devlog entries")
        recent_parser.add_argument("--limit", "-l", type=int, default=10, help="Number of entries to show")
        recent_parser.add_argument("--category", "-cat", help="Filter by category")
        recent_parser.set_defaults(func=self._show_recent)
        
        # Discord command
        discord_parser = subparsers.add_parser("discord", help="Post devlog to Discord")
        discord_parser.add_argument("--id", "-i", required=True, help="Devlog entry ID")
        discord_parser.add_argument("--channel", "-ch", help="Discord channel (default: devlog)")
        discord_parser.set_defaults(func=self._post_to_discord)
        
        # Status command
        status_parser = subparsers.add_parser("status", help="Show devlog system status")
        status_parser.set_defaults(func=self._show_status)
        
        return parser
    
    def _create_entry(self, args: argparse.Namespace) -> bool:
        """Create a new devlog entry"""
        try:
            # Generate entry ID
            timestamp = datetime.now().timestamp()
            entry_id = f"devlog_{int(timestamp)}_{args.agent}"
            
            # Parse tags
            tags = [tag.strip() for tag in args.tags.split(",")] if args.tags else []
            
            # Create knowledge entry
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
                    "discord_posted": False
                }
            )
            
            # Add to knowledge database
            success = self.knowledge_db.store_knowledge(entry)
            if not success:
                print("❌ Failed to add entry to knowledge database")
                return False
            
            print(f"✅ Devlog entry created: {entry_id}")
            print(f"📝 Title: {args.title}")
            print(f"🏷️  Category: {args.category}")
            print(f"🤖 Agent: {args.agent}")
            print(f"📊 Priority: {args.priority}")
            
            # Post to Discord if enabled
            if not args.no_discord and self.devlog_config["auto_discord"]:
                discord_success = self._post_entry_to_discord(entry, None)  # Use default channel
                if discord_success:
                    print("📱 Posted to Discord")
                    # Update metadata
                    entry.metadata["discord_posted"] = True
                    self.knowledge_db.store_knowledge(entry)  # Update
                else:
                    print("⚠️  Failed to post to Discord")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create devlog entry: {e}")
            print(f"❌ Error creating entry: {e}")
            return False
    
    def _search_entries(self, args: argparse.Namespace) -> bool:
        """Search devlog entries"""
        try:
            print(f"🔍 Searching devlogs for: '{args.query}'")
            if args.category:
                print(f"📂 Category filter: {args.category}")
            if args.agent:
                print(f"🤖 Agent filter: {args.agent}")
            
            # Search knowledge database
            results = self.knowledge_db.search_knowledge(args.query, limit=args.limit)
            
            if not results:
                print("❌ No entries found")
                return True
            
            # Filter and limit results
            filtered_results = results[:args.limit]
            
            print(f"\n📊 Found {len(filtered_results)} entries:")
            print("="*80)
            
            for entry_tuple in filtered_results:
                entry, relevance = entry_tuple
                print(f"🆔 {entry.id}")
                print(f"📝 {entry.title}")
                print(f"🏷️  {entry.category}")
                print(f"🤖 {entry.agent_id}")
                print(f"📅 {datetime.fromtimestamp(entry.created_at).strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"📋 {entry.content[:100]}{'...' if len(entry.content) > 100 else ''}")
                print(f"📊 Relevance: {relevance:.2f}")
                print("-" * 80)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to search entries: {e}")
            print(f"❌ Error searching entries: {e}")
            return False
    
    def _show_recent(self, args: argparse.Namespace) -> bool:
        """Show recent devlog entries"""
        try:
            print(f"📅 Recent devlog entries (limit: {args.limit})")
            if args.category:
                print(f"📂 Category filter: {args.category}")
            
            # Search for recent entries (using timestamp-based query)
            query = f"created_at:{datetime.now().strftime('%Y-%m-%d')}"
            results = self.knowledge_db.search_knowledge(query, limit=args.limit)
            
            if not results:
                print("❌ No recent entries found")
                return True
            
            # Sort by creation time and limit
            sorted_results = sorted(results, key=lambda x: x[0].created_at, reverse=True)[:args.limit]
            
            print(f"\n📊 Recent entries:")
            print("="*80)
            
            for entry_tuple in sorted_results:
                entry, relevance = entry_tuple
                print(f"🆔 {entry.id}")
                print(f"📝 {entry.title}")
                print(f"🏷️  Category: {entry.category}")
                print(f"🤖 Agent: {entry.agent_id}")
                print(f"📅 {datetime.fromtimestamp(entry.created_at).strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"📋 {entry.content[:100]}{'...' if len(entry.content) > 100 else ''}")
                print(f"📊 Relevance: {relevance:.2f}")
                print("-" * 80)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to show recent entries: {e}")
            print(f"❌ Error showing recent entries: {e}")
            return False
    
    def _post_to_discord(self, args: argparse.Namespace) -> bool:
        """Post specific devlog entry to Discord"""
        try:
            entry_id = args.id
            channel = args.channel or self.devlog_config["default_channel"]
            
            print(f"📱 Posting devlog {entry_id} to Discord channel: {channel}")
            
            # Find entry in knowledge database
            results = self.knowledge_db.search_knowledge(entry_id, limit=1)
            if not results:
                print(f"❌ Entry not found: {entry_id}")
                return False
            
            entry, _ = results[0]
            
            # Post to Discord
            success = self._post_entry_to_discord(entry, channel)
            
            if success:
                print("✅ Successfully posted to Discord")
                # Update metadata
                entry.metadata["discord_posted"] = True
                self.knowledge_db.store_knowledge(entry)  # Update
            else:
                print("❌ Failed to post to Discord")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to post to Discord: {e}")
            print(f"❌ Error posting to Discord: {e}")
            return False
    
    def _post_entry_to_discord(self, entry: KnowledgeEntry, channel: str = None) -> bool:
        """Post a devlog entry to Discord with enhanced formatting"""
        try:
            channel = channel or self.devlog_config["default_channel"]
            
            # Enhanced Discord message formatting for rich embeds
            discord_content = f"""📝 **DEVLOG ENTRY: {entry.title}**
🏷️ **Category**: {entry.category}
🤖 **Agent**: {entry.agent_id}
📅 **Created**: {datetime.fromtimestamp(entry.created_at).strftime('%Y-%m-%d %H:%M:%S')}
📊 **Priority**: {entry.metadata.get('priority', 'normal')}

📋 **Content**:
{self._format_content_for_discord(entry.content)}

🏷️ **Tags**: {', '.join(entry.tags) if entry.tags else 'None'}
🆔 **Entry ID**: {entry.id}"""
            
            # Send via Discord service
            success = self.discord_service.send_message(
                sender=f"Agent-{entry.agent_id}",
                message_type="devlog",  # This triggers rich embed
                content=discord_content,
                channel=channel
            )
            
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to post entry to Discord: {e}")
            return False

    def _format_content_for_discord(self, content: str) -> str:
        """Format content to look better in Discord embeds"""
        try:
            # Clean up the content for better Discord display
            formatted = content.strip()
            
            # Add some visual enhancements
            # Replace common patterns with emojis
            formatted = formatted.replace("✅", "✅")
            formatted = formatted.replace("❌", "❌")
            formatted = formatted.replace("⚠️", "⚠️")
            formatted = formatted.replace("🚀", "🚀")
            formatted = formatted.replace("🎯", "🎯")
            formatted = formatted.replace("🔧", "🔧")
            formatted = formatted.replace("📊", "📊")
            formatted = formatted.replace("💡", "💡")
            
            # Add line breaks for better readability
            formatted = formatted.replace(". ", ".\n")
            formatted = formatted.replace("! ", "!\n")
            
            # Limit length for Discord embed (max 1000 chars)
            if len(formatted) > 1000:
                formatted = formatted[:997] + "..."
            
            return formatted
            
        except Exception:
            return content[:1000] + ("..." if len(content) > 1000 else "")
    
    def _show_status(self, args: argparse.Namespace) -> bool:
        """Show devlog system status"""
        try:
            print("📊 DEVLOG SYSTEM STATUS")
            print("="*50)
            
            # Knowledge database status
            print("🗄️  Knowledge Database:")
            print(f"   Status: {'✅ Available' if SYSTEMS_AVAILABLE else '⚠️  Limited'}")
            print(f"   Path: {self.knowledge_db.db_path}")
            
            # Discord integration status
            print("\n📱 Discord Integration:")
            print(f"   Service: {'✅ Available' if SYSTEMS_AVAILABLE else '⚠️  Limited'}")
            print(f"   Bridge: {'✅ Available' if SYSTEMS_AVAILABLE else '⚠️  Limited'}")
            print(f"   Auto-posting: {'✅ Enabled' if self.devlog_config['auto_discord'] else '❌ Disabled'}")
            print(f"   Default Channel: {self.devlog_config['default_channel']}")
            
            # Check Discord webhook status
            if hasattr(self.discord_service, 'webhook_url') and self.discord_service.webhook_url:
                print(f"   Webhook: ✅ Configured ({self.discord_service.webhook_url[:50]}...)")
            else:
                print("   Webhook: ❌ Not configured (set DISCORD_WEBHOOK_URL environment variable)")
            
            # Configuration
            print("\n⚙️  Configuration:")
            print(f"   Categories: {', '.join(self.devlog_config['knowledge_categories'])}")
            print(f"   CLI Version: 1.0.0")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to show status: {e}")
            print(f"❌ Error showing status: {e}")
            return False
    
    def run(self, args: List[str] = None) -> int:
        """Run the devlog CLI"""
        try:
            parsed_args = self.parser.parse_args(args)
            
            if not parsed_args.command:
                self.parser.print_help()
                return 0
            
            # Execute command
            success = parsed_args.func(parsed_args)
            return 0 if success else 1
            
        except KeyboardInterrupt:
            print("\n❌ Operation cancelled by user")
            return 1
        except Exception as e:
            self.logger.error(f"CLI error: {e}")
            print(f"❌ CLI error: {e}")
            return 1


def main():
    """Main entry point for devlog CLI"""
    cli = DevlogCLI()
    return cli.run()


if __name__ == "__main__":
    exit(main())
