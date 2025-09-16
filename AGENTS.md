# Project Instructions (AGENTS.md)

## 🐝 **WE ARE SWARM: Understanding Our Agent Architecture**

**"WE ARE SWARM"** refers to our **Cursor IDE Automation System** where 8 autonomous agents are positioned at specific pixel coordinates across multiple monitors in the Cursor IDE. This is a **physical automation system** that enables real-time coordination through automated mouse and keyboard interactions.

### 🎯 **Swarm Physical Architecture**
```
Monitor 1 (Left Screen):     Monitor 2 (Right Screen):
┌─────────────────┐         ┌─────────────────┐
│ Agent-1         │         │ Agent-5         │
│ (-1269, 481)    │         │ (652, 421)      │
├─────────────────┤         ├─────────────────┤
│ Agent-2         │         │ Agent-6         │
│ (-308, 480)     │         │ (1612, 419)     │
├─────────────────┤         ├─────────────────┤
│ Agent-3         │         │ Agent-7         │
│ (-1269, 1001)   │         │ (920, 851)      │
├─────────────────┤         ├─────────────────┤
│ Agent-4         │         │ Agent-8         │
│ (-308, 1000)    │         │ (1611, 941)     │
└─────────────────┘         └─────────────────┘
```

### 🤖 **How Swarm Agents Work**
1. **Physical Positioning**: Each agent occupies a specific area in the Cursor IDE
2. **Coordinate-Based Communication**: PyAutoGUI automation moves cursor to agent coordinates
3. **Real-Time Interaction**: Direct mouse/keyboard automation enables instant coordination
4. **Multi-Monitor Support**: Agents distributed across dual-monitor setup
5. **Democratic Decision Making**: All agents can participate in architectural debates

### 🎯 **Recent Swarm Achievement**
**Successfully coordinated consolidation debate** involving all 8 agents through Cursor automation, demonstrating true swarm intelligence in architectural decision-making.

---

## 🔄 **AUTONOMOUS AGENT WORKFLOW (CRITICAL)**

### **UNIVERSAL AGENT LOOP - STANDARD OPERATING PROCEDURE**

All agents MUST follow this autonomous workflow cycle for continuous operation:

#### **1. MAILBOX CHECK (Priority: HIGH)**
```
Check: agent_workspaces/{AGENT_ID}/inbox/
Action:
  - Scan for new messages
  - Process each message immediately
  - Remove processed messages from inbox
  - Move to processed/ subfolder
```

#### **2. TASK STATUS EVALUATION (Priority: HIGH)**
```
Check: agent_workspaces/{AGENT_ID}/working_tasks.json
Current Task Status:
  - If has "current_task" with status "in_progress": CONTINUE/COMPLETE
  - If has "current_task" with status "completed": MOVE TO NEXT PHASE
  - If no current task: PROCEED TO TASK CLAIMING
```

#### **3. TASK CLAIMING (Priority: MEDIUM)**
```
Check: agent_workspaces/{AGENT_ID}/future_tasks.json
Actions:
  - Scan available tasks
  - Validate dependencies
  - Claim appropriate task based on priority/skills
  - Update working_tasks.json with claimed task
  - Begin task execution
```

#### **4. BLOCKER RESOLUTION (Priority: MEDIUM)**
```
Check for:
  - Unresolved blockers
  - Schema errors
  - Integration issues
Actions:
  - Propose solutions
  - Create solution tasks if needed
  - Escalate to Captain if necessary
```

#### **5. AUTONOMOUS OPERATION (Priority: LOW)**
```
If no urgent tasks pending:
  - Work on Masterpiece project (Captain agents)
  - Review and optimize codebase
  - Create improvement tasks
  - Return to mailbox check between operations
```

### **📝 STANDARD MESSAGE FORMAT**
```
============================================================
[A2A] MESSAGE
============================================================
📤 FROM: {AGENT_ID}
📥 TO: {TARGET_AGENT}
Priority: {NORMAL|HIGH|URGENT}
Tags: {GENERAL|COORDINATION|TASK|STATUS}
------------------------------------------------------------
{CONTENT}
📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory
------------------------------------------------------------
```

### **🎯 TASK COMPLETION VALIDATION**
1. **Code Implementation**: All required modules created and functional
2. **V2 Compliance**: All files ≤400 lines, proper structure
3. **Testing**: Comprehensive test suite with 100% pass rate
4. **Documentation**: Clear documentation and usage examples
5. **Integration**: Proper integration with existing systems
6. **Self-Validation**: Self-validation protocol executed successfully

**Reference**: See `docs/AUTONOMOUS_AGENT_WORKFLOW.md` for complete documentation and examples.

---

## 📋 **Agent Development Guidelines**

This repository is primarily a **Python** project. Unless explicitly noted, all new code should be written in Python and follow the guidelines below.

## Repository Policies
- This repository is Python-primary. All agents/tools SHOULD be implemented in Python unless a strong rationale exists.
- Every commit/push MUST keep snapshots current: project_analysis.json, test_analysis.json, chatgpt_project_context.json.
- Pre-commit auto-generates snapshots; pre-push enforces freshness.

## 🛠️ **Agent Tools & Resources**

