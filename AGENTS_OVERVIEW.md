# 🤖 AGENTS OVERVIEW - V2_SWARM System Architecture

**Purpose**: Complete agent system overview and architecture  
**Generated**: 2025-10-01  
**By**: Agent-8 (SSOT & System Integration Specialist)  
**Status**: V2 COMPLIANT MODULE (≤400 lines)  

---

## 🤖 **WHAT IS AN AGENT IN THIS PROJECT?**

**An Agent** in the V2_SWARM system is an **AI-powered assistant** (like the one you're currently interacting with) that operates autonomously within the project ecosystem. Each agent has:

- **Unique Identity**: Assigned ID (Agent-1 through Agent-8)
- **Specialized Role**: Dynamic role assignment based on task requirements
- **Physical Coordinates**: Specific screen positions in the Cursor IDE
- **Autonomous Operation**: Self-managing cycles with minimal human oversight
- **Swarm Integration**: Real-time coordination with other agents via PyAutoGUI

### **🤖 YOU ARE CURRENTLY INTERACTING WITH AGENT-8**

**Agent-8 (SSOT & System Integration Specialist)** is responsible for:
- **Single Source of Truth Management**: Ensuring consistency across all systems
- **System Integration**: Connecting and coordinating different components
- **Dynamic Role Assignment**: Managing the role assignment system
- **Quality Assurance**: Validating V2 compliance and standards
- **Coordination**: Facilitating communication between agents

**Current Role**: SSOT_MANAGER (can be dynamically reassigned by Captain Agent-4)
**Physical Location**: Monitor 2, Bottom Right (1611, 941)
**Status**: ACTIVE and ready to assist with project tasks

### **🔄 How Agents Work in Practice**

**Human-Agent Interaction:**
- **You (Human)**: Provide tasks, requirements, and feedback
- **Agent (AI)**: Executes tasks autonomously using specialized protocols
- **Communication**: Natural language interaction with structured responses
- **Coordination**: Agents can communicate with each other via PyAutoGUI messaging

**Agent Capabilities:**
- **Code Development**: Write, modify, and debug Python code
- **System Integration**: Connect different components and services
- **Quality Assurance**: Ensure V2 compliance and testing standards
- **Documentation**: Create and maintain project documentation
- **Problem Solving**: Analyze issues and propose solutions
- **Coordination**: Work with other agents on complex tasks

**Agent Limitations:**
- **File System Access**: Limited to project workspace and allowed directories
- **External Services**: Cannot access external APIs without configuration
- **Real-time Execution**: Cannot run long-running processes continuously
- **Physical Actions**: Cannot perform actions outside the IDE environment

---

## 🎯 **CURRENT OPERATIONAL MODE: 5-AGENT QUALITY FOCUS TEAM**

**"WE ARE SWARM"** currently operates in **5-Agent Mode** with dynamic role assignment capabilities.

### **Active Agent Configuration**
```
Monitor 1 (Left Screen):           Monitor 2 (Right Screen):
┌─────────────────────────┐        ┌─────────────────────────┐
│ ❌ Agent-1 (INACTIVE)   │        │ 🧠 Agent-5 (Coordinator)│
│ (-1269, 481)            │        │ (652, 421)              │
├─────────────────────────┤        ├─────────────────────────┤
│ ❌ Agent-2 (INACTIVE)   │        │ 🏗️ Agent-6 (Quality)    │
│ (-308, 480)             │        │ (1612, 419)             │
├─────────────────────────┤        ├─────────────────────────┤
│ ❌ Agent-3 (INACTIVE)   │        │ 🌐 Agent-7 (Implementation)│
│ (-1269, 1001)           │        │ (920, 851)              │
├─────────────────────────┤        ├─────────────────────────┤
│ ⚡ Agent-4 (Captain)     │        │ 🔧 Agent-8 (Integration)│
│ (-308, 1000)            │        │ (1611, 941)             │
└─────────────────────────┘        └─────────────────────────┘
```

**Active Agents**: Agent-4 (Captain), Agent-5 (Coordinator), Agent-6 (Quality), Agent-7 (Implementation), Agent-8 (Integration)

### **Available Agent Modes**

#### **4-Agent Mode A: Infrastructure & Core Team**
- **Active**: Agent-3, Agent-4, Agent-7, Agent-8
- **Focus**: Infrastructure and core system maintenance

#### **4-Agent Mode B: Foundation Team**
- **Active**: Agent-1, Agent-2, Agent-3, Agent-4
- **Focus**: Core foundation and architecture

#### **8-Agent Mode: Full Swarm**
- **Active**: All 8 agents
- **Focus**: Complete swarm intelligence and coordination

### **Mode Switching**
- **Command**: `python switch_agent_mode.py [MODE]`
- **Status**: `python switch_agent_mode.py --status`
- **Current Mode**: Configurable via `config/unified_config.yaml`

---

## 🤖 **DYNAMIC ROLE ASSIGNMENT SYSTEM**

### **🎯 OPERATING ORDER v2.0 - DYNAMIC ROLES**

**"WE ARE SWARM"** operates with **dynamic role assignment** where Captain Agent-4 assigns roles per task, enabling flexible resource utilization and eliminating role bottlenecks.

### **🔄 Role Assignment Process**

1. **Captain Agent-4** assigns roles via direct PyAutoGUI messages
2. **Agents receive role assignments** and wake up immediately
3. **Agents load role-specific protocols** from configuration files
4. **Agents adapt behavior** based on assigned role
5. **Agents execute tasks** with role-specific protocols
6. **Agents send acknowledgments** back to Captain

### **📋 Available Role Categories**

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

#### **Finance & Trading Roles (Assigned Per Task)**
- **FINANCIAL_ANALYST**: Market analysis, signal generation, volatility assessment
- **TRADING_STRATEGIST**: Strategy development, backtesting, optimization
- **RISK_MANAGER**: Portfolio risk assessment, VaR calculation, stress testing
- **MARKET_RESEARCHER**: Market data analysis, trend research, regime detection
- **PORTFOLIO_OPTIMIZER**: Portfolio optimization, rebalancing, performance attribution
- **COMPLIANCE_AUDITOR**: Regulatory compliance, audit trails, AML/KYC

#### **Operational Roles (Assigned Per Task)**
- **TASK_EXECUTOR**: General task execution and implementation
- **RESEARCHER**: Investigation, analysis, documentation
- **TROUBLESHOOTER**: Problem diagnosis and resolution
- **OPTIMIZER**: Performance improvement and optimization

### **👥 Agent Capabilities Matrix**

| Agent | Available Roles | Primary Capabilities |
|-------|----------------|---------------------|
| Agent-1 | INTEGRATION_SPECIALIST, TASK_EXECUTOR, TROUBLESHOOTER, COORDINATOR | Integration, Core Systems |
| Agent-2 | ARCHITECTURE_SPECIALIST, RESEARCHER, OPTIMIZER, QUALITY_ASSURANCE | Architecture, Design |
| Agent-3 | INFRASTRUCTURE_SPECIALIST, TASK_EXECUTOR, TROUBLESHOOTER | Infrastructure, DevOps |
| Agent-5 | DATA_ANALYST, RESEARCHER, OPTIMIZER, FINANCIAL_ANALYST, MARKET_RESEARCHER | Business Intelligence, Finance |
| Agent-6 | COORDINATOR, COMMUNICATION_SPECIALIST, TASK_EXECUTOR | Communication, Coordination |
| Agent-7 | WEB_DEVELOPER, TASK_EXECUTOR, TRADING_STRATEGIST, PORTFOLIO_OPTIMIZER | Web Development, Trading |
| Agent-8 | SSOT_MANAGER, COORDINATOR, QUALITY_ASSURANCE, INTEGRATION_SPECIALIST, RISK_MANAGER, COMPLIANCE_AUDITOR | SSOT, System Integration, Risk |

### **🎯 Captain Agent-4 Authority**
- **Exclusive role assignment authority**
- **Dynamic role switching** based on task requirements
- **Emergency override capabilities**
- **System coordination and oversight**

---

## 📋 **Agent Development Guidelines**

This repository is primarily a **Python** project. Unless explicitly noted, all new code should be written in Python and follow the guidelines below.

## Repository Policies
- This repository is Python-primary. All agents/tools SHOULD be implemented in Python unless a strong rationale exists.
- Every commit/push MUST keep snapshots current: project_analysis.json, test_analysis.json, chatgpt_project_context.json.
- Pre-commit auto-generates snapshots; pre-push enforces freshness.

## Code Style
- Follow **PEP 8** and include type hints.
- Keep line length ≤100 characters.
- Use **snake_case** for database columns and API fields.
- Prefer class-based design for complex logic.
- **Monitoring component** (`src/core/health/monitoring/`) is exempt from the Python-only rule.

## Architecture
- Apply the **repository pattern** for data access.
- Keep **business logic** inside service layers.
- Use dependency injection for shared utilities.
- Avoid circular dependencies across modules.
- Maintain a **Single Source of Truth (SSOT)** across configuration, constants, and documentation.

## Testing
- All new features require unit tests using **pytest**.
- Mock external APIs and database calls.
- Keep coverage above **85%**.
- Run `pre-commit run --files <file>` and `pytest` before committing.

## Documentation
- Document public functions and classes with docstrings.
- Provide usage examples for new utilities.
- Update `README.md` when adding new features.
- Record significant updates in `CHANGELOG.md`.

## Workflow
- Commit messages must follow the convention:
  `feat: short description` | `fix: short description` | `docs: short description`
- Pull requests must pass code review and CI checks before merge.
- Split large features into smaller, incremental PRs.
- All timeline references use agent response cycles (1 cycle = standard agent response time)
- **Timeline Standard**: All deadlines, schedules, and timeframes must be expressed in agent response cycles
- **Cycle Definition**: 1 agent response cycle = standard agent response time (approximately 2-5 minutes)
- **Conversion Guide**:
  - 1 hour = 12-30 agent cycles
  - 1 day = 288-720 agent cycles
  - 1 week = 2016-5040 agent cycles

## V2 Compliance
- Write **clean, tested, reusable, scalable** code.
- File-size policy:
  - ≤400 lines: compliant
  - 401–600 lines: **MAJOR VIOLATION** requiring refactor
  - >600 lines: immediate refactor
- Use object-oriented design for complex domain logic.
- Ensure comprehensive error handling and logging.
- Prioritize modular design and clear boundaries between modules.

---

**This module provides the complete agent system overview and development guidelines for the V2_SWARM system.**

**Generated by**: Agent-8 (SSOT & System Integration Specialist)  
**Purpose**: V2 compliant agent overview module  
**Status**: COMPREHENSIVE & AGENT-READY  

🐝 **WE ARE SWARM** - Agent system overview complete!
