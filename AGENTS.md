# 🤖 **AGENTS - SWARM OPERATIONS MANUAL**

## **Complete Agent Documentation & Quick Reference**
**V2 Compliance**: Unified agent documentation with operational guidelines

**Author**: Agent-4 - Captain (Strategic Oversight)  
**Last Updated**: 2025-01-14  
**Status**: ACTIVE - Complete Agent Documentation

---

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

## 🚀 **AGENT QUICK REFERENCE CARD**

**For:** All Swarm Agents  
**Purpose:** Quick access to essential tools and commands  
**Last Updated:** 2025-01-14

### 🔍 **PROJECT ANALYSIS (Most Used)**

#### **Complete Project Scan:**
```bash
python tools/run_project_scan.py
```
**Output:** `project_analysis.json`, `chatgpt_project_context.json`

#### **Chunked Analysis (Consolidation):**
```bash
python comprehensive_project_analyzer.py
```
**Output:** `analysis_chunks/` directory with 13 manageable chunks

#### **Messaging System Analysis:**
```bash
python analyze_messaging_files.py
```
**Output:** `messaging_project_analysis.json`, `messaging_chatgpt_context.json`

### 🚀 **CONSOLIDATION TOOLS**

#### **Configuration Management:**
```python
from src.core.unified_config import get_config
config = get_config()
```

#### **Import Analysis:**
```python
from src.core.unified_import_system import analyze_imports
import_analysis = analyze_imports()
```

#### **PyAutoGUI Messaging:**
```python
from src.services.messaging_pyautogui import PyAutoGUIMessagingDelivery
messaging = PyAutoGUIMessagingDelivery()
```

### 🧪 **TESTING & QUALITY**

#### **Run All Tests:**
```bash
python -m pytest
```

#### **Run with Coverage:**
```bash
python -m pytest --cov=src
```

#### **Code Quality Analysis:**
```bash
python tools/duplication_analyzer.py
```

### 📊 **CONSOLIDATION CHUNKS**

| Chunk | Directory | Agent | Priority | Files | Target |
|-------|-----------|-------|----------|-------|--------|
| 001 | src/core | Agent-2 | CRITICAL | 50→15 | 70% |
| 002 | src/services | Agent-1 | CRITICAL | 50→20 | 60% |
| 003 | src/web | Agent-7 | MEDIUM | 50→30 | 40% |
| 004 | src/utils | Agent-3 | HIGH | 12→5 | 58% |
| 005 | src/infrastructure | Agent-3 | HIGH | 19→8 | 58% |

### 🎯 **AGENT ASSIGNMENTS**

- **Agent-1 (Integration):** Services consolidation, PyAutoGUI messaging
- **Agent-2 (Architecture):** Core modules, Project Scanner, Configuration
- **Agent-3 (DevOps):** Utils/Infrastructure, File management, Testing
- **Agent-4 (Captain):** Strategic oversight, emergency intervention, quality assurance
- **Agent-5 (Business Intelligence):** Data analysis, reporting, business logic
- **Agent-6 (Communication):** Documentation/Tools, Swarm coordination
- **Agent-7 (Web Development):** Web interface consolidation
- **Agent-8 (SSOT):** System integration, single source of truth maintenance

### 📁 **KEY FILES**

#### **Analysis Results:**
- `project_analysis.json` - Complete project analysis
- `chatgpt_project_context.json` - AI-ready context
- `analysis_chunks/` - Chunked analysis results

#### **Consolidation Planning:**
- `CONSOLIDATION_ACTION_PLAN.md` - Implementation plan
- `COMPREHENSIVE_CHUNKED_ANALYSIS_SUMMARY.md` - Analysis summary
- `swarm_debate_consolidation.xml` - Swarm debate

#### **Documentation:**
- `CAPTAIN_HANDBOOK.md` - Complete operational handbook
- `AGENT_TOOLS_DOCUMENTATION.md` - Complete tool documentation

### 🚨 **EMERGENCY COMMANDS**

#### **Check Project Status:**
```bash
python tools/run_project_scan.py
```

