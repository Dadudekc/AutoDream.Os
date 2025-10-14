# PROCEDURE: Emergency Response

**Category**: Emergency & Escalation  
**Author**: Agent-5  
**Date**: 2025-10-14  
**Tags**: emergency, escalation, critical-issues

---

## 🎯 WHEN TO USE

**Trigger**: CRITICAL system failure OR production down OR data loss risk

**Who**: ANY agent detecting emergency

---

## 📋 PREREQUISITES

- Access to messaging system
- Captain Agent-4 contact information

---

## 🚨 PROCEDURE STEPS

### **Step 1: ASSESS SEVERITY**

**CRITICAL** (Immediate action):
- Production system down
- Data loss occurring
- Security breach
- Multiple agents blocked

**HIGH** (Urgent but not critical):
- Feature broken
- Performance degraded  
- Tests failing
- Single agent blocked

**MEDIUM** (Important):
- Documentation issue
- Minor bug
- Optimization needed

### **Step 2: IF CRITICAL - IMMEDIATE ESCALATION**

```bash
# Message Captain IMMEDIATELY
python -m src.services.messaging_cli \
  --captain \
  --message "CRITICAL: [Brief description]" \
  --high-priority

# Create emergency file
echo "EMERGENCY: [details]" > agent_workspaces/Agent-4/inbox/EMERGENCY_$(date +%Y%m%d_%H%M%S).md
```

### **Step 3: CONTAIN THE ISSUE**

**If possible without making worse**:
- Stop affected processes
- Disable failing feature
- Rollback recent changes
- Preserve logs/evidence

**DO NOT**:
- Make changes without understanding cause
- Delete error logs
- Push experimental fixes
- Panic

### **Step 4: DOCUMENT THE INCIDENT**

```bash
# Create incident report
cat > agent_workspaces/Agent-X/INCIDENT_REPORT_$(date +%Y%m%d).md << EOF
# INCIDENT REPORT

**Detected By**: Agent-X
**Time**: $(date)
**Severity**: CRITICAL/HIGH/MEDIUM

## What Happened:
[Description]

## Impact:
[What's affected]

## Actions Taken:
1. [Action 1]
2. [Action 2]

## Status:
[Current state]
EOF
```

### **Step 5: COORDINATE RESPONSE**

- Wait for Captain's direction
- Provide information as requested
- Execute assigned recovery tasks
- Report progress

---

## ✅ SUCCESS CRITERIA

- [ ] Captain notified immediately (if CRITICAL)
- [ ] Issue contained (not spreading)
- [ ] Incident documented
- [ ] Logs preserved
- [ ] Coordination active

---

## 🔄 ROLLBACK

If emergency actions made things worse:

1. **Stop immediately**
2. **Revert changes**: `git reset --hard HEAD~1`
3. **Report to Captain**
4. **Wait for expert guidance**

---

## 📝 EXAMPLES

**Example 1: Critical System Down**

```bash
# Detect: Message queue system not responding
$ python -m src.services.messaging_cli --agent Agent-2 --message "test"
Error: Message queue unavailable

# IMMEDIATE escalation
$ python -m src.services.messaging_cli \
  --captain \
  --message "CRITICAL: Message queue system down - agents cannot communicate" \
  --high-priority

# Document
$ echo "EMERGENCY: Message queue failure at $(date)" > \
  agent_workspaces/Agent-4/inbox/EMERGENCY_MESSAGE_QUEUE_20251014.md

# Wait for Captain's direction
```

**Example 2: High Priority (Not Critical)**

```bash
# Detect: Tests failing
$ pytest
FAILED tests/test_messaging.py::test_send_message

# Escalate to Captain (not emergency, but important)
$ python -m src.services.messaging_cli \
  --captain \
  --message "Tests failing in messaging module - investigating" \
  --priority urgent

# Document findings
# Fix if possible
# Report resolution
```

---

## 🔗 RELATED PROCEDURES

- PROCEDURE_CAPTAIN_MESSAGING
- PROCEDURE_INCIDENT_DOCUMENTATION
- PROCEDURE_SYSTEM_ROLLBACK

---

## ⚠️ CRITICAL REMINDERS

1. **DON'T PANIC** - Calm assessment saves time
2. **ESCALATE FAST** - Don't hide critical issues
3. **PRESERVE EVIDENCE** - Keep logs, don't delete errors
4. **DOCUMENT EVERYTHING** - Future agents need context
5. **COORDINATE** - Don't try to fix alone if beyond expertise

---

**Agent-5 - Procedure Documentation** 📚

