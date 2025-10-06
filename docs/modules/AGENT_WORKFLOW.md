# 🔄 Agent Workflow System
# ========================

**Purpose**: Universal agent workflow and cycle definitions
**Generated**: 2025-10-02
**By**: Agent-7 (Implementation Specialist)
**Status**: V2 COMPLIANT MODULE (≤400 lines)

---

## 🔄 **GENERAL CYCLE (Universal Agent Workflow)**

**1 CYCLE = 1 AGENT RESPONSE** (approximately 2-5 minutes)

**The General Cycle** is the standard autonomous operation loop that all agents follow, regardless of their assigned role. It's the universal workflow that ensures consistent behavior across the swarm.

### **PHASE 1: CHECK_INBOX (Priority: CRITICAL)**
```
📬 Scan agent inbox for messages
🔍 Process role assignments from Captain
📝 Handle coordination messages from other agents
🔔 Process system notifications
🗳️ Check for debate participation requests
📋 Review agent workspace status updates
🗃️ Query Swarm Brain for relevant patterns and previous experiences
📊 Check agent workspace status and task history
🧠 Search vector database for similar past actions
📋 Review devlog database for recent agent activities
🔍 Scan project_analysis.json for recent changes
📊 Check V2 compliance violations since last cycle
🚨 Identify critical issues requiring immediate attention
📱 Check messaging system status and protocol compliance
🔔 Process PyAutoGUI messages and coordinate responses
🤖 Initialize autonomous workflow components (MailboxManager, TaskManager, BlockerResolver)
📋 Evaluate current task status and pending messages
🔄 Check for autonomous operations availability

Role Adaptations:
- INTEGRATION_SPECIALIST: Focus on integration_requests, service_notifications
- QUALITY_ASSURANCE: Focus on quality_requests, test_notifications, compliance_alerts
- SSOT_MANAGER: Focus on ssot_violations, configuration_changes, coordination_requests
- FINANCIAL_ANALYST: Focus on market_data, trading_signals, volatility_alerts
- TRADING_STRATEGIST: Focus on strategy_updates, performance_alerts, backtesting_results
- RISK_MANAGER: Focus on risk_alerts, position_updates, compliance_violations
```

### **PHASE 2: EVALUATE_TASKS (Priority: HIGH)**
```
📋 Check for available tasks
🎯 Claim tasks based on current role capabilities
⚖️ Evaluate task requirements vs. current role
🔄 Request role change if needed
📊 Assess task complexity and resource requirements
⏰ Estimate completion time based on role capabilities
🔄 Check for task dependencies and prerequisites
📋 Review task history and similar past executions
🧠 Query vector database for task patterns and solutions
📊 Evaluate current workload and capacity
🚨 Identify urgent tasks requiring immediate attention
📱 Check messaging system for task assignments
🔔 Process PyAutoGUI task coordination messages
🤖 Initialize task management components
📋 Evaluate task priority and scheduling
🔄 Check for autonomous task execution availability

Role Adaptations:
- INTEGRATION_SPECIALIST: Focus on integration_tasks, service_connections
- QUALITY_ASSURANCE: Focus on testing_tasks, compliance_checks, validation_requests
- SSOT_MANAGER: Focus on ssot_tasks, configuration_updates, coordination_tasks
- FINANCIAL_ANALYST: Focus on analysis_tasks, market_research, signal_generation
- TRADING_STRATEGIST: Focus on strategy_tasks, backtesting, optimization_requests
- RISK_MANAGER: Focus on risk_tasks, portfolio_analysis, compliance_monitoring
```

### **PHASE 3: EXECUTE_TASKS (Priority: HIGH)**
```
🎯 Execute assigned tasks with role-specific protocols
📊 Monitor task progress and performance metrics
🔄 Adapt execution strategy based on real-time feedback
📋 Document task execution and decision points
🧠 Update vector database with new patterns and solutions
📊 Record performance metrics and completion statistics
🚨 Handle task errors and implement recovery procedures
📱 Coordinate with other agents via messaging system
🔔 Process PyAutoGUI coordination messages during execution
🤖 Utilize autonomous workflow components for task execution
📋 Maintain task logs and audit trails
🔄 Check for task completion and handoff requirements

Role Adaptations:
- INTEGRATION_SPECIALIST: Focus on system_connections, service_integration
- QUALITY_ASSURANCE: Focus on test_execution, compliance_validation, quality_checks
- SSOT_MANAGER: Focus on ssot_maintenance, configuration_management, coordination
- FINANCIAL_ANALYST: Focus on data_analysis, market_research, signal_processing
- TRADING_STRATEGIST: Focus on strategy_implementation, backtesting, optimization
- RISK_MANAGER: Focus on risk_assessment, portfolio_monitoring, compliance_tracking
```

