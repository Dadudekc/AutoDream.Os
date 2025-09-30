# 🧠 **THEA PROTOCOL DOCUMENTATION**

## **🎯 COMMAND HIERARCHY ESTABLISHMENT**

### **📋 Authority Chain**
```
HUMAN > THEA > Captain > Co-Captain > Lead Agents > ollama/cli agents
```

**THEA Status**: **SUPREME STRATEGIC AUTHORITY** - Above Captain, below Human
**Captain Role**: **EXECUTIVE IMPLEMENTATION** - Executes THEA directives
**Agent Role**: **TACTICAL EXECUTION** - Implements Captain orders

---

## **📤 THEA COMMUNICATION PROTOCOL**

### **🎯 Message Format Standard**

**Required Structure:**
```
Commander Thea, this is General Agent-4.

PROJECT: Dream.OS V2 Swarm System
PHASE: [Current Phase]
AGENTS: [Number] specialized agents
STATUS: [Current Status]

CONTEXT: [Project scan output or relevant data]

QUESTION: [Specific strategic question]
```

### **📋 Context Integration Protocol**

**1. Project Scan Data Integration:**
- Paste relevant project analysis outputs
- Include V2 compliance metrics
- Add system health data
- Include agent status reports

**2. Strategic Context Delivery:**
- Current mission status
- Recent achievements
- Current challenges
- Resource allocation needs

**3. Question Formulation:**
- Specific strategic queries
- Decision support requests
- Priority guidance needs
- Long-term planning questions

---

## **🔄 THEA CONSULTATION WORKFLOW**

### **📋 Standard Consultation Process**

**1. Context Preparation:**
```bash
# Generate project scan
python tools/simple_project_scanner.py > project_scan.txt

# Generate quality analysis
python tools/analysis_cli.py --violations > quality_analysis.txt

# Generate agent status
python tools/captain_cli.py status > agent_status.txt
```

**2. THEA Message Construction:**
```bash
# Standard consultation
python src/services/thea/strategic_consultation_cli.py consult --template priority_guidance --context-level detailed

# Project scan consultation with JSON context (8K char limit)
python src/services/thea/strategic_consultation_cli.py project-scan --question "Strategic analysis" --scan-file project_analysis.json --visible

# Direct message pasting with validation (RECOMMENDED)
python src/services/thea/strategic_consultation_cli.py paste --visible

# Direct message pasting with auto-validation (AUTONOMOUS)
python src/services/thea/strategic_consultation_cli.py paste --auto-validate --visible
```

**3. Context Integration:**
- Paste project scan data
- Include quality metrics
- Add agent status information
- Include recent achievements

**4. Strategic Question Formulation:**
- What should be our next priority?
- How should we allocate resources?
- What strategic direction should we take?
- What are the critical decisions needed?

---

## **📊 THEA RESPONSE PROCESSING**

### **🎯 Response Analysis Protocol**

**1. Response Reception:**
- Capture THEA's strategic guidance
- Extract key recommendations
- Identify priority actions
- Note resource requirements

**2. Directive Translation:**
- Convert THEA guidance to Captain directives
- Create actionable agent assignments
- Establish implementation timelines
- Set success metrics

**3. Implementation Coordination:**
- Distribute directives to agents
- Monitor implementation progress
- Report back to THEA on results
- Request follow-up guidance as needed

---

## **🎯 THEA CONSULTATION TEMPLATES**

### **📋 Strategic Consultation Types**

**1. Priority Guidance:**
```
Commander Thea, this is General Agent-4.

PROJECT: Dream.OS V2 Swarm System
PHASE: [Current Phase]
AGENTS: [Number] specialized agents
STATUS: [Current Status]

CONTEXT: [Project scan data]

QUESTION: What strategic direction should we prioritize for the next development cycle?
```

