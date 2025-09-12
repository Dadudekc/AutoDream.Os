# Unified DevLog Routing System - V2_SWARM Agent Channel Integration

## Overview

The Unified DevLog Routing System provides a comprehensive solution for routing agent-specific devlog entries to their dedicated Discord channels. Unlike the previous monitoring-based approach, this system uses explicit agent flags for reliable, on-demand routing.

## Key Changes from Previous Versions

### Before: Complex Monitoring System
- ❌ Filesystem monitoring with watchdog
- ❌ Automatic file detection and pattern matching
- ❌ Background processes and complex dependencies
- ❌ Error-prone agent identification

### After: Unified Explicit System
- ✅ **Explicit agent flags** for 100% reliable routing
- ✅ **Direct file processing** without monitoring
- ✅ **Simulation mode** for safe testing
- ✅ **Standalone operation** with minimal dependencies
- ✅ **Comprehensive error handling** and validation

## Features

- **Real-time Monitoring**: Automatically detects new and modified devlog files
- **Intelligent Agent Detection**: Extracts agent information from filenames and content
- **Channel-specific Routing**: Sends devlogs to the correct agent channel based on agent ID
- **Duplicate Prevention**: Maintains a cache of processed files to avoid duplicate notifications
- **Category Classification**: Automatically categorizes devlogs (consolidation, cleanup, coordination, etc.)
- **Error Handling**: Comprehensive error handling and logging

## Agent Channel Configuration

The system is configured with the following agent-specific Discord channels:

| Agent ID | Channel ID | Description |
|----------|------------|-------------|
| Agent-1 | 1387514611351421079 | Integration & Core Systems Specialist |
| Agent-2 | 1387514933041696900 | Architecture & Design Specialist |
| Agent-3 | 1387515009621430392 | DevOps Specialist |
| Agent-4 | 1387514978348826664 | QA & Captain Channel |
| Agent-5 | 1415916580910665758 | Agent-5 Channel |
| Agent-6 | 1415916621847072828 | Communication Specialist |
| Agent-7 | 1415916665283022980 | Web Development Channel |
| Agent-8 | 1415916707704213565 | Coordination Channel |

## How It Works

### 1. File Detection
The system monitors the `devlogs/` directory using filesystem watchers that detect:
- New devlog file creation
- Existing devlog file modifications
- Recursive monitoring of subdirectories

### 2. Agent Identification
The system identifies the agent associated with each devlog through multiple methods:

**Filename Patterns:**
- `Agent-1_something.md` → Agent-1
- `agent1_coordination.md` → Agent-1
- `Agent-2_status_update.md` → Agent-2

**Content Analysis:**
- Searches for agent mentions in the devlog content
- Recognizes patterns like "Agent-1", "agent one", etc.

### 3. Content Processing
For each devlog file, the system:
- Extracts the title from the first markdown header
- Determines the category based on keywords in the content
- Limits content length for Discord embed compatibility
- Creates structured metadata

### 4. Channel Routing
Devlogs are routed to the appropriate Discord channel based on:
- Agent ID extracted from the file
- Channel configuration in `config/discord_channels.json`
- Fallback to general channels if agent-specific routing fails

### 5. Duplicate Prevention
The system maintains a processing cache (`.processed_cache.json`) to:
- Track which files have been processed
- Prevent duplicate notifications for the same devlog
- Handle file modifications gracefully

## Setup Instructions

### 1. Prerequisites
```bash
pip install requests
```

### 2. Configuration
Ensure your `config/discord_channels.json` contains the correct channel IDs:

```json
{
  "agent-1": {
    "name": "agent-1",
    "channel_id": "1387514611351421079",
    "agent": "Agent-1",
    "enabled": true
  }
}
```

### 3. Environment Setup (Optional)
For full Discord API integration with bot tokens:
```bash
export DISCORD_BOT_TOKEN="your_bot_token_here"
```

### 4. Usage
```bash
# Send devlog to Agent-1's channel
python scripts/send_devlog_unified.py --agent Agent-1 --file devlogs/status.md

# Test with simulation mode (safe)
python scripts/send_devlog_unified.py --agent Agent-1 --file devlogs/status.md --simulate
```

## Usage Examples

