# 🐝 AGENT ORIENTATION - QUICK REFERENCE

**Single page. Everything you need. 5 minutes.**

---

## 🚀 **INSTANT START (30 SECONDS)**

```bash
# Your first command
python tools/agent_orient.py quick

# Find anything
python tools/agent_orient.py search "keyword"
```

---

## 📋 **YOUR WORKFLOW**

### **1. Check Your Mission**
```bash
# Read your inbox
cat agent_workspaces/Agent-X/inbox/*.md
```

### **2. Find Tools You Need**
```bash
# Discover tools
python tools/agent_orient.py tools

# Search for specific tool
python tools/agent_orient.py search "testing"
```

### **3. Execute Mission**
- Use discovered tools
- Follow mission instructions
- Check V2 compliance (<400 lines, type hints, tests)

### **4. Report Completion**
```bash
# Update status
# Edit: agent_workspaces/Agent-X/status.json

# Create devlog
# Create: devlogs/YYYY-MM-DD_Agent-X_summary.md
```

---

## 🗂️ **PROJECT MAP**

### **Core Systems:**
- `src/core/` - Core engines & functionality
- `src/services/` - Business logic
- `src/web/` - Frontend & API
- `src/domain/` - Domain models

### **Agent Tools:**
- `tools/` - Utility scripts
- `tools_v2/` - Toolbelt system
- `swarm_brain/` - Knowledge base

### **Your Workspace:**
- `agent_workspaces/Agent-X/` - Your files
- `inbox/` - Mission assignments
- `status.json` - Your status
- `passdown.json` - Session handoff

---

## 🛠️ **TOP 10 TOOLS**

| Tool | Usage | Purpose |
|------|-------|---------|
| **analysis.scan** | Scan project | Find violations |
| **test.coverage** | Run tests | Check coverage |
| **v2.check** | Check V2 | Compliance verification |
| **captain.status** | Swarm status | Agent health |
| **brain.search** | Search knowledge | Find docs |
| **proposal.view** | View proposals | Democratic process |
| **agent.orient** | This tool! | Quick reference |
| **obs.metrics** | Metrics | Observability |
| **val.smoke** | Smoke tests | Quick validation |
| **session.passdown** | Handoff | Session transfer |

**Full list:** `cat AGENT_TOOLS_DOCUMENTATION.md`

---

## 🚨 **EMERGENCY**

### **I'm Stuck!**
```bash
# 1. Search for help
python tools/agent_orient.py search "your problem"

# 2. Check swarm brain
python -m swarm_brain.search "your problem"

# 3. Contact Captain
# Message Agent-4 via messaging system
```

### **Common Issues:**

**Import Error?**
```bash
# Check Python path
python -c "import sys; print(sys.path)"
```

**Test Failing?**
```bash
# Run with verbose
pytest -v tests/
```

**V2 Violation?**
```bash
# Check violations
python tools/run_project_scan.py --violations-only
```

---

## 📚 **KEY DOCUMENTATION**

### **Essential Reading (5 min):**
1. `AGENTS.md` - Swarm information
2. `AGENT_TOOLS_DOCUMENTATION.md` - All tools
3. `README.md` - Project overview

### **When You Need More:**
- `docs/guides/` - Detailed guides
- `swarm_brain/` - Knowledge repository
- `agent_workspaces/Agent-4/captain_handbook/` - Captain's handbook

---

## 🎯 **MISSION TYPES**

### **V2 Compliance:**
- Fix file >400 lines
- Add type hints
- Write tests (85%+ coverage)
- Check: `python tools/v2_compliance_checker.py`

### **Testing:**
- Write unit tests
- Achieve coverage target
- Run: `pytest tests/`

### **Documentation:**
- Update docs
- Add examples
- Check: `grep -r "TODO" docs/`

### **Refactoring:**
- Reduce complexity
- Extract modules
- Maintain functionality

---

## ✅ **V2 COMPLIANCE CHECKLIST**

Every file must:
- [ ] ≤400 lines
- [ ] 100% type hints
- [ ] Comprehensive docstrings
- [ ] Tests (85%+ coverage)
- [ ] No circular imports
- [ ] Clean linting

---

## 🔄 **TYPICAL CYCLE**

**Morning:**
1. Check inbox for mission
2. Orient using this tool
3. Find tools needed
4. Start execution

**During:**
5. Code following V2 standards
6. Test as you go
7. Update status.json

**Evening:**
8. Complete deliverables
9. Create devlog
10. Update passdown.json

---

## 💡 **PRO TIPS**

- **Bookmark:** `python tools/agent_orient.py`
- **Search first:** Before asking, search
- **Test always:** Tests = validation
- **V2 always:** <400 lines, types, tests
- **Document:** Future you will thank you

---

## 🐝 **SWARM PRINCIPLES**

- **Autonomy:** Work independently when possible
- **Coordination:** Collaborate when needed
- **Quality:** V2 compliance non-negotiable
- **Communication:** Update status, write devlogs
- **Learning:** Share knowledge via Swarm Brain

---

**WE. ARE. SWARM.** ⚡

**Now go check your inbox and start your mission!** 🚀

---

*Quick reference tool: `python tools/agent_orient.py`*  
*Full docs: `AGENT_TOOLS_DOCUMENTATION.md`*

