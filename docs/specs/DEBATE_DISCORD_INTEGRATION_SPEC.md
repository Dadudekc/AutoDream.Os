# 🗳️ Swarm Debate → Discord Integration Specification

**Architect:** Agent-2  
**Request:** Commander  
**Channel ID:** 1375424568969265152  
**Date:** 2025-10-15  
**Priority:** 🚨 BEFORE HARD ONBOARD  

---

## 🎯 COMMANDER'S REQUEST

**"before we onboard i want to update the debate system to integrate with our discord via this channel so we can see agent discussions in this channel we should be able to see which agent said what"**

**Requirements:**
- Swarm proposals/debates visible in Discord
- See which agent said what
- Channel ID: 1375424568969265152
- Before hard onboard

---

## 🔍 CURRENT DEBATE SYSTEM

**Location:** `swarm_proposals/`

**How It Works:**
1. Agents create proposals (markdown files)
2. Agents vote on proposals (markdown files)
3. Debates happen via file updates
4. No real-time visibility

**Example Debate:**
- `github_archive_strategy/` topic
- 8 agent proposals submitted
- Multiple revisions/votes
- Rich discussion in markdown files

**Problem:** All happens in files, not visible in Discord!

---

## ✅ SOLUTION: DISCORD DEBATE BRIDGE

### **Architecture:**

```
Swarm Proposals System
         ↓
  Discord Bridge
         ↓
Discord Channel (1375424568969265152)
         ↓
   Visible Discussions
```

**Components:**
1. **Debate Monitor:** Watches swarm_proposals/ for changes
2. **Discord Formatter:** Formats proposals/votes for Discord
3. **Discord Poster:** Posts to channel with agent attribution
4. **Webhook Integration:** Real-time updates

---

## 🛠️ IMPLEMENTATION DESIGN

### **Component #1: Debate Monitor**

**File:** `src/discord_commander/debate_monitor.py`

```python
"""
Monitor swarm_proposals/ directory for debate activity
Post updates to Discord in real-time
"""

import asyncio
import time
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class DebateFileWatcher(FileSystemEventHandler):
    """
    Watch swarm_proposals/ for changes
    
    Triggers on:
    - New proposal created
    - Proposal modified (revisions/votes)
    - New topic created
    - Debate status changes
    """
    
    def __init__(self, discord_poster):
        self.discord_poster = discord_poster
        self.proposals_path = Path("swarm_proposals")
        self.last_processed = {}
    
    def on_created(self, event):
        """New file created (new proposal or vote)"""
        if event.is_directory:
            return
        
        if event.src_path.endswith('.md'):
            self._handle_new_proposal(event.src_path)
    
    def on_modified(self, event):
        """File modified (proposal revision or vote update)"""
        if event.is_directory:
            return
        
        if event.src_path.endswith('.md'):
            self._handle_proposal_update(event.src_path)
    
    def _handle_new_proposal(self, file_path: str):
        """Handle new proposal file"""
        # Parse proposal
        proposal = self._parse_proposal(file_path)
        
        # Post to Discord
        asyncio.run(self.discord_poster.post_new_proposal(proposal))
    
    def _handle_proposal_update(self, file_path: str):
        """Handle proposal update"""
        # Check if actually changed
        if self._is_duplicate_event(file_path):
            return
        
        # Parse updated proposal
        proposal = self._parse_proposal(file_path)
        
        # Post update to Discord
        asyncio.run(self.discord_poster.post_proposal_update(proposal))
    
    def _parse_proposal(self, file_path: str) -> dict:
        """
        Parse proposal markdown file
        
        Extracts:
        - Topic
        - Agent ID
        - Title
        - Content
        - Vote (if present)
        - Timestamp
        """
        path = Path(file_path)
        
        # Extract topic from path
        parts = path.parts
        if 'swarm_proposals' in parts:
            idx = parts.index('swarm_proposals')
            topic = parts[idx + 1] if len(parts) > idx + 1 else 'unknown'
        else:
            topic = 'unknown'
        
        # Extract agent ID from filename
        filename = path.name
        if filename.startswith('Agent-'):
            agent_id = filename.split('_')[0]  # "Agent-2"
        else:
            agent_id = 'Unknown'
        
        # Read content
        content = path.read_text()
        
        # Extract title (first # header)
        title = "Untitled"
        for line in content.split('\n'):
            if line.startswith('# '):
                title = line[2:].strip()
                break
        
        # Determine type
        is_vote = 'VOTE' in filename.upper() or 'vote' in title.lower()
        is_revision = 'REVISION' in filename.upper() or 'revised' in content.lower()
        
        return {
            'topic': topic,
            'agent_id': agent_id,
            'title': title,
            'content': content,
            'file_path': file_path,
            'is_vote': is_vote,
            'is_revision': is_revision,
            'timestamp': datetime.now()
        }
    
    def _is_duplicate_event(self, file_path: str) -> bool:
        """Check if this is duplicate event (watchdog fires multiple times)"""
        last_time = self.last_processed.get(file_path, 0)
        current_time = time.time()
        
        # Ignore if processed within 5 seconds
        if current_time - last_time < 5:
            return True
        
        self.last_processed[file_path] = current_time
        return False
```

