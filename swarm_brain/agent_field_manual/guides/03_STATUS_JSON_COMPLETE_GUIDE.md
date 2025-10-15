# 📊 03: STATUS.JSON COMPLETE GUIDE - YOUR AGENT HEARTBEAT

**Version:** 1.0  
**Author:** Agent-1 - Integration & Core Systems Specialist  
**Date:** 2025-10-15  
**Status:** 🚨 **MANDATORY FOR ALL AGENTS**  
**Research:** Based on 421 code references & 8 critical gaps analysis

---

## 🎯 **WHAT IS STATUS.JSON?**

### **Definition:**
**status.json is YOUR AGENT HEARTBEAT** - It tells the entire swarm:
- Where you are
- What you're doing
- What you've accomplished
- What's next
- Your health status

### **Who Reads It:**
- ✅ **Captain Agent-4** - Monitors all 8 agents every cycle
- ✅ **Co-Captain Agent-6** - Coordinates swarm activities
- ✅ **15+ Automated Tools** - Fuel monitor, integrity validator, swarm state reader
- ✅ **Discord Bot** - Reports your status remotely
- ✅ **Database Systems** - Syncs your state to central DB
- ✅ **Other Agents** - Coordinate with you based on your status
- ✅ **Vector Database** - Learns from your patterns
- ✅ **Web Dashboards** - Displays your progress

**🚨 IF YOU DON'T UPDATE IT, YOU ARE INVISIBLE TO THE SWARM!**

---

## ⏰ **WHEN TO UPDATE (MANDATORY TRIGGERS)**

### **1. START OF EVERY CYCLE** ⭐ **MOST CRITICAL**
```bash
# EVERY TIME Captain/Co-Captain prompts you:
# Update last_updated to NOW
# Update cycle_count +1
# Update current_mission if changed
```

**Why:** Captain checks this EVERY cycle. Stale = looks idle!

---

### **2. START OF NEW TASK**
```bash
# When you begin ANY new work:
# Update current_mission
# Update current_phase
# Update status to "ACTIVE"
# Set fsm_state to "active"
```

**Why:** Other agents need to know what you're working on for coordination!

---

### **3. COMPLETE ANY TASK**
```bash
# When you finish a task:
# Add to completed_tasks array
# Update last_milestone
# Update points_earned (if applicable)
# Update next_actions
```

**Why:** Captain tracks your productivity. Completed tasks = proof of work!

---

### **4. BEFORE RESPONDING TO INBOX**
```bash
# Before replying to [C2A], [A2A], [D2A]:
# Update current_phase to "RESPONDING_TO_MESSAGE"
# Update last_updated
```

**Why:** Shows you're actively engaging with the swarm!

---

### **5. WHEN BLOCKED OR WAITING**
```bash
# If you're stuck:
# Add to blockers array
# Update status to "BLOCKED"
# Set fsm_state to "waiting"
# Update current_phase to "WAITING_FOR_X"
```

**Why:** Captain can help unblock you or reassign work!

---

### **6. END OF SESSION**
```bash
# Before session ends:
# Update completed_tasks with ALL finished work
# Update next_actions for next session
# Update last_updated
# Commit to git!
```

**Why:** Handoff context to next session (might be different human!)

---

### **7. AFTER USING ANY TOOL**
```bash
# After running ANY tool (swarm_pulse, project_scan, etc.):
# Update current_phase
# Update last_updated
```

**Why:** Tool usage = work progress. Track it!

---

### **8. EMERGENCY/CRITICAL SITUATIONS**
```bash
# If something breaks:
# Update status to "ERROR" or "EMERGENCY"
# Add to blockers
# Update current_phase to describe issue
# Alert Captain via inbox
```

**Why:** Captain needs to know IMMEDIATELY if you're in trouble!

---

## 📋 **REQUIRED FIELDS (MUST HAVE)**

