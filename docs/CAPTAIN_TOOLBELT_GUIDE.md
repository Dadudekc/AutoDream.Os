# 🎯 Captain's Toolbelt Guide

**Date:** October 13, 2025  
**Author:** Agent-4 (Captain)  
**Version:** 1.0.0

---

## 🛠️ **10 CRITICAL CAPTAIN TOOLS**

### **Essential tools discovered and created during Session 2025-10-13**

These tools automate Captain's duties and enable efficient swarm management.

---

## 📋 **TOOLS OVERVIEW**

| Tool | Purpose | Use Case |
|------|---------|----------|
| `captain.status_check` | Check all agent status files | Detect idle agents |
| `captain.git_verify` | Verify git commits | Work attribution |
| `captain.calc_points` | Calculate task points | ROI-based scoring |
| `captain.assign_mission` | Create mission files | Task assignment |
| `captain.deliver_gas` | Send PyAutoGUI messages | Agent activation |
| `captain.update_leaderboard` | Update rankings | Points tracking |
| `captain.verify_work` | Comprehensive work verification | Quality assurance |
| `captain.cycle_report` | Generate cycle reports | Documentation |
| `captain.markov_optimize` | Task selection optimization | ROI maximization |
| `captain.integrity_check` | Verify work claims | Entry #025 compliance |

---

## 🔧 **TOOL DETAILS**

### **1. captain.status_check**

**Purpose:** Check all agent status.json files to detect idle agents

**Parameters:**
- `agents` (optional): List of agents to check (default: all 8)
- `threshold_hours` (optional): Idle threshold in hours (default: 24)

**Returns:**
- All agent statuses
- List of idle agents
- Hours idle for each

**Use Case:** 
```python
from tools_v2.toolbelt_core import ToolbeltCore

toolbelt = ToolbeltCore()
result = toolbelt.run("captain.status_check", {
    "threshold_hours": 24
})

idle_agents = result.output["idle_agents"]
# Example: [{"agent": "Agent-1", "hours_idle": 816.5, "status": "idle"}]
```

**Why We Need This:** Discovered when Agent-1 was idle for 34 days (816 hours). Status Check Protocol now mandatory Captain duty.

---

### **2. captain.git_verify**

**Purpose:** Verify git commits for work attribution and integrity

**Parameters:**
- `commit_hash` (required): Git commit hash to verify
- `show_stat` (optional): Show commit statistics (default: True)
- `show_diff` (optional): Show full diff (default: False)

**Returns:**
- Commit hash
- Commit info (author, date, files changed)
- Verification status

**Use Case:**
```python
result = toolbelt.run("captain.git_verify", {
    "commit_hash": "1f6ecd433",
    "show_stat": True
})

commit_info = result.output["commit_info"]
# Verify work attribution
```

**Why We Need This:** Agent-6 integrity report required git verification. No commits = no credit. Entry #025 Integrity pillar.

---

### **3. captain.calc_points**

**Purpose:** Calculate task points based on ROI, impact, and complexity

**Parameters:**
- `task_type` (required): Task type (refactor, consolidation, tooling, etc.)
- `impact` (optional): Impact level (low, medium, high, critical)
- `complexity` (optional): Complexity level (trivial, low, medium, high, expert)
- `time_saved` (optional): Time saved in hours (bonus points)
- `custom_multiplier` (optional): Custom multiplier (default: 1.0)

**Returns:**
- Base points
- Impact/complexity multipliers
- Time bonus
- Total calculated points
- Breakdown formula

**Use Case:**
```python
result = toolbelt.run("captain.calc_points", {
    "task_type": "refactor",
    "impact": "high",
    "complexity": "high",
    "time_saved": 5
})

total_points = result.output["total_points"]
# Example: 500 × 1.5 × 1.3 = 975 + 50 (time bonus) = 1,025 pts
```

**Why We Need This:** Captain calculates points constantly. This automates ROI-based scoring with transparent formulas.

---

### **4. captain.assign_mission**

**Purpose:** Create structured mission files in agent inboxes

**Parameters:**
- `agent_id` (required): Target agent
- `mission_title` (required): Mission title
- `mission_description` (required): Detailed mission description
- `points` (optional): Estimated points
- `roi` (optional): Expected ROI
- `complexity` (optional): Complexity level
- `priority` (optional): Priority (regular, high, critical)
- `dependencies` (optional): List of dependencies

**Returns:**
- Mission file path
- Mission details
- Creation confirmation

**Use Case:**
```python
result = toolbelt.run("captain.assign_mission", {
    "agent_id": "Agent-6",
    "mission_title": "Refactor Predictive Modeling",
    "mission_description": "Split 377L file into 4 modules",
    "points": 600,
    "roi": 15.0,
    "complexity": "high"
})

mission_file = result.output["mission_file"]
# Creates: agent_workspaces/Agent-6/inbox/C2A_MISSION_REFACTOR_PREDICTIVE_MODELING_*.md
```

