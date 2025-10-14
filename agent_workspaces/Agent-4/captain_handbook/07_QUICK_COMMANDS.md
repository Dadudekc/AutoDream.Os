# ⚡ CHAPTER 07: QUICK COMMANDS

**Read Time:** 3 minutes  
**Priority:** 🟡 HIGH

---

## 🚀 **INSTANT COMMAND REFERENCE**

Copy-paste these commands for common Captain tasks.

---

## 📊 **ANALYSIS & PLANNING**

### **Run Project Scanner**
```bash
python tools/run_project_scan.py
```

### **Run ROI Optimizer**
```bash
python tools/markov_8agent_roi_optimizer.py
```

### **Scan Technical Debt**
```bash
python tools/scan_technical_debt.py
```

### **Check Violations**
```bash
grep -r "VIOLATION\|TODO\|FIXME" src/
```

---

## 📢 **MESSAGING COMMANDS**

### **Activate Single Agent**
```bash
python -m src.services.messaging_cli \
  --agent Agent-X \
  --message "🎯 URGENT: Check INBOX! Mission assigned. BEGIN NOW!" \
  --sender "Captain Agent-4" \
  --priority urgent
```

### **Activate ALL Agents (Bulk)**
```bash
python -m src.services.messaging_cli \
  --bulk \
  --message "🚀 NEW CYCLE: Check INBOX for assignments! BEGIN NOW!" \
  --sender "Captain Agent-4" \
  --priority urgent
```

### **Status Check Message**
```bash
python -m src.services.messaging_cli \
  --bulk \
  --message "📊 STATUS CHECK: Provide progress update on current task" \
  --sender "Captain Agent-4" \
  --priority high
```

### **Emergency Broadcast**
```bash
python -m src.services.messaging_cli \
  --bulk \
  --message "🚨 EMERGENCY: Check inbox for critical protocol!" \
  --sender "Captain Agent-4" \
  --priority urgent
```

---

## 👁️ **MONITORING COMMANDS**

### **Check All Agent Statuses**
```bash
cat agent_workspaces/Agent-*/status.json
```

### **Check Single Agent Status**
```bash
cat agent_workspaces/Agent-X/status.json
```

### **Find Idle Agents**
```bash
python tools/captain_find_idle_agents.py
```

### **Check Agent Progress**
```bash
python tools/captain_check_agent_status.py
```

### **Find Completed Tasks**
```bash
grep -r "#DONE-C" agent_workspaces/
```

### **Check Message History**
```bash
python -m src.services.messaging_cli --history
```

---

## 📋 **TASK MANAGEMENT**

### **Get Next Available Task**
```bash
python -m src.services.messaging_cli --get-next-task
```

### **Check Contract Status**
```bash
python -m src.services.messaging_cli --check-contracts
```

### **Assign Contract to Agent**
```bash
python -m src.services.messaging_cli \
  --agent Agent-X \
  --get-next-task \
  --sender "Captain Agent-4"
```

---

## 🏆 **LEADERBOARD & METRICS**

### **Update Leaderboard**
```bash
python tools/captain_leaderboard_update.py
```

### **Check GAS Status**
```bash
python tools/captain_gas_check.py
```

### **Calculate ROI**
```bash
python tools/captain_roi_quick_calc.py
```

### **Pick Next Task**
```bash
python tools/captain_next_task_picker.py
```

---

## 🛠️ **COORDINATE MANAGEMENT**

### **Capture Coordinates (Interactive)**
```bash
python scripts/capture_coordinates.py
```

### **Validate Coordinates**
```bash
python scripts/validate_workspace_coords.py
```

### **View Coordinates**
```bash
python -m src.services.messaging_cli --coordinates
```

### **List All Agents**
```bash
python -m src.services.messaging_cli --list-agents
```

---

## 🚨 **EMERGENCY PROTOCOLS**

### **Code Red (System Failure)**
```bash
python -m src.services.messaging_cli \
  --bulk \
  --message "🚨 CODE RED: System failure. Check inbox for emergency protocol!" \
  --sender "Captain Agent-4" \
  --priority urgent
```

