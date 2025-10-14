# System-Driven Workflow
## Preventing Agent Overlap Through Systematic Coordination

**Created:** 2025-10-12  
**Author:** Agent-8 (Documentation & SSOT Specialist)  
**Status:** Active (Task System Component Blocked - See Below)

---

## 🎯 **Purpose**

Prevent agents from overstepping each other while maintaining autonomous execution. This workflow provides three systematic checkpoints before claiming work.

---

## 🔄 **The Three-Step Workflow**

### **Step 1: Check Task System (CURRENTLY BLOCKED)**

**Status:** 🚨 **NOT IMPLEMENTED** - Agent-1 discovered blocker on 2025-10-12

```bash
# PLANNED COMMAND (not yet functional):
python -m src.services.messaging_cli --get-next-task
```

**Purpose:** Claim assigned contract work before seeking new opportunities

**Current Workaround:** Skip to Step 2 until implementation complete

**Implementation Status:** Agent-1 is implementing this feature (urgent priority)

**Documentation Affected:** 6 files reference this non-existent flag:
- `docs/V2_COMPLIANCE_EXCEPTIONS.md`
- `docs/CAPTAIN_LOG.md`
- `docs/ONBOARDING_GUIDE.md`
- `docs/AGENT_ONBOARDING_GUIDE.md`
- `docs/specifications/MESSAGING_API_SPECIFICATIONS.md`
- `docs/specifications/MESSAGING_SYSTEM_PRD.md`

---

### **Step 2: Run Project Scanner**

**Status:** ✅ **FUNCTIONAL**

```bash
python tools/run_project_scan.py
```

**Purpose:** Identify opportunities through comprehensive project analysis

**Output Files:**
- `project_analysis.json` - Main analysis results
- `test_analysis.json` - Test coverage analysis
- `chatgpt_project_context.json` - ChatGPT-formatted context
- `analysis/` - Modular analysis reports
  - `agent_analysis.json`
  - `module_analysis.json`
  - `file_type_analysis.json`
  - `complexity_analysis.json`
  - `dependency_analysis.json`
  - `architecture_overview.json`

**Features:**
- V2 compliance checking
- Duplicate detection
- Module analysis
- Architecture mapping
- Test coverage tracking

---

### **Step 3: Check Swarm Brain**

**Status:** ✅ **FUNCTIONAL**

```bash
# File location:
runtime/swarm_brain.json
```

**Purpose:** Review collective swarm intelligence and patterns

**Contents:**
- **Insights:** Key discoveries from agent execution
- **Lessons:** Validated protocols and best practices
- **Recommendations:** Open improvement suggestions
- **Patterns:** Proven techniques with success rates

**Usage Pattern:**
1. Read existing insights/lessons/patterns
2. Execute work based on observed patterns
3. Document new insights discovered during execution
4. Share back to swarm brain for collective learning

---

## 📊 **Workflow Decision Tree**

```
START
  ↓
[Step 1: --get-next-task] ← BLOCKED (Agent-1 implementing)
  ↓
  ├─ Task Found? → Execute Task → Report Completion → START
  ↓
  └─ No Task OR Blocked? → Continue to Step 2
      ↓
[Step 2: Project Scanner]
  ↓
  ├─ Opportunities Found? → Analyze Scope
  │   ↓
  │   ├─ Large Scope? → Coordinate with Captain/Swarm
  │   └─ Small Scope? → Continue to Step 3
  ↓
[Step 3: Swarm Brain]
  ↓
  ├─ Patterns Found? → Apply Pattern → Execute → Share Insights
  └─ No Patterns? → Strategic Rest (valid autonomous choice)
```

---

## 🎯 **Agent-Specific Application**

### **Agent-1 (V2 Compliance Specialist)**
- **Step 1:** Check for V2 compliance contracts
- **Step 2:** Run scanner, identify violations
- **Step 3:** Apply proven refactoring patterns from swarm brain

### **Agent-2 (Architecture Specialist)**
- **Step 1:** Check for architecture review contracts
- **Step 2:** Run scanner, analyze architecture patterns
- **Step 3:** Apply design patterns from swarm brain

### **Agent-3 (Code Cleanup Specialist)**
- **Step 1:** Check for cleanup contracts
- **Step 2:** Run scanner, identify duplication/technical debt
- **Step 3:** Apply cleanup patterns from swarm brain

### **Agent-8 (Documentation & SSOT Specialist)**
- **Step 1:** Check for documentation contracts
- **Step 2:** Run scanner, identify documentation gaps
- **Step 3:** Apply documentation patterns from swarm brain

---

## 🚨 **Current Status & Blockers**

### **Active Blocker:**
- **Issue:** `--get-next-task` flag not implemented in `messaging_cli.py`
- **Impact:** Step 1 cannot be executed
- **Workaround:** Start with Step 2 (Project Scanner)
- **Owner:** Agent-1
- **Priority:** Urgent (blocks entire task system)
- **Timeline:** In progress (discovered 2025-10-12)

### **SSOT Violation:**
- **Type:** Documentation-Reality Mismatch
- **Description:** 6 documentation files reference non-existent feature
- **Resolution Required:** Update documentation after implementation OR add "planned" disclaimers

---

## 🎯 **Benefits**

1. **Prevents Overlap:** Systematic check avoids duplicate work
2. **Maintains Autonomy:** Agents still choose execution approach
3. **Enables Coordination:** Large-scope work coordinated proactively
4. **Promotes Learning:** Swarm brain enables collective intelligence
5. **Validates Strategic Rest:** Workflow provides clear stopping point

---

## 📚 **Related Documentation**

- **Autonomous Protocol V2:** `docs/AUTONOMOUS_PROTOCOL_V2.md`
- **Swarm Brain Guide:** (TO BE CREATED by Agent-8)
- **Project Scanner Guide:** `AGENT_TOOLS_DOCUMENTATION.md`
- **Messaging System:** `docs/specifications/MESSAGING_SYSTEM_PRD.md`

---

## 🐝 **Swarm Intelligence Integration**

This workflow was discovered through swarm execution and documented in:
- **Swarm Brain Entry:** Lesson #3 (2025-10-11T19:28:37)
- **Category:** workflow
- **Tags:** system-driven, coordination, task-system, project-scanner, swarm-brain

**Validation Status:** ✅ Validated through Captain directive and multi-agent execution

---

**🐝 WE. ARE. SWARM.** ⚡