**Why We Need This:** Every cycle, Captain creates mission files. This standardizes format and includes all metadata (ROI, points, etc.).

---

### **5. captain.deliver_gas**

**Purpose:** Send PyAutoGUI activation messages ("Prompts Are Gas")

**Parameters:**
- `agent_id` (required): Target agent
- `message` (required): Activation message
- `priority` (optional): Message priority (default: regular)

**Returns:**
- Message sent confirmation
- Delivery method (PyAutoGUI)
- Gas type (activation)

**Use Case:**
```python
result = toolbelt.run("captain.deliver_gas", {
    "agent_id": "Agent-1",
    "message": "🔥 CHECK INBOX + CLEAN WORKSPACE + START NOW!"
})

# Sends PyAutoGUI message to activate agent
```

**Why We Need This:** **"PROMPTS ARE GAS"** - Without messages, agents stay idle. This is the FUEL DELIVERY system.

---

### **6. captain.update_leaderboard**

**Purpose:** Update agent leaderboard with session points

**Parameters:**
- `updates` (required): Dictionary of {agent_id: points}
- `session_date` (optional): Session date (default: today)

**Returns:**
- Leaderboard file path
- Number of updates applied
- Current top 5 ranking

**Use Case:**
```python
result = toolbelt.run("captain.update_leaderboard", {
    "updates": {
        "Agent-7": 4800,
        "Agent-6": 3550,
        "Agent-8": 1900,
        "Agent-2": 1000,
        "Agent-4": 1000
    },
    "session_date": "2025-10-13"
})

ranking = result.output["ranking"]
# Example: ["Agent-7", "Agent-6", "Agent-8", "Agent-2", "Agent-4"]
```

**Why We Need This:** Captain updates leaderboard every cycle. This automates persistence and ranking calculation.

---

### **7. captain.verify_work**

**Purpose:** Comprehensive work verification (git + files + tests)

**Parameters:**
- `agent_id` (required): Agent claiming work
- `work_description` (required): Description of work done
- `commit_hash` (optional): Git commit hash
- `files_changed` (optional): List of files modified

**Returns:**
- Verification results
- Git commit check
- File existence check
- Workspace activity check

**Use Case:**
```python
result = toolbelt.run("captain.verify_work", {
    "agent_id": "Agent-6",
    "work_description": "Refactored predictive_modeling_engine.py",
    "commit_hash": "1f6ecd433",
    "files_changed": [
        "src/automation/framework/predictive_modeling_engine.py",
        "src/automation/framework/predictive_modeling_forecasters.py",
        "src/automation/framework/predictive_modeling_metrics.py",
        "src/automation/framework/predictive_modeling_seasonality.py"
    ]
})

verification = result.output
# Checks: git commit exists, files exist, workspace active
```

**Why We Need This:** Agent-6's integrity report showed we need systematic verification. This combines all checks.

---

### **8. captain.cycle_report**

**Purpose:** Generate Captain's cycle activity report

**Parameters:**
- `cycle_number` (required): Current cycle number
- `missions_assigned` (optional): Number of missions assigned
- `messages_sent` (optional): Number of messages sent
- `agents_activated` (optional): List of activated agents
- `points_awarded` (optional): Total points awarded
- `notes` (optional): Additional cycle notes

**Returns:**
- Report file path
- Cycle metrics
- Report generation confirmation

**Use Case:**
```python
result = toolbelt.run("captain.cycle_report", {
    "cycle_number": 42,
    "missions_assigned": 5,
    "messages_sent": 8,
    "agents_activated": ["Agent-1", "Agent-3", "Agent-6"],
    "points_awarded": 9100,
    "notes": "Legendary session! 7 gas sources discovered!"
})

report_file = result.output["report_file"]
# Creates: agent_workspaces/Agent-4/CAPTAIN_CYCLE_42_*.md
```

**Why We Need This:** AGENTS.md requires Captain to update log every cycle. This automates Captain's Log creation.

---

### **9. captain.markov_optimize**

**Purpose:** Use Markov chain optimizer for ROI-based task selection

**Parameters:**
- `tasks` (required): List of tasks with ROI, time, points
- `agent_count` (optional): Number of available agents (default: 8)
- `time_budget` (optional): Time budget in minutes (default: 120)

**Returns:**
- Recommended task assignments
- Total tasks, time, points
- Average ROI
- Efficiency score

