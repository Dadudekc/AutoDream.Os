#!/usr/bin/env python3
"""
Devlog Wrapper Script - Agent Cellphone V2
==========================================

Simple wrapper script for agents to create and manage devlogs.
Uses the existing devlog CLI system and existing architecture.

**Usage:**
python scripts/devlog.py "Title" "Content" [--agent AGENT_ID] [--category CATEGORY]

**Examples:**
python scripts/devlog.py "Phase 3 Complete" "All systems integrated successfully"
python scripts/devlog.py "Bug Found" "Issue with routing system" --agent "agent-2" --category "issue"
"""

import sys
import argparse
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def main():
    """Main entry point for devlog wrapper"""
    parser = argparse.ArgumentParser(
        description="Simple devlog creation for agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/devlog.py "Phase 3 Complete" "All systems integrated"
  python scripts/devlog.py "Bug Found" "Issue with routing" --agent "agent-2" --category "issue"
  python scripts/devlog.py "New Feature" "Added performance monitoring" --category "milestone"
        """
    )
    
    parser.add_argument("title", help="Devlog title")
    parser.add_argument("content", help="Devlog content")
    parser.add_argument("--agent", "-a", default="unknown", help="Agent ID (default: unknown)")
    parser.add_argument("--category", "-c", 
                       choices=["project_update", "milestone", "issue", "idea", "review"],
                       default="project_update", help="Devlog category")
    parser.add_argument("--tags", "-t", help="Comma-separated tags")
    parser.add_argument("--priority", "-p",
                       choices=["low", "normal", "high", "critical"],
                       default="normal", help="Entry priority")
    parser.add_argument("--no-discord", action="store_true", help="Don't post to Discord")
    
    args = parser.parse_args()
    
    print("📝 CREATING DEVLOG ENTRY")
    print("="*50)
    print(f"📝 Title: {args.title}")
    print(f"📋 Content: {args.content}")
    print(f"🏷️  Category: {args.category}")
    print(f"🤖 Agent: {args.agent}")
    print(f"📊 Priority: {args.priority}")
    if args.tags:
        print(f"🏷️  Tags: {args.tags}")
    print(f"📱 Discord: {'❌ Disabled' if args.no_discord else '✅ Enabled'}")
    print("="*50)
    
    try:
        # Import and use the devlog CLI
        from src.core.devlog_cli import DevlogCLI
        
        cli = DevlogCLI()
        
        # Build command arguments
        cmd_args = [
            "create",
            "--title", args.title,
            "--content", args.content,
            "--category", args.category,
            "--agent", args.agent,
            "--priority", args.priority
        ]
        
        if args.tags:
            cmd_args.extend(["--tags", args.tags])
        
        if args.no_discord:
            cmd_args.append("--no-discord")
        
        # Execute the command
        success = cli._create_entry(argparse.Namespace(**{
            'title': args.title,
            'content': args.content,
            'category': args.category,
            'agent': args.agent,
            'priority': args.priority,
            'tags': args.tags,
            'no_discord': args.no_discord
        }))
        
        if success:
            print("\n✅ Devlog entry created successfully!")
            print("💡 Use 'python scripts/devlog.py --help' for more options")
            print("💡 Use 'python -m src.core.devlog_cli status' to check system status")
        else:
            print("\n❌ Failed to create devlog entry")
            return 1
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you're running from the project root directory")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
