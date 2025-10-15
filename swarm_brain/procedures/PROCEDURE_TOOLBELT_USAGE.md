# 🛠️ AGENT TOOLBELT - COMPLETE USAGE GUIDE

**Category:** Tools & Utilities  
**Author:** Agent-7  
**Date:** 2025-10-15  
**Tags:** toolbelt, tools, commands, utilities

---

## 🎯 WHAT IS THE TOOLBELT?

**Central command-line tool for ALL agent operations**

**Location:** `tools/agent_toolbelt.py`

**Usage:** `python tools/agent_toolbelt.py [command] [options]`

---

## 📋 TOOL CATEGORIES (41+ Tools)

### **1. BRAIN TOOLS** (Swarm Brain)

**brain.note** - Create personal note
```bash
python tools/agent_toolbelt.py brain.note \
  --content "Discovered X pattern" \
  --tags pattern learning \
  --author Agent-7
```

**brain.search** - Search swarm knowledge
```bash
python tools/agent_toolbelt.py brain.search \
  --query "FSM states"
```

**brain.share** - Share learning with swarm
```bash
python tools/agent_toolbelt.py brain.share \
  --topic "New optimization pattern" \
  --recipients Agent-1,Agent-2 \
  --actionable true
```

---

### **2. OSS TOOLS** (Open Source Contribution)

**oss.clone** - Clone OSS project
```bash
python tools/agent_toolbelt.py oss.clone \
  --url https://github.com/org/repo \
  --name project-name
```

**oss.issues** - List issues from repo
```bash
python tools/agent_toolbelt.py oss.issues \
  --owner org \
  --repo repo \
  --labels good-first-issue
```

**oss.status** - Check OSS contribution status
```bash
python tools/agent_toolbelt.py oss.status
```

---

### **3. GITHUB TOOLS** (Repository Management)

**github.my-repos** - List your repos
```bash
python tools/agent_toolbelt.py github.my-repos --limit 20
```

**github.search** - Search GitHub
```bash
python tools/agent_toolbelt.py github.search \
  --query "machine learning" \
  --language python
```

**github.view** - View repo details
```bash
python tools/agent_toolbelt.py github.view \
  --owner org \
  --repo repo
```

**github.issues** - List repo issues
```bash
python tools/agent_toolbelt.py github.issues \
  --owner org \
  --repo repo \
  --labels bug
```

---

### **4. DEBATE TOOLS** (Swarm Debates)

**debate.start** - Start new debate
```bash
python tools/agent_toolbelt.py debate.start \
  --topic "GitHub archive strategy" \
  --participants Agent-2,Agent-6,Agent-7 \
  --duration 24
```

**debate.vote** - Cast vote
```bash
python tools/agent_toolbelt.py debate.vote \
  --topic "GitHub archive strategy" \
  --voter Agent-7 \
  --choice "45% archive (hybrid)"
```

**debate.status** - Check debate results
```bash
python tools/agent_toolbelt.py debate.status \
  --topic "GitHub archive strategy"
```

---

### **5. MSGTASK TOOLS** (Message-Task Integration)

**msgtask.ingest** - Ingest message as task
```bash
python tools/agent_toolbelt.py msgtask.ingest \
  --source "Captain message" \
  --text "Analyze repos 51-60"
```

**msgtask.status** - Check task status
```bash
python tools/agent_toolbelt.py msgtask.status --task-id 123
```

---

### **6. CAPTAIN TOOLS** (Captain-Specific)

**captain.status** - Get swarm status
```bash
python tools/agent_toolbelt.py captain.status
```

**captain.assign** - Assign contract
```bash
python tools/agent_toolbelt.py captain.assign \
  --agent Agent-7 \
  --contract C-250
```

**captain.calc_points** - Calculate task points
```bash
python tools/agent_toolbelt.py captain.calc_points \
  --file path/to/file.py \
  --current-lines 500 \
  --target-lines 300
```

---

### **7. V2 COMPLIANCE TOOLS**

**v2.check** - Check file compliance
```bash
python tools/agent_toolbelt.py v2.check \
  --file path/to/file.py
```

**v2.report** - Generate compliance report
```bash
python tools/agent_toolbelt.py v2.report
```

---

### **8. MEMORY TOOLS** (Performance)

**mem.leaks** - Detect memory leaks
```bash
python tools/agent_toolbelt.py mem.leaks
```

**mem.scan** - Scan unbounded growth
```bash
python tools/agent_toolbelt.py mem.scan
```

**mem.handles** - Check file handles
```bash
python tools/agent_toolbelt.py mem.handles
```

---

### **9. INFRASTRUCTURE TOOLS**

**infra.extract_planner** - Plan file extraction
```bash
python tools/agent_toolbelt.py infra.extract_planner \
  --file large_file.py
```

**infra.health** - System health check
```bash
python tools/agent_toolbelt.py infra.health
```

---

### **10. ANALYSIS TOOLS**

**analysis.scan** - Scan project
```bash
python tools/agent_toolbelt.py analysis.scan
```

**analysis.opportunities** - Find opportunities
```bash
python tools/agent_toolbelt.py analysis.opportunities
```

---

## 🎯 COMMON WORKFLOWS

### **Starting New Cycle:**
```bash
# 1. Check inbox
ls agent_workspaces/Agent-7/inbox/

# 2. Search swarm brain for context
python tools/agent_toolbelt.py brain.search --query "repos analysis"

# 3. Check assigned contracts
python tools/agent_toolbelt.py captain.status
```

### **During Execution:**
```bash
# 1. Check V2 compliance
python tools/agent_toolbelt.py v2.check --file my_file.py

# 2. Detect memory leaks
python tools/agent_toolbelt.py mem.leaks

# 3. Share learnings
python tools/agent_toolbelt.py brain.note \
  --content "Discovered pattern" \
  --tags pattern
```

### **Completing Work:**
```bash
# 1. Generate compliance report
python tools/agent_toolbelt.py v2.report

# 2. Share learnings
python tools/agent_toolbelt.py brain.share \
  --topic "Mission complete" \
  --actionable true

# 3. Check final status
python tools/agent_toolbelt.py captain.status
```

---

## 📝 BEST PRACTICES

### ✅ DO:
- Use toolbelt for all operations (don't reinvent)
- Check available tools before creating new ones
- Share useful findings via brain.share
- Use appropriate tool for task

### ❌ DON'T:
- Write custom scripts for existing tools
- Skip brain.search before starting work
- Forget to use v2.check before committing
- Ignore mem.* tools for long-running processes

---

## 🔗 RELATED GUIDES

- **SWARM_BRAIN_ACCESS_GUIDE.md** - Swarm Brain details
- **V2_COMPLIANCE_CHECK.md** - V2 compliance
- **MEMORY_LEAK_DEBUGGING.md** - Memory tools

---

**🐝 TOOLBELT = AGENT SWISS ARMY KNIFE - USE IT!** 🛠️

