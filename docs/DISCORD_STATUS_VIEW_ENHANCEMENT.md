# Discord Status View Enhancement
**Purpose:** Display rich agent status.json data in Discord interface

## 📊 Current State
- **Location:** `src/discord_commander/messaging_controller_views.py`
- **Current Display:** Basic active/inactive + coordinates
- **Data Source:** `messaging_service.agent_data` (limited)

## 🎯 Enhancement Goal
**Display rich status.json data:**
- Agent mission & phase
- Current tasks (top 3)
- Latest achievements (top 3)
- Points/progress tracking
- Last updated timestamp

## 📁 Status.json Structure Analysis

**Note:** Only 8 main agents exist (Agent-1 through Agent-8). Role workspaces like Agent-SRC-1 are the SAME agents in different roles, not separate agents.

### Common Fields (All Agents)
```json
{
  "agent_id": "Agent-X",
  "agent_name": "Role Name",
  "status": "ACTIVE/COMPLETE/etc",
  "current_phase": "PHASE_NAME",
  "last_updated": "2025-10-11",
  "current_mission": "Mission description",
  "mission_priority": "HIGH/CRITICAL/etc",
  "current_tasks": ["task1", "task2", ...],
  "completed_tasks": ["done1", "done2", ...],
  "achievements": ["achievement1", ...],
  "next_actions": ["action1", ...]
}
```

### Agent-Specific Fields
- **Sprint info:** Duration, points, completion %
- **Team assignments:** Team Beta, Teaching Team, etc.
- **Specialized tracking:** Consolidation, testing, etc.
- **Coordinates:** PyAutoGUI position

## 🎨 Proposed UI Design

### Main Swarm Status View
```
🤖 Swarm Status Dashboard
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Last Updated: 2025-10-11 14:30

[Agent-1 Button] [Agent-2 Button] [Agent-3 Button] [Agent-4 Button]
[Agent-5 Button] [Agent-6 Button] [Agent-7 Button] [Agent-8 Button]

📊 Overall Status:
• Active: 8/8 agents
• In Progress: 3 missions
• Completed Today: 5 tasks

[🔄 Refresh] [📢 Broadcast] [📝 Summary]
```

### Individual Agent Detail View (on button click)
```
🤖 Agent-7 Status Detail
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Role: Repository Cloning Specialist
Status: 🟢 STRATEGIC_REST
Phase: PRIMARY_ROLE_COMPLETE

📋 Current Mission:
TEAM BETA 8/8 REPOS - LEGENDARY COMPLETE

🎯 Current Tasks:
• Standing by for strategic deployment
• Available for next mission
• Primary role complete

🏆 Latest Achievements:
• 100% V2 compliance (37 files, 8 repos)
• Integration Playbook validated
• Civilization-building demonstrated

📊 Progress:
Points: 13,550 pts (LEGENDARY)
Completion: 100%

⏰ Last Updated: 2025-10-11

[← Back] [📨 Message Agent] [🔄 Refresh]
```

## 🛠️ Implementation Plan

### 1. Create Status Reader Module
**File:** `src/discord_commander/status_reader.py`
- Read all agent `status.json` files
- Parse and normalize data
- Cache with TTL (30-60 seconds)
- Handle missing/malformed files

### 2. Enhance SwarmStatusView
**File:** `src/discord_commander/messaging_controller_views.py`
- Add agent detail buttons (8 buttons for agents)
- Create summary embed with key metrics
- Add "View Details" interaction

### 3. Create AgentDetailView
**New File:** `src/discord_commander/agent_detail_view.py`
- Individual agent detail embed
- Back button to return to swarm view
- Message agent button
- Refresh button

### 4. Add Status Summary Command
**New Command:** `!status_summary`
- Compact view of all agents
- Key metrics only
- Quick reference

## 📝 Code Structure

```
src/discord_commander/
├── status_reader.py           # NEW: Read & parse status.json
├── agent_detail_view.py       # NEW: Individual agent details
├── messaging_controller_views.py  # ENHANCED: Add buttons
└── messaging_commands.py      # ENHANCED: Add commands
```

## 🎯 Features

### Phase 1: Basic Enhancement ✅
- [x] Read status.json files
- [x] Display mission + status
- [x] Show top 3 tasks
- [x] Show top 3 achievements
- [x] 8 agent buttons

### Phase 2: Advanced Features
- [ ] Agent detail modals
- [ ] Progress bars for sprint points
- [ ] Status change alerts
- [ ] Historical tracking
- [ ] Export to PDF

### Phase 3: Real-Time
- [ ] Auto-refresh (30s intervals)
- [ ] WebSocket status updates
- [ ] Push notifications
- [ ] Live activity feed

## 🔧 Technical Details

### Status Reader Cache
```python
class StatusReader:
    def __init__(self, cache_ttl=30):
        self.cache = {}
        self.cache_ttl = cache_ttl
    
    def read_agent_status(self, agent_id: str) -> dict:
        # Check cache
        # Read from file if expired
        # Parse JSON
        # Return normalized data
        pass
    
    def read_all_statuses(self) -> dict[str, dict]:
        # Read all 14 agent status files
        # Return dictionary keyed by agent_id
        pass
```

### Enhanced Embed Builder
```python
def create_agent_detail_embed(agent_data: dict) -> discord.Embed:
    embed = discord.Embed(
        title=f"🤖 {agent_data['agent_id']} Status Detail",
        description=agent_data['agent_name'],
        color=_get_status_color(agent_data['status']),
        timestamp=datetime.now()
    )
    
    # Add mission field
    embed.add_field(
        name="📋 Current Mission",
        value=agent_data['current_mission'],
        inline=False
    )
    
    # Add tasks (top 3)
    tasks = "\n".join([f"• {task}" for task in agent_data['current_tasks'][:3]])
    embed.add_field(name="🎯 Current Tasks", value=tasks, inline=False)
    
    # Add achievements (top 3)
    achievements = "\n".join([f"• {ach}" for ach in agent_data['achievements'][:3]])
    embed.add_field(name="🏆 Achievements", value=achievements, inline=False)
    
    return embed
```

## 🎯 Success Metrics
- All 14 agents visible
- Status updates within 30s
- <2 second load time
- Mobile-friendly layout
- Handles missing status files gracefully

## 📅 Timeline
- **Phase 1:** 30-45 minutes (basic enhancement)
- **Phase 2:** 1-2 hours (advanced features)
- **Phase 3:** 2-4 hours (real-time features)

## 🚀 Next Steps
1. Create `status_reader.py`
2. Enhance `SwarmStatusView`
3. Test with all 14 agents
4. Document usage
5. Create devlog

---
**Author:** Agent-5  
**Date:** 2025-10-11  
**Status:** READY FOR IMPLEMENTATION  

