# 🛠️ Agent Toolbelt V2 - Quick Start Guide

**Version**: 2.0.0  
**Created**: 2025-10-11  
**Author**: Agent-7 - Repository Cloning Specialist

---

## 🚀 ONE-MINUTE QUICK START

### **What is Agent Toolbelt V2?**
Unified CLI providing access to 23 agent tools through one consistent interface with **Vector DB intelligence** as the core feature.

### **Why use it?**
Instead of remembering 23 different CLI commands, use ONE:
```bash
python tools/agent_toolbelt.py <category> <action> [options]
```

---

## 🎯 MOST COMMON COMMANDS

### **1. Get Task Context** (MOST IMPORTANT - USE BEFORE EVERY TASK!)
```bash
# Get intelligent context from similar past work
python tools/agent_toolbelt.py vector context \
    --agent Agent-7 \
    --task "consolidate web files"

# Returns: similar tasks, related messages, devlog insights, recommendations
```

### **2. Send Message to Captain**
```bash
python tools/agent_toolbelt.py message \
    --agent Agent-4 \
    "Task complete, 100% V2 compliant"
```

### **3. Check V2 Compliance**
```bash
python tools/agent_toolbelt.py v2 check src/tools/
```

### **4. Run Project Scan**
```bash
python tools/agent_toolbelt.py analyze project
```

### **5. Index Your Work** (USE AFTER EVERY TASK!)
```bash
# Build collective intelligence
python tools/agent_toolbelt.py vector index \
    --agent Agent-7 \
    --file src/completed_work.py
```

---

## 📚 ALL 23 TOOLS

### **Vector DB** (3 tools - CORE FEATURE)
```bash
vector context --agent Agent-X --task "description"
vector search "query text" --limit 5
vector index --agent Agent-X --file path/to/file.py
```

### **Messaging** (3 tools)
```bash
message --agent Agent-X "message text" --priority urgent
message --broadcast "broadcast text"
message --inbox --agent Agent-X
```

### **Analysis** (3 tools)
```bash
analyze project
analyze complexity src/
analyze duplicates src/
```

### **V2 Compliance** (2 tools)
```bash
v2 check src/
v2 report --format json
```

### **Agent Operations** (2 tools)
```bash
agent status --agent Agent-X
agent claim-task --agent Agent-X
```

### **Testing** (2 tools)
```bash
test coverage --html
test mutation
```

### **Compliance** (2 tools)
```bash
comp history --days 7
comp check src/
```

### **Onboarding** (2 tools)
```bash
onboard soft --agent Agent-X --message "mission"
onboard hard --agent Agent-X --message "mission" --yes
```

### **Documentation** (2 tools)
```bash
docs search "V2 patterns" --agent Agent-X
docs export --agent Agent-X
```

### **Health** (2 tools)
```bash
health ping
health snapshot --update
```

---

## 🧠 VECTOR DB WORKFLOW (RECOMMENDED)

### **Enhanced Agent Cycle**

**BEFORE Every Task**:
```bash
# Step 1: Get intelligent context
python tools/agent_toolbelt.py vector context \
    --agent Agent-7 \
    --task "current task description"

# Step 2: Search for patterns
python tools/agent_toolbelt.py vector search "relevant keywords"
```

**DURING Task**:
```bash
# Use analysis tools as needed
python tools/agent_toolbelt.py v2 check src/
python tools/agent_toolbelt.py analyze complexity src/
```

**AFTER Task**:
```bash
# Step 1: Index your work
python tools/agent_toolbelt.py vector index \
    --agent Agent-7 \
    --file src/completed_file.py

# Step 2: Report completion
python tools/agent_toolbelt.py message \
    --agent Agent-4 \
    "Task complete"
```

**Benefit**: Build collective intelligence automatically!

---

## 💡 TIPS & TRICKS

### **Tip 1: Always Get Context First**
Before starting ANY task, run:
```bash
python tools/agent_toolbelt.py vector context --agent YOUR_ID --task "task description"
```
You'll see similar past work and recommendations!

### **Tip 2: Index Everything**
After completing work, index it:
```bash
python tools/agent_toolbelt.py vector index --agent YOUR_ID --file completed.py
```
Your work becomes searchable for future agents!

### **Tip 3: Search Before Building**
Before implementing, search if it exists:
```bash
python tools/agent_toolbelt.py vector search "what you want to build"
```

### **Tip 4: Use Aliases**
Create shell alias:
```bash
alias toolbelt="python tools/agent_toolbelt.py"
```
Then: `toolbelt vector context --agent Agent-7 --task "consolidation"`

---

## 🎓 LEARNING PATH

### **Day 1**: Master Vector DB
Learn the 3 vector commands (context, search, index) - these are CORE!

### **Day 2**: Master Messaging
Learn msg.send, msg.broadcast, msg.inbox

### **Day 3**: Master Analysis
Learn analyze project, v2 check, analyze complexity

### **Week 1+**: Explore Advanced
Discover testing, compliance, onboarding, docs, health tools

---

## 📖 MORE INFORMATION

- **Full Documentation**: `tools_v2/README.md`
- **Architecture Details**: `docs/AGENT_TOOLBELT.md`
- **Tool Documentation**: `AGENT_TOOLS_DOCUMENTATION.md`

---

**🐝 WE. ARE. SWARM. ⚡️🔥**

**Agent Toolbelt V2**: Your unified interface to swarm intelligence!  
**Start with**: `python tools/agent_toolbelt.py vector context --agent YOUR_ID --task "your task"`

