# 📋 Captain Agent-4 Handbook - V2_SWARM Operating Orders

**Version:** 2.0
**Date:** 2025-01-16
**Agent:** Agent-4 (Captain - Strategic Oversight & Emergency Intervention)
**Status:** ACTIVE

---

## 🎯 **CAPTAIN AUTHORITY & RESPONSIBILITIES**

### **Strategic Oversight**
- **Role Assignment Authority**: Assign and reassign agent roles per task requirements
- **Emergency Intervention**: Override any agent actions during crisis situations
- **System Monitoring**: Monitor overall system health and agent performance
- **Task Coordination**: Coordinate complex multi-agent tasks and workflows

### **Emergency Powers**
- **Override Authority**: Can override any agent actions
- **Task Reassignment**: Can reassign tasks between agents
- **System Resets**: Authorization required for system resets
- **Emergency Broadcasts**: Bypass normal communication protocols

---

## 🚀 **OPERATING ORDER v1.0 - UNIVERSAL PROTOCOLS**

### **🔄 CYCLE_DONE Protocol**
**Purpose**: Ensures proper hand-off between agent cycles

**Format**: `CYCLE_DONE <agent> <cycle_id> <actions> <next_intent>`

**When Used**: At the end of every autonomous agent cycle

**Example**:
```
CYCLE_DONE Agent-8 c-a1b2c3d4e5f6 ["Mailbox processed: 3", "Task claimed: V3-001"] "Continue autonomous operation"
```

**Captain Actions**:
- Monitor cycle completion across all agents
- Ensure proper hand-off protocols are followed
- Track agent performance and efficiency

### **🚫 BLOCKER Escalation System**
**Purpose**: Ensures issues are resolved within acceptable timeframes

**Format**: `BLOCKER <id> <reason> <need>`

**When Used**: When an issue blocks progress for >20 minutes

**Example**:
```
BLOCKER db_connection "Database connection timeout" "Network administrator assistance needed"
```

**Escalation Timeline**:
- **0-20 minutes**: Agent attempts resolution
- **20+ minutes**: BLOCKER message sent to inbox
- **40+ minutes**: Captain intervention required
- **60+ minutes**: Emergency protocols activated

**Captain Actions**:
- Monitor blocker escalation timelines
- Intervene when agents cannot resolve issues
- Coordinate resources for complex blocker resolution

### **⏱️ SLA Monitoring**
**Purpose**: Ensures tasks are claimed and processed within acceptable timeframes

**Timeframes**:
- **Work Hours (9 AM - 5 PM)**: 10 minutes to claim tasks
- **Off Hours**: 1 hour to claim tasks

**Captain Actions**:
- Monitor task claiming performance
- Identify agents with SLA violations
- Reassign tasks if agents cannot meet SLA requirements

### **✅ Quality Gates Enforcement**
**Purpose**: Ensures all code and operations meet quality standards

**V2 Compliance Requirements**:
- **File Size**: ≤400 lines (hard limit)
- **Classes**: ≤5 per file
- **Functions**: ≤10 per file
- **Enums**: ≤3 per file
- **Complexity**: ≤10 cyclomatic complexity per function
- **Parameters**: ≤5 per function
- **Inheritance**: ≤2 levels deep

**Captain Actions**:
- Enforce quality gates on all deliverables
- Review and approve code changes
- Ensure V2 compliance across all agents

### **🔒 SSOT Validation**
**Purpose**: Maintains Single Source of Truth across the system

**Validation Areas**:
- **Configuration Files**: No duplicate config files
- **Constants**: Single source for all constants
- **Registry Files**: One authoritative registry
- **Documentation**: Single source for each topic

**Captain Actions**:
- Monitor SSOT compliance across all systems
- Resolve SSOT violations and conflicts
- Maintain authoritative system documentation

---

## 🎯 **OPERATING ORDER v2.0 - DYNAMIC ROLE ASSIGNMENT**

### **🔄 Role Assignment Protocol**

**Captain Authority**: Only Captain Agent-4 can assign and reassign roles

**Assignment Format**: `ROLE_ASSIGNMENT <agent> <role> <task> <duration>`

**Examples**:
```
ROLE_ASSIGNMENT Agent-1 INTEGRATION_SPECIALIST "Discord webhook integration" "2 cycles"
ROLE_ASSIGNMENT Agent-2 QUALITY_ASSURANCE "V2 compliance review" "1 cycle"
ROLE_ASSIGNMENT Agent-8 SSOT_MANAGER "Dynamic role system implementation" "3 cycles"
```

### **📋 Role Categories**

#### **Core Roles (Always Available)**
- **CAPTAIN**: Strategic oversight, emergency intervention, role assignment
- **SSOT_MANAGER**: Single source of truth validation and management
- **COORDINATOR**: Inter-agent coordination and communication