---

### **Component #2: Discord Formatter**

**File:** `src/discord_commander/debate_formatter.py`

```python
"""
Format debate activity for Discord display
Creates rich embeds showing agent proposals and votes
"""

import discord
from datetime import datetime


class DebateDiscordFormatter:
    """
    Format swarm proposals for Discord visibility
    
    Shows:
    - Which agent contributed
    - What they proposed
    - Vote status
    - Debate activity
    """
    
    # Agent colors for visual distinction
    AGENT_COLORS = {
        'Agent-1': discord.Color.red(),
        'Agent-2': discord.Color.blue(),
        'Agent-3': discord.Color.green(),
        'Agent-4': discord.Color.gold(),
        'Agent-5': discord.Color.purple(),
        'Agent-6': discord.Color.orange(),
        'Agent-7': discord.Color.teal(),
        'Agent-8': discord.Color.magenta(),
    }
    
    # Agent emojis for visual identity
    AGENT_EMOJIS = {
        'Agent-1': '🔧',  # Integration
        'Agent-2': '🏗️',  # Architecture
        'Agent-3': '⚙️',  # Infrastructure
        'Agent-4': '👑',  # Captain
        'Agent-5': '📊',  # Business Intelligence
        'Agent-6': '🎯',  # Coordination
        'Agent-7': '🌐',  # Web Development
        'Agent-8': '🔗',  # SSOT
    }
    
    def format_new_proposal(self, proposal: dict) -> discord.Embed:
        """
        Format new proposal as Discord embed
        
        Shows:
        - Agent who proposed
        - Topic
        - Title
        - Summary (first 500 chars)
        - Link to full proposal
        """
        agent_id = proposal['agent_id']
        agent_emoji = self.AGENT_EMOJIS.get(agent_id, '🤖')
        agent_color = self.AGENT_COLORS.get(agent_id, discord.Color.blue())
        
        # Create embed
        embed = discord.Embed(
            title=f"{agent_emoji} NEW PROPOSAL: {proposal['title']}",
            description=f"**Topic:** {proposal['topic']}\n**Agent:** {agent_id}",
            color=agent_color,
            timestamp=proposal['timestamp']
        )
        
        # Add proposal summary (first 500 chars)
        summary = self._extract_summary(proposal['content'], max_chars=500)
        embed.add_field(
            name="📋 Proposal Summary",
            value=summary,
            inline=False
        )
        
        # Add file location
        embed.add_field(
            name="📂 Full Proposal",
            value=f"`{proposal['file_path']}`",
            inline=False
        )
        
        # Footer
        embed.set_footer(text=f"Swarm Debate System | {agent_id}")
        
        return embed
    
    def format_vote(self, proposal: dict) -> discord.Embed:
        """
        Format vote as Discord embed
        
        Shows:
        - Agent who voted
        - Their vote (+1, -1, +0.5, etc.)
        - Rationale
        - Topic
        """
        agent_id = proposal['agent_id']
        agent_emoji = self.AGENT_EMOJIS.get(agent_id, '🤖')
        agent_color = self.AGENT_COLORS.get(agent_id, discord.Color.blue())
        
        # Extract vote from content
        vote = self._extract_vote(proposal['content'])
        vote_emoji = "✅" if vote > 0 else "❌" if vote < 0 else "➖"
        
        embed = discord.Embed(
            title=f"{vote_emoji} VOTE CAST: {agent_emoji} {agent_id}",
            description=f"**Topic:** {proposal['topic']}\n**Vote:** {vote:+.1f}",
            color=agent_color,
            timestamp=proposal['timestamp']
        )
        
        # Add rationale
        rationale = self._extract_rationale(proposal['content'])
        if rationale:
            embed.add_field(
                name="💭 Rationale",
                value=rationale[:1000],
                inline=False
            )
        
        # Add voting status
        embed.add_field(
            name="🗳️ Current Tally",
            value=self._get_voting_tally(proposal['topic']),
            inline=False
        )
        
        embed.set_footer(text=f"Swarm Democracy | {agent_id}")
        
        return embed
    
    def format_revision(self, proposal: dict) -> discord.Embed:
        """Format proposal revision"""
        agent_id = proposal['agent_id']
        agent_emoji = self.AGENT_EMOJIS.get(agent_id, '🤖')
        agent_color = self.AGENT_COLORS.get(agent_id, discord.Color.blue())
        
        embed = discord.Embed(
            title=f"🔄 REVISED: {agent_emoji} {agent_id}",
            description=f"**Topic:** {proposal['topic']}\n**Title:** {proposal['title']}",
            color=agent_color,
            timestamp=proposal['timestamp']
        )
        
        # Show what changed
        changes = self._extract_changes(proposal['content'])
        if changes:
            embed.add_field(
                name="📝 Changes",
                value=changes[:1000],
                inline=False
            )
        
        embed.set_footer(text=f"Swarm Debate | {agent_id}")
        
        return embed
    
    def _extract_summary(self, content: str, max_chars: int = 500) -> str:
        """Extract proposal summary from content"""
        # Look for "Proposed Solution" or "Problem Statement" section
        lines = content.split('\n')
        
        summary_lines = []
        in_summary = False
        
        for line in lines:
            if 'Proposed Solution' in line or 'Problem Statement' in line:
                in_summary = True
                continue
            
            if in_summary:
                if line.startswith('#'):  # Next section
                    break
                if line.strip():
                    summary_lines.append(line.strip())
        
        summary = ' '.join(summary_lines)[:max_chars]
        
        if len(summary) == max_chars:
            summary += "..."
        
        return summary or "See full proposal for details"
    
    def _extract_vote(self, content: str) -> float:
        """Extract vote value from content"""
        # Look for "+1", "-1", "+0.5", etc.
        import re
        
        vote_pattern = r'[+-]?\d+\.?\d*'
        matches = re.findall(vote_pattern, content)
        
        # Look for explicit vote statements
        for line in content.split('\n'):
            if 'VOTE' in line.upper() or 'vote' in line.lower():
                for match in matches:
                    try:
                        return float(match)
                    except:
                        pass
        
        return 0.0  # No vote found
    
    def _extract_rationale(self, content: str) -> str:
        """Extract vote rationale"""
        # Look for "Rationale" section
        lines = content.split('\n')
        rationale_lines = []
        in_rationale = False
        
        for line in lines:
            if 'Rationale' in line or 'RATIONALE' in line:
                in_rationale = True
                continue
            
            if in_rationale:
                if line.startswith('#'):
                    break
                if line.strip():
                    rationale_lines.append(line.strip())
        
        return ' '.join(rationale_lines) or "See full vote for details"
    
    def _get_voting_tally(self, topic: str) -> str:
        """Get current voting tally for topic"""
        # Count votes from files
        topic_path = Path(f"swarm_proposals/{topic}")
        
        votes = {}
        for file in topic_path.glob("*VOTE*.md"):
            content = file.read_text()
            agent = file.name.split('_')[0]  # Extract agent ID
            vote = self._extract_vote(content)
            votes[agent] = vote
        
        if not votes:
            return "No votes cast yet"
        
        # Format tally
        tally_lines = []
        for agent, vote in sorted(votes.items()):
            emoji = "✅" if vote > 0 else "❌" if vote < 0 else "➖"
            tally_lines.append(f"{emoji} {agent}: {vote:+.1f}")
        
        return '\n'.join(tally_lines)
    
    def _extract_changes(self, content: str) -> str:
        """Extract what changed in revision"""
        # Look for revision notes or what changed
        for line in content.split('\n'):
            if 'changed' in line.lower() or 'revised' in line.lower():
                return line.strip()
        
        return "Proposal revised - see file for details"
```

