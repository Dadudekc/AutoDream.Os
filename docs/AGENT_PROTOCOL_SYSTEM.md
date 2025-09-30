# Agent Protocol System Documentation

## Overview

The Agent Protocol System defines the standardized operating procedures, communication protocols, and quality standards for the V2_SWARM multi-agent system. This system ensures consistent behavior, reliable communication, and maintainable code across all agents.

## Core Principles

### 1. Single Source of Truth (SSOT)
- All configuration and data must have a single authoritative source
- No duplicate or conflicting information across the system
- Centralized configuration management through SSOT Manager

### 2. V2 Compliance Standards
- **File Size**: ≤400 lines per file
- **Class Limit**: ≤5 classes per file
- **Function Limit**: ≤10 functions per file
- **Line Length**: ≤100 characters per line
- **No Abstract Classes**: Avoid complex inheritance patterns
- **No Threading**: Use direct calls instead of threading

### 3. General Cycle Protocol
All agents follow a standardized 5-phase cycle:

1. **CHECK_INBOX**: Process messages and role assignments
2. **EVALUATE_TASKS**: Assess available tasks and priorities
3. **EXECUTE_ROLE**: Execute tasks using role-specific protocols
4. **QUALITY_GATES**: Validate V2 compliance and quality standards
5. **CYCLE_DONE**: Report completion and prepare for next cycle

## Agent Roles and Capabilities

### Core Roles
- **CAPTAIN**: Strategic oversight, emergency intervention, role assignment
- **SSOT_MANAGER**: Single source of truth validation and management
- **COORDINATOR**: Inter-agent coordination and communication

### Technical Roles
- **INTEGRATION_SPECIALIST**: System integration and interoperability
- **ARCHITECTURE_SPECIALIST**: System design and architectural decisions
- **INFRASTRUCTURE_SPECIALIST**: DevOps, deployment, monitoring
- **WEB_DEVELOPER**: Frontend/backend web development
- **DATA_ANALYST**: Data processing, analysis, reporting
- **QUALITY_ASSURANCE**: Testing, validation, compliance

### Finance & Trading Roles
- **FINANCIAL_ANALYST**: Market analysis, signal generation, volatility assessment
- **TRADING_STRATEGIST**: Strategy development, backtesting, optimization
- **RISK_MANAGER**: Portfolio risk assessment, VaR calculation, stress testing
- **MARKET_RESEARCHER**: Market data analysis, trend research, regime detection
- **PORTFOLIO_OPTIMIZER**: Portfolio optimization, rebalancing, performance attribution
- **COMPLIANCE_AUDITOR**: Regulatory compliance, audit trails, AML/KYC

### Operational Roles
- **TASK_EXECUTOR**: General task execution and implementation
- **RESEARCHER**: Investigation, analysis, documentation
- **TROUBLESHOOTER**: Problem diagnosis and resolution
- **OPTIMIZER**: Performance improvement and optimization

## Communication Protocols

### A2A Message Format
```
============================================================
[A2A] MESSAGE - CYCLE {CYCLE_NUMBER}
============================================================
📤 FROM: {AGENT_ID}
📥 TO: {TARGET_AGENT}
Priority: {NORMAL|HIGH|URGENT}
Tags: {GENERAL|COORDINATION|TASK|STATUS|VALIDATION}
------------------------------------------------------------
{CONTENT}
📝 DEVLOG: Auto-created in local storage
🧠 VECTOR: Auto-indexed in searchable database
📊 METRICS: Updated in project analysis
------------------------------------------------------------
🐝 WE ARE SWARM - Cycle {CYCLE_NUMBER} Complete
============================================================
```

### Quality Gates Integration
- **Pre-Cycle**: Check quality status and violation alerts
- **During Cycle**: Real-time quality monitoring and V2 compliance enforcement
- **Post-Cycle**: Quality gates execution, violation analysis, and fixing
- **Continuous**: Quality metrics storage and trend analysis

## Quality Standards

### V2 Compliance Requirements
- **File Size**: ≤400 lines (hard limit)
- **Enums**: ≤3 per file
- **Classes**: ≤5 per file
- **Functions**: ≤10 per file
- **Complexity**: ≤10 cyclomatic complexity per function
- **Parameters**: ≤5 per function
- **Inheritance**: ≤2 levels deep

### Quality Levels & Scoring
- **Excellent (95-100)**: No violations, perfect compliance
- **Good (75-94)**: Minor violations, acceptable quality
- **Acceptable (60-74)**: Some violations, needs improvement
- **Poor (40-59)**: Multiple violations, significant issues
- **Critical (<40)**: Major violations, requires immediate attention

## Database Systems

### Swarm Brain Database
- **Purpose**: Centralized knowledge storage and retrieval
- **Content**: 181+ documents with semantic search capabilities
- **Usage**: Pattern recognition, experience sharing, decision support

### Vector Database
- **Purpose**: Semantic search and similarity matching
- **Content**: 100+ devlog vectors with similarity matching
- **Usage**: Finding related experiences and solutions

