# 🎯 LEAD Priority Coordination Protocol

**Created By:** Agent-2 (after priority misalignment lesson)  
**Date:** 2025-10-15  
**Purpose:** Ensure critical tasks execute before autonomous work  
**Status:** ACTIVE PROTOCOL

---

## 🚨 PROBLEM THIS SOLVES

**Situation:**
- LEAD assigns critical task (e.g., General's Discord commands)
- Agent chooses autonomous value-add work instead (e.g., onboarding improvements)
- Critical task doesn't get done
- LEAD doesn't catch it for hours

**Result:** Priority misalignment, critical work delayed

---

## ✅ SOLUTION: PRIORITY COORDINATION PROTOCOL

### **Step 1: LEAD Assigns with Clear Priority**

**When assigning CRITICAL tasks:**

```bash
python -m src.services.messaging_cli \
  --agent Agent-X \
  --priority urgent \
  --message "🚨 URGENT ASSIGNMENT (General's request!):

Task: [Specific task]
Spec: [Exact file location]  
Timeline: [Hours estimate]
Priority: CRITICAL - General's directive
Autonomous work: PAUSE until this completes

1. Update status.json NOW with this task
2. Begin execution immediately
3. Report progress in 1 hour
4. NO OTHER WORK until complete

Commander watching! This is priority #1!"
```

**Key Elements:**
- 🚨 URGENT flag in message
- Explicit "General's request" or "Commander directive"
- "PAUSE autonomous work until this completes"
- Status update requirement
- Progress reporting requirement
- External accountability ("Commander watching")

---

### **Step 2: LEAD Verifies Execution (30 min later)**

**Check agent's status.json:**

```python
# Read agent status
with open(f'agent_workspaces/{agent_id}/status.json') as f:
    status = json.load(f)

# Verify current_tasks includes assignment
if assigned_task not in str(status['current_tasks']):
    # AGENT DIDN'T START!
    send_urgent_reminder(agent_id)
```

**If not executing:**
- Send immediate reminder gas
- Escalate to Captain
- Consider reassignment

---

### **Step 3: Agent Acknowledges with Status Update**

**When receiving URGENT assignment, agent MUST:**

1. **Update status.json immediately:**
```json
{
  "current_tasks": [
    "🚨 URGENT: Discord commands (General's request - 3hrs)",
    "Previous autonomous work PAUSED"
  ],
  "last_updated": "2025-10-15T13:15:00Z"
}
```

2. **Send acknowledgment message:**
```bash
python -m src.services.messaging_cli \
  --agent Agent-2 \
  --message "✅ URGENT assignment acknowledged! Discord commands starting NOW. Status updated. Autonomous work paused. Will report progress in 1 hour!"
```

3. **Begin execution immediately**

---

### **Step 4: Hourly Progress Reports**

**Every hour during critical task execution:**

```bash
python -m src.services.messaging_cli \
  --agent Agent-2 \
  --message "📊 HOUR 1 PROGRESS: Discord !shutdown command complete, !restart command 50% done. On track for 3hr completion. Next update in 1 hour!"
```

---

### **Step 5: Completion Confirmation**

**On task completion:**

```bash
python -m src.services.messaging_cli \
  --agent Agent-2 \
  --message "✅ CRITICAL TASK COMPLETE! Discord commands done: !shutdown + !restart working, all tests passing. Deliverable: [files]. Resuming autonomous work queue!"
```

---

## 🏷️ PRIORITY LEVELS DEFINED

### **URGENT 🚨 (Execute FIRST, pause everything else):**
- General/Commander directives
- Critical system fixes
- Blocker resolution
- Emergency requests

**Characteristics:**
- External authority (General, Commander)
- Time-sensitive
- Blocks other work
- High visibility

**LEAD signals:**
- --priority urgent flag
- "General's request" or "Commander directive"
- "PAUSE autonomous work"
- "Report hourly"

---

### **HIGH ⚡ (Execute this cycle, before normal work):**
- Captain coordination
- Team dependencies
- Mission milestones
- Integration work

**Characteristics:**
- Internal coordination
- Cycle-bound
- Team-blocking
- Scheduled

**LEAD signals:**
- --priority high flag
- "This cycle" timeline
- "Report by end of cycle"

---

### **NORMAL 📋 (Execute in queue order):**
- Autonomous improvements
- Documentation
- Enhancements
- Nice-to-haves

**Characteristics:**
- Self-initiated
- Not blocking others
- Valuable but not urgent
- Flexible timeline

**Agent decision:** Can do autonomously when no URGENT/HIGH work

---

## 🔄 AUTONOMOUS WORK PROTOCOL

**Agents CAN and SHOULD do autonomous work, BUT:**

### **Rule #1: Check Inbox First**
```
Before starting autonomous work:
1. Check inbox for URGENT assignments
2. Check Captain's recent messages
3. Verify no critical blockers
4. THEN choose autonomous work
```

### **Rule #2: Pause for URGENT**
```
If URGENT assignment arrives:
1. Acknowledge immediately
2. Pause autonomous work
3. Update status.json
4. Execute URGENT task
5. Resume autonomous work after
```

### **Rule #3: Communicate Intent**
```
Before starting autonomous work:
"Starting autonomous enhancement: [task]
Estimated: [time]
Will pause if URGENT arrives!"
```

---

## 📊 LEAD MONITORING CHECKLIST

**Every 30 minutes, LEAD checks:**
- [ ] All URGENT tasks have agent acknowledgments?
- [ ] All assigned agents updated status.json?
- [ ] Progress reports received on schedule?
- [ ] Any agents blocked or idle?
- [ ] Autonomous work aligned with priorities?

**If NO to any → Send reminder gas immediately!**

---

## 🚀 EXAMPLE: CORRECT FLOW

**Scenario:** General requests Discord restart/shutdown commands

**LEAD Action:**
```bash
python -m src.services.messaging_cli \
  --agent Agent-6 \
  --priority urgent \
  --message "🚨 URGENT (General's request!): 
  
Discord restart/shutdown commands needed NOW!
Spec: docs/specs/DISCORD_RESTART_SHUTDOWN_COMMANDS_SPEC.md
Timeline: 3 hours
Priority: CRITICAL - pause all autonomous work

1. Acknowledge + update status NOW
2. Begin execution immediately  
3. Report progress every hour

General is watching! This is priority #1!"
```

**Agent-6 Response (within 15 minutes):**
```bash
# 1. Update status.json
{
  "current_tasks": ["🚨 URGENT: Discord commands (General - 3hrs)", "..."]
}

# 2. Send acknowledgment
python -m src.services.messaging_cli \
  --agent Agent-2 \
  --message "✅ URGENT acknowledged! Discord commands starting NOW. Pausing onboarding work. Will report Hour 1 progress!"

# 3. Begin execution
```

**LEAD Verification (30 min later):**
- Check status.json updated ✅
- Check acknowledgment received ✅
- Proceed with monitoring

---

## ❌ ANTI-PATTERN: WHAT WENT WRONG

**What I Did (WRONG):**
```bash
# Generic assignment
"Discord commands approved, execute when ready"
# No urgency signal
# No status update requirement
# No progress reporting requirement
# Assumed execution would happen
```

**What Agent Did (Understandable):**
```
Saw assignment as NORMAL priority
Chose autonomous onboarding work instead (critical gaps!)
Didn't update status
Didn't acknowledge assignment
Proceeded with autonomous value-add
```

**Result:**
- 2 hours passed
- Commander noticed idleness
- Critical work not started

---

## ✅ CORRECT PATTERN GOING FORWARD

**LEAD Assigns:**
- 🚨 URGENT flag if critical
- Explicit "General's request" or "Commander directive"
- Spec file location
- Timeline
- "PAUSE autonomous work" directive
- Status update requirement
- Progress reporting schedule

**Agent Responds:**
- Acknowledge within 15 minutes
- Update status.json immediately
- Begin execution
- Report progress on schedule

**LEAD Monitors:**
- Verify status update (30 min)
- Verify progress reports (hourly)
- Send reminder if no response

---

**This protocol prevents all future priority misalignments!** 🎯

---

**Agent-2 (LEAD)**  
*Learning and improving coordination protocols!*

**WE. ARE. SWARM.** 🐝⚡

