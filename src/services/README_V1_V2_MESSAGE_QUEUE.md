# V1-V2 Message Queue System

## Overview

The V1-V2 Message Queue System is a comprehensive messaging solution that integrates the proven V1 PyAutoGUI approach with V2's scalable architecture. It provides a robust message queuing system for multiple agents with priority-based delivery and a high-priority flag system.

## Key Features

- **🔗 V1-V2 Integration**: Combines V1's reliable PyAutoGUI message delivery with V2's modern architecture
- **📨 Message Queuing**: Queue-based system for handling multiple messages efficiently
- **🚨 High-Priority Flags**: Ctrl+Enter x2 system for urgent message delivery
- **⚡ Priority-Based Delivery**: 5-level priority system (LOW, NORMAL, HIGH, URGENT, CRITICAL)
- **🔄 Retry Mechanisms**: Automatic retry logic with configurable attempts
- **👷 Multi-Threaded**: Worker thread system for concurrent message processing
- **📊 Monitoring**: Real-time status monitoring and statistics
- **🛡️ Error Handling**: Comprehensive error handling and logging

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    V1-V2 Message Queue System                  │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────┐ │
│  │   Message Queue │    │  Worker Threads │    │   V1/V2    │ │
│  │   (Priority)    │───▶│   (Processing)  │───▶│ Integration│ │
│  └─────────────────┘    └─────────────────┘    └─────────────┘ │
│           │                       │                    │        │
│           ▼                       ▼                    ▼        │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────┐ │
│  │   Statistics    │    │   Agent Status  │    │  PyAutoGUI  │ │
│  │   & Monitoring  │    │   & Tracking    │    │   Delivery  │ │
│  └─────────────────┘    └─────────────────┘    └─────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Installation

### Prerequisites

- Python 3.8+
- PyAutoGUI (`pip install pyautogui`)
- pyperclip (`pip install pyperclip`)

### Setup

1. **Clone the repository**:
   ```bash
   cd Agent_Cellphone_V2_Repository/src/services
   ```

2. **Install dependencies**:
   ```bash
   pip install pyautogui pyperclip
   ```

3. **Verify installation**:
   ```bash
   python test_v1_v2_message_queue.py
   ```

## Quick Start

### Basic Usage

```python
from v1_v2_message_queue_system import V1V2MessageQueueSystem, MessagePriority

# Create message queue system
mq_system = V1V2MessageQueueSystem(max_workers=4)

# Queue a normal message
msg_id = mq_system.queue_message(
    sender="Agent-1",
    recipient="Agent-3",
    content="Hello Agent-3! How are you today?",
    priority=MessagePriority.NORMAL
)

# Queue a high-priority message
msg_id = mq_system.queue_message(
    sender="Agent-5",
    recipient="Agent-3",
    content="URGENT: Please respond immediately!",
    priority=MessagePriority.URGENT,
    high_priority_flag=True  # Uses Ctrl+Enter x2
)

# Get status
status = mq_system.get_queue_status()
print(f"Messages delivered: {status['messages_delivered']}")

# Cleanup
mq_system.shutdown()
```

### Convenience Functions

```python
from v1_v2_message_queue_system import (
    create_message_queue_system,
    send_high_priority_message,
    send_normal_message
)

# Create system
mq_system = create_message_queue_system(max_workers=2)

# Send normal message
msg_id = send_normal_message(
    mq_system, "Agent-1", "Agent-3", "Hello there!"
)

# Send high-priority message (Ctrl+Enter x2)
msg_id = send_high_priority_message(
    mq_system, "Agent-5", "Agent-3", "URGENT: System alert!"
)
```

## Message Priority System

The system supports 5 priority levels:

| Priority | Value | Description | Use Case |
|----------|-------|-------------|----------|
| **LOW** | 1 | Low priority | Background tasks, non-urgent updates |
| **NORMAL** | 2 | Standard priority | Regular communication, status updates |
| **HIGH** | 3 | High priority | Important tasks, time-sensitive requests |
| **URGENT** | 4 | Urgent priority | Immediate attention required |
| **CRITICAL** | 5 | Critical priority | System failures, emergency alerts |