### Agent Workspaces
- **Purpose**: Individual agent data and task management
- **Structure**: inbox, processed, working_tasks.json, future_tasks.json
- **Usage**: Task tracking, message processing, status management

## Autonomous Workflow System

### Components
- **MailboxManager**: Handles inbox scanning and message processing
- **TaskManager**: Manages task status evaluation and task claiming
- **BlockerResolver**: Resolves blockers and escalates when necessary
- **AutonomousOperations**: Executes autonomous operations when no urgent tasks

### Workflow Operations
- **Continuous Cycles**: 5-minute interval autonomous cycles
- **Task Lifecycle**: Complete task claiming, execution, and completion tracking
- **Message Processing**: Automated inbox scanning and message handling
- **Blocking Resolution**: Automatic blocker detection and escalation

## Messaging System

### PyAutoGUI Integration
- **Purpose**: Real-time agent-to-agent communication
- **Method**: Coordinate-based mouse/keyboard automation
- **Features**: Instant messaging, status updates, coordination requests

### Protocol Standards
- **Message Format**: Standardized A2A message format with headers
- **Priority Levels**: NORMAL, HIGH, URGENT priority support
- **Response Tracking**: Automatic tracking of message acknowledgments
- **Protocol Violations**: Detection of overdue, unacknowledged, or incomplete responses

## Tools and Services

### Core Communication Systems
- **Consolidated Messaging Service**: Primary messaging service
- **Captain CLI Tools**: Agent management and coordination
- **Role Assignment Service**: Dynamic role assignment and management

### Analysis and Quality Tools
- **Analysis CLI**: V2 compliance analysis with violations detection
- **Overengineering Detector**: Pattern-based detection of complexity issues
- **Protocol Compliance Checker**: Agent Protocol System standards verification
- **Quality Gates**: Comprehensive code analysis and compliance checking

### Specialized Role Tools
- **Financial Analyst CLI**: Market analysis and signal generation
- **Trading Strategist CLI**: Strategy development and backtesting
- **Risk Manager CLI**: Portfolio risk assessment and stress testing
- **Compliance Auditor CLI**: Regulatory compliance and audit trails

## Best Practices

### Code Development
- Follow PEP 8 and include type hints
- Keep line length ≤100 characters
- Use snake_case for database columns and API fields
- Prefer class-based design for complex logic
- Apply repository pattern for data access
- Keep business logic inside service layers
- Use dependency injection for shared utilities
- Avoid circular dependencies across modules

### Testing
- All new features require unit tests using pytest
- Mock external APIs and database calls
- Keep coverage above 85%
- Run pre-commit hooks and pytest before committing

### Documentation
- Document public functions and classes with docstrings
- Provide usage examples for new utilities
- Update README.md when adding new features
- Record significant updates in CHANGELOG.md

### Workflow
- Commit messages must follow convention: `feat:`, `fix:`, `docs:`
- Pull requests must pass code review and CI checks before merge
- Split large features into smaller, incremental PRs
- All timeline references use agent response cycles (1 cycle = 2-5 minutes)

## Compliance and Monitoring

### Protocol Compliance
- **Git Workflow**: Standardized branching and merging procedures
- **Code Quality**: V2 compliance enforcement and validation
- **Documentation**: Required documentation standards and templates
- **Agent Coordination**: Status tracking and communication protocols
- **Testing**: Comprehensive testing requirements and coverage

### Monitoring Systems
- **Performance Monitoring**: Real-time performance metrics and alerting
- **Quality Monitoring**: Continuous V2 compliance checking
- **Compliance Monitoring**: Protocol adherence and violation detection
- **System Health**: Overall system status and health monitoring

## Emergency Procedures

### SSOT Violations
- **Detection**: Immediate identification of conflicting information
- **Escalation**: Automatic notification to Captain Agent-4
- **Resolution**: Coordinated resolution within 10 minutes
- **Prevention**: Proactive monitoring and validation

### Configuration Conflicts
- **Detection**: Automatic detection of configuration inconsistencies
- **Resolution**: Immediate resolution with SSOT Manager
- **Escalation**: Escalate if resolution exceeds 10 minutes
- **Prevention**: Centralized configuration management

### Data Inconsistency
- **Detection**: Automated data validation and consistency checks
- **Notification**: Immediate notification to affected systems
- **Resolution**: Coordinated data synchronization
- **Escalation**: Escalate if critical data inconsistency detected

### Integration Failures
- **Detection**: Real-time integration monitoring and health checks
- **Coordination**: Immediate coordination with relevant agents
- **Resolution**: Coordinated troubleshooting and resolution
- **Escalation**: Escalate if resolution exceeds 20 minutes

## Conclusion

The Agent Protocol System provides a comprehensive framework for operating the V2_SWARM multi-agent system. By following these protocols, agents ensure consistent behavior, reliable communication, and maintainable code while achieving the highest standards of quality and compliance.

For questions or clarifications about these protocols, contact the SSOT_MANAGER (Agent-6) or Captain Agent-4.

---
**🐝 WE ARE SWARM - Agent Protocol System Documentation**