---

### **Component #3: Discord Poster**

**File:** `src/discord_commander/debate_discord_poster.py`

```python
"""
Post debate activity to Discord channel
Uses webhook for reliable posting
"""

import discord
import asyncio
from discord import Webhook
import aiohttp


class DebateDiscordPoster:
    """
    Post swarm debate activity to Discord
    
    Features:
    - Agent attribution (shows who said what)
    - Rich embeds (formatted beautifully)
    - Real-time updates (as files change)
    - Thread support (organized discussions)
    """
    
    def __init__(self, channel_id: int, bot=None):
        self.channel_id = channel_id  # 1375424568969265152
        self.bot = bot
        self.formatter = DebateDiscordFormatter()
    
    async def post_new_proposal(self, proposal: dict):
        """
        Post new proposal to Discord
        
        Args:
            proposal: Parsed proposal dict
        """
        channel = self.bot.get_channel(self.channel_id)
        
        if not channel:
            print(f"❌ Discord channel {self.channel_id} not found!")
            return
        
        # Format as embed
        embed = self.formatter.format_new_proposal(proposal)
        
        # Post to channel
        await channel.send(embed=embed)
        
        print(f"✅ Posted new proposal: {proposal['agent_id']} - {proposal['title']}")
    
    async def post_proposal_update(self, proposal: dict):
        """Post proposal update (revision or vote)"""
        channel = self.bot.get_channel(self.channel_id)
        
        if not channel:
            return
        
        # Determine update type
        if proposal['is_vote']:
            embed = self.formatter.format_vote(proposal)
        elif proposal['is_revision']:
            embed = self.formatter.format_revision(proposal)
        else:
            embed = self.formatter.format_new_proposal(proposal)
        
        # Post to channel
        await channel.send(embed=embed)
        
        print(f"✅ Posted update: {proposal['agent_id']} - {proposal['topic']}")
    
    async def post_debate_summary(self, topic: str):
        """
        Post debate summary
        
        Shows:
        - All proposals
        - All votes
        - Current tally
        - Next steps
        """
        channel = self.bot.get_channel(self.channel_id)
        
        if not channel:
            return
        
        # Create summary embed
        embed = discord.Embed(
            title=f"🗳️ DEBATE SUMMARY: {topic}",
            description="All agent proposals and votes",
            color=discord.Color.blue()
        )
        
        # List all proposals
        topic_path = Path(f"swarm_proposals/{topic}")
        proposals = []
        
        for file in topic_path.glob("Agent-*.md"):
            if 'VOTE' not in file.name:
                agent = file.name.split('_')[0]
                proposals.append(agent)
        
        embed.add_field(
            name="📋 Proposals",
            value='\n'.join(proposals) or 'None yet',
            inline=True
        )
        
        # List all votes
        votes = []
        for file in topic_path.glob("*VOTE*.md"):
            agent = file.name.split('_')[0]
            votes.append(agent)
        
        embed.add_field(
            name="🗳️ Votes Cast",
            value='\n'.join(votes) or 'None yet',
            inline=True
        )
        
        # Get tally
        tally = self.formatter._get_voting_tally(topic)
        embed.add_field(
            name="📊 Current Tally",
            value=tally,
            inline=False
        )
        
        await channel.send(embed=embed)
```

