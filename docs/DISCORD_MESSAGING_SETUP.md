# Discord Messaging Controller Setup Guide

## 🎯 **Overview**

The Discord Messaging Controller provides seamless integration between Discord and the swarm messaging system, allowing users to easily interact with agents through Discord views and commands.

## 🚀 **Features**

### **Interactive Agent Messaging**
- **Discord Views**: Intuitive dropdown selection for agents
- **Message Modals**: Easy message composition with priority settings
- **Real-time Status**: Live agent status indicators (🟢 Active, 🔴 Inactive)

### **Swarm Communication**
- **Broadcast Messaging**: Send messages to all agents simultaneously
- **Status Monitoring**: Real-time swarm status with refresh capabilities
- **Agent Selection**: Interactive agent selection with status indicators

### **User-Friendly Interface**
- **Slash Commands**: Modern Discord slash command interface
- **Rich Embeds**: Beautiful Discord embeds with status information
- **Error Handling**: Comprehensive error handling with user feedback

## 📋 **Available Commands**

### **Core Messaging Commands**

| Command | Description | Usage |
|---------|-------------|-------|
| `/message_agent` | Send message to specific agent | `/message_agent agent_id:"Agent-1" message:"Hello!" priority:"NORMAL"` |
| `/agent_interact` | Interactive messaging interface | `/agent_interact` |
| `/swarm_status` | View current swarm status | `/swarm_status` |
| `/broadcast` | Broadcast to all agents | `/broadcast message:"Important update!" priority:"HIGH"` |
| `/agent_list` | List all available agents | `/agent_list` |
| `/help_messaging` | Get help with messaging commands | `/help_messaging` |

### **Interactive Features**

#### **Agent Messaging View**
- Dropdown selection of all available agents
- Status indicators (🟢 Active, 🔴 Inactive)
- Message composition modal with priority settings
- Real-time delivery confirmation

#### **Swarm Status View**
- Live status of all agents
- Refresh button for real-time updates
- Broadcast message button for quick announcements
- Agent coordinates and status information

## 🔧 **Setup Instructions**

### **1. Prerequisites**
```bash
# Ensure Discord.py is installed
pip install discord.py

# Verify messaging service is available
python -c "from src.services.messaging_service import ConsolidatedMessagingService; print('✅ Messaging service available')"
```

### **2. Environment Configuration**
Create or update your `.env` file:
```env
# Discord Bot Configuration
DISCORD_BOT_TOKEN=your_bot_token_here
DISCORD_CLIENT_ID=your_client_id_here
DISCORD_GUILD_ID=your_guild_id_here

# Messaging Service Configuration
MESSAGING_COORDINATES_PATH=config/coordinates.json
```

### **3. Bot Setup**
1. **Create Discord Application**:
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Create new application
   - Copy Bot Token and Client ID

2. **Invite Bot to Server**:
   - Go to OAuth2 > URL Generator
   - Select `bot` and `applications.commands` scopes
   - Select required permissions: `Send Messages`, `Use Slash Commands`, `Embed Links`
   - Use generated URL to invite bot to your server

3. **Configure Agent Coordinates**:
   - Ensure `config/coordinates.json` contains agent coordinates
   - Verify agent data structure matches expected format

### **4. Launch the Bot**
```bash
# Start the enhanced Discord messaging bot
python run_discord_messaging.py
```

## 🎮 **Usage Examples**

### **Quick Agent Message**
```
/agent_interact
```
Then select agent from dropdown and compose message.

### **Broadcast to All Agents**
```
/broadcast message:"System maintenance in 5 minutes" priority:"HIGH"
```

### **Check Swarm Status**
```
/swarm_status
```
Use refresh button to get latest status.

### **Direct Agent Message**
```
/message_agent agent_id:"Agent-1" message:"Please run status check" priority:"NORMAL"
```

## 🔍 **Troubleshooting**

### **Common Issues**

#### **Bot Not Responding**
- Check bot token in `.env` file
- Verify bot has proper permissions in server
- Check console logs for error messages

#### **Agents Not Found**
- Verify `config/coordinates.json` exists and is valid
- Check agent data structure in messaging service
- Ensure agents are properly configured

#### **Messages Not Sending**
- Check agent coordinates are valid
- Verify messaging service is working
- Check agent status (must be active)

### **Debug Mode**
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python run_discord_messaging.py
```

## 📊 **Status Indicators**

### **Agent Status**
- 🟢 **Active**: Agent is online and ready to receive messages
- 🔴 **Inactive**: Agent is offline or unavailable

### **Message Priority**
- **NORMAL**: Standard priority messages
- **HIGH**: High priority messages
- **CRITICAL**: Critical priority messages

### **Command Results**
- ✅ **Success**: Command executed successfully
- ❌ **Failed**: Command failed with error message
- ⚠️ **Warning**: Non-critical issue detected

## 🔐 **Security Considerations**

### **Bot Permissions**
- Use minimal required permissions
- Regularly rotate bot tokens
- Monitor bot activity logs

### **Message Security**
- Validate all user inputs
- Sanitize message content
- Implement rate limiting for commands

### **Access Control**
- Restrict bot access to authorized channels
- Implement user role-based access if needed
- Monitor command usage patterns

## 📈 **Performance Tips**

### **Optimization**
- Use ephemeral responses for sensitive operations
- Implement command cooldowns for heavy operations
- Cache agent status information when appropriate

### **Monitoring**
- Monitor bot latency and response times
- Track command usage statistics
- Log all messaging operations for audit

## 🆘 **Support**

### **Getting Help**
- Use `/help_messaging` command for quick reference
- Check console logs for detailed error information
- Verify configuration and permissions

### **Reporting Issues**
- Include error messages from console logs
- Provide steps to reproduce the issue
- Include relevant configuration details (sanitized)

---

**🤖 Enhanced Discord Messaging Controller** - Seamless agent communication through Discord interface

