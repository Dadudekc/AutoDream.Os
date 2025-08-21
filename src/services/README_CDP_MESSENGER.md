# CDP Messenger - Headless Agent Chat Messaging

## Overview

The CDP Messenger is a headless messaging system that sends messages to Cursor agent chats **without moving the mouse** by injecting text and "press Enter" via the Chrome DevTools Protocol (CDP). This works in the background and integrates perfectly with our V1-V2 Message Queue System.

## 🚀 Key Features

- **🖱️ No Mouse Movement**: Works completely in the background
- **🔌 CDP Integration**: Uses Chrome DevTools Protocol for reliable messaging
- **🎯 Agent Targeting**: Send messages to specific agents (Agent-3, Agent-5, etc.)
- **📢 Broadcast Support**: Send to all open agent chats simultaneously
- **⚡ Priority System**: Support for different message priorities
- **🔄 Retry Logic**: Automatic retry on failures
- **📊 Status Monitoring**: Real-time delivery status and reporting

## 🏗️ Architecture

```
V1-V2 Message Queue → CDP Messenger → Chrome DevTools Protocol → Cursor Agent Chats
        ↓                    ↓                    ↓                    ↓
   Message Queue      Headless Delivery      CDP Endpoint      Agent Input Fields
```

## 📋 Prerequisites

### 1. Install Dependencies

```bash
# Install required Python packages
pip install -r requirements_cdp.txt

# Or install manually
pip install websocket-client requests urllib3
```

### 2. Launch Cursor with CDP Enabled

**Option A: PowerShell Script (Recommended)**
```powershell
# Launch Cursor with CDP on port 9222
.\launch_cursor_with_cdp.ps1

# Or use custom port
.\launch_cursor_with_cdp.ps1 -Port 9223
```

**Option B: Manual Launch**
```bash
# Windows
"C:\Users\%USERNAME%\AppData\Local\Programs\Cursor\Cursor.exe" --remote-debugging-port=9222

# macOS
/Applications/Cursor.app/Contents/MacOS/Cursor --remote-debugging-port=9222

# Linux
cursor --remote-debugging-port=9222
```

## 🎯 Quick Start

### 1. Test the System

```bash
# Run the test suite
python test_cdp_messenger.py

# Test basic functionality
python cdp_send_message.py "Hello Agent-3!" --target "Agent-3"
```

### 2. Send Your First Message

```bash
# Send a message to Agent-3
python cdp_send_message.py "Agent-3: begin integration tests for services_v2/auth. Report in 60m." --target "Agent-3"

# Send to all agents
python cdp_send_message.py "ALL AGENTS: no acknowledgments—only diffs, commits, and checkmarks." --all
```

## 📚 Usage Examples

### Basic Messaging

```bash
# Send to specific agent
python cdp_send_message.py "Agent-3: Hello there!" --target "Agent-3"

# Send with priority
python cdp_send_message.py "URGENT: System alert!" --target "Agent-5" --priority urgent

# Use custom port
python cdp_send_message.py "Test message" --port 9223
```

### Advanced Scenarios

```bash
# Broadcast to all agents
python cdp_send_message.py "📢 BROADCAST: Team meeting in 5 minutes" --all

# High-priority alert
python cdp_send_message.py "🚨 CRITICAL: Database connection failed!" --target "Agent-4" --priority critical

# Task assignment
python cdp_send_message.py "Agent-3: TASK: Review the new authentication service. Due: EOD" --target "Agent-3"
```

## 🔧 Configuration

### Environment Variables

```bash
# Set custom CDP port
export CURSOR_CDP_PORT=9223

# Windows PowerShell
$env:CURSOR_CDP_PORT=9223
```

### Command Line Options

```bash
python cdp_send_message.py --help

# Available options:
#   --target TEXT     Target agent (default: General)
#   --all            Broadcast to all targets
#   --priority TEXT  Message priority (low/normal/high/urgent/critical)
#   --port INTEGER   CDP port (default: 9222)
```

## 🧪 Testing

### Run All Tests

```bash
python test_cdp_messenger.py
```

### Individual Test Functions

```python
from test_cdp_messenger import (
    test_cdp_connection,
    test_message_sending,
    test_agent_targeting,
    test_broadcast
)

# Test CDP connection
test_cdp_connection()

# Test message sending
test_message_sending()
```

## 🔗 Integration with V1-V2 Message Queue

The CDP Messenger integrates seamlessly with our V1-V2 Message Queue System:

```python
from v1_v2_message_queue_system import V1V2MessageQueueSystem
from cdp_send_message import send_to_target

# Create message queue system
mq_system = V1V2MessageQueueSystem(max_workers=4)

# Queue a message that will be delivered via CDP
msg_id = mq_system.queue_message(
    "Agent-5", "Agent-3", "URGENT: System integration test required!",
    priority=MessagePriority.URGENT,
    high_priority_flag=True
)

# The system will automatically use CDP for delivery
```

## 🚨 Troubleshooting

### Common Issues

#### 1. CDP Connection Failed

```bash
❌ CDP connection failed: HTTP request failed
💡 Make sure Cursor is running with: --remote-debugging-port=9222
```

