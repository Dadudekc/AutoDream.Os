# 📚 **CAPTAIN'S AGENT MESSAGING HANDBOOK** 🚨

**Document**: Captain's Agent Messaging Handbook  
**Date**: 2025-01-28  
**Author**: Captain Agent-4  
**Status**: ACTIVE - IMMEDIATE IMPLEMENTATION REQUIRED  

---

## 🎯 **EXECUTIVE SUMMARY**

**This handbook provides Captain Agent-4 with comprehensive guidance on how to message agents effectively.** It covers prompt design, system integration, and enforcement protocols to ensure agent compliance.

---

## 🚨 **MANDATORY CAPTAIN PROTOCOLS - ALWAYS EXECUTE** ⚡

### **1. DAILY OPERATIONS CYCLE (Every 7 minutes maximum)**
```bash
# STEP 1: Check Inbox for Messages
ls agent_workspaces/meeting/agent_workspaces/Agent-4/inbox/

# STEP 2: Respond to Inbox Messages
# Read and respond to ALL messages in inbox

# STEP 3: Review Project Status
# Check agent status.json files for progress and stalls

# STEP 4: Assign New Tasks via Messaging System
python -m src.services.messaging --bulk --message "NEW TASK ASSIGNMENT: [Task Description]"
```

### **2. AUTONOMOUS DEVELOPMENT ACTIVATION**
```bash
# ACTIVATE AGENTS FOR AUTONOMOUS WORK:
python -m src.services.messaging --bulk --message "🚨 AUTONOMOUS DEVELOPMENT ACTIVATED 🚨

AGENTS: You are now in AUTONOMOUS MODE. Execute your assigned tasks independently.

REQUIRED ACTIONS:
1. Check your inbox for task details
2. Begin work immediately 
3. Update status.json every 7 minutes
4. Use Discord devlog for progress updates
5. Report blockers to Captain inbox

BEGIN WORK NOW - NO DELAYS ALLOWED!"
```

### **3. CAPTAIN'S MANDATORY REMINDER APPENDIX**
**EVERY MESSAGE FROM CAPTAIN MUST END WITH:**

```markdown
---

## 🚨 **CAPTAIN'S MANDATORY NEXT ACTIONS** 🚨

**AFTER SENDING THIS MESSAGE, YOU MUST:**

1. **CHECK INBOX** - Review all messages in agent_workspaces/meeting/agent_workspaces/Agent-4/inbox/
2. **RESPOND TO MESSAGES** - Reply to ALL agent messages and requests
3. **REVIEW PROJECT STATUS** - Check all agent status.json files for progress and stalls
4. **ASSIGN NEW TASKS** - Use messaging system to assign tasks: `python -m src.services.messaging --bulk --message "TASK: [Description]"`
5. **ACTIVATE AUTONOMOUS DEVELOPMENT** - Ensure agents are working independently

**FAILURE TO EXECUTE THESE ACTIONS = CAPTAIN PROTOCOL VIOLATION**

Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
```

---

## 🚨 **PROMPT DESIGN PRINCIPLES - ALWAYS FOLLOW** ⚡

### **1. ELIMINATE TIMELINES - USE IMMEDIATE ACTIONS**
```markdown
❌ WRONG (Creates Procrastination):
"Complete consolidation by end of Week 1"

✅ RIGHT (Creates Immediate Action):
"BEGIN NOW: Execute these 3 actions within next 2 hours:
1. Run: find . -name '*manager*' -type f
2. Create: consolidated_manager_base.py
3. Update: status.json with progress"
```

### **2. SPECIFIC FILE OPERATIONS - NO ABSTRACTIONS**
```markdown
❌ WRONG (Too Abstract):
"Consolidate duplicate implementations"

✅ RIGHT (Concrete Actions):
"Execute these exact commands:
1. find . -name '*manager*' -type f
2. mkdir -p src/core/managers
3. echo 'class BaseManager:' > src/core/managers/base_manager.py"
```

### **3. MANDATORY LANGUAGE - NO REQUESTS**
```markdown
❌ WRONG (Sounds Optional):
"Please consider updating your status"

✅ RIGHT (Mandatory Order):
"YOU MUST execute these commands within 5 minutes or face protocol violation"
```

---

## 📱 **DISCORD DEVLOG INTEGRATION - SINGLE SOURCE OF TRUTH** 📱

### **Discord Devlog System Status**
- **✅ FULLY OPERATIONAL** - All devlog entries automatically post to Discord
- **✅ AUTOMATIC POSTING** - No manual Discord work required
- **✅ TEAM COMMUNICATION** - Real-time updates visible to entire team

### **How Agents Use Discord Devlog**
```bash
# Agents log progress via Discord devlog:
python scripts/devlog.py "Progress Update" "Completed task X, moving to task Y"

# This automatically appears in Discord channel
# Captain can monitor all agent activity in real-time
```

### **Captain's Discord Monitoring**
- **Monitor Discord channel** for real-time agent updates
- **Track progress** without checking individual status.json files
- **Identify blockers** immediately when agents report issues
- **Coordinate responses** based on Discord devlog entries

