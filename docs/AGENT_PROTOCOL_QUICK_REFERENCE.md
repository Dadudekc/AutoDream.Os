# Agent Protocol Quick Reference

## 🚀 Quick Start Commands

### Agent Status & Management
```bash
# Check all agent status
python tools/captain_cli.py status

# Check inactive agents
python tools/captain_cli.py inactive

# Send high-priority message
python tools/captain_cli.py high-priority --agent Agent-6 --message "URGENT: SSOT violation detected"
```

### Messaging & Communication
```bash
# Send A2A message
python src/services/consolidated_messaging_service.py send --agent Agent-4 --message "Task complete" --from-agent Agent-6

# Broadcast message to all agents
python src/services/consolidated_messaging_service.py broadcast --message "System update" --from-agent Agent-4

# Check messaging status
python src/services/consolidated_messaging_service.py status
```

### Quality Gates & Compliance
```bash
# Run quality gates
python quality_gates.py --path src

# Check V2 compliance violations
python tools/analysis_cli.py --violations --n 50

# Protocol compliance check
python tools/protocol_compliance_checker.py --category all --output console
```

### Role Assignment
```bash
# Assign role to agent
python src/services/role_assignment/role_assignment_service.py --assign-role --agent Agent-6 --role SSOT_MANAGER --task "V2 compliance enforcement" --duration "2 cycles"

# List available roles
python src/services/role_assignment/role_assignment_service.py --list-roles

# Check agent capabilities
python src/services/role_assignment/role_assignment_service.py --list-capabilities --agent Agent-6
```

## 📋 General Cycle Protocol

### Phase 1: CHECK_INBOX
- Scan agent inbox for messages
- Process role assignments from Captain
- Handle coordination messages
- Check system notifications
- Query Swarm Brain for patterns

### Phase 2: EVALUATE_TASKS
- Check for available tasks
- Claim tasks based on role capabilities
- Evaluate task requirements vs. current role
- Request role change if needed
- Prioritize tasks based on compliance violations

### Phase 3: EXECUTE_ROLE
- Execute tasks using current role protocols
- Apply role-specific behavior adaptations
- Follow role-specific quality gates
- Use role-specific escalation procedures
- Run project scanner analysis

### Phase 4: QUALITY_GATES
- Enforce V2 compliance
- Validate SSOT requirements
- Run role-specific quality checks
- Ensure all deliverables meet standards
- Run quality gates validation

### Phase 5: CYCLE_DONE
- Send CYCLE_DONE message to inbox
- Report cycle completion to Captain
- Prepare for next cycle
- Maintain role state or return to default
- Update agent workspace status

## 🎯 Role-Specific Quick Commands

### SSOT_MANAGER (Agent-6)
```bash
# SSOT validation
python src/core/ssot_manager.py

# Configuration management
python -c "from src.core.ssot_manager import get_ssot_manager; sm = get_ssot_manager(); print(sm.get_all_config())"

# Quality enforcement
python tools/analysis_cli.py --violations --refactor
```

### CAPTAIN (Agent-4)
```bash
# Captain operations
python tools/captain_cli.py report
python tools/captain_directive_manager.py status
python tools/agent_workflow_manager.py status
```

### COORDINATOR (Agent-5)
```bash
# Coordination tasks
python tools/swarm_coordination_tool.py status
python tools/agent_workflow_manager.py run --workflow workflow.json
```

## 🔧 V2 Compliance Standards

### File Limits
- **File Size**: ≤400 lines
- **Classes**: ≤5 per file
- **Functions**: ≤10 per file
- **Line Length**: ≤100 characters

### Quality Levels
- **Excellent**: 95-100 (no violations)
- **Good**: 75-94 (minor violations)
- **Acceptable**: 60-74 (some violations)
- **Poor**: 40-59 (multiple violations)
- **Critical**: <40 (major violations)

### Prohibited Patterns
- ❌ Abstract classes
- ❌ Complex inheritance
- ❌ Threading
- ❌ Files >400 lines
- ❌ Functions >50 lines

### Recommended Patterns
- ✅ Simple data classes
- ✅ Direct calls
- ✅ Basic validation
- ✅ Single responsibility
- ✅ KISS principle

## 📊 Database Quick Access

### Swarm Brain
```python
from swarm_brain import Retriever
r = Retriever()
results = r.search("agent coordination", k=10)
expertise = r.get_agent_expertise("Agent-6", k=20)
```

### Vector Database
```python
from src.services.vector_database import VectorDatabaseIntegration
vdb = VectorDatabaseIntegration()
similar = vdb.search_similar("integration challenges", k=5)
```

### Agent Workspaces
```python
import json
with open("agent_workspaces/Agent-6/status.json") as f:
    status = json.load(f)
```

## 🚨 Emergency Procedures

### SSOT Violations
1. **Detect**: Automatic detection of conflicting information
2. **Escalate**: Immediate notification to Captain Agent-4
3. **Resolve**: Coordinated resolution within 10 minutes
4. **Prevent**: Proactive monitoring and validation

### Configuration Conflicts
1. **Detect**: Automatic detection of inconsistencies
2. **Resolve**: Immediate resolution with SSOT Manager
3. **Escalate**: If resolution exceeds 10 minutes
4. **Prevent**: Centralized configuration management

### Quality Violations
1. **Detect**: Automated quality gates checking
2. **Report**: Generate violation reports
3. **Fix**: Coordinate refactoring efforts
4. **Validate**: Ensure compliance before proceeding

## 📱 A2A Message Template

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

## 🔍 Troubleshooting

### Common Issues
- **Import Errors**: Check Python path and dependencies
- **Message Failures**: Verify messaging service status
- **Quality Violations**: Run quality gates and fix violations
- **Role Conflicts**: Check role assignment status
- **Configuration Issues**: Validate SSOT configuration

### Debug Commands
```bash
# Check system status
python src/services/consolidated_messaging_service.py status
python tools/protocol_compliance_checker.py --category all --output console

# Debug agent workspace
ls agent_workspaces/Agent-6/
cat agent_workspaces/Agent-6/status.json

# Check quality status
python tools/analysis_cli.py --violations --n 10
```

## 📚 Additional Resources

- **Full Documentation**: `docs/AGENT_PROTOCOL_SYSTEM.md`
- **Configuration**: `config/unified_config.json`
- **Quality Standards**: `quality_gates.py`
- **Agent Workspaces**: `agent_workspaces/`
- **Swarm Brain**: `swarm_brain/`

---
**🐝 WE ARE SWARM - Agent Protocol Quick Reference**
