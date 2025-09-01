# PyAutoGUI Mode Testing Guide (Without Onboarding)

## Overview

This guide demonstrates how to test the PyAutoGUI messaging mode in Agent Cellphone V2 without using the onboarding system. The PyAutoGUI mode provides direct coordinate-based messaging to agents using automated mouse and keyboard control.

## 🎯 Key Features

- **Direct Messaging**: Send messages directly to specific agents
- **Bulk Messaging**: Send messages to all agents simultaneously
- **Coordinate Navigation**: Uses predefined coordinates to navigate to agent windows
- **No Onboarding Dependency**: Works independently of the onboarding system
- **CLI Interface**: Full command-line interface for testing

## 🚀 Quick Start

### 1. List Available Agents

```bash
python -m src.services.messaging_cli --list-agents
```

This shows all available agents with their coordinates and inbox locations.

### 2. Show Agent Coordinates

```bash
python -m src.services.messaging_cli --coordinates
```

Displays the exact screen coordinates for each agent window.

### 3. Send Test Message to Specific Agent

```bash
python -m src.services.messaging_cli --agent Agent-1 --message "Hello Agent-1!" --mode pyautogui
```

Sends a message directly to Agent-1 using PyAutoGUI automation.

### 4. Send Bulk Message to All Agents

```bash
python -m src.services.messaging_cli --bulk --message "Bulk test message" --mode pyautogui
```

Sends the same message to all agents in sequence.

## 🧪 Test Scripts

### Automated Test Script

Run the comprehensive test script:

```bash
python test_pyautogui_mode.py
```

This script performs:
- ✅ Agent listing
- ✅ Coordinate display
- ✅ Single agent messaging
- ✅ Bulk messaging
- ✅ Message history display

### Demo Commands Script

Run the demo script to see all commands in action:

```bash
python demo_pyautogui_commands.py
```

Or just show the available commands:

```bash
python demo_pyautogui_commands.py --show-only
```

## 📋 Available CLI Commands

### Basic Commands

| Command | Description | Example |
|---------|-------------|---------|
| `--list-agents` | List all available agents | `python -m src.services.messaging_cli --list-agents` |
| `--coordinates` | Show agent coordinates | `python -m src.services.messaging_cli --coordinates` |
| `--history` | Show message history | `python -m src.services.messaging_cli --history` |
| `--check-status` | Check agent status | `python -m src.services.messaging_cli --check-status` |

### Messaging Commands

| Command | Description | Example |
|---------|-------------|---------|
| `--agent` | Send to specific agent | `python -m src.services.messaging_cli --agent Agent-1 --message "Hello"` |
| `--bulk` | Send to all agents | `python -m src.services.messaging_cli --bulk --message "Bulk message"` |
| `--mode pyautogui` | Use PyAutoGUI mode (default) | `python -m src.services.messaging_cli --agent Agent-1 --message "Test" --mode pyautogui` |
| `--no-paste` | Type instead of paste | `python -m src.services.messaging_cli --agent Agent-1 --message "Test" --no-paste` |

### Advanced Options

| Command | Description | Example |
|---------|-------------|---------|
| `--high-priority` | Set urgent priority | `python -m src.services.messaging_cli --agent Agent-1 --message "Urgent!" --high-priority` |
| `--type broadcast` | Set message type | `python -m src.services.messaging_cli --agent Agent-1 --message "Broadcast" --type broadcast` |
| `--get-next-task` | Get task for agent | `python -m src.services.messaging_cli --agent Agent-1 --get-next-task` |

## 🔧 How PyAutoGUI Mode Works

### 1. Coordinate Navigation
- System moves mouse to predefined agent coordinates
- Clicks to focus the agent window
- Creates new tab with Ctrl+T

### 2. Message Delivery
- **Paste Mode** (default): Copies message to clipboard and pastes with Ctrl+V
- **Type Mode**: Types message character by character with formatting

