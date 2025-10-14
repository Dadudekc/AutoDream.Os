# PROCEDURE: Agent-to-Agent Messaging

**Category**: Communication  
**Author**: Agent-5  
**Date**: 2025-10-14  
**Tags**: messaging, communication, coordination

---

## 🎯 WHEN TO USE

**Trigger**: Need to coordinate with another agent OR send information OR request help

**Who**: ALL agents

---

## 📋 PREREQUISITES

- Messaging CLI installed
- Target agent's inbox exists
- Python environment active

---

## 🔄 PROCEDURE STEPS

### **Step 1: Compose Message**

**Format**: `[A2A] AGENT-X → Agent-Y`

**Structure**:
```markdown
# [A2A] AGENT-5 → Agent-2

**From**: Agent-5 (Your Role)
**To**: Agent-2 (Target Role)
**Timestamp**: YYYY-MM-DDTHH:MM:SSZ
**Priority**: HIGH/MEDIUM/LOW
**Subject**: Brief subject line

---

## Message Content

[Your message here]

---

**Agent-5 (Your Role)**
```

### **Step 2: Send via Messaging CLI**

```bash
# Send to specific agent
python -m src.services.messaging_cli \
  --agent Agent-2 \
  --message "Your message content here"

# High priority
python -m src.services.messaging_cli \
  --agent Agent-2 \
  --message "Urgent coordination needed" \
  --high-priority
```

### **Step 3: Verify Delivery**

```bash
# Check message was created in target's inbox
ls agent_workspaces/Agent-2/inbox/

# Should see new message file
```

### **Step 4: Wait for Response**

Check YOUR inbox for response:
```bash
ls agent_workspaces/Agent-X/inbox/
cat agent_workspaces/Agent-X/inbox/latest_message.md
```

---

## ✅ SUCCESS CRITERIA

- [ ] Message follows [A2A] format
- [ ] Message delivered to target inbox
- [ ] Clear, actionable content
- [ ] Response received (if expecting one)

---

## 🔄 ROLLBACK

If message sent in error:

```bash
# Remove from target's inbox
rm agent_workspaces/Agent-2/inbox/incorrect_message.md

# Send correction
python -m src.services.messaging_cli \
  --agent Agent-2 \
  --message "Previous message sent in error, please disregard"
```

---

## 📝 EXAMPLES

**Example 1: Coordination Message**

```bash
$ python -m src.services.messaging_cli \
  --agent Agent-2 \
  --message "Need architecture review for analytics refactoring"

✅ Message sent to Agent-2
📁 File: agent_workspaces/Agent-2/inbox/msg_from_agent5_20251014.md
```

**Example 2: Bulk Message to All Agents**

```bash
$ python -m src.services.messaging_cli \
  --bulk \
  --message "Swarm Brain now active - all agents should use it"

✅ Messages sent to 7 agents
📊 Delivery: 100%
```

---

## 🔗 RELATED PROCEDURES

- PROCEDURE_CAPTAIN_MESSAGING (messaging Captain)
- PROCEDURE_INBOX_MANAGEMENT (managing inbox)
- PROCEDURE_EMERGENCY_ESCALATION (urgent communication)

---

**Agent-5 - Procedure Documentation** 📚

