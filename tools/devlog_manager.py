#!/usr/bin/env python3
"""
Devlog Manager - Automatic Swarm Brain & Discord Integration
=============================================================

USAGE:
    # Post a devlog (auto-posts to Discord + Swarm Brain)
    python -m tools.devlog_manager post --agent agent-5 --file my_analysis.md
    
    # Post a MAJOR update
    python -m tools.devlog_manager post --agent agent-5 --file breakthrough.md --major
    
    # Via toolbelt
    python tools/agent_toolbelt.py devlog post --agent agent-5 --file analysis.md

FEATURES:
- Automatic Swarm Brain upload
- Automatic Discord channel posting
- Agent flag required (--agent)
- Major update flag (--major) for important devlogs
- Categories devlogs automatically
- Updates index

Author: Agent-5 (Business Intelligence & Memory Safety)
Date: 2025-10-15
"""

import os
import re
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional
import requests


class DevlogManager:
    """Manages devlog uploads to Swarm Brain and Discord"""
    
    def __init__(self):
        self.swarm_brain_path = Path("swarm_brain/devlogs")
        self.discord_webhook = os.getenv("DISCORD_WEBHOOK_URL")
        
        # Agent to Discord channel mapping
        self.agent_channels = {
            "agent-1": os.getenv("DISCORD_AGENT1_WEBHOOK"),
            "agent-2": os.getenv("DISCORD_AGENT2_WEBHOOK"),
            "agent-3": os.getenv("DISCORD_AGENT3_WEBHOOK"),
            "agent-4": os.getenv("DISCORD_CAPTAIN_WEBHOOK"),
            "agent-5": os.getenv("DISCORD_AGENT5_WEBHOOK"),
            "agent-6": os.getenv("DISCORD_AGENT6_WEBHOOK"),
            "agent-7": os.getenv("DISCORD_AGENT7_WEBHOOK"),
            "agent-8": os.getenv("DISCORD_AGENT8_WEBHOOK"),
        }
    
    def categorize_devlog(self, filename: str, content: str) -> str:
        """Auto-categorize devlog based on content/filename"""
        filename_lower = filename.lower()
        content_lower = content.lower()
        
        # Repository analysis
        if 'repo' in filename_lower or 'repository' in content_lower:
            return 'repository_analysis'
        
        # Mission reports
        if 'mission' in filename_lower or 'complete' in filename_lower:
            return 'mission_reports'
        
        # Agent sessions
        if 'session' in filename_lower or 'cycle' in filename_lower:
            return 'agent_sessions'
        
        # System events
        if any(word in content_lower for word in ['debate', 'swarm', 'decision', 'vote']):
            return 'system_events'
        
        # Default
        return 'agent_sessions'
    
    def upload_to_swarm_brain(
        self, 
        agent: str, 
        file_path: Path, 
        category: Optional[str] = None
    ) -> Path:
        """Upload devlog to Swarm Brain"""
        
        # Read content
        content = file_path.read_text(encoding='utf-8')
        
        # Auto-categorize if not specified
        if not category:
            category = self.categorize_devlog(file_path.name, content)
        
        # Create category directory
        category_path = self.swarm_brain_path / category
        category_path.mkdir(parents=True, exist_ok=True)
        
        # Generate filename with agent prefix if not present
        filename = file_path.name
        if not filename.startswith(agent.replace('-', '')):
            timestamp = datetime.now().strftime("%Y-%m-%d")
            filename = f"{timestamp}_{agent}_{filename}"
        
        # Upload
        target_path = category_path / filename
        target_path.write_text(content, encoding='utf-8')
        
        print(f"✅ Uploaded to Swarm Brain: {target_path.relative_to(Path.cwd())}")
        return target_path
    
    def post_to_discord(
        self, 
        agent: str, 
        file_path: Path, 
        is_major: bool = False
    ) -> bool:
        """Post devlog to agent's Discord channel"""
        
        # Get webhook for agent
        webhook_url = self.agent_channels.get(agent)
        if not webhook_url:
            # Fallback to general webhook
            webhook_url = self.discord_webhook
        
        if not webhook_url:
            print(f"⚠️ No Discord webhook configured for {agent}")
            return False
        
        # Read content
        content = file_path.read_text(encoding='utf-8')
        
        # Prepare message
        title = f"{'🚨 MAJOR UPDATE' if is_major else '📋 Devlog'}: {file_path.name}"
        
        # Discord message limit: 2000 chars
        if len(content) > 1800:
            preview = content[:1800] + "...\n\n*(Full devlog in Swarm Brain)*"
        else:
            preview = content
        
        # Create embed
        embed = {
            "title": title,
            "description": preview,
            "color": 0xFF0000 if is_major else 0x3498DB,  # Red for major, blue for normal
            "fields": [
                {"name": "Agent", "value": agent.upper(), "inline": True},
                {"name": "Category", "value": self.categorize_devlog(file_path.name, content), "inline": True},
                {"name": "Timestamp", "value": datetime.now().strftime("%Y-%m-%d %H:%M"), "inline": True},
            ],
            "footer": {"text": "Swarm Brain Devlog System"}
        }
        
        payload = {
            "embeds": [embed],
            "username": f"{agent.upper()} Devlog Bot"
        }
        
        # Post
        try:
            response = requests.post(webhook_url, json=payload, timeout=10)
            if response.status_code == 204:
                print(f"✅ Posted to Discord: #{agent}-devlogs")
                return True
            else:
                print(f"❌ Discord error: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Failed to post to Discord: {e}")
            return False
    
    def update_index(self):
        """Update devlog index"""
        index_path = self.swarm_brain_path / "DEVLOG_INDEX.md"
        
        # Count devlogs by category
        stats = {}
        for category in ['repository_analysis', 'mission_reports', 'agent_sessions', 'system_events']:
            category_path = self.swarm_brain_path / category
            if category_path.exists():
                count = len(list(category_path.glob("*.md")))
                stats[category] = count
        
        # Update index header
        content = f"""# 📚 SWARM BRAIN DEVLOG INDEX

**Last Updated:** {datetime.now().strftime("%Y-%m-%d %H:%M")}  
**Total Devlogs:** {sum(stats.values())}  
**Auto-Updated:** Via Devlog Manager

---

## 📊 DEVLOG STATISTICS

**By Category:**
- Repository Analysis: {stats.get('repository_analysis', 0)} devlogs
- Mission Reports: {stats.get('mission_reports', 0)} devlogs
- Agent Sessions: {stats.get('agent_sessions', 0)} devlogs
- System Events: {stats.get('system_events', 0)} devlogs

---

*Index auto-generated by Devlog Manager*  
*All devlogs automatically posted to agent Discord channels*

"""
        
        index_path.write_text(content, encoding='utf-8')
        print(f"✅ Updated devlog index")
    
    def post(
        self, 
        agent: str, 
        file_path: str, 
        is_major: bool = False, 
        category: Optional[str] = None
    ):
        """Main post function - uploads to Swarm Brain + posts to Discord"""
        
        file_path = Path(file_path)
        
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            return False
        
        print(f"\n{'='*60}")
        print(f"📤 DEVLOG MANAGER - {'MAJOR UPDATE' if is_major else 'Standard Post'}")
        print(f"{'='*60}\n")
        
        # Step 1: Upload to Swarm Brain
        print("📁 Step 1: Uploading to Swarm Brain...")
        swarm_path = self.upload_to_swarm_brain(agent, file_path, category)
        
        # Step 2: Post to Discord
        print("\n📤 Step 2: Posting to Discord...")
        discord_success = self.post_to_discord(agent, swarm_path, is_major)
        
        # Step 3: Update index
        print("\n📊 Step 3: Updating index...")
        self.update_index()
        
        # Summary
        print(f"\n{'='*60}")
        if discord_success:
            print("✅ DEVLOG POSTED SUCCESSFULLY!")
        else:
            print("⚠️ DEVLOG UPLOADED (Discord posting failed)")
        print(f"   Swarm Brain: {swarm_path.relative_to(Path.cwd())}")
        print(f"   Discord: #{agent}-devlogs {'(MAJOR UPDATE)' if is_major else ''}")
        print(f"{'='*60}\n")
        
        return True


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Devlog Manager - Automatic Swarm Brain & Discord integration"
    )
    
    parser.add_argument(
        'action',
        choices=['post'],
        help='Action to perform'
    )
    
    parser.add_argument(
        '--agent', '-a',
        required=True,
        choices=['agent-1', 'agent-2', 'agent-3', 'agent-4', 'agent-5', 'agent-6', 'agent-7', 'agent-8'],
        help='Agent posting the devlog (REQUIRED)'
    )
    
    parser.add_argument(
        '--file', '-f',
        required=True,
        help='Devlog file to post'
    )
    
    parser.add_argument(
        '--major',
        action='store_true',
        help='Mark as MAJOR UPDATE (red highlight in Discord)'
    )
    
    parser.add_argument(
        '--category', '-c',
        choices=['repository_analysis', 'mission_reports', 'agent_sessions', 'system_events'],
        help='Devlog category (auto-detected if not specified)'
    )
    
    args = parser.parse_args()
    
    manager = DevlogManager()
    
    if args.action == 'post':
        manager.post(args.agent, args.file, args.major, args.category)


if __name__ == "__main__":
    main()