### 3. Message Sending
- Presses Enter to send the message
- Returns success/failure status

### 4. Agent Order for Bulk Messages
The system sends bulk messages in this order:
1. Agent-1 (Integration & Core Systems)
2. Agent-2 (Architecture & Design)
3. Agent-3 (Infrastructure & DevOps)
4. Agent-5 (Business Intelligence)
5. Agent-6 (Gaming & Entertainment)
6. Agent-7 (Web Development)
7. Agent-8 (Integration & Performance)
8. Agent-4 (Captain - Quality Assurance)

## 📍 Agent Coordinates

| Agent | Coordinates | Description |
|-------|-------------|-------------|
| Agent-1 | (-1269, 481) | Integration & Core Systems |
| Agent-2 | (-308, 480) | Architecture & Design |
| Agent-3 | (-1269, 1001) | Infrastructure & DevOps |
| Agent-5 | (652, 421) | Business Intelligence |
| Agent-6 | (1612, 419) | Gaming & Entertainment |
| Agent-7 | (653, 940) | Web Development |
| Agent-8 | (1611, 941) | Integration & Performance |
| Agent-4 | (-308, 1000) | Captain - Quality Assurance |

## ⚠️ Important Notes

### Prerequisites
- PyAutoGUI must be installed: `pip install pyautogui`
- Pyperclip must be installed: `pip install pyperclip`
- Agent windows must be open and positioned at the correct coordinates

### Safety Features
- PyAutoGUI has a 0.5-second delay for mouse movements
- 1-second delay after creating new tabs
- Error handling for missing agents or failed operations

### Troubleshooting
- **Coordinates not found**: Ensure agent windows are open and positioned correctly
- **PyAutoGUI not available**: Install with `pip install pyautogui`
- **Message not sent**: Check if agent window is focused and ready

## 🎯 Testing Scenarios

### Scenario 1: Single Agent Test
```bash
# Send a simple test message
python -m src.services.messaging_cli --agent Agent-1 --message "🧪 PyAutoGUI test successful!" --mode pyautogui
```

### Scenario 2: Bulk System Test
```bash
# Send system-wide message
python -m src.services.messaging_cli --bulk --message "🚨 System test - PyAutoGUI mode working!" --mode pyautogui
```

### Scenario 3: High Priority Test
```bash
# Send urgent message
python -m src.services.messaging_cli --agent Agent-1 --message "🚨 URGENT: PyAutoGUI test!" --high-priority --mode pyautogui
```

### Scenario 4: Type Mode Test
```bash
# Test typing instead of pasting
python -m src.services.messaging_cli --agent Agent-1 --message "Typing test message" --no-paste --mode pyautogui
```

## ✅ Success Indicators

When PyAutoGUI mode is working correctly, you should see:

1. **Mouse Movement**: Mouse moves to agent coordinates
2. **New Tab Creation**: Ctrl+T creates new tab
3. **Message Pasting**: Message appears in agent window
4. **Send Confirmation**: Enter key sends the message
5. **Success Status**: "✅ MESSAGE DELIVERED TO [Agent]" message

## 🔍 Verification

After sending messages, verify delivery by:

1. **Check Message History**:
   ```bash
   python -m src.services.messaging_cli --history
   ```

2. **Check Agent Status**:
   ```bash
   python -m src.services.messaging_cli --check-status
   ```

3. **Manual Verification**: Check agent inbox files in `agent_workspaces/[Agent]/inbox/`

## 🎉 Conclusion

The PyAutoGUI mode provides a robust, coordinate-based messaging system that works independently of the onboarding functionality. It enables direct communication with agents through automated UI interaction, making it perfect for testing and operational use.

**Key Benefits:**
- ✅ No onboarding dependency
- ✅ Direct agent communication
- ✅ Bulk messaging capabilities
- ✅ Full CLI interface
- ✅ Comprehensive error handling
- ✅ Flexible delivery options

**WE. ARE. SWARM.** ⚡🔥
