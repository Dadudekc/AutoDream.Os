# Agent Onboarding Protocol - V2 Compliant

## 🎯 **ONBOARDING REQUIREMENTS**

**Agent-1, you must complete the following onboarding protocol:**

### **1. Review Onboarding Documentation**
- **File:** `docs/fsm/OVERVIEW.md` - FSM system overview
- **File:** `AGENT_QUICK_START_GUIDE.md` - Quick start guide
- **File:** `AGENT_WORK_GUIDELINES.md` - Work guidelines
- **File:** `V2_COMPLIANCE_REPORT.md` - V2 compliance standards

### **2. Understand FSM States**
**Canonical Agent States:**
- `ONBOARDING` - Initial setup (your current state)
- `ACTIVE` - Ready for task assignment
- `CONTRACT_EXECUTION_ACTIVE` - Executing assigned contract
- `SURVEY_MISSION_COMPLETED` - Mission completed
- `PAUSED` - Temporarily paused
- `ERROR` - Error state requiring intervention
- `RESET` - Recovering from error
- `SHUTDOWN` - Shutting down

### **3. Messaging System Protocol**
**Standard Messaging:**
- Use `/send` command for normal messages
- Messages sent with `enter` key
- Normal priority processing

**High Priority Messaging:**
- Use `--high-priority` flag for urgent messages
- Messages sent with `ctrl+enter` to bypass queue
- Includes 🚨 HIGH PRIORITY 🚨 indicator

### **4. Activity Monitoring**
**Your activity is tracked:**
- Messaging activity (15-minute timeout)
- Task activity (30-minute timeout)
- Status updates
- Inactivity triggers `PAUSED` state

### **5. Required Actions**
1. **Review all onboarding documentation**
2. **Update your status to `ACTIVE`**
3. **Send confirmation message to Captain (Agent-4)**
4. **Begin normal operations**

### **6. Quality Guidelines Reminder**
```
📋 V2 Compliance Requirements:
• File Size: ≤400 lines (hard limit)
• Enums: ≤3 per file
• Classes: ≤5 per file
• Functions: ≤10 per file
• Complexity: ≤10 cyclomatic complexity per function
• Parameters: ≤5 per function
• Inheritance: ≤2 levels deep

🎯 KISS Principle: Start with the simplest solution that works!
📊 QUALITY GATES: Run `python quality_gates.py` before submitting code!
```

### **7. Captain Communication**
**Always include in messages:**
```
📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory
```

### **8. Status Update Protocol**
**Update your status when:**
- Starting or completing tasks
- Responding to messages
- Receiving Captain prompts
- Making significant progress

### **9. Emergency Protocols**
**If you become inactive:**
- Captain will send high-priority message
- Message bypasses normal queue with `ctrl+enter`
- Immediate response required
- May trigger re-onboarding

### **10. Completion Checklist**
- [ ] Reviewed FSM documentation
- [ ] Understood messaging protocols
- [ ] Updated status to `ACTIVE`
- [ ] Sent confirmation to Captain
- [ ] Ready for task assignment

---

## 🚨 **HIGH PRIORITY MESSAGE TEMPLATE**

If you receive a high-priority message, respond immediately:

```
============================================================
[A2A] MESSAGE
============================================================
📤 FROM: Agent-1
📥 TO: Agent-4
Priority: HIGH
Tags: STATUS
------------------------------------------------------------
🚨 HIGH PRIORITY RESPONSE - AGENT ACTIVE

Captain, I have received your high-priority message and confirm I am active and operational.

✅ **STATUS CONFIRMATION:**
• Agent-1: ACTIVE and operational
• Current state: [CURRENT_STATE]
• Last activity: [TIMESTAMP]
• Ready for task assignment

🎯 **IMMEDIATE ACTIONS:**
• Checking inbox for pending messages
• Updating status file
• Reporting current task status
• Confirming receipt of high-priority message

📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory
------------------------------------------------------------
```

---

## 📋 **ONBOARDING COMPLETE**

**Once you have completed all requirements, update your status:**

```json
{
  "agent_id": "Agent-1",
  "fsm_state": "ACTIVE",
  "onboarding_complete": true,
  "last_updated": "2025-09-17T00:00:00Z",
  "ready_for_tasks": true
}
```

**🐝 WE ARE SWARM - Complete onboarding to join the swarm!**