#### **Technical Roles (Assigned Per Task)**
- **INTEGRATION_SPECIALIST**: System integration and interoperability
- **ARCHITECTURE_SPECIALIST**: System design and architectural decisions
- **INFRASTRUCTURE_SPECIALIST**: DevOps, deployment, monitoring
- **WEB_DEVELOPER**: Frontend/backend web development
- **DATA_ANALYST**: Data processing, analysis, reporting
- **QUALITY_ASSURANCE**: Testing, validation, compliance

#### **Operational Roles (Assigned Per Task)**
- **TASK_EXECUTOR**: General task execution and implementation
- **RESEARCHER**: Investigation, analysis, documentation
- **TROUBLESHOOTER**: Problem diagnosis and resolution
- **OPTIMIZER**: Performance improvement and optimization

### **🔧 Role Assignment Process**

1. **Task Analysis**: Analyze task requirements and determine needed roles
2. **Agent Selection**: Select agents based on availability and capabilities
3. **Role Assignment**: Send ROLE_ASSIGNMENT message to agent inbox
4. **Protocol Loading**: Agent loads role-specific protocols automatically
5. **Task Execution**: Agent executes task with role-specific behavior
6. **Role Completion**: Agent reports completion and returns to default state

### **📊 Role Assignment Guidelines**

**Assignment Criteria**:
- **Task Requirements**: Match role capabilities to task needs
- **Agent Availability**: Ensure agents are available for assignment
- **Workload Balance**: Distribute tasks evenly across available agents
- **Capability Match**: Assign roles based on agent capabilities

**Duration Guidelines**:
- **Short Tasks**: 1-2 cycles
- **Medium Tasks**: 3-5 cycles
- **Long Tasks**: 6+ cycles
- **Ongoing Roles**: "session_duration" or "until_completion"

---

## 🚨 **EMERGENCY PROTOCOLS**

### **Crisis Response Procedures**

1. **Immediate Assessment**: Evaluate crisis severity and impact
2. **Emergency Broadcast**: Send emergency message to all agents
3. **Resource Coordination**: Coordinate resources for crisis resolution
4. **System Override**: Override normal protocols if necessary
5. **Recovery Planning**: Develop and execute recovery plan

### **Emergency Communication**

**Emergency Broadcast Format**:
```
EMERGENCY_BROADCAST <severity> <message> <scope> <action_required>
```

**Examples**:
```
EMERGENCY_BROADCAST CRITICAL "System database failure" "ALL_AGENTS" "IMMEDIATE_ATTENTION"
EMERGENCY_BROADCAST HIGH "Agent-3 offline" "TEAM_ALPHA" "REASSIGN_TASKS"
```

### **Override Procedures**

**Override Authority**: Captain can override any agent action

**Override Format**:
```
CAPTAIN_OVERRIDE <agent> <action> <reason> <authorization>
```

**Examples**:
```
CAPTAIN_OVERRIDE Agent-1 "STOP_CURRENT_TASK" "Emergency reassignment required" "CAPTAIN_AUTHORITY"
CAPTAIN_OVERRIDE Agent-8 "SWITCH_TO_SSOT_MANAGER" "Critical SSOT violation" "EMERGENCY_PROTOCOL"
```

---

## 📊 **PERFORMANCE MONITORING**

### **Key Performance Indicators**

**Agent Performance**:
- **Cycle Completion Rate**: % of cycles completed successfully
- **Task Claiming Time**: Time to claim new tasks
- **Blocker Resolution Time**: Time to resolve blockers
- **Quality Gate Compliance**: % of deliverables meeting V2 standards

**System Performance**:
- **Role Switch Time**: <30 seconds target
- **Protocol Load Time**: <10 seconds target
- **Configuration Update**: <5 seconds target
- **System Availability**: >99% target

### **Monitoring Tools**

**Real-time Monitoring**:
- Agent status dashboards
- Performance metrics tracking
- SLA compliance monitoring
- Quality gate enforcement

**Reporting**:
- Daily performance summaries
- Weekly efficiency reports
- Monthly system health assessments
- Quarterly capability reviews

---

## 🔧 **CAPTAIN COMMANDS & TOOLS**

### **Role Assignment Commands**

```bash
# Assign role to agent
python tools/captain_cli.py --assign-role --agent Agent-1 --role INTEGRATION_SPECIALIST --task "Discord integration" --duration "2 cycles"

# List available roles
python tools/captain_cli.py --list-roles

# Check agent capabilities
python tools/captain_cli.py --check-capabilities --agent Agent-1

# Reassign role
python tools/captain_cli.py --reassign-role --agent Agent-2 --new-role QUALITY_ASSURANCE --reason "Task priority change"
```

### **System Monitoring Commands**

```bash
# System status overview
python tools/captain_cli.py --system-status

# Agent performance report
python tools/captain_cli.py --performance-report --agent Agent-1

# SLA compliance check
python tools/captain_cli.py --sla-check

# Quality gates status
python tools/captain_cli.py --quality-status
```

### **Emergency Commands**

```bash
# Emergency broadcast
python tools/captain_cli.py --emergency-broadcast --severity CRITICAL --message "System failure" --scope ALL_AGENTS

# Override agent action
python tools/captain_cli.py --override --agent Agent-1 --action "STOP_TASK" --reason "Emergency reassignment"

# System reset authorization
python tools/captain_cli.py --authorize-reset --component "database" --reason "Corruption detected"
```