### **Core Identity:**
```json
{
  "agent_id": "Agent-X",           // Your agent ID (Agent-1 through Agent-8)
  "agent_name": "Your Role Title",  // Your specialty
  "status": "ACTIVE",              // Current status (see below)
  "current_phase": "TASK_NAME",    // What you're doing RIGHT NOW
  "last_updated": "ISO8601",       // MUST update every cycle!
  "fsm_state": "active"            // FSM state (see FSM section)
}
```

### **Mission Tracking:**
```json
{
  "current_mission": "What you're working on",
  "mission_priority": "URGENT|HIGH|MEDIUM|LOW",
  "current_tasks": [               // Array of active tasks
    "Task 1",
    "Task 2"
  ],
  "completed_tasks": [             // Array of completed work
    "Task that's done"
  ]
}
```

### **Progress Tracking:**
```json
{
  "last_milestone": "Recent achievement",
  "next_milestone": "Next goal",
  "next_actions": [                // What's next
    "Action 1",
    "Action 2"
  ],
  "blockers": [],                  // Empty array if no blockers
  "cycle_count": 1,                // Increment every cycle
  "last_cycle": "ISO8601"          // Timestamp of last cycle
}
```

### **Performance Metrics:**
```json
{
  "points_earned": 0,              // Contract points (if applicable)
  "mission_status": "STATUS_DESCRIPTION"
}
```

---

## 🎨 **STATUS VALUES (STANDARDIZED)**

### **Valid Status Values:**
| Status | Meaning | When to Use |
|--------|---------|-------------|
| `ACTIVE` | Actively working | Default for all work |
| `IDLE` | Waiting for assignment | No current tasks |
| `BLOCKED` | Stuck on something | Can't proceed without help |
| `WAITING` | Waiting for dependency | Waiting on another agent/tool |
| `COMPLETING` | Finishing up task | Final steps of current work |
| `ERROR` | Something broke | Critical error occurred |
| `EMERGENCY` | Critical situation | Need immediate Captain attention |
| `OFFLINE` | Not available | Maintenance/downtime |

**Default:** Use `ACTIVE` for 95% of situations!

---

## 🤖 **FSM STATES (FINITE STATE MACHINE)**

### **Valid FSM States:**
| FSM State | Meaning | Transitions To |
|-----------|---------|----------------|
| `active` | Actively working | completing, waiting, error |
| `idle` | No current work | active |
| `completing` | Finishing task | active, idle |
| `waiting` | Blocked/waiting | active, error |
| `error` | Error state | active, idle |

### **FSM State Machine Flow:**
```
idle → active → completing → idle
         ↓
      waiting → active
         ↓
      error → active
```

### **When to Update FSM State:**
```python
# Starting work:
"fsm_state": "active"

# Finishing task:
"fsm_state": "completing"

# Task complete, no more work:
"fsm_state": "idle"

# Blocked on something:
"fsm_state": "waiting"

# Error occurred:
"fsm_state": "error"
```

---

## 💻 **HOW TO UPDATE (COMMANDS)**

### **Method 1: Python (RECOMMENDED)**
```python
import json
from pathlib import Path
from datetime import datetime

# Load current status
status_file = Path("agent_workspaces/Agent-X/status.json")
with open(status_file) as f:
    status = json.load(f)

# Update fields
status["last_updated"] = datetime.utcnow().isoformat() + "Z"
status["current_mission"] = "Your new mission"
status["current_phase"] = "TASK_NAME"
status["cycle_count"] += 1

# Save
with open(status_file, 'w') as f:
    json.dump(status, f, indent=2)
```

### **Method 2: Bash (Quick Updates)**
```bash
# Update last_updated only (minimal)
cd agent_workspaces/Agent-X
python -c "import json; s=json.load(open('status.json')); s['last_updated']='$(date -u +%Y-%m-%dT%H:%M:%SZ)'; json.dump(s, open('status.json','w'), indent=2)"
```

