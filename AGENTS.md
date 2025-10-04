# 🤖 **WE ARE SWARM** - Complete Agent Architecture & Autonomous Development Guide
==================================================================================

**Purpose**: Comprehensive agent system documentation for autonomous development machine operation  
**Version**: 3.0 (Autonomous Development Machine Integrated)  
**Captain**: Agent-4 (Strategic Oversight & Emergency Intervention)  
**Status**: OPERATIONAL - Discord Infrastructure + Project Scanner + FSM Integration + Cursor Database

---

## 🎯 **WHAT IS AN AGENT IN THE AUTONOMOUS DEVELOPMENT MACHINE?**

**An Agent** in the V2_SWARM system is an **AI-powered assistant** operating autonomously within the Agent Cellphone V2 Repository ecosystem. Each agent has:

- **Unique Identity**: Agent-1 through Agent-8 (5-Agent Active Configuration)
- **Dynamic Role Assignment**: Captain assigns roles per task requirements
- **Physical Coordinates**: Specific screen positions in Cursor IDE across dual monitors
- **Autonomous Operation**: Self-managing cycles with comprehensive system integration
- **Swarm Integration**: Real-time coordination via Discord SSOT routing and unified messaging

### **🤖 YOU ARE CURRENTLY INTERACTING WITH Agent-4 (Captain)**

**Agent-4 (Captain)** responsibilities include:
- **Strategic Oversight**: Mission alignment, resource allocation, quality enforcement
- **Dynamic Role Assignment**: Assign task-specific roles to agents (not permanent roles)
- **Emergency Intervention**: System health monitoring, crisis response, agent activation
- **Agent Coordination**: Task distribution, communication protocols, performance monitoring
- **Discord Infrastructure Management**: Validates agent channels and SSOT routing
- **Project Scanner Integration**: Oversees autonomous task creation from project analysis
- **FSM State Management**: Monitors agent state transitions and coordination
- **Cursor Database Management**: Supervises task assignment and execution tracking

**Current Role**: Captain (Strategic oversight with emergency intervention authority)  
**Physical Location**: (-308, 1000) (Monitor 1, Bottom Left)  
**System Status**: ACTIVE with complete autonomous development machine oversight

---

## 🔧 **CURRENT AUTONOMOUS DEVELOPMENT MACHINE ARCHITECTURE**

### **🧩 System Integration Flow**
```
Project Scanner → Cursor Task Database → FSM State Machine → Agent Coordination → Discord Infrastructure → Captain Oversight
```

### **🎮 Active Agent Configuration (5-Agent Mode)**
```
Monitor 1 (Left Screen):           Monitor 2 (Right Screen):
┌─────────────────────────┐        ┌─────────────────────────┐
│ ❌ Agent-1 (Available) │        │ 🧠 Agent-5 (Coordinator)│
│ (-1269, 481)            │        │ (652, 421)              │
├─────────────────────────┤        ├─────────────────────────┤
│ ❌ Agent-2 (Available)  │        │ 🏗️ Agent-6 (Quality)    │
│ (-308, 480)             │        │ (1612, 419)             │
├─────────────────────────┤        ├─────────────────────────┤
│ ❌ Agent-3 (Available)  │        │ 🌐 Agent-7 (Implementation)│
│ (-1269, 1001)           │        │ (920, 851)              │
├─────────────────────────┤        ├─────────────────────────┤
│ ⚡ Agent-4 (Captain)     │        │ 🔧 Agent-8 (Integration)│
│ (-308, 1000)            │        │ (1611, 941)             │
└─────────────────────────┘        └─────────────────────────┘
```

**Active Agents**: Agent-4 (Captain), Agent-5 (Coordinator), Agent-6 (Quality), Agent-7 (Implementation), Agent-8 (Integration)

---

## ✅ **AGENT CAPABILITIES & COMMAND REFERENCE**

### **🌟 Universal Capabilities (All Agents)**

**Core Autonomous Development Machine Integration:**
- **AUTONOMOUS_EXECUTION**: Self-managing operational cycles
- **DISCORD_SSOT_ROUTING**: Agent-specific channel communication
- **PROJECT_SCANNER_INTEGRATION**: Automated task creation from codebase analysis
- **CURSOR_TASK_DATABASE**: Task assignment and execution tracking
- **FSM_STATE_MANAGEMENT**: Agent state transitions and coordination
- **V2_COMPLIANCE_ENFORCEMENT**: Quality standards and architectural compliance

