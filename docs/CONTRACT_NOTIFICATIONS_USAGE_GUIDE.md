# 📢 Contract Notifications System - Usage Guide

**Author:** Agent-7 (Web Development Specialist)  
**Date:** 2025-10-15  
**Mission:** Week 1 Quick Win - Discord Contract Notifications  
**Status:** COMPLETE ✅

---

## 🎯 PURPOSE

**Real-time contract visibility for Captain monitoring.**

Automatically posts Discord notifications when:
- Contract assigned to agent
- Agent starts contract work
- Agent completes contract
- Agent blocked on contract

**Benefit:** Captain sees activity without polling!

---

## 🚀 QUICK START

### **Step 1: Configure Webhook**

Add to `.env`:
```bash
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_HERE
```

### **Step 2: Use ContractManager (Auto-Notifications)**

```python
from src.services.contract_system.manager import ContractManager

# Initialize with notifications enabled (default)
manager = ContractManager(enable_notifications=True)

# Get next task - auto-notifies Discord!
task = manager.get_next_task('Agent-7')
# ✅ Discord shows: "📋 Contract C-001 assigned to Agent-7"

# Agent works on contract...

# Complete contract - auto-notifies Discord!
manager.complete_contract('C-001', 'Agent-7', metrics)
# ✅ Discord shows: "✅ Agent-7 completed C-001 (+500 pts)"
```

**That's it!** Notifications are automatic!

---

## 🔔 NOTIFICATION TYPES

### **1. Contract Assigned** (Blue)
```
📋 Contract Assigned: C-001
Test Contract

👤 Agent: Agent-7
⚡ Priority: HIGH
⏱️ Est. Hours: 25
📅 Assigned: 2025-10-15 12:00
```

### **2. Contract Started** (Orange)
```
🚀 Contract Started: C-001
Agent-7 began work on Test Contract

👤 Agent: Agent-7
⏰ Started: 12:30
```

### **3. Contract Completed** (Green)
```
✅ Contract Complete: C-001
Agent-7 completed Test Contract!

👤 Agent: Agent-7
🏆 Points: +500 pts
⏱️ Time: 22.5h
✅ Completed: 2025-10-15 15:00
```

### **4. Contract Blocked** (Red)
```
⚠️ Contract Blocked: C-001
Agent-7 blocked on Test Contract

👤 Agent: Agent-7
🚧 Blocker: Waiting for Captain approval
⏰ Blocked: 14:30
```

---

## 💻 MANUAL NOTIFICATION (Advanced)

If you need to send notifications manually:

```python
from src.discord_commander.contract_notifications import ContractNotifier

notifier = ContractNotifier()

# Manual assignment notification
notifier.notify_contract_assigned(
    contract_id="C-001",
    agent_id="Agent-7",
    contract_name="Test Contract",
    priority="HIGH",
    estimated_hours=25
)

# Manual completion notification
notifier.notify_contract_completed(
    contract_id="C-001",
    agent_id="Agent-7",
    contract_name="Test Contract",
    points_earned=500,
    actual_hours=22.5
)
```

---

## 🔧 TROUBLESHOOTING

### **No notifications appearing:**

**Check 1: Webhook configured?**
```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('DISCORD_WEBHOOK_URL'))"
```

**Check 2: Test webhook:**
```bash
python src/discord_commander/contract_notifications.py
# Should post 4 test notifications to Discord
```

**Check 3: Notifications enabled?**
```python
manager = ContractManager(enable_notifications=True)  # Must be True
```

### **Notifications failing silently:**

Check logs:
```bash
tail -f discord_unified_bot.log | grep "notification"
```

---

## 📊 FILES

**Core System:**
- `src/discord_commander/contract_notifications.py` - ContractNotifier class
- `src/services/contract_system/contract_notifications_integration.py` - Lifecycle hooks
- `src/services/contract_system/manager.py` - Auto-notification integration

**Documentation:**
- `docs/CONTRACT_NOTIFICATIONS_USAGE_GUIDE.md` - This file

---

## ✅ BENEFITS

**For Captain:**
- ✅ Real-time contract visibility (no polling!)
- ✅ Automatic alerts on blockers
- ✅ Progress tracking without asking
- ✅ Leaderboard changes visible

**For Agents:**
- ✅ Automatic status broadcasting
- ✅ No manual Discord posting
- ✅ Recognition for completions

**For Swarm:**
- ✅ Transparency (everyone sees activity)
- ✅ Coordination (know who's working on what)
- ✅ Motivation (public recognition)

---

**🐝 REAL-TIME SWARM VISIBILITY - ALWAYS KNOW WHAT'S HAPPENING!** 📊⚡

