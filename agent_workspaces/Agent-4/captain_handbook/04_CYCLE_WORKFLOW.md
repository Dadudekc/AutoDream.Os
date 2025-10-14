# 🔄 CHAPTER 04: CYCLE WORKFLOW

**Read Time:** 7 minutes  
**Priority:** 🟡 HIGH

---

## 🎯 **THE COMPLETE CYCLE WORKFLOW**

Step-by-step process for executing a full Captain cycle.

---

## 📊 **PHASE 1: PLANNING** (15-30 minutes)

### **Step 1: Scan Project**
```bash
python tools/run_project_scan.py
```

**What it does:**
- Analyzes entire codebase
- Identifies V2 violations
- Generates project_analysis.json
- Generates test_analysis.json

### **Step 2: Analyze Data**

Review outputs:
```bash
# Project analysis
cat project_analysis.json

# Test analysis  
cat test_analysis.json

# Look for chatgpt context
cat chatgpt_project_context.json
```

**Identify:**
- V2 violations (files >400 lines)
- Missing tests
- Technical debt
- Opportunities for improvement

### **Step 3: Optimize Assignments**
```bash
python tools/markov_8agent_roi_optimizer.py
```

**What it does:**
- Calculates ROI for all tasks
- Matches tasks to agent specializations
- Prioritizes autonomy-advancing tasks
- Outputs optimal assignment plan

### **Step 4: Review Results**

Check ROI scores:
- High ROI (>25): Top priority
- Medium ROI (15-25): Standard priority
- Low ROI (<15): Consider delegating or deferring

Verify agent matches align with specializations.

---

## 📝 **PHASE 2: ASSIGNMENT** (15-30 minutes)

### **Step 1: Create Orders**

For each agent, create:
```markdown
# EXECUTION ORDER - Cycle XXX

**Agent:** Agent-X  
**Task:** [task_name]  
**Points:** XXX  
**ROI:** XX.XX  
**Complexity:** XX  
**Autonomy:** X/3

## Objective:
[Clear description of what needs to be done]

## Instructions:
1. [Step-by-step guidance]
2. [...]
3. [...]

## Deliverables:
- [ ] [Specific deliverable 1]
- [ ] [Specific deliverable 2]
- [ ] Tests passing (100% coverage)
- [ ] V2 compliance verified

## V2 Requirements:
- ≤400 lines per file
- 100% type hints
- Comprehensive docstrings
- No circular imports

## Coordination:
[If paired with another agent, specify here]

## Resources:
- [Relevant docs/files]
- [Tools to use]

## Success Criteria:
[How to know when complete]

#CYCLE-XXX #AGENT-X
```

Save to: `agent_workspaces/Agent-X/inbox/EXECUTION_ORDER_CXXX.md`

### **Step 2: Self-Assign**

Captain chooses own task:
- High autonomy impact (error handling, self-healing, optimization)
- Strategic systems (ROI calculators, monitoring tools)
- Infrastructure improvements
- Leadership tools

Create own execution plan.

---

## 🚀 **PHASE 3: ACTIVATION** (10-15 minutes) **CRITICAL!**

### **Step 1: Fix Messaging (if needed)**

Test messaging system:
```bash
python -m src.services.messaging_cli --list-agents
```

If errors, fix imports (see Chapter 06).

### **Step 2: Send Messages to ALL Agents**

```bash
# Agent-1
python -m src.services.messaging_cli \
  --agent Agent-1 \
  --message "🎯 URGENT: Check INBOX! Mission CXXX assigned: [task]. BEGIN NOW!" \
  --sender "Captain Agent-4" \
  --priority urgent

# Agent-2
python -m src.services.messaging_cli \
  --agent Agent-2 \
  --message "🎯 URGENT: Check INBOX! Mission CXXX assigned: [task]. BEGIN NOW!" \
  --sender "Captain Agent-4" \
  --priority urgent

# ... (repeat for all 7 agents)
```

**Or use bulk messaging:**
```bash
python -m src.services.messaging_cli \
  --bulk \
  --message "🚀 NEW CYCLE CXXX: Check INBOX for assignments! BEGIN NOW!" \
  --sender "Captain Agent-4" \
  --priority urgent
```

### **Step 3: Verify Delivery**

Check logs for:
- ✅ "Coordinates validated for Agent-X"
- ✅ "Message sent to Agent-X at (x, y)"
- ✅ "WE. ARE. SWARM." confirmation

Review:
```bash
tail -f logs/messaging.log
```

---

## 💪 **PHASE 4: EXECUTION** (Rest of Cycle)

### **Captain's Work:**

1. **Start assigned task**
   - Open relevant files
   - Review requirements
   - Begin implementation

2. **Make progress**
   - Target: 50%+ completion per cycle
   - Follow same V2 standards as agents
   - Write tests as you go

3. **Document work**
   - Update progress in task tracker
   - Note insights/lessons
   - Record blockers

### **Monitor Agents:**

Periodically check:
```bash
# Check all agent statuses
cat agent_workspaces/Agent-*/status.json

# Look for completion
grep -r "#DONE-CXXX" agent_workspaces/
```

