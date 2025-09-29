#!/usr/bin/env python3
"""
Agent Devlog CLI
================

Command-line interface for Agent Devlog Posting Service
V2 Compliant: ≤400 lines, focused CLI logic
"""

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
            epilog="🐝 WE ARE SWARM - Agent Devlog Posting System (LOCAL ONLY)",
        )

        # Main action group
        action_group = parser.add_mutually_exclusive_group(required=True)

        # Post devlog
        action_group.add_argument("--agent", "-a", help="Agent ID (Agent-1 through Agent-8)")

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
🤖 Agent Devlog Posting Service - Detailed Help
===============================================

OVERVIEW:
This service allows agents to post devlogs to LOCAL FILES only.
NO Discord dependency - completely independent system.

AGENT FLAGS:
- Agent-1: Integration & Core Systems Specialist
- Agent-2: Architecture & Design Specialist
- Agent-3: Infrastructure & DevOps Specialist
- Agent-4: Quality Assurance Specialist (CAPTAIN)
- Agent-5: Business Intelligence Specialist
- Agent-6: Coordination & Communication Specialist
- Agent-7: Web Development Specialist
- Agent-8: Operations & Support Specialist

USAGE EXAMPLES:

1. Post a devlog:
   python src/services/agent_devlog_posting.py --agent Agent-4 --action "Task completed" --status completed --details "Details here"

2. Search devlogs:
   python src/services/agent_devlog_posting.py --search "discord dependency"

3. Show statistics:
   python src/services/agent_devlog_posting.py --stats

4. Dry run:
   python src/services/agent_devlog_posting.py --agent Agent-4 --action "Test" --dry-run

5. Cleanup old files:
   python src/services/agent_devlog_posting.py --cleanup --days-to-keep 7

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

        if args.agent:
            await self.handle_post_devlog(args)
        elif args.search:
            await self.handle_search(args)
        elif args.stats:
            await self.handle_stats(args)
        elif args.cleanup:
            await self.handle_cleanup(args)
        else:
            print("❌ No valid action specified. Use --show-help for usage information.")


async def main():
    """Main CLI entry point"""
    cli = AgentDevlogCLI()
    parser = cli.create_parser()
    args = parser.parse_args()

    await cli.run(args)


if __name__ == "__main__":
    asyncio.run(main())
