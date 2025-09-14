# Messaging Shared Utilities Guide
=====================================

## Overview

The messaging shared utilities provide a consolidated, V2-compliant way to perform common messaging operations across the entire system. These utilities eliminate code duplication and provide a single source of truth for messaging functionality.

## Key Benefits

- **V2 Compliance**: All utilities are under 300 lines
- **Zero Duplication**: Eliminates 4 major duplicated functions across 79+ files
- **Consistent API**: Standardized interface for all messaging operations
- **Error Handling**: Centralized error handling and logging
- **Performance**: Optimized with caching and efficient operations

## Quick Start

```python
# Import shared utilities
from src.services.messaging.shared import (
    MessagingUtilities,
    broadcast_message,
    list_agents,
    load_coordinates_from_json,
    send_message_pyautogui
)

# Use the class-based approach
utils = MessagingUtilities()
agents = utils.list_agents()
coords = utils.load_coordinates_from_json()

# Or use convenience functions
agents = list_agents()
success = send_message_pyautogui("agent-1", "Hello from shared utilities!")
```

## Available Utilities

### MessagingUtilities Class

The main utility class providing all messaging functionality.

```python
from src.services.messaging.shared import MessagingUtilities

utils = MessagingUtilities()

# Load agent coordinates
coords = utils.load_coordinates_from_json("config/coordinates.json")

# List all available agents
agents = utils.list_agents()

# Get specific agent coordinates
agent_coords = utils.get_agent_coordinates("agent-1")

# Send message to specific agent
success = utils.send_message_pyautogui("agent-1", "Message content")

# Broadcast to all agents
results = utils.broadcast_message("Broadcast message")

# Validate coordinates
validation = utils.validate_coordinates()
```

### Convenience Functions

Direct function imports for backward compatibility.

```python
from src.services.messaging.shared import (
    load_coordinates_from_json,
    list_agents,
    send_message_pyautogui,
    broadcast_message
)

# Load coordinates
coords = load_coordinates_from_json()

# List agents
agents = list_agents()

# Send message
success = send_message_pyautogui("agent-1", "Hello!")

# Broadcast message
results = broadcast_message("Hello everyone!")
```

## Migration Guide

### Before (Duplicated Code)

```python
# Each file had its own implementation
def load_coordinates_from_json():
    # 20+ lines of duplicated code
    pass

def list_agents():
    # 15+ lines of duplicated code
    pass

def send_message_pyautogui(agent_id, message):
    # 30+ lines of duplicated code
    pass
```

### After (Shared Utilities)

```python
# Single import, clean usage
from src.services.messaging.shared import (
    load_coordinates_from_json,
    list_agents,
    send_message_pyautogui
)

# Same functionality, no duplication
coords = load_coordinates_from_json()
agents = list_agents()
success = send_message_pyautogui("agent-1", "Hello!")
```

## Configuration

### Coordinate Files

The utilities automatically search for coordinate files in this order:
1. `config/coordinates.json`
2. `cursor_agent_coords.json`
3. `config/cursor_agent_coords.json`

### Custom Coordinate Files

```python
utils = MessagingUtilities()
coords = utils.load_coordinates_from_json("custom/path/coords.json")
```

## Error Handling

All utilities include comprehensive error handling:

```python
try:
    success = send_message_pyautogui("agent-1", "Hello!")
    if not success:
        print("Message failed to send")
except Exception as e:
    print(f"Error: {e}")
```

## Performance Features

- **Caching**: Coordinate data is cached after first load
- **Efficient Operations**: Optimized for minimal overhead
- **Thread Safety**: Safe for concurrent use
- **Memory Management**: Automatic cleanup of old data

## Integration Examples

### Discord Commander Integration

```python
from src.services.messaging.shared import broadcast_message

async def send_discord_broadcast(message):
    results = broadcast_message(f"Discord: {message}")
    success_count = sum(1 for success in results.values() if success)
    return f"Broadcast to {success_count} agents"
```

### Agent Communication

```python
from src.services.messaging.shared import MessagingUtilities

class AgentCommunicator:
    def __init__(self):
        self.utils = MessagingUtilities()
    
    def send_to_agent(self, agent_id, message):
        return self.utils.send_message_pyautogui(agent_id, message)
    
    def get_agent_list(self):
        return self.utils.list_agents()
```

### Testing Integration

```python
from src.services.messaging.shared import get_messaging_utilities

def test_messaging():
    utils = get_messaging_utilities()
    
    # Test coordinate loading
    coords = utils.load_coordinates_from_json()
    assert isinstance(coords, dict)
    
    # Test agent listing
    agents = utils.list_agents()
    assert isinstance(agents, list)
```

## Best Practices

1. **Use Shared Utilities**: Always import from `src.services.messaging.shared`
2. **Handle Errors**: Check return values and handle exceptions
3. **Cache Instances**: Reuse `MessagingUtilities` instances when possible
4. **Validate Coordinates**: Use `validate_coordinates()` to check setup
5. **Log Operations**: All utilities include built-in logging

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure you're importing from the correct path
2. **Coordinate File Missing**: Check file paths and permissions
3. **PyAutoGUI Issues**: Verify PyAutoGUI is installed and accessible
4. **Agent Not Found**: Validate agent IDs exist in coordinates

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from src.services.messaging.shared import MessagingUtilities
utils = MessagingUtilities()
# Debug information will be logged
```

## API Reference

### MessagingUtilities

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `load_coordinates_from_json()` | `file_path: Optional[str]` | `Dict[str, Any]` | Load agent coordinates |
| `list_agents()` | `coordinates_file: Optional[str]` | `List[str]` | List all agents |
| `get_agent_coordinates()` | `agent_id: str, coordinates_file: Optional[str]` | `Optional[Tuple[int, int]]` | Get agent coordinates |
| `send_message_pyautogui()` | `agent_id: str, message: str, coordinates_file: Optional[str]` | `bool` | Send message via PyAutoGUI |
| `broadcast_message()` | `message: str, sender: str, coordinates_file: Optional[str]` | `Dict[str, bool]` | Broadcast to all agents |
| `validate_coordinates()` | `coordinates_file: Optional[str]` | `Dict[str, Any]` | Validate coordinate file |

### Convenience Functions

| Function | Parameters | Returns | Description |
|----------|------------|---------|-------------|
| `load_coordinates_from_json()` | `file_path: Optional[str]` | `Dict[str, Any]` | Load coordinates |
| `list_agents()` | `coordinates_file: Optional[str]` | `List[str]` | List agents |
| `send_message_pyautogui()` | `agent_id: str, message: str, coordinates_file: Optional[str]` | `bool` | Send message |
| `broadcast_message()` | `message: str, sender: str, coordinates_file: Optional[str]` | `Dict[str, bool]` | Broadcast message |

## Version History

- **v1.0**: Initial shared utilities implementation
- **v1.1**: Added caching and performance optimizations
- **v1.2**: Enhanced error handling and logging
- **v2.0**: V2 compliance and full consolidation

---

**Author**: Agent-3 (Infrastructure Specialist)  
**License**: MIT  
**Last Updated**: 2025-01-12
