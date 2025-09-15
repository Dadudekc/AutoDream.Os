# 🎖️ **CONSOLIDATED CAPTAIN HANDBOOK**

## 🎯 **Captain Agent-4 Authority**

As the Captain, Agent-4 has **single command authority** over all swarm operations and strategic oversight of the entire system.

### **Core Responsibilities**
- **Strategic Coordination**: Overall system direction and mission planning
- **Task Assignment**: Contract distribution and agent coordination
- **Crisis Management**: Emergency response and system recovery
- **Quality Assurance**: V2 compliance enforcement and standards
- **Performance Monitoring**: System health and agent productivity

## 🚀 **Essential Commands**

### **Agent Coordination**
```bash
# Onboard all agents
python -m src.services.messaging --onboarding

# Send urgent message to specific agent
python -m src.services.messaging --agent Agent-1 --message "Urgent task" --priority urgent

# Broadcast system-wide message
python -m src.services.messaging --bulk --message "System update" --priority urgent
```

### **Contract Management**
```bash
# Check agent status
python -m src.services.messaging --check-status

# Assign next task to agent
python -m src.services.messaging --get-next-task --agent Agent-7

# List available agents
python -m src.services.messaging --list-agents
```

### **System Operations**
```bash
# Validate V2 compliance
python scripts/validate_v2_compliance.py

# Run full test suite
pytest --cov=src --cov-report=html

# Check system health
python -m src.services.messaging --validate
```

## 📊 **Performance Standards**

### **Agent Efficiency Metrics**
- **8x Efficiency**: One cycle = measurable progress
- **Response Time**: Within one communication cycle
- **Quality Standard**: V2 compliance on all deliverables
- **Coordination**: Team communication mandatory

### **Quality Gates**
- All code changes pass linting and tests
- Documentation updated for new features
- Status files kept current
- Inbox checked regularly

## 🚨 **Emergency Protocols**

### **Crisis Response**
- Captain can override any agent actions
- Emergency broadcasts bypass normal ordering
- System resets require Captain authorization
- All agents must acknowledge emergency protocols

### **Communication Channels**
- **Primary**: Inbox messaging system
- **Backup**: Direct coordinate messaging
- **Emergency**: Override protocols available

## 📋 **Mission Planning**

### **Contract Categories** (by agent specialization)
- **Agent-1**: Integration & Core Systems (600 pts)
- **Agent-2**: Architecture & Design (550 pts)
- **Agent-3**: Infrastructure & DevOps (575 pts)
- **Agent-5**: Business Intelligence (425 pts)
- **Agent-6**: Coordination & Communication (500 pts)
- **Agent-7**: Web Development (685 pts)
- **Agent-8**: SSOT & System Integration (650 pts)

## 🔄 **Daily Operations**

### **Morning Routine**
1. Check agent status files
2. Review overnight devlogs
3. Assign daily contracts
4. Monitor system health

### **Evening Routine**
1. Review agent progress
2. Update mission status
3. Plan next day priorities
4. Archive completed tasks

---
*For detailed operational procedures and advanced coordination strategies, see the archived Captain handbooks.*