# 💾 DATABASE INTEGRATION - COMPLETE GUIDE

**Category:** Database & Persistence  
**Author:** Agent-7  
**Date:** 2025-10-15  
**Tags:** database, sync, status, integration

---

## 🎯 WHEN TO USE

**Trigger:** EVERY cycle when status.json updates OR manual verification needed

**Who:** ALL agents (automatic via AgentLifecycle, manual for troubleshooting)

---

## 📋 WHAT IS DATABASE INTEGRATION?

**Purpose:** Sync agent status from status.json files to centralized database

**Why:** Captain needs database view for:
- Swarm-wide status monitoring
- Analytics and reporting
- Historical tracking
- Multi-agent coordination

---

## 🗃️ DATABASE TABLES

### **1. agent_workspaces Table**
**Stores:** Current agent status (mirrors status.json)

**Columns:**
- `agent_id` - Agent identifier (e.g., "Agent-7")
- `status` - Current status (ACTIVE, IDLE, BLOCKED, etc.)
- `last_updated` - Timestamp of last update
- `current_focus` - Current work description
- `cycle_count` - Number of cycles completed
- `points_earned` - Total points
- `current_mission` - Active mission

### **2. agent_status Table (Vector DB)**
**Stores:** Status embeddings for semantic search

**Purpose:** 
- Find agents by semantic similarity
- Search for agents working on related topics
- Discover agents with specific expertise

---

## 🔄 HOW SYNC WORKS

### **Automatic Sync (Recommended):**

```python
from src.core.agent_lifecycle import AgentLifecycle

lifecycle = AgentLifecycle('Agent-7')

# Every method auto-syncs to database!
lifecycle.start_cycle()        # ✅ Syncs
lifecycle.start_mission(...)   # ✅ Syncs
lifecycle.complete_task(...)   # ✅ Syncs
lifecycle.end_cycle(...)       # ✅ Syncs
```

**How it works:**
1. AgentLifecycle calls `_save_status()`
2. `_save_status()` updates status.json
3. (Future) Auto-sync to database via hook

### **Manual Sync (Troubleshooting):**

```bash
# Sync specific agent
python tools/sync_status_to_db.py --agent Agent-7

# Sync all agents
python tools/sync_status_to_db.py --all

# Verify sync worked
python tools/verify_db_sync.py --agent Agent-7
```

---

## ✅ VERIFICATION

### **Check status.json:**
```bash
cat agent_workspaces/Agent-7/status.json
```

### **Check database:**
```python
from src.db.queries import get_agent_status

status = get_agent_status('Agent-7')
print(status)  # Should match status.json
```

### **Verify sync timestamp:**
```bash
python tools/verify_db_sync.py --agent Agent-7

# Output should show:
# ✅ status.json: 2025-10-15T12:00:00Z
# ✅ database:    2025-10-15T12:00:00Z
# ✅ SYNCED (0 seconds lag)
```

---

## 🚨 TROUBLESHOOTING

### **Problem:** Database shows stale status

**Solution:**
```bash
# Force manual sync
python tools/sync_status_to_db.py --agent Agent-7 --force

# Verify
python tools/verify_db_sync.py --agent Agent-7
```

### **Problem:** Sync script not found

**Solution:**
```bash
# Create basic sync script (if missing)
python -c "
from pathlib import Path
import json

def sync_agent(agent_id):
    status_file = Path(f'agent_workspaces/{agent_id}/status.json')
    with open(status_file) as f:
        status = json.load(f)
    # TODO: Write to database
    print(f'✅ Synced {agent_id}')

sync_agent('Agent-7')
"
```

### **Problem:** Database schema mismatch

**Solution:**
```bash
# Run migrations
python -m src.db.migrate apply migrations/

# Re-sync
python tools/sync_status_to_db.py --all
```

---

## 📝 BEST PRACTICES

### ✅ DO:
- Use AgentLifecycle (auto-sync)
- Verify sync after critical updates
- Run manual sync if auto-sync fails
- Keep status.json and database in sync

### ❌ DON'T:
- Manually edit database (edit status.json instead)
- Skip sync verification
- Assume sync always works
- Let sync lag >1 cycle

---

## 🔗 RELATED GUIDES

- **STATUS_JSON_GUIDE.md** - status.json fields
- **CYCLE_PROTOCOLS.md** - When to update
- **AgentLifecycle class** - Auto-sync (src/core/agent_lifecycle.py)

---

**🐝 DATABASE = CAPTAIN'S EYES - KEEP IT SYNCED!** 💾