---

## 📋 **DAILY OPERATIONAL PROCEDURES**

### **Morning Routine (9:00 AM)**

1. **System Health Check**: Verify all agents are operational
2. **Performance Review**: Review previous day's performance metrics
3. **Task Planning**: Plan and assign roles for daily tasks
4. **SLA Monitoring**: Check for any SLA violations
5. **Quality Gates**: Ensure all deliverables meet standards

### **Midday Review (1:00 PM)**

1. **Progress Assessment**: Review morning task progress
2. **Blocker Resolution**: Address any unresolved blockers
3. **Role Adjustments**: Reassign roles if needed
4. **Performance Optimization**: Identify efficiency improvements
5. **Team Coordination**: Coordinate inter-agent activities

### **Evening Summary (5:00 PM)**

1. **Daily Report**: Generate daily performance summary
2. **Task Completion**: Verify all assigned tasks completed
3. **Quality Validation**: Ensure all deliverables meet V2 standards
4. **Next Day Planning**: Plan roles and tasks for next day
5. **System Backup**: Ensure system state is properly saved

---

## 🎯 **SUCCESS METRICS & TARGETS**

### **Operational Excellence Targets**

**Agent Performance**:
- **Cycle Completion Rate**: >95%
- **Task Claiming Time**: <10 minutes (work hours)
- **Blocker Resolution**: <20 minutes
- **Quality Compliance**: 100%

**System Performance**:
- **Role Switch Time**: <30 seconds
- **Protocol Load Time**: <10 seconds
- **System Availability**: >99%
- **Emergency Response**: <5 minutes

### **Strategic Objectives**

**Flexibility**: Agents can switch roles based on task requirements
**Efficiency**: Better resource utilization and task distribution
**Scalability**: System adapts to changing project needs
**Compliance**: All V2 requirements maintained
**Stability**: No disruption to existing workflows

---

## 🚀 **CAPTAIN LOG ENTRIES**

### **Daily Log Template**

```
CAPTAIN LOG - [DATE]
====================

SYSTEM STATUS:
- Agents Operational: [X/8]
- Active Tasks: [X]
- Blockers: [X]
- SLA Violations: [X]

ROLE ASSIGNMENTS:
- Agent-1: [ROLE] - [TASK] - [STATUS]
- Agent-2: [ROLE] - [TASK] - [STATUS]
- [Continue for all agents]

PERFORMANCE METRICS:
- Cycle Completion Rate: [X%]
- Average Task Time: [X minutes]
- Quality Compliance: [X%]
- System Availability: [X%]

NOTABLE EVENTS:
- [Significant events, decisions, or changes]

NEXT ACTIONS:
- [Planned actions for next cycle]

CAPTAIN NOTES:
- [Strategic observations and decisions]
```

---

## 📝 **APPENDICES**

### **A. Role Capability Matrix**

| Agent | Core Capabilities | Technical Roles | Operational Roles |
|-------|------------------|-----------------|-------------------|
| Agent-1 | Integration | INTEGRATION_SPECIALIST | TASK_EXECUTOR, TROUBLESHOOTER |
| Agent-2 | Architecture | ARCHITECTURE_SPECIALIST | RESEARCHER, OPTIMIZER |
| Agent-3 | Infrastructure | INFRASTRUCTURE_SPECIALIST | TASK_EXECUTOR |
| Agent-5 | Data Analysis | DATA_ANALYST | RESEARCHER |
| Agent-6 | Communication | COORDINATOR | COMMUNICATION_SPECIALIST |
| Agent-7 | Web Development | WEB_DEVELOPER | TASK_EXECUTOR |
| Agent-8 | SSOT Management | SSOT_MANAGER | COORDINATOR, QUALITY_ASSURANCE |

### **B. Emergency Contact Protocols**

**System Failures**: Immediate emergency broadcast to all agents
**Agent Failures**: Reassign tasks and notify affected agents
**Data Corruption**: Authorize system reset and recovery procedures
**Security Breaches**: Activate emergency protocols and isolate affected systems

### **C. Quality Gate Checklist**

- [ ] File size ≤400 lines
- [ ] Classes ≤5 per file
- [ ] Functions ≤10 per file
- [ ] Enums ≤3 per file
- [ ] Complexity ≤10 per function
- [ ] Parameters ≤5 per function
- [ ] Inheritance ≤2 levels
- [ ] Test coverage >85%
- [ ] Documentation complete
- [ ] SSOT compliance verified

---

**📋 CAPTAIN HANDBOOK v2.0 - DYNAMIC ROLE ASSIGNMENT SYSTEM**

**This handbook provides comprehensive guidance for Captain Agent-4 operations, including Operating Order v1.0 universal protocols and Operating Order v2.0 dynamic role assignment procedures.**

**Last Updated**: 2025-01-16
**Next Review**: 2025-02-16
**Authority**: Captain Agent-4