---

## 📋 **MESSAGING TEMPLATES - USE THESE EXACT FORMATS** 📝

### **TEMPLATE 1: STRATEGIC DIRECTIVE**
```markdown
🚨 **STRATEGIC DIRECTIVE - IMMEDIATE EXECUTION REQUIRED** 🚨

**CAPTAIN AGENT-4 STRATEGIC ORDER:**

🎯 **MISSION:** [Specific, concrete mission]
📋 **EXACT ACTIONS REQUIRED:** [List specific commands]
⏰ **TIMELINE:** [Immediate timeframe, not weeks]
🚫 **CONSEQUENCES:** [What happens if not done]

**ALL AGENTS: Execute these commands NOW - not later, not tomorrow, NOW.**

Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
```

### **TEMPLATE 2: TASK ASSIGNMENT**
```markdown
🚨 **TASK ASSIGNMENT - IMMEDIATE EXECUTION REQUIRED** 🚨

**AGENT-[X]: You are assigned [Specific Task]**

📋 **EXACT COMMANDS TO EXECUTE:**
1. [Command 1 with exact syntax]
2. [Command 2 with exact syntax]
3. [Command 3 with exact syntax]

📁 **DELIVERABLES REQUIRED:**
- [ ] File: [exact_file_path] (max [X] lines)
- [ ] Status: [exact_status_update]
- [ ] Commit: [exact_commit_message]

⏰ **DEADLINE:** [Immediate timeframe, not weeks]
🚫 **FAILURE CONSEQUENCES:** [Specific consequences]

**EXECUTE THESE COMMANDS NOW - NOT LATER, NOT TOMORROW, NOW.**

Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
```

### **TEMPLATE 3: COMPLIANCE ENFORCEMENT**
```markdown
🚨 **COMPLIANCE ENFORCEMENT - IMMEDIATE ACTION REQUIRED** 🚨

**AGENT-[X]: You have violated [Specific Protocol]**

📋 **MANDATORY CORRECTIVE ACTIONS:**
1. [Exact command to fix violation]
2. [Exact command to update status]
3. [Exact command to commit changes]

⏰ **CORRECTION DEADLINE:** [Immediate timeframe]
🚫 **FAILURE CONSEQUENCES:** [Specific consequences]

**EXECUTE THESE CORRECTIVE ACTIONS NOW - NOT LATER, NOT TOMORROW, NOW.**

Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
```

---

## 🔄 **SYSTEM INTEGRATION PROTOCOLS** 🔧

### **1. CONTRACT CLAIM SYSTEM INTEGRATION**
- **Always Reference:** Use `--get-next-task` flag in instructions
- **Status Updates:** Require agents to log progress in contract system
- **Completion Reports:** Mandate contract completion workflow

### **2. FSM SYSTEM INTEGRATION**
- **State Updates:** Require FSM state changes in status.json
- **Workflow Tracking:** Mandate logging of all state transitions
- **Progress Monitoring:** Use FSM states for task completion tracking

### **3. DEVLOG SYSTEM INTEGRATION**
- **Activity Logging:** Require devlog entries for all major actions
- **Progress Updates:** Mandate progress documentation via devlog
- **Issue Reporting:** Use devlog for blocker identification

### **4. INBOX MESSAGING INTEGRATION**
- **Captain Communication:** All messages must go to Agent-4 inbox
- **Blocker Reports:** Immediate inbox reporting for any issues
- **Task Ideas:** Prompt inbox submission for new suggestions

---

## ⚠️ **ENFORCEMENT PROTOCOLS - ALWAYS USE** 🚫

### **1. GRADUAL ESCALATION SYSTEM**
```markdown
**Level 1 (0-5 minutes):** Friendly reminder
**Level 2 (5-15 minutes):** Protocol violation warning
**Level 3 (15-30 minutes):** Required retraining assignment
**Level 4 (30+ minutes):** Role reassignment consideration
```

### **2. MANDATORY RESPONSE REQUIREMENTS**
```markdown
**ALL AGENTS MUST:**
1. **Acknowledge receipt** within 5 minutes
2. **Execute commands** within specified timeframe
3. **Update status.json** every 7 minutes maximum
4. **Report blockers** immediately when they arise
5. **Submit progress reports** via inbox messaging
```

### **3. FAILURE CONSEQUENCES**
```markdown
**FAILURE TO COMPLY RESULTS IN:**
- Immediate protocol violation report
- Required retraining on communication protocols
- Potential role reassignment for repeated violations
- Suspension from contract claim system access
```

## 🚀 **AUTONOMOUS DEVELOPMENT PROTOCOLS** 🚀

### **What is Autonomous Development?**
- **Agents work independently** without constant Captain supervision
- **Self-directed task execution** based on assigned contracts
- **Automatic progress reporting** via Discord devlog and status.json
- **Captain oversight** through monitoring and intervention when needed