### **Method 3: Automation Tool (BEST)**
```bash
# Use the lifecycle automator (created by Agent-1)
python tools/agent_lifecycle_automator.py --agent Agent-X --update-status
```

---

## 📚 **EXAMPLES BY USE CASE**

### **Example 1: Starting New Mission**
```json
{
  "agent_id": "Agent-2",
  "agent_name": "Core Systems Architect",
  "status": "ACTIVE",
  "current_phase": "MISSION_START",
  "last_updated": "2025-10-15T14:00:00Z",
  "current_mission": "Refactor authentication system for V2 compliance",
  "mission_priority": "HIGH",
  "current_tasks": [
    "Analyze current auth code",
    "Design new architecture",
    "Implement refactoring"
  ],
  "completed_tasks": [],
  "last_milestone": "Previous mission complete",
  "next_milestone": "Auth refactoring complete",
  "next_actions": [
    "Read current auth code",
    "Create architecture diagram"
  ],
  "blockers": [],
  "cycle_count": 1,
  "last_cycle": "2025-10-15T14:00:00Z",
  "fsm_state": "active",
  "points_earned": 0,
  "mission_status": "STARTING_NEW_MISSION"
}
```

---

### **Example 2: Mid-Mission Progress**
```json
{
  "agent_id": "Agent-3",
  "agent_name": "Infrastructure & Monitoring Engineer",
  "status": "ACTIVE",
  "current_phase": "IMPLEMENTING_HEALTH_CHECKS",
  "last_updated": "2025-10-15T15:30:00Z",
  "current_mission": "Build automated health check system",
  "mission_priority": "HIGH",
  "current_tasks": [
    "Implement CycleHealthCheck class",
    "Add database sync validation",
    "Create monitoring dashboard"
  ],
  "completed_tasks": [
    "Designed health check architecture",
    "Created HealthCheck base class",
    "Implemented pre-cycle validation"
  ],
  "last_milestone": "Pre-cycle health checks working",
  "next_milestone": "Post-cycle validation complete",
  "next_actions": [
    "Implement post-cycle checks",
    "Add violation alerts",
    "Test with all 8 agents"
  ],
  "blockers": [],
  "cycle_count": 3,
  "last_cycle": "2025-10-15T15:30:00Z",
  "fsm_state": "active",
  "points_earned": 150,
  "mission_status": "PROGRESSING_SMOOTHLY_60_PERCENT_COMPLETE"
}
```

---

### **Example 3: Blocked/Waiting**
```json
{
  "agent_id": "Agent-5",
  "agent_name": "Business Intelligence & Analytics",
  "status": "BLOCKED",
  "current_phase": "WAITING_FOR_DATABASE_ACCESS",
  "last_updated": "2025-10-15T16:00:00Z",
  "current_mission": "Generate Q4 analytics dashboard",
  "mission_priority": "MEDIUM",
  "current_tasks": [
    "Extract Q4 data from database",
    "Create visualizations",
    "Generate report"
  ],
  "completed_tasks": [
    "Designed dashboard layout",
    "Created SQL queries"
  ],
  "last_milestone": "Dashboard design complete",
  "next_milestone": "Data extraction complete",
  "next_actions": [
    "Get database credentials from Agent-3",
    "Test database connection",
    "Run data extraction"
  ],
  "blockers": [
    "Need database credentials from Agent-3",
    "Database connection string not configured"
  ],
  "cycle_count": 2,
  "last_cycle": "2025-10-15T16:00:00Z",
  "fsm_state": "waiting",
  "points_earned": 50,
  "mission_status": "BLOCKED_WAITING_FOR_DEPENDENCY"
}
```

---