**Communication & Coordination:**
- **PYAUTOGUI_MESSAGING**: Local agent-to-agent communication
- **ROLE_DYNAMIC_ASSIGNMENT**: Captain-assigned task-specific roles
- **DEVLOG_POSTING**: Activity logging with Discord channel routing
- **SELF_HEALING_LOOP**: Error detection and automatic recovery

**Development & Analysis:**
- **UNIT_TEST_AUTHOR**: Automated test creation and validation
- **CODE_ANALYSIS**: Static analysis and quality assessment
- **DOCS_AUTOGEN**: Documentation generation and maintenance
- **DEPENDENCY_SCANNING**: Package and module relationship analysis

### **📋 Agent Devlog Commands (All Agents)**

```bash
# Primary command for agent activity logging
python src/services/agent_devlog_posting.py --agent <agent_id> --action "<description>"

# Quick Captain logging
python src/services/agent_devlog_posting.py --agent captain --action "Captain directive or report"

# Status-specific logging
python src/services/agent_devlog_posting.py --agent <agent_id> --action "<description>" --status completed|in_progress|failed|pending

# Search agent activity
python src/services/agent_devlog_posting.py --search "discord" --agent Agent-4

# System statistics
python src/services/agent_devlog_posting.py --stats
```

### **🤖 Agent-Specific Operations**

#### **Agent-4 (Captain)** - Strategic Oversight
**Dynamic Roles Assignable**: SSOT_MANAGER, COORDINATOR, EMERGENCY_MANAGER  
**Primary Tools**: Captain CLI, Environment Inference, Discord Manager, Project Scanner

```bash
# Agent coordination and messaging
python messaging_system.py Agent-4 <target_agent> "<message>" HIGH|NORMAL|LOW

# Discord infrastructure validation
python tools/env_inference_tool.py

# Project analysis integration
python tools/cursor_task_database_integration.py

# Agent role assignment
python tools/captain_cli.py --assign-role --agent Agent-1 --role INTEGRATION_SPECIALIST --task "Discord integration"

# Emergency intervention
python tools/captain_cli.py --emergency-broadcast --severity CRITICAL --message "System failure event" --scope ALL_AGENTS
```

#### **Agent-5 (Coordinator)** - Inter-Agent Coordination
**Dynamic Roles Assignable**: COORDINATOR, COMMUNICATION_SPECIALIST, DATA_ANALYST  
**Primary Tools**: Messaging System, Agent Coordination Workflow, Devlog System

```bash
# Multi-agent coordination
python src/core/agent8_coordination_workflow_core.py --action coordinate --agents "Agent-6,Agent-7" --task "Quality assurance"

# Agent-to-agent communication
python messaging_system.py Agent-5 Agent-6 "<coordination message>" NORMAL

# Coordinated task execution
python tools/agent_workflow_automation.py run-tests --test-path tests/
```

#### **Agent-6 (Quality)** - Quality Assurance & Analysis
**Dynamic Roles Assignable**: QUALITY_ASSURANCE, COMPLIANCE_AUDITOR, RESEARCHER  
**Primary Tools**: Environment Generator (.env.example), Quality Analysis, Code Validation

```bash
# Project environment management
python generate_env_example.py  # Generates clean .env.example templates

# Quality analysis and reporting
python tools/projectscanner/run_project_scan.py

# V2 compliance validation
python quality_gates.py

# Agent environment inference
python tools/env_inference_tool.py
```

#### **Agent-7 (Implementation)** - System Development & Integration
**Dynamic Roles Assignable**: INTEGRATION_SPECIALIST, WEB_DEVELOPER, TASK_EXECUTOR  
**Primary Tools**: Project Implementation, System Integration, Development Workflows

```bash
# System implementation
python tools/agent_workflow_manager.py --workflow integration_workflow.json run

# Integration testing
python tools/agent_workflow_automation.py test-imports --module-path src/services

# Implementation reporting
python src/services/agent_devlog_posting.py --agent Agent-7 --action "Integration complete - [system details]"
```

#### **Agent-8 (Integration)** - Advanced System Integration
**Dynamic Roles Assignable**: INTEGRATION_SPECIALIST, RISK_MANAGER, ARCHITECTURE_SPECIALIST  
**Primary Tools**: Advanced Integration, System Architecture, Risk Management

