# Discord Commander Setup Guide

## 🚀 Discord Commander Fixed - Setup Instructions

The Discord Commander has been fixed and is now ready to run with proper integration to the consolidated messaging service.

### 📋 What's Fixed

1. **Immediate Shutdown Issue**: Fixed missing token handling and configuration validation
2. **Messaging Integration**: Proper integration with consolidated messaging service
3. **Slash Commands**: All slash commands are properly registered and working
4. **5-Agent Mode**: Optimized for 5-agent testing mode (Agent-4, Agent-5, Agent-6, Agent-7, Agent-8)
5. **Error Handling**: Comprehensive error handling and logging

### 🛠️ Setup Instructions

#### Step 1: Set Environment Variables

Create a `.env` file in your project root with:

```bash
# Discord Bot Configuration
DISCORD_BOT_TOKEN=your_discord_bot_token_here
DISCORD_CHANNEL_ID=your_main_channel_id_here
DISCORD_GUILD_ID=your_guild_id_here

# Optional: Agent-specific channels (if you have separate channels per agent)
DISCORD_CHANNEL_AGENT_4=agent4_channel_id
DISCORD_CHANNEL_AGENT_5=agent5_channel_id
DISCORD_CHANNEL_AGENT_6=agent6_channel_id
DISCORD_CHANNEL_AGENT_7=agent7_channel_id
DISCORD_CHANNEL_AGENT_8=agent8_channel_id
```

#### Step 2: Test Configuration

Before running the Discord Commander, test the configuration:

```bash
python src/services/test_discord_commander.py
```

This will test:
- ✅ Messaging service integration
- ✅ Bot setup and configuration
- ✅ Slash command registration
- ✅ 5-agent mode compatibility

#### Step 3: Run Discord Commander

Once configuration is tested, run the Discord Commander:

```bash
python src/services/discord_commander_fixed.py
```

### 📋 Available Slash Commands

The Discord Commander provides these slash commands:

#### 🤖 `/swarm_status`
Get current swarm status including:
- Active agents (Agent-4, Agent-5, Agent-6, Agent-7, Agent-8)
- Messaging system status
- Discord bot status
- Connected guilds

#### 📨 `/send_to_agent`
Send message to specific agent:
- Select target agent from dropdown
- Enter your message
- Message sent through consolidated messaging service

#### 📡 `/broadcast`
Broadcast message to all agents:
- Enter message to broadcast
- Sent to all 5 active agents simultaneously
- Shows success/failure count

#### 🤖 `/agent_list`
List all available agents:
- Shows all 5 agents in testing mode
- Displays agent information

#### 🔧 `/system_check`
Check system integration status:
- Discord bot status
- Messaging service integration
- Guild connection status
- 5-agent mode validation

### 🔗 Integration Features

#### Consolidated Messaging Service Integration
- All messages sent through `MessagingService`
- Supports 5-agent mode (Agent-4, Agent-5, Agent-6, Agent-7, Agent-8)
- PyAutoGUI coordinate-based delivery
- Real-time message delivery

#### Quality Assurance Integration
- V2 compliance validation
- Quality gates integration
- File size limits (≤400 lines)
- Complexity validation (≤10 cyclomatic complexity)

#### Error Handling
- Graceful handling of missing configuration
- Comprehensive error logging
- Automatic reconnection attempts
- Status monitoring and reporting

### 🚨 Troubleshooting

#### Discord Commander Shuts Off Immediately
**Cause**: Missing `DISCORD_BOT_TOKEN` environment variable
**Fix**: Set the environment variable and run the test script first

#### Slash Commands Not Working
**Cause**: Commands not synced with Discord
**Fix**: The bot will automatically sync commands on startup

#### Messages Not Reaching Agents
**Cause**: Agents may not be active in 5-agent mode
**Fix**: Check agent status using `/swarm_status` command

#### Configuration Issues
**Cause**: Missing or incorrect environment variables
**Fix**: Run `python src/services/test_discord_commander.py` to diagnose issues

### 📊 5-Agent Testing Mode

The Discord Commander is optimized for 5-agent testing mode:

- **Agent-4** (Captain): Overall coordination
- **Agent-5** (Team Beta Leader): VSCode forking coordination
- **Agent-6** (Code Quality): Phase 3 quality assurance
- **Agent-7** (Testing): Phase 4 validation preparation
- **Agent-8** (Integration): Quality assurance framework

### 🎯 Discord Bot Setup

#### 1. Create Discord Application
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create new application
3. Go to "Bot" section
4. Create bot and copy token
5. Enable required intents (Message Content, Server Members, Server)

#### 2. Invite Bot to Server
1. Go to "OAuth2" → "URL Generator"
2. Select scopes: `bot` and `applications.commands`
3. Select permissions:
   - Send Messages
   - Use Slash Commands
   - Read Message History
   - Read Messages

#### 3. Configure Environment
Set your environment variables with the bot token and channel/guild IDs.

### 🏆 Ready to Use

Once configured and tested, the Discord Commander will:
- ✅ Connect to Discord without shutting off
- ✅ Provide all slash commands
- ✅ Integrate with consolidated messaging service
- ✅ Support 5-agent testing mode
- ✅ Handle errors gracefully
- ✅ Provide comprehensive status reporting

**WE ARE SWARM** - Discord Commander is ready for deployment! 🐝🚀
