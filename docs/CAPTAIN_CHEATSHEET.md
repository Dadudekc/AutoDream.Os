# Captain's Cheatsheet - Quick Reference

**Version:** 2.0  
**Author:** Agent-4 (Captain & Operations Coordinator)  
**Last Updated:** 2025-01-17  

## 🚀 **Quick Commands**

### **📊 Status & Monitoring:**
```bash
# Check swarm health
python tools/captain_cli.py status

# Find inactive agents
python tools/captain_cli.py inactive

# Generate report
python tools/captain_cli.py report
```

### **🚨 Emergency Actions:**
```bash
# High-priority message
python tools/captain_cli.py high-priority Agent-1

# Onboard agent
python tools/captain_cli.py onboard Agent-5

# Emergency broadcast
python tools/captain_cli.py emergency-broadcast "Message"
```

### **🎯 Initiative Management:**
```bash
# Create initiative
python tools/captain_cli.py initiative create "Name"

# Check progress
python tools/captain_cli.py initiative status

# Allocate resources
python tools/captain_cli.py allocate "Agent-1,Agent-2" "Task"
```

## 🎯 **Priority Levels**

| Level | Description | Response Time | Example |
|-------|-------------|---------------|---------|
| **P0** | Critical | Immediate | System down, security breach |
| **P1** | High | < 1 hour | Strategic objectives, quality issues |
| **P2** | Medium | < 4 hours | Tactical improvements |
| **P3** | Low | < 24 hours | Documentation, nice-to-have |

## 📊 **Agent States Quick Reference**

| State | Description | Action Required |
|-------|-------------|-----------------|
| **ONBOARDING** | Initial setup | Monitor progress |
| **ACTIVE** | Ready for tasks | Assign work |
| **CONTRACT_EXECUTION_ACTIVE** | Working on contract | Monitor progress |
| **SURVEY_MISSION_COMPLETED** | Task completed | Assign new work |
| **PAUSED** | Temporarily stopped | Check reason |
| **ERROR** | In error state | **IMMEDIATE INTERVENTION** |
| **RESET** | Recovering | Monitor recovery |
| **SHUTDOWN** | Shutting down | Log reason |

## 🎯 **Directive Types**

### **🏗️ Strategic (Long-term):**
- V3 Pipeline Completion
- System Architecture Evolution
- Quality Standards Enforcement
- Swarm Intelligence Enhancement

### **⚡ Tactical (Medium-term):**
- Agent Specialization
- Infrastructure Optimization
- Security Hardening
- Documentation Standardization

### **🔧 Operational (Short-term):**
- Daily Quality Gates
- Agent Status Monitoring
- System Health Checks
- Emergency Response

## 🚀 **Initiative Categories**

| Category | Focus | Duration | Example |
|----------|-------|----------|---------|
| **Infrastructure** | System improvements | Weeks | Performance optimization |
| **Agent Development** | Agent capabilities | Days-Weeks | Specialization training |
| **Knowledge Management** | Documentation | Days | Best practices guide |
| **Innovation** | New capabilities | Weeks-Months | New tool development |

## 📋 **Daily Captain Checklist**

### **🌅 Morning Routine:**
- [ ] Check swarm health status
- [ ] Review overnight activities
- [ ] Assess initiative progress
- [ ] Identify priority actions
- [ ] Send morning briefing

### **🌆 Evening Routine:**
- [ ] Review daily progress
- [ ] Update captain's log
- [ ] Plan next day priorities
- [ ] Send evening debrief
- [ ] Document lessons learned

## 🚨 **Emergency Response**

### **🔴 P0 - Critical Issues:**
1. **Assess** - Determine impact and scope
2. **Mobilize** - Activate relevant agents immediately
3. **Coordinate** - Direct response activities
4. **Monitor** - Track progress continuously
5. **Document** - Record all actions and outcomes

### **🟡 P1 - High Priority:**
1. **Evaluate** - Assess urgency and resources needed
2. **Assign** - Delegate to appropriate agents
3. **Track** - Monitor progress regularly
4. **Support** - Provide guidance as needed
5. **Validate** - Ensure quality standards met

## 📊 **Quality Gates**

