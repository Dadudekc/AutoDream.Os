# 🚀 **Quick Start Guide - Agent Cellphone V2**

**Get up and running with Agent Cellphone V2 in minutes**

---

## 🎯 **Prerequisites**

### **System Requirements**
- **Python 3.8+** (recommended: Python 3.11+)
- **Windows 10/11** (primary platform)
- **Dual Monitor Setup** (recommended for full swarm functionality)
- **Cursor IDE** (for swarm coordination)

### **Required Dependencies**
```bash
# Core dependencies
pip install pyautogui pyperclip
pip install discord.py
pip install pyyaml
pip install asyncio

# Development dependencies (optional)
pip install pytest pytest-asyncio
pip install black ruff
```

---

## ⚡ **5-Minute Setup**

### **Step 1: Clone and Install**
```bash
# Clone the repository
git clone <repository-url>
cd Agent_Cellphone_V2_Repository

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import src.services.consolidated_messaging_service; print('✅ Installation successful')"
```

### **Step 2: Configure Coordinates**
```bash
# Check if coordinates are configured
python -c "from src.core.coordinate_loader import get_coordinate_loader; loader = get_coordinate_loader(); print(f'Agents: {loader.get_all_agents()}')"

# If coordinates are missing, create config/coordinates.json:
# {
#   "agents": {
#     "Agent-1": {"x": -1269, "y": 481},
#     "Agent-2": {"x": -308, "y": 480},
#     "Agent-3": {"x": -1269, "y": 1001},
#     "Agent-4": {"x": -308, "y": 1000},
#     "Agent-5": {"x": 652, "y": 421},
#     "Agent-6": {"x": 1612, "y": 419},
#     "Agent-7": {"x": 920, "y": 851},
#     "Agent-8": {"x": 1611, "y": 941}
#   }
# }
```

### **Step 3: Test Basic Functionality**
```bash
# Test coordinate system
python -c "
from src.core.coordinate_loader import get_coordinate_loader
loader = get_coordinate_loader()
agents = loader.get_all_agents()
print(f'✅ {len(agents)} agents configured')
for agent in agents[:3]:
    coords = loader.get_agent_coordinates(agent)
    print(f'   {agent}: {coords}')
"

# Test messaging system
python -c "
import asyncio
from src.services.consolidated_messaging_service import list_agents
async def test():
    agents = await list_agents()
    print(f'✅ Messaging system: {len(agents)} agents available')
asyncio.run(test())
"
```

### **Step 4: Send Your First Message**
```bash
# Send a test message
python -c "
import asyncio
from src.services.consolidated_messaging_service import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority, send_message

async def send_test():
    message = UnifiedMessage(
        content='Hello from Quick Start!',
        sender='QuickStart',
        recipient='Agent-1',
        message_type=UnifiedMessageType.AGENT_TO_AGENT,
        priority=UnifiedMessagePriority.NORMAL
    )
    success = await send_message(message)
    print(f'✅ Test message: {\"Sent\" if success else \"Failed\"}')

asyncio.run(send_test())
"
```

### **Step 5: Verify System Health**
```bash
# Run comprehensive health check
python -c "
import asyncio
import sys
from pathlib import Path
sys.path.insert(0, '.')

async def health_check():
    print('🔍 Agent Cellphone V2 - Health Check')
    print('=' * 40)

    # Test coordinate system
    try:
        from src.core.coordinate_loader import get_coordinate_loader
        loader = get_coordinate_loader()
        agents = loader.get_all_agents()
        print(f'✅ Coordinate System: {len(agents)} agents')
    except Exception as e:
        print(f'❌ Coordinate System: {e}')

    # Test messaging system
    try:
        from src.services.consolidated_messaging_service import list_agents
        agents = await list_agents()
        print(f'✅ Messaging System: {len(agents)} agents')
    except Exception as e:
        print(f'❌ Messaging System: {e}')

    # Test backup system
    try:
        from src.core.backup_disaster_recovery import BackupSystemCore
        backup = BackupSystemCore()
        print('✅ Backup System: Ready')
    except Exception as e:
        print(f'❌ Backup System: {e}')

    print('\\n🎉 Quick Start Complete!')

asyncio.run(health_check())
"
```

---

## 🎯 **Common Use Cases**

### **1. Send Message to Specific Agent**
```python
import asyncio
from src.services.consolidated_messaging_service import (
    UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority, send_message
)

async def send_to_agent():
    message = UnifiedMessage(
        content="Hello Agent-5!",
        sender="YourName",
        recipient="Agent-5",
        message_type=UnifiedMessageType.AGENT_TO_AGENT,
        priority=UnifiedMessagePriority.NORMAL
    )

    success = await send_message(message)
    print(f"Message sent: {success}")

asyncio.run(send_to_agent())
```

### **2. Broadcast to All Agents**
```python
import asyncio
from src.services.consolidated_messaging_service import broadcast_message

async def broadcast_to_all():
    success = await broadcast_message(
        "System maintenance in 10 minutes",
        "SystemAdmin"
    )
    print(f"Broadcast sent: {success}")

asyncio.run(broadcast_to_all())
```

### **3. Create System Backup**
```python
import asyncio
from src.core.backup_disaster_recovery import BackupSystemCore

async def create_backup():
    backup_system = BackupSystemCore()
    result = await backup_system.create_backup(
        backup_type="full",
        source_path=".",
        custom_name="quick_start_backup"
    )
    print(f"Backup created: {result.get('backup_id', 'Unknown')}")

asyncio.run(create_backup())
```