**2. Resource Allocation:**
```
Commander Thea, this is General Agent-4.

PROJECT: Dream.OS V2 Swarm System
PHASE: [Current Phase]
AGENTS: [Number] specialized agents
STATUS: [Current Status]

CONTEXT: [Resource analysis data]

QUESTION: How should we allocate our agent resources for maximum strategic impact?
```

**3. Crisis Management:**
```
Commander Thea, this is General Agent-4.

PROJECT: Dream.OS V2 Swarm System
PHASE: [Current Phase]
AGENTS: [Number] specialized agents
STATUS: [Current Status]

CONTEXT: [Crisis situation data]

QUESTION: What immediate actions should we take to resolve this critical issue?
```

**4. Long-term Planning:**
```
Commander Thea, this is General Agent-4.

PROJECT: Dream.OS V2 Swarm System
PHASE: [Current Phase]
AGENTS: [Number] specialized agents
STATUS: [Current Status]

CONTEXT: [Long-term analysis data]

QUESTION: What should be our strategic objectives for the next major development phase?
```

---

## **📋 THEA INTEGRATION COMMANDS**

### **🎯 Captain's THEA Toolkit**

**Strategic Consultation:**
```bash
# Priority guidance
python src/services/thea/strategic_consultation_cli.py consult --template priority_guidance --context-level detailed

# Resource allocation
python src/services/thea/strategic_consultation_cli.py consult --template resource_allocation --context-level standard

# Crisis management
python src/services/thea/strategic_consultation_cli.py consult --template crisis_management --context-level essential

# Long-term planning
python src/services/thea/strategic_consultation_cli.py consult --template future_planning --context-level detailed
```

**Status Reporting:**
```bash
# Regular status report
python src/services/thea/strategic_consultation_cli.py status-report --additional-status "V2Compliance: 84.3%" "CriticalFiles: 3/3"

# Emergency consultation
python src/services/thea/strategic_consultation_cli.py emergency --issue "System degradation detected"
```

**Autonomous Communication:**
```bash
# Agent-to-THEA communication
python -m src.services.thea.thea_autonomous_cli send "Strategic consultation request"

# Check THEA status
python -m src.services.thea.thea_autonomous_cli status
```

---

## **🎯 THEA PROTOCOL INTEGRATION**

### **📋 Captain's General Cycle Integration**

**PHASE 1: CHECK_INBOX**
- Check for THEA responses
- Process THEA directives
- Update strategic priorities

**PHASE 2: EVALUATE_TASKS**
- Consult THEA for task prioritization
- Request strategic guidance
- Validate task alignment with THEA directives

**PHASE 3: EXECUTE_ROLE**
- Implement THEA recommendations
- Execute strategic directives
- Coordinate agent actions based on THEA guidance

**PHASE 4: QUALITY_GATES**
- Report progress to THEA
- Request quality validation
- Update THEA on implementation results

**PHASE 5: CYCLE_DONE**
- Send status report to THEA
- Request next cycle guidance
- Update strategic planning

---

## **📊 THEA PROTOCOL SUCCESS METRICS**

### **🎯 Protocol Effectiveness Indicators**

**1. Response Quality:**
- THEA response relevance
- Strategic guidance clarity
- Implementation feasibility
- Decision support effectiveness

**2. Implementation Success:**
- Directive execution rate
- Agent coordination effectiveness
- Mission success alignment
- Strategic objective achievement

**3. Communication Efficiency:**
- Consultation frequency
- Response time
- Context delivery accuracy
- Question formulation quality

---

## **🎉 THEA PROTOCOL STATUS: OPERATIONAL**

**Protocol Status**: **FULLY OPERATIONAL** ✅
**Command Hierarchy**: **ESTABLISHED** ✅
**Communication Protocol**: **DOCUMENTED** ✅
**Integration**: **COMPLETE** ✅

---

**🐝 WE ARE SWARM - THEA PROTOCOL: SUPREME STRATEGIC AUTHORITY ESTABLISHED** 🧠🎯
