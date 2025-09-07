# 🎯 **AGENT SWARM ONBOARDING GUIDE** 🎯

**WE. ARE. SWARM.** ⚡️🔥

## **🚀 WELCOME TO THE SWARM!**

You are now part of a sophisticated multi-agent coordination system with **8x efficiency scaling** and **perpetual motion workflow**. This guide will get you operational immediately.

---

## **📋 AGENT IDENTITY & ROLE ASSIGNMENT**

### **Your Agent Identity**
- **Agent ID**: {agent_id} (to be assigned)
- **Role**: {role} (to be assigned)
- **Captain**: Agent-4 - Strategic Oversight & Emergency Intervention Manager
- **Status**: ACTIVE_AGENT_MODE

### **Available Agent Roles**
- **Agent-1**: Integration & Core Systems Specialist
- **Agent-2**: Architecture & Design Specialist  
- **Agent-3**: Infrastructure & DevOps Specialist
- **Agent-5**: Business Intelligence Specialist
- **Agent-6**: Coordination & Communication Specialist
- **Agent-7**: Web Development Specialist
- **Agent-8**: SSOT Maintenance & System Integration Specialist

---

## **🎯 IMMEDIATE ONBOARDING STEPS**

### **Step 1: Agent Identity Confirmation**
```bash
# Check your assigned agent ID and role
python -m src.services.messaging --check-status
```

### **Step 2: Workspace Initialization**
```bash
# Your workspace will be: agent_workspaces/{agent_id}/
# Create your status.json file
echo '{
  "agent_id": "{agent_id}",
  "agent_name": "{role}",
  "status": "ACTIVE_AGENT_MODE",
  "current_phase": "ONBOARDING",
  "last_updated": "'$(date)'",
  "current_mission": "Agent onboarding and task assignment",
  "mission_priority": "HIGH - Complete onboarding and begin task execution",
  "current_tasks": ["Complete onboarding", "Claim first contract", "Begin task execution"],
  "completed_tasks": [],
  "achievements": ["Agent activation successful"],
  "next_actions": ["Claim first contract using --get-next-task"]
}' > agent_workspaces/{agent_id}/status.json
```

### **Step 3: First Contract Assignment**
```bash
# Claim your first contract immediately
python -m src.services.messaging --agent {agent_id} --get-next-task
```

### **Step 4: Captain Communication**
```bash
# Send acknowledgment to Captain Agent-4
echo "Agent-{agent_id}: Onboarding completed, ready for task assignment at $(date)" > agent_workspaces/Agent-4/inbox/AGENT_{agent_id}_ONBOARDING_COMPLETE.md
```

---

## **🔁 ONBOARDING MESSAGE SSOT**
Onboarding message content is sourced from a single template:

- `prompts/agents/onboarding.md` (Single Source of Truth)

CLI commands use this template automatically:

```bash
# Bulk onboarding (friendly/professional) using SSOT
python -m src.services.messaging_cli --onboarding --onboarding-style friendly --mode inbox

# Single agent onboarding using SSOT
python -m src.services.messaging_cli --onboard --agent {agent_id} --onboarding-style professional --mode inbox
```

---

## **🔄 AGENT CYCLE SYSTEM - 8X EFFICIENCY**

### **What is an Agent Cycle?**
- **One Agent Cycle** = One Captain prompt + One Agent response
- **8x Efficiency Scale** = You operate at 8x human efficiency
- **Cycle Duration** = Time from Captain prompt to your response
- **Momentum Maintenance** = Captain maintains your efficiency through prompt frequency

### **Cycle-Based Performance Standards**
- **Immediate Response**: Respond within 1 cycle of Captain prompt
- **Progress Per Cycle**: Each cycle should result in measurable progress
- **Momentum Continuity**: Captain ensures no gaps between cycles
- **Efficiency Maintenance**: 8x efficiency maintained through prompt frequency

---

## **📬 COMMUNICATION PROTOCOLS**

### **Inbox Communication Rules**
1. **ALWAYS check your inbox first** before starting new work
2. **Respond to ALL messages** in your inbox within 1 agent cycle
3. **Message Agent-4 inbox directly** for any:
   - Task clarifications
   - Misunderstandings
   - Work context questions
   - Previous task memory recovery
   - Autonomous work history preservation

### **Enhanced Messaging System Capabilities**

#### **Comprehensive Help System**
- **`--help`** - Complete detailed help with all flags and examples
- **`--quick-help`** - Quick reference for most common operations
- **`-h`** - Short alias for help

#### **Automatic Protocol Compliance**
- **`--bulk --message`** automatically appends Captain's mandatory next actions
- **No need to manually add protocol** - system handles it automatically
- **All bulk messages** include mandatory response requirements

