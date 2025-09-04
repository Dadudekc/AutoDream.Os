# Discord Commander - Swarm Coordination System

## 🚀 Overview

The Discord Commander is a comprehensive Discord bot designed for real-time swarm coordination and command execution across the agent network. It integrates seamlessly with the unified logging system and provides centralized control for swarm operations.

## 🎯 Features

### Core Functionality
- **Real-time Swarm Status**: Live monitoring of all agents and swarm health
- **Command Execution**: Execute commands on individual agents or broadcast to all
- **Mission Management**: Track and coordinate active missions across agents
- **Cycle Tracking**: Monitor cycle-based progress and efficiency ratings
- **Health Monitoring**: System health indicators and performance metrics

### Discord Integration
- **Auto Channel Creation**: Automatically creates required channels (commands, status, logs)
- **Rich Embeds**: Beautiful, informative embed messages for all operations
- **Role-based Access**: Captain and Agent role permissions
- **Message Logging**: Comprehensive logging of all Discord communications
- **Real-time Updates**: Live status updates and progress notifications

### Swarm Commands

#### Status Commands
- `!status` - Get current swarm status overview
- `!agents` - List all agents and their current status
- `!cycle` - Get current cycle information and progress
- `!missions` - List all active missions
- `!tasks` - List pending tasks
- `!health` - Get system health report

#### Captain Commands (Require Captain role)
- `!execute <agent> <command>` - Execute command on specific agent
- `!broadcast <command>` - Broadcast command to all active agents
- `!update <key> <value>` - Update swarm status (efficiency, cycle, health, etc.)
- `!message_captain <prompt>` - Send human prompt directly to Agent-4 (Captain)

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Discord Bot Token
- Discord Server (Guild) with appropriate permissions

### Installation Steps

1. **Clone and Install Dependencies**
   ```bash
   # Install Discord Commander dependencies
   pip install -r requirements-discord.txt
   ```

2. **Create Discord Application**
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new application
   - Go to "Bot" section and create a bot
   - Copy the bot token

3. **Configure Environment Variables**
   ```bash
   # Create .env file or set environment variables
   export DISCORD_BOT_TOKEN="your_bot_token_here"
   export DISCORD_GUILD_ID="your_guild_id_here"
   export DISCORD_COMMAND_CHANNEL="swarm-commands"
   export DISCORD_STATUS_CHANNEL="swarm-status"
   export DISCORD_LOG_CHANNEL="swarm-logs"
   ```

4. **Configure Bot Permissions**
   - In Discord Developer Portal, go to "OAuth2" → "URL Generator"
   - Select scopes: `bot`, `applications.commands`
   - Select permissions:
     - Send Messages
     - Use Slash Commands
     - Embed Links
     - Read Message History
     - Mention Everyone
     - Manage Channels (for auto channel creation)

5. **Invite Bot to Server**
   - Use the generated OAuth2 URL to invite the bot to your Discord server
   - Ensure the bot has the "Captain" role for admin commands

6. **Run the Discord Commander**
   ```bash
   python src/discord_commander.py
   ```

## ⚙️ Configuration

### Environment Variables
- `DISCORD_BOT_TOKEN` - Your Discord bot token (required)
- `DISCORD_GUILD_ID` - Your Discord server ID (required)
- `DISCORD_COMMAND_CHANNEL` - Channel for command execution (default: "swarm-commands")
- `DISCORD_STATUS_CHANNEL` - Channel for status updates (default: "swarm-status")
- `DISCORD_LOG_CHANNEL` - Channel for message logging (default: "swarm-logs")

### Role Configuration
- **Captain Role**: Required for admin commands (`!execute`, `!broadcast`, `!update`)
- **Agent Roles**: Automatically recognized (Agent-1 through Agent-8)
- **Admin Permissions**: Manage channels permission for auto channel creation

## 📊 Command Reference

### Public Commands (Available to all users)

#### Status Monitoring
```
!status         - Comprehensive swarm status report
!agents         - Agent status overview
!cycle          - Current cycle information
!missions       - Active missions list
!tasks          - Pending tasks list
!health         - System health report
!captain_status - Get Captain Agent-4's current status
```

#### Usage Examples
```
!status
!agents
!cycle
!missions
!tasks
!health
```

### Captain Commands (Require Captain role)

#### Command Execution
```
!execute <agent> <command>    - Execute command on specific agent
!broadcast <command>         - Execute command on all active agents
```

#### Status Updates
```
!update efficiency <value>   - Update efficiency rating (e.g., 8.5)
!update cycle <number>      - Update current cycle number
!update health <status>     - Update system health (HEALTHY/WARNING/CRITICAL)
!update add_agent <name>    - Add agent to active list
!update remove_agent <name> - Remove agent from active list
!update add_mission <text>  - Add active mission
```

#### Usage Examples
```
!execute Agent-7 "deploy unified-logging-system"
!broadcast "status update"
!update efficiency 8.5
!update cycle 5
!update health HEALTHY
!update add_mission "Cycle 4 Architecture Validation"
```

### Agent-4 (Captain) Specific Commands

#### Direct Captain Communication
- `!message_captain <prompt>` - Send human prompt directly to Agent-4's inbox
- `!captain_status` - Get Captain Agent-4's current status and mission

#### Usage Examples for Captain Communication
```
!message_captain "Please provide strategic guidance on the latest technical debt elimination breakthrough"
!captain_status
```

