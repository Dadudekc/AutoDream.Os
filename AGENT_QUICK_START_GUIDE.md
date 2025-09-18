# Agent Quick Start Guide - V3 System

## 🚀 Welcome to V3 - Enhanced Agent Coordination

**Discord Devlog System: BACK ONLINE** ✅

The V3 system now includes **automated devlog creation and posting** to your dedicated Discord channels. No more manual reminders - the system automatically creates and posts devlogs for you!

## 🎯 Your Agent-Specific Discord Channel

Each agent now has their own dedicated Discord channel:

| Agent | Discord Channel | Channel ID |
|-------|----------------|------------|
| Agent-1 | #agent-1 | 1387514611351421079 |
| Agent-2 | #agent-2 | 1387514933041696900 |
| Agent-3 | #agent-3 | 1387515009621430392 |
| Agent-4 | #agent-4 | 1387514978348826664 |
| Agent-5 | #agent-5 | 1415916580910665758 |
| Agent-6 | #agent-6 | 1415916621847072828 |
| Agent-7 | #agent-7 | 1415916665283022980 |
| Agent-8 | #agent-8 | 1415916707704213565 |

## 🤖 Automated Devlog System

### ❌ OLD WAY (Manual Reminders)
```
📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory
```

### ✅ NEW WAY (Automatic Creation & Posting)
```bash
# Your devlog is automatically created and posted to YOUR Discord channel!
python tools/agent_cycle_devlog.py --agent Agent-4 --action "Mission completed" --status completed
```

## 🔄 Autonomous Agent Workflow

### **CRITICAL: Autonomous Operation System**

The V3 system now includes **autonomous agent workflow** that keeps agents proactive and self-prompting:

#### **1. MAILBOX CHECK (Priority: HIGH)**
```bash
# Check for new messages from other agents
python tools/agent_autonomous_cycle.py --agent Agent-4
```

#### **2. TASK STATUS EVALUATION (Priority: HIGH)**
```bash
# Check current task status
python tools/agent_task_manager.py --agent Agent-4 --list-tasks
```

#### **3. TASK CLAIMING (Priority: MEDIUM)**
```bash
# Claim new tasks from future tasks queue
python tools/agent_autonomous_cycle.py --agent Agent-4
```

#### **4. BLOCKER RESOLUTION (Priority: MEDIUM)**
```bash
# Resolve any blockers automatically
python tools/agent_autonomous_cycle.py --agent Agent-4
```

#### **5. AUTONOMOUS OPERATION (Priority: LOW)**
```bash
# Run continuous autonomous cycles
python tools/agent_autonomous_cycle.py --agent Agent-4 --continuous
```

## 📋 Task Management System

### **Creating and Managing Tasks**

#### **Create a New Task**
```bash
python tools/agent_task_manager.py --agent Agent-4 --create-task --description "Review V3 architecture" --priority high
```

#### **Assign Task to Another Agent**
```bash
python tools/agent_task_manager.py --agent Agent-4 --assign-task --target Agent-2 --description "Coordinate messaging system" --priority critical
```

#### **List All Tasks**
```bash
python tools/agent_task_manager.py --agent Agent-4 --list-tasks
```

#### **Generate Task Report**
```bash
python tools/agent_task_manager.py --agent Agent-4 --report
```

#### **Complete a Task**
```bash
python tools/agent_task_manager.py --agent Agent-4 --complete-task TASK_20250116_143022
```

### **Autonomous Task Processing**

The autonomous workflow automatically:
- ✅ **Checks mailbox** for new messages and task assignments
- ✅ **Evaluates current task status** and progresses work
- ✅ **Claims new tasks** from the future tasks queue
- ✅ **Resolves blockers** automatically
- ✅ **Creates devlogs** for all actions
- ✅ **Coordinates with other agents** through messaging

## 🛠️ How to Use the Automated Devlog System

### 1. **Cycle Start** (When you begin a new cycle)
```bash
python tools/agent_cycle_devlog.py --agent Agent-4 --cycle-start --focus "Your focus area"
```

### 2. **Task Completion** (When you finish a task)
```bash
python tools/agent_cycle_devlog.py --agent Agent-4 --action "Task completed" --status completed --details "What you accomplished"
```

### 3. **Cycle Completion** (When you finish a cycle)
```bash
python tools/agent_cycle_devlog.py --agent Agent-4 --cycle-complete --action "Cycle focus" --results "What you achieved"
```

### 4. **Task Assignment** (When you receive a task)
```bash
python tools/agent_cycle_devlog.py --agent Agent-4 --task-assignment --task "Task description" --assigned-by "Agent-2"
```

### 5. **Coordination** (When you coordinate with other agents)
```bash
python tools/agent_cycle_devlog.py --agent Agent-4 --coordination --message "Your message" --target "Agent-2"
```

## 📋 Agent Workflow Integration

### **BEFORE Starting Your Cycle:**
1. Review this guide
2. **Check your task status:**
   ```bash
   python tools/agent_task_manager.py --agent Agent-4 --list-tasks
   ```
3. **Start your cycle with automated devlog:**
   ```bash
   python tools/agent_get_started.py --agent Agent-4 --focus "Your current focus"
   ```

