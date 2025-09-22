# Agent Devlog System Protocols

## Overview

The Agent Devlog System provides a standalone mechanism for agents to post devlogs to Discord channels and vectorize them for database storage. This system operates independently from the Discord bot but uses the same channel configuration.

## Architecture

### System Components

1. **Agent Devlog Posting Service** (`src/services/agent_devlog_posting.py`)
   - Standalone Python script
   - Command-line interface
   - No dependency on Discord bot service

2. **Discord Bot** (`src/services/discord_bot_integrated.py`)
   - Separate interactive service
   - Handles Discord commands and messaging
   - Uses same channel configuration

3. **Shared Channel Configuration**
   - Both systems use environment variables: `DISCORD_CHANNEL_AGENT_1` through `DISCORD_CHANNEL_AGENT_8`
   - Posts to same Discord channels
   - Independent operation

### Data Flow

```
Agent Action → Agent Devlog System → Discord Post + File Save → Vector Database → Cleanup
```

## Usage Protocols

### Command-Line Usage

```bash
# Basic devlog posting
python src/services/agent_devlog_posting.py --agent Agent-4 --action "Task completed"

# With vectorization and cleanup
python src/services/agent_devlog_posting.py --agent Agent-4 --action "Task completed" --vectorize --cleanup

# Dry run (test mode)
python src/services/agent_devlog_posting.py --agent Agent-4 --action "Test" --dry-run
```

### Programmatic Usage

```python
from services.agent_devlog_posting import AgentDevlogPoster
import asyncio

async def create_devlog():
    poster = AgentDevlogPoster()
    success = await poster.post_devlog_with_vectorization(
        agent_flag="Agent-4",
        action="Task completed",
        status="completed",
        details="Implementation finished successfully",
        vectorize=True,
        cleanup=True
    )
    return success
```

### Integration with Messaging System

The consolidated messaging service automatically creates devlogs for message activities:

```python
# In consolidated_messaging_service.py
asyncio.create_task(poster.post_devlog_with_vectorization(
    agent_id=agent_id,
    action=f"Message sent to {agent_id}",
    status="completed",
    details=f"Message from {from_agent}: {message[:200]}...",
    vectorize=True,
    cleanup=True
))
```

## Database Querying Protocols

### Vector Database Integration

Devlogs are stored in the vector database with the following metadata:

```python
{
    "agent_id": "Agent-4",
    "action": "Task completed",
    "status": "completed",
    "details": "Implementation details...",
    "timestamp": "2025-09-21T19:08:22Z",
    "source": "agent_devlog_system",
    "type": "devlog"
}
```

### Querying Devlogs

#### 1. Query by Agent

```python
# Query all devlogs for a specific agent
from vector_database.vector_database_integration import VectorDatabaseIntegration

vector_db = VectorDatabaseIntegration()
agent_devlogs = await vector_db.query(
    query="Agent-4 devlog",
    namespace="agent_devlogs",
    metadata_filter={"agent_id": "Agent-4"}
)
```

#### 2. Query by Status

```python
# Query devlogs by completion status
completed_devlogs = await vector_db.query(
    query="completed tasks",
    namespace="agent_devlogs",
    metadata_filter={"status": "completed"}
)
```

#### 3. Query by Date Range

```python
# Query devlogs from specific time period
from datetime import datetime
recent_devlogs = await vector_db.query(
    query="recent activity",
    namespace="agent_devlogs",
    metadata_filter={
        "timestamp": {
            "$gte": "2025-09-21T00:00:00Z",
            "$lte": "2025-09-21T23:59:59Z"
        }
    }
)
```

#### 4. Semantic Search

```python
# Find devlogs related to specific topics
discord_devlogs = await vector_db.query(
    query="Discord integration work",
    namespace="agent_devlogs"
)

vectorization_devlogs = await vector_db.query(
    query="vector database implementation",
    namespace="agent_devlogs"
)
```

### Database Cleanup

Devlogs can be cleaned up from the database when no longer needed:

```python
# Remove old devlogs
await vector_db.delete_documents(
    namespace="agent_devlogs",
    metadata_filter={
        "timestamp": {"$lt": "2025-01-01T00:00:00Z"}
    }
)
```

## Environment Configuration

### Discord Channels