### **4. Check Agent Coordinates**
```python
from src.core.coordinate_loader import get_coordinate_loader

def check_coordinates():
    loader = get_coordinate_loader()
    agents = loader.get_all_agents()

    print("Agent Coordinates:")
    for agent_id in agents:
        coords = loader.get_agent_coordinates(agent_id)
        print(f"  {agent_id}: {coords}")

check_coordinates()
```

---

## 🛠️ **Configuration**

### **Environment Variables**
Create a `.env` file in the project root:
```bash
# PyAutoGUI Settings
PYAUTO_PAUSE_S=0.05
PYAUTO_MOVE_DURATION=0.4
PYAUTO_SEND_RETRIES=2

# Discord Bot (optional)
DISCORD_BOT_TOKEN=your_discord_bot_token
DISCORD_CHANNEL_ID=your_channel_id

# Logging
LOG_LEVEL=INFO
```

### **Configuration Files**

#### **config/coordinates.json**
```json
{
  "agents": {
    "Agent-1": {"x": -1269, "y": 481},
    "Agent-2": {"x": -308, "y": 480},
    "Agent-3": {"x": -1269, "y": 1001},
    "Agent-4": {"x": -308, "y": 1000},
    "Agent-5": {"x": 652, "y": 421},
    "Agent-6": {"x": 1612, "y": 419},
    "Agent-7": {"x": 920, "y": 851},
    "Agent-8": {"x": 1611, "y": 941}
  }
}
```

#### **config/unified_config.yaml**
```yaml
messaging:
  timeout: 30
  retry_attempts: 3
  fallback_enabled: true

coordinates:
  validation_enabled: true
  bounds_check: true

logging:
  level: INFO
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

backup:
  enabled: true
  default_type: "incremental"
  retention_days: 30
```

---

## 🧪 **Testing**

### **Run Basic Tests**
```bash
# Test coordinate system
python -c "
from src.core.coordinate_loader import get_coordinate_loader
loader = get_coordinate_loader()
print('✅ Coordinate system test passed')
"

# Test messaging system
python -c "
import asyncio
from src.services.consolidated_messaging_service import list_agents
async def test():
    agents = await list_agents()
    assert len(agents) > 0, 'No agents found'
    print('✅ Messaging system test passed')
asyncio.run(test())
"

# Test backup system
python -c "
from src.core.backup_disaster_recovery import BackupSystemCore
backup = BackupSystemCore()
print('✅ Backup system test passed')
"
```

### **Run Full Test Suite**
```bash
# Run all tests
pytest tests/ -v

# Run specific test categories
pytest tests/ -k "messaging" -v
pytest tests/ -k "coordinates" -v
pytest tests/ -k "backup" -v
```

---

## 🚨 **Troubleshooting**

### **Common Issues**

#### **1. Import Errors**
```bash
# Error: ModuleNotFoundError: No module named 'src'
# Solution: Add project root to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
# Or use: python -c "import sys; sys.path.insert(0, '.')"
```

#### **2. Coordinate Errors**
```bash
# Error: ValueError: Agent not found
# Solution: Check config/coordinates.json exists and has valid data
python -c "
import json
with open('config/coordinates.json', 'r') as f:
    data = json.load(f)
    print(f'Agents configured: {list(data.get(\"agents\", {}).keys())}')
"
```

#### **3. PyAutoGUI Issues**
```bash
# Error: PyAutoGUI not working
# Solution: Check if PyAutoGUI is installed and working
python -c "
import pyautogui
print(f'PyAutoGUI version: {pyautogui.__version__}')
print(f'Screen size: {pyautogui.size()}')
"
```

#### **4. Permission Errors**
```bash
# Error: Permission denied
# Solution: Run with appropriate permissions
# Windows: Run as Administrator
# Linux/Mac: Use sudo if needed
```

### **Debug Mode**
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Run with verbose output
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
# Your code here
"
```

---

## 📚 **Next Steps**

### **Learn More**
1. **[API Reference](API_REFERENCE.md)** - Complete API documentation
2. **[Usage Examples](USAGE_EXAMPLES.md)** - Comprehensive examples
3. **[Architecture Overview](ARCHITECTURE.md)** - System design details

### **Advanced Features**
1. **Discord Integration** - Set up Discord bot for remote control
2. **Backup Automation** - Configure automated backup schedules
3. **Business Continuity** - Set up disaster recovery plans
4. **Custom Agents** - Add your own agent types

### **Development**
1. **Contributing** - Learn how to contribute to the project
2. **Testing** - Add tests for new features
3. **Documentation** - Help improve documentation

---

## 🆘 **Getting Help**

### **Resources**
- **[Troubleshooting Guide](TROUBLESHOOTING.md)** - Common issues and solutions
- **[Development Workflow](DEVELOPMENT_WORKFLOW.md)** - Development guidelines
- **[Agent Tools Documentation](AGENT_TOOLS_DOCUMENTATION.md)** - Complete tools reference

### **Support**
- **Issues**: Report bugs and request features
- **Discussions**: Ask questions and share ideas
- **Documentation**: Check existing documentation first

---

## 🎉 **Congratulations!**

You've successfully set up Agent Cellphone V2!

**What you can do now:**
- ✅ Send messages between agents
- ✅ Broadcast to all agents
- ✅ Create system backups
- ✅ Manage agent coordinates
- ✅ Run comprehensive health checks

**Ready for more?** Check out the [Usage Examples](USAGE_EXAMPLES.md) for advanced workflows and integrations.

---

**📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory**
