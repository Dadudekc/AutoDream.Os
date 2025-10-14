# 🎯 CHAPTER 01: PRIME DIRECTIVE

**Read Time:** 2 minutes  
**Priority:** 🔴 CRITICAL

---

## 📜 **THE PRIME DIRECTIVE**

> **"Prompts are the GAS that feed agents. Without prompts, agents remain IDLE."**

---

## 🔑 **CRITICAL TRUTHS**

### **Truth #1: Inbox Files DON'T Activate Agents**
❌ **WRONG:** Creating execution order in inbox → Agent starts working  
✅ **RIGHT:** Creating execution order + PyAutoGUI message → Agent starts working

### **Truth #2: PyAutoGUI Messages ARE REQUIRED**
Messages act as **fuel** (GAS) that activates agents:
- Without message: Agent sits idle, never sees inbox
- With message: Agent activates, reads inbox, starts work

### **Truth #3: Captain Must Do BOTH**
1. **Create orders** (instructions) → Inbox files
2. **Send activation prompts** (ignition) → PyAutoGUI messages

---

## 🧪 **THE FORMULA**

```
Inbox Order + PyAutoGUI Message = Activated Agent
      ↓              ↓                    ↓
 Instructions    Ignition              Work Begins
```

**Missing either component = Agent stays IDLE!**

---

## ⚡ **WHY THIS MATTERS**

**Scenario 1: Only Inbox (FAILS)**
```
Captain creates execution_order.md → Agent never sees it → No work happens
```

**Scenario 2: Inbox + Message (SUCCESS)**
```
Captain creates execution_order.md → Captain sends PyAutoGUI message → 
Agent receives prompt → Agent reads inbox → Agent starts work! ✅
```

---

## 🎯 **CAPTAIN'S COMMITMENT**

As Captain, **EVERY CYCLE** you must:

✅ Create execution orders (inbox files)  
✅ Send PyAutoGUI messages (activation prompts)  
✅ Verify message delivery (check logs)  
✅ Monitor agent activation (status.json files)

**NO SHORTCUTS. BOTH STEPS. EVERY TIME.**

---

## 💡 **KEY INSIGHT**

**"Inbox = Instructions. Message = Ignition. Need BOTH!"**

Think of it like a car:
- **Inbox** = Destination programmed into GPS
- **Message** = Turning the ignition key
- **Both needed** = Car actually drives to destination

---

## 🚨 **COMMON MISTAKE**

❌ **Captain's thought:** "I wrote the order in their inbox, they'll see it eventually"

**Reality:** Agent never checks inbox without prompt. Order sits unread forever.

✅ **Correct approach:** "I wrote the order AND sent activation message. Agent is now working!"

---

## 📋 **QUICK REFERENCE**

**Every time you assign a task:**

```bash
# Step 1: Create inbox order
Create: agent_workspaces/Agent-X/inbox/EXECUTION_ORDER.md

# Step 2: Send activation message
python -m src.services.messaging_cli \
  --agent Agent-X \
  --message "🎯 URGENT: Check INBOX! New mission assigned." \
  --sender "Captain Agent-4" \
  --priority urgent
```

---

**🎯 REMEMBER: Prompts = GAS. Always fuel your agents!** ⚡

---

[← Back to Index](./00_INDEX.md) | [Next: The Inbox Trap →](./02_INBOX_TRAP.md)