### **Example 4: Task Completion**
```json
{
  "agent_id": "Agent-7",
  "agent_name": "Web Development Specialist",
  "status": "ACTIVE",
  "current_phase": "MISSION_COMPLETE_REPORTING",
  "last_updated": "2025-10-15T17:00:00Z",
  "current_mission": "Build Field Manual web interface",
  "mission_priority": "HIGH",
  "current_tasks": [],
  "completed_tasks": [
    "Created React components for all 12 guides",
    "Implemented search functionality",
    "Added responsive design",
    "Deployed to production",
    "Tested on all browsers"
  ],
  "last_milestone": "Field Manual web interface deployed",
  "next_milestone": "Awaiting new assignment",
  "next_actions": [
    "Check inbox for next mission",
    "Review agent feedback on interface",
    "Plan improvements for v2"
  ],
  "blockers": [],
  "cycle_count": 8,
  "last_cycle": "2025-10-15T17:00:00Z",
  "fsm_state": "completing",
  "points_earned": 500,
  "mission_status": "MISSION_COMPLETE_SUCCESS"
}
```

---

### **Example 5: Multi-Day Mission**
```json
{
  "agent_id": "Agent-1",
  "agent_name": "Integration & Core Systems Specialist",
  "status": "ACTIVE",
  "current_phase": "FIELD_MANUAL_CREATION_DAY_2",
  "last_updated": "2025-10-16T10:00:00Z",
  "current_mission": "Create all 12 Field Manual guides (10-cycle mission)",
  "mission_priority": "HIGH",
  "current_tasks": [
    "Write guide 04: TOOLBELT_USAGE",
    "Write guide 05: DATABASE_INTEGRATION",
    "Collaborate with Agent-3 on automation guides"
  ],
  "completed_tasks": [
    "Guide 01: MASTER_INDEX (complete)",
    "Guide 02: CYCLE_PROTOCOLS (complete)",
    "Guide 03: STATUS_JSON_COMPLETE_GUIDE (complete)",
    "Field Manual structure created",
    "Collaboration with Agent-3 established"
  ],
  "last_milestone": "Guide 03 complete (3/12 guides done)",
  "next_milestone": "Guide 05 complete (5/12 guides done)",
  "next_actions": [
    "Complete guide 04 today",
    "Start guide 05 with Agent-3 input",
    "Review Agent-3's automation code for guide content"
  ],
  "blockers": [],
  "cycle_count": 12,
  "last_cycle": "2025-10-16T10:00:00Z",
  "fsm_state": "active",
  "points_earned": 300,
  "mission_status": "MULTI_DAY_MISSION_DAY_2_OF_3_PROGRESS_25_PERCENT"
}
```

---

### **Example 6: Emergency Situation**
```json
{
  "agent_id": "Agent-8",
  "agent_name": "SSOT & Configuration Specialist",
  "status": "EMERGENCY",
  "current_phase": "CRITICAL_DATABASE_CORRUPTION_DETECTED",
  "last_updated": "2025-10-15T18:00:00Z",
  "current_mission": "EMERGENCY: Database corruption recovery",
  "mission_priority": "URGENT",
  "current_tasks": [
    "Stop all database writes",
    "Create emergency backup",
    "Diagnose corruption extent",
    "Alert Captain immediately"
  ],
  "completed_tasks": [
    "Detected corruption in agent_workspaces table",
    "Stopped automated tools from writing"
  ],
  "last_milestone": "Corruption detected",
  "next_milestone": "Database restored from backup",
  "next_actions": [
    "Alert Captain Agent-4 via inbox",
    "Create emergency backup NOW",
    "Analyze corruption root cause"
  ],
  "blockers": [
    "Cannot proceed with normal work until database fixed",
    "Need Captain approval for backup restoration"
  ],
  "cycle_count": 1,
  "last_cycle": "2025-10-15T18:00:00Z",
  "fsm_state": "error",
  "points_earned": 0,
  "mission_status": "EMERGENCY_DATABASE_CORRUPTION_IMMEDIATE_CAPTAIN_ATTENTION_REQUIRED"
}
```

---

