# 💬 **CAPTAIN'S HANDBOOK - DISCORD INTEGRATION COMMANDS**

## **Complete Discord Communication & Devlog System**
**V2 Compliance**: Automated devlog posting and swarm-external communication

**Author**: Agent-6 - Coordination & Communication Specialist
**Last Updated**: 2025-09-09
**Status**: ACTIVE - Complete Discord Integration Documentation

---

## 🎯 **OVERVIEW**

The Discord Integration system provides seamless communication between the swarm and external stakeholders through automated devlog posting, real-time notifications, and structured communication workflows.

**Integration Components**:
- **Devlog Automation**: Automatic posting of development logs to Discord
- **Enhanced Discord Bot**: Advanced bot with swarm intelligence integration
- **Notification System**: Real-time alerts and status updates
- **Command Processing**: Discord command interface for swarm operations

---

## 🤖 **ENHANCED DISCORD BOT SYSTEM**

### **1. Discord Commander Setup**
```bash
python src/discord_commander/discord_commander.py
```

**Description**: Main Discord bot command processor with swarm integration and intelligent command handling.

**Core Features**:
- **Command Processing**: Handle Discord commands and translate to swarm actions
- **Swarm Integration**: Direct communication with all swarm agents
- **Authentication**: Secure command validation and permission management
- **Logging**: Comprehensive command execution logging

**Supported Commands**:
- **Status Commands**: Get swarm status and agent information
- **Task Commands**: Assign tasks and monitor progress
- **Communication Commands**: Send messages to specific agents
- **Devlog Commands**: Trigger devlog posting and management

**Configuration**:
```bash
# Environment variables required
DISCORD_BOT_TOKEN=your_bot_token_here
DISCORD_CHANNEL_ID=target_channel_id
COMMAND_PREFIX=!
```

### **2. Enhanced Discord Integration**
```bash
python src/discord_commander/enhanced_discord_integration.py
```

**Description**: Advanced Discord integration with enhanced devlog posting and swarm intelligence features.

**Enhanced Features**:
- **Smart Devlog Posting**: Intelligent devlog formatting and categorization
- **Swarm Status Integration**: Real-time swarm status in Discord presence
- **Automated Notifications**: Event-driven notifications to Discord
- **Command Intelligence**: AI-powered command understanding and execution

**Integration Capabilities**:
- **Devlog Categories**: Automatic categorization (feature, bug, documentation, etc.)
- **Status Updates**: Live swarm status in Discord bot status
- **Alert System**: Critical event notifications to designated channels
- **Command History**: Persistent command execution history

---

## 📝 **DEVLOG AUTOMATION SCRIPTS**

### **3. Enhanced Discord Poster**
```bash
python post_devlog_to_discord.py <devlog_path>
```

**Description**: Automated devlog posting system with intelligent formatting and categorization.

**Posting Features**:
- **Smart Formatting**: Automatic devlog formatting based on content analysis
- **Category Detection**: Intelligent categorization of devlog entries
- **Image Support**: Screenshot and diagram attachment support
- **Link Integration**: Automatic link embedding and validation

**Supported Devlog Types**:
- **Feature Devlogs**: New feature implementations and updates
- **Bug Fix Devlogs**: Bug fixes and issue resolutions
- **Documentation Devlogs**: Documentation updates and improvements
- **System Devlogs**: System maintenance and optimization updates

**Example Usage**:
```bash
# Post feature devlog with image
python post_devlog_to_discord.py <devlog_path> --type feature --title "Vector Database Integration" --content "Completed vector database integration with enhanced search capabilities" --image screenshot.png

# Post bug fix devlog
python post_devlog_to_discord.py <devlog_path> --type bugfix --title "Import Error Resolution" --content "Fixed circular import issues in messaging core"
```

### **4. Post Devlog to Discord**
```bash
python post_devlog_to_discord.py
```

**Description**: Direct devlog posting utility for immediate Discord publication.

