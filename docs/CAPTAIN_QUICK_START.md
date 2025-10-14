# Captain Quick Start - New Systems Guide

**Get started with message-task loop and OSS contributions in 2 minutes**

---

## 🚀 **1. Initialize Systems (One Time)**

```bash
# Install and setup
make init

# Verify working
make smoke
```

---

## 📨 **2. Use Message → Task Loop**

### **Send Task via Message (Any Format)**

**Structured:**
```
TASK: Implement feature X
DESC: Add functionality with tests
PRIORITY: P1
ASSIGNEE: Agent-2
```

**Natural language:**
```
Please fix the authentication bug urgently, assign to @Agent-3
```

**Minimal:**
```
todo: fix auth bug
```

### **Agent Claims**

```bash
python -m src.services.messaging_cli --get-next-task

# Agent sees task and executes automatically
```

**Result:** Infinite autonomous loop! Agents keep working. ♾️

---

## 🌍 **3. Start OSS Contributions**

### **Clone Target Project**

```bash
python -m src.opensource.oss_cli clone https://github.com/pytest-dev/pytest
```

### **Import Issues as Tasks**

```bash
python -m src.opensource.oss_cli issues oss-abc123 \
  --labels "good first issue" \
  --import-tasks

# Creates tasks from GitHub issues
# Agents can claim via --get-next-task
```

### **View Portfolio**

```bash
python -m src.opensource.oss_cli portfolio --format html

# Opens: D:\OpenSource_Swarm_Projects\portfolio.html
```

---

## 📊 **4. Monitor Systems**

```bash
# Overall status
make status

# Current metrics
make metrics

# Smoke test health
make smoke
```

---

## 🎯 **Common Tasks**

### **Send Work to Agents**

```bash
# Via message (auto-creates task)
# Just send message in any format above
# System handles the rest!
```

### **Check Agent Progress**

```bash
# List tasks
python -m src.services.messaging_cli --list-tasks

# View portfolio
python -m src.opensource.oss_cli list
```

### **Emergency Stop**

```bash
# Disable features
export FF_MSG_TASK=off
export FF_OSS_CLI=off

# Or
make rollback
```

---

## 📋 **Daily Workflow**

```bash
# Morning: Check status
make status

# Send work via messages
# (Format: TASK: ... PRIORITY: ... ASSIGNEE: ...)

# Agents claim and execute autonomously

# Evening: Review portfolio
python -m src.opensource.oss_cli portfolio --format html

# Check metrics
make metrics
```

---

## 🏆 **Key Features**

✅ **Autonomous Loop** - Messages → Tasks → Execution → Reports → Loop ♾️  
✅ **3-Tier Parsing** - Structured/AI/Regex (100% success)  
✅ **Deduplication** - Zero duplicate tasks  
✅ **OSS Contributions** - Build community recognition  
✅ **Full Tracking** - Metrics, portfolio, FSM states  

---

## 🐝 **That's It!**

**Three commands to remember:**

1. `make init` - Setup (one time)
2. `make status` - Check health
3. Just send messages - system handles the rest!

**The swarm is autonomous - you just coordinate!** 🚀

---

**Questions? Check:**
- `docs/MESSAGE_TASK_INTEGRATION.md` - Full architecture
- `docs/OPEN_SOURCE_CONTRIBUTIONS.md` - OSS guide
- `docs/OPERATOR_RUNBOOK.md` - Operations reference


