# 👁️ CHAPTER 08: MONITORING TOOLS

**Read Time:** 4 minutes  
**Priority:** 🟡 HIGH

---

## 🎯 **MONITORING OVERVIEW**

Tools and techniques for tracking agent progress and swarm health.

---

## 📊 **STATUS.JSON FILES**

### **What They Are:**
Each agent has a `status.json` file tracking current state:
```json
{
  "agent_id": "Agent-X",
  "status": "working|idle|blocked|complete",
  "current_task": "task_name",
  "progress_percentage": 75,
  "last_updated": "2025-10-14T10:30:00",
  "last_message_received": "2025-10-14T09:00:00",
  "points_earned_this_cycle": 350,
  "blockers": []
}
```

### **How to Check:**

**Single agent:**
```bash
cat agent_workspaces/Agent-X/status.json
```

**All agents:**
```bash
cat agent_workspaces/Agent-*/status.json
```

**Formatted view:**
```bash
cat agent_workspaces/Agent-*/status.json | jq
```

### **What to Look For:**

✅ **Good Signs:**
- Status: "working" or "complete"
- Progress: Increasing over time
- Last updated: Recent timestamp
- Blockers: Empty array

🚨 **Warning Signs:**
- Status: "idle" (no work assigned)
- Status: "blocked" (needs intervention)
- Progress: Stuck at same percentage
- Last updated: Old timestamp (>4 hours)
- Blockers: Non-empty array

---

## 🔍 **COMPLETION TRACKING**

### **#DONE Tags:**

Agents mark completed work with tags:
```markdown
#DONE-C001
#DONE-CYCLE-XXX
#TASK-COMPLETE
```

**Find completed tasks:**
```bash
# All completions
grep -r "#DONE" agent_workspaces/

# Specific cycle
grep -r "#DONE-C001" agent_workspaces/

# Recent completions
grep -r "#DONE" agent_workspaces/ --include="*.md" | tail -20
```

### **Devlog Monitoring:**

Check recent devlogs:
```bash
# List recent devlogs
ls -lt devlogs/ | head -10

# View latest devlog
cat devlogs/$(ls -t devlogs/ | head -1)

# Search for completion markers
grep -r "COMPLETE\|FINISHED\|DELIVERED" devlogs/
```

### **Passdown Files:**

Review agent handoffs:
```bash
# Check all passdowns
cat agent_workspaces/Agent-*/passdown.json

# Single agent passdown
cat agent_workspaces/Agent-X/passdown.json | jq
```

---

## 🛠️ **CAPTAIN'S MONITORING TOOLS**

### **Find Idle Agents:**
```bash
python tools/captain_find_idle_agents.py
```

**Output:**
```
🔍 Idle Agent Scan Results:
- Agent-2: IDLE (last updated 4h ago)
- Agent-7: IDLE (no current task)

✅ Active Agents: 5/7
⚠️ Idle Agents: 2/7
```

### **Check Agent Status:**
```bash
python tools/captain_check_agent_status.py
```

**Output:**
```
📊 Agent Status Summary:
Agent-1: WORKING (75% complete)
Agent-2: IDLE
Agent-3: WORKING (50% complete)
Agent-4: WORKING (60% complete) [CAPTAIN]
Agent-5: BLOCKED (dependency issue)
Agent-6: COMPLETE
Agent-7: IDLE
Agent-8: WORKING (30% complete)
```

### **GAS Check (Fuel Status):**
```bash
python tools/captain_gas_check.py
```

**Output:**
```
⛽ GAS Status (Activation Messages):
Agent-1: ✅ Fueled (10:30 AM)
Agent-2: ❌ No fuel (last: yesterday)
Agent-3: ✅ Fueled (10:32 AM)
Agent-5: ✅ Fueled (10:35 AM)
Agent-6: ✅ Fueled (10:37 AM)
Agent-7: ❌ No fuel (last: 2 days ago)
Agent-8: ✅ Fueled (10:40 AM)

⚠️ Agents needing fuel: Agent-2, Agent-7
```

### **Message History:**
```bash
python -m src.services.messaging_cli --history
```

**Output:**
```
📜 Recent Messages:
[10:40] Captain → Agent-8: "Check INBOX! Mission assigned"
[10:37] Captain → Agent-6: "Check INBOX! Mission assigned"
[10:35] Captain → Agent-5: "Check INBOX! Mission assigned"
...
```

---

## 📈 **PROGRESS METRICS**

### **Points Tracking:**

**Cycle totals:**
```bash
# Sum points from status files
cat agent_workspaces/Agent-*/status.json | jq -r '.points_earned_this_cycle' | awk '{s+=$1} END {print s}'
```