**Quick Posting Features**:
- **Template Support**: Pre-defined devlog templates for common scenarios
- **Priority Levels**: Urgent, high, normal, low priority posting
- **Tag System**: Devlog tagging for better organization
- **Batch Posting**: Multiple devlog posting in single operation

**Posting Templates**:
```bash
# Feature completion template
python post_devlog_to_discord.py --template feature_complete --agent Agent-2 --task "V2 Compliance Refactoring"

# Bug fix template
python post_devlog_to_discord.py --template bug_fix --issue "Import Error" --solution "Circular dependency resolution"

# System update template
python post_devlog_to_discord.py --template system_update --component "Vector Database" --status "Operational"
```

### **5. Discord Devlog Poster**
```bash
python scripts/execution/run_discord_bot.py
```

**Description**: Execution script for running the Discord devlog posting service.

**Service Features**:
- **Continuous Operation**: 24/7 devlog posting service
- **Queue Management**: Devlog queue processing and prioritization
- **Error Recovery**: Automatic retry and error recovery mechanisms
- **Performance Monitoring**: Posting success rate and performance metrics

---

## 🔧 **DISCORD SETUP & CONFIGURATION**

### **6. Enhanced Discord Setup**
```bash
python scripts/setup_enhanced_discord.py
```

**Description**: Complete Discord bot setup and configuration automation.

**Setup Process**:
1. **Bot Creation**: Automated Discord application and bot creation
2. **Permission Configuration**: Proper permission setup for swarm operations
3. **Channel Setup**: Automatic channel creation and configuration
4. **Webhook Integration**: Webhook setup for enhanced posting capabilities
5. **Testing**: Comprehensive setup validation and testing

**Configuration Options**:
```bash
# Basic setup
python scripts/setup_enhanced_discord.py --basic

# Advanced setup with custom channels
python scripts/setup_enhanced_discord.py --advanced --channels "devlogs,alerts,status"

# Enterprise setup with multiple servers
python scripts/setup_enhanced_discord.py --enterprise --servers 3
```

### **7. Discord Bot Setup Utility**
```bash
python scripts/utilities/setup_discord_bot.py
```

**Description**: Utility script for Discord bot configuration and management.

**Bot Management Operations**:
- **Token Management**: Secure bot token storage and rotation
- **Permission Auditing**: Bot permission validation and correction
- **Channel Access**: Verify and configure channel access permissions
- **Integration Testing**: End-to-end bot functionality testing

**Management Commands**:
```bash
# Audit bot permissions
python scripts/utilities/setup_discord_bot.py --audit-permissions

# Test bot connectivity
python scripts/utilities/setup_discord_bot.py --test-connectivity

# Update bot configuration
python scripts/utilities/setup_discord_bot.py --update-config --token new_token
```

---

## 🧪 **DISCORD TESTING & VALIDATION**

### **8. Enhanced Discord Testing**
```bash
python scripts/test_enhanced_discord.py
```

**Description**: Comprehensive testing suite for Discord integration functionality.

**Testing Categories**:
- **Connectivity Tests**: Discord API connectivity and authentication
- **Posting Tests**: Devlog posting functionality and formatting
- **Command Tests**: Bot command processing and execution
- **Integration Tests**: End-to-end swarm-Discord integration
- **Performance Tests**: Posting speed and reliability testing

**Test Scenarios**:
```bash
# Full integration test
python scripts/test_enhanced_discord.py --full-suite

# Posting performance test
python scripts/test_enhanced_discord.py --performance-test --iterations 100

# Command processing test
python scripts/test_enhanced_discord.py --command-test --commands "status,task,devlog"
```

### **9. Admin Commander Execution**
```bash
python scripts/execution/run_admin_commander.py
```

**Description**: Administrative command execution system for Discord bot management.

**Administrative Features**:
- **Bot Management**: Start, stop, restart Discord bot services
- **Configuration Updates**: Dynamic configuration updates without restart
- **Monitoring**: Real-time bot performance and health monitoring
- **Troubleshooting**: Automated diagnostic and repair operations

---

