# 🎮 Discord Commander - User Guide

**Quick Agent Control from Discord**

---

## 🚀 **QUICK START**

### **1. Setup Environment Variables**

Create `.env` file:
```env
DISCORD_BOT_TOKEN=your_bot_token_here
DISCORD_GUILD_ID=your_server_id_here
DISCORD_CHANNEL_ID=your_channel_id_here
```

### **2. Start Discord Commander**

```bash
python run_discord_commander.py
```

### **3. Use Commands in Discord**

```
/agent_status - See all 5 agents status
/send <agent> <message> - Send custom message to any agent
/scan 5-agent - Run project scan in 5-agent mode
/fix_violations - Fix remaining compliance issues
/help - Show all commands
```

---

## 📋 **AVAILABLE COMMANDS**

### **Agent Control**

**Send Custom Message:**
```
/send Agent-5 "Please analyze the trading module"
/send Agent-7 "Refactor the dashboard component"
```

**Broadcast to All:**
```
/broadcast "Run quality gates on your modules"
```

### **Work Modes**

**Project Scan:**
```
/scan 5-agent - Full scan with 5 active agents
/scan focus compliance - Focus on compliance issues
```

**Fix Issues:**
```
/fix_violations - Auto-fix compliance violations
/fix_syntax - Fix syntax errors
/cleanup - Delete unnecessary files
```

### **Status & Monitoring**

**Agent Status:**
```
/agent_status - All agents
/agent_status Agent-5 - Specific agent
```

**System Health:**
```
/health - System health check
/quality - Quality gates summary
```

### **Custom Tasks**

**Assign Specific Task:**
```
/task Agent-8 "Update vector database with latest work"
/task Agent-7 "Refactor analytics/predictive_core.py"
```

---

## 🎯 **COMMON USE CASES**

### **Morning Check-in**
```
/agent_status
/health
/scan 5-agent
```

### **Assign Work**
```
/send Agent-5 "Refactor large files in src/core"
/send Agent-7 "Fix poor score files in src/services"
/task Agent-8 "Complete test suite"
```

###  **Quick Fixes**
```
/fix_violations
/cleanup
/quality
```

### **Custom Coordination**
```
/send Agent-5 "Coordinate with Agent-7 on integration"
/broadcast "Prepare for deployment - run quality checks"
```

---

## 🔧 **TROUBLESHOOTING**

### **Bot Won't Start**
1. Check `.env` file exists
2. Verify DISCORD_BOT_TOKEN is valid
3. Check bot has proper Discord permissions
4. Review logs in `logs/discord_commander.log`

### **Commands Not Working**
1. Ensure bot is online in Discord
2. Check you're in the correct channel (DISCORD_CHANNEL_ID)
3. Verify command syntax (use `/help`)
4. Check agent coordinates are correct

### **Agents Not Responding**
1. Run `/agent_status` to check agent health
2. Verify agents are in 5-agent mode (4, 5, 6, 7, 8)
3. Check agent coordinates in cursor_agent_coords.json
4. Review agent logs in agent_workspaces/

---

## 📊 **RESPONSE FORMAT**

**Successful Command:**
```
✅ Message sent to Agent-5
📬 Agent-5 will respond in their workspace
🔔 Check agent_workspaces/Agent-5/inbox for confirmation
```

**Agent Response:**
```
📤 Agent-5 Response:
Task acknowledged. Beginning refactoring of src/core files.
ETA: 2-3 cycles for completion.
```

---

## 🎯 **BEST PRACTICES**

1. **Be Specific**: Include file names, targets, expected outcomes
2. **Use Agent Numbers**: Agent-5, Agent-7, etc. (not roles)
3. **Check Status First**: `/agent_status` before assigning work
4. **One Task at a Time**: Don't overload agents
5. **Monitor Progress**: Check responses in agent workspaces

---

## 🐝 **5-AGENT MODE**

**Active Agents:**
- **Agent-4 (Captain)**: Strategic oversight, coordination
- **Agent-5 (Coordinator)**: Business intelligence, coordination
- **Agent-6 (Quality)**: Quality assurance, testing
- **Agent-7 (Implementation)**: Web development, implementation
- **Agent-8 (Integration)**: System integration, SSOT management

**Inactive Agents (Don't assign):**
- Agent-1, Agent-2, Agent-3

---

## 📝 **EXAMPLE SESSION**

```discord
User: /agent_status
Bot: ✅ Agent-4: ACTIVE | Agent-5: ACTIVE | Agent-6: ACTIVE | Agent-7: ACTIVE | Agent-8: ACTIVE

User: /scan 5-agent
Bot: 🔍 Running project scan with 5 agents...
Bot: ✅ Scan complete: 921 Python files, 94.4% compliant, 50 violations found

User: /send Agent-5 "Fix the top 10 violations"
Bot: ✅ Message sent to Agent-5
Bot: 📬 Agent-5 acknowledged and is executing

User: /send Agent-7 "Refactor largest files"
Bot: ✅ Message sent to Agent-7
Bot: 📬 Agent-7 working on predictive_core.py (576 lines)
```

---

**Created by Captain Agent-4 for easy agent control**
**Last Updated**: 2025-10-01

