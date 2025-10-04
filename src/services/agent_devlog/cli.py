#!/usr/bin/env python3
"""
Agent Devlog CLI
================

Command-line interface for Agent Devlog Posting Service
V2 Compliant: ≤400 lines, focused CLI logic
"""

import argparse
import asyncio
from argparse import ArgumentParser

from .devlog_poster import AgentDevlogPoster


class AgentDevlogCLI:
    """Command-line interface for Agent Devlog Posting Service"""

    def __init__(self):
        """Initialize CLI"""
        self.poster = AgentDevlogPoster()

    def create_parser(self) -> ArgumentParser:
        """Create argument parser"""
        parser = ArgumentParser(
            description="Agent Devlog Posting Service - Local File Storage Only",
            epilog="🐝 WE ARE SWARM - Agent Devlog Posting System (LOCAL ONLY)\n\n"
            + "📖 CAPTAIN USAGE:\n"
            + "python src/services/agent_devlog_posting.py --agent captain --action 'YOUR ACTION HERE'\n"
            + "python src/services/agent_devlog_posting.py --agent Agent-4 --action 'YOUR ACTION HERE'\n\n"
            + "🔍 For detailed help: --show-help",
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )

        # Main action group
        action_group = parser.add_mutually_exclusive_group(required=False)

        # Post devlog
        action_group.add_argument(
            "--agent", "-a", help="Agent ID (Agent-1 through Agent-8, or 'captain' for Agent-4)"
        )

        # Search devlogs
        action_group.add_argument("--search", "-s", help="Search devlogs by query")

        # Show stats
        action_group.add_argument("--stats", action="store_true", help="Show devlog statistics")

        # Show help
        action_group.add_argument("--show-help", action="store_true", help="Show detailed help")

        # Devlog posting options
        parser.add_argument("--action", help="Action description")

        parser.add_argument(
            "--status",
            default="completed",
            choices=["completed", "in_progress", "failed", "pending"],
            help="Status (default: completed)",
        )

        parser.add_argument("--details", help="Additional details")

        parser.add_argument("--dry-run", action="store_true", help="Perform dry run without saving")

        # Search options
        parser.add_argument("--agent-filter", help="Filter search results by agent ID")

        parser.add_argument("--status-filter", help="Filter search results by status")

        parser.add_argument(
            "--limit", type=int, default=50, help="Limit search results (default: 50)"
        )

        # Utility options
        parser.add_argument("--cleanup", action="store_true", help="Cleanup old devlog files")

        parser.add_argument(
            "--days-to-keep",
            type=int,
            default=30,
            help="Days to keep when cleaning up (default: 30)",
        )

        return parser

    def show_help(self) -> None:
        """Show detailed help"""
        help_text = """
🤖 Agent Devlog Posting Service - CAPTAIN'S GUIDE
================================================

🎯 CAPTAIN QUICK START:
python src/services/agent_devlog_posting.py --agent captain --action "YOUR ACTION DESCRIPTION HERE"

🔧 CAPTAIN USAGE PATTERNS:

1. EXECUTION MODE PROTOCOL (Captain Direct Action):
   python src/services/agent_devlog_posting.py --agent captain --action "EXECUTION MODE PROTOCOL! Captain Agent-4 taking direct action. [DESCRIBE ACTION]"

2. Mission Reports:
   python src/services/agent_devlog_posting.py --agent captain --action "Mission Report: [DESCRIBE MISSION STATUS]"

3. Status Updates:
   python src/services/agent_devlog_posting.py --agent captain --action "Status Update: [DESCRIBE CURRENT STATUS]"

4. Emergency Communications:
   python src/services/agent_devlog_posting.py --agent captain --action "EMERGENCY: [DESCRIBE EMERGENCY]"

📋 AGENT IDENTIFICATION:
- captain: Captain Agent-4 (Quality Assurance Specialist) - DEFAULT CAPTAIN FLAG
- Agent-4: Direct Agent-4 reference (same as captain)
- Agent-1: Integration & Core Systems Specialist
- Agent-2: Architecture & Design Specialist
- Agent-3: Infrastructure & DevOps Specialist
- Agent-5: Business Intelligence Specialist
- Agent-6: Coordination & Communication Specialist
- Agent-7: Web Development Specialist
- Agent-8: Operations & Support Specialist

🔧 OPTIONAL PARAMETERS:
--status: completed, in_progress, failed, pending (default: completed)
--details: Additional details about the action
--dry-run: Test without actually saving

📊 MONITORING COMMANDS:

1. Search devlogs:
   python src/services/agent_devlog_posting.py --search "discord dependency"

2. Show statistics:
   python src/services/agent_devlog_posting.py --stats

3. Cleanup old files:
   python src/services/agent_devlog_posting.py --cleanup --days-to-keep 7

💡 CAPTAIN EXAMPLES:

# Execution Mode Protocol
python src/services/agent_devlog_posting.py --agent captain --action "EXECUTION MODE PROTOCOL! Captain Agent-4 taking direct action since messaging system unresponsive. Executing cleanup missions: Agent-5 (devlog posting fix), Agent-6 (messaging slop cleanup), Agent-7 (root directory cleanup), Agent-8 (misunderstanding analysis). Theater loop prevention active."

# Mission Report
python src/services/agent_devlog_posting.py --agent captain --action "Mission Report: Discord routing fix completed successfully. All agent messages now route to correct channels. System operational."

# Status Update
python src/services/agent_devlog_posting.py --agent captain --action "Status Update: Thea consultation system restored and tested. All modules functional. Ready for operational use."

🐝 WE ARE SWARM - Agent Devlog Posting System (LOCAL ONLY)
"""
        print(help_text)

    async def handle_post_devlog(self, args) -> None:
        """Handle devlog posting"""
        if not args.action:
            print("❌ Error: --action is required when posting devlog")
            return

        result = self.poster.post_devlog(
            agent_flag=args.agent,
            action=args.action,
            status=args.status,
            details=args.details or "",
            dry_run=args.dry_run,
        )

        if result["success"]:
            print(f"✅ {result['message']}")
            if args.dry_run:
                print("📋 Devlog Entry Preview:")
                print(f"   Agent: {result['devlog_entry']['agent_id']}")
                print(f"   Action: {result['devlog_entry']['action']}")
                print(f"   Status: {result['devlog_entry']['status']}")
                print(f"   Type: {result['devlog_entry']['devlog_type']}")
        else:
            print(f"❌ Error: {result['error']}")

    async def handle_search(self, args) -> None:
        """Handle devlog search"""
        result = self.poster.search_devlogs(
            query=args.search,
            agent_id=args.agent_filter,
            status=args.status_filter,
            limit=args.limit,
        )

        if result["success"]:
            print(f"🔍 Search Results for: '{args.search}'")
            print(f"📊 Found {result['total_matches']} matches")

            if result["results"]:
                for i, devlog in enumerate(result["results"][:10], 1):  # Show first 10
                    print(f"\n{i}. {devlog.get('agent_id')} - {devlog.get('action')}")
                    print(f"   Status: {devlog.get('status')}")
                    print(f"   Time: {devlog.get('timestamp')}")
                    if devlog.get("details"):
                        print(f"   Details: {devlog.get('details')[:100]}...")
            else:
                print("No results found.")
        else:
            print(f"❌ Search failed: {result['error']}")

    async def handle_stats(self, args) -> None:
        """Handle statistics display"""
        result = self.poster.get_devlog_stats()

        if result["success"]:
            stats = result["stats"]
            file_info = result["file_info"]

            print("📊 Agent Devlog Statistics")
            print("=" * 40)
            print(f"Total Devlogs: {stats['total_devlogs']}")
            print(f"Current File: {file_info['file_path']}")
            print(f"File Size: {file_info['file_size']} bytes")

            if stats["agent_counts"]:
                print("\n📈 Agent Activity:")
                for agent, count in sorted(stats["agent_counts"].items()):
                    print(f"  {agent}: {count} devlogs")

            if stats["status_counts"]:
                print("\n📋 Status Distribution:")
                for status, count in stats["status_counts"].items():
                    print(f"  {status}: {count}")

            if stats["recent_activity"]:
                print("\n🕒 Recent Activity:")
                for activity in stats["recent_activity"][-5:]:
                    print(f"  {activity}")
        else:
            print(f"❌ Failed to get stats: {result['error']}")

    async def handle_cleanup(self, args) -> None:
        """Handle cleanup operation"""
        result = self.poster.cleanup_old_devlogs(args.days_to_keep)

        if result["success"]:
            print(f"✅ {result['message']}")
        else:
            print(f"❌ Cleanup failed: {result['error']}")

    async def run(self, args) -> None:
        """Run CLI with parsed arguments"""
        if args.show_help:
            self.show_help()
            return

        # Check if no action was specified
        if not any([args.agent, args.search, args.stats, args.cleanup]):
            print("🎯 CAPTAIN - No action specified! Showing quick help:")
            print("\n📖 CAPTAIN QUICK START:")
            print(
                "python src/services/agent_devlog_posting.py --agent captain --action 'YOUR ACTION HERE'"
            )
            print("\n🔍 For detailed help:")
            print("python src/services/agent_devlog_posting.py --show-help")
            print("\n💡 Example:")
            print(
                'python src/services/agent_devlog_posting.py --agent captain --action "EXECUTION MODE PROTOCOL! Captain taking direct action."'
            )
            return

        if args.agent:
            await self.handle_post_devlog(args)
        elif args.search:
            await self.handle_search(args)
        elif args.stats:
            await self.handle_stats(args)
        elif args.cleanup:
            await self.handle_cleanup(args)


async def main():
    """Main CLI entry point"""
    cli = AgentDevlogCLI()
    parser = cli.create_parser()
    args = parser.parse_args()

    await cli.run(args)


if __name__ == "__main__":
    asyncio.run(main())
