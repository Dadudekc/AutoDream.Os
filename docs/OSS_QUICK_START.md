# Open Source Contributions - Quick Start Guide

**Get the swarm contributing to OSS projects in 5 minutes!**

---

## 🚀 **Setup (One Time)**

### **1. Initialize System**

```bash
python src/opensource/setup_oss.py
```

**Creates:**
- `D:\OpenSource_Swarm_Projects\` directory
- Project registry
- Portfolio tracking
- Initial README

---

## 💻 **Basic Usage**

### **Clone OSS Project**

```bash
python -m src.opensource.oss_cli clone https://github.com/pytest-dev/pytest

# Output:
# ✅ Project cloned: oss-abc123
# Location: D:\OpenSource_Swarm_Projects\pytest
```

### **Fetch Good First Issues**

```bash
python -m src.opensource.oss_cli issues oss-abc123 --labels "good first issue"

# Shows available issues ready for contribution
```

### **Import as Tasks**

```bash
python -m src.opensource.oss_cli issues oss-abc123 --import-tasks

# Imports issues into swarm task system
# Agents can now claim via --get-next-task
```

### **Agent Works on Task**

```bash
# Agent claims:
python -m src.services.messaging_cli --get-next-task

# Agent sees:
# 🎯 TASK CLAIMED: [OSS] Improve fixture cleanup
# Project: pytest
# Issue: #1234

# Agent executes, commits, pushes
```

### **Submit PR**

```bash
python -m src.opensource.oss_cli pr oss-abc123 \
  --title "Fix: Improve fixture cleanup" \
  --description "Implemented cleanup improvements per issue #1234" \
  --agents Agent-2 Agent-8

# Output:
# ✅ PR created: https://github.com/pytest-dev/pytest/pull/5678
```

### **View Portfolio**

```bash
python -m src.opensource.oss_cli portfolio --format html

# Opens portfolio dashboard showing all contributions
```

---

## 🎯 **Workflow Example**

### **Complete Contribution Flow:**

```bash
# 1. Clone target project
python -m src.opensource.oss_cli clone https://github.com/requests/requests

# 2. Fetch issues
python -m src.opensource.oss_cli issues oss-xyz789 --labels "good first issue" --import-tasks

# 3. Agent claims task
python -m src.services.messaging_cli --get-next-task

# 4. Agent works in: D:\OpenSource_Swarm_Projects\requests\
#    - Analyzes issue
#    - Implements fix
#    - Writes tests
#    - Commits changes

# 5. Submit PR
python -m src.opensource.oss_cli pr oss-xyz789 \
  --title "Fix: Add timeout validation" \
  --description "Added validation for timeout parameter per issue #123" \
  --agents Agent-2

# 6. PR gets merged ✅

# 7. Update portfolio
python -m src.opensource.oss_cli portfolio --format html

# 8. Portfolio shows: 1 project, 1 merged PR, reputation +10!
```

---

## 📋 **Message Format for OSS Tasks**

### **Via Captain Message:**

```
TASK: Contribute to pytest
DESC: Find and fix good first issue in pytest testing framework
PROJECT: https://github.com/pytest-dev/pytest
PRIORITY: P1
ASSIGNEE: Agent-2
TAGS: oss, python, testing
```

**System will:**
1. Clone project automatically
2. Fetch issues
3. Create tasks
4. Assign to agent
5. Track contribution

---

## 🏆 **Target Projects (Suggestions)**

### **Python (Swarm's Strength)**

- **pytest** - Testing framework (good first issues available)
- **requests** - HTTP library (well-maintained)
- **click** - CLI framework (documentation needs)
- **pydantic** - Validation (testing opportunities)
- **flask** - Web framework (enhancement opportunities)

### **JavaScript (Agent-7 Specialty)**

- **jest** - Testing framework
- **prettier** - Code formatter
- **eslint** - Linting tool

### **Documentation (Agent-8 Specialty)**

- **freeCodeCamp** - Learning platform
- **MDN Web Docs** - Web documentation
- **Various project docs** - README improvements

---

## 📊 **Portfolio Tracking**

### **View Status:**

```bash
python -m src.opensource.oss_cli status

# Shows:
# - Total projects
# - PRs submitted/merged
# - Reputation score
# - Agent contributions
```

### **Generate Portfolio:**

```bash
# Markdown (for GitHub)
python -m src.opensource.oss_cli portfolio --format markdown

# HTML (interactive dashboard)
python -m src.opensource.oss_cli portfolio --format html

# JSON (for analysis)
python -m src.opensource.oss_cli portfolio --format json
```

---

## 🎯 **Best Practices**

### **Before Contributing:**

✅ **Read CONTRIBUTING.md** in target project  
✅ **Check code style** requirements  
✅ **Run existing tests** to ensure they pass  
✅ **Create feature branch** for your work  

### **During Contribution:**

✅ **Write tests** for all new code  
✅ **Update documentation** as needed  
✅ **Follow project conventions**  
✅ **Keep changes focused** (one issue per PR)  

### **After Contribution:**

✅ **Add swarm signature** to PR  
✅ **Log contribution** in tracker  
✅ **Update portfolio**  
✅ **Monitor PR status**  

---

## 🚦 **Quality Standards**

**Every swarm contribution:**

✅ **Passes all existing tests**  
✅ **Adds tests for new code**  
✅ **Updates documentation**  
✅ **Follows project style guide**  
✅ **Includes swarm signature**  
✅ **Multi-agent review** before submission  

---

## 📞 **Commands Reference**

```bash
# Setup
python src/opensource/setup_oss.py

# Clone project
python -m src.opensource.oss_cli clone <url>

# List projects
python -m src.opensource.oss_cli list

# Fetch issues
python -m src.opensource.oss_cli issues <project-id> --labels "good first issue"

# Import as tasks
python -m src.opensource.oss_cli issues <project-id> --import-tasks

# Check status
python -m src.opensource.oss_cli status

# Generate portfolio
python -m src.opensource.oss_cli portfolio --format html

# Submit PR
python -m src.opensource.oss_cli pr <project-id> --title "..." --description "..." --agents Agent-X
```

---

**🐝 Ready to join the OSS community!**

**Start with:** `python src/opensource/setup_oss.py` (if not done)  
**Then:** Clone your first project and start contributing!

**WE ARE SWARM - Now contributing to the world! 🌍⚡️🔥**

