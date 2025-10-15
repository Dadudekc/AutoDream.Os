# 🔄 AGENT LIFECYCLE & FSM - COMPLETE GUIDE

**Last Updated:** 2025-10-15  
**Purpose:** Understanding agent lifecycle states and FSM integration

---

## 🎯 WHAT IS FSM?

**FSM = Finite State Machine** - Tracks agent's current state in their lifecycle

**Integration:** FSM states sync with status.json's `fsm_state` field

---

## 📊 FSM STATES (6 Total)

### **1. START** 
**When:** Agent first onboarded or beginning new mission  
**status.json:** `{"fsm_state": "start", "status": "IDLE"}`  
**Actions:** Check inbox, review mission, initialize

### **2. ACTIVE**
**When:** Agent actively working on tasks  
**status.json:** `{"fsm_state": "active", "status": "ACTIVE"}`  
**Actions:** Execute tasks, update progress, communicate

### **3. PROCESS**
**When:** Agent deep in execution (task processing)  
**status.json:** `{"fsm_state": "process", "status": "ACTIVE"}`  
**Actions:** Heavy processing, minimal interruption

### **4. BLOCKED**
**When:** Agent waiting for external input  
**status.json:** `{"fsm_state": "blocked", "status": "BLOCKED"}`  
**Actions:** Document blocker, notify Captain, wait

### **5. COMPLETE**
**When:** Mission/task completed successfully  
**status.json:** `{"fsm_state": "complete", "status": "COMPLETE"}`  
**Actions:** Finalize deliverables, report results

### **6. END**
**When:** Agent wrapping up, awaiting next assignment  
**status.json:** `{"fsm_state": "end", "status": "IDLE"}`  
**Actions:** Clean up, update status, wait for new mission

---

## 🔄 STATE TRANSITIONS

### **Valid Transitions:**
```
START → ACTIVE     (Begin work)
ACTIVE → PROCESS   (Deep work)
PROCESS → ACTIVE   (Return to normal)
ACTIVE → BLOCKED   (Hit blocker)
BLOCKED → ACTIVE   (Blocker resolved)
ACTIVE → COMPLETE  (Task done)
COMPLETE → END     (Wrap up)
END → START        (New mission)
```

### **Invalid Transitions:**
- ❌ START → COMPLETE (can't complete before starting!)
- ❌ BLOCKED → END (must resolve blocker first)
- ❌ PROCESS → BLOCKED (return to ACTIVE first)

---

## 💻 INTEGRATION WITH AgentLifecycle

**Automatic FSM management:**

```python
from src.core.agent_lifecycle import AgentLifecycle

lifecycle = AgentLifecycle('Agent-7')

# START → ACTIVE
lifecycle.start_cycle()  # Sets fsm_state="active"

# ACTIVE → PROCESS (manual if needed)
lifecycle.status['fsm_state'] = 'process'
lifecycle._save_status()

# ACTIVE → BLOCKED
lifecycle.add_blocker("Waiting for approval")  # Sets fsm_state="blocked"

# BLOCKED → ACTIVE
lifecycle.clear_blockers()  # Sets fsm_state="active"

# ACTIVE → COMPLETE
lifecycle.complete_mission()  # Sets fsm_state="complete"

# COMPLETE → END (manual)
lifecycle.status['fsm_state'] = 'end'
lifecycle._save_status()
```

---

## 📋 FSM BEST PRACTICES

### ✅ DO:
- Update fsm_state when transitioning
- Use AgentLifecycle for automatic updates
- Document state changes in status.json
- Sync to database after state changes

### ❌ DON'T:
- Skip intermediate states
- Leave fsm_state stale
- Use invalid transitions
- Forget to sync to database

---

## 🔍 TROUBLESHOOTING

**Issue:** fsm_state stuck on "blocked"  
**Solution:** Use `lifecycle.clear_blockers()`

**Issue:** fsm_state doesn't match status  
**Solution:** Manually align and save

**Issue:** Invalid state transition  
**Solution:** Go through valid intermediate states

---

## 🔗 RELATED GUIDES

- **STATUS_JSON_GUIDE.md** - status.json fields
- **CYCLE_PROTOCOLS.md** - When to update
- **AgentLifecycle class** - Automation (src/core/agent_lifecycle.py)

---

**🐝 FSM TRACKS YOUR LIFECYCLE - KEEP IT CURRENT!** 🔄