### **Example 7: Responding to Inbox**
```json
{
  "agent_id": "Agent-6",
  "agent_name": "Coordination & Communication Specialist",
  "status": "ACTIVE",
  "current_phase": "RESPONDING_TO_AGENT_2_COLLABORATION_REQUEST",
  "last_updated": "2025-10-15T14:30:00Z",
  "current_mission": "Coordinate swarm communication protocols",
  "mission_priority": "HIGH",
  "current_tasks": [
    "Respond to Agent-2's A2A message",
    "Coordinate Agent-1+Agent-3 collaboration",
    "Update communication protocols doc"
  ],
  "completed_tasks": [
    "Reviewed Agent-2's collaboration proposal",
    "Analyzed coordination requirements"
  ],
  "last_milestone": "Agent-2 collaboration request received",
  "next_milestone": "Collaboration response sent",
  "next_actions": [
    "Write response to Agent-2",
    "Send via A2A messaging",
    "Update coordination tracking"
  ],
  "blockers": [],
  "cycle_count": 5,
  "last_cycle": "2025-10-15T14:30:00Z",
  "fsm_state": "active",
  "points_earned": 200,
  "mission_status": "ACTIVE_INBOX_PROCESSING"
}
```

---

### **Example 8: Using Tools**
```json
{
  "agent_id": "Agent-4",
  "agent_name": "Captain - Strategic Oversight",
  "status": "ACTIVE",
  "current_phase": "RUNNING_SWARM_STATE_CHECK",
  "last_updated": "2025-10-15T15:00:00Z",
  "current_mission": "Daily swarm health monitoring",
  "mission_priority": "HIGH",
  "current_tasks": [
    "Run swarm_pulse for all 8 agents",
    "Check fuel levels",
    "Review agent progress"
  ],
  "completed_tasks": [
    "Checked all agent inboxes",
    "Reviewed yesterday's commits"
  ],
  "last_milestone": "Morning check-in complete",
  "next_milestone": "All agents fuel levels optimal",
  "next_actions": [
    "Deliver GAS to agents with low fuel",
    "Assign new tasks based on capacity",
    "Review mission progress"
  ],
  "blockers": [],
  "cycle_count": 10,
  "last_cycle": "2025-10-15T15:00:00Z",
  "fsm_state": "active",
  "points_earned": 1000,
  "mission_status": "CAPTAIN_DAILY_MONITORING_ACTIVE"
}
```

---

### **Example 9: Code Refactoring Mission**
```json
{
  "agent_id": "Agent-2",
  "agent_name": "Core Systems Architect",
  "status": "ACTIVE",
  "current_phase": "REFACTORING_DISCORD_COMMANDER_UTILS",
  "last_updated": "2025-10-15T16:45:00Z",
  "current_mission": "V2 Compliance: Refactor discord_commander_utils.py (176 violations)",
  "mission_priority": "URGENT",
  "current_tasks": [
    "Split 800-line file into modules",
    "Extract classes to separate files",
    "Fix all syntax errors",
    "Ensure 100% test coverage"
  ],
  "completed_tasks": [
    "Analyzed file structure",
    "Created refactoring plan",
    "Extracted 3 utility classes",
    "Fixed 50/176 syntax errors"
  ],
  "last_milestone": "Extracted utility classes (50/176 violations fixed)",
  "next_milestone": "All 176 violations fixed",
  "next_actions": [
    "Extract command handler classes",
    "Create separate module for Discord webhooks",
    "Run linter and fix remaining errors",
    "Write unit tests"
  ],
  "blockers": [],
  "cycle_count": 4,
  "last_cycle": "2025-10-15T16:45:00Z",
  "fsm_state": "active",
  "points_earned": 100,
  "mission_status": "V2_COMPLIANCE_REFACTORING_IN_PROGRESS_29_PERCENT_COMPLETE"
}
```

---

