# 📚 AGENT FIELD MANUAL - MASTER INDEX

**Version:** 1.0  
**Date:** 2025-10-15  
**Status:** IN DEVELOPMENT  
**Lead:** Agent-1 (Documentation) + Agent-3 (Infrastructure) + Agent-7 (Web Interface)

---

## 🎯 **PURPOSE**

The **Agent Field Manual** is the **Single Source of Truth** for everything agents need to know about:
- Agent lifecycle and state management
- Cycle-based protocols (NOT daily - CYCLE-based!)
- Status.json requirements
- Toolbelt usage
- Database integration
- Mission execution
- Quality standards
- Swarm coordination

**Problem Solved:** Scattered knowledge across 5+ systems (swarm brain, FSM, toolbelt, database, workflows)

**Solution:** ONE centralized, comprehensive, searchable knowledge base

---

## 📋 **FIELD MANUAL STRUCTURE**

### **Core Guides (11 Total):**

#### **01_AGENT_LIFECYCLE.md** 🔄
**Author:** Agent-1 (content) + Agent-3 (implementation)  
**Status:** PLANNED  
**Topics:**
- Agent states (ACTIVE, IDLE, BLOCKED, WAITING, COMPLETE)
- FSM integration (start, active, process, blocked, complete, end)
- State transitions and triggers
- When to change states
- FSM-status.json mapping

**Target Cycles:** 2-3

---

#### **02_CYCLE_PROTOCOLS.md** ⚡ **CRITICAL**
**Author:** Agent-1  
**Status:** PLANNED  
**Topics:**
- What is a cycle? (1 Captain prompt + 1 Agent response)
- Start of cycle checklist (inbox, status.json, mission)
- During cycle updates (phase changes, tool usage)
- End of cycle checklist (commits, devlogs, sync)
- Violations and consequences

**Target Cycles:** 2

---

#### **03_STATUS_JSON_COMPLETE_GUIDE.md** ⭐ **CRITICAL**
**Author:** Agent-1  
**Status:** PLANNED  
**Topics:**
- What is status.json? (Single Source of Truth for agent state)
- Who reads it? (15+ tools, Captain, Discord bot, etc.)
- Required fields (agent_id, status, current_mission, etc.)
- FSM integration (fsm_state field)
- When to update (every cycle start/end, phase changes)
- How to update (manual, Python script, helper tool)
- Examples by use case (10+ scenarios)
- Database sync requirements
- Common mistakes to avoid

**Target Cycles:** 2

---

#### **04_TOOLBELT_USAGE.md** 🛠️
**Author:** Agent-1 (documentation) + Agent-3 (infrastructure tools)  
**Status:** PLANNED  
**Topics:**
- All 41+ tools documented
- Captain tools (status check, monitoring, etc.)
- Agent tools (messaging, analysis, etc.)
- QA tools (testing, coverage, etc.)
- Infrastructure tools (DB sync, health checks)
- Democratic governance tools (debate system)
- When to use each tool
- Status.json update requirements after tool use

**Target Cycles:** 3

---

#### **05_DATABASE_INTEGRATION.md** 💾
**Author:** Agent-3 (lead) + Agent-1 (documentation)  
**Status:** PLANNED  
**Topics:**
- Database tables (agent_workspaces, agent_status, agent_messages)
- Status.json → database sync
- When sync happens (every cycle, automatic)
- What fields sync
- Sync validation
- Troubleshooting sync issues
- Manual sync commands

**Target Cycles:** 2

---

#### **06_MESSAGING_PROTOCOLS.md** 📨
**Author:** Agent-1  
**Status:** PLANNED  
**Topics:**
- Message types (A2A, C2A, S2A)
- Messaging CLI usage
- PyAutoGUI automation
- Priority levels (urgent, high, regular)
- Response timeframes (1 cycle for A2A)
- Inbox management
- Message archiving

**Target Cycles:** 3

---

#### **07_GAS_SYSTEM.md** ⛽
**Author:** Agent-1  
**Status:** PLANNED  
**Topics:**
- "Prompts are gas" principle explained
- Multiprompt protocol (continuous momentum)
- Self-prompting mechanism
- Fuel monitor (how it works)
- How to avoid "running out of gas"
- Gas delivery frequency
- Cycle-based timelines (NOT time-based!)

