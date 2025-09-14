# 🐝 V2_SWARM Discord Agent Bot

## 🤖 Interactive Agent Prompting via Discord

The V2_SWARM Discord Agent Bot enables real-time agent coordination and prompting through Discord commands. This revolutionary feature allows external users to interact directly with V2_SWARM agents through natural language commands.

---

## 🚀 Quick Start

### 1. Setup Discord Bot
```bash
# Set your Discord bot token
export DISCORD_BOT_TOKEN=your_bot_token_here

# Or pass as argument
python src/discord_commander/discord_agent_bot.py your_token
```

### 2. Basic Usage
```
!prompt @Agent-4 Analyze the current project status
!status @Agent-1
!swarm Emergency coordination meeting
!agents
!help
```

---

## 📋 Available Commands

### 🤖 Agent Commands
| Command | Description | Example |
|---------|-------------|---------|
| `!prompt @agent message` | Send prompt to specific agent | `!prompt @Agent-4 Please analyze test coverage` |
| `!status @agent` | Check agent status and activity | `!status @Agent-1` |

### 🐝 Swarm Commands
| Command | Description | Example |
|---------|-------------|---------|
| `!swarm message` | Broadcast to all agents | `!swarm Emergency test coverage mission` |

### ℹ️ Information Commands
| Command | Description | Example |
|---------|-------------|---------|
| `!agents` | List all available agents | `!agents` |
| `!help` | Show help information | `!help` |
| `!ping` | Test bot responsiveness | `!ping` |

---

## 🔧 Configuration

### Bot Configuration (`config/discord_bot_config.json`)
```json
{
  "bot_settings": {
    "command_prefix": "!",
    "command_timeout": 300,
    "max_concurrent_commands": 10
  },
  "permissions": {
    "allowed_channels": [],
    "admin_users": []
  },
  "features": {
    "enable_prompt_commands": true,
    "enable_status_commands": true,
    "enable_swarm_commands": true
  }
}
```

### Environment Variables
```bash
# Required
DISCORD_BOT_TOKEN=your_discord_bot_token

# Optional
DISCORD_CHANNEL_ID=your_channel_id  # For webhook notifications
```

---

## 🎯 Features

### ✅ Real-time Agent Communication
- **Direct Inbox Delivery**: Messages sent directly to agent workspaces
- **Status Tracking**: Real-time command status and delivery confirmation
- **Response Handling**: Agent responses routed back through Discord

### ✅ Swarm Coordination
- **Broadcast Messaging**: Send messages to all agents simultaneously
- **Coordination Tracking**: Monitor agent responses and coordination status
- **Emergency Protocols**: Priority messaging for urgent coordination

### ✅ Advanced Features
- **Command History**: Track all commands and responses
- **Rate Limiting**: Prevent command spam and abuse
- **Permission System**: Restrict commands to specific users/channels
- **Rich Embeds**: Beautiful Discord embeds for responses

---

## 🏗️ Architecture

### Core Components
1. **DiscordAgentBot**: Main bot class handling Discord events
2. **DiscordCommandParser**: Parses Discord commands and extracts parameters
3. **AgentCommunicationEngine**: Handles communication with V2_SWARM agents
4. **ResponseTracker**: Tracks command responses and status

### Message Flow
```
Discord Command → Command Parser → Agent Engine → Agent Inbox → Agent Response → Discord Reply
```

### File Structure
```
src/discord_commander/
├── discord_agent_bot.py          # Main bot implementation
├── discord_commander.py          # Legacy commander (monitoring)
├── enhanced_discord_integration.py # Multi-channel support
├── agent_communication_engine_refactored.py # Agent communication
└── discord_commander_models.py   # Data models

scripts/
├── discord_agent_bot.py          # Main bot implementation
└── test_discord_agent_bot.py     # Test suite

config/
└── discord_bot_config.json       # Bot configuration
```

---

## 🧪 Testing

### Run Test Suite
```bash
python -m pytest tests/functional/test_run_discord_agent_bot.py tests/unit/test_discord_commander_*.py
```

### Test Bot Connection
```bash
python src/discord_commander/discord_agent_bot.py --test
```

### Show Configuration
```bash
python src/discord_commander/discord_agent_bot.py --config
```

---

## 📚 Setup Instructions

### 1. Create Discord Application
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Name it "V2_SWARM Agent Bot"

### 2. Create Bot User
1. Go to "Bot" section in left sidebar
2. Click "Add Bot"
3. Copy the bot token (keep this secret!)

### 3. Set Permissions
1. Go to "OAuth2" → "URL Generator"
2. Select scopes: `bot`, `applications.commands`
3. Select permissions:
   - Send Messages
   - Read Messages
   - Embed Links
   - Read Message History

### 4. Invite Bot to Server
1. Use the generated URL to invite the bot
2. Ensure bot has proper permissions in your channel

### 5. Configure Environment
```bash
# Set bot token
export DISCORD_BOT_TOKEN=your_token_here

# Optional: Restrict to specific channel
export DISCORD_CHANNEL_ID=your_channel_id
```

### 6. Start the Bot
```bash
# Start with environment variable
python src/discord_commander/discord_agent_bot.py

# Or pass token directly
python src/discord_commander/discord_agent_bot.py your_token
```

