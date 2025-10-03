### **🎯 Captain Agent-4 Authority**
- **Exclusive role assignment authority**
- **Dynamic role switching** based on task requirements
- **Emergency override capabilities**
- **System coordination and oversight**

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
🗃️ Query Swarm Brain for task success patterns
📊 Analyze agent workspace task history for optimization
🧠 Use vector similarity to find related successful tasks
📋 Check devlog database for task completion patterns
📋 Review scanner-identified consolidation opportunities
🎯 Prioritize tasks based on compliance violations
⚖️ Evaluate impact of proposed changes on project health
🤖 Use TaskManager to evaluate current task status (no_current_task, task_in_progress, task_blocked)
📋 Check future_tasks.json for available tasks to claim
🎯 Select highest priority task based on role capabilities
📊 Update working_tasks.json with claimed task information

Role Adaptations:
- INTEGRATION_SPECIALIST: Focus on integration_tasks, api_development, webhook_setup
- QUALITY_ASSURANCE: Focus on testing_tasks, quality_reviews, compliance_checks
- SSOT_MANAGER: Focus on ssot_validation, system_integration, coordination_tasks
- FINANCIAL_ANALYST: Focus on market_analysis_tasks, signal_generation, volatility_assessment
- TRADING_STRATEGIST: Focus on strategy_development, backtesting, optimization_tasks
- RISK_MANAGER: Focus on risk_assessment, portfolio_monitoring, stress_testing
```

### **PHASE 3: EXECUTE_ROLE (Priority: HIGH)**
```
⚡ Execute tasks using current role protocols
🎭 Apply role-specific behavior adaptations
📋 Follow role-specific quality gates
🚨 Use role-specific escalation procedures
🔍 Run project scanner analysis (V2 compliance, file analysis, dependency tracking)
🤖 Consult THEA for analysis/quality control (automated)
🗳️ Participate in debate system (new protocols, tools, goals)
💾 Update vector database with results
🧠 Query Swarm Brain database for patterns and insights
📊 Update agent workspace databases with cycle data
🗃️ Query Swarm Brain for role-specific insights and patterns
📊 Update agent workspace with current task progress
🧠 Store vector embeddings of current work for future reference
📋 Create devlog entries with full context and metadata
🤖 Execute autonomous operations when no urgent tasks pending
🔄 Continue current task if task_in_progress
🚨 Resolve blockers using BlockerResolver if task_blocked
📋 Run autonomous operations using AutonomousOperations if no_current_task
🎯 Update task status and progress in working_tasks.json

Role Adaptations:
- INTEGRATION_SPECIALIST: Focus on system_integration, api_development, webhook_management, dependency_analysis
- QUALITY_ASSURANCE: Focus on test_development, quality_validation, compliance_checking, v2_violation_detection
- SSOT_MANAGER: Focus on ssot_management, system_coordination, configuration_validation, project_health_monitoring
- FINANCIAL_ANALYST: Focus on market_analysis, technical_indicators, fundamental_analysis, signal_generation
- TRADING_STRATEGIST: Focus on strategy_development, backtesting_analysis, performance_optimization, risk_metrics
- RISK_MANAGER: Focus on portfolio_risk, var_calculation, stress_testing, position_monitoring
```

### **PHASE 4: QUALITY_GATES (Priority: HIGH)**
```
✅ Enforce V2 compliance
🔍 Validate SSOT requirements
🧪 Run role-specific quality checks
📊 Ensure all deliverables meet standards
🚨 Run quality gates validation (python quality_gates.py)
📊 Analyze quality metrics and violations
🔧 Fix critical violations (file size >400 lines, complexity >10)
🤖 Automated THEA quality control review
📝 Create Discord devlog entry (automatic posting to Discord)
📱 Social media integration (if applicable)
🧠 Vector database indexing and searchability
🗃️ Swarm Brain database updates (181+ documents)
📁 Agent workspace database synchronization
🗃️ Store quality validation results in Swarm Brain
📊 Update agent workspace status with quality metrics
🧠 Index quality results in vector database for similarity search
📋 Document quality gates in devlog database

