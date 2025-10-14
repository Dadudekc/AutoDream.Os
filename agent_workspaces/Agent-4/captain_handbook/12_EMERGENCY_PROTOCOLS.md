# 🚨 CHAPTER 12: EMERGENCY PROTOCOLS

**Read Time:** 4 minutes  
**Priority:** 🟡 HIGH

---

## ⚠️ **EMERGENCY RESPONSE GUIDE**

What to do when things go wrong.

---

## 🔴 **CODE RED: SYSTEM FAILURE**

### **When to Declare:**
- Critical system component down
- Multiple agents unable to work
- Data corruption detected
- Security breach suspected

### **Immediate Actions:**

```bash
# 1. Alert all agents
python -m src.services.messaging_cli --bulk \
  --message "🚨 CODE RED: System failure detected. Check inbox for emergency protocol. IMMEDIATE ACTION REQUIRED!" \
  --sender "Captain Agent-4" \
  --priority urgent

# 2. Create emergency protocol document
cat > emergency_protocol.md << 'EOF'
# CODE RED - EMERGENCY PROTOCOL

## Situation: [Brief description]

## All Agents:
1. STOP current work immediately
2. Save all progress to safe location
3. Do NOT commit any changes
4. Stand by for further instructions

## Captain Actions:
- Assess damage
- Identify root cause
- Coordinate recovery
- Update within 30 minutes

STATUS: INVESTIGATING
EOF

# 3. Investigate root cause
tail -f logs/error.log
python tools/system_diagnostic.py

# 4. Coordinate recovery
# [Follow specific recovery procedure based on issue]

# 5. Update agents when resolved
python -m src.services.messaging_cli --bulk \
  --message "✅ CODE RED RESOLVED: System restored. Resume normal operations." \
  --sender "Captain Agent-4"
```

---

## ⚫ **CODE BLACK: COORDINATE FAILURE**

### **When to Declare:**
- PyAutoGUI messaging system down
- Coordinate validation failing
- Cursor IDE position changed
- Screen resolution changed

### **Immediate Actions:**

```bash
# 1. Alert via any working channel
python -m src.services.messaging_cli --bulk \
  --message "🚨 CODE BLACK: Coordinate system down. Switch to INBOX-ONLY mode. Check inbox regularly for updates." \
  --sender "Captain Agent-4" \
  --priority urgent

# 2. Create inbox notices for all agents
for agent in Agent-1 Agent-2 Agent-3 Agent-5 Agent-6 Agent-7 Agent-8; do
  cat > agent_workspaces/$agent/inbox/CODE_BLACK_NOTICE.md << 'EOF'
# 🚨 CODE BLACK - COORDINATE SYSTEM DOWN

## SITUATION:
PyAutoGUI messaging unavailable. 

## YOUR ACTIONS:
1. Check inbox every 30 minutes manually
2. Continue current task if safe
3. Document all progress in status.json
4. Do NOT wait for activation messages

## COMMUNICATION:
- Use inbox files for all communication
- Captain will update via inbox
- Check for RESOLUTION_NOTICE.md

## DURATION:
Unknown - Captain working on fix
EOF
done

# 3. Fix coordinate system
python scripts/capture_coordinates.py
# Re-capture all agent coordinates

# 4. Validate coordinates
python scripts/validate_workspace_coords.py

# 5. Test messaging
python -m src.services.messaging_cli --agent Agent-1 --message "Test message" --sender "Captain Agent-4"

# 6. Announce resolution
python -m src.services.messaging_cli --bulk \
  --message "✅ CODE BLACK RESOLVED: Coordinates restored. PyAutoGUI messaging operational." \
  --sender "Captain Agent-4"
```

---

## 🟡 **CODE YELLOW: PARTIAL FAILURE**

### **When to Declare:**
- Single agent blocked
- Non-critical system degraded
- Performance issues
- Partial service outage

### **Immediate Actions:**

```bash
# 1. Assess impact
python tools/captain_check_agent_status.py

# 2. Notify affected agents
python -m src.services.messaging_cli \
  --agent Agent-X \
  --message "⚠️ CODE YELLOW: [Issue description]. Attempting workaround. Stand by." \
  --sender "Captain Agent-4" \
  --priority high

# 3. Attempt workaround or fix
# [Specific to the issue]

# 4. Update when resolved
python -m src.services.messaging_cli \
  --agent Agent-X \
  --message "✅ CODE YELLOW RESOLVED: [Resolution]. Resume normal operations." \
  --sender "Captain Agent-4"
```

---

## 🟢 **CODE GREEN: ALL CLEAR**

### **When to Declare:**
- Emergency resolved
- Systems restored
- Normal operations resumed

### **Actions:**

