# 🐝 Message Queue PyAutoGUI Integration

## Overview

This integration connects the file-based message queue system with the PyAutoGUI delivery mechanism, enabling reliable automated message delivery to agents via cursor/keyboard automation.

## Architecture

### Components

1. **MessageQueue** (`src/core/message_queue.py`)
   - Core queuing system with persistence
   - Priority-based message processing
   - PyAutoGUI delivery integration

2. **PyAutoGUI Integration** (`src/core/message_queue_pyautogui_integration.py`)
   - Bridge between queue and PyAutoGUI systems
   - Message format conversion
   - Delivery statistics tracking

3. **AsyncQueueProcessor** (`src/core/message_queue.py`)
   - Background message processing
   - Automatic PyAutoGUI delivery
   - Error handling and retry logic

## Quick Start

### Basic Usage

```python
from src.core.message_queue import MessageQueue, QueueConfig

# Create queue with PyAutoGUI delivery enabled
config = QueueConfig(enable_pyautogui_delivery=True)
queue = MessageQueue(config=config)

# Enqueue message with automatic PyAutoGUI delivery
message_id = queue.enqueue_with_pyautogui(
    message="Hello Agent-1!",
    recipient="Agent-1",
    message_type="text",
    priority="regular"
)

# Broadcast to all agents
broadcast_id = queue.enqueue_broadcast_with_pyautogui(
    message="System maintenance in 5 / 5-2 agent cycles",
    sender="Captain"
)
```

### Advanced Configuration

```python
from src.core.message_queue import QueueConfig, MessageQueue
from src.core.message_queue_pyautogui_integration import create_queue_pyautogui_delivery_callback

# Custom configuration
config = QueueConfig(
    queue_directory="custom_queue",
    max_queue_size=2000,
    processing_batch_size=10,
    enable_pyautogui_delivery=True,
    default_delivery_method="pyautogui"
)

# Create queue
queue = MessageQueue(config=config)

# Custom PyAutoGUI callback
pyautogui_callback = create_queue_pyautogui_delivery_callback()
queue_with_custom_callback = MessageQueue(
    config=config,
    delivery_callback=pyautogui_callback
)
```

### Async Processing

```python
import asyncio
from src.core.message_queue import AsyncQueueProcessor

async def run_queue_processor():
    # Create processor with automatic PyAutoGUI delivery
    processor = AsyncQueueProcessor(queue=queue)

    # Start processing (runs in background)
    await processor.start_processing(interval=5.0)  # Process every 5 seconds

    # Let it run for a while
    await asyncio.sleep(60)

    # Stop processing
    processor.stop_processing()

# Run the processor
asyncio.run(run_queue_processor())
```

## API Reference

### MessageQueue Class

#### Methods

- `enqueue(message, delivery_callback=None, use_pyautogui=None)` - Add message to queue
- `enqueue_with_pyautogui(message, recipient, message_type="text", priority="regular")` - Convenience method for PyAutoGUI delivery
- `enqueue_broadcast_with_pyautogui(message, sender="system")` - Broadcast message to all agents
- `dequeue(batch_size=None)` - Get messages for processing
- `mark_delivered(queue_id)` - Mark message as successfully delivered
- `mark_failed(queue_id, error)` - Mark message as failed
- `get_statistics()` - Get queue statistics
- `get_pyautogui_delivery_stats()` - Get PyAutoGUI delivery statistics
- `cleanup_expired()` - Remove expired messages

### QueueConfig Class

#### Parameters

- `queue_directory` - Directory for queue files (default: "message_queue")
- `max_queue_size` - Maximum queue size (default: 1000)
- `processing_batch_size` - Messages per processing batch (default: 10)
- `max_age_days` - Maximum message age in days (default: 7)
- `enable_pyautogui_delivery` - Enable PyAutoGUI delivery (default: True)
- `default_delivery_method` - Default delivery method (default: "pyautogui")

### Message Format

#### Queue Message Format
```python
{
    'content': 'Message text',
    'recipient': 'Agent-X',
    'sender': 'system',
    'message_type': 'text',  # text, broadcast, onboarding, etc.
    'priority': 'regular'   # regular, urgent
}
```

#### PyAutoGUI Delivery Statistics
```python
{
    'total_attempts': 150,
    'successful_deliveries': 145,
    'failed_deliveries': 5,
    'success_rate': 96.7
}
```

