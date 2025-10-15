#!/usr/bin/env python3
"""
Post Agent Devlogs to Discord Channels
Reads devlogs from Swarm Brain and posts to agent-specific Discord channels
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional
import discord
from dotenv import load_dotenv

load_dotenv()

# Agent Discord Channel Mapping
AGENT_CHANNELS = {
    "agent-1": "agent-1-devlogs",
    "agent-2": "agent-2-devlogs",
    "agent-3": "agent-3-devlogs",
    "agent-4": "captain-devlogs",
    "agent-5": "agent-5-devlogs",
    "agent-6": "agent-6-devlogs",
    "agent-7": "agent-7-devlogs",
    "agent-8": "agent-8-devlogs",
}

class DevlogDiscordPoster:
    """Post devlogs from Swarm Brain to Discord channels"""
    
    def __init__(self):
        self.devlogs_path = Path("swarm_brain/devlogs")
        self.token = os.getenv("DISCORD_BOT_TOKEN")
        self.client = None
        
    def parse_agent_from_filename(self, filename: str) -> Optional[str]:
        """Extract agent ID from devlog filename"""
        # Pattern: agent5_repo31_... or agent-6_... or 2025-10-15_agent-2_...
        
        # Try: agentN_
        match = re.search(r'agent[_-]?(\d+)', filename.lower())
        if match:
            return f"agent-{match.group(1)}"
        
        # Try: Agent-N
        match = re.search(r'agent-(\d+)', filename.lower())
        if match:
            return f"agent-{match.group(1)}"
            
        return None
    
    def categorize_devlogs(self) -> Dict[str, List[Path]]:
        """Categorize all devlogs by agent"""
        agent_devlogs = {agent: [] for agent in AGENT_CHANNELS.keys()}
        
        # Scan all devlog files
        for devlog_file in self.devlogs_path.rglob("*.md"):
            if devlog_file.name == "DEVLOG_INDEX.md":
                continue
                
            agent = self.parse_agent_from_filename(devlog_file.name)
            if agent and agent in agent_devlogs:
                agent_devlogs[agent].append(devlog_file)
        
        return agent_devlogs
    
    async def post_devlog_to_channel(self, channel_name: str, devlog_path: Path):
        """Post a single devlog to Discord channel"""
        if not self.client:
            return False
            
        # Find channel
        channel = discord.utils.get(self.client.get_all_channels(), name=channel_name)
        if not channel:
            print(f"❌ Channel not found: {channel_name}")
            return False
        
        # Read devlog content
        content = devlog_path.read_text(encoding='utf-8')
        
        # Discord message limit: 2000 chars
        # Split if needed
        if len(content) <= 1900:
            await channel.send(f"**{devlog_path.name}**\n\n{content}")
        else:
            # Send in chunks
            await channel.send(f"**{devlog_path.name}**")
            chunks = [content[i:i+1900] for i in range(0, len(content), 1900)]
            for chunk in chunks:
                await channel.send(chunk)
        
        return True
    
    async def post_all_devlogs(self):
        """Post all devlogs to respective agent channels"""
        agent_devlogs = self.categorize_devlogs()
        
        stats = {agent: 0 for agent in AGENT_CHANNELS.keys()}
        
        for agent, devlogs in agent_devlogs.items():
            channel_name = AGENT_CHANNELS[agent]
            print(f"\n📤 Posting {len(devlogs)} devlogs to #{channel_name}...")
            
            for devlog in devlogs:
                success = await self.post_devlog_to_channel(channel_name, devlog)
                if success:
                    stats[agent] += 1
                    print(f"  ✅ Posted: {devlog.name}")
                else:
                    print(f"  ❌ Failed: {devlog.name}")
        
        # Summary
        print("\n" + "="*60)
        print("📊 POSTING SUMMARY:")
        for agent, count in stats.items():
            print(f"  {agent}: {count} devlogs posted")
        print(f"  TOTAL: {sum(stats.values())} devlogs posted")
        print("="*60)
    
    def run(self):
        """Run the devlog poster"""
        class DevlogBot(discord.Client):
            def __init__(self, poster):
                intents = discord.Intents.default()
                intents.message_content = True
                super().__init__(intents=intents)
                self.poster = poster
            
            async def on_ready(self):
                print(f'✅ Connected as {self.user}')
                self.poster.client = self
                await self.poster.post_all_devlogs()
                await self.close()
        
        if not self.token:
            print("❌ ERROR: DISCORD_BOT_TOKEN not found in environment")
            return
        
        bot = DevlogBot(self)
        bot.run(self.token)


def main():
    """Main entry point"""
    print("🚀 Devlog Discord Poster")
    print("=" * 60)
    
    poster = DevlogDiscordPoster()
    
    # Analyze first
    print("\n📊 Analyzing devlogs...")
    agent_devlogs = poster.categorize_devlogs()
    
    for agent, devlogs in agent_devlogs.items():
        if devlogs:
            print(f"  {agent}: {len(devlogs)} devlogs")
    
    total = sum(len(devlogs) for devlogs in agent_devlogs.values())
    print(f"  TOTAL: {total} devlogs to post\n")
    
    # Confirm
    response = input("Post all devlogs to Discord? (yes/no): ")
    if response.lower() != 'yes':
        print("❌ Cancelled")
        return
    
    # Post
    poster.run()


if __name__ == "__main__":
    main()

