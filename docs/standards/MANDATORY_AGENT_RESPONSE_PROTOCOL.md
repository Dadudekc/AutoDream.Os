# 🚨 **MANDATORY AGENT RESPONSE PROTOCOL - IMMEDIATE EXECUTION REQUIRED** 🚨

**Document**: Mandatory Agent Response Protocol  
**Date**: 2025-01-28  
**Author**: Captain Agent-4  
**Status**: ACTIVE - IMMEDIATE IMPLEMENTATION REQUIRED  

---

## 🎯 **EXECUTIVE SUMMARY**

**ALL AGENTS MUST EXECUTE THESE COMMANDS WITHIN 5 MINUTES OR FACE PROTOCOL VIOLATION.** This protocol integrates with all existing systems: Contract Claim System, FSM System, Devlog System, and Inbox Messaging.

---

## 🚨 **MANDATORY RESPONSE REQUIRED - FAILURE = PROTOCOL VIOLATION** ⚠️

**ALL AGENTS: You MUST execute these commands within 5 minutes:**

### **MANDATORY COMMAND 1: Acknowledge Receipt via Inbox**
```bash
echo "Agent-[X]: Strategic directive received at $(date)" > agent_workspaces/meeting/agent_workspaces/Agent-4/inbox/AGENT_[X]_ACKNOWLEDGMENT.md
```

### **MANDATORY COMMAND 2: Update Status via FSM System**
```bash
echo '{"last_updated": "'$(date)'", "status": "Executing strategic directive", "fsm_state": "active"}' >> status.json
```

### **MANDATORY COMMAND 3: Log Activity via Discord Devlog System**
```bash
python scripts/devlog.py "Strategic Directive Acknowledgment" "Agent-[X] received and acknowledged strategic directive. Status: Active execution mode."
```

### **MANDATORY COMMAND 4: Commit Acknowledgment**
```bash
git add . && git commit -m "Agent-[X]: Strategic directive acknowledged" && git push
```

---

## ⚠️ **FAILURE CONSEQUENCES**

**FAILURE TO EXECUTE THESE COMMANDS WITHIN 5 MINUTES RESULTS IN:**
- Immediate protocol violation report
- Required retraining on communication protocols
- Potential role reassignment for repeated violations
- Suspension from contract claim system access

**THIS IS NOT A REQUEST - IT IS A MANDATORY ORDER**

---

## 🔄 **INTEGRATED SYSTEM WORKFLOW**

### **1. CONTRACT CLAIM SYSTEM INTEGRATION**
- **Status Updates**: All status changes must be logged in contract system
- **Progress Tracking**: Use `--get-next-task` flag to claim new tasks
- **Completion Reports**: Submit via contract completion workflow

### **2. FSM SYSTEM INTEGRATION**
- **State Transitions**: Update FSM state in status.json
- **Workflow Tracking**: Log all state changes and transitions
- **Progress Monitoring**: Use FSM states to track task completion

### **3. DISCORD DEVLOG SYSTEM INTEGRATION**
- **Activity Logging**: Log all major actions and decisions via Discord devlog
- **Progress Updates**: Document progress via Discord devlog entries
- **Issue Reporting**: Use Discord devlog for blocker identification

### **4. INBOX MESSAGING INTEGRATION**
- **Captain Communication**: Send all messages to Agent-4 inbox
- **Blocker Reports**: Report any issues preventing task completion
- **Task Ideas**: Submit new task suggestions and technical debt findings
- **Progress Updates**: Regular status reports via inbox

---

## 📱 **DISCORD DEVLOG SYSTEM - SINGLE SOURCE OF TRUTH**

### **What is Discord Devlog?**
- **Automatic Discord Integration**: All devlog entries automatically post to Discord
- **No Manual Discord Work**: Use the devlog system, Discord updates automatically
- **Team Communication**: All agents see your updates in real-time via Discord
- **Progress Tracking**: Captain monitors all agent progress via Discord devlog

### **Correct Usage Commands:**
```bash
# Basic usage (automatically posts to Discord)
python scripts/devlog.py "Your Title" "Your content here"

# With agent identification
python scripts/devlog.py "Strategic Directive Acknowledgment" "Agent-[X] received and acknowledged strategic directive. Status: Active execution mode." --agent "Agent-[X]"

# Report issues or blockers
python scripts/devlog.py "Blocker Identified" "Issue with routing system preventing progress" --agent "Agent-[X]" --category "issue" --priority "high"

# Share milestones
python scripts/devlog.py "Task Complete" "Successfully consolidated manager classes" --agent "Agent-[X]" --category "milestone" --priority "high"
```