### Priority Processing

Messages are processed in priority order:
1. **Critical** messages are processed first
2. **Urgent** messages follow
3. **High** priority messages come next
4. **Normal** priority messages follow
5. **Low** priority messages are processed last

## High-Priority Flag System (Ctrl+Enter x2)

The high-priority flag system provides an additional way to mark messages as urgent:

### How It Works

1. **Normal Message**: Uses standard `Enter` key for delivery
2. **High-Priority Flag**: Uses `Ctrl+Enter` twice for delivery

### Usage

```python
# Normal message (Enter key)
mq_system.queue_message(
    "Agent-1", "Agent-3", "Regular message",
    priority=MessagePriority.NORMAL,
    high_priority_flag=False  # Default
)

# High-priority message (Ctrl+Enter x2)
mq_system.queue_message(
    "Agent-5", "Agent-3", "URGENT message!",
    priority=MessagePriority.URGENT,
    high_priority_flag=True  # Uses Ctrl+Enter x2
)
```

### Delivery Method

- **Normal**: Types message → Presses `Enter`
- **High-Priority**: Types message → `Ctrl+Enter` → `Ctrl+Enter`

## Configuration

### System Parameters

```python
mq_system = V1V2MessageQueueSystem(
    v1_coordinates_file="../runtime/agent_comms/cursor_agent_coords.json",
    v2_coordinates_file="agent_complete_locations.json",
    queue_size=1000,        # Maximum messages in queue
    max_workers=4           # Number of worker threads
)
```

### Coordinate Files

The system automatically loads coordinates from both V1 and V2 systems:

- **V1 Coordinates**: `../runtime/agent_comms/cursor_agent_coords.json`
- **V2 Coordinates**: `agent_complete_locations.json`

## Monitoring and Statistics

### Queue Status

```python
status = mq_system.get_queue_status()

print(f"Queue Size: {status['queue_size']}")
print(f"Active Workers: {status['active_workers']}")
print(f"Messages Queued: {status['messages_queued']}")
print(f"Messages Delivered: {status['messages_delivered']}")
print(f"Messages Failed: {status['messages_failed']}")
print(f"Average Delivery Time: {status['average_delivery_time']:.2f}s")
print(f"Uptime: {status['uptime']:.0f}s")
```

### Agent Status

```python
status = mq_system.get_queue_status()

for agent_id, agent_info in status['agent_status'].items():
    print(f"{agent_id}:")
    print(f"  Status: {agent_info['status']}")
    print(f"  Messages Received: {agent_info['messages_received']}")
    print(f"  Last Message: {agent_info['last_message']}")
    print(f"  Last Delivery Time: {agent_info['last_delivery_time']:.2f}s")
```

## Error Handling and Retries

### Retry Logic

- **Default Retries**: 3 attempts per message
- **Retry Priority**: Decreases priority on each retry
- **Failure Handling**: Messages that fail after max retries are marked as failed

### Error Types

- **Coordinate Errors**: Agent coordinates not found
- **PyAutoGUI Errors**: Display/permission issues
- **Delivery Errors**: Message sending failures
- **System Errors**: General system issues

### Error Recovery

```python
# Check failed messages
if mq_system.failed_messages:
    for msg_id, failure_info in mq_system.failed_messages.items():
        msg = failure_info['message']
        print(f"Failed: {msg.sender} → {msg.recipient}")
        print(f"Reason: {failure_info['failure_reason']}")

# Clear failed messages
mq_system.failed_messages.clear()
```

## Examples

### Multi-Agent Coordination