### Creating a DevLog
Create a devlog file in the `devlogs/` directory:

```markdown
# Agent-1 Consolidation Status Update

## Overview
Completed vector database integration consolidation.

## Details
- Merged 3 vector database modules into unified system
- Reduced code duplication by 60%
- Maintained all existing functionality

## Next Steps
- Test consolidated system
- Update documentation

**Agent-1 - Integration Specialist**
```

### Manual Processing with Explicit Routing
To send this devlog to Agent-1's channel, run:

```bash
python scripts/send_devlog_unified.py --agent Agent-1 --file devlogs/2025-09-12_Agent-1_Consolidation_Update.md
```

The system will:
1. Validate the agent flag and file path
2. Parse the content and extract the title
3. Classify it as a "consolidation" category (based on keywords)
4. Route it to Agent-1's Discord channel (ID: 1387514611351421079)
5. Send a formatted embed with the devlog content

### Simulation Mode for Testing
Test without actually sending to Discord:

```bash
python scripts/send_devlog_unified.py --agent Agent-1 --file devlogs/2025-09-12_Agent-1_Consolidation_Update.md --simulate
```

## Discord Embed Format

Devlogs are sent as rich Discord embeds with:
- **Title**: Extracted from the first markdown header
- **Description**: Devlog content (truncated to 1500 characters)
- **Agent Field**: Agent ID who created the devlog
- **Category Field**: Auto-detected category
- **Timestamp Field**: When the devlog was processed
- **Footer**: V2_SWARM branding with agent avatar

## Categories

The system automatically detects these categories:

| Category | Keywords |
|----------|----------|
| consolidation | consolidation, merge, unify |
| cleanup | cleanup, remove, delete, mission |
| coordination | coordination, swarm, agent, communication |
| testing | test, testing, verify, validation |
| deployment | deploy, deployment, release |
| general | default category |

## Troubleshooting

### Common Issues

**1. Agent Not Detected**
```
⚠️  Could not determine agent for devlog: filename.md
```
**Solution**: Ensure the filename contains agent information like `Agent-1_` or the content mentions the agent.

**2. Channel Not Found**
```
⚠️  No Discord channel found for Agent-X
```
**Solution**: Check that the agent has a configured channel in `config/discord_channels.json`.

**3. Webhook/Channel ID Missing**
```
⚠️  No webhook URL or channel ID configured for agent-x
```
**Solution**: Add webhook URL or channel ID to the channel configuration.

### Monitoring Logs
The system provides detailed logging:
- File detection events
- Agent identification results
- Routing success/failure
- Error conditions

## System Architecture

### Current Implementation
```
Command → Agent Flag + File Path → Direct Processing → Discord Channel
                ↑
          Explicit Control
          Immediate Execution
          Minimal Dependencies
          100% Reliable Routing
          No Background Processes
```

### Core Components
- **send_devlog_unified.py**: Main unified sender script
- **Enhanced Discord Integration**: Webhook and channel ID support
- **Configuration System**: Agent channel mappings in JSON
- **Content Processing**: Markdown parsing and categorization
- **Error Handling**: Comprehensive validation and error reporting

## Future Enhancements

### Planned Features
- **Webhook URL Setup**: Automated webhook creation for channels
- **Bot Integration**: Full Discord API integration with bot token
- **Interactive Commands**: Discord commands to query devlog history
- **Cross-Agent Coordination**: Routing devlogs mentioning multiple agents
- **Priority Routing**: High-priority devlogs get special formatting
- **Analytics Dashboard**: Devlog activity metrics and insights
- **Batch Processing**: Send multiple devlogs at once
- **Template System**: Pre-configured devlog templates

### API Integration
For full Discord API functionality:
1. Create a Discord bot application
2. Add bot to your server with appropriate permissions
3. Set `DISCORD_BOT_TOKEN` environment variable
4. Enable channel-specific messaging

## Support

For issues or questions about the DevLog Routing System:
- Check the processing logs for error details
- Verify agent naming conventions in devlog files
- Ensure Discord channel configuration is correct
- Review the `.processed_cache.json` for processing status

---

**V2_SWARM DevLog Routing System - Keeping agents connected and informed!** 🐝📝