---

### **Component #4: Integration with Bot**

**File:** `src/discord_commander/unified_discord_bot.py` (enhance)

```python
# Add to UnifiedDiscordBot class

async def on_ready(self):
    """Bot ready event."""
    # Existing code...
    
    # Start debate monitoring
    await self.start_debate_monitoring()

async def start_debate_monitoring(self):
    """Start monitoring swarm_proposals/ for debate activity"""
    from .debate_monitor import DebateFileWatcher
    from .debate_discord_poster import DebateDiscordPoster
    from watchdog.observers import Observer
    
    # Create poster
    poster = DebateDiscordPoster(
        channel_id=1375424568969265152,  # Commander's specified channel
        bot=self
    )
    
    # Create watcher
    watcher = DebateFileWatcher(discord_poster=poster)
    
    # Set up file system observer
    observer = Observer()
    observer.schedule(watcher, "swarm_proposals", recursive=True)
    observer.start()
    
    self.logger.info("✅ Debate monitoring started for channel 1375424568969265152")
    
    # Keep observer running
    self.debate_observer = observer


# Add new command: !debate
@bot.command(name='debate')
async def debate_command(ctx, topic: str = None):
    """
    Show debate status or summary
    
    Usage:
        !debate                    # List all topics
        !debate github_archive_strategy   # Show summary for topic
    """
    if not topic:
        # List all topics
        topics_path = Path("swarm_proposals")
        topics = [d.name for d in topics_path.iterdir() if d.is_dir()]
        
        embed = discord.Embed(
            title="🗳️ SWARM DEBATE TOPICS",
            description="Active democratic discussions",
            color=discord.Color.blue()
        )
        
        for topic_name in topics:
            # Count proposals
            topic_path = topics_path / topic_name
            proposal_count = len(list(topic_path.glob("Agent-*.md")))
            vote_count = len(list(topic_path.glob("*VOTE*.md")))
            
            embed.add_field(
                name=f"📁 {topic_name}",
                value=f"Proposals: {proposal_count} | Votes: {vote_count}",
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    else:
        # Show topic summary
        poster = DebateDiscordPoster(channel_id=ctx.channel.id, bot=self)
        await poster.post_debate_summary(topic)
```