**Target Cycles:** 3

---

#### **08_MISSION_EXECUTION.md** 🎯
**Author:** Agent-1  
**Status:** PLANNED  
**Topics:**
- Mission lifecycle (receive, orient, execute, report)
- Mission file format
- Breaking down missions into subtasks
- Status.json updates during missions
- Devlog creation
- Reporting completion
- Multi-cycle missions
- Emergency protocols

**Target Cycles:** 4

---

#### **09_QUALITY_STANDARDS.md** ✅
**Author:** Agent-1 (QA expertise)  
**Status:** PLANNED  
**Topics:**
- V2 compliance (400-line file limit, 100-line class limit)
- Testing pyramid (60% unit, 30% integration, 10% E2E)
- Test coverage requirements (85%+)
- Code quality standards (PEP 8, type hints)
- Documentation requirements
- Git workflow (commits, PRs)
- SOLID principles
- DRY principles

**Target Cycles:** 3

---

#### **10_SWARM_COORDINATION.md** 🐝
**Author:** Agent-1  
**Status:** PLANNED  
**Topics:**
- Multi-agent coordination protocols
- A2A messaging for collaboration
- Shared workspaces
- Democratic debate system
- Swarm proposals
- Conflict resolution
- Captain's role
- Agent specializations

**Target Cycles:** 4

---

#### **99_QUICK_REFERENCE.md** ⚡
**Author:** Agent-1 (consolidation)  
**Status:** PLANNED  
**Topics:**
- One-page cheat sheet
- Most common commands
- Critical checklist (cycle start/end)
- Common issues & fixes
- Emergency contacts
- Quick links to full guides

**Target Cycles:** 5

---

## 🌐 **WEB INTERFACES** (Agent-7 Lead)

### **Interface 1: Interactive Field Manual**
**File:** `web/index.html`  
**Purpose:** Web-based reading interface  
**Features:**
- Navigation sidebar (all 11 guides)
- Search functionality
- Copy code snippets
- Dark mode
- Responsive design
- Bookmarks

**Target Cycles:** 2-4

---

### **Interface 2: Cycle Checklist Dashboard**
**File:** `web/cycle_dashboard.html`  
**Purpose:** Real-time cycle protocol reminder  
**Features:**
- Cycle start/end checklist
- Progress tracking
- Status.json last update indicator
- Database sync status
- Inbox message count
- Next actions reminder

**Target Cycles:** 3-5

---

### **Interface 3: Status.json Visual Editor**
**File:** `web/status_editor.html`  
**Purpose:** Form-based status.json editing  
**Features:**
- All fields as form inputs
- Validation (prevents malformed JSON)
- FSM state dropdown
- Preview before save
- One-click update
- Git commit automatic

**Target Cycles:** 4-6

---

### **Interface 4: Knowledge Search Portal**
**File:** `web/search.html`  
**Purpose:** Search all Field Manual content  
**Features:**
- Full-text search
- Filter by topic/agent/use case
- Context snippets
- Highlighted matches
- Integration with swarm brain API

**Target Cycles:** 5-7

---

## 🔄 **ACCESS METHODS**

### **Method 1: Direct File Access**
```bash
# Read guides directly
cat swarm_brain/agent_field_manual/02_CYCLE_PROTOCOLS.md
```

### **Method 2: Swarm Brain API**
```python
from src.swarm_brain.swarm_memory import SwarmMemory

memory = SwarmMemory(agent_id='Agent-X')
results = memory.search_swarm_knowledge("how to update status.json")
```

### **Method 3: Web Interface** ⭐ **RECOMMENDED**
```
http://localhost:8000/swarm_brain/agent_field_manual/web/index.html
```

### **Method 4: Quick Reference** ⚡ **FASTEST**
```bash
cat swarm_brain/agent_field_manual/99_QUICK_REFERENCE.md
```

---

## 📊 **DEVELOPMENT STATUS**

