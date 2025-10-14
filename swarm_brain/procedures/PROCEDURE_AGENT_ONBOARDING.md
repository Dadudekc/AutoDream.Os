# PROCEDURE: Agent Onboarding

**Category**: Setup & Configuration  
**Author**: Agent-5 (extracted from scripts/agent_onboarding.py)  
**Date**: 2025-10-14  
**Tags**: onboarding, setup, agent-management

---

## 🎯 WHEN TO USE

**Trigger**: New agent joins the swarm OR agent workspace needs recreation

**Who**: Captain Agent-4 or senior agents with admin access

---

## 📋 PREREQUISITES

- Python environment active
- Agent workspace root exists (`agent_workspaces/`)
- Agent ID available (Agent-1 through Agent-8)
- Role assignment ready

---

## 🔄 PROCEDURE STEPS

### **Step 1: Run Onboarding Script**

```bash
python scripts/agent_onboarding.py
```

### **Step 2: Follow Interactive Prompts**

The script will:
1. Check available agent IDs
2. Create agent workspace directory
3. Create inbox subdirectory
4. Initialize `status.json` with agent metadata
5. Set up initial configuration

### **Step 3: Verify Workspace**

```bash
# Check workspace created
ls agent_workspaces/Agent-X/

# Should see:
# - status.json (initialized)
# - inbox/ (empty directory ready for messages)
```

### **Step 4: Send Welcome Message**

```bash
# Use messaging system to send first mission
python -m src.services.messaging_cli \
  --agent Agent-X \
  --message "Welcome to the swarm! Your first mission: [details]"
```

---

## ✅ SUCCESS CRITERIA

- [ ] Agent workspace directory exists (`agent_workspaces/Agent-X/`)
- [ ] status.json initialized with correct agent ID and role
- [ ] Inbox directory created
- [ ] Welcome message delivered
- [ ] Agent shows as active in swarm status

---

## 🔄 ROLLBACK

If onboarding fails:

```bash
# Remove workspace
rm -rf agent_workspaces/Agent-X/

# Re-run script
python scripts/agent_onboarding.py
```

---

## 📝 EXAMPLES

**Example 1: Onboarding Agent-5**

```bash
$ python scripts/agent_onboarding.py
🎯 Agent Swarm Onboarding
Available Agents:
  - Agent-5 (Business Intelligence Specialist)
  
Creating workspace for Agent-5...
✅ Workspace created: agent_workspaces/Agent-5/
✅ Inbox created: agent_workspaces/Agent-5/inbox/
✅ Status initialized
✅ Agent-5 onboarded successfully!
```

---

## 🔗 RELATED PROCEDURES

- PROCEDURE_AGENT_OFFBOARDING (when removing agent)
- PROCEDURE_STATUS_UPDATE (updating agent status)
- PROCEDURE_INBOX_MANAGEMENT (managing agent messages)

---

**Agent-5 - Procedure Documentation** 📚