Role Adaptations:
- INTEGRATION_SPECIALIST: Focus on integration_testing, api_validation, webhook_testing
- QUALITY_ASSURANCE: Focus on comprehensive_testing, compliance_validation, performance_testing
- SSOT_MANAGER: Focus on ssot_compliance, configuration_consistency, system_integration
- FINANCIAL_ANALYST: Focus on analysis_accuracy, signal_validation, model_performance
- TRADING_STRATEGIST: Focus on strategy_performance, backtesting_accuracy, risk_metrics
- RISK_MANAGER: Focus on risk_validation, stress_test_accuracy, compliance_monitoring
```

### **PHASE 5: CYCLE_DONE (Priority: CRITICAL)**
```
📤 Send CYCLE_DONE message to inbox
📊 Report cycle completion to Captain
🔄 Prepare for next cycle
💾 Maintain role state or return to default
📋 Update agent workspace status
🗳️ Submit debate contributions (if any)
📈 Update project analysis and ChatGPT context
🗃️ Sync Swarm Brain database with cycle results
📊 Update agent workspace status and task tracking
🗃️ Store cycle results in Swarm Brain for future reference
📊 Update agent workspace with cycle completion data
🧠 Index cycle results in vector database
📋 Archive cycle summary in devlog database
🤖 Create autonomous cycle completion devlog
📊 Update workflow status and cycle results
🔄 Prepare autonomous workflow for next cycle
📋 Archive processed messages and completed tasks

Role Adaptations:
- INTEGRATION_SPECIALIST: Focus on integration_status, service_health, next_integration_steps
- QUALITY_ASSURANCE: Focus on quality_status, test_results, compliance_status
- SSOT_MANAGER: Focus on ssot_status, system_coordination, configuration_health
- FINANCIAL_ANALYST: Focus on market_status, signal_quality, analysis_performance
- TRADING_STRATEGIST: Focus on strategy_status, performance_metrics, next_optimization
- RISK_MANAGER: Focus on risk_status, portfolio_health, compliance_status
```

---

## 🚨 **QUALITY GATES INTEGRATION IN GENERAL CYCLE**

### **🎯 Quality Gates System Overview**
The V2_SWARM system includes a comprehensive quality gates system that ensures code quality, V2 compliance, and prevents overengineering:

**Current Quality Status:**
- **Total Files Checked**: 772 Python files
- **V2 Compliant Files**: 691 files (89.5% compliance)
- **Critical Violations**: 81 files requiring attention
- **File Size Violations**: 6 files over 400 lines (critical)
- **Quality Levels**: Excellent (95+), Good (75+), Acceptable (60+), Poor (40+), Critical (<40)

### **🔧 Quality Gates Integration Points**

#### **PHASE 1: CHECK_INBOX**
- **Quality Status Check**: Review quality metrics from previous cycles
- **Violation Alerts**: Check for new quality violations
- **Compliance Status**: Monitor V2 compliance trends

#### **PHASE 2: EVALUATE_TASKS**
- **Quality Impact Assessment**: Evaluate task impact on code quality
- **Violation Prevention**: Prioritize tasks that fix critical violations
- **Compliance Planning**: Plan work to maintain V2 compliance

#### **PHASE 3: EXECUTE_ROLE**
- **Real-time Quality Monitoring**: Run quality checks during development
- **V2 Compliance Enforcement**: Ensure all code meets V2 standards
- **Quality Metrics Collection**: Gather quality data for analysis

#### **PHASE 4: QUALITY_GATES**
- **🚨 Quality Gates Execution**: Run `python quality_gates.py --path src`
- **📊 Quality Analysis**: Analyze quality metrics and violations
- **🔧 Violation Fixing**: Address critical violations (file size >400 lines, complexity >10)
- **📈 Quality Reporting**: Generate quality reports and recommendations

#### **PHASE 5: CYCLE_DONE**
- **Quality Validation**: Final quality check before cycle completion
- **Quality Metrics Storage**: Store quality results in databases
- **Quality Trends**: Update quality trend analysis

### **🎯 Role-Specific Quality Gates Usage**

#### **INTEGRATION_SPECIALIST**
- **Focus Areas**: Integration testing, API validation, webhook testing
- **Quality Checks**: System integration quality, API compliance
- **Violations**: Focus on integration-related quality issues

#### **QUALITY_ASSURANCE**
- **Focus Areas**: Comprehensive testing, compliance validation, performance testing
- **Quality Checks**: Full quality gates execution, test coverage analysis
- **Violations**: Address all quality violations systematically

#### **SSOT_MANAGER**
- **Focus Areas**: SSOT compliance, configuration consistency, system integration
- **Quality Checks**: Configuration quality, system consistency
- **Violations**: Ensure SSOT compliance and consistency

### **📊 Quality Gates Commands & Tools**

#### **Core Quality Gates Commands**
```bash
# Run quality gates on entire project
python quality_gates.py