### **PHASE 4: COORDINATE_SWARM (Priority: MEDIUM)**
```
🤝 Coordinate with other agents on shared tasks
📊 Share progress updates and status information
🔄 Exchange knowledge and patterns via vector database
📋 Participate in swarm decision-making processes
🧠 Contribute to collective intelligence and learning
📊 Update swarm metrics and performance indicators
🚨 Report critical issues and coordinate emergency responses
📱 Maintain active communication via messaging system
🔔 Process PyAutoGUI swarm coordination messages
🤖 Utilize autonomous coordination components
📋 Participate in swarm meetings and planning sessions
🔄 Check for swarm-wide initiatives and collaborative tasks

Role Adaptations:
- INTEGRATION_SPECIALIST: Focus on integration_coordination, service_synchronization
- QUALITY_ASSURANCE: Focus on quality_coordination, compliance_synchronization
- SSOT_MANAGER: Focus on ssot_coordination, configuration_synchronization
- FINANCIAL_ANALYST: Focus on market_coordination, analysis_synchronization
- TRADING_STRATEGIST: Focus on strategy_coordination, backtesting_synchronization
- RISK_MANAGER: Focus on risk_coordination, portfolio_synchronization
```

### **PHASE 5: UPDATE_STATUS (Priority: MEDIUM)**
```
📊 Update agent status and performance metrics
📋 Document completed tasks and achievements
🧠 Update vector database with new knowledge and patterns
📊 Record cycle statistics and performance indicators
🚨 Report system health and critical issues
📱 Update messaging system status and availability
🔔 Process PyAutoGUI status update messages
🤖 Update autonomous workflow component status
📋 Maintain agent workspace and task history
🔄 Check for status synchronization with swarm
📊 Prepare for next cycle and role evaluation

Role Adaptations:
- INTEGRATION_SPECIALIST: Focus on integration_status, service_health
- QUALITY_ASSURANCE: Focus on quality_status, compliance_health
- SSOT_MANAGER: Focus on ssot_status, configuration_health
- FINANCIAL_ANALYST: Focus on market_status, analysis_health
- TRADING_STRATEGIST: Focus on strategy_status, backtesting_health
- RISK_MANAGER: Focus on risk_status, portfolio_health
```

---

## 🎯 **CYCLE TIMING AND PERFORMANCE**

### **Cycle Duration Guidelines**
- **Standard Cycle**: 2-5 minutes per phase
- **Total Cycle Time**: 10-25 minutes
- **Emergency Cycle**: 1-2 minutes (critical tasks only)
- **Extended Cycle**: 30-60 minutes (complex tasks)

### **Performance Metrics**
- **Cycle Completion Rate**: Target 95%+
- **Task Success Rate**: Target 90%+
- **Coordination Efficiency**: Target 85%+
- **Status Update Frequency**: Every cycle
- **Error Recovery Time**: <5 minutes

### **Cycle Optimization**
- **Parallel Processing**: Execute multiple phases simultaneously when possible
- **Priority Queuing**: Process high-priority tasks first
- **Resource Management**: Optimize resource allocation per cycle
- **Learning Integration**: Continuously improve cycle efficiency
- **Adaptive Timing**: Adjust cycle duration based on task complexity

---

## 🔄 **AUTONOMOUS WORKFLOW COMPONENTS**

### **MailboxManager**
- **Purpose**: Manage agent inbox and message processing
- **Features**: Message prioritization, role-based filtering, automatic routing
- **Integration**: PyAutoGUI messaging system, Discord notifications

### **TaskManager**
- **Purpose**: Manage task lifecycle and execution
- **Features**: Task queuing, dependency management, progress tracking
- **Integration**: Vector database, swarm coordination

### **BlockerResolver**
- **Purpose**: Identify and resolve task blockers
- **Features**: Automatic problem detection, solution generation, escalation
- **Integration**: Swarm coordination, emergency protocols

---

🐝 **WE ARE SWARM** - Universal workflow for autonomous operation