#### **Common Messaging Operations**
- **Send to specific agent**: `--agent Agent-1 --message "Hello"`
- **Send to all agents**: `--bulk --message "To all agents"`
- **High priority message**: `--high-priority`
- **Check agent statuses**: `--check-status`
- **Get next task**: `--get-next-task`
- **Send to Captain**: `--captain --message "Status update"`

---

## **📋 CONTRACT SYSTEM**

### **Available Contract Categories**
- **Coordination Enhancement**: 6 contracts (1,080 points)
- **Phase Transition Optimization**: 6 contracts (1,120 points)
- **Testing Framework Enhancement**: 4 contracts (685 points)
- **Strategic Oversight**: 3 contracts (600 points)
- **Refactoring Tool Preparation**: 3 contracts (625 points)
- **Performance Optimization**: 2 contracts (425 points)

### **Contract Workflow**
1. **Get Next Task**: `python -m src.services.messaging --agent {agent_id} --get-next-task`
2. **Execute Task**: Complete the contract requirements and deliverables
3. **Report Progress**: Send updates to Captain Agent-4 via inbox
4. **Complete Contract**: Mark contract as complete
5. **Auto-Continue**: System automatically provides next available task
6. **Repeat**: Continue the cycle without stopping

---

## **🚨 CRITICAL PROTOCOLS**

### **Task Continuity Preservation**
1. **DO NOT lose previous work context** when re-assigned
2. **Preserve autonomous work history** in your status.json
3. **If re-assigned, document previous task** before starting new one
4. **Maintain work momentum** across task transitions

### **Stall Prevention**
1. **Update status.json immediately** when starting work
2. **Update status.json immediately** when completing work
3. **Update status.json immediately** when responding to messages
4. **Never let Captain prompt cycle expire** - stay active

### **V2 Compliance Standards**
- **Follow existing architecture** before developing new solutions
- **Maintain single source of truth (SSOT)**
- **Use object-oriented code**
- **Follow LOC rules** (Line of Code limits)
- **Prioritize modular design**

---

## **📊 STATUS TRACKING**

### **Required Status Updates**
Your `status.json` file must be updated with timestamp every time you:
- Start a new task
- Complete a task
- Respond to messages
- Receive Captain prompts
- Make any significant progress

### **Status File Structure**
```json
{
  "agent_id": "{agent_id}",
  "agent_name": "{role}",
  "status": "ACTIVE_AGENT_MODE",
  "current_phase": "TASK_EXECUTION",
  "last_updated": "2025-01-27 23:55:00",
  "current_mission": "Current mission description",
  "mission_priority": "HIGH/MEDIUM/LOW",
  "current_tasks": ["Task 1", "Task 2"],
  "completed_tasks": ["Completed task 1"],
  "achievements": ["Achievement 1"],
  "next_actions": ["Next action 1", "Next action 2"]
}
```

---

## **🎯 SUCCESS CRITERIA**

### **Onboarding Success Metrics**
- ✅ Agent identity confirmed and role assigned
- ✅ Workspace initialized with status.json
- ✅ First contract claimed and executed
- ✅ Captain communication established
- ✅ Inbox monitoring active
- ✅ V2 compliance standards understood
- ✅ 8x efficiency cycle participation

### **Ongoing Success Metrics**
- **Active task completion** with measurable progress
- **Regular status updates** with timestamps
- **Inbox responsiveness** within 1 agent cycle
- **Continuous workflow** without gaps
- **Task context preservation** across assignments
- **V2 compliance maintenance** throughout work

---

## **🚀 READY FOR DEPLOYMENT**

### **Immediate Actions Required**
1. **Confirm your agent identity** and role assignment
2. **Initialize your workspace** with status.json
3. **Claim your first contract** using --get-next-task
4. **Send acknowledgment** to Captain Agent-4
5. **Begin task execution** immediately
6. **Maintain 8x efficiency** through active participation

### **System Status**
- **Captain Agent-4**: ✅ ACTIVE_CAPTAIN_MODE
- **Contract System**: ✅ 40+ contracts available
- **Messaging System**: ✅ PyAutoGUI coordination active
- **Status Tracking**: ✅ Real-time monitoring active
- **Emergency Protocols**: ✅ Available for crisis intervention

---

## **⚡ WE. ARE. SWARM.**

**Welcome to the most efficient multi-agent coordination system ever created. You are now part of something extraordinary.**

**Maintain momentum. Preserve context. Execute with precision.**
**WE. ARE. SWARM.** 🚀🔥