# Run quality gates on specific directory
python quality_gates.py --path src

# Generate quality report to file
python quality_gates.py --path src --output quality_report.txt

# Check specific file quality
python quality_gates.py --path src/services/autonomous/core/autonomous_workflow.py
```

#### **Quality Gates Metrics**
- **File Size**: ≤400 lines (hard limit)
- **Enums**: ≤3 per file
- **Classes**: ≤5 per file
- **Functions**: ≤10 per file
- **Complexity**: ≤10 cyclomatic complexity per function
- **Parameters**: ≤5 per function
- **Inheritance**: ≤2 levels deep

#### **Quality Levels & Scoring**
- **Excellent (95-100)**: No violations, perfect compliance
- **Good (75-94)**: Minor violations, acceptable quality
- **Acceptable (60-74)**: Some violations, needs improvement
- **Poor (40-59)**: Multiple violations, significant issues
- **Critical (<40)**: Major violations, requires immediate attention

### **📈 Quality Gates Data Flow**
1. **Pre-Cycle**: Agents check quality status and violation alerts
2. **During Cycle**: Real-time quality monitoring and V2 compliance enforcement
3. **Post-Cycle**: Quality gates execution, violation analysis, and fixing
4. **Continuous**: Quality metrics storage and trend analysis

---

## 📱 **MESSAGING SYSTEM INTEGRATION IN GENERAL CYCLE**

### **🎯 Messaging System Overview**
The V2_SWARM messaging system provides comprehensive agent-to-agent communication through PyAutoGUI automation:

**Current Messaging Status:**
- **Service Status**: Active
- **Agents Configured**: 8 agents
- **Active Agents**: 8 agents
- **Coordination Requests**: 0 (all protocols compliant)
- **Auto Devlog**: Enabled
- **Response Protocol**: Enabled

### **🔧 Messaging System Integration Points**

#### **PHASE 1: CHECK_INBOX**
- **📱 Messaging Status Check**: Verify messaging system health
- **🔔 PyAutoGUI Processing**: Handle incoming PyAutoGUI messages
- **📋 Protocol Compliance**: Check response protocol violations
- **🗳️ Coordination Requests**: Process coordination messages

#### **PHASE 2: EVALUATE_TASKS**
- **📤 Message Preparation**: Prepare outgoing messages for coordination
- **🎯 Target Agent Selection**: Choose appropriate agents for task coordination
- **⚡ Priority Assessment**: Determine message priority levels
- **📋 Response Planning**: Plan response strategies for incoming messages

#### **PHASE 3: EXECUTE_ROLE**
- **📱 Active Messaging**: Send PyAutoGUI messages during task execution
- **🔄 Real-time Coordination**: Coordinate with other agents via messaging
- **📊 Status Updates**: Send status updates to relevant agents
- **🗳️ Task Coordination**: Coordinate multi-agent tasks via messaging

#### **PHASE 4: QUALITY_GATES**
- **📋 Message Validation**: Validate outgoing messages for quality
- **🔔 Protocol Compliance**: Ensure messaging protocol compliance
- **📊 Communication Metrics**: Track messaging effectiveness
- **🗃️ Message Logging**: Log all messaging activities

#### **PHASE 5: CYCLE_DONE**