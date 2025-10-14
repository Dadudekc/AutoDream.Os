# Discord Status View - Usage Guide
**Purpose:** View rich agent status.json data in Discord

## ✅ Implementation Complete

### Features Implemented
- ✅ **Status Reader Module:** `src/discord_commander/status_reader.py`
- ✅ **Enhanced Swarm Status View:** Rich status.json display
- ✅ **30-second cache:** Efficient file reading with TTL
- ✅ **14 agents supported:** All main + specialized agents
- ✅ **Summary statistics:** Total agents, active missions, points

## 🚀 How to Use

### Start the Discord Bot
```bash
python scripts/execution/run_discord_bot.py
```

**Note:** Unified into single Discord bot (consolidated from multiple versions)

### View Enhanced Status
In Discord, type:
```
!status
```

**You'll see:**
```
🤖 Swarm Status Dashboard
Real-time agent status from status.json files
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Overall Status
• Total Agents: 14
• Active Missions: 6
• Total Points: 25,000+

✅ Agent-1
Role: Integration & Core Systems...
Status: SURVEY_MISSION_COMPLETED
Mission: Services Integration Domain Survey - COMPL...
Task: Survey mission completed successfully

🟢 Agent-2
Role: Core Module Consolidation...
Status: ACTIVE_AGENT_MODE
Mission: 8-Week Sprint: Core Module Consolidation
Task: C-055 monitoring and execution support

... (all 14 agents displayed)

Cached: 14 agents | TTL: 30s
```

### Other Commands
- **`!message <agent-id> <message>`** - Send message to specific agent
- **`!broadcast <message>`** - Send to all 8 agents
- **`!agents`** - List all agents with coordinates
- **`!commands`** - Show help

## 📊 Status Display Format

### For Each Agent
```
<emoji> Agent-X
Role: <agent_name>
Status: <status>
Mission: <current_mission>
Task: <first current_task>
```

### Status Emojis
- ✅ Complete / Success
- 💤 Rest / Standby
- 🟢 Active / In Progress
- 🔴 Error / Failed
- 🟡 Unknown / Other

## 🔧 Technical Details

### Status Reader
**File:** `src/discord_commander/status_reader.py`

**Features:**
- Reads from `agent_workspaces/Agent-X/status.json`
- 30-second cache TTL (configurable)
- Normalizes data structure
- Handles missing/malformed files
- Extracts points from various formats

**Cache Settings:**
```python
status_reader = StatusReader(
    workspace_dir="agent_workspaces",
    cache_ttl=30  # seconds
)
```

### Data Normalization
The status reader normalizes data to a standard format:
```python
{
    "agent_id": "Agent-X",
    "agent_name": "Role Name",
    "status": "ACTIVE",
    "current_phase": "PHASE_NAME",
    "current_mission": "Mission description",
    "mission_priority": "HIGH",
    "current_tasks": [...],
    "completed_tasks": [...],
    "achievements": [...],
    "next_actions": [...],
    "points": "13,550 pts"  # extracted from various locations
}
```

### Summary Statistics
- **Total Agents:** 8 main agents (Agent-1 through Agent-8 only)
- **Active Missions:** Agents not in COMPLETE/REST status
- **Total Points:** Sum of all agent points (from various point fields)
- **Note:** Role workspaces (Agent-SRC-1, etc.) are NOT separate agents

## 📁 Project Structure

```
src/discord_commander/
├── status_reader.py              # NEW: Read & parse status.json
├── messaging_controller_views.py # ENHANCED: Rich status display
├── messaging_commands.py         # Unchanged: !swarm_status command
└── enhanced_bot.py               # Unchanged: Bot manager

agent_workspaces/
├── Agent-1/status.json
├── Agent-2/status.json
├── ... (14 total)
```

## 🎯 What Changed

### Before Enhancement
- **Data Source:** `messaging_service.agent_data` (coordinates only)
- **Display:** Active/Inactive + coordinates
- **Information:** Minimal

### After Enhancement
- **Data Source:** `agent_workspaces/*/status.json` files
- **Display:** Role, status, mission, current task
- **Information:** Rich real-time agent state
- **Cache:** 30-second TTL for efficiency

## 🧪 Testing

### Test Status Reader
```bash
python test_status_reader.py
```

**Output:**
```
✅ Read 8 agent statuses

  - Agent-1: SURVEY_MISSION_COMPLETED
    Mission: Services Integration Domain Survey - COM...
    Tasks: 5 current

  ... (all 8 main agents)

📊 Cache Stats:
  - Cached agents: 8
  - Cache TTL: 30s
```

### Test in Discord
1. Start bot: `python scripts/execution/run_discord_bot.py`
2. Type: `!status`
3. Verify: All 8 main agents display with rich data from status.json
4. Verify: Summary shows total agents, active missions, points

## 🐛 Troubleshooting

### "No Status Data" Error
**Cause:** Cannot read status.json files  
**Fix:** Verify `agent_workspaces/` directory exists and contains status.json files

### Missing Agent Data
**Cause:** status.json file missing or malformed  
**Fix:** Check agent workspace directory and JSON syntax

### Cache Not Refreshing
**Cause:** Cache TTL not expired  
**Fix:** Wait 30 seconds or restart bot to clear cache

## 🚀 Future Enhancements

### Phase 2 (Planned)
- [ ] Individual agent detail modals (click agent for full status)
- [ ] Progress bars for sprint points
- [ ] Status change alerts (notify when agent status changes)
- [ ] Historical tracking (track status over time)

### Phase 3 (Planned)
- [ ] Auto-refresh (30s intervals, no manual refresh needed)
- [ ] WebSocket updates (real-time status changes)
- [ ] Push notifications (alert on important events)
- [ ] Live activity feed (show recent agent actions)

## 📝 Notes

- **Cache TTL:** 30 seconds balances performance vs. freshness
- **8 Agents Only:** Main agents (Agent-1 through Agent-8) - role workspaces are NOT separate agents
- **Embed limits:** Discord limits 25 fields per embed, we display all 8 agents
- **Mobile friendly:** Layout works on mobile Discord clients

---

**Implementation:** Agent-5  
**Date:** 2025-10-11  
**Status:** ✅ COMPLETE AND TESTED  
**Files Changed:** 2 new, 1 enhanced  

