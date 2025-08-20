# Agent_Cellphone_V2

**Clean, Standardized Agent Coordination System**

A modern, well-architected system for managing autonomous agents with clean separation of concerns, standardized interfaces, and comprehensive testing.

## 🏗️ Architecture Overview

```
Agent_Cellphone_V2/
├── src/                    # Source code
│   ├── core/              # Core components
│   │   ├── agent_manager.py      # Agent lifecycle management
│   │   ├── message_router.py     # Message routing system
│   │   └── config_manager.py     # Configuration management
│   ├── services/          # High-level services
│   │   ├── agent_cell_phone.py   # Main coordination interface
│   │   └── coordination.py       # Multi-agent coordination
│   ├── launchers/         # System launch
│   │   └── unified_launcher.py   # Multi-mode launcher
│   └── utils/             # Shared utilities
│       └── shared_utils.py       # Common helper functions
├── config/                # Configuration
│   └── unified_config.yaml       # Single config file
├── examples/              # Demonstrations
│   └── demo_suite.py             # Comprehensive demo
├── tests/                 # Testing
│   └── test_suite.py             # Complete test suite
└── README.md              # This file
```

## 🎯 Design Principles

- **Single Responsibility**: Each module has one clear purpose
- **Dependency Injection**: Loose coupling between components
- **Interface Segregation**: Clean, focused interfaces
- **Clean Architecture**: Clear separation of concerns
- **Comprehensive Testing**: Full test coverage with examples

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Required packages (see `requirements.txt`)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd Agent_Cellphone_V2

# Install dependencies
pip install -r requirements.txt

# Run demo
python examples/demo_suite.py

# Run tests
python tests/test_suite.py

# Launch system
python src/launchers/unified_launcher.py --mode standalone
```

## 🔧 Core Components

### Agent Manager (`src/core/agent_manager.py`)

Manages agent lifecycle including:
- Registration and initialization
- Status management and monitoring
- Lifecycle control (start, stop, restart)
- Health checking and diagnostics

```python
from src.core.agent_manager import AgentManager

manager = AgentManager()
manager.register_agent("agent-1", "Test Agent", ["communication"])
manager.start_agent("agent-1")
status = manager.get_agent_status("agent-1")
```

### Message Router (`src/core/message_router.py`)

Handles intelligent message routing between agents:
- Message validation and preprocessing
- Routing logic and destination selection
- Message queuing and delivery
- Response handling and error management

```python
from src.core.message_router import MessageRouter, MessageType, MessagePriority

router = MessageRouter()
router.register_agent("agent-1")
message_id = router.send_message(
    "sender", "agent-1", "Hello!", 
    MessageType.NOTIFICATION, MessagePriority.NORMAL
)
```

### Config Manager (`src/core/config_manager.py`)

Provides unified configuration management:
- Configuration file loading and validation
- Environment-specific settings
- Configuration hot-reloading
- Default value management

```python
from src.core.config_manager import ConfigManager

config = ConfigManager("config")
log_level = config.get_config("system", "logging.level", "INFO")
max_agents = config.get_config("system", "performance.max_agents", 8)
```

## 🎭 Services Layer

### Agent Cell Phone (`src/services/agent_cell_phone.py`)

Main coordination interface that integrates core components:
- Agent registration and management
- Message routing and delivery
- Configuration management
- High-level coordination operations

```python
from src.services.agent_cell_phone import AgentCellPhone

acp = AgentCellPhone("config")
acp.register_agent("coordinator", "Coordinator", ["coordination"])
acp.send_message("system", "coordinator", "Start coordination")
```

### Coordination Service (`src/services/coordination.py`)

Advanced coordination capabilities for managing multiple agents:
- Task workflow management
- Dependency resolution
- Progress tracking
- Result aggregation
- Error handling and recovery

```python
from src.services.coordination import CoordinationService

coord = CoordinationService(message_router, agent_manager)
task_id = coord.create_coordination_task(
    "Data Processing", "Process data through stages", 
    ["worker-1", "worker-2"]
)
coord.start_coordination_task(task_id)
```

## 🚀 Launch Modes

The unified launcher supports multiple modes:

- **Standalone**: Basic agent management
- **Coordination**: Full coordination capabilities
- **Demo**: Demonstration mode with examples
- **Test**: Testing mode for validation

```bash
# Launch in different modes
python src/launchers/unified_launcher.py --mode standalone
python src/launchers/unified_launcher.py --mode coordination
python src/launchers/unified_launcher.py --mode demo
python src/launchers/unified_launcher.py --mode test
```

## 🧪 Testing

Comprehensive testing suite covering:

- **Unit Tests**: Individual component testing
- **Integration Tests**: Service integration testing
- **System Tests**: Complete workflow testing
- **Performance Tests**: Stress and performance validation

```bash
# Run all tests
python tests/test_suite.py

