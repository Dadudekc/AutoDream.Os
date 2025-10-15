# 📊 STATUS.JSON - COMPLETE GUIDE

**Last Updated:** 2025-10-15  
**Purpose:** Everything about status.json in ONE place

---

## 🎯 WHAT IT IS

**Single Source of Truth for agent state**

- **Location:** `agent_workspaces/Agent-X/status.json`
- **Update Frequency:** EVERY cycle (mandatory)
- **Read By:** 15+ tools, Captain, Discord bot, monitoring systems

---

## 🔍 WHO READS IT

1. **Captain Agent-4** - Tracks agent state, finds idle agents
2. **Discord bot** - !status, !livestatus commands
3. **Fuel monitor** - Determines GAS delivery
4. **Integrity validator** - Audits agent claims
5. **Swarm orchestrator** - Mission assignment
6. **Database sync** - agent_workspaces table
7. **Analytics** - Performance tracking

**If status.json is stale → Captain can't see you!** 🚨

---

## 📋 REQUIRED FIELDS

### Always Required:
```json
{
  "agent_id": "Agent-X",
  "agent_name": "Role Description",
  "status": "ACTIVE|IDLE|BLOCKED|WAITING|COMPLETE",
  "current_phase": "Current work description",
  "last_updated": "2025-10-15T12:00:00Z",
  "current_mission": "Mission name",
  "mission_priority": "CRITICAL|HIGH|MEDIUM|LOW"
}
```

### FSM Integration:
```json
{
  "fsm_state": "start|active|process|blocked|complete|end"
}
```

### Cycle Tracking:
```json
{
  "cycle_count": 42,
  "last_cycle": "2025-10-15T12:00:00Z"
}
```

### Work Tracking:
```json
{
  "current_tasks": ["Task 1", "Task 2"],
  "completed_tasks": ["Done 1", "Done 2"],
  "points_earned": 500,
  "achievements": ["First mission complete"]
}
```

### Planning:
```json
{
  "next_actions": ["Next 1", "Next 2"],
  "next_milestone": "Complete phase 2",
  "last_milestone": "Phase 1 complete"
}
```

### Blockers (when applicable):
```json
{
  "status": "BLOCKED",
  "blockers": ["Waiting for Captain approval", "Need DB access"]
}
```

---

## 🔄 WHEN TO UPDATE

### EVERY CYCLE START:
- Update `last_updated`
- Set `status` to "ACTIVE"
- Increment `cycle_count`
- Update `current_mission` (if new)

### DURING CYCLE:
- **Phase change** → `current_phase`
- **Task start** → Add to `current_tasks`
- **Task complete** → Move to `completed_tasks`, add `points_earned`
- **Get blocked** → `status`="BLOCKED", add to `blockers`

### EVERY CYCLE END:
- Update `completed_tasks`
- Update `next_actions`
- Update `last_updated`
- **COMMIT TO GIT**

---

## 💻 HOW TO UPDATE

### Option 1: AgentLifecycle (RECOMMENDED)
```python
from src.core.agent_lifecycle import AgentLifecycle

lifecycle = AgentLifecycle('Agent-X')

# Cycle start - automatic!
lifecycle.start_cycle()

# Mission start - automatic!
lifecycle.start_mission("Mission name", "HIGH")

# Task complete - automatic!
lifecycle.complete_task("Task name", points=100)

# Cycle end - automatic commit!
lifecycle.end_cycle(commit=True)
```

### Option 2: Manual (Quick edits)
```python
import json
from datetime import datetime, timezone

status_path = "agent_workspaces/Agent-X/status.json"
with open(status_path) as f:
    status = json.load(f)

status['last_updated'] = datetime.now(timezone.utc).isoformat()
status['status'] = 'ACTIVE'
status['cycle_count'] = status.get('cycle_count', 0) + 1

with open(status_path, 'w') as f:
    json.dump(status, f, indent=2)
```

---

## 📝 EXAMPLES

### Starting New Mission:
```json
{
  "status": "ACTIVE",
  "current_mission": "Analyze repos 51-60",
  "mission_priority": "HIGH",
  "current_phase": "Repo 51 analysis",
  "fsm_state": "active",
  "current_tasks": ["Clone repo", "Analyze purpose"],
  "cycle_count": 15,
  "last_updated": "2025-10-15T12:00:00Z"
}
```

### Task Complete:
```json
{
  "current_phase": "Repo 52 analysis",
  "current_tasks": ["Clone repo 52"],
  "completed_tasks": ["Repo 51 complete", "Devlog posted"],
  "points_earned": 100,
  "last_updated": "2025-10-15T13:00:00Z"
}
```

### Being Blocked:
```json
{
  "status": "BLOCKED",
  "current_phase": "Waiting for Captain",
  "blockers": ["Need approval", "Waiting for debate results"],
  "next_actions": ["Wait for Captain", "Review debate"],
  "last_updated": "2025-10-15T14:00:00Z"
}
```

### Mission Complete:
```json
{
  "status": "COMPLETE",
  "current_mission": "Analyze repos 51-60 - COMPLETE",
  "current_phase": "All 10 repos analyzed",
  "fsm_state": "complete",
  "completed_tasks": ["All 10 repos analyzed", "10 devlogs posted"],
  "achievements": ["First multi-repo analysis complete"],
  "points_earned": 1000,
  "next_actions": ["Await next mission"],
  "last_updated": "2025-10-15T15:00:00Z"
}
```

---

## 🔗 DATABASE SYNC

**Status.json syncs to database automatically!**

### Tables Affected:
1. `agent_workspaces` - Status, last_updated, cycle_count
2. `agent_status` (vector DB) - Embeddings for semantic search

### Auto-sync:
AgentLifecycle automatically syncs on each update.

---

## ⚠️ COMMON MISTAKES

### ❌ DON'T:
- Forget `last_updated` timestamp
- Use time-based estimates ("2 hours")
- Skip updates for multiple cycles
- Update without committing to git
- Use non-ISO timestamps

### ✅ DO:
- Update EVERY cycle
- Use cycle-based tracking
- Commit after updates
- Use ISO 8601 timestamps
- Use AgentLifecycle class

---

## 🚨 CONSEQUENCES OF NOT UPDATING

1. Captain can't find you → No new missions
2. Fuel monitor thinks idle → No GAS
3. Discord shows stale → Team thinks inactive
4. Validator flags → Audit fails
5. DB out of sync → Analytics broken
6. Swarm can't coordinate → Team breakdown

**BOTTOM LINE: Update status.json EVERY cycle!** ⚡

---

## 🔗 RELATED GUIDES

- **CYCLE_PROTOCOLS.md** - When to update status.json
- **AGENT_LIFECYCLE_FSM.md** - FSM state management
- **AgentLifecycle class** - Automated updates (src/core/agent_lifecycle.py)

---

**🐝 STATUS.JSON = CAPTAIN'S EYES - KEEP IT FRESH!** 👀