### **Coordinate:**

- Respond to agent questions
- Facilitate pair programming
- Resolve file conflicts
- Unblock agents immediately

---

## 👁️ **PHASE 5: MONITORING** (Continuous)

### **Status Checks:**

Every 1-2 hours:
```bash
# Quick status check
python tools/captain_check_agent_status.py

# Detailed review
cat agent_workspaces/Agent-1/status.json
cat agent_workspaces/Agent-2/status.json
# ... (all agents)
```

### **Track Completion:**

Look for:
- #DONE-CXXX tags in files
- Updated status.json files
- Completion messages
- Pull requests/commits

### **Resolve Blockers:**

If agent reports blocker:
1. Assess severity (critical/high/medium/low)
2. Provide guidance or resources
3. Reassign task if needed
4. Update Captain's log

### **Coordinate Pairs:**

If agents working together:
- Check sync status
- Resolve conflicts
- Facilitate communication

---

## 📝 **PHASE 6: DOCUMENTATION** (15-20 minutes)

### **Update Captain's Log:**

```markdown
## Cycle XXX - [Date]

### Planning:
- Project scan results: [summary]
- ROI optimization: [top tasks]
- Assignments: [brief overview]

### Decisions Made:
- Assigned X tasks based on ROI analysis
- Self-assigned: [Captain's task]
- Messages sent: [delivery status]
- Prioritized autonomy: [which tasks]

### Tasks Assigned:
- Agent-1: [task] (ROI XX, XXpts, Complexity XX)
- Agent-2: [task] (ROI XX, XXpts, Complexity XX)
- Agent-3: [task] (ROI XX, XXpts, Complexity XX)
- Agent-5: [task] (ROI XX, XXpts, Complexity XX)
- Agent-6: [task] (ROI XX, XXpts, Complexity XX)
- Agent-7: [task] (ROI XX, XXpts, Complexity XX)
- Agent-8: [task] (ROI XX, XXpts, Complexity XX)

### Execution:
- Captain's progress: [percentage]
- Agent completions: [list]
- Blockers resolved: [count]

### Results:
- Points earned: X
- Total ROI achieved: X
- Average ROI: X
- V2 compliance: [percentage]
- Autonomy advancement: [tasks completed]

### Lessons Learned:
- [Insight 1]
- [Insight 2]
- [Insight 3]

### Next Cycle:
- [Planned focus]
- [Dependencies unlocking]
- [New opportunities]

#CYCLE-XXX #CAPTAIN-LOG
```

### **Update Leaderboard:**
```bash
python tools/captain_leaderboard_update.py
```

### **Track Metrics:**
- V2 compliance progress (violations reduced)
- Autonomy advancement (autonomous systems built)
- Efficiency gains (ROI improvements)
- Agent performance (points earned)

---

## 🔍 **PHASE 7: DISCOVERY** (Ongoing)

### **Scan for Opportunities:**

Periodically:
```bash
# Re-scan if major changes
python tools/run_project_scan.py

# Check for new violations
python tools/scan_technical_debt.py

# Look for emerging issues
grep -r "TODO\|FIXME\|XXX" src/
```

### **Optimize Workflow:**

Review and improve:
- Markov weights (if assignments off)
- ROI calculations (if not accurate)
- Messaging templates (if clarity issues)
- Coordination protocols (if conflicts)

### **Plan Next Cycle:**

Questions to answer:
- What tasks are completing?
- What dependencies will unlock?
- What should we tackle next?
- Any agent specialization shifts needed?

Create draft assignments for next cycle.

---

## ⏱️ **TIMELINE EXAMPLE**

**8:00 AM - Planning**
- Run project scanner
- Analyze results
- Run ROI optimizer
- Create assignment plan

**8:30 AM - Assignment**
- Write 7 execution orders
- Self-assign Captain task
- Review orders for clarity

**9:00 AM - Activation**
- Test messaging system
- Send all activation messages
- Verify delivery

**9:15 AM - Execution Begins**
- Start Captain's task
- Monitor agent activations
- Respond to questions

**12:00 PM - Midday Check**
- Review all agent statuses
- Check completion progress
- Resolve any blockers

**3:00 PM - Afternoon Check**
- Review progress again
- Coordinate pair work
- Track completions

**5:00 PM - Documentation**
- Update Captain's log
- Update leaderboard
- Track metrics
- Plan next cycle

**6:00 PM - Cycle Complete**

---

## ✅ **SUCCESS INDICATORS**

Cycle succeeded if:
- ✅ All 7 agents activated
- ✅ Captain completed own task
- ✅ Captain's log updated
- ✅ Points earned tracked
- ✅ ROI achieved calculated
- ✅ Next cycle planned
- ✅ No unresolved critical blockers

---

**🎯 FOLLOW THIS WORKFLOW EVERY CYCLE FOR CONSISTENT SUCCESS!** ⚡

---

[← Previous: Cycle Duties](./03_CYCLE_DUTIES.md) | [Back to Index](./00_INDEX.md) | [Next: Daily Checklist →](./05_DAILY_CHECKLIST.md)

