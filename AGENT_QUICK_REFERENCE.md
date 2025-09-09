# 🚀 **AGENT QUICK REFERENCE CARD**

**For:** All Swarm Agents  
**Purpose:** Quick access to essential tools and commands  
**Last Updated:** 2025-09-09

---

## 🔍 **PROJECT ANALYSIS (Most Used)**

### **Complete Project Scan:**
```bash
python tools/run_project_scan.py
```
**Output:** `project_analysis.json`, `chatgpt_project_context.json`

### **Chunked Analysis (Consolidation):**
```bash
python comprehensive_project_analyzer.py
```
**Output:** `analysis_chunks/` directory with 13 manageable chunks

### **Messaging System Analysis:**
```bash
python analyze_messaging_files.py
```
**Output:** `messaging_project_analysis.json`, `messaging_chatgpt_context.json`

---

## 🚀 **CONSOLIDATION TOOLS**

### **Configuration Management:**
```python
from src.core.unified_config import get_config
config = get_config()
```

### **Import Analysis:**
```python
from src.core.unified_import_system import analyze_imports
import_analysis = analyze_imports()
```

### **PyAutoGUI Messaging:**
```python
from src.services.messaging_pyautogui import PyAutoGUIMessagingDelivery
messaging = PyAutoGUIMessagingDelivery()
```

---

## 🧪 **TESTING & QUALITY**

### **Run All Tests:**
```bash
python -m pytest
```

### **Run with Coverage:**
```bash
python -m pytest --cov=src
```

### **Code Quality Analysis:**
```bash
python tools/duplication_analyzer.py
```

---

## 📊 **CONSOLIDATION CHUNKS**

| Chunk | Directory | Agent | Priority | Files | Target |
|-------|-----------|-------|----------|-------|--------|
| 001 | src/core | Agent-2 | CRITICAL | 50→15 | 70% |
| 002 | src/services | Agent-1 | CRITICAL | 50→20 | 60% |
| 003 | src/web | Agent-7 | MEDIUM | 50→30 | 40% |
| 004 | src/utils | Agent-3 | HIGH | 12→5 | 58% |
| 005 | src/infrastructure | Agent-3 | HIGH | 19→8 | 58% |

---

## 🎯 **AGENT ASSIGNMENTS**

- **Agent-1 (Integration):** Services consolidation, PyAutoGUI messaging
- **Agent-2 (Architecture):** Core modules, Project Scanner, Configuration
- **Agent-3 (DevOps):** Utils/Infrastructure, File management, Testing
- **Agent-4 (QA):** Domain-specific consolidation, Quality assurance
- **Agent-6 (Communication):** Documentation/Tools, Swarm coordination
- **Agent-7 (Web Development):** Web interface consolidation

---

## 📁 **KEY FILES**

### **Analysis Results:**
- `project_analysis.json` - Complete project analysis
- `chatgpt_project_context.json` - AI-ready context
- `analysis_chunks/` - Chunked analysis results

### **Consolidation Planning:**
- `CONSOLIDATION_ACTION_PLAN.md` - Implementation plan
- `COMPREHENSIVE_CHUNKED_ANALYSIS_SUMMARY.md` - Analysis summary
- `swarm_debate_consolidation.xml` - Swarm debate

### **Documentation:**
- `AGENT_TOOLS_DOCUMENTATION.md` - Complete tool documentation
- `AGENTS.md` - Agent guidelines and policies

---

## 🚨 **EMERGENCY COMMANDS**

### **Check Project Status:**
```bash
python tools/run_project_scan.py
```

### **Validate Consolidation:**
```bash
python -m pytest
```

### **Backup Current State:**
```bash
python src/utils/backup.py
```

---

## 📞 **SWARM COORDINATION**

### **Debate Participation:**
- Review `swarm_debate_consolidation.xml`
- Add arguments via PyAutoGUI messaging
- Update task progress in markdown files

### **Progress Reporting:**
- Update `CONSOLIDATION_ACTION_PLAN.md`
- Report via PyAutoGUI messaging
- Document changes in appropriate files

---

**🐝 WE ARE SWARM - Quick reference ready for all agents!**

Keep this reference handy for immediate access to essential tools and commands during consolidation efforts.