```bash
# 1. Verify all systems operational
python tools/system_health_check.py

# 2. Announce all clear
python -m src.services.messaging_cli --bulk \
  --message "✅ CODE GREEN: All systems operational. Emergency concluded. Resume normal operations. Full debrief in next cycle." \
  --sender "Captain Agent-4"

# 3. Document incident
cat > incident_report_$(date +%Y%m%d).md << 'EOF'
# INCIDENT REPORT - [Date]

## Emergency Code: [RED/BLACK/YELLOW]
## Duration: [Start time - End time]

## Issue:
[Description of what went wrong]

## Impact:
- Agents affected: [list]
- Work lost: [description]
- Downtime: [duration]

## Root Cause:
[What caused the issue]

## Resolution:
[How it was fixed]

## Prevention:
[How to prevent in future]

## Lessons Learned:
1. [Lesson 1]
2. [Lesson 2]

#INCIDENT #POST-MORTEM
EOF

# 4. Update Captain's log
```

---

## 🛠️ **COMMON EMERGENCIES**

### **1. Import System Failure**

**Symptoms:**
- ModuleNotFoundError
- Circular import errors
- Import system broken

**Fix:**
```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Fix sys.path in affected files
# Add at top of file BEFORE imports:
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Verify fix
python -m src.services.messaging_cli --list-agents
```

---

### **2. Database Corruption**

**Symptoms:**
- Database errors
- Data inconsistency
- Query failures

**Fix:**
```bash
# Backup current DB
cp unified.db unified.db.backup.$(date +%Y%m%d_%H%M%S)

# Run integrity check
sqlite3 unified.db "PRAGMA integrity_check;"

# If corrupted, restore from backup
cp backups/unified.db.backup.[latest] unified.db

# Re-run migrations if needed
python -m alembic upgrade head
```

---

### **3. Agent Unresponsive**

**Symptoms:**
- Agent not responding to messages
- No status updates
- Appears frozen

**Fix:**
```bash
# Check agent status
cat agent_workspaces/Agent-X/status.json

# Check for blockers
cat agent_workspaces/Agent-X/status.json | jq '.blockers'

# Send high-priority message
python -m src.services.messaging_cli \
  --agent Agent-X \
  --message "🚨 URGENT: Provide status update immediately. Captain needs confirmation of operational status." \
  --sender "Captain Agent-4" \
  --priority urgent

# If still no response after 1hr, reassign work
python tools/captain_reassign_task.py --from Agent-X --to Agent-Y
```

---

### **4. V2 Compliance Breach**

**Symptoms:**
- File >400 lines created
- Circular imports introduced
- Type hints missing
- Tests failing

**Fix:**
```bash
# Identify violations
python tools/run_project_scan.py --violations-only

# Create emergency refactor task
python -m src.services.messaging_cli \
  --agent [appropriate-specialist] \
  --message "🚨 URGENT: V2 violation detected in [file]. Immediate refactor required. Target: ≤400 lines, 100% type hints." \
  --sender "Captain Agent-4" \
  --priority urgent

# Monitor progress
# Verify compliance before proceeding
```

---

### **5. Merge Conflict Crisis**

**Symptoms:**
- Multiple agents editing same file
- Git conflicts blocking progress
- Work loss risk

**Fix:**
```bash
# Halt all work on affected file
python -m src.services.messaging_cli --bulk \
  --message "⚠️ STOP: Merge conflict on [file]. All agents STOP editing this file immediately!" \
  --sender "Captain Agent-4" \
  --priority urgent

# Coordinate resolution
# 1. Identify all agents with changes
# 2. Have each create patch file
# 3. Captain manually merges
# 4. Verify no work lost
# 5. Resume operations

# Announce resolution
python -m src.services.messaging_cli --bulk \
  --message "✅ Conflict resolved. [Agent-X] has latest version. Other agents pull latest before resuming." \
  --sender "Captain Agent-4"
```

---

## 📋 **EMERGENCY CONTACTS**

### **Escalation Path:**

**Level 1: Captain (Agent-4)**
- All operational issues
- Agent blockers
- System degradation

**Level 2: Human Commander**
- Code RED situations
- Data loss risk
- Security breaches
- Architecture decisions beyond Captain authority

**Level 3: System Administrator**
- Infrastructure failures
- Database corruption
- Deployment issues

---

## 🎯 **EMERGENCY RESPONSE CHECKLIST**

**When emergency occurs:**

- [ ] Classify severity (RED/BLACK/YELLOW)
- [ ] Alert all affected agents immediately
- [ ] Create emergency protocol document
- [ ] Assess root cause
- [ ] Implement fix or workaround
- [ ] Verify resolution
- [ ] Announce all clear (CODE GREEN)
- [ ] Document incident (post-mortem)
- [ ] Update prevention measures
- [ ] Review lessons learned with swarm

---

## 💡 **PREVENTION BEST PRACTICES**

**Avoid emergencies:**

1. **Regular Testing:** Test messaging system before bulk operations
2. **Frequent Backups:** Backup DB and critical files regularly
3. **Monitoring:** Watch for warning signs (errors, degradation)
4. **Coordination:** Clear agent assignments prevent conflicts
5. **Documentation:** Keep runbooks updated
6. **Redundancy:** Have fallback communication channels

---

## 🚨 **REMEMBER**

> **Stay calm. Assess quickly. Act decisively. Communicate clearly.**

**Emergencies are rare, but preparedness is essential!** ⚡

---

[← Previous: Captain's Mantras](./11_CAPTAINS_MANTRAS.md) | [Back to Index](./00_INDEX.md)