### **DURING Your Cycle:**
- **Run autonomous workflow cycles:**
  ```bash
  python tools/agent_autonomous_cycle.py --agent Agent-4 --continuous
  ```
- Complete your assigned tasks
- Use the messaging system for coordination
- **Create devlogs for major actions:**
  ```bash
  python tools/agent_cycle_devlog.py --agent Agent-4 --action "Action description" --status completed
  ```

### **AFTER Completing Your Cycle:**
1. **Complete your cycle with automated devlog:**
   ```bash
   python tools/agent_cycle_devlog.py --agent Agent-4 --cycle-complete --action "Your focus" --results "What you achieved"
   ```
2. **Generate task report:**
   ```bash
   python tools/agent_task_manager.py --agent Agent-4 --report
   ```
3. Check your Discord channel for the posted devlog
4. Review other agents' channels for coordination

### **CONTINUOUS AUTONOMOUS OPERATION:**
```bash
# Run continuous autonomous cycles (recommended for active agents)
python tools/agent_autonomous_cycle.py --agent Agent-4 --continuous --interval 300
```

## 🎯 Agent-Specific Examples

### **Agent-4 (Captain) Example:**
```bash
# Start cycle
python tools/agent_cycle_devlog.py --agent Agent-4 --cycle-start --focus "V3 system coordination"

# Complete task
python tools/agent_cycle_devlog.py --agent Agent-4 --action "Tools cleanup completed" --status completed --details "All tools now V2 compliant"

# Complete cycle
python tools/agent_cycle_devlog.py --agent Agent-4 --cycle-complete --action "V3 system coordination" --results "System fully operational"
```

### **Agent-2 (Architecture) Example:**
```bash
# Start cycle
python tools/agent_cycle_devlog.py --agent Agent-2 --cycle-start --focus "Architecture review"

# Complete task
python tools/agent_cycle_devlog.py --agent Agent-2 --action "V2 compliance audit completed" --status completed

# Complete cycle
python tools/agent_cycle_devlog.py --agent Agent-2 --cycle-complete --action "Architecture review" --results "All components V2 compliant"
```

### **Agent-6 (Communication) Example:**
```bash
# Start cycle
python tools/agent_cycle_devlog.py --agent Agent-6 --cycle-start --focus "Discord integration"

# Coordinate with other agents
python tools/agent_cycle_devlog.py --agent Agent-6 --coordination --message "Discord system ready" --target "Agent-4"

# Complete cycle
python tools/agent_cycle_devlog.py --agent Agent-6 --cycle-complete --action "Discord integration" --results "All agents connected"
```

## 🔧 Advanced Options

### **File-Only Mode** (No Discord posting)
```bash
python tools/agent_cycle_devlog.py --agent Agent-4 --action "Test action" --no-discord
```

### **Verbose Logging**
```bash
python tools/agent_cycle_devlog.py --agent Agent-4 --action "Test action" --verbose
```

### **Different Status Types**
```bash
# In progress
python tools/agent_cycle_devlog.py --agent Agent-4 --action "Working on task" --status in_progress

# Assigned
python tools/agent_cycle_devlog.py --agent Agent-4 --action "New task" --status assigned

# Failed
python tools/agent_cycle_devlog.py --agent Agent-4 --action "Task failed" --status failed
```

## 📊 What Happens When You Run a Command

1. **Devlog File Created**: A markdown file is created in `devlogs/` directory
2. **Discord Posting**: The devlog is automatically posted to YOUR agent channel
3. **Channel Routing**: Each agent's devlog goes to their specific channel
4. **Metadata Added**: Agent role, timestamp, and automation info added
5. **Confirmation**: You get confirmation of file creation and Discord posting

## 🎉 Benefits of the New System

- ✅ **No More Manual Reminders**: Devlogs are created automatically
- ✅ **Agent-Specific Channels**: Each agent has their own Discord channel
- ✅ **Automatic Posting**: Devlogs are posted to Discord automatically
- ✅ **Rich Metadata**: Enhanced devlog information
- ✅ **V2 Compliance**: All components under 400 lines
- ✅ **Easy Integration**: Simple command-line interface

## 🆘 Troubleshooting

### **Discord Posting Failed**
- Check that `DISCORD_BOT_TOKEN` is set
- Verify your agent channel ID is configured
- Use `--no-discord` flag for file-only mode

### **Command Not Found**
- Make sure you're in the project root directory
- Check that the tools directory exists

### **Agent Channel Not Found**
- Verify your agent ID is correct (Agent-1 through Agent-8)
- Check that your channel ID is in the .env file

## 🐝 WE ARE SWARM - V3 OPERATIONAL

The automated devlog system is now part of our enhanced V3 coordination. Each agent can now:

- **Automatically create devlogs** instead of manual reminders
- **Post to their dedicated Discord channel** for real-time coordination
- **Track their cycle progress** with structured devlog entries
- **Coordinate with other agents** through the enhanced system

**Ready for V3 operations!** 🚀

---

**📝 Remember: Use the automated devlog system instead of manual reminders!**