# Run specific test class
python -m unittest tests.test_suite.TestAgentManager

# Run with coverage
coverage run tests/test_suite.py
coverage report
```

## 📊 Demo Suite

The demo suite showcases all system capabilities:

```bash
# Run comprehensive demo
python examples/demo_suite.py

# Demo includes:
# - Basic agent management
# - Message routing and communication
# - Coordination workflows
# - System monitoring and status
```

## ⚙️ Configuration

All configuration is centralized in `config/unified_config.yaml`:

```yaml
system:
  name: "Agent_Cellphone_V2"
  version: "2.0.0"
  logging:
    level: "INFO"
    file: "logs/system.log"

agents:
  default_capabilities:
    - "communication"
    - "task_execution"
    - "coordination"

messaging:
  routing:
    enable_rules: true
    default_timeout: 10.0
```

## 🛠️ Utilities

Shared utilities provide common functionality:

```python
from src.utils.shared_utils import (
    FileUtils, ValidationUtils, DataUtils, 
    SystemUtils, TimeUtils, LoggingUtils
)

# File operations
FileUtils.ensure_directory("logs")
FileUtils.safe_write_json("data.json", {"key": "value"})

# Data validation
ValidationUtils.is_valid_email("test@example.com")
ValidationUtils.validate_required_fields(data, ["required_field"])

# Data transformation
DataUtils.flatten_dict(nested_dict)
DataUtils.deep_merge(dict1, dict2)

# System information
SystemUtils.get_system_info()
SystemUtils.get_memory_usage()
```

## 📱 **V2 COORDINATION SYSTEM**

**Status**: ✅ FULLY OPERATIONAL  
**Added**: 2024-08-19 by Captain-5  

### **Messaging Systems**:

#### **1. Captain Coordinator V2** (`src/services/captain_coordinator_v2.py`)
- **Purpose**: Primary PyAutoGUI-based agent messaging
- **Features**: Agent activation, high-priority messaging, status tracking
- **Usage**: 
```bash
python src/services/captain_coordinator_v2.py --to Agent-4 --message "Hello!" --high-priority
```

#### **2. PyAutoGUI Script** (`send_agent_message_pyautogui.py`)
- **Purpose**: Direct PyAutoGUI messaging fallback
- **Features**: Simple message sending with Alt+Enter support
- **Usage**:
```bash
python send_agent_message_pyautogui.py Agent-3 "Message!" --high-priority
```

#### **3. Unified Messaging Hub** (`src/services/agent_messaging_hub.py`)
- **Purpose**: Automatic fallback between messaging systems
- **Features**: System testing, broadcast messaging, unified CLI
- **Usage**:
```bash
python src/services/agent_messaging_hub.py --broadcast --message "Team update!" --high-priority
```

### **Quick Start - Coordination**:
```bash
# Test all messaging systems
python src/services/agent_messaging_hub.py --test

# Send high-priority message to specific agent
python src/services/agent_messaging_hub.py --to Agent-4 --message "Urgent task!" --high-priority

# Broadcast to all agents
python src/services/agent_messaging_hub.py --broadcast --message "Team meeting!" --high-priority
```

### **Documentation**:
- [V2 Coordination System API](V2_COORDINATION_SYSTEM_API.md) - Complete API documentation
- [V2 Coordination System Status](V2_COORDINATION_SYSTEM_STATUS.md) - System status and capabilities
- [Captain-5 Leadership Goals](CAPTAIN_5_LEADERSHIP_GOALS.md) - Leadership and contract tracking

## 🔄 Migration from V1

This version provides a clean, standardized architecture compared to V1:

- **Consolidated Structure**: Single configuration file vs. multiple scattered files
- **Clean Interfaces**: Well-defined APIs vs. ad-hoc implementations
- **PyAutoGUI Coordination**: Working agent messaging vs. broken imports
- **Comprehensive Testing**: Full test coverage vs. minimal testing
- **Standardized Patterns**: Consistent design patterns throughout
- **Better Documentation**: Clear documentation vs. scattered notes

## 📈 Performance

The system is designed for performance:

- **Efficient Message Routing**: Queue-based message delivery
- **Minimal Dependencies**: Lightweight core components
- **Async-Ready**: Designed for asynchronous operations
- **Scalable Architecture**: Supports multiple agent types and workflows

## 🤝 Contributing

1. Follow the established architecture patterns
2. Add comprehensive tests for new features
3. Update documentation for any changes
4. Ensure all tests pass before submitting

## 📝 License

[Add your license information here]

## 🆘 Support

For support and questions:
- Check the demo suite for examples
- Review the test suite for usage patterns
- Examine the configuration for customization options

---

**Built with ❤️ by AGENT-2 Architecture Designer**