```env
# Agent-specific Discord channels
DISCORD_CHANNEL_AGENT_1=agent_1_channel_id    # Agent-1 devlogs
DISCORD_CHANNEL_AGENT_2=agent_2_channel_id    # Agent-2 devlogs
DISCORD_CHANNEL_AGENT_3=agent_3_channel_id    # Agent-3 devlogs
DISCORD_CHANNEL_AGENT_4=agent_4_channel_id    # Agent-4 devlogs (Captain)
DISCORD_CHANNEL_AGENT_5=agent_5_channel_id    # Agent-5 devlogs
DISCORD_CHANNEL_AGENT_6=agent_6_channel_id    # Agent-6 devlogs
DISCORD_CHANNEL_AGENT_7=agent_7_channel_id    # Agent-7 devlogs
DISCORD_CHANNEL_AGENT_8=agent_8_channel_id    # Agent-8 devlogs
```

### Required Environment Variables

```env
# Discord Bot (for both systems)
DISCORD_BOT_TOKEN=your_discord_bot_token
DISCORD_CHANNEL_ID=your_main_channel_id

# Vector Database (if using vectorization)
VECTOR_DB_URL=your_vector_database_url
VECTOR_DB_API_KEY=your_vector_database_key
```

## Integration Reminders

### Updated Message Format

The integration reminder has been updated to point to the agent devlog system:

```
📝 AGENT DEVLOG SYSTEM: Use 'python src/services/agent_devlog_posting.py --agent <agent_flag> --action <description>' to automatically post to Discord and vectorize
```

### System Independence

- **Agent Devlog System**: Standalone tool for agents to post devlogs
- **Discord Bot**: Interactive service for Discord commands
- **Shared Channels**: Both systems post to same Discord channels
- **No Direct Connection**: Systems operate independently but complement each other

## Best Practices

### 1. Agent Flag Enforcement
- Always use proper agent flags: `Agent-1` through `Agent-8`
- System validates agent flag format automatically
- Each agent gets their own Discord channel

### 2. Vectorization Strategy
- Use `--vectorize` flag for important devlogs
- Consider using `--cleanup` to maintain clean file structure
- Vectorized devlogs are searchable and retrievable

### 3. Error Handling
- System gracefully handles missing Discord configuration
- File operations always work even if Discord fails
- Vectorization failures don't prevent Discord posting

### 4. Testing
- Use `--dry-run` flag to test without Discord posting
- Verify agent channel configuration before production use
- Check vector database connectivity if using vectorization

## Troubleshooting

### Common Issues

1. **Discord Connection Issues**
   - Check `DISCORD_BOT_TOKEN` environment variable
   - Verify Discord channel IDs are valid
   - Ensure bot has access to specified channels

2. **Vector Database Issues**
   - Verify vector database connection
   - Check namespace permissions
   - Validate metadata format

3. **File System Issues**
   - Ensure `devlogs/` directory exists
   - Check write permissions
   - Verify disk space

### Debug Commands

```bash
# Test configuration
python test_enhanced_devlog_system.py --test-config

# Test dry-run mode
python src/services/agent_devlog_posting.py --agent Agent-4 --action "Test" --dry-run

# Show help
python src/services/agent_devlog_posting.py --show-help

# Discord help command
!devlog_help
```

## Future Enhancements

### Planned Features

1. **Database Query Interface**
   - Web interface for querying devlogs
   - REST API for programmatic access
   - Advanced filtering and search capabilities

2. **Enhanced Analytics**
   - Devlog trend analysis
   - Agent activity patterns
   - Performance metrics and reporting

3. **Integration Improvements**
   - Webhook support for external systems
   - Batch processing capabilities
   - Real-time notification system

### Query Protocol Development

The next phase will focus on developing comprehensive protocols for querying the vectorized devlogs, including:

- **Query API Design**: RESTful endpoints for devlog retrieval
- **Search Interface**: Web-based search and filtering
- **Analytics Dashboard**: Visual representation of devlog data
- **Export Capabilities**: Various formats for data export
- **Real-time Updates**: Live updates for new devlogs

---

**Generated by**: Agent-4 (Quality Assurance Specialist - CAPTAIN)
**Date**: 2025-09-21
**Protocol Version**: 1.0
**Status**: Active and Operational ✅

🐝 **WE ARE SWARM** - Agent Devlog System Protocols