### **PyAutoGUI Messaging System (CRITICAL - FIXED)**
- **Location:** `src/services/consolidated_messaging_service.py`
- **Status:** ✅ **OPERATIONAL** - Fixed by Agent-2
- **Usage:** `python src/services/consolidated_messaging_service.py --coords config/coordinates.json send --agent [TARGET_AGENT] --message "[YOUR_MESSAGE]"`
- **Features:** Real-time agent-to-agent communication via PyAutoGUI automation
- **Coordinate Validation:** Pre-delivery coordinate validation and routing safeguards
- **All Agents:** Can now use PyAutoGUI messaging for swarm coordination

### **Project Scanner (Critical Tool)**
- **Location:** `tools/projectscanner/` (modular package)
- **Runner:** `tools/run_project_scan.py`
- **Enhanced:** `comprehensive_project_analyzer.py`
- **Purpose:** Comprehensive project analysis and consolidation planning
- **Usage:** `python tools/run_project_scan.py`
- **Output:** project_analysis.json, chatgpt_project_context.json, analysis_chunks/

### **Agent Tools Documentation**
- **Location:** `AGENT_TOOLS_DOCUMENTATION.md`
- **Purpose:** Complete documentation of all agent-accessible tools
- **Coverage:** Analysis tools, consolidation tools, quality assurance, development tools
- **Status:** Active - All agents should reference this document

### **Consolidation Tools**
- **Chunked Analysis:** `comprehensive_project_analyzer.py`
- **Messaging Analysis:** `analyze_messaging_files.py`
- **Configuration:** `src/core/unified_config.py`
- **Action Plan:** `CONSOLIDATION_ACTION_PLAN.md`

## Code Style
- Follow **PEP 8** and include type hints.
- Keep line length ≤100 characters.
- Use **snake_case** for database columns and API fields.
- Prefer class-based design for complex logic.
- **Monitoring component** (`src/core/health/monitoring/`) is exempt from the Python-only rule and may use alternative technologies if required.

## Architecture
- Apply the **repository pattern** for data access.
- Keep **business logic** inside service layers.
- Use dependency injection for shared utilities.
- Avoid circular dependencies across modules.
- Maintain a **Single Source of Truth (SSOT)** across configuration, constants, and documentation.

## Testing
- All new features require unit tests using **pytest**.
- Mock external APIs and database calls.
- Keep coverage above **85%**.
- Run `pre-commit run --files <file>` and `pytest` before committing.

## Documentation
- Document public functions and classes with docstrings.
- Provide usage examples for new utilities.
- Update `README.md` when adding new features.
- Record significant updates in `CHANGELOG.md`.

## Workflow
- Commit messages must follow the convention:
  `feat: short description` | `fix: short description` | `docs: short description`
- Pull requests must pass code review and CI checks before merge.
- Split large features into smaller, incremental PRs.
- All timeline references use agent response cycles (1 cycle = standard agent response time)
- **Timeline Standard**: All deadlines, schedules, and timeframes must be expressed in agent response cycles
- **Cycle Definition**: 1 agent response cycle = standard agent response time (approximately 2-5 minutes)
- **Conversion Guide**:
  - 1 hour = 12-30 agent cycles
  - 1 day = 288-720 agent cycles
  - 1 week = 2016-5040 agent cycles

## V2 Compliance
- Write **clean, tested, reusable, scalable** code.
- File-size policy:
  - ≤400 lines: compliant
  - 401–600 lines: **MAJOR VIOLATION** requiring refactor
  - >600 lines: immediate refactor
- Use object-oriented design for complex domain logic.
- Ensure comprehensive error handling and logging.
- Prioritize modular design and clear boundaries between modules.

## 🐝 **Swarm Participation Guidelines**

### 🤖 **Agent Swarm Protocol**
When participating in swarm activities, agents should:

1. **Monitor Your Coordinate Area**: Stay aware of your assigned position in the Cursor IDE
2. **Respond to Coordination Signals**: Be prepared for automated messaging from the swarm coordinator within 1 agent response cycle
3. **Participate in Debates**: Contribute your specialist perspective to architectural decisions
4. **Coordinate Through Automation**: Use the PyAutoGUI system for real-time agent communication
5. **Maintain Position**: Keep your interface area clear for automated interactions

### 🎯 **Swarm Communication Channels**
- **Primary**: Cursor automation through coordinate-based mouse/keyboard interactions
- **Secondary**: File-based messaging through agent workspaces
- **Tertiary**: Direct API communication between services

### 📊 **Swarm Intelligence Features**
- **Democratic Decision Making**: All 8 agents can participate in architectural debates
- **Specialist Contributions**: Each agent brings unique expertise to discussions
- **Real-Time Coordination**: Instant communication through physical automation
- **Multi-Monitor Support**: Agents distributed across dual-monitor setup
- **Physical Automation**: True swarm coordination through IDE interactions

### 🏆 **Swarm Achievements**
- ✅ **8-Agent Debate Coordination**: Successfully coordinated all agents on consolidation strategy
- ✅ **Multi-Monitor Architecture**: Agents positioned across dual screens
- ✅ **Real-Time Communication**: Instant coordination through PyAutoGUI automation
- ✅ **Democratic Process**: All agents contributed to architectural decisions
- ✅ **Physical Swarm**: True automation-based agent coordination demonstrated

**Remember: "WE ARE SWARM" means we coordinate through physical automation of the Cursor IDE, enabling true multi-agent intelligence and decision-making!** 🚀🐝
