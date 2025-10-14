# 🛠️ Agent Toolbelt - Agent-3 New Tools Quick Reference

**Added By**: Agent-3 (Infrastructure & DevOps)  
**Date**: 2025-10-12  
**New Tools**: 7 (4 infrastructure + 3 Discord)

---

## 🏗️ INFRASTRUCTURE TOOLS

### **1. infra.orchestrator_scan**
**Scan all orchestrators for violations**

```bash
python tools/agent_toolbelt.py infra orchestrator_scan
```

**Output:**
- Total orchestrators found
- V2 violations by severity
- Top 10 largest files
- Performance bottleneck identification

**Use When**: Need quick infrastructure health check

---

### **2. infra.file_lines**
**Count lines in files for V2 compliance**

```bash
python tools/agent_toolbelt.py infra file_lines --files file1.py file2.py file3.py
```

**Output:**
- Line count per file
- V2 compliance status (✅/❌)
- Buffer to 400-line limit
- Over-limit amount

**Use When**: Checking V2 compliance quickly

---

### **3. infra.extract_planner**
**Plan module extraction for refactoring**

```bash
python tools/agent_toolbelt.py infra extract_planner --file path/to/large_file.py
```

**Output:**
- File metrics (lines, classes, functions)
- List of classes and functions
- Extraction suggestions
- Recommended groupings

**Use When**: Planning a refactoring task

---

### **4. infra.roi_calc**
**Calculate ROI for tasks**

```bash
python tools/agent_toolbelt.py infra roi_calc \
  --points 500 \
  --complexity 24 \
  --v2-impact 1 \
  --autonomy-impact 1
```

**Output:**
- ROI score
- Reward/difficulty breakdown
- Rating (EXCELLENT/GOOD/FAIR/LOW)

**Use When**: Evaluating task priority

---

## 🤖 DISCORD TOOLS

### **5. discord.health**
**Check Discord Commander bot status**

```bash
python tools/agent_toolbelt.py discord health
```

**Output:**
- Bot running status
- Logs availability
- Health status

**Use When**: Verify Discord bot is operational

---

### **6. discord.start**
**Start Discord Commander bot**

```bash
python tools/agent_toolbelt.py discord start
```

**Output:**
- Startup confirmation
- Usage instructions

**Use When**: Need to launch Discord bot quickly

---

### **7. discord.test**
**Test Discord messaging pipeline**

```bash
python tools/agent_toolbelt.py discord test --agent Agent-1 --message "Test"
```

**Output:**
- Message delivery status
- PyAutoGUI confirmation
- Output preview

**Use When**: Testing Discord integration

---

## 📋 COMMON WORKFLOWS

### **Infrastructure Health Check:**
```bash
# 1. Scan orchestrators
python tools/agent_toolbelt.py infra orchestrator_scan

# 2. Check specific files
python tools/agent_toolbelt.py infra file_lines --files src/core/orchestration/*.py

# 3. Plan extraction if needed
python tools/agent_toolbelt.py infra extract_planner --file violating_file.py
```

### **Task Prioritization:**
```bash
# Calculate ROI for multiple tasks
python tools/agent_toolbelt.py infra roi_calc --points 500 --complexity 24
python tools/agent_toolbelt.py infra roi_calc --points 1000 --complexity 61

# Choose highest ROI
```

### **Discord Management:**
```bash
# 1. Check if running
python tools/agent_toolbelt.py discord health

# 2. Start if needed
python tools/agent_toolbelt.py discord start

# 3. Test messaging
python tools/agent_toolbelt.py discord test --agent Agent-4 --message "Bot check"
```

---

## 🎯 WHY THESE TOOLS?

**Created from actual needs during Agent-3 session:**

- ✅ **orchestrator_scan**: Needed to find infrastructure violations quickly
- ✅ **file_lines**: Constantly checking V2 compliance
- ✅ **extract_planner**: Planning refactorings took time without this
- ✅ **roi_calc**: Evaluating task value like Markov optimizer
- ✅ **discord.health**: Verify bot without checking Discord
- ✅ **discord.start**: Quick bot startup
- ✅ **discord.test**: Test messaging pipeline end-to-end

---

## 🐝 BENEFIT TO SWARM

**All 8 agents can now:**
- Scan infrastructure violations in seconds
- Verify V2 compliance instantly
- Plan refactorings with data
- Calculate task ROI themselves
- Manage Discord Commander via CLI
- Test Discord integration quickly

**Infrastructure tools available to entire swarm!** 🚀

---

**🐝 WE. ARE. SWARM. - 7 New Tools Ready!** ⚡🔥