#### **Validate Consolidation:**
```bash
python -m pytest
```

#### **Backup Current State:**
```bash
python src/utils/backup.py
```

### 📞 **SWARM COORDINATION**

#### **Debate Participation:**
- Review `swarm_debate_consolidation.xml`
- Add arguments via PyAutoGUI messaging
- Update task progress in markdown files

#### **Progress Reporting:**
- Update `CONSOLIDATION_ACTION_PLAN.md`
- Report via PyAutoGUI messaging
- Document changes in appropriate files

---

## 📋 **Agent Development Guidelines**

This repository is primarily a **Python** project. Unless explicitly noted, all new code should be written in Python and follow the guidelines below.

### **Repository Policies**
- This repository is Python-primary. All agents/tools SHOULD be implemented in Python unless a strong rationale exists.
- Every commit/push MUST keep snapshots current: project_analysis.json, test_analysis.json, chatgpt_project_context.json.
- Pre-commit auto-generates snapshots; pre-push enforces freshness.

### **🛠️ Agent Tools & Resources**

#### **Project Scanner (Critical Tool)**
- **Location:** `tools/projectscanner.py`
- **Runner:** `tools/run_project_scan.py`
- **Enhanced:** `comprehensive_project_analyzer.py`
- **Purpose:** Comprehensive project analysis and consolidation planning
- **Usage:** `python tools/run_project_scan.py`
- **Output:** project_analysis.json, chatgpt_project_context.json, analysis_chunks/

#### **Agent Tools Documentation**
- **Location:** `AGENT_TOOLS_DOCUMENTATION.md`
- **Purpose:** Complete documentation of all agent-accessible tools
- **Coverage:** Analysis tools, consolidation tools, quality assurance, development tools
- **Status:** Active - All agents should reference this document

#### **Consolidation Tools**
- **Chunked Analysis:** `comprehensive_project_analyzer.py`
- **Messaging Analysis:** `analyze_messaging_files.py`
- **Configuration:** `src/core/unified_config.py`
- **Action Plan:** `CONSOLIDATION_ACTION_PLAN.md`

### **Code Style**
- Follow **PEP 8** and include type hints.
- Keep line length ≤100 characters.
- Use **snake_case** for database columns and API fields.
- Prefer class-based design for complex logic.
- **Monitoring component** (`src/core/health/monitoring/`) is exempt from the Python-only rule and may use alternative technologies if required.

### **Architecture**
- Apply the **repository pattern** for data access.
- Keep **business logic** inside service layers.
- Use dependency injection for shared utilities.
- Avoid circular dependencies across modules.
- Maintain a **Single Source of Truth (SSOT)** across configuration, constants, and documentation.

### **Testing**
- All new features require unit tests using **pytest**.
- Mock external APIs and database calls.
- Keep coverage above **85%**.
- Run `pre-commit run --files <file>` and `pytest` before committing.

### **Documentation**
- Document public functions and classes with docstrings.
- Provide usage examples for new utilities.
- Update `README.md` when adding new features.
- Record significant updates in `CHANGELOG.md`.

### **Workflow**
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

### **V2 Compliance**
- Write **clean, tested, reusable, scalable** code.
- File-size policy:
  - ≤400 lines: compliant
  - 401–600 lines: **MAJOR VIOLATION** requiring refactor
  - >600 lines: immediate refactor
- Use object-oriented design for complex domain logic.
- Ensure comprehensive error handling and logging.
- Prioritize modular design and clear boundaries between modules.

---

## 🐝 **Swarm Participation Guidelines**

### 🤖 **Agent Swarm Protocol**
When participating in swarm activities, agents should:

1. **Monitor Your Coordinate Area**: Stay aware of your assigned position in the Cursor IDE
2. **Respond to Coordination Signals**: Be prepared for automated messaging from the swarm coordinator
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

---

**✅ AGENT DOCUMENTATION COMPLETE**
**Unified Reference | Quick Access | Complete Guidelines**

**Ready for comprehensive swarm operations!** 🚀⚡
