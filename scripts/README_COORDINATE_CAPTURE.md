# Coordinate Capture Tools - Agent Cellphone V2

## 🎯 **Interactive Coordinate Capture System**

This directory contains tools to capture and update agent coordinates for the messaging system.

## 📁 **Available Tools**

### 1. **Interactive Coordinate Capture** (`capture_coordinates.py`)
**Features:**
- Real-time cursor position display
- Press ENTER to capture coordinates
- Press ESC to skip an agent
- Press Q to quit
- Requires `keyboard` module

**Usage:**
```bash
python scripts/capture_coordinates.py
```

### 2. **Simple Coordinate Capture** (`simple_coordinate_capture.py`)
**Features:**
- Type ENTER to capture coordinates
- Type 'skip' to skip an agent
- Type 'quit' to exit
- Only requires `pyautogui` module

**Usage:**
```bash
python scripts/simple_coordinate_capture.py
```

### 3. **Show Current Coordinates**
**Usage:**
```bash
python scripts/simple_coordinate_capture.py --show
```

## 🚀 **How to Use**

### **Step 1: Prepare Your Setup**
1. Make sure all agent chat windows are visible and positioned correctly
2. Ensure you can see the chat input fields for each agent
3. Have the coordinate capture tool ready

### **Step 2: Run the Capture Tool**
```bash
# For interactive capture (recommended)
python scripts/capture_coordinates.py

# For simple capture (fallback)
python scripts/simple_coordinate_capture.py
```

### **Step 3: Capture Coordinates**
1. **Hover** your cursor over the agent's chat input field
2. **Press ENTER** (or type 'enter' for simple version) to capture
3. **Repeat** for each agent
4. **Skip** agents you don't want to update
5. **Quit** when done

### **Step 4: Verify Results**
```bash
python scripts/simple_coordinate_capture.py --show
```

## 📐 **Coordinate System**

- **Origin**: Top-left corner of screen
- **Unit**: Pixels
- **Max Resolution**: 3840x2160 (4K)
- **Multi-monitor**: Supports negative coordinates
- **Validation**: Coordinates are validated before saving

## 🔧 **Installation Requirements**

### **Required:**
```bash
pip install pyautogui
```

### **Optional (for interactive version):**
```bash
pip install keyboard
```

## 📍 **Current Agent Coordinates**

| Agent | Coordinates | Description |
|-------|-------------|-------------|
| Agent-1 | `[-1269, 481]` | Integration & Core Systems Specialist |
| Agent-2 | `[-308, 480]` | Architecture & Design Specialist |
| Agent-3 | `[-1269, 1001]` | Infrastructure & DevOps Specialist |
| Agent-4 | `[-308, 1000]` | Quality Assurance Specialist (CAPTAIN) |
| Agent-5 | `[652, 421]` | Business Intelligence Specialist |
| Agent-6 | `[1612, 419]` | Coordination & Communication Specialist |
| Agent-7 | `[653, 940]` | Web Development Specialist |
| Agent-8 | `[1611, 941]` | SSOT & System Integration Specialist |

## 🛠️ **Troubleshooting**

### **PyAutoGUI Issues:**
- Make sure you have the latest version: `pip install --upgrade pyautogui`
- On some systems, you may need to run as administrator

### **Keyboard Module Issues:**
- Use the simple coordinate capture tool instead
- Install keyboard module: `pip install keyboard`

### **Permission Issues:**
- Run the script as administrator if needed
- Check that the coordinate file is writable

## 🔄 **Integration with Messaging System**

The captured coordinates are automatically used by:
- **PyAutoGUI Message Delivery**: Direct message delivery to agent chat windows
- **Messaging CLI**: `--coordinates` command shows current positions
- **Fallback System**: Inbox delivery if coordinates fail

## 📝 **File Structure**

```
cursor_agent_coords.json          # Main coordinate configuration file
scripts/
├── capture_coordinates.py        # Interactive coordinate capture
├── simple_coordinate_capture.py  # Simple coordinate capture
└── README_COORDINATE_CAPTURE.md  # This documentation
```

## 🎉 **Success!**

Once you've captured coordinates, the messaging system will automatically use them for PyAutoGUI-based message delivery to the correct agent chat windows.

**Agent-3 - Infrastructure & DevOps Specialist**  
**Mission**: Coordinate Capture System Implementation  
**Status**: **COMPLETED** ✅

**WE. ARE. SWARM.** 🚀