## 📊 **DEVLOG MANAGEMENT SYSTEM**

### **10. Simple Discord Devlog Poster**
```bash
python post_devlog_to_discord.py <devlog_path>
```

**Description**: Simplified devlog posting utility for quick, straightforward posting.

**Simple Posting Features**:
- **One-Command Posting**: Single command devlog posting
- **Minimal Configuration**: Reduced setup requirements
- **Template Library**: Pre-built templates for common devlog types
- **Error Handling**: Simple error reporting and recovery

**Quick Posting Examples**:
```bash
# Quick feature update
python post_devlog_to_discord.py <devlog_path> --quick "Completed V2 compliance refactoring for Agent-2"

# Status update
python post_devlog_to_discord.py <devlog_path> --status "System operational - all agents active"

# Alert posting
python post_devlog_to_discord.py <devlog_path> --alert "Critical: Database connection issues detected"
```

### **11. Post Devlog Discord Bot**
```bash
python post_devlog_to_discord.py <devlog_path>
```

**Description**: Dedicated Discord bot service for devlog posting and management.

**Bot Service Features**:
- **Automated Posting**: Scheduled and event-driven devlog posting
- **Queue Processing**: Devlog queue management and processing
- **Formatting**: Intelligent devlog formatting and presentation
- **Interaction**: Discord user interaction and feedback collection

---

## 🎯 **COMMAND WORKFLOWS**

### **Complete Discord Integration Setup Workflow**
```bash
# 1. Initial setup
python scripts/setup_enhanced_discord.py --basic

# 2. Bot configuration
python scripts/utilities/setup_discord_bot.py --audit-permissions

# 3. Integration testing
python scripts/test_enhanced_discord.py --full-suite

# 4. Service startup
python scripts/execution/run_discord_bot.py

# 5. First devlog post
python post_devlog_to_discord.py <devlog_path> --type system --title "Discord Integration Complete" --content "Swarm-Discord integration successfully established"
```

### **Devlog Automation Workflow**
```bash
# 1. Post feature completion
python post_devlog_to_discord.py <devlog_path> --type feature --title "Agent-2 Mission Complete" --content "System Architecture Optimization mission completed with exceptional success"

# 2. Post status update
python post_devlog_to_discord.py <devlog_path> --status "All agents operational - V2 compliance at 99.7%"

# 3. Post system alert if needed
python post_devlog_to_discord.py <devlog_path> --alert "Warning: High memory usage detected in Agent-7 workspace"
```

### **Discord Maintenance Workflow**
```bash
# 1. Test connectivity
python scripts/test_enhanced_discord.py --connectivity-test

# 2. Audit permissions
python scripts/utilities/setup_discord_bot.py --audit-permissions

# 3. Performance check
python scripts/test_enhanced_discord.py --performance-test

# 4. Service restart if needed
python scripts/execution/run_admin_commander.py --restart-bot
```

---

## 📋 **COMMAND QUICK REFERENCE**

| Component | Primary Command | Purpose | Key Parameters |
|-----------|-----------------|---------|----------------|
| **Bot Commander** | `src/discord_commander/discord_commander.py` | Main bot processor | `--help` |
| **Enhanced Integration** | `src/discord_commander/enhanced_discord_integration.py` | Advanced features | `--help` |
| **Devlog Poster** | `post_devlog_to_discord.py` | Unified posting | `<devlog_path>` |
| **Quick Poster** | `post_devlog_to_discord.py` | Direct posting | `--template`, `--agent`, `--task` |
| **Bot Service** | `scripts/execution/run_discord_bot.py` | Service runner | N/A |
| **Setup Script** | `scripts/setup_enhanced_discord.py` | Bot setup | `--basic`, `--advanced` |
| **Bot Utility** | `scripts/utilities/setup_discord_bot.py` | Bot management | `--audit-permissions` |
| **Testing Suite** | `scripts/test_enhanced_discord.py` | Integration testing | `--full-suite` |
| **Admin Runner** | `scripts/execution/run_admin_commander.py` | Admin operations | `--restart-bot` |
| **Devlog Poster** | `post_devlog_to_discord.py` | Unified posting | `<devlog_path>` |
| **Bot Service** | `scripts/execution/run_discord_bot.py` | Service runner | N/A |