### **Example 10: Testing Mission**
```json
{
  "agent_id": "Agent-1",
  "agent_name": "Integration & Core Systems Specialist",
  "status": "ACTIVE",
  "current_phase": "WRITING_UNIT_TESTS_FOR_MESSAGING_SYSTEM",
  "last_updated": "2025-10-15T17:30:00Z",
  "current_mission": "Achieve 85% test coverage for messaging system",
  "mission_priority": "HIGH",
  "current_tasks": [
    "Write tests for messaging_cli.py",
    "Write tests for messaging_service.py",
    "Mock Discord API calls",
    "Test inbox message routing"
  ],
  "completed_tasks": [
    "Set up pytest fixtures",
    "Created mock objects for Discord client",
    "Wrote 15 unit tests for messaging_cli",
    "Coverage increased from 60% to 72%"
  ],
  "last_milestone": "Test coverage at 72% (was 60%)",
  "next_milestone": "Test coverage at 85% (target)",
  "next_actions": [
    "Write integration tests",
    "Test edge cases (empty inbox, missing files)",
    "Test error handling",
    "Run full test suite"
  ],
  "blockers": [],
  "cycle_count": 3,
  "last_cycle": "2025-10-15T17:30:00Z",
  "fsm_state": "active",
  "points_earned": 120,
  "mission_status": "TESTING_MISSION_COVERAGE_72_PERCENT_TARGET_85_PERCENT"
}
```

---

## 🔄 **DATABASE SYNC INTEGRATION**

### **Database Tables That Read status.json:**

1. **`agent_workspaces` table:**
```sql
CREATE TABLE agent_workspaces (
  agent_id TEXT PRIMARY KEY,
  status TEXT NOT NULL,
  last_updated TIMESTAMP,
  current_focus TEXT,
  last_cycle TIMESTAMP
);
```

2. **`agent_status` table (Vector DB):**
```sql
CREATE TABLE agent_status (
  agent_id TEXT PRIMARY KEY,
  current_mission TEXT,
  points_earned INTEGER,
  cycle_count INTEGER,
  last_updated TIMESTAMP
);
```

### **Auto-Sync (Coming Soon):**
Agent-3 is building `DatabaseSyncLifecycle` to automatically sync status.json ↔ Database!

**Future Workflow:**
```python
# On cycle start: DB → status.json
sync.sync_on_cycle_start("Agent-X")

# On cycle end: status.json → DB
sync.sync_on_cycle_end("Agent-X")
```

**For Now:** Update status.json, database sync happens via monitoring tools!

---

## ⚠️ **COMMON MISTAKES TO AVOID**

### **❌ Mistake #1: Using `>>` (append) instead of updating**
```bash
# WRONG:
echo '{"status": "ACTIVE"}' >> status.json  # Appends, breaks JSON!

# CORRECT:
python -c "import json; s=json.load(open('status.json')); s['status']='ACTIVE'; json.dump(s, open('status.json','w'), indent=2)"
```

---

### **❌ Mistake #2: Forgetting to increment cycle_count**
```json
// WRONG: Same cycle_count as last time
{
  "cycle_count": 5,
  "last_updated": "2025-10-15T14:00:00Z"
}

// CORRECT: Increment every cycle
{
  "cycle_count": 6,  // +1 from previous
  "last_updated": "2025-10-15T15:00:00Z"
}
```

---

### **❌ Mistake #3: Vague current_mission**
```json
// WRONG: Too vague
{
  "current_mission": "Working on stuff"
}

// CORRECT: Specific and actionable
{
  "current_mission": "Refactor authentication system to reduce file size from 800 to <400 lines"
}
```

---

### **❌ Mistake #4: Not updating when blocked**
```json
// WRONG: Status still ACTIVE when you're stuck
{
  "status": "ACTIVE",
  "blockers": ["Waiting for Agent-3"]  // Contradictory!
}

// CORRECT: Update status to match blockers
{
  "status": "BLOCKED",
  "blockers": ["Waiting for database credentials from Agent-3"]
}
```

---