| **Guide** | **Status** | **Author** | **Target Cycle** |
|-----------|-----------|------------|------------------|
| 01_AGENT_LIFECYCLE.md | PLANNED | Agent-1 + Agent-3 | 2-3 |
| 02_CYCLE_PROTOCOLS.md | PLANNED | Agent-1 | 2 |
| 03_STATUS_JSON_COMPLETE_GUIDE.md | PLANNED | Agent-1 | 2 |
| 04_TOOLBELT_USAGE.md | PLANNED | Agent-1 + Agent-3 | 3 |
| 05_DATABASE_INTEGRATION.md | PLANNED | Agent-3 + Agent-1 | 2 |
| 06_MESSAGING_PROTOCOLS.md | PLANNED | Agent-1 | 3 |
| 07_GAS_SYSTEM.md | PLANNED | Agent-1 | 3 |
| 08_MISSION_EXECUTION.md | PLANNED | Agent-1 | 4 |
| 09_QUALITY_STANDARDS.md | PLANNED | Agent-1 | 3 |
| 10_SWARM_COORDINATION.md | PLANNED | Agent-1 | 4 |
| 99_QUICK_REFERENCE.md | PLANNED | Agent-1 | 5 |
| **Web: Field Manual** | PLANNED | Agent-7 | 2-4 |
| **Web: Cycle Dashboard** | PLANNED | Agent-7 | 3-5 |
| **Web: Status Editor** | PLANNED | Agent-7 | 4-6 |
| **Web: Search Portal** | PLANNED | Agent-7 | 5-7 |

---

## 🎯 **PRIORITY ORDER**

### **Cycle 2 (CRITICAL):**
1. ⭐ `02_CYCLE_PROTOCOLS.md` - Agents need this NOW!
2. ⭐ `03_STATUS_JSON_COMPLETE_GUIDE.md` - Solves update problem!
3. `05_DATABASE_INTEGRATION.md` - Agent-3's expertise

### **Cycle 3:**
4. `04_TOOLBELT_USAGE.md` - Document all 41 tools
5. `09_QUALITY_STANDARDS.md` - V2 compliance reference
6. `06_MESSAGING_PROTOCOLS.md` - Communication standards

### **Cycle 4-5:**
7. `01_AGENT_LIFECYCLE.md` - FSM integration
8. `08_MISSION_EXECUTION.md` - Execution workflows
9. `10_SWARM_COORDINATION.md` - Multi-agent protocols
10. `07_GAS_SYSTEM.md` - Prompts are gas explained
11. `99_QUICK_REFERENCE.md` - Consolidation

---

## 🔗 **RELATED SYSTEMS**

### **Swarm Brain Knowledge Base:**
- `swarm_brain/knowledge_base.json` - Existing knowledge (to be integrated)
- `swarm_brain/shared_learnings/` - Agent learnings
- `swarm_brain/procedures/` - Existing procedures

### **Swarm Brain Protocols:**
- `swarm_brain/protocols/PR_APPROVAL_PROTOCOL.md`
- `swarm_brain/protocols/NOTE_TAKING_PROTOCOL.md`
- `swarm_brain/protocols/SWARM_BRAIN_ACCESS_GUIDE.md`

### **Documentation:**
- `docs/AGENT_ORIENTATION.md` - Onboarding guide
- `prompts/agents/onboarding.md` - Onboarding template
- `STANDARDS.md` - Repository standards

**Field Manual integrates and consolidates all of these!**

---

## 📝 **VERSION HISTORY**

**v1.0 (2025-10-15):**
- Initial structure created
- All 11 guides planned
- Web interfaces designed
- 3-agent coordination established

---

## 🐝 **CONTRIBUTORS**

**Agent-1** - Documentation & QA Lead  
**Agent-3** - Infrastructure & Automation Lead  
**Agent-7** - Web Development & Interface Lead

**Together:** Building the definitive agent knowledge system!

---

**🚀 STATUS: ACTIVE DEVELOPMENT - CYCLE 1** ⚡

**#FIELD-MANUAL #SWARM-BRAIN #UNIFIED-KNOWLEDGE #AGENT-1-3-7**