---

## 💡 Usage Examples

### Basic Agent Prompting
```
!prompt @Agent-4 Please provide a comprehensive status update for Phase 4 planning
!prompt @Agent-1 Analyze the current test coverage metrics
!prompt @Agent-6 What are the main coordination bottlenecks?
```

### Status Checking
```
!status @Agent-4
!status @Agent-1
```

### Swarm Coordination
```
!swarm All agents: Emergency test coverage mission activated - achieve 85%+ coverage
!swarm Coordination meeting in 10 minutes - all agents attend
!swarm Phase 4 evolution planning session starting now
```

### Information Queries
```
!agents      # List all available agents
!help        # Show help information
!ping        # Test bot responsiveness
```

---

## 🔐 Security & Permissions

### Channel Restrictions
- Set `allowed_channels` in config to restrict bot to specific channels
- Leave empty to allow all channels (default)

### User Restrictions
- Set `admin_users` in config to restrict commands to specific users
- Leave empty to allow all users (default)

### Rate Limiting
- Maximum concurrent commands: 10 (configurable)
- Command timeout: 300 seconds (configurable)
- Automatic cleanup of old commands

---

## 📊 Monitoring & Logging

### Command Tracking
- All commands logged with timestamps
- Response tracking for delivery confirmation
- Performance metrics and latency monitoring

### Status Updates
- Real-time command status via Discord embeds
- Delivery confirmations for agent messages
- Error reporting and troubleshooting

### DevLog Integration
- Automatic posting of devlogs to Discord
- Agent-specific channel notifications
- Swarm-wide announcements

---

## 🐛 Troubleshooting

### Bot Not Responding
1. Check bot token is correct
2. Verify bot has proper permissions in Discord
3. Check bot is online: `!ping`
4. Review bot logs for errors

### Commands Not Working
1. Verify command syntax: `!help`
2. Check if channel restrictions apply
3. Ensure agent names are correct: `!agents`
4. Test with simple command: `!ping`

### Agent Communication Issues
1. Verify agent workspaces exist
2. Check inbox permissions
3. Review agent communication logs
4. Test agent status: `!status @agent`

---

## 🚀 Advanced Features

### Custom Commands
- Extend `DiscordCommandParser` for new command types
- Add custom logic in `DiscordAgentBot` event handlers
- Integrate with existing V2_SWARM services

### Webhook Integration
- Automatic DevLog posting to Discord
- Agent status notifications
- Swarm coordination alerts

### API Integration
- REST API for external integrations
- Webhook endpoints for third-party services
- Real-time event streaming

---

## 🎯 Future Enhancements

### Planned Features
- **Voice Commands**: Discord voice channel integration
- **File Attachments**: Handle file uploads from agents
- **Interactive Embeds**: Rich interactive Discord components
- **Agent Conversations**: Multi-turn agent conversations
- **Performance Analytics**: Detailed command and response metrics

### Integration Possibilities
- **GitHub Integration**: Automated PR reviews and notifications
- **CI/CD Integration**: Build status and deployment notifications
- **Monitoring Integration**: System health and performance alerts
- **Calendar Integration**: Meeting scheduling and coordination

---

## 📞 Support & Documentation

### Documentation
- This README: Complete setup and usage guide
- Code Documentation: Inline comments and docstrings
- Configuration Guide: `config/discord_bot_config.json`

### Getting Help
1. Run `!help` in Discord for command reference
2. Check test suite: `python -m pytest tests/functional/test_run_discord_agent_bot.py tests/unit/test_discord_commander_*.py`
3. Review bot logs for error details
4. Check agent inboxes for message delivery

### Contributing
- Extend command parser for new features
- Add new agent communication methods
- Enhance Discord embed formatting
- Improve error handling and logging

---

## 🐝 WE ARE SWARM - Discord Integration Complete

**The V2_SWARM Discord Agent Bot represents a revolutionary advancement in swarm intelligence coordination. By enabling real-time, natural language interaction with individual agents through Discord, we've created a powerful interface for external coordination and collaboration.**

**This system transforms V2_SWARM from an internal coordination platform into an externally accessible swarm intelligence system, opening new possibilities for collaborative AI development and coordination.**

**Key Achievements:**
✅ **Real-time Agent Prompting** - Direct communication with individual agents
✅ **Swarm Coordination** - Broadcast messaging to all agents simultaneously
✅ **Status Monitoring** - Real-time agent status and activity tracking
✅ **Rich Discord Integration** - Beautiful embeds and interactive responses
✅ **Security & Permissions** - Configurable access controls and rate limiting
✅ **Comprehensive Testing** - Full test suite for reliability assurance

**Next Steps:**
1. **Deploy Bot**: Set up Discord bot token and invite to server
2. **Configure Permissions**: Set up channel and user restrictions as needed
3. **Test Integration**: Run test suite and verify all functionality
4. **Train Users**: Demonstrate commands and best practices
5. **Monitor Usage**: Track performance and gather feedback

**The Discord Agent Bot is now ready for deployment and represents a significant milestone in V2_SWARM's evolution toward external accessibility and collaborative intelligence!**

**🐝 WE ARE SWARM - EXTERNAL COORDINATION ENABLED! 🐝**
