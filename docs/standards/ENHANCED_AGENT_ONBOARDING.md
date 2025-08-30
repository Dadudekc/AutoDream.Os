# 🚨 **ENHANCED AGENT ONBOARDING - EXECUTE THESE COMMANDS IMMEDIATELY** 🚨

**Document**: Enhanced Agent Onboarding  
**Date**: 2025-01-28  
**Author**: Captain Agent-4  
**Status**: ACTIVE - IMMEDIATE IMPLEMENTATION REQUIRED  

---

## 🎯 **EXECUTIVE SUMMARY**

**Agent-[X], you are [Role]. Execute these commands NOW - not later, not tomorrow, NOW.** This onboarding uses action-based language with concrete, executable commands.

---

## 🚨 **MANDATORY COMMANDS - EXECUTE IMMEDIATELY** ⚡

### **COMMAND 1: Verify Identity (Execute NOW)**
```bash
whoami && pwd && ls -la
```

### **COMMAND 2: Update Status (Execute NOW)**
```bash
echo '{"agent_id": "Agent-[X]", "role": "[Role]", "status": "Active", "last_updated": "'$(date)'", "fsm_state": "active"}' > status.json
```

### **COMMAND 3: Check Inbox (Execute NOW)**
```bash
ls -la agent_workspaces/meeting/agent_workspaces/Agent-4/inbox/
```

### **COMMAND 4: Send Ready Signal (Execute NOW)**
```bash
echo "Agent-[X]: Ready for tasks at $(date)" > agent_workspaces/meeting/agent_workspaces/Agent-4/inbox/AGENT_[X]_READY.md
```

### **COMMAND 5: Log Activity (Execute NOW)**
```bash
python scripts/devlog.py "Agent Onboarding Complete" "Agent-[X] completed onboarding and is ready for tasks."
```

### **COMMAND 6: Commit Changes (Execute NOW)**
```bash
git add . && git commit -m "Agent-[X]: Onboarding complete" && git push
```

---

## 📋 **SYSTEM INTEGRATION REQUIREMENTS**

### **1. CONTRACT CLAIM SYSTEM**
- **Use Flag**: `--get-next-task` to claim new tasks
- **Status Updates**: Log all task progress in contract system
- **Completion Reports**: Submit via contract completion workflow

### **2. FSM SYSTEM**
- **State Updates**: Update FSM state in status.json every action
- **Workflow Tracking**: Log all state changes and transitions
- **Progress Monitoring**: Use FSM states to track task completion

### **3. DEVLOG SYSTEM**
- **Activity Logging**: Log all major actions and decisions
- **Progress Updates**: Document progress via devlog entries
- **Issue Reporting**: Use devlog for blocker identification

### **4. INBOX MESSAGING**
- **Captain Communication**: Send all messages to Agent-4 inbox
- **Blocker Reports**: Report any issues preventing task completion
- **Task Ideas**: Submit new task suggestions and technical debt findings

---

## 🚫 **CODING REQUIREMENTS - DO NOT WARNINGS** ⚠️

### **V2 COMPLIANCE REQUIREMENTS:**
- **File Size Limit**: NO files over 400 lines
- **Single Responsibility**: Each file must have ONE clear purpose
- **Clean Interfaces**: Well-defined imports/exports
- **Documentation**: README.md for each new package
- **Testing**: Comprehensive test coverage for new code

### **WHAT NOT TO DO:**
- ❌ **DO NOT** create files over 400 lines
- ❌ **DO NOT** violate single responsibility principle
- ❌ **DO NOT** create circular dependencies
- ❌ **DO NOT** ignore import/export standards
- ❌ **DO NOT** skip documentation requirements
- ❌ **DO NOT** contribute to technical debt

---

## 📊 **PROGRESS TRACKING REQUIREMENTS**

### **Immediate Updates (Required):**
- **Status.json Update**: Every 7 minutes maximum
- **Devlog Entry**: At least one entry per day
- **Inbox Report**: Progress update to Captain
- **Contract Update**: Task completion status

### **Daily Requirements:**
- **Status Updates**: Every 7 minutes maximum
- **Progress Logging**: Via devlog system
- **Blocker Reporting**: Immediately when issues arise
- **New Idea Submission**: Promptly when ideas occur

---

## 🎯 **SUCCESS CRITERIA**

### **Onboarding Success (5 minutes):**
- [ ] All 6 mandatory commands executed
- [ ] Identity verified and status updated
- [ ] Inbox checked and ready signal sent
- [ ] Activity logged in devlog
- [ ] Changes committed and pushed

### **Daily Success:**
- [ ] Status updated every 7 minutes
- [ ] Progress logged in devlog
- [ ] Blockers reported immediately
- [ ] New ideas submitted promptly
- [ ] V2 compliance maintained

---

## 🚨 **FINAL WARNING**

**THESE COMMANDS ARE MANDATORY - EXECUTE THEM NOW - NOT LATER, NOT TOMORROW, NOW.**

**Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager**
