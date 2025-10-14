# 📡 CHAPTER 06: MESSAGING SYSTEM

**Read Time:** 5 minutes  
**Priority:** 🔴 CRITICAL

---

## 🎯 **THE MESSAGING SYSTEM**

How to send PyAutoGUI messages to activate agents.

---

## 🚀 **QUICK START**

**Send message to single agent:**
```bash
python -m src.services.messaging_cli \
  --agent Agent-X \
  --message "YOUR MESSAGE" \
  --sender "Captain Agent-4" \
  --priority urgent
```

**Send message to ALL agents (bulk):**
```bash
python -m src.services.messaging_cli \
  --bulk \
  --message "YOUR MESSAGE" \
  --sender "Captain Agent-4" \
  --priority urgent
```

---

## 📝 **MESSAGE TEMPLATES**

### **Template 1: Task Assignment (Most Common)**
```
🎯 URGENT: Check INBOX!

New mission assigned: [task_name]
Location: agent_workspaces/Agent-X/inbox/EXECUTION_ORDER_CXXX.md

Task: [brief description]
Points: XXX
ROI: XX.XX
Priority: [HIGH/URGENT/CRITICAL]

Clean workspace first, then read full order.

BEGIN NOW! 🐝
```

### **Template 2: Status Check**
```
📊 STATUS CHECK REQUIRED

Provide update on current task:
- Progress percentage
- Blockers (if any)
- ETA for completion

Reply within 1 cycle.
```

### **Template 3: Coordination**
```
🤝 COORDINATION NEEDED

You're paired with Agent-Y on [task].

Coordinate approach, divide work, then execute.
Update Captain when coordination complete.
```

### **Template 4: Emergency**
```
🚨 EMERGENCY: STOP CURRENT WORK

Critical issue detected in [area].
Check inbox for emergency protocol.

IMMEDIATE ACTION REQUIRED!
```

### **Template 5: Acknowledgment**
```
✅ MISSION COMPLETE - EXCELLENT WORK!

Task: [task_name]
Points earned: XXX
Quality: Excellent
Impact: [brief description]

Next assignment incoming shortly!
```

---

## 🔧 **COMMAND STRUCTURE**

### **Required Parameters:**
```bash
--agent Agent-X        # Target agent (or --bulk for all)
--message "..."        # Message content
--sender "..."         # Your identifier
```

### **Optional Parameters:**
```bash
--priority urgent      # Priority level (regular/high/urgent)
--type captain_to_agent # Message type
--pyautogui           # Enable PyAutoGUI delivery (default: true)
```

### **Full Command:**
```bash
python -m src.services.messaging_cli \
  --agent Agent-2 \
  --message "🎯 URGENT: Check INBOX! Mission C001 assigned." \
  --sender "Captain Agent-4" \
  --priority urgent \
  --type captain_to_agent
```

---

## 🛠️ **TROUBLESHOOTING**

### **Error: "ModuleNotFoundError: No module named 'src'"**

**Fix:** Update `messaging_cli.py` imports

Add this at TOP of file (before other imports):
```python
import sys
from pathlib import Path

# CRITICAL: Add to path BEFORE imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# NOW import
from src.services.messaging_cli_handlers import ...
```

### **Error: "Agent coordinates not found"**

**Fix:** Verify coordinate file exists
```bash
# Check coordinate file
cat cursor_agent_coords.json

# If missing, run coordinate capture
python scripts/capture_coordinates.py
```

### **Error: "PyAutoGUI not available"**

**Fix:** Install PyAutoGUI
```bash
pip install pyautogui pyperclip
```

### **Error: "Message delivery failed"**

**Checks:**
1. Verify agent exists in agent_registry.json
2. Check coordinates are valid (within screen bounds)
3. Ensure cursor IDE is open and visible
4. Review messaging logs for details

---

## ✅ **VERIFYING DELIVERY**

### **Success Indicators:**