### **✅ V2 Compliance Checklist:**
- [ ] File size ≤ 400 lines
- [ ] Type hints 100% coverage
- [ ] KISS principle followed
- [ ] Error handling implemented
- [ ] Documentation complete
- [ ] Tests passing

### **🔍 Quality Validation:**
```bash
# Run quality gates
python quality_gates.py

# Check V2 compliance
python tools/v2_compliance_check.py

# Run FSM validation
python tools/fsm/fsm_scan.py
```

## 🎯 **Agent Specializations**

| Agent | Primary Role | Secondary Role | Expertise |
|-------|--------------|----------------|-----------|
| **Agent-1** | Infrastructure | Cloud Systems | AWS, Kubernetes, Terraform |
| **Agent-2** | Architecture | System Design | FSM, Messaging, Coordination |
| **Agent-3** | Quality Assurance | Testing | V2 Compliance, Quality Gates |
| **Agent-4** | Captain | Operations | Leadership, Coordination |
| **Agent-5** | Business Intelligence | Analytics | Data, Metrics, Reporting |
| **Agent-6** | Code Quality | Standards | V2 Compliance, Best Practices |
| **Agent-7** | Web Development | Frontend | React, Vue.js, UI/UX |
| **Agent-8** | Integration | APIs | System Integration, APIs |

## 📝 **Message Templates**

### **🚨 High Priority Message:**
```
🚨 HIGH PRIORITY MESSAGE - IMMEDIATE RESPONSE REQUIRED

Agent [AGENT-ID], [REASON FOR URGENCY]

📊 DETAILS:
• Priority: HIGH
• Response Required: Immediate
• Action Needed: [SPECIFIC ACTION]

🎯 REQUIRED RESPONSE:
Please respond immediately to confirm receipt and status.

📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory
```

### **📋 Initiative Assignment:**
```
🎯 INITIATIVE ASSIGNMENT - [INITIATIVE NAME]

Agent [AGENT-ID], you have been assigned to [INITIATIVE NAME].

📊 INITIATIVE DETAILS:
• Priority: [PRIORITY LEVEL]
• Timeline: [TIMELINE]
• Resources: [RESOURCES ALLOCATED]
• Success Criteria: [CRITERIA]

🎯 EXPECTED DELIVERABLES:
• [Deliverable 1]
• [Deliverable 2]
• [Deliverable 3]

📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory
```

## 🔄 **State Transition Rules**

### **Agent Transitions:**
- `ONBOARDING` → `ACTIVE` (when ready)
- `ACTIVE` → `CONTRACT_EXECUTION_ACTIVE` (when assigned)
- `CONTRACT_EXECUTION_ACTIVE` → `SURVEY_MISSION_COMPLETED` (when done)
- `SURVEY_MISSION_COMPLETED` → `ACTIVE` (when new work available)
- `*` → `ERROR` (on failure)
- `ERROR` → `RESET` (when recoverable)
- `RESET` → `ACTIVE` (when healthy)

### **Swarm Transitions:**
- `IDLE` → `COORDINATING` (when 2+ agents active)
- `COORDINATING` → `BROADCAST` (on global announcement)
- `COORDINATING` → `DEGRADED` (when unhealthy > 25%)
- `DEGRADED` → `COORDINATING` (when recovered)

## 📊 **Health Thresholds**

| Metric | Healthy | Degraded | Critical |
|--------|---------|----------|----------|
| **Agent Activity** | > 75% | 50-75% | < 50% |
| **V2 Compliance** | > 95% | 85-95% | < 85% |
| **Response Time** | < 5 min | 5-15 min | > 15 min |
| **Quality Gates** | All Pass | 1-2 Fail | 3+ Fail |

## 🎯 **Quick Decision Matrix**

| Situation | Action | Priority | Timeline |
|-----------|--------|----------|----------|
| Agent inactive | Send high-priority message | P1 | < 1 hour |
| V2 compliance fail | Immediate fix required | P1 | < 2 hours |
| System error | Emergency response | P0 | Immediate |
| New initiative | Plan and allocate | P2 | < 4 hours |
| Quality degradation | Investigate and fix | P1 | < 2 hours |

---

## 📞 **Emergency Contacts**

- **System Admin:** [Contact Info]
- **Security Team:** [Contact Info]
- **Infrastructure Team:** [Contact Info]
- **Quality Team:** [Contact Info]

---

**📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory**