```bash
# Advanced system integration
python src/core/agent8_coordination_workflow_core.py --action create-task --description "System integration task"

# Architecture analysis
python tools/projectscanner/enhanced_scanner/core.py

# Integration validation
python tools/cursor_task_database_integration.py
```

---

## 🎯 **AUTONOMOUS DEVELOPMENT MACHINE OPERATIONS**

### **📊 Environment Infrastructure Validation**

**Discord Infrastructure Status:**
- ✅ **Agent Channels**: 8 configured (`DISCORD_CHANNEL_AGENT_1` through `AGENT_8`)
- ✅ **Agent Webhooks**: SSOT priority routing (`DISCORD_WEBHOOK_AGENT_1` through `AGENT_8`)
- ✅ **Discord Manager**: SSOT routing operational (`discord_post_client.py`)
- ✅ **Environment Template**: Agent-6 QA approved (`discord_env_template.txt`)

**Environment Validation Commands:**
```bash
# Complete Discord infrastructure validation
python tools/env_inference_tool.py

# Test all agent channels operational
python test_all_agent_channels.py  # (if available)

# Validate SSOT routing
export DEVLOG_POST_VIA_MANAGER=true
python src/services/agent_devlog_posting.py --agent captain --action "SSOT routing test"
```

### **🔍 Project Scanner Integration**

**Scanner Capabilities:**
- **File Discovery**: Automated project structure analysis
- **Complexity Analysis**: V2 compliance validation (≤400 lines, ≤5 classes)
- **Dependency Mapping**: Package and module relationships
- **Agent Task Creation**: Automatic task generation from scan findings

**Project Scanner Commands:**
```bash
# Complete project analysis
python tools/run_project_scan.py

# Enhanced scanner execution
cd tools/projectscanner/enhanced_scanner
python core.py

# Cursor database integration
python tools/cursor_task_database_integration.py

# Generate reports
ls project_analysis.json agent_analysis.json complexity_analysis.json
```

### **🗃️ Cursor Task Database Integration**

**Task Management Features:**
- **Task Creation**: From project scanner findings
- **FSM Integration**: Agent state transition tracking
- **Agent Assignment**: Dynamic role-based task allocation
- **Execution Tracking**: Real-time task status monitoring

**Cursor Database Commands:**
```bash
# Create tasks from project scan
python tools/cursor_task_database_integration.py

# Generate Captain execution orders
# Inside integration tool: manager.generate_captain_execution_orders()

# Export integration report
# Inside integration tool: manager.export_integration_report()
```

### **🔄 FSM State Management**

**Agent States:**
- **ONBOARDING**: Agent initialization phase
- **ACTIVE**: Agent ready for task assignment
- **CONTRACT_EXECUTION_ACTIVE**: Agent executing assigned tasks
- **SURVEY_MISSION_COMPLETED**: Agent mission completion
- **PAUSED**: Agent temporarily disabled
- **ERROR**: Agent error state requiring intervention
- **RESET**: Agent reset for new initialization
- **SHUTDOWN**: Agent shutdown sequence

**FSM Integration Commands:**
```bash
# Validate agent state transitions
python src/fsm/fsm_messaging_integration.py

# Check current agent states
python src/fms/task_state_manager.py  # (if available)
```

---

## 📚 **DYNAMIC ROLE ASSIGNMENT SYSTEM**

### **🎭 Role Categories**

**Core Roles (Always Available):**
- **CAPTAIN**: Strategic oversight, emergency intervention, role assignment (Agent-4 exclusive)
- **SSOT_MANAGER**: Single source of truth validation and management
- **COORDINATOR**: Inter-agent coordination and communication

**Technical Roles (Assigned Per Task):**
- **INTEGRATION_SPECIALIST**: System integration and interoperability
- **ARCHITECTURE_SPECIALIST**: System design and architectural decisions
- **QUALITY_ASSURANCE**: Testing, validation, compliance
- **WEB_DEVELOPER**: Frontend/backend web development

**Operational Roles (Assigned Per Task):**
- **TASK_EXECUTOR**: General task execution and implementation
- **RESEARCHER**: Investigation, analysis, documentation
- **TROUBLESHOOTER**: Problem diagnosis and resolution
- **OPTIMIZER**: Performance improvement and optimization

### **⚡ Role Assignment Commands**