**Agent leaderboard:**
```bash
python tools/captain_leaderboard_update.py --view
```

### **ROI Tracking:**

**Calculate achieved ROI:**
```bash
python tools/captain_roi_quick_calc.py --cycle CXXX
```

**Output:**
```
📊 ROI Results - Cycle XXX:
Total Points: 4,750
Total ROI: 158.23
Average ROI: 19.78
Top Performer: Agent-3 (ROI 33.33)
```

### **V2 Compliance:**

**Check violations:**
```bash
python tools/run_project_scan.py --violations-only
```

**Track improvement:**
```bash
# Compare to previous scan
diff <(cat previous_violations.txt) <(cat current_violations.txt)
```

---

## 🚨 **BLOCKER DETECTION**

### **Status File Blockers:**

```bash
# Find agents with blockers
cat agent_workspaces/Agent-*/status.json | jq 'select(.blockers | length > 0)'
```

### **Agent Messages:**

Search for blocker keywords:
```bash
grep -ri "BLOCKED\|BLOCKER\|STUCK\|HELP\|ERROR" agent_workspaces/*/inbox/
```

### **Log Analysis:**

Check error logs:
```bash
# Recent errors
tail -f logs/error.log

# Agent-specific errors
grep "Agent-X" logs/error.log
```

---

## 📊 **DASHBOARD VIEW**

### **Quick Status Dashboard:**

Create your own monitoring script:
```bash
#!/bin/bash
# dashboard.sh

echo "🐝 SWARM STATUS DASHBOARD"
echo "========================="
echo ""

echo "📊 AGENT STATUS:"
for agent in Agent-1 Agent-2 Agent-3 Agent-5 Agent-6 Agent-7 Agent-8; do
  status=$(cat agent_workspaces/$agent/status.json 2>/dev/null | jq -r '.status')
  task=$(cat agent_workspaces/$agent/status.json 2>/dev/null | jq -r '.current_task')
  progress=$(cat agent_workspaces/$agent/status.json 2>/dev/null | jq -r '.progress_percentage')
  echo "$agent: $status | $task ($progress%)"
done

echo ""
echo "⛽ FUEL STATUS:"
python tools/captain_gas_check.py --brief

echo ""
echo "🏆 POINTS SUMMARY:"
python tools/captain_leaderboard_update.py --summary

echo ""
echo "🚨 BLOCKERS:"
cat agent_workspaces/Agent-*/status.json | jq 'select(.blockers | length > 0) | {agent_id, blockers}'
```

**Run dashboard:**
```bash
bash dashboard.sh
```

---

## ⏰ **MONITORING SCHEDULE**

### **Continuous (Every 30 min):**
- Quick status check (all agents)
- Watch for completion tags
- Monitor logs for errors

### **Every 1-2 Hours:**
- Detailed status review
- Check for blockers
- Verify message delivery
- Track progress percentages

### **Every 4 Hours:**
- Full GAS check
- ROI calculations
- Points tracking
- Dashboard review

### **End of Cycle:**
- Final completion check
- Points totals
- ROI achieved
- Lessons learned capture

---

## 🔔 **ALERT TRIGGERS**

Set up alerts for:

**Critical:**
- Agent blocked >1 hour
- Agent idle >2 hours
- System error detected
- Zero progress >4 hours

**High:**
- Agent not fueled in 24 hours
- Blocker reported
- Dependency conflict
- File access error

**Medium:**
- Progress <25% at midpoint
- Low test coverage
- V2 violation introduced

---

## 📋 **MONITORING CHECKLIST**

**Every cycle, check:**
- [ ] All agent status.json files reviewed
- [ ] Idle agents identified and addressed
- [ ] Blockers detected and resolved
- [ ] GAS status verified (all agents fueled)
- [ ] Progress percentages tracked
- [ ] Completion tags found and logged
- [ ] Points earned calculated
- [ ] ROI achieved calculated
- [ ] Dashboard updated

---

## 🎯 **SUCCESS METRICS**

**Healthy Swarm:**
- 0 idle agents (or justified rest)
- 0 unresolved blockers
- All agents fueled in last 24h
- Progress >50% at cycle midpoint
- All completions tagged and tracked

---

**🎯 MONITOR CONTINUOUSLY. INTERVENE QUICKLY. KEEP SWARM HEALTHY!** ⚡

---

[← Previous: Quick Commands](./07_QUICK_COMMANDS.md) | [Back to Index](./00_INDEX.md) | [Next: Work Focus Areas →](./09_WORK_FOCUS_AREAS.md)