Look for these in command output:
```
✅ "Coordinates validated for Agent-X"
✅ "Message sent to Agent-X at (x, y)"
✅ "WE. ARE. SWARM." confirmation
```

### **Log Files:**

Check these logs:
```bash
# Messaging logs
tail -f logs/messaging.log

# PyAutoGUI logs
tail -f logs/pyautogui.log
```

### **Agent Status:**

Verify agent received message:
```bash
# Check agent's status file
cat agent_workspaces/Agent-X/status.json

# Look for updated "last_message_received" timestamp
```

---

## 📊 **BULK MESSAGING**

### **When to Use:**
- Starting new cycle (activate all agents)
- System-wide announcements
- Emergency protocols
- Status checks

### **Command:**
```bash
python -m src.services.messaging_cli \
  --bulk \
  --message "🚀 NEW CYCLE: Check INBOX for assignments! BEGIN NOW!" \
  --sender "Captain Agent-4" \
  --priority urgent
```

### **Bulk Message Features:**
- Sends to all 7 agents (Agent-1, 2, 3, 5, 6, 7, 8)
- Skips Agent-4 (Captain, yourself)
- Validates coordinates for each agent
- Reports delivery status for each
- Continues even if one agent fails

---

## 🎯 **BEST PRACTICES**

### **DO:**
✅ Send clear, actionable messages  
✅ Include specific task details  
✅ Reference inbox location  
✅ Use appropriate priority level  
✅ Verify delivery before proceeding  
✅ Keep messages concise but complete  

### **DON'T:**
❌ Send vague messages ("do something")  
❌ Forget to include inbox location  
❌ Skip delivery verification  
❌ Send messages without inbox orders ready  
❌ Use all caps (looks aggressive)  
❌ Send duplicate messages (causes confusion)  

---

## ⚡ **ACTIVATION PROTOCOL**

### **Standard Activation Sequence:**

```bash
# 1. Create inbox order FIRST
Create: agent_workspaces/Agent-X/inbox/EXECUTION_ORDER_CXXX.md

# 2. THEN send activation message
python -m src.services.messaging_cli \
  --agent Agent-X \
  --message "🎯 URGENT: Check INBOX! Mission CXXX assigned. BEGIN NOW!" \
  --sender "Captain Agent-4" \
  --priority urgent

# 3. Verify delivery
Check logs for "Message sent to Agent-X"

# 4. Monitor activation
cat agent_workspaces/Agent-X/status.json
```

**NEVER reverse steps 1 and 2!** (Order first, message second)

---

## 🚨 **EMERGENCY MESSAGING**

### **Code Red (System Failure):**
```bash
python -m src.services.messaging_cli --bulk \
  --message "🚨 CODE RED: System failure detected. Check inbox for emergency protocol. IMMEDIATE ACTION REQUIRED!" \
  --sender "Captain Agent-4" \
  --priority urgent
```

### **Code Black (Coordinate Failure):**
```bash
python -m src.services.messaging_cli --bulk \
  --message "🚨 CODE BLACK: Coordinate system down. Switch to inbox-only mode. Continue current tasks." \
  --sender "Captain Agent-4" \
  --priority urgent
```

---

## 📋 **QUICK REFERENCE**

| Task | Command |
|------|---------|
| **Activate single agent** | `--agent Agent-X --message "..." --priority urgent` |
| **Activate all agents** | `--bulk --message "..." --priority urgent` |
| **Check status** | `--check-status` |
| **List agents** | `--list-agents` |
| **View coordinates** | `--coordinates` |
| **Message history** | `--history` |

---

**🎯 REMEMBER: Message = Activation. No message = Idle agent!** ⚡

---

[← Previous: Daily Checklist](./05_DAILY_CHECKLIST.md) | [Back to Index](./00_INDEX.md) | [Next: Quick Commands →](./07_QUICK_COMMANDS.md)