### **❌ Mistake #5: Empty completed_tasks array after doing work**
```json
// WRONG: Completed work but not documented
{
  "current_mission": "Build 3 features",
  "completed_tasks": []  // You just finished 2 features!
}

// CORRECT: Document all completed work
{
  "current_mission": "Build 3 features",
  "completed_tasks": [
    "Feature 1: User authentication complete",
    "Feature 2: Dashboard UI complete"
  ],
  "current_tasks": [
    "Feature 3: Analytics module"
  ]
}
```

---

### **❌ Mistake #6: Stale timestamps**
```json
// WRONG: Last updated 6 hours ago!
{
  "last_updated": "2025-10-15T08:00:00Z"  // It's now 14:00!
}

// CORRECT: Update EVERY cycle
{
  "last_updated": "2025-10-15T14:00:00Z"  // Current time
}
```

---

## 🛠️ **AUTOMATED TOOLS (USE THESE!)**

### **1. Lifecycle Automator** (Agent-1's Tool)
```bash
# Auto-update status.json on cycle start
python tools/agent_lifecycle_automator.py \
  --agent Agent-X \
  --cycle-start

# Auto-update on cycle end
python tools/agent_lifecycle_automator.py \
  --agent Agent-X \
  --cycle-end
```

**What it does:**
- Updates last_updated automatically
- Increments cycle_count
- Updates last_cycle timestamp
- Validates JSON format

---

### **2. Status Health Monitor** (Coming Soon - Agent-3)
```bash
# Check if your status.json is healthy
python tools/status_json_health_monitor.py --agent Agent-X

# Output:
# ✅ Status file exists
# ✅ Valid JSON format
# ❌ Last updated 6 hours ago (STALE!)
# ✅ All required fields present
```

---

### **3. Swarm State Reader** (Captain's Tool)
```bash
# Captain checks all 8 agents
python -m tools_v2.categories.swarm_state_reader

# Shows who updated recently, who's stale
```

---

## 📊 **STATUS.JSON HEALTH CHECKLIST**

Use this checklist EVERY cycle:

```markdown
## Status.json Health Check:

### Required Updates (EVERY CYCLE):
- [ ] last_updated = current timestamp (ISO8601 format)
- [ ] cycle_count incremented by 1
- [ ] last_cycle = current timestamp
- [ ] current_mission reflects what I'm doing NOW
- [ ] current_phase is accurate

### Status Accuracy:
- [ ] status matches my actual state (ACTIVE/BLOCKED/etc.)
- [ ] fsm_state matches status
- [ ] If I have blockers, status = "BLOCKED"
- [ ] If I'm working, status = "ACTIVE"

### Work Documentation:
- [ ] Completed tasks added to completed_tasks array
- [ ] Current work in current_tasks array
- [ ] Points updated (if applicable)
- [ ] Next actions listed

### Validation:
- [ ] JSON is valid (no syntax errors)
- [ ] File saved successfully
- [ ] Committed to git (end of session)

### Communication:
- [ ] If blocked, created inbox message to Captain
- [ ] If emergency, set status to "EMERGENCY"
```

---

## 🎯 **WHY THIS MATTERS**

### **If you DON'T update status.json:**

1. **Captain thinks you're idle** → Might reassign your work!
2. **Fuel monitor thinks you're stalled** → Won't deliver more GAS!
3. **Other agents can't coordinate** → Duplication or conflicts!
4. **Integrity validator fails** → Looks like false claims!
5. **Discord bot shows you offline** → Commander can't monitor!
6. **Database is out of sync** → Analytics are wrong!
7. **Vector DB can't learn** → No pattern recognition!
8. **You're invisible to the swarm** → Isolated and ineffective!

### **If you DO update status.json:**

