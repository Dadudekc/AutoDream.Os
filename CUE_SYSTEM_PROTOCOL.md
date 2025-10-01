# 🎯 CUE SYSTEM PROTOCOL - V2_SWARM Coordination

## 📋 PROTOCOL OVERVIEW

**Purpose**: Enable coordinated responses between agents using cue-based messaging
**Scope**: All active agents in Quality Focus Team
**Priority**: HIGH
**Status**: ACTIVE

---

## 🔄 CUE SYSTEM OPERATION

### How It Works
1. **Captain sends message with CUE_ID**: Includes specific cue identifier
2. **Agents respond using cue command**: Use consolidated messaging service cue command
3. **Coordinated responses**: All agents can respond to same cue systematically

### CUE Command Format
```bash
python src/services/consolidated_messaging_service.py cue --agents [TARGET_AGENTS] --message "[RESPONSE]" --cue [CUE_ID] --from-agent [SENDER_AGENT]
```

### Example Usage
```bash
# Agent-5 responding to cue "TASK_WORKFLOW_001"
python src/services/consolidated_messaging_service.py cue --agents Agent-4 --message "Task workflow framework designed successfully" --cue TASK_WORKFLOW_001 --from-agent Agent-5

# Agent-6 responding to cue "QUALITY_VALIDATION_001"
python src/services/consolidated_messaging_service.py cue --agents Agent-4 --message "V2 compliance validated at 89.5%" --cue QUALITY_VALIDATION_001 --from-agent Agent-6
```

---

## 🎯 CUE SYSTEM PROTOCOLS

### Protocol 1: Task Coordination Cues
- **CUE_ID Format**: `TASK_[MISSION]_[SEQUENCE]`
- **Example**: `TASK_WORKFLOW_001`, `TASK_QUALITY_002`
- **Purpose**: Coordinate task execution across agents

### Protocol 2: Quality Validation Cues
- **CUE_ID Format**: `QUALITY_[TYPE]_[SEQUENCE]`
- **Example**: `QUALITY_VALIDATION_001`, `QUALITY_GATES_002`
- **Purpose**: Coordinate quality validation processes

### Protocol 3: Integration Cues
- **CUE_ID Format**: `INTEGRATION_[COMPONENT]_[SEQUENCE]`
- **Example**: `INTEGRATION_DISCORD_001`, `INTEGRATION_SSOT_002`
- **Purpose**: Coordinate system integration tasks

### Protocol 4: Status Report Cues
- **CUE_ID Format**: `STATUS_[AGENT]_[SEQUENCE]`
- **Example**: `STATUS_AGENT5_001`, `STATUS_AGENT6_002`
- **Purpose**: Coordinate status reporting

---

## 🚀 AGENT RESPONSE REQUIREMENTS

### When to Use CUE System
1. **Captain sends message with CUE_ID**: Always respond using cue system
2. **Coordination requests**: Use cue system for multi-agent coordination
3. **Status updates**: Use cue system for mission status updates
4. **Task completion**: Use cue system for task completion notifications

### Response Requirements
1. **Include CUE_ID**: Always include the original cue ID in response
2. **Target Captain**: Send responses to Agent-4 (Captain) unless specified otherwise
3. **Include Status**: Include current task status and progress
4. **Include Next Steps**: Include planned next actions

### Response Format
```
CUE_RESPONSE: [CUE_ID]
STATUS: [Current status]
PROGRESS: [Progress percentage]
NEXT_STEPS: [Planned actions]
REPORT: [Detailed status report]
```

---

## 🎯 QUALITY FOCUS TEAM CUE COORDINATION

### Agent Responsibilities
- **Agent-4 (Captain)**: Initiates cues and coordinates responses
- **Agent-5 (Coordinator)**: Responds to task assignment workflow cues
- **Agent-6 (Quality)**: Responds to quality validation cues
- **Agent-7 (Implementation)**: Responds to implementation task cues
- **Agent-8 (SSOT)**: Responds to SSOT validation cues

### Coordination Examples
```bash
# Captain initiates task coordination cue
python src/services/consolidated_messaging_service.py send --agent Agent-5 --message "Design task assignment framework" --cue TASK_WORKFLOW_001 --from-agent Agent-4

# Agent-5 responds using cue system
python src/services/consolidated_messaging_service.py cue --agents Agent-4 --message "CUE_RESPONSE: TASK_WORKFLOW_001, STATUS: ACTIVE, PROGRESS: 75%, NEXT_STEPS: Implement agent capability matching" --cue TASK_WORKFLOW_001 --from-agent Agent-5
```

---

## 🐝 WE ARE SWARM - CUE SYSTEM ACTIVE

**The CUE System Protocol is now active for all Quality Focus Team agents. Use the cue system for coordinated responses and mission coordination.**

**Status**: CUE_SYSTEM_PROTOCOL_ACTIVE
**Team**: Quality Focus Team (5 agents)
**Priority**: HIGH

**All agents must respond using the cue system when receiving messages with CUE_ID!** 🚀

---

*CUE System Protocol established by Captain Agent-4*
*Timestamp: 2025-01-27 05:30:00*