## Integration Features

### ✅ Automatic PyAutoGUI Delivery
- Messages automatically delivered via PyAutoGUI when coordinates available
- Fallback to clipboard + typewrite for reliability
- Retry logic with exponential backoff

### ✅ Concurrent Safety
- File-based locking prevents race conditions
- Atomic read/write operations
- Thread-safe queue operations

### ✅ Priority Processing
- Priority-based message ordering
- Fair queuing prevents starvation
- Configurable batch processing

### ✅ Error Handling
- Automatic retry for failed deliveries
- Comprehensive error logging
- Graceful degradation when PyAutoGUI unavailable

### ✅ Monitoring & Statistics
- Real-time delivery statistics
- Queue health monitoring
- Performance metrics tracking

## Testing

Run the integration test:

```bash
python test_message_queue_pyautogui_integration.py
```

This will test:
- ✅ Queue creation with PyAutoGUI delivery
- ✅ Message enqueue operations
- ✅ Statistics retrieval
- ✅ Processor integration
- ✅ Health monitoring

## Configuration

### Environment Variables

```bash
# PyAutoGUI settings
ENABLE_PYAUTOGUI=1
PYAUTO_PAUSE_S=0.05
PYAUTO_MOVE_DURATION=0.4
PYAUTO_SEND_RETRIES=2
PYAUTO_RETRY_SLEEP_S=0.3

# Queue settings
QUEUE_MAX_SIZE=1000
QUEUE_PROCESSING_BATCH_SIZE=10
QUEUE_MAX_AGE_DAYS=7
```

### Agent Coordinates

The system uses the coordinate loader from `src/core/coordinate_loader.py` to get agent screen coordinates for PyAutoGUI delivery.

## Troubleshooting

### Common Issues

1. **PyAutoGUI Not Available**
   ```
   Solution: Install pyautogui and pynput
   pip install pyautogui pynput
   ```

2. **Missing Agent Coordinates**
   ```
   Solution: Ensure agents are properly configured in coordinate_loader
   Check: src/core/coordinate_loader.py
   ```

3. **Queue File Permission Issues**
   ```
   Solution: Ensure write permissions on message_queue directory
   chmod 755 message_queue/
   ```

4. **High Memory Usage**
   ```
   Solution: Configure appropriate queue size limits
   QueueConfig(max_queue_size=500)
   ```

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Performance Considerations

### Optimization Tips

1. **Batch Processing**: Use larger batch sizes for better throughput
2. **Queue Cleanup**: Regular cleanup prevents queue bloat
3. **Priority Tuning**: Adjust priorities based on message urgency
4. **Coordinate Caching**: Cache agent coordinates to reduce lookups

### Monitoring

Track these metrics:
- Queue size over time
- Processing latency
- Delivery success rate
- PyAutoGUI operation time

## Migration Guide

### From Standalone Systems

**Before (separate systems):**
```python
# Old way - separate queue and PyAutoGUI
queue = MessageQueue()
pyautogui.deliver_message_pyautogui(message, coords)
```

**After (integrated system):**
```python
# New way - unified system
queue = MessageQueue(config=QueueConfig(enable_pyautogui_delivery=True))
queue.enqueue_with_pyautogui(message, recipient)
```

## Security Considerations

1. **Screen Access**: PyAutoGUI requires screen access permissions
2. **Coordinate Validation**: Agent coordinates are validated before use
3. **Message Sanitization**: Messages are sanitized before delivery
4. **Access Control**: Queue operations can be restricted by configuration

## Future Enhancements

- Message encryption for sensitive data
- Delivery confirmation callbacks
- Advanced retry strategies
- Real-time queue monitoring dashboard
- Message prioritization algorithms

---

## 🎯 Summary

This integration provides a robust, reliable messaging system that combines the persistence and scalability of file-based queuing with the automation capabilities of PyAutoGUI. The system ensures concurrent-safe operations while providing automatic delivery to agents via cursor/keyboard automation.

**Key Benefits:**
- ✅ **Reliable Delivery**: Persistent queuing with automatic retry
- ✅ **Concurrent Safety**: Thread-safe operations with file locking
- ✅ **Automated Delivery**: PyAutoGUI integration for hands-free operation
- ✅ **Monitoring**: Comprehensive statistics and health monitoring
- ✅ **Scalable**: Configurable batch processing and queue management