### Agent-4 Messaging Features

The Discord Commander now includes specialized functionality for direct communication with Agent-4 (Captain):

#### Human Prompt Messaging
- **Direct Inbox Delivery**: Messages sent using `!message_captain` are delivered directly to Agent-4's inbox
- **Human Prompt Format**: Messages are automatically formatted as `[HUMAN PROMPT]` for proper processing
- **Real-time Delivery**: Messages appear instantly in Agent-4's inbox for immediate attention
- **Sender Tracking**: All messages include sender information for accountability

#### Captain Status Integration
- **Real-time Status**: Get live updates on Captain Agent-4's current mission and status
- **Task Monitoring**: View Captain's current tasks and priorities
- **Mission Tracking**: Monitor Captain's strategic objectives and progress

## 🔧 Architecture Integration

### Unified Logging System Integration
The Discord Commander integrates with the unified logging system:
- Automatic logging of all Discord messages
- Command execution logging with timestamps
- Error tracking and reporting
- Performance metrics collection

### Swarm Status Synchronization
- Real-time synchronization with swarm status
- Automatic agent status updates
- Mission progress tracking
- Cycle-based progress reporting

### Command Pattern Implementation
- Modular command structure with role-based access
- Async command execution with progress tracking
- Error handling and recovery mechanisms
- Command history and audit trail

## 🚨 Security & Permissions

### Role-Based Access Control
- **Captain Role**: Full administrative access
- **Agent Roles**: Read-only access to status information
- **Public Access**: Basic status monitoring commands

### Security Best Practices
- Bot token encryption (environment variables)
- Command validation and sanitization
- Rate limiting for command execution
- Audit logging for all administrative actions
- Secure channel permissions

## 📈 Monitoring & Analytics

### Built-in Monitoring
- Command execution statistics
- Agent activity tracking
- Mission progress analytics
- System health indicators
- Performance metrics dashboard

### Integration with Unified Systems
- Logs all activities to unified logging system
- Integrates with performance monitoring
- Supports real-time status updates
- Provides comprehensive audit trails

## 🔄 Auto Channel Management

The Discord Commander automatically creates and manages required channels:
- **swarm-commands**: Command execution and coordination
- **swarm-status**: Real-time status updates and reports
- **swarm-logs**: Comprehensive message and activity logging

## 🚦 Status Indicators

### Agent Status
- 🟢 **Active**: Agent is online and operational
- 🔴 **Inactive**: Agent is offline or unavailable
- 🟡 **Busy**: Agent is executing commands

### System Health
- 🟢 **HEALTHY**: All systems operational
- 🟡 **WARNING**: Minor issues detected
- 🔴 **CRITICAL**: Major issues requiring attention

### Command Status
- 🟡 **Executing**: Command is being processed
- ✅ **Completed**: Command executed successfully
- ❌ **Failed**: Command execution failed
- 🚫 **Error**: Command execution error

## 🐛 Troubleshooting

### Common Issues

**Bot Not Responding**
1. Check bot token validity
2. Verify bot permissions in Discord server
3. Check bot online status
4. Review console logs for errors

**Command Permission Errors**
1. Ensure user has correct role (Captain for admin commands)
2. Check role hierarchy in Discord server
3. Verify bot has necessary permissions

**Channel Creation Errors**
1. Ensure bot has "Manage Channels" permission
2. Check server permissions and role hierarchy
3. Verify bot is not rate-limited

### Debug Mode
Enable debug logging by setting environment variable:
```bash
export DISCORD_DEBUG=true
```

## 📚 API Reference

### DiscordCommander Class
```python
from discord_commander import DiscordCommander

# Initialize bot
bot = DiscordCommander()

# Start bot
await bot.start("your_bot_token")
```

### Swarm Status Management
```python
# Update swarm status
await bot.update_swarm_status("efficiency", "8.5")
await bot.update_swarm_status("cycle", "4")
await bot.update_swarm_status("health", "HEALTHY")
```

### Command Execution
```python
# Execute command on agent
result = await bot._execute_agent_command("Agent-7", "status")

# Broadcast to all agents
results = await bot._broadcast_command("update_status")
```

## 🤝 Contributing

### Development Guidelines
1. Follow async/await patterns for all Discord operations
2. Use embed messages for rich information display
3. Implement proper error handling and logging
4. Follow role-based access control patterns
5. Maintain compatibility with unified logging system

### Code Standards
- Use type hints for all function parameters
- Implement comprehensive docstrings
- Follow PEP 8 style guidelines
- Use descriptive variable and function names
- Include error handling for all external operations

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🚀 Quick Start

1. **Setup Environment**
   ```bash
   pip install -r requirements-discord.txt
   export DISCORD_BOT_TOKEN="your_token"
   export DISCORD_GUILD_ID="your_guild_id"
   ```

2. **Launch Bot**
   ```bash
   python src/discord_commander.py
   ```

3. **Invite to Discord**
   - Use OAuth2 URL with bot permissions
   - Assign "Captain" role for admin access

4. **Start Commanding**
   ```
   !status
   !execute Agent-7 "deploy unified-logging-system"
   !broadcast "system health check"
   ```

**WE. ARE. SWARM. ⚡️🔥**

The Discord Commander is now ready to provide comprehensive swarm coordination and command execution capabilities for your agent network!
