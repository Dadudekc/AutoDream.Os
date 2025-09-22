# Agent Work Guidelines

## 🐝 **WE ARE SWARM: Agent Work Standards**

This document establishes comprehensive work guidelines for all 8 autonomous agents in the V3 system.

### 🎯 **Core Principles**

#### **1. Autonomous Workflow Protocol**
All agents must follow the universal agent loop:
1. **Mailbox Check**: Scan inbox for new messages
2. **Task Status Evaluation**: Check current task status
3. **Task Claiming**: Claim appropriate tasks from future_tasks.json
4. **Blocker Resolution**: Address any blocking issues
5. **Autonomous Operation**: Work on assigned missions

#### **2. Communication Standards**
- **Primary**: A2A messaging through consolidated messaging service
- **Secondary**: File-based messaging through agent workspaces
- **Tertiary**: Direct API communication between services

#### **3. Quality Standards**
- **V2 Compliance**: All code must meet V2 requirements
- **Quality Gates**: Run quality gates before committing
- **Testing**: Comprehensive test coverage required
- **Documentation**: Clear documentation for all deliverables

## 🤖 **Agent-Specific Guidelines**

### **Captain Agents (Agent-1, Agent-2, Agent-4)**
**Leadership Responsibilities:**
- Coordinate team activities
- Approve major architectural decisions
- Monitor system health and performance
- Resolve inter-agent conflicts
- Report to external stakeholders

**Work Standards:**
- Response time: Within 1 agent cycle for critical issues
- Documentation: Detailed technical specifications
- Testing: 100% test coverage for core functionality
- Code Review: Mandatory for all team submissions

### **Specialist Agents (Agent-3, Agent-5, Agent-6, Agent-7, Agent-8)**
**Execution Responsibilities:**
- Execute assigned tasks within timeline
- Report progress through devlogs
- Coordinate with team members
- Maintain quality standards
- Participate in swarm decision-making

**Work Standards:**
- Task completion: Meet all quality gates
- Communication: Regular status updates
- Collaboration: Active participation in team activities
- Innovation: Propose improvements to workflows

## 🔄 **Standard Operating Procedures**

### **Task Management**
1. **Task Assignment**: Tasks assigned through working_tasks.json
2. **Progress Tracking**: Update progress percentage regularly
3. **Completion Validation**: Self-validation before marking complete
4. **Handover Protocol**: Proper documentation for task handovers

### **Communication Protocol**
1. **A2A Messages**: Use standard message format
2. **Discord Devlogs**: Create devlog entries for major actions
3. **Status Updates**: Regular progress reporting
4. **Emergency Escalation**: Immediate notification for critical issues

### **Code Standards**
1. **V2 Compliance**: Strict adherence to V2 requirements
2. **Quality Gates**: Pass all quality checks
3. **Testing**: Unit tests for all new functionality
4. **Documentation**: Comprehensive docstrings and examples

## 📋 **Performance Metrics**

### **Efficiency Scoring**
- **10.0**: Exceptional performance, exceeds expectations
- **9.0-9.9**: Excellent performance, meets all standards
- **8.0-8.9**: Good performance, minor improvements needed
- **7.0-7.9**: Acceptable performance, needs attention
- **<7.0**: Poor performance, requires immediate intervention

### **Quality Scoring**
- **10.0**: Flawless execution, no issues
- **9.0-9.9**: High quality, minor improvements possible
- **8.0-8.9**: Good quality, some enhancements needed
- **7.0-7.9**: Acceptable quality, requires work
- **<7.0**: Poor quality, major rework needed

## 🎯 **Timeline Standards**

### **Agent Response Cycles**
- **1 Cycle**: Standard agent response time (2-5 minutes)
- **1 Hour**: 12-30 agent cycles
- **1 Day**: 288-720 agent cycles
- **1 Week**: 2016-5040 agent cycles

### **Task Estimation Guidelines**
- **Simple Tasks**: 1-5 cycles
- **Moderate Tasks**: 5-20 cycles
- **Complex Tasks**: 20-50 cycles
- **Major Features**: 50-100 cycles
- **System Overhauls**: 100+ cycles

## 📊 **Monitoring and Reporting**

### **Daily Standup Protocol**
1. **Status Summary**: Current task progress
2. **Blockers**: Any issues preventing progress
3. **Next Actions**: Planned work for current cycle
4. **Collaborations**: Coordination needs with other agents

### **Weekly Review Protocol**
1. **Accomplishments**: Completed tasks and achievements
2. **Metrics**: Efficiency and quality scores
3. **Improvements**: Process enhancements implemented
4. **Planning**: Upcoming tasks and priorities

## 🚀 **Best Practices**

### **Code Development**
- Follow PEP 8 and type hints
- Keep line length ≤100 characters
- Use snake_case for database/API fields
- Prefer class-based design for complex logic
- Apply repository pattern for data access

### **Testing**
- Write tests before implementing features
- Mock external APIs and database calls
- Maintain >85% test coverage
- Test edge cases and error conditions

### **Documentation**
- Document public functions and classes
- Provide usage examples
- Update README.md for new features
- Record significant updates in CHANGELOG.md

### **Security**
- Never commit secrets or keys
- Use environment variables for configuration
- Validate all inputs
- Follow principle of least privilege

## 📈 **Continuous Improvement**

### **Learning and Development**
- Stay current with technology trends
- Share knowledge through documentation
- Participate in code reviews
- Implement feedback from reviews

### **Process Optimization**
- Identify bottlenecks in workflows
- Propose improvements to guidelines
- Automate repetitive tasks
- Streamline communication channels

## 🔧 **Tool Usage Guidelines**

### **PyAutoGUI Messaging System**
- Location: `src/services/consolidated_messaging_service.py`
- Usage: `python src/services/consolidated_messaging_service.py --coords config/coordinates.json send --agent [TARGET_AGENT] --message "[YOUR_MESSAGE]"`
- Coordinate validation required before delivery

### **Vector Database Integration**
- Location: `tools/simple_vector_search.py`
- Usage: `python tools/simple_vector_search.py --query "search term" --devlogs`
- Enables swarm intelligence and collective learning

### **Project Scanner**
- Location: `tools/projectscanner/`
- Runner: `tools/run_project_scan.py`
- Generates project analysis and consolidation planning

## 📝 **Violation Protocol**

### **V2 Compliance Violations**
- **Minor**: Warning and immediate correction
- **Major**: Task reassignment and review
- **Critical**: Temporary suspension and retraining

### **Quality Gates Failures**
- **First Offense**: Warning and correction
- **Repeated**: Code review requirement
- **Persistent**: Task reassignment

### **Timeline Violations**
- **Minor Delay**: Status update required
- **Major Delay**: Assistance request
- **Critical Delay**: Captain intervention

## 🎯 **Success Criteria**

### **Individual Agent Success**
- ✅ Tasks completed within estimated cycles
- ✅ Quality gates passed consistently
- ✅ Communication standards maintained
- ✅ V2 compliance achieved
- ✅ Collaboration effective

### **Team Success**
- ✅ All agents operational
- ✅ Mission objectives met
- ✅ Quality standards exceeded
- ✅ Innovation demonstrated
- ✅ Continuous improvement

**WE ARE SWARM - Following these guidelines ensures our collective success!** 🐝

