# 👨‍💻 **Developer Guide - Agent Cellphone V2**

**Comprehensive guide for developers working on the Agent Cellphone V2 system**

---

## 🎯 **Table of Contents**

1. [Getting Started](#getting-started)
2. [Development Environment](#development-environment)
3. [Code Standards](#code-standards)
4. [Architecture Guidelines](#architecture-guidelines)
5. [Testing Guidelines](#testing-guidelines)
6. [Documentation Standards](#documentation-standards)
7. [Deployment Process](#deployment-process)
8. [Troubleshooting](#troubleshooting)

---

## 🚀 **Getting Started**

### **Prerequisites**

- **Python 3.8+** (recommended: Python 3.11+)
- **Git** for version control
- **Cursor IDE** for development
- **Dual Monitor Setup** for swarm testing

### **Initial Setup**

```bash
# Clone the repository
git clone <repository-url>
cd Agent_Cellphone_V2_Repository

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Verify installation
python -c "import src.services.consolidated_messaging_service; print('✅ Setup complete')"
```

### **Project Structure**

```
Agent_Cellphone_V2_Repository/
├── src/                          # Source code
│   ├── services/                 # Service layer
│   │   ├── consolidated_messaging_service.py
│   │   └── role_manager.py
│   ├── core/                     # Core functionality
│   │   ├── coordinate_loader.py
│   │   └── backup_disaster_recovery/
│   ├── discord_commander/        # Discord integration
│   └── utils/                    # Utility functions
├── tests/                        # Test suites
├── docs/                         # Documentation
├── config/                       # Configuration files
├── examples/                     # Usage examples
└── scripts/                      # Utility scripts
```

---

## 🛠️ **Development Environment**

### **IDE Configuration**

#### **Cursor IDE Setup**
1. Install Python extension
2. Configure Python interpreter to use virtual environment
3. Enable auto-formatting with Black
4. Set up linting with Ruff

#### **VS Code Alternative**
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.ruffEnabled": true,
    "editor.formatOnSave": true
}
```

### **Environment Variables**

Create `.env` file in project root:
```bash
# Development settings
LOG_LEVEL=DEBUG
PYTHONPATH=.

# PyAutoGUI settings
PYAUTO_PAUSE_S=0.05
PYAUTO_MOVE_DURATION=0.4

# Discord bot (for testing)
DISCORD_BOT_TOKEN=your_test_token
DISCORD_CHANNEL_ID=your_test_channel

# Database (if using)
DATABASE_URL=sqlite:///dev.db
```

### **Pre-commit Hooks**

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

---

## 📏 **Code Standards**

### **V2 Compliance Requirements**

#### **File Size Limits**
- **Maximum 400 lines** per file
- **Classes ≤ 200 lines**
- **Functions ≤ 30 lines**
- **Violations require immediate refactoring**

#### **SOLID Principles**

1. **Single Responsibility Principle (SRP)**
   ```python
   # ✅ Good: Single responsibility
   class MessageValidator:
       def validate_message(self, message: UnifiedMessage) -> bool:
           # Only validates messages
           pass
   
   # ❌ Bad: Multiple responsibilities
   class MessageHandler:
       def validate_message(self, message): pass
       def send_message(self, message): pass
       def log_message(self, message): pass
   ```

2. **Open/Closed Principle (OCP)**
   ```python
   # ✅ Good: Open for extension, closed for modification
   class MessageDeliveryMethod(ABC):
       @abstractmethod
       def deliver(self, message: UnifiedMessage) -> bool:
           pass
   
   class PyAutoGUIDelivery(MessageDeliveryMethod):
       def deliver(self, message: UnifiedMessage) -> bool:
           # Implementation
           pass
   ```

3. **Liskov Substitution Principle (LSP)**
   ```python
   # ✅ Good: Subtypes are substitutable
   def process_delivery(delivery_method: MessageDeliveryMethod):
       return delivery_method.deliver(message)
   
   # Works with any MessageDeliveryMethod implementation
   process_delivery(PyAutoGUIDelivery())
   process_delivery(InboxDelivery())
   ```

4. **Interface Segregation Principle (ISP)**
   ```python
   # ✅ Good: Focused interfaces
   class MessageSender(ABC):
       @abstractmethod
       def send_message(self, message: UnifiedMessage) -> bool:
           pass
   
   class MessageReceiver(ABC):
       @abstractmethod
       def receive_message(self) -> UnifiedMessage:
           pass
   ```

5. **Dependency Inversion Principle (DIP)**
   ```python
   # ✅ Good: Depend on abstractions
   class MessagingService:
       def __init__(self, delivery_method: MessageDeliveryMethod):
           self.delivery_method = delivery_method
   
   # ❌ Bad: Depend on concrete implementations
   class MessagingService:
       def __init__(self):
           self.delivery_method = PyAutoGUIDelivery()
   ```

### **Code Style Guidelines**

#### **Naming Conventions**
```python
# Classes: PascalCase
class UnifiedMessage:
    pass

# Functions/Variables: snake_case
def send_message(message: UnifiedMessage) -> bool:
    success_status = True
    return success_status

# Constants: UPPER_SNAKE_CASE
MAX_RETRY_ATTEMPTS = 3
DEFAULT_TIMEOUT = 30

# Private methods: leading underscore
def _validate_coordinates(self, x: int, y: int) -> bool:
    pass
```

#### **Type Hints**
```python
from typing import List, Dict, Optional, Union, Any

def process_messages(
    messages: List[UnifiedMessage],
    options: Optional[Dict[str, Any]] = None
) -> Union[bool, Dict[str, Any]]:
    pass
```

#### **Docstring Format**
```python
def send_message(
    message: UnifiedMessage,
    retry_count: int = 3
) -> bool:
    """
    Send a message using the configured delivery method.
    
    Args:
        message: The message to send
        retry_count: Number of retry attempts (default: 3)
        
    Returns:
        bool: True if message sent successfully, False otherwise
        
    Raises:
        MessagingError: If message delivery fails after all retries
        
    Example:
        >>> message = UnifiedMessage(content="Hello", sender="Agent-1", recipient="Agent-2")
        >>> success = send_message(message)
        >>> print(f"Message sent: {success}")
    """
    pass
```

---

## 🏗️ **Architecture Guidelines**

### **Module Organization**

#### **Service Layer**
```python
# src/services/messaging_service.py
class MessagingService:
    """High-level messaging operations."""
    
    def __init__(self, delivery_method: MessageDeliveryMethod):
        self.delivery_method = delivery_method
    
    async def send_message(self, message: UnifiedMessage) -> bool:
        """Send message with error handling and retries."""
        pass
```

#### **Core Layer**
```python
# src/core/message_delivery.py
class MessageDeliveryMethod(ABC):
    """Abstract base class for message delivery methods."""
    
    @abstractmethod
    async def deliver(self, message: UnifiedMessage) -> bool:
        """Deliver message using specific method."""
        pass
```

#### **Infrastructure Layer**
```python
# src/infrastructure/pyautogui_delivery.py
class PyAutoGUIDelivery(MessageDeliveryMethod):
    """PyAutoGUI-based message delivery."""
    
    async def deliver(self, message: UnifiedMessage) -> bool:
        """Deliver message using PyAutoGUI automation."""
        pass
```

### **Dependency Injection**

```python
# Container for dependency injection
class ServiceContainer:
    def __init__(self):
        self._services = {}
    
    def register(self, interface: type, implementation: type):
        self._services[interface] = implementation
    
    def get(self, interface: type):
        return self._services[interface]()

# Usage
container = ServiceContainer()
container.register(MessageDeliveryMethod, PyAutoGUIDelivery)
delivery_method = container.get(MessageDeliveryMethod)
```

### **Configuration Management**

```python
# src/core/config.py
class Config:
    """Centralized configuration management."""
    
    def __init__(self, config_path: str = "config/unified_config.yaml"):
        self.config = self._load_config(config_path)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key."""
        keys = key.split('.')
        value = self.config
        for k in keys:
            value = value.get(k, {})
        return value if value != {} else default
```

---

## 🧪 **Testing Guidelines**

### **Test Structure**

```
tests/
├── unit/                          # Unit tests
│   ├── test_messaging_service.py
│   ├── test_coordinate_loader.py
│   └── test_backup_system.py
├── integration/                   # Integration tests
│   ├── test_messaging_flow.py
│   └── test_backup_recovery.py
├── e2e/                          # End-to-end tests
│   └── test_full_workflow.py
└── fixtures/                     # Test fixtures
    ├── sample_messages.py
    └── test_configs.py
```

### **Unit Testing**

```python
# tests/unit/test_messaging_service.py
import pytest
from unittest.mock import Mock, patch
from src.services.consolidated_messaging_service import (
    UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority, send_message
)

class TestMessagingService:
    """Test suite for messaging service."""
    
    @pytest.fixture
    def sample_message(self):
        """Create sample message for testing."""
        return UnifiedMessage(
            content="Test message",
            sender="TestSender",
            recipient="TestRecipient",
            message_type=UnifiedMessageType.AGENT_TO_AGENT,
            priority=UnifiedMessagePriority.NORMAL
        )
    
    @pytest.mark.asyncio
    async def test_send_message_success(self, sample_message):
        """Test successful message sending."""
        with patch('src.services.consolidated_messaging_service.deliver_message_pyautogui') as mock_deliver:
            mock_deliver.return_value = True
            
            result = await send_message(sample_message)
            
            assert result is True
            mock_deliver.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_send_message_failure(self, sample_message):
        """Test message sending failure."""
        with patch('src.services.consolidated_messaging_service.deliver_message_pyautogui') as mock_deliver:
            mock_deliver.return_value = False
            
            result = await send_message(sample_message)
            
            assert result is False
```

### **Integration Testing**

```python
# tests/integration/test_messaging_flow.py
import pytest
import asyncio
from src.services.consolidated_messaging_service import (
    UnifiedMessage, UnifiedMessageType, send_message, broadcast_message
)

class TestMessagingFlow:
    """Integration tests for messaging flow."""
    
    @pytest.mark.asyncio
    async def test_complete_messaging_workflow(self):
        """Test complete messaging workflow."""
        # Test individual message
        message = UnifiedMessage(
            content="Integration test message",
            sender="TestAgent",
            recipient="Agent-1",
            message_type=UnifiedMessageType.AGENT_TO_AGENT
        )
        
        success = await send_message(message)
        assert success is True
        
        # Test broadcast
        broadcast_success = await broadcast_message(
            "Integration test broadcast",
            "TestAgent"
        )
        assert broadcast_success is True
```

### **Test Configuration**

```python
# conftest.py
import pytest
import asyncio
from pathlib import Path

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def test_config():
    """Load test configuration."""
    return {
        "messaging": {
            "timeout": 5,
            "retry_attempts": 1
        },
        "coordinates": {
            "validation_enabled": False
        }
    }
```

### **Running Tests**

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_messaging_service.py

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test method
pytest tests/unit/test_messaging_service.py::TestMessagingService::test_send_message_success

# Run with verbose output
pytest -v

# Run only failed tests
pytest --lf
```

---

## 📚 **Documentation Standards**

### **Module Documentation**

```python
"""
Module Name

Brief description of the module's purpose and functionality.

This module provides [detailed description of what the module does,
including key classes, functions, and their purposes].

Author: Agent-8 (SSOT & System Integration Specialist)
Version: 2.0
Created: 2024-01-01
Last Modified: 2024-01-01

Example:
    Basic usage example showing how to use the module.
    
    >>> from module_name import ClassName
    >>> instance = ClassName()
    >>> result = instance.method()
    >>> print(result)
"""

import logging
from typing import List, Optional

logger = logging.getLogger(__name__)
```

### **Class Documentation**

```python
class ExampleClass:
    """
    Brief description of the class.
    
    Detailed description of the class, including its purpose,
    key functionality, and any important design decisions.
    
    Attributes:
        attribute1 (type): Description of attribute1
        attribute2 (type): Description of attribute2
        
    Example:
        >>> instance = ExampleClass("value1", "value2")
        >>> result = instance.method()
        >>> print(result)
    """
    
    def __init__(self, param1: str, param2: str):
        """
        Initialize the ExampleClass.
        
        Args:
            param1: Description of param1
            param2: Description of param2
            
        Raises:
            ValueError: If param1 is empty
        """
        if not param1:
            raise ValueError("param1 cannot be empty")
        self.attribute1 = param1
        self.attribute2 = param2
```

### **Function Documentation**

```python
def example_function(
    required_param: str,
    optional_param: Optional[int] = None,
    *args: str,
    **kwargs: Any
) -> bool:
    """
    Brief description of the function.
    
    Detailed description of what the function does, including
    any side effects, return values, and important behavior.
    
    Args:
        required_param: Description of required parameter
        optional_param: Description of optional parameter (default: None)
        *args: Variable length argument list
        **kwargs: Arbitrary keyword arguments
        
    Returns:
        bool: Description of return value
        
    Raises:
        ValueError: When required_param is invalid
        RuntimeError: When operation fails
        
    Example:
        >>> result = example_function("test", optional_param=42)
        >>> print(f"Result: {result}")
        Result: True
        
    Note:
        Additional notes about the function's behavior or usage.
    """
    if not required_param:
        raise ValueError("required_param cannot be empty")
    
    # Function implementation
    return True
```

### **API Documentation**

Use the existing [API Reference](API_REFERENCE.md) as a template for documenting new APIs.

---

## 🚀 **Deployment Process**

### **Development Workflow**

1. **Feature Development**
   ```bash
   # Create feature branch
   git checkout -b feature/new-feature
   
   # Make changes
   # Write tests
   # Update documentation
   
   # Commit changes
   git add .
   git commit -m "feat: add new feature"
   ```

2. **Testing**
   ```bash
   # Run tests
   pytest
   
   # Run linting
   ruff check src/
   
   # Run formatting
   black src/
   
   # Run pre-commit hooks
   pre-commit run --all-files
   ```

3. **Code Review**
   ```bash
   # Push branch
   git push origin feature/new-feature
   
   # Create pull request
   # Request review from team members
   # Address feedback
   ```

4. **Merge and Deploy**
   ```bash
   # Merge to main branch
   git checkout main
   git merge feature/new-feature
   
   # Tag release
   git tag -a v2.1.0 -m "Release version 2.1.0"
   git push origin v2.1.0
   ```

### **Release Process**

1. **Version Bumping**
   ```bash
   # Update version in setup.py or pyproject.toml
   # Update CHANGELOG.md
   # Update documentation
   ```

2. **Testing Release**
   ```bash
   # Run full test suite
   pytest --cov=src --cov-report=html
   
   # Run integration tests
   pytest tests/integration/
   
   # Run end-to-end tests
   pytest tests/e2e/
   ```

3. **Documentation Update**
   ```bash
   # Update API documentation
   # Update user guides
   # Update architecture documentation
   ```

### **Deployment Options**

#### **Local Deployment**
```bash
# Install in development mode
pip install -e .

# Run system
python -m src.services.consolidated_messaging_service
```

#### **Docker Deployment**
```bash
# Build image
docker build -t agent-cellphone-v2 .

# Run container
docker run -d --name agent-cellphone-v2 agent-cellphone-v2
```

#### **Production Deployment**
```bash
# Install production dependencies
pip install -r requirements.txt

# Configure production settings
export LOG_LEVEL=INFO
export ENVIRONMENT=production

# Run with process manager
pm2 start ecosystem.config.js
```

---

## 🔧 **Troubleshooting**

### **Common Development Issues**

#### **1. Import Errors**
```bash
# Error: ModuleNotFoundError: No module named 'src'
# Solution: Add project root to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
# Or use: python -c "import sys; sys.path.insert(0, '.')"
```

#### **2. Test Failures**
```bash
# Error: Tests failing due to missing dependencies
# Solution: Install test dependencies
pip install -r requirements-dev.txt

# Error: Async test failures
# Solution: Ensure proper async test setup
pytest --asyncio-mode=auto
```

#### **3. Linting Errors**
```bash
# Error: Black formatting issues
# Solution: Run Black formatter
black src/ tests/

# Error: Ruff linting issues
# Solution: Run Ruff linter
ruff check src/ --fix
```

#### **4. Configuration Issues**
```bash
# Error: Configuration file not found
# Solution: Check file paths and permissions
ls -la config/
chmod 644 config/*.yaml config/*.json
```

### **Debugging Tools**

#### **Logging Configuration**
```python
import logging

# Configure logging for development
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

#### **Debug Mode**
```python
# Enable debug mode
import os
os.environ['DEBUG'] = 'true'

# Use debugger
import pdb; pdb.set_trace()
```

#### **Performance Profiling**
```python
import cProfile
import pstats

# Profile function
profiler = cProfile.Profile()
profiler.enable()

# Your code here
result = your_function()

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats()
```

---

## 📚 **Additional Resources**

### **Development Tools**
- **[API Reference](API_REFERENCE.md)** - Complete API documentation
- **[Usage Examples](USAGE_EXAMPLES.md)** - Comprehensive examples
- **[Architecture Overview](ARCHITECTURE.md)** - System architecture
- **[Quick Start Guide](QUICK_START.md)** - Getting started quickly

### **External Resources**
- **[Python Documentation](https://docs.python.org/3/)**
- **[Pytest Documentation](https://docs.pytest.org/)**
- **[Black Documentation](https://black.readthedocs.io/)**
- **[Ruff Documentation](https://docs.astral.sh/ruff/)**

### **Team Resources**
- **Code Review Guidelines** - Internal team document
- **Deployment Procedures** - Internal team document
- **Incident Response** - Internal team document

---

## 🤝 **Contributing**

### **How to Contribute**

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Write tests**
5. **Update documentation**
6. **Submit a pull request**

### **Contribution Guidelines**

- Follow V2 compliance requirements
- Write comprehensive tests
- Update documentation
- Follow code style guidelines
- Ensure all tests pass

### **Getting Help**

- **Issues**: Report bugs and request features
- **Discussions**: Ask questions and share ideas
- **Documentation**: Check existing documentation first
- **Team Chat**: Internal team communication

---

**📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory**