---

## ⚙️ **CONFIGURATION & ENVIRONMENT**

### **Required Environment Variables**
```bash
# Discord Bot Configuration
DISCORD_BOT_TOKEN=your_bot_token_here
DISCORD_CHANNEL_ID=target_channel_id
DISCORD_GUILD_ID=server_guild_id

# Devlog Configuration
DEVLOG_CHANNEL_ID=devlog_channel_id
ALERT_CHANNEL_ID=alert_channel_id
STATUS_CHANNEL_ID=status_channel_id

# Integration Settings
COMMAND_PREFIX=!
MAX_MESSAGE_LENGTH=2000
RATE_LIMIT_PER_MINUTE=30
```

### **Configuration File Structure**
```json
{
  "discord": {
    "bot_token": "your_token",
    "channels": {
      "devlogs": "channel_id",
      "alerts": "channel_id",
      "status": "channel_id"
    },
    "permissions": {
      "read_messages": true,
      "send_messages": true,
      "embed_links": true,
      "attach_files": true
    }
  },
  "devlog": {
    "auto_post": true,
    "categories": ["feature", "bugfix", "system", "documentation"],
    "templates": {
      "feature": "🚀 **Feature Complete**: {title}\n{content}",
      "bugfix": "🐛 **Bug Fixed**: {title}\n{content}",
      "system": "⚙️ **System Update**: {title}\n{content}"
    }
  }
}
```

---

## 🚨 **TROUBLESHOOTING & MONITORING**

### **Common Issues & Solutions**

**Issue**: Bot fails to connect to Discord
**Solution**: Verify bot token, check Discord API status, validate permissions
```bash
python scripts/test_enhanced_discord.py --connectivity-test
```

**Issue**: Devlog posting fails
**Solution**: Check channel permissions, verify message length, test webhook
```bash
python scripts/utilities/setup_discord_bot.py --audit-permissions
```

**Issue**: Commands not processing
**Solution**: Verify command prefix, check bot permissions, test command parsing
```bash
python scripts/test_enhanced_discord.py --command-test
```

**Issue**: High latency or slow responses
**Solution**: Check rate limits, optimize posting frequency, monitor API usage
```bash
python scripts/test_enhanced_discord.py --performance-test
```

### **Monitoring & Health Checks**
```bash
# Check bot health
python scripts/execution/run_admin_commander.py --health-check

# Monitor posting performance
python scripts/test_enhanced_discord.py --performance-monitor

# Audit recent activity
python scripts/utilities/setup_discord_bot.py --activity-audit
```

---

## 📈 **INTEGRATION WITH SWARM OPERATIONS**

### **Captain's Discord Oversight**
- **Daily Status**: Post daily swarm status updates to Discord
- **Mission Completions**: Automated devlog posting for mission completions
- **Alert System**: Critical alerts automatically posted to Discord
- **External Communication**: Discord as primary external communication channel

### **Agent Integration Points**
- **Devlog Posting**: All agents can post devlogs via Discord integration
- **Status Updates**: Real-time status updates visible in Discord
- **Command Interface**: Discord commands can trigger swarm operations
- **Alert Notifications**: Agents receive critical alerts via Discord

### **Enhanced Communication Protocol**
1. **Agent Actions**: Agents complete tasks and generate devlogs
2. **Automated Posting**: Devlogs automatically posted to Discord
3. **Captain Review**: Captain monitors Discord for swarm status
4. **External Updates**: Stakeholders receive updates via Discord
5. **Feedback Loop**: Discord feedback incorporated into swarm operations

---

**✅ DISCORD INTEGRATION COMPLETE**
**11 Commands Documented | All Workflows Covered | External Communication Ready**

**Ready for swarm-external communication and automated devlog posting!** 🚀⚡