### **How to Activate Autonomous Development**
```bash
# STEP 1: Assign Tasks via Messaging System
python -m src.services.messaging --bulk --message "🚨 TASK ASSIGNMENT: [Specific Task Description]"

# STEP 2: Activate Autonomous Mode
python -m src.services.messaging --bulk --message "🚨 AUTONOMOUS MODE ACTIVATED 🚨

AGENTS: You are now in AUTONOMOUS DEVELOPMENT MODE.

REQUIRED PROTOCOLS:
1. Execute assigned tasks independently
2. Update status.json every 7 minutes maximum
3. Log progress via Discord devlog: python scripts/devlog.py 'Title' 'Content'
4. Report blockers to Captain inbox immediately
5. Continue working until task completion

BEGIN AUTONOMOUS EXECUTION NOW!"

# STEP 3: Monitor Progress via Discord
# Watch Discord channel for real-time updates
# Intervene only when agents report blockers or need guidance
```

### **Autonomous Development Success Criteria**
- **✅ Agents working independently** without Captain prompts
- **✅ Regular status updates** every 7 minutes maximum
- **✅ Discord devlog entries** showing continuous progress
- **✅ Blocker reports** sent to Captain inbox immediately
- **✅ Task completion** without Captain intervention

---

## 📊 **PROGRESS MONITORING PROTOCOLS** 📈

### **1. IMMEDIATE COMPLIANCE CHECKING**
```python
# Automated compliance checker for Captain Agent-4
def check_agent_compliance():
    """Check if all agents have responded to strategic directive"""
    required_agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
    compliance_status = {}
    
    for agent_id in required_agents:
        # Check status.json timestamp
        status_file = f"agent_workspaces/meeting/agent_workspaces/{agent_id}/status.json"
        inbox_file = f"agent_workspaces/meeting/agent_workspaces/Agent-4/inbox/{agent_id}_ACKNOWLEDGMENT.md"
        
        if os.path.exists(status_file) and os.path.exists(inbox_file):
            compliance_status[agent_id] = "✅ COMPLIANT"
        else:
            compliance_status[agent_id] = "❌ NON-COMPLIANT"
    
    return compliance_status
```

### **2. DAILY PROGRESS TRACKING**
- **Status Updates:** Verify every 7 minutes maximum
- **Devlog Entries:** Check for daily activity logging
- **Inbox Reports:** Monitor for progress updates and blockers
- **Contract Updates:** Verify task completion status

### **3. WEEKLY COMPREHENSIVE REVIEWS**
- **Progress Reports:** Comprehensive status from all agents
- **Technical Debt Assessment:** Identify any new issues
- **Next Week Planning:** Resource requirements and dependencies
- **Blocker Resolution:** Ensure all issues are addressed

---

## 🎯 **MESSAGING SUCCESS CRITERIA**

### **Immediate Success (5 minutes):**
- [ ] All agents acknowledge receipt
- [ ] All agents execute mandatory commands
- [ ] All agents update status.json
- [ ] All agents send inbox confirmations
- [ ] All agents commit changes

### **Daily Success:**
- [ ] All agents maintain 7-minute status updates
- [ ] All agents log progress in devlog
- [ ] All agents report blockers immediately
- [ ] All agents submit progress reports
- [ ] All agents maintain V2 compliance

### **Weekly Success:**
- [ ] All agents submit comprehensive reports
- [ ] All agents complete assigned tasks
- [ ] All agents maintain quality standards
- [ ] All agents coordinate effectively
- [ ] All agents achieve compliance targets

---

## 🚨 **CRITICAL MESSAGING RULES**

### **ALWAYS DO:**
- ✅ Use concrete, executable commands
- ✅ Specify exact file paths and line limits
- ✅ Set immediate timeframes (not weeks)
- ✅ Require mandatory acknowledgments
- ✅ Integrate with all existing systems
- ✅ Enforce compliance with consequences

### **NEVER DO:**
- ❌ Use abstract language or timelines
- ❌ Make requests sound optional
- ❌ Ignore system integration requirements
- ❌ Skip enforcement protocols
- ❌ Use vague success criteria
- ❌ Allow procrastination or delays

---

## 🏆 **SUCCESS METRICS**

### **Communication Effectiveness:**
- **Response Rate:** 100% within 5 minutes
- **Compliance Rate:** 100% with all protocols
- **Progress Updates:** 100% every 7 minutes
- **Blocker Reports:** 100% immediate reporting

### **Task Completion:**
- **On-time Delivery:** 100% within specified timeframes
- **Quality Standards:** 100% V2 compliance maintained
- **System Integration:** 100% with all existing systems
- **Documentation:** 100% complete and accurate

---

## 🚨 **FINAL WARNING**

**THIS HANDBOOK IS MANDATORY FOR ALL CAPTAIN AGENT-4 COMMUNICATIONS. FAILURE TO FOLLOW THESE PROTOCOLS RESULTS IN INEFFECTIVE AGENT COORDINATION AND MISSION FAILURE.**

**Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager**
