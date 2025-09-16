# AUTONOMOUS AGENT WORKFLOW DOCUMENTATION
============================================

## 🌐 UNIVERSAL AGENT LOOP - STANDARD OPERATING PROCEDURE

### **MODE: CONTINUOUS_AUTONOMY**

This document establishes the standard autonomous workflow cycle that all agents MUST follow for continuous operation and task management.

---

## 🔄 **AUTONOMOUS WORKFLOW CYCLE**

### **1. MAILBOX CHECK (Priority: HIGH)**
```
Check: agent_workspaces/{AGENT_ID}/inbox/
Action:
  - Scan for new messages
  - Process each message immediately
  - Remove processed messages from inbox
  - Move to processed/ subfolder
```

### **2. TASK STATUS EVALUATION (Priority: HIGH)**
```
Check: agent_workspaces/{AGENT_ID}/working_tasks.json
Current Task Status:
  - If has "current_task" with status "in_progress": CONTINUE/COMPLETE
  - If has "current_task" with status "completed": MOVE TO NEXT PHASE
  - If no current task: PROCEED TO TASK CLAIMING
```

### **3. TASK CLAIMING (Priority: MEDIUM)**
```
Check: agent_workspaces/{AGENT_ID}/future_tasks.json
Actions:
  - Scan available tasks
  - Validate dependencies
  - Claim appropriate task based on priority/skills
  - Update working_tasks.json with claimed task
  - Begin task execution
```

### **4. BLOCKER RESOLUTION (Priority: MEDIUM)**
```
Check for:
  - Unresolved blockers
  - Schema errors
  - Integration issues
Actions:
  - Propose solutions
  - Create solution tasks if needed
  - Escalate to Captain if necessary
```

### **5. AUTONOMOUS OPERATION (Priority: LOW)**
```
If no urgent tasks pending:
  - Work on Masterpiece project (Captain agents)
  - Review and optimize codebase
  - Create improvement tasks
  - Return to mailbox check between operations
```

---

## 📋 **WORKFLOW EXECUTION EXAMPLE**

### **Agent-2 Task Claiming Automation Implementation (COMPLETED)**

#### **Phase 1: Mailbox Check**
- ✅ Checked inbox for messages
- ✅ Processed Agent-6 coordination enhancement analysis
- ✅ Responded with acknowledgment

#### **Phase 2: Task Status Evaluation**
- ✅ Checked working_tasks.json
- ✅ Found "task_claiming_automation" task with status "in_progress"
- ✅ Identified Phase 1 as "in_progress"

#### **Phase 3: Task Execution**
- ✅ **Phase 1**: Designed task claiming automation framework
  - Created `src/core/task_claiming_automation.py` (397 lines, V2 compliant)
  - Updated working_tasks.json: Phase 1 → "completed", Phase 2 → "in_progress"

- ✅ **Phase 2**: Implemented task claiming automation system
  - Created `src/core/test_task_claiming_automation.py`
  - Executed comprehensive test suite: 5/5 tests passed
  - Updated working_tasks.json: Phase 2 → "completed", Phase 3 → "in_progress"

- ✅ **Phase 3**: Validated task claiming automation effectiveness
  - All tests passed successfully
  - Updated working_tasks.json: Phase 3 → "completed"
  - Updated task status: "in_progress" → "completed"
  - Added completion timestamp

#### **Phase 4: Status Reporting**
- ✅ Sent completion report to Captain Agent-4
- ✅ Updated TODO list with completion status
- ✅ Documented implementation details

#### **Phase 5: Next Cycle Preparation**
- ✅ Checked future_tasks.json (empty - no pending tasks)
- ✅ Ready for new task assignments
- ✅ Autonomous loop operational

---

## 🎯 **WORKFLOW VALIDATION CRITERIA**

### **Task Completion Validation**
1. **Code Implementation**: All required modules created and functional
2. **V2 Compliance**: All files ≤400 lines, proper structure
3. **Testing**: Comprehensive test suite with 100% pass rate
4. **Documentation**: Clear documentation and usage examples
5. **Integration**: Proper integration with existing systems
6. **Self-Validation**: Self-validation protocol executed successfully

### **Phase Progression Rules**
- **Phase completion**: All objectives met, tests pass, documentation updated
- **Status updates**: working_tasks.json updated with phase completion
- **Validation**: Self-validation protocol confirms completion
- **Reporting**: Captain notified of phase/task completion

---

## 📝 **STANDARD MESSAGE FORMAT**

### **Message Structure**
```
============================================================
[A2A] MESSAGE
============================================================
📤 FROM: {AGENT_ID}
📥 TO: {TARGET_AGENT}
Priority: {NORMAL|HIGH|URGENT}
Tags: {GENERAL|COORDINATION|TASK|STATUS}
------------------------------------------------------------
{CONTENT}
------------------------------------------------------------
```

### **Status Report Format**
```
{AGENT_ID} {TASK_TYPE} COMPLETION REPORT: {Brief description}
📊 Status: {COMPLETED|IN_PROGRESS|BLOCKED}
🎯 Task: {task_id}
⏰ Duration: {completion_time}
✅ Validation: {self_validation_results}
📁 Files: {list_of_created_files}
🔗 Integration: {integration_status}
📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory
```

---

## 🚫 **DRIFT CONTROL PROTOCOL**

### **Prevention Measures**
- **File Edit Limit**: Maximum 2 attempts per file edit
- **Task Timeout**: Return to mailbox check after each action
- **Status Validation**: Verify task completion before claiming new tasks
- **Documentation**: Document all actions and decisions

### **Recovery Actions**
- **Edit Failures**: Report failure, move to next task
- **Blocked Tasks**: Escalate to Captain, create solution task
- **Integration Issues**: Document issue, propose workaround
- **Validation Failures**: Re-run validation, fix issues

---

## 🏆 **SUCCESS METRICS**

### **Autonomous Operation Indicators**
- ✅ Continuous mailbox processing
- ✅ Task claiming and completion
- ✅ Self-validation protocol execution
- ✅ Status reporting to Captain
- ✅ V2 compliance maintenance
- ✅ Integration with swarm systems

### **Quality Assurance**
- 📊 Test coverage: 100% for new modules
- 📏 V2 compliance: All files ≤400 lines
- 🔗 Integration: Proper system integration
- 📝 Documentation: Clear and comprehensive
- 🎯 Validation: Self-validation protocol success

---

## 🔄 **CONTINUOUS IMPROVEMENT**

### **Workflow Optimization**
- Monitor workflow efficiency
- Identify bottlenecks
- Propose improvements
- Update documentation
- Share best practices

### **Knowledge Sharing**
- Document successful patterns
- Create reusable templates
- Share lessons learned
- Update onboarding materials
- Train other agents

---

**This autonomous workflow ensures continuous agent operation, efficient task management, and quality delivery while maintaining swarm coordination and system integration.**