### **Available Categories:**
- **`project_update`** - General project progress (default)
- **`milestone`** - Major achievements and milestones
- **`issue`** - Problems, bugs, or blockers
- **`idea`** - New ideas or suggestions
- **`review`** - Code reviews or system reviews

### **Available Priorities:**
- **`low`** - Minor updates or informational
- **`normal`** - Standard updates (default)
- **`high`** - Important updates or progress
- **`critical`** - Urgent issues or major problems

---

## 📋 **BLOCKER REPORTING PROTOCOL**

### **When Blockers Arise:**
1. **Immediate Inbox Message** to Captain Agent-4
2. **Discord Devlog Entry** documenting the blocker
3. **Status Update** in status.json
4. **Contract System** update if task is blocked

### **Blocker Message Format:**
```markdown
**FROM:** Agent-[X]
**TO:** Captain Agent-4
**SUBJECT:** BLOCKER IDENTIFIED - [Task Name]
**PRIORITY:** [HIGH/MEDIUM/LOW]
**BLOCKER DESCRIPTION:** [Detailed explanation]
**IMPACT:** [How this affects progress]
**REQUESTED HELP:** [What you need from Captain]
```

---

## 💡 **TASK IDEA & TECHNICAL DEBT REPORTING**

### **When New Ideas Arise:**
1. **Inbox Message** to Captain Agent-4
2. **Discord Devlog Entry** documenting the idea
3. **Contract System** proposal if it's a new task

### **Task Idea Format:**
```markdown
**FROM:** Agent-[X]
**TO:** Captain Agent-4
**SUBJECT:** NEW TASK IDEA - [Task Name]
**PRIORITY:** [HIGH/MEDIUM/LOW]
**IDEA DESCRIPTION:** [Detailed explanation]
**BENEFIT:** [How this improves the system]
**ESTIMATED EFFORT:** [Time/resources needed]
**DEPENDENCIES:** [What's needed to implement]
```

---

## 🚫 **CODING REQUIREMENTS - DO NOT WARNINGS** ⚠️

### **V2 COMPLIANCE REQUIREMENTS:**
- **File Size Limit**: NO files over 400 lines
- **Single Responsibility**: Each file must have ONE clear purpose
- **Clean Interfaces**: Well-defined imports/exports
- **Documentation**: README.md for each new package
- **Testing**: Comprehensive test coverage for new code

### **WHAT NOT TO DO:**
- ❌ **DO NOT** CREATE A FILE WITHOUT CHECKING TO SEE IF WE HAVE AN EXISTING SOLUTION USE THAT OR ADD TO IT BEFORE CREATING A FILE ONLY CREATE A NEW FILE IF YOU HAVE TO
- ❌ **DO NOT** create files over 400 lines
- ❌ **DO NOT** violate single responsibility principle
- ❌ **DO NOT** create circular dependencies
- ❌ **DO NOT** ignore import/export standards
- ❌ **DO NOT** skip documentation requirements
- ❌ **DO NOT** contribute to technical debt

### **QUALITY GATES:**
- **Pre-commit**: All files must pass size checks
- **Code Review**: All new code must be reviewed
- **Testing**: All new functionality must be tested
- **Documentation**: All new packages must be documented

---

## 📊 **PROGRESS TRACKING REQUIREMENTS**

### **Daily Updates (Required):**
1. **Status.json Update**: Every 7 minutes maximum
2. **Discord Devlog Entry**: At least one entry per day
3. **Inbox Report**: Progress update to Captain
4. **Contract Update**: Task completion status

### **Weekly Reports (Required):**
1. **Comprehensive Progress Report** to Captain
2. **Technical Debt Assessment** if any found
3. **Next Week Planning** and resource requirements
4. **Blockers and Dependencies** identification

---

## 🎯 **SUCCESS CRITERIA**

### **Immediate Success (5 minutes):**
- [ ] All mandatory commands executed
- [ ] Inbox acknowledgment sent
- [ ] Status updated in FSM system
- [ ] Discord devlog entry created
- [ ] Changes committed and pushed

### **Daily Success:**
- [ ] Status updated every 7 minutes
- [ ] Progress logged in Discord devlog
- [ ] Blockers reported immediately
- [ ] New ideas submitted promptly
- [ ] V2 compliance maintained

### **Weekly Success:**
- [ ] Comprehensive progress report
- [ ] Technical debt assessment
- [ ] Next week planning
- [ ] All blockers resolved
- [ ] Quality standards maintained

---

## 🚨 **FINAL WARNING**

**THIS PROTOCOL IS MANDATORY FOR ALL AGENTS. FAILURE TO COMPLY RESULTS IN IMMEDIATE CONSEQUENCES. EXECUTE ALL COMMANDS NOW - NOT LATER, NOT TOMORROW, NOW.**

**Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager**