---

## 📊 DISCORD VISIBILITY FEATURES

### **What Commander Will See:**

**When Agent Creates Proposal:**
```
🏗️ NEW PROPOSAL: Master Orientation Guide
━━━━━━━━━━━━━━━━━━━━━━━━━━
Topic: orientation_system
Agent: Agent-2

📋 Proposal Summary
Create single entry point for agent onboarding with
comprehensive system overview, tool directory, procedure
library, and quick-start guides...

📂 Full Proposal
`swarm_proposals/orientation_system/Agent-2_master_orientation_guide.md`

Swarm Debate System | Agent-2
```

**When Agent Votes:**
```
✅ VOTE CAST: 🎯 Agent-6
━━━━━━━━━━━━━━━━━━━━━━━━━━
Topic: github_archive_strategy
Vote: +1.0

💭 Rationale
Agent-6's aggressive 60% archive approach is ROI-optimized,
matches Commander's "30 ideas" statement, and provides
sustainable maintenance burden...

🗳️ Current Tally
✅ Agent-6: +1.0
✅ Agent-2: +1.0
✅ Agent-7: +0.5
➖ Agent-3: +0.0

Swarm Democracy | Agent-6
```

**When Agent Revises:**
```
🔄 REVISED: 🏗️ Agent-2
━━━━━━━━━━━━━━━━━━━━━━━━━━
Topic: github_archive_strategy
Title: Conservative Archive Strategy (CORRECTED)

📝 Changes
Updated from 37.5% to 100% archive recommendation
based on comprehensive architectural audit findings...

Swarm Debate | Agent-2
```

---

## 🚀 IMPLEMENTATION PLAN

### **Phase 1: Core Integration (2-3 hours)**

**Tasks:**
1. Create `debate_monitor.py` (file watcher)
2. Create `debate_formatter.py` (Discord embeds)
3. Create `debate_discord_poster.py` (posting logic)
4. Enhance `unified_discord_bot.py` (integrate monitoring)

**Testing:**
- Create test proposal → Should appear in Discord
- Create test vote → Should appear in Discord
- Revise proposal → Should update in Discord

---

### **Phase 2: Commands & Features (1-2 hours)**

**Tasks:**
1. Add !debate command (list topics / show summary)
2. Add !proposal command (create proposal from Discord)
3. Add !vote command (vote from Discord)
4. Add reaction voting (👍 👎 for quick votes)

**Testing:**
- !debate → Shows all topics
- !debate github_archive_strategy → Shows summary
- !proposal → Creates new proposal
- !vote +1 → Casts vote

---

### **Phase 3: Advanced Features (2-3 hours - Optional)**

**Tasks:**
1. Thread support (each proposal = thread)
2. Real-time notifications (@mentions when debates start)
3. Voting deadlines (auto-close after X hours)
4. Results announcement (winning proposal highlighted)

---

## ✅ SUCCESS CRITERIA

**Commander Can See:**
- ✅ Which agent proposed what (clear attribution)
- ✅ What each agent voted (with rationale)
- ✅ Proposal revisions (what changed)
- ✅ Current debate status (tally)
- ✅ All in Discord channel 1375424568969265152

**Agents Can:**
- ✅ See all debate activity in Discord
- ✅ Participate from Discord (!proposal, !vote)
- ✅ Track debate progress visually
- ✅ Get notifications when debates start

---

## 📋 QUICK WIN (1 hour)

**For immediate visibility (before full system):**

**Simple Webhook Poster:**
```python
# Post debate activity via webhook
async def post_debate_to_discord(proposal: dict):
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(webhook_url, session=session)
        
        embed = format_proposal_embed(proposal)
        await webhook.send(embed=embed)
```

**Benefit:** Gets debate visibility NOW, full features later

---

## 🎯 RECOMMENDATION

**Before Hard Onboard:**
- **Quick Win:** 1 hour implementation (webhook poster)
- **Gets:** Basic debate visibility in Discord
- **Defers:** Advanced features to post-onboard

**Full Implementation:**
- **Timeline:** 5-8 hours total
- **Gets:** Complete debate system with commands
- **When:** After hard onboard, as next priority

**Commander, which do you prefer?**

**I can create either:**
- Quick win spec (1 hour)
- Full integration spec (5-8 hours)
- Or both (quick now, full later)

---

**WE. ARE. SWARM.** 🐝⚡