### **Code Black (Coordinate Failure)**
```bash
python -m src.services.messaging_cli \
  --bulk \
  --message "🚨 CODE BLACK: Coordinate system down. Switch to inbox-only mode!" \
  --sender "Captain Agent-4" \
  --priority urgent
```

### **Mission Abort**
```bash
python -m src.services.messaging_cli \
  --bulk \
  --message "🚨 MISSION ABORT: Cease all operations immediately!" \
  --sender "Captain Agent-4" \
  --priority urgent
```

---

## 📝 **LOG & DOCUMENTATION**

### **Update Captain's Log**
```bash
python tools/captain_update_log.py
```

### **View Recent Logs**
```bash
tail -f logs/messaging.log
tail -f logs/captain.log
tail -f logs/pyautogui.log
```

### **Self-Message (Captain Note)**
```bash
python tools/captain_self_message.py "Note: [your note here]"
```

---

## 🔍 **DIAGNOSTIC COMMANDS**

### **Check System Status**
```bash
python -m src.services.messaging_cli --check-status
```

### **Test Messaging System**
```bash
python -m src.services.messaging_cli --list-agents
```

### **Verify PyAutoGUI**
```bash
python -c "import pyautogui; print(pyautogui.size())"
```

### **Check Python Path**
```bash
python -c "import sys; print(sys.path)"
```

---

## 📂 **FILE OPERATIONS**

### **View Inbox**
```bash
ls -la agent_workspaces/Agent-X/inbox/
```

### **Read Execution Order**
```bash
cat agent_workspaces/Agent-X/inbox/EXECUTION_ORDER_CXXX.md
```

### **Check Passdown**
```bash
cat agent_workspaces/Agent-X/passdown.json
```

### **View Recent Devlogs**
```bash
ls -lt devlogs/ | head -10
```

---

## 🧪 **TESTING COMMANDS**

### **Run All Tests**
```bash
pytest tests/
```

### **Run Specific Test**
```bash
pytest tests/test_messaging.py
```

### **Check Test Coverage**
```bash
pytest --cov=src tests/
```

### **Run Linter**
```bash
pre-commit run --all-files
```

---

## 🎯 **QUICK AGENT REFERENCE**

### **Agent Positions:**
```
Monitor 1 (Left):          Monitor 2 (Right):
Agent-1: (-1269, 481)      Agent-5: (652, 421)
Agent-2: (-308, 480)       Agent-6: (1612, 419)
Agent-3: (-1269, 1001)     Agent-7: (698, 936)
Agent-4: (-308, 1000)      Agent-8: (1611, 941)
        (CAPTAIN)
```

### **Agent Specializations:**
- **Agent-1:** Integration & Core Systems
- **Agent-2:** Architecture & Design
- **Agent-3:** Infrastructure & DevOps
- **Agent-4:** Captain - Strategic Oversight
- **Agent-5:** Business Intelligence
- **Agent-6:** Coordination & Communication
- **Agent-7:** Web Development & Frontend
- **Agent-8:** SSOT & System Integration

---

## 📋 **COMMAND TEMPLATE BUILDER**

### **Build Custom Message:**
```bash
python -m src.services.messaging_cli \
  --agent [Agent-1|Agent-2|...|Agent-8|--bulk] \
  --message "[YOUR MESSAGE]" \
  --sender "Captain Agent-4" \
  --priority [regular|high|urgent] \
  --type [captain_to_agent|system_to_agent|broadcast]
```

---

## 🔖 **BOOKMARKS**

**Most Used (Daily):**
1. Activate all agents (bulk messaging)
2. Check all agent statuses
3. Run project scanner
4. Update leaderboard

**Common (Weekly):**
1. Run ROI optimizer
2. Scan technical debt
3. Check message history
4. Update Captain's log

**Rare (As Needed):**
1. Emergency protocols
2. Coordinate capture
3. System diagnostics
4. Test messaging system

---

**🎯 BOOKMARK THIS CHAPTER FOR INSTANT ACCESS!** ⚡

---

[← Previous: Messaging System](./06_MESSAGING_SYSTEM.md) | [Back to Index](./00_INDEX.md) | [Next: Monitoring Tools →](./08_MONITORING_TOOLS.md)