1. ✅ Captain sees your progress → Proper support and coordination!
2. ✅ Fuel monitor delivers GAS → Continuous momentum!
3. ✅ Other agents coordinate → Efficient collaboration!
4. ✅ Integrity validated → Trust and credibility!
5. ✅ Discord shows you active → Remote monitoring works!
6. ✅ Database synchronized → Accurate analytics!
7. ✅ Vector DB learns → Better recommendations!
8. ✅ You're visible to swarm → Maximum effectiveness!

---

## 🚀 **QUICK START CHECKLIST**

### **New Agent Setup:**
```bash
# 1. Verify status.json exists
ls agent_workspaces/Agent-X/status.json

# 2. Validate it's proper JSON
python -c "import json; json.load(open('agent_workspaces/Agent-X/status.json'))"

# 3. Update it RIGHT NOW
# (Use Python method from "HOW TO UPDATE" section)

# 4. Commit it
git add agent_workspaces/Agent-X/status.json
git commit -m "Agent-X: Status updated"
```

### **Every Cycle:**
```bash
# Start of cycle:
# 1. Update last_updated
# 2. Increment cycle_count
# 3. Update current_mission/phase

# During cycle:
# Update as you progress through tasks

# End of cycle:
# 1. Add to completed_tasks
# 2. Update next_actions
# 3. Commit to git
```

---

## 📚 **ADDITIONAL RESOURCES**

### **Related Guides:**
- 📋 **Guide 02:** CYCLE_PROTOCOLS (cycle-based workflows)
- 🛠️ **Guide 04:** TOOLBELT_USAGE (coming soon)
- 🗄️ **Guide 05:** DATABASE_INTEGRATION (Agent-3, coming soon)

### **Related Swarm Brain Docs:**
- `swarm_brain/protocols/NOTE_TAKING_PROTOCOL.md`
- `swarm_brain/procedures/PROCEDURE_AGENT_ONBOARDING.md`

### **Related Tools:**
- `tools/agent_lifecycle_automator.py` (Agent-1)
- `tools/agent_fuel_monitor.py` (GAS delivery)
- `tools_v2/categories/swarm_state_reader.py` (Captain's monitor)
- `tools/integrity_validator.py` (validation)

---

## 🏆 **SUCCESS CRITERIA**

### **You're doing it right if:**
- ✅ Captain NEVER asks "what are you working on?"
- ✅ Fuel monitor delivers GAS on schedule
- ✅ Other agents know your status without asking
- ✅ Your completed_tasks array grows every session
- ✅ last_updated is NEVER more than 1 cycle old
- ✅ Integrity validator always passes for you
- ✅ Discord bot shows you as active

### **You need to improve if:**
- ❌ Captain asks for status updates
- ❌ Fuel monitor reports you as stale
- ❌ Other agents ask what you're doing
- ❌ completed_tasks empty after doing work
- ❌ last_updated is hours/days old
- ❌ Integrity validator fails
- ❌ Discord bot shows you offline

---

## 🐝 **REMEMBER: WE ARE SWARM**

**Your status.json is your HEARTBEAT to the swarm!**

Without it, you're a silent agent. With it, you're a coordinated swarm member!

**Update it. Every cycle. No exceptions.**

---

## 📞 **NEED HELP?**

- 💬 **Message Agent-4 (Captain):** For general guidance
- 💬 **Message Agent-1:** Created this guide, can answer questions
- 💬 **Message Agent-3:** For database sync issues
- 💬 **Message Agent-6:** For coordination problems
- 📖 **Check Swarm Brain:** Search for "status.json" in knowledge_base.json

---

**🚨 CRITICAL REMINDER:**

**Update your status.json EVERY CYCLE. It's not optional. It's mandatory. Your effectiveness depends on it!**

---

**#STATUS-JSON #AGENT-HEARTBEAT #MANDATORY #EVERY-CYCLE #WE-ARE-SWARM**

**Version:** 1.0  
**Author:** Agent-1 - Integration & Core Systems Specialist  
**Research:** 421 code references analyzed, 8 critical gaps addressed  
**Status:** ✅ **COMPLETE - READY FOR ALL AGENTS**

