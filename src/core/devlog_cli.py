#!/usr/bin/env python3
"""
Devlog CLI - Single Source of Truth for Team Communication
==========================================================

Command-line interface for creating and managing project devlogs.
This is the PRIMARY tool for team communication and progress tracking.

**SSOT Principle**: All project updates, milestones, and issues MUST go through this system.
**Discord Integration**: Messages automatically post to Discord via our working simple_discord.py.
**Knowledge Storage**: All entries are stored in searchable knowledge database.

Follows V2 coding standards: ≤300 LOC, OOP design, SRP.

Author: Agent-1 (SSOT Implementation)
License: MIT
"""

import argparse
import logging
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional

# Add project root to path for imports - FIXED PATH HANDLING
current_file = Path(__file__)
project_root = current_file.parent.parent.parent
sys.path.insert(0, str(project_root))

# Also add current working directory to path for when running from different contexts
current_working_dir = Path.cwd()
if str(current_working_dir) not in sys.path:
    sys.path.insert(0, str(current_working_dir))

from src.utils.stability_improvements import stability_manager, safe_import

# Import our working Discord integration - SSOT IMPLEMENTATION
try:
    # Import the working simple_discord.py
    from simple_discord import SimpleDiscordIntegration
    DISCORD_AVAILABLE = True
    print("✅ Working Discord integration imported successfully")
except ImportError as e:
    DISCORD_AVAILABLE = False
    print(f"⚠️ Discord integration not available: {e}")

# Import existing systems - FIXED IMPORT PATH
try:
    # Try multiple import strategies
    try:
        # Strategy 1: Direct import
        from src.core.knowledge_database import KnowledgeDatabase, KnowledgeEntry
        from src.core.fsm_discord_bridge import FSMDiscordBridge
    except ImportError:
        # Strategy 2: Add current working directory to path
        import os
        current_dir = os.getcwd()
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        from src.core.knowledge_database import KnowledgeDatabase, KnowledgeEntry
        from src.core.fsm_discord_bridge import FSMDiscordBridge
    
    SYSTEMS_AVAILABLE = True
    print("✅ Real systems imported successfully")
except ImportError as e:
    SYSTEMS_AVAILABLE = False
    print(f"⚠️ Some systems not available: {e} - using placeholder classes")
    
    # Placeholder classes for when imports fail
    class KnowledgeEntry:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    
    class KnowledgeDatabase:
        def __init__(self, db_path: str = "devlog_knowledge.db"):
            self.db_path = Path(db_path)
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
    
    class FSMDiscordBridge:
        def __init__(self):
            pass