**Solution:**
- Launch Cursor with CDP enabled
- Check if port is already in use
- Verify Cursor is fully loaded

#### 2. No Targets Found

```bash
❌ No suitable CDP targets found
💡 Make sure Cursor is running with: --remote-debugging-port=9222
```

**Solution:**
- Open agent chats in Cursor
- Wait for Cursor to fully load
- Check if targets are filtered correctly

#### 3. Message Delivery Failed

```bash
❌ Failed: input_not_found
   Details: Could not find input for Agent-3
```

**Solution:**
- Ensure agent chat is open and active
- Check if input field is visible
- Try different target selectors

#### 4. WebSocket Not Available

```bash
❌ websocket-client not available
💡 Install with: pip install websocket-client
```

**Solution:**
```bash
pip install websocket-client
```

### Debug Mode

Enable detailed logging for troubleshooting:

```python
import logging
logging.getLogger().setLevel(logging.DEBUG)
```

## 📊 Performance Considerations

### Optimization Tips

1. **Batch Messages**: Send multiple messages at once for efficiency
2. **Target Selection**: Use specific agent targeting instead of broadcast when possible
3. **Connection Reuse**: The system automatically manages CDP connections
4. **Error Handling**: Built-in retry logic for failed deliveries

### Scaling

- **Small Scale**: 1-5 concurrent messages
- **Medium Scale**: 5-20 concurrent messages
- **Large Scale**: 20+ concurrent messages (monitor system resources)

## 🔒 Security Considerations

### CDP Security

- CDP is only accessible locally (127.0.0.1)
- No external network access required
- Messages are sent within the local Cursor instance

### Best Practices

1. **Port Management**: Use non-standard ports in production
2. **Access Control**: Ensure only authorized users can access the system
3. **Message Validation**: Validate message content before sending
4. **Rate Limiting**: Implement rate limiting for high-volume scenarios

## 🚀 Advanced Features

### Custom JavaScript Injection

You can customize the JavaScript injection for specific use cases:

```python
# Modify the JS_TEMPLATE in cdp_send_message.py
# Add custom selectors or behavior for your specific setup
```

### Multi-Port Support

Run multiple Cursor instances with different CDP ports:

```bash
# Instance 1
.\launch_cursor_with_cdp.ps1 -Port 9222

# Instance 2  
.\launch_cursor_with_cdp.ps1 -Port 9223

# Send to specific instance
python cdp_send_message.py "Message" --port 9223
```

### Integration with Other Systems

The CDP Messenger can be integrated with:

- **CI/CD Pipelines**: Automated testing and deployment notifications
- **Monitoring Systems**: Alert delivery to agent chats
- **Workflow Automation**: Task assignment and status updates
- **Team Coordination**: Real-time communication and updates

## 📈 Monitoring and Metrics

### Status Reporting

```python
# Get delivery status
result = send_to_target(ws_url, message, target_agent)
if result.get("ok"):
    print(f"✅ Success: {result['method']}")
    print(f"🎯 Target: {result['target']}")
else:
    print(f"❌ Failed: {result['reason']}")
```

### Performance Metrics

- **Delivery Success Rate**: Percentage of successful message deliveries
- **Response Time**: Time from message send to delivery confirmation
- **Error Rates**: Frequency and types of delivery failures
- **Target Availability**: Number of active CDP targets

## 🔮 Future Enhancements

### Planned Features

1. **Message Templates**: Pre-defined message templates for common scenarios
2. **Scheduled Messaging**: Send messages at specific times
3. **Message History**: Track and retrieve message delivery history
4. **Advanced Targeting**: More sophisticated agent targeting algorithms
5. **Message Encryption**: End-to-end encryption for sensitive messages

### Extensibility

The system is designed to be easily extensible:

- **Custom Delivery Methods**: Add new delivery mechanisms
- **Plugin System**: Support for third-party integrations
- **API Endpoints**: REST API for external system integration
- **Web Interface**: Web-based message composition and delivery

## 📞 Support

### Getting Help

1. **Check Troubleshooting**: Review the troubleshooting section above
2. **Run Tests**: Use the test suite to diagnose issues
3. **Check Logs**: Enable debug logging for detailed information
4. **Verify Setup**: Ensure all prerequisites are met

### Contributing

1. **Report Issues**: Create detailed bug reports with error messages
2. **Suggest Features**: Propose new features and improvements
3. **Submit PRs**: Contribute code improvements and fixes
4. **Documentation**: Help improve documentation and examples

---

## 🎉 Success!

You now have a powerful headless messaging system that can:

- ✅ Send messages to Agent-3 without moving the mouse
- ✅ Integrate with the V1-V2 Message Queue System
- ✅ Broadcast to all agents simultaneously
- ✅ Handle different message priorities
- ✅ Work completely in the background
- ✅ Provide detailed delivery status and reporting

**Next Steps:**
1. Launch Cursor with CDP: `.\launch_cursor_with_cdp.ps1`
2. Test the system: `python test_cdp_messenger.py`
3. Send your first message: `python cdp_send_message.py "Agent-3: Hello!" --target "Agent-3"`
4. Integrate with the message queue system for automated messaging

The CDP Messenger brings the power of headless messaging to your agent coordination system! 🚀
