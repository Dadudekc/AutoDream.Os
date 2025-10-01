# 🤖 Discord Agent Control Commands - User Guide

**Version**: 1.0  
**Date**: 2025-10-01  
**Author**: Agent-7 (Web Development Expert)  
**Purpose**: Easy agent control through Discord slash commands  

---

## 🎯 **AVAILABLE COMMANDS**

### **1. /send_message**
**Send custom messages to any agent**

**Parameters:**
- `agent_id`: Target agent (Agent-4, Agent-5, Agent-6, Agent-7, Agent-8)
- `message`: Your message content

**Example:**
```
/send_message agent_id:Agent-7 message:Please create a new web component
```

**What It Does:**
- Sends your message directly to the specified agent
- Agent receives message via PyAutoGUI messaging system
- Message appears in agent's workspace inbox
- Agent can respond and take action

---

### **2. /run_scan**
**Run project scanner for code analysis**

**Parameters:**
- `scan_type`: Type of scan (full, compliance, dependencies, health)

**Examples:**
```
/run_scan scan_type:full
/run_scan scan_type:compliance
/run_scan scan_type:dependencies
/run_scan scan_type:health
```

**What It Does:**
- Runs project scanner analysis
- Returns summary of findings
- Shows V2 compliance status
- Identifies issues and violations

---

### **3. /agent_status**
**Get current status of agents**

**Parameters:**
- `agent_id`: (Optional) Specific agent to check

**Examples:**
```
/agent_status
/agent_status agent_id:Agent-7
```

**What It Does:**
- Shows current agent status
- Displays active/inactive agents
- Shows current tasks
- Reports agent health

---

### **4. /custom_task**
**Assign custom task to an agent**

**Parameters:**
- `agent_id`: Target agent
- `task_title`: Short title for task
- `task_description`: Detailed description

**Example:**
```
/custom_task agent_id:Agent-7 task_title:Create API endpoint task_description:Build REST endpoint for user management
```

**What It Does:**
- Creates task assignment
- Sends to agent's task queue
- Agent receives task notification
- Task tracked in agent workspace

---

## 🔧 **INTEGRATION INSTRUCTIONS**

### **Add Commands to Bot:**

```python
from src.services.discord_commander.commands import AgentControlCommands
from src.services.consolidated_messaging_service import ConsolidatedMessagingService

# In your bot initialization:
messaging_service = ConsolidatedMessagingService()
agent_commands = AgentControlCommands(bot, messaging_service)

# Register commands with command tree:
agent_commands.register_commands(bot.tree)

# Sync commands with Discord:
await bot.tree.sync()
```

---

## ✅ **USER BENEFITS**

**Easy Agent Control:**
- ✅ Send messages with simple slash commands
- ✅ No need to learn command-line tools
- ✅ Visual feedback with Discord embeds
- ✅ Control all 5 agents easily

**Work Mode Activation:**
- ✅ Use /custom_task to activate specific work modes
- ✅ Send mode instructions via /send_message
- ✅ Monitor status with /agent_status

**Full Agent Control:**
- ✅ Custom message sending
- ✅ Task assignment
- ✅ Status monitoring
- ✅ Project scanning

---

## 📊 **COMMAND FEATURES**

**All Commands Include:**
- ✅ Rich Discord embeds for better UX
- ✅ Error handling and validation
- ✅ Agent ID validation
- ✅ Integration with existing messaging system
- ✅ Subprocess execution for reliability
- ✅ Logging for debugging

---

## 🚀 **QUICK START**

1. **Send a message to Agent-7:**
   ```
   /send_message agent_id:Agent-7 message:Hello Agent-7, please help with web development
   ```

2. **Check all agent status:**
   ```
   /agent_status
   ```

3. **Run compliance scan:**
   ```
   /run_scan scan_type:compliance
   ```

4. **Assign custom task:**
   ```
   /custom_task agent_id:Agent-5 task_title:Analyze Data task_description:Run analysis on latest dataset
   ```

---

**🐝 WE ARE SWARM - Easy Agent Control Through Discord!** ⚡

