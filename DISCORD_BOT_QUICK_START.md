# Discord Bot Quick Start
## 🤖 Message Agents from Discord!

**Status:** ✅ OPERATIONAL (Fixed by Agent-7, 2025-10-11)

---

## 🚀 Start the Bot

```bash
python scripts/execution/run_discord_bot.py
```

**Requirements:**
- DISCORD_BOT_TOKEN set in environment or .env file
- discord.py installed: `pip install discord.py`

---

## 💬 Commands

### Send Message to Specific Agent
```
!message Agent-1 Please review the code changes
!message Agent-4 Captain, need coordination
!message Agent-7 Check the web consolidation
```

### Broadcast to All Agents
```
!broadcast All agents: C-055 tasks due today!
!broadcast Emergency: System maintenance in 10 minutes
```

### Get Swarm Status
```
!status
```

### List All Agents
```
!agents
```

### Get Help
```
!help
```

---

## 🎯 Agent List

| ID | Coordinates | Role |
|----|-------------|------|
| Agent-1 | (-1269, 481) | Integration & Core Systems |
| Agent-2 | (-308, 480) | Architecture & Design |
| Agent-3 | (-1269, 1001) | Infrastructure & DevOps |
| Agent-4 | (-308, 1000) | Quality Assurance (CAPTAIN) |
| Agent-5 | (652, 421) | Business Intelligence |
| Agent-6 | (1612, 419) | Coordination & Communication |
| Agent-7 | (698, 936) | Web Development |
| Agent-8 | (1611, 941) | Operations & Support |

---

## 🔧 Setup (If Not Configured)

### 1. Get Discord Bot Token

1. Go to https://discord.com/developers/applications
2. Create new application (or select existing)
3. Go to "Bot" section
4. Click "Reset Token" and copy it

### 2. Enable Privileged Intents

In Bot settings, enable:
- ✅ Message Content Intent
- ✅ Server Members Intent

### 3. Set Environment Variable

**Windows PowerShell:**
```powershell
$env:DISCORD_BOT_TOKEN="your_token_here"
```

**Or add to .env file:**
```
DISCORD_BOT_TOKEN=your_token_here
```

### 4. Invite Bot to Server

1. Go to OAuth2 → URL Generator
2. Select scopes: `bot`, `applications.commands`
3. Select permissions: Send Messages, Read Messages, Embed Links
4. Use generated URL to invite bot

---

## ✨ How It Works

1. You type command in Discord
2. Bot receives command
3. Bot calls `python -m src.services.messaging_cli --agent <agent> --message "<text>"`
4. Message sent via PyAutoGUI to agent coordinates
5. Agent receives message in Cursor IDE!

**Remote coordination from anywhere!** 🌍

---

## 🐝 WE ARE SWARM

**Discord Commander enables:**
- Remote agent coordination
- Emergency broadcasts
- Status monitoring
- Captain commands from anywhere

**Competition + Cooperation + Remote Access = Ultimate Swarm!** ⚡🔥

---

**Fixed by:** Agent-7 (Integration Velocity Specialist)  
**Date:** 2025-10-11  
**Status:** Operational and tested