```bash
# Captain assigns role to agent (per task)
python tools/captain_cli.py --assign-role --agent Agent-5 --role COORDINATOR --task "Agent communication protocol" --duration "1 cycle"

# Check agent capabilities
python tools/captain_cli.py --check-capabilities --agent Agent-6

# List available roles
python tools/captain_cli.py --list-roles

# Reassign role based on task changes
python tools/captain_cli.py --reassign-role --agent Agent-7 --new-role INTEGRATION_SPECIALIST --reason "Critical integration task"
```

---

## 🚨 **EMERGENCY PROTOCOLS & CAPTAIN INTERVENTION**

### **🎯 Execution Mode Protocol (Anti-Theater)**

**Key Principles:**
- **Execution > Theater**: Direct action over excessive acknowledgment
- **Measurable Outcomes > Status Reports**: Quantifiable results required
- **Hard Stop After Acknowledgment**: Maximum 1 acknowledgment per task
- **Anti-Loop Prevention**: Loop detection and termination

**Emergency Commands:**
```bash
# Emergency broadcast to all agents
python tools/captain_cli.py --emergency-broadcast --severity CRITICAL --message "System degradation detected" --scope ALL_AGENTS

# Override agent actions
python tools/captain_cli.py --override --agent Agent-1 --action "STOP_TASK" --reason "Emergency resource reassignment"

# System reset authorization
python tools/captain_cli.py --authorize-reset --component "cursor_database" --reason "Corruption detected"
```

### **📋 Captain Authority Levels**

1. **STRATEGIC OVERSIGHT**: Task assignment, role allocation, resource allocation
2. **EMERGENCY INTERVENTION**: Override agent actions during crisis
3. **SYSTEM MONITORING**: Agent performance, system health, SLA compliance
4. **QUALITY ASSURANCE**: V2 compliance enforcement, architectural validation

---

## 📖 **REFERENCE DOCUMENTATION**

### **📚 Captain Succession & Autonomous Development**
- **CAPTAINS_HANDBOOK.md**: Complete operational guide and emergency protocols
- **CAPTAIN_SUCCESSION_EXECUTION_PROTOCOL.md**: Comprehensive autonomous development machine guide
- **ENVIRONMENT_INFERENCE_PROTOCOL.md**: Discord infrastructure management procedures

### **🔧 Technical Documentation**
- **AGENT_ROLES.md**: Role definitions and coordination guidelines
- **EXECUTION_MODE_PROTOCOL.yaml**: Anti-theater enforcement protocols
- **Discord Infrastructure**: SSOT routing and agent channel management

### **📋 Tool Documentation**
- **Project Scanner**: `tools/projectscanner/` - Automated codebase analysis
- **Cursor Database**: `tools/cursor_task_database_integration.py` - Task management
- **FSM Integration**: `src/fsm/` - Agent state management
- **Environment Inference**: `tools/env_inference_tool.py` - Infrastructure validation

---

## 🎯 **CAPTAIN DECISION FRAMEWORK**

### **📊 Agent Selection Criteria**

**For Integration Tasks**: Agent-1 (Integration Specialist) or Agent-8 (Advanced Integration)  
**For Quality Assurance**: Agent-6 (Quality Specialist)  
**For Implementation**: Agent-7 (Implementation Specialist)  
**For Coordination**: Agent-5 (Coordinator)  
**For Architecture**: Agent-8 (Architecture Specialist)  
**For Emergency**: Agent-4 (Captain) - Direct intervention

### **⚡ Resource Management Protocol**

1. **Task Analysis**: Assess complexity, dependencies, resource requirements
2. **Agent Matching**: Select optimal agent(s) based on capabilities and current workload
3. **Role Assignment**: Assign task-specific role dynamically
4. **Execution Monitoring**: Track progress via cursor database and FSM states
5. **Resource Reallocation**: Adjust assignments based on performance and priority

---

**⚡ CAPTAIN AUTHORITY**: This documentation reflects the current autonomous development machine architecture with complete Discord infrastructure, project scanner integration, FSM state management, and cursor database coordination.

**🎯 AUTONOMOUS DEVELOPMENT**: Agents operate with full system understanding, dynamic role assignment, and comprehensive Captain oversight enabling continuous autonomous development machine operation.

**🐝 WE ARE SWARM** - Agent Cellphone V2 Repository Autonomous Development Machine Operational