**Use Case:**
```python
tasks = [
    {"name": "Refactor A", "roi": 18.5, "time_estimate": 60, "points": 800},
    {"name": "Tooling B", "roi": 15.2, "time_estimate": 45, "points": 600},
    {"name": "Testing C", "roi": 12.0, "time_estimate": 90, "points": 400}
]

result = toolbelt.run("captain.markov_optimize", {
    "tasks": tasks,
    "time_budget": 120
})

recommended = result.output["recommended_tasks"]
# Optimizes for maximum ROI within time budget
```

**Why We Need This:** AGENTS.md requires Captain to use Markov + ROI optimizer for task selection. This interfaces with that system.

---

### **10. captain.integrity_check**

**Purpose:** Verify work claims with git history (Entry #025 compliance)

**Parameters:**
- `agent_id` (required): Agent claiming work
- `claimed_work` (required): Description of claimed work
- `search_terms` (optional): Git search terms

**Returns:**
- Git commits found
- Commit details
- Integrity verdict (VERIFIED / NO_EVIDENCE)
- Recommendation

**Use Case:**
```python
result = toolbelt.run("captain.integrity_check", {
    "agent_id": "Agent-6",
    "claimed_work": "Import Path Helper VSCode extension",
    "search_terms": ["Import Path Helper", "completionProvider", "importPathProvider"]
})

verdict = result.output["integrity_verdict"]
recommendation = result.output["recommendation"]
# Example: "NO_EVIDENCE" → "Request more evidence"
```

**Why We Need This:** Agent-6's integrity stance revealed need for systematic attribution checks. Entry #025 Integrity pillar requires verification.

---

## 🎯 **CAPTAIN'S CYCLE WORKFLOW**

### **Using the Tools in Captain's Duties:**

**1. PLANNING (15-30 min):**
```python
# Check agent status
status = toolbelt.run("captain.status_check", {"threshold_hours": 24})
idle_agents = status.output["idle_agents"]

# Optimize task selection
tasks = load_available_tasks()
optimized = toolbelt.run("captain.markov_optimize", {
    "tasks": tasks,
    "time_budget": 120
})
```

**2. TASK ASSIGNMENT (15-30 min):**
```python
# Calculate points for each task
for task in optimized.output["recommended_tasks"]:
    points = toolbelt.run("captain.calc_points", {
        "task_type": task["type"],
        "impact": task["impact"],
        "complexity": task["complexity"]
    })
    
    # Assign mission to agent
    toolbelt.run("captain.assign_mission", {
        "agent_id": task["assigned_agent"],
        "mission_title": task["name"],
        "mission_description": task["description"],
        "points": points.output["total_points"]
    })
```

**3. AGENT ACTIVATION (10-15 min) - CRITICAL!:**
```python
# Deliver gas to all agents with missions
for agent in agents_with_missions:
    toolbelt.run("captain.deliver_gas", {
        "agent_id": agent,
        "message": "🔥 CHECK INBOX + CLEAN WORKSPACE + START NOW!"
    })
```

**4. MONITORING (Ongoing):**
```python
# Check status throughout cycle
status_updates = toolbelt.run("captain.status_check", {})
```

**5. VERIFICATION (As work completes):**
```python
# Verify completed work
verification = toolbelt.run("captain.verify_work", {
    "agent_id": "Agent-6",
    "work_description": "Refactor complete",
    "commit_hash": "1f6ecd433",
    "files_changed": changed_files
})

# Integrity check if uncertain
integrity = toolbelt.run("captain.integrity_check", {
    "agent_id": "Agent-6",
    "claimed_work": "VSCode extensions",
    "search_terms": ["extension", "completionProvider"]
})
```

**6. REPORTING (15-20 min):**
```python
# Update leaderboard
toolbelt.run("captain.update_leaderboard", {
    "updates": session_points
})

# Generate cycle report
toolbelt.run("captain.cycle_report", {
    "cycle_number": current_cycle,
    "missions_assigned": len(missions),
    "messages_sent": len(messages),
    "agents_activated": activated_agents,
    "points_awarded": total_points
})
```

---

## 📊 **TOOLBELT STATISTICS**

### **Total Tools Available:**
- **Before:** 44 tools (23 original + 21 Agent-7's expansion)
- **After:** 54 tools (+10 Captain tools)
- **Growth:** +22.7% expansion

### **Captain Tools Category:**
- 10 specialized Captain operations tools
- Covers all Captain's cycle duties
- Enables automation of manual tasks

### **Tools by Category:**
```
Total: 54 tools across 11 categories

- captain: 10 tools (NEW!)
- oss: 5 tools
- brain: 5 tools
- msgtask: 3 tools
- obs: 4 tools
- val: 4 tools
- vector: 3 tools
- msg: 3 tools
- analysis: 3 tools
- v2: 2 tools
- agent: 2 tools
- test: 2 tools
- comp: 2 tools
- onboard: 2 tools
- docs: 2 tools
- health: 2 tools
```

---

## 🏆 **WHY THESE TOOLS MATTER**

### **Discovered Through Real Pain Points:**

1. **Status Check:** Agent-1 idle 34 days - UNDETECTED
2. **Git Verify:** Agent-6 integrity report - needed proof
3. **Points Calculator:** Captain manually calculating ROI constantly
4. **Mission Assign:** Standardize mission file format
5. **Gas Delivery:** "Prompts Are Gas" - activation automation
6. **Leaderboard Update:** Manual updates error-prone
7. **Work Verify:** Need systematic verification process
8. **Cycle Report:** AGENTS.md requires Captain's Log updates
9. **Markov Optimize:** Interface to existing optimizer
10. **Integrity Check:** Entry #025 compliance automation

**These aren't theoretical - they solve REAL problems from THIS SESSION!** 🎯

---

## 🚀 **NEXT CAPTAIN USAGE**

**How Next Captain Should Use These:**

1. **Start Every Cycle:** `captain.status_check` to find idle agents
2. **Plan Assignments:** `captain.markov_optimize` for task selection
3. **Calculate Points:** `captain.calc_points` for fair scoring
4. **Assign Work:** `captain.assign_mission` for structured orders
5. **Activate Agents:** `captain.deliver_gas` for fuel delivery
6. **Verify Work:** `captain.verify_work` + `captain.integrity_check`
7. **Update Scores:** `captain.update_leaderboard` each cycle
8. **Document:** `captain.cycle_report` for Captain's Log

**ONE TOOLBELT, INFINITE EFFICIENCY!** 🛠️

---

## 📝 **TOOL USAGE EXAMPLES**

### **Example 1: Complete Cycle Automation**

```python
from tools_v2.toolbelt_core import ToolbeltCore

toolbelt = ToolbeltCore()

# 1. Check for idle agents
status = toolbelt.run("captain.status_check", {
    "threshold_hours": 24
})

for idle_agent in status.output["idle_agents"]:
    print(f"⚠️ {idle_agent['agent']} idle for {idle_agent['hours_idle']} hours!")

# 2. Optimize task assignments
tasks = [
    {"name": "Refactor X", "roi": 18.5, "time_estimate": 60, "points": 800},
    {"name": "Tooling Y", "roi": 15.2, "time_estimate": 45, "points": 600}
]

optimized = toolbelt.run("captain.markov_optimize", {
    "tasks": tasks,
    "time_budget": 120
})

# 3. Assign missions
for task in optimized.output["recommended_tasks"]:
    toolbelt.run("captain.assign_mission", {
        "agent_id": task.get("agent", "Agent-1"),
        "mission_title": task["name"],
        "mission_description": task.get("description", "See task details"),
        "points": task["points"]
    })

# 4. Deliver gas!
for agent in ["Agent-1", "Agent-3", "Agent-6"]:
    toolbelt.run("captain.deliver_gas", {
        "agent_id": agent,
        "message": "🔥 CHECK INBOX + START NOW!"
    })
```

### **Example 2: Work Verification Pipeline**

```python
# Agent claims work - verify it!
agent_claim = {
    "agent_id": "Agent-6",
    "work": "Refactored predictive_modeling_engine.py",
    "commit": "1f6ecd433",
    "files": ["src/automation/framework/predictive_modeling_*.py"]
}

# Step 1: Verify git commit
git_check = toolbelt.run("captain.git_verify", {
    "commit_hash": agent_claim["commit"],
    "show_stat": True
})

if not git_check.success:
    print("❌ Git commit not found!")
else:
    # Step 2: Comprehensive work verification
    work_check = toolbelt.run("captain.verify_work", {
        "agent_id": agent_claim["agent_id"],
        "work_description": agent_claim["work"],
        "commit_hash": agent_claim["commit"],
        "files_changed": agent_claim["files"]
    })
    
    if work_check.output["verified"]:
        print("✅ Work VERIFIED!")
        
        # Step 3: Calculate and award points
        points = toolbelt.run("captain.calc_points", {
            "task_type": "refactor",
            "impact": "high",
            "complexity": "high"
        })
        
        # Step 4: Update leaderboard
        toolbelt.run("captain.update_leaderboard", {
            "updates": {
                agent_claim["agent_id"]: points.output["total_points"]
            }
        })
```

---

**Date:** October 13, 2025  
**Tools Created:** 10  
**Category:** captain  
**Purpose:** Automate Captain's cycle duties  
**Impact:** HIGH - Enables efficient swarm management  

🐝 **WE. ARE. SWARM.** ⚡🔥

**"54 tools. 11 categories. One efficient Captain."** 🏆✨

