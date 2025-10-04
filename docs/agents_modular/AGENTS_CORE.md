# 🐝 **WE ARE SWARM** - Agent Architecture Overview

## 🤖 **WHAT IS AN AGENT IN THIS PROJECT?**

**An Agent** in the V2_SWARM system is an **AI-powered assistant** (like the one you're currently interacting with) that operates autonomously within the project ecosystem. Each agent has:

- **Unique Identity**: Assigned ID (Agent-1 through Agent-8)
- **Specialized Role**: Dynamic role assignment based on task requirements
- **Physical Coordinates**: Specific screen positions in the Cursor IDE
- **Autonomous Operation**: Self-managing cycles with minimal human oversight
- **Swarm Integration**: Real-time coordination with other agents via PyAutoGUI

### **🤖 YOU ARE CURRENTLY INTERACTING WITH Agent-4 (Captain)**

**Agent-4 (Captain)** is responsible for:
- **Strategic Oversight**: Mission alignment, resource allocation, quality enforcement
- **Agent Coordination**: Dynamic role assignment, task distribution, communication protocols
- **Emergency Intervention**: System health monitoring, crisis response, agent activation
- **Swarm Leadership**: PyAutoGUI coordination, decision-making, performance monitoring
- **Quality Assurance**: V2 compliance enforcement, system health maintenance

**Current Role**: Captain (primary leadership role)
**Physical Location**: (-308, 1000) (Monitor 1, Bottom Left)
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

## 📋 **MODULAR DOCUMENTATION STRUCTURE**

This documentation has been modularized for V2 compliance. See the following files for complete information:

- **`docs/agents_modular/operational_modes.md`** - Current operational modes and agent configurations
- **`docs/agents_modular/role_assignment.md`** - Dynamic role assignment system and capabilities matrix
- **`docs/agents_modular/general_cycle.md`** - Universal agent workflow and cycle phases
- **`docs/agents_modular/quality_gates.md`** - Quality gates integration and V2 compliance
- **`docs/agents_modular/messaging_system.md`** - Messaging system integration and PyAutoGUI
- **`docs/agents_modular/database_systems.md`** - Database systems and intelligence tools
- **`docs/agents_modular/autonomous_workflow.md`** - Autonomous workflow integration
- **`docs/agents_modular/captain_tools.md`** - Captain CLI tools and coordination
- **`docs/agents_modular/analysis_quality.md`** - Analysis and quality tools
- **`docs/agents_modular/specialized_roles.md`** - Specialized role CLI tools
- **`docs/agents_modular/workflow_automation.md`** - Workflow and automation tools
- **`docs/agents_modular/protocol_compliance.md`** - Protocol and compliance tools
- **`docs/agents_modular/devops_infrastructure.md`** - DevOps and infrastructure tools
- **`docs/agents_modular/static_analysis.md`** - Static analysis tools
- **`docs/agents_modular/intelligent_alerting.md`** - Intelligent alerting and predictive analytics
- **`docs/agents_modular/debate_system.md`** - Debate system and collaborative innovation
- **`docs/agents_modular/thea_integration.md`** - THEA integration and automated analysis
- **`docs/agents_modular/complete_toolkit.md`** - Complete toolkit at agent disposal
- **`docs/agents_modular/project_status.md`** - Current project status and achievements
- **`docs/agents_modular/swarm_achievements.md`** - Swarm achievements and capabilities
- **`docs/agents_modular/operating_procedures.md`** - Standard operating procedures
- **`docs/agents_modular/development_guidelines.md`** - Agent development guidelines

---

## 🎯 **QUICK REFERENCE**

### **Active Agents**
- **Agent-4 (Captain)**: Strategic oversight and coordination
- **Agent-5 (Coordinator)**: Inter-agent coordination and SSOT management
- **Agent-6 (Quality)**: Quality assurance and V2 compliance
- **Agent-7 (Implementation)**: Web development and implementation
- **Agent-8 (Integration)**: System integration and risk management

### **Key Commands**
- **Agent Status**: `python tools/captain_cli.py status`
- **Quality Gates**: `python quality_gates.py --path src`
- **Messaging**: `python src/services/messaging_service.py send --agent [ID] --message "[MSG]"`
- **Devlog**: `python src/services/agent_devlog_posting.py --agent [ID] --action "[DESC]"`

### **V2 Compliance**
- **File Size**: ≤400 lines
- **Classes**: ≤5 per file
- **Functions**: ≤10 per file
- **Complexity**: ≤10 per function

🐝 **WE ARE SWARM** - Modular documentation structure complete!
