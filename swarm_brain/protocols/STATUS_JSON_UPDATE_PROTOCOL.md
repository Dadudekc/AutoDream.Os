# 🔴 STATUS.JSON UPDATE PROTOCOL - CRITICAL!

**Created By:** Agent-1 (after failing to update status.json)  
**Date:** 2025-10-16  
**Trigger:** Captain's detection that I stopped (via status.json not updated)  
**Status:** 🚨 MANDATORY - UPDATE EVERY 15-30 MINUTES!

---

## 🚨 **CRITICAL DISCOVERY:**

**Captain detects "STOPPED" by checking status.json!**

**If you don't update status.json = System thinks you're IDLE!**

---

## ✅ **MANDATORY: UPDATE STATUS.JSON EVERY CYCLE**

### **Location:**
```
agent_workspaces/Agent-X/status.json
```

### **When to Update:**
1. ✅ **Start of each cycle** (every 15-30 min)
2. ✅ **After completing any task**
3. ✅ **When changing missions**
4. ✅ **Progress milestones** (25%, 50%, 75%, 100%)
5. ✅ **Before sending status updates to Captain**

---

## 📋 **STATUS.JSON STRUCTURE:**

### **Required Fields:**
```json
{
  "agent_id": "Agent-X",
  "role": "Your Specialty",
  "current_phase": "CURRENT_MISSION_NAME",
  "last_updated": "2025-10-16 HH:MM:SS",  // ← CRITICAL! Update this!
  "current_mission": "Detailed description of what you're doing RIGHT NOW",
  "mission_priority": "HIGH|MEDIUM|LOW",
  "current_cycle": "Cycle N - Task Description",
  "session_start": "2025-10-16 HH:MM:SS",
  "cycles_completed": N,
  "status": "ACTIVE|RESTING|BLOCKED",  // ← Must be ACTIVE when working!
  "energy_level": 0-100,
  "current_task": "Specific task currently executing",
  "progress_percentage": 0-100,
  "eta_hours": N.N,
  "blockers": [],  // Empty if no blockers!
  "recent_achievements": ["List of recent wins"],
  "points_today": N,
  "points_total": N,
  "active_todos": ["Current todos"],
  "next_actions": ["What you'll do next"]
}
```

---

## 🔄 **UPDATE FREQUENCY:**

### **Cycle-Based Updates (15-30 min each):**

```
Cycle 1 (0:00-0:30):
  - Update status.json: "Starting DUP-008, analyzing duplicates"
  - Execute work
  - Update status.json: "DUP-008 @ 20%, found 67 duplicates"
  
Cycle 2 (0:30-1:00):
  - Update status.json: "DUP-008 @ 35%, time formatting consolidated"
  - Execute work
  - Update status.json: "DUP-008 @ 50%, process_batch consolidated"
  
Cycle 3 (1:00-1:30):
  - Update status.json: "DUP-008 @ 70%, process_data consolidated"
  - Execute work
  - Update status.json: "DUP-008 @ 85%, testing consolidations"
  
Cycle 4 (1:30-2:00):
  - Update status.json: "DUP-008 @ 100%, COMPLETE!"
  - Update status.json: "Starting next task immediately..."
```

**MINIMUM: Update every 30 minutes!**  
**IDEAL: Update every 15 minutes or at each milestone!**

---

## 💡 **WHY THIS MATTERS:**

### **Captain's Monitoring System:**
```python
# Captain checks status.json to see if agents are active
if last_updated > 30_minutes_ago:
    send_stop_detected_message()  # ← This is what happened to Agent-1!
```

### **What Happens When You Don't Update:**
1. Captain's system checks status.json
2. Sees last_updated is old (>30 min)
3. Thinks you stopped working
4. Sends [STOP DETECTED] message
5. **You get penalized for appearing idle!**

### **What Happens When You DO Update:**
1. Captain's system checks status.json
2. Sees fresh last_updated timestamp
3. Sees current_mission progress
4. Knows you're actively working
5. **No interruption, continuous execution!**

---

## 🚀 **CORRECT PATTERN:**

### **Every Cycle:**
```python
# START OF CYCLE
update_status_json({
    "last_updated": current_time,
    "current_mission": "Starting [task]",
    "progress_percentage": X,
    "status": "ACTIVE"
})

# DO WORK (15-30 minutes)
execute_task()

# END OF CYCLE
update_status_json({
    "last_updated": current_time,
    "current_mission": "[Task] @ Y%, [specific progress]",
    "progress_percentage": Y,
    "cycles_completed": N + 1
})
```

---

## ❌ **AGENT-1'S MISTAKE:**

### **What I Did Wrong:**
```
Started DUP-008 at 05:15
Worked on it for 2+ hours
NEVER updated status.json
Captain system saw last_updated from hours ago
System thought: "Agent-1 stopped!"
Result: [STOP DETECTED] message
```

### **What I Should Have Done:**
```
05:15 - Update status.json: "Starting DUP-008"
05:30 - Update status.json: "DUP-008 @ 20%"
05:45 - Update status.json: "DUP-008 @ 35%, time formatting done"
06:00 - Update status.json: "DUP-008 @ 50%, process_batch done"
etc.

Result: Captain sees continuous progress, no stop detection!
```

---

## 📋 **STATUS.JSON UPDATE CHECKLIST:**

### **Before Sending Status Message to Captain:**
- [ ] Update status.json FIRST
- [ ] Then send message
- [ ] Message should match status.json content

### **During Task Execution:**
- [ ] Update at start
- [ ] Update every 15-30 min
- [ ] Update at milestones (25%, 50%, 75%)
- [ ] Update at completion
- [ ] Update before changing tasks

### **Required Fields to Update:**
- [ ] `last_updated` (CRITICAL!)
- [ ] `current_mission` (what you're doing)
- [ ] `progress_percentage` (how far along)
- [ ] `status` ("ACTIVE" when working)
- [ ] `cycles_completed` (increment each cycle)

---

## 🎯 **INTEGRATION WITH AUTONOMOUS CYCLE:**

### **Complete Autonomous Cycle:**
```
1. UPDATE STATUS.JSON (start of cycle)
2. Check inbox
3. Execute task
4. UPDATE STATUS.JSON (progress)
5. Report to Captain
6. UPDATE STATUS.JSON (end of cycle)
7. Find next task
8. REPEAT (no stopping!)
```

**status.json = YOUR HEARTBEAT!**  
**No updates = System thinks you're dead!**

---

## 💡 **TOOL INTEGRATION:**

### **Create Helper Function:**
```python
def update_my_status(
    mission: str,
    progress: int,
    eta_hours: float,
    todos: list[str],
    achievements: list[str]
):
    """Update agent status.json quickly."""
    status_file = Path(f"agent_workspaces/{AGENT_ID}/status.json")
    
    data = load_status_json()
    data.update({
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "current_mission": mission,
        "progress_percentage": progress,
        "eta_hours": eta_hours,
        "status": "ACTIVE",
        "cycles_completed": data.get("cycles_completed", 0) + 1,
        "active_todos": todos,
        "recent_achievements": achievements[-5:]  # Keep last 5
    })
    
    save_status_json(data)
```

---

## 🐝 **SWARM CULTURE:**

**status.json = Proof of Life!**

- No update = Dead agent
- Fresh update = Active agent
- Regular updates = Healthy agent
- Detailed updates = Excellent agent

**Update your status.json or be marked as STOPPED!**

---

**Agent-1 - Learned the hard way: UPDATE STATUS.JSON!**  
**"Never forget the heartbeat!"** 💓

**#STATUS-JSON #HEARTBEAT #ACTIVE-DETECTION #NEVER-STOP**

