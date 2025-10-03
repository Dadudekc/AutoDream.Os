# Discord Commander Setup Guide

## 🚀 **Quick Start - Running the Discord Commander**

### **Step 1: Set Environment Variables**

You need to set three environment variables:

```bash
# Set your Discord bot token
export DISCORD_BOT_TOKEN="your_actual_discord_bot_token_here"

# Set your main Discord channel ID
export DISCORD_CHANNEL_ID="1234567890123456789"

# Set your Discord server (guild) ID
export DISCORD_GUILD_ID="1234567890123456789"
```

**Windows PowerShell:**
```powershell
$env:DISCORD_BOT_TOKEN="your_actual_discord_bot_token_here"
$env:DISCORD_CHANNEL_ID="1234567890123456789"
$env:DISCORD_GUILD_ID="1234567890123456789"
```

### **Step 2: Run the Discord Commander**

```bash
python run_discord_commander.py
```

## 🔧 **Getting Your Discord Bot Token**

### **1. Create a Discord Application**
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Name it "V2_SWARM Discord Commander"
4. Click "Create"

### **2. Create a Bot**
1. In your application, go to "Bot" section
2. Click "Add Bot"
3. Copy the "Token" - this is your `DISCORD_BOT_TOKEN`

### **3. Get Channel ID**
1. In Discord, right-click on the channel where you want the bot to operate
2. Click "Copy Channel ID" (you need Developer Mode enabled)
3. This is your `DISCORD_CHANNEL_ID`

### **4. Get Guild ID (Server ID)**
1. In Discord, right-click on your server name in the server list
2. Click "Copy Server ID" (you need Developer Mode enabled)
3. This is your `DISCORD_GUILD_ID`

### **5. Enable Developer Mode (if needed)**
1. Discord Settings → Advanced → Developer Mode (ON)

## 🎯 **Bot Permissions**

Your Discord bot needs these permissions:
- **Send Messages**
- **Use Slash Commands**
- **Embed Links**
- **Read Message History**
- **Add Reactions**

## 🚀 **Running the Commander**

Once you have your tokens set:

```bash
# Check configuration
python discord_bot_config.py

# Run the Discord Commander
python run_discord_commander.py
```

## 📋 **Available Commands**

Once running, your Discord Commander will have these slash commands:

### **Basic Commands**
- `/ping` - Test bot responsiveness
- `/commands` - Show help information
- `/status` - Show system status

### **Agent Management**
- `/agents` - List all agents and their status
- `/swarm` - Send message to all agents

### **Messaging**
- `/send` - Send message to specific agent
- `/send-advanced` - Send with priority options
- `/broadcast-advanced` - Broadcast to all agents

### **Project Updates**
- `/project-update` - Send project updates
- `/milestone` - Send milestone notifications
- `/v2-compliance` - Send compliance updates

### **Devlog**
- `/devlog` - Create devlog entries
- `/agent-devlog` - Create agent-specific devlogs

## 🧪 **Testing Without Discord**

If you want to test the commands without running Discord:

```bash
# Quick tests
python test_discord_commander.py --quick

# User experience tests
python test_discord_commander.py --user-experience

# All tests
python test_discord_commander.py
```

## 🔍 **Troubleshooting**

### **"Bot Token Not Set" Error**
```bash
export DISCORD_BOT_TOKEN="your_token_here"
```

### **"Channel ID Not Set" Error**
```bash
export DISCORD_CHANNEL_ID="your_channel_id_here"
```

### **"Guild ID Not Set" Error**
```bash
export DISCORD_GUILD_ID="your_guild_id_here"
```

### **"Invalid Channel ID" Error**
- Make sure the channel ID is a number (not a string)
- Ensure the bot has access to that channel
- Check that Developer Mode is enabled in Discord

### **"Invalid Guild ID" Error**
- Make sure the guild ID is a number (not a string)
- Ensure the bot is added to that server
- Check that Developer Mode is enabled in Discord

### **"Bot Not Responding" Error**
- Verify the bot is online in Discord
- Check bot permissions in the server
- Ensure slash commands are synced

## 📊 **Configuration Status**

Check your configuration anytime:
```bash
python discord_bot_config.py
```

## 🎉 **Success!**

When everything is working, you'll see:
```
🚀 Starting Discord Commander...
🤖 Discord Commander initialized
📋 Available commands:
   - /ping - Test bot responsiveness
   - /commands - Show help information
   - /agents - List all agents and their status
   - /swarm - Send message to all agents
   - /send - Send message to specific agent
   - /devlog - Create devlog entry
   - And many more...

🔗 Connecting to Discord...
✅ V2_SWARM_Bot is online and ready!
✅ Synced 30+ slash commands
```

## 🐝 **WE ARE SWARM - Ready to Command!**

Your Discord Commander is now ready to coordinate the swarm! 🚀