```python
# Coordinate a team workflow
workflow_messages = [
    ("Agent-5", "Agent-1", "TASK: Begin strategic planning"),
    ("Agent-5", "Agent-2", "TASK: Prepare resource analysis"),
    ("Agent-5", "Agent-3", "TASK: Start technical planning"),
    ("Agent-5", "Agent-4", "TASK: Review security protocols"),
]

for sender, recipient, content in workflow_messages:
    mq_system.queue_message(sender, recipient, content, MessagePriority.HIGH)
```

### Priority-Based Communication

```python
# Send different priority messages
mq_system.queue_message("Agent-1", "Agent-3", "Background update", MessagePriority.LOW)
mq_system.queue_message("Agent-2", "Agent-4", "Regular status", MessagePriority.NORMAL)
mq_system.queue_message("Agent-5", "Agent-1", "Important task", MessagePriority.HIGH)
mq_system.queue_message("Agent-3", "Agent-2", "Urgent request", MessagePriority.URGENT)
mq_system.queue_message("Agent-4", "Agent-5", "CRITICAL ALERT!", MessagePriority.CRITICAL)
```

### High-Priority Alerts

```python
# Send urgent alerts with Ctrl+Enter x2
mq_system.queue_message(
    "Agent-5", "Agent-3",
    "🚨 SYSTEM ALERT: Immediate attention required!",
    priority=MessagePriority.CRITICAL,
    high_priority_flag=True
)
```

## Testing

### Run Tests

```bash
# Run all tests
python test_v1_v2_message_queue.py

# Run demo
python v1_v2_message_queue_demo.py
```

### Test Coverage

The test suite covers:
- ✅ Basic message queuing
- ✅ Priority-based delivery
- ✅ High-priority flag system
- ✅ Error handling and retries
- ✅ Multi-agent coordination
- ✅ System shutdown

## Troubleshooting

### Common Issues

1. **PyAutoGUI Not Available**
   - Install: `pip install pyautogui`
   - Check permissions on your system

2. **Coordinate File Not Found**
   - Verify file paths in configuration
   - Check file permissions

3. **Message Delivery Failures**
   - Verify agent coordinates are correct
   - Check if target agents are active
   - Review error logs for specific issues

4. **Performance Issues**
   - Reduce `max_workers` if system is overwhelmed
   - Increase `queue_size` for high-volume scenarios
   - Monitor system resources

### Debug Mode

Enable debug logging for detailed information:

```python
import logging
logging.getLogger().setLevel(logging.DEBUG)
```

## Performance Considerations

### Optimization Tips

1. **Worker Threads**: Adjust `max_workers` based on system capabilities
2. **Queue Size**: Set appropriate `queue_size` for your use case
3. **Message Batching**: Queue multiple messages at once for efficiency
4. **Priority Management**: Use appropriate priorities to optimize delivery order

### Scaling

- **Small Scale**: 1-2 workers, queue size 100-500
- **Medium Scale**: 4-8 workers, queue size 1000-5000
- **Large Scale**: 8+ workers, queue size 5000+

## Integration with Existing Systems

### V1 System Integration

The system automatically integrates with existing V1 PyAutoGUI coordinators:

```python
# V1 coordinator will be auto-detected if available
if mq_system.v1_coordinator:
    print("V1 coordinator available")
```

### V2 System Integration

V2 services are automatically detected and used when available:

```python
# V2 services will be auto-detected if available
if mq_system.v2_delivery_service:
    print("V2 delivery service available")
```

## Contributing

### Development

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Add tests**
5. **Submit a pull request**

### Testing

- Run existing tests: `python test_v1_v2_message_queue.py`
- Add new tests for new features
- Ensure all tests pass before submitting

## License

This project is part of the Agent Cellphone V2 system and follows the same licensing terms.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review error logs
3. Run test suite
4. Create an issue with detailed error information

---

**🎉 Congratulations!** You now have a powerful V1-V2 Message Queue System that combines the best of both worlds: V1's proven PyAutoGUI reliability with V2's modern architecture, plus the innovative high-priority flag system with Ctrl+Enter x2 functionality.
