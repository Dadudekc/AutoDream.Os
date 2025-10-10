# MCP Servers for Agent Swarm

This directory contains Model Context Protocol (MCP) servers that expose Agent Swarm capabilities.

## Swarm Messaging Server

Exposes the swarm messaging system via MCP, allowing agents and external tools to send messages to agents via PyAutoGUI coordinates.

### Configuration

Add to your MCP settings (e.g., Claude Desktop config):

```json
{
  "mcpServers": {
    "swarm-messaging": {
      "command": "python",
      "args": ["D:/Agent_Cellphone_V2_Repository/mcp_servers/messaging_server.py"]
    }
  }
}
```

### Available Tools

1. **send_agent_message**: Send message to specific agent
   - `agent_id`: Target agent (Agent-1 through Agent-8)
   - `message`: Message content
   - `priority`: "regular" or "urgent"

2. **broadcast_message**: Send message to all agents
   - `message`: Message content
   - `priority`: "regular" or "urgent"

3. **get_agent_coordinates**: Get coordinates and status for all agents
   - Returns: Agent positions, active status, descriptions

### Usage Examples

```python
# Send message to Agent-1
send_agent_message(
    agent_id="Agent-1",
    message="Execute vector consolidation now",
    priority="urgent"
)

# Broadcast to all agents
broadcast_message(
    message="V2 compliance check required",
    priority="regular"
)

# Get agent coordinates
get_agent_coordinates()
```

## Integration with Global MCP

The messaging server is designed to work with any MCP-compatible client:
- Claude Desktop
- Cursor IDE
- Custom MCP clients
- Other AI tools with MCP support

This enables seamless swarm coordination from any MCP-enabled environment.