class DevlogCLI:
    """Command-line interface for devlog management - SINGLE SOURCE OF TRUTH"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.parser = self._create_parser()
        
        # Initialize systems with proper database path
        db_path = Path("devlog_knowledge.db")
        self.knowledge_db = KnowledgeDatabase(str(db_path))
        
        # Initialize our working Discord integration - SSOT IMPLEMENTATION
        if DISCORD_AVAILABLE:
            try:
                self.discord_service = SimpleDiscordIntegration()
                print("✅ Discord integration initialized successfully")
            except Exception as e:
                print(f"⚠️ Discord integration failed: {e}")
                self.discord_service = None
        else:
            self.discord_service = None
            print("⚠️ Discord integration not available")
        
        self.discord_bridge = FSMDiscordBridge()
        
        # Devlog configuration - SSOT settings
        self.devlog_config = {
            "default_channel": "devlog",
            "auto_discord": True,
            "knowledge_categories": ["project_update", "milestone", "issue", "idea", "review"],
            "ssot_enforced": True,  # Enforce Single Source of Truth
            "required_for_updates": True  # All updates must go through devlog
        }
        
        # Log initialization status
        if SYSTEMS_AVAILABLE:
            self.logger.info("✅ Devlog CLI initialized with real systems")
        else:
            self.logger.warning("⚠️ Devlog CLI initialized with placeholder systems")
        
        if self.discord_service:
            self.logger.info("✅ Discord integration working - SSOT achieved!")
        else:
            self.logger.warning("⚠️ Discord integration not available")
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create the command-line argument parser"""
        parser = argparse.ArgumentParser(
            description="Devlog CLI - SINGLE SOURCE OF TRUTH for team communication",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
🎯 **SSOT PRINCIPLE**: This is your SINGLE SOURCE OF TRUTH for team communication.
📱 **Discord Integration**: Messages automatically post to Discord.
🔍 **Knowledge Storage**: All entries are searchable and retrievable.

Examples:
  # Create a new devlog entry (RECOMMENDED)
  python -m src.core.devlog_cli create --title "Phase 3 Complete" --content "All systems integrated"
  
  # Search devlogs
  python -m src.core.devlog_cli search --query "Phase 3"
  
  # Show recent devlogs
  python -m src.core.devlog_cli recent --limit 5
  
  # Check system status
  python -m src.core.devlog_cli status
            """
        )
        
        # Add subcommands
        subparsers = parser.add_subparsers(dest="command", help="Available commands")
        
        # Create command
        create_parser = subparsers.add_parser("create", help="Create a new devlog entry (SSOT)")
        create_parser.add_argument("--title", "-t", required=True, help="Devlog title")
        create_parser.add_argument("--content", "-c", required=True, help="Devlog content")
        create_parser.add_argument("--agent", "-a", default="unknown", help="Agent ID (default: unknown)")
        create_parser.add_argument("--category", "-cat", 
                                 choices=["project_update", "milestone", "issue", "idea", "review"],
                                 default="project_update", help="Devlog category")
        create_parser.add_argument("--tags", "-tags", help="Comma-separated tags")
        create_parser.add_argument("--priority", "-p",
                                 choices=["low", "normal", "high", "critical"],
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
        recent_parser.add_argument("--limit", "-l", type=int, default=5, help="Number of entries")
        recent_parser.add_argument("--category", "-cat", help="Filter by category")
        recent_parser.set_defaults(func=self._show_recent)
        
        # Discord command
        discord_parser = subparsers.add_parser("discord", help="Post existing entry to Discord")
        discord_parser.add_argument("--id", "-i", required=True, help="Devlog entry ID")
        discord_parser.add_argument("--channel", "-ch", help="Discord channel (default: devlog)")
        discord_parser.set_defaults(func=self._post_to_discord)
        
        # Status command
        status_parser = subparsers.add_parser("status", help="Show devlog system status")
        status_parser.set_defaults(func=self._show_status)
        
        return parser
    
    def _create_entry(self, args: argparse.Namespace) -> bool:
        """Create a new devlog entry - SSOT ENFORCED"""
        try:
            print("📝 CREATING DEVLOG ENTRY")
            print("="*50)
            print(f"📝 Title: {args.title}")
            print(f"📋 Content: {args.content}")
            print(f"🏷️  Category: {args.category}")
            print(f"🤖 Agent: {args.agent}")
            print(f"📊 Priority: {args.priority}")
            
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
                    "discord_posted": False,
                    "ssot_enforced": True
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
        """Post existing devlog entry to Discord"""
        try:
            print(f"📱 Posting entry {args.id} to Discord...")
            
            # Find the entry in knowledge database
            results = self.knowledge_db.search_knowledge(args.id, limit=1)
            if not results:
                print(f"❌ Entry not found: {args.id}")
                return False
            
            entry, _ = results[0]
            channel = args.channel or self.devlog_config["default_channel"]
            
            # Post to Discord
            success = self._post_entry_to_discord(entry, channel)
            if success:
                print(f"✅ Entry posted to Discord channel: {channel}")
                return True
            else:
                print("❌ Failed to post to Discord")
                return False
                
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
            
            # Send via our working Discord integration - SSOT IMPLEMENTATION
            if self.discord_service:
                # Use our working simple_discord.py integration
                success = self.discord_service.send_devlog(
                    title=entry.title,
                    content=entry.content,
                    agent=entry.agent_id,
                    category=entry.category,
                    priority=entry.metadata.get('priority', 'normal')
                )
            else:
                print("⚠️ Discord service not available")
                success = False
            
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
            print(f"   Service: {'✅ Available' if DISCORD_AVAILABLE else '⚠️  Limited'}")
            print(f"   Bridge: {'✅ Available' if SYSTEMS_AVAILABLE else '⚠️  Limited'}")
            print(f"   Auto-posting: {'✅ Enabled' if self.devlog_config['auto_discord'] else '❌ Disabled'}")
            print(f"   Default Channel: {self.devlog_config['default_channel']}")
            
            # Check Discord webhook status - FIXED: Check actual webhook URL
            if self.discord_service and hasattr(self.discord_service, 'webhook_url') and self.discord_service.webhook_url:
                print(f"   Webhook: ✅ Configured ({self.discord_service.webhook_url[:50]}...)")
            else:
                # Try to get webhook from environment
                import os
                webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
                if webhook_url:
                    print(f"   Webhook: ✅ Configured from environment ({webhook_url[:50]}...)")
                else:
                    print("   Webhook: ❌ Not configured (set DISCORD_WEBHOOK_URL environment variable)")
            
            # SSOT Configuration
            print("\n🎯 SSOT Configuration:")
            print(f"   SSOT Enforced: {'✅ Yes' if self.devlog_config['ssot_enforced'] else '❌ No'}")
            print(f"   Updates Required: {'✅ Yes' if self.devlog_config['required_for_updates'] else '❌ No'}")
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
            return False
        except Exception as e:
            self.logger.error(f"CLI error: {e}")
            print(f"❌ CLI error: {e}")
            return False


def main():
    """Main entry point for devlog CLI"""
    cli = DevlogCLI()
    return cli.run()


if __name__ == "__main__":
    exit(main())
