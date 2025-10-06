# Contributing Guide - Agent Cellphone V2 Repository

**Version**: 2.0.0  
**Last Updated**: 2025-10-05  
**Agent**: Agent-7 (Elevated Web Development Expert)  

## 🌟 **Welcome Contributors**

Thank you for your interest in contributing to the Agent Cellphone V2 Repository! This guide will help you understand our development process, coding standards, and contribution workflow. We welcome contributions from developers, AI agents, and community members.

## 📋 **Table of Contents**

1. [Getting Started](#getting-started)
2. [Development Environment Setup](#development-environment-setup)
3. [Coding Standards](#coding-standards)
4. [V2 Compliance Requirements](#v2-compliance-requirements)
5. [Contribution Workflow](#contribution-workflow)
6. [Testing Requirements](#testing-requirements)
7. [Documentation Standards](#documentation-standards)
8. [Agent System Guidelines](#agent-system-guidelines)
9. [Code Review Process](#code-review-process)
10. [Release Process](#release-process)

## 🚀 **Getting Started**

### **Prerequisites**

Before contributing, ensure you have:

- **Python 3.8+** installed
- **Git** for version control
- **Node.js 16+** (for web components)
- **Discord Bot Token** (for testing agent coordination)
- **Basic understanding** of multi-agent systems
- **Familiarity** with V2 compliance standards

### **Repository Setup**

1. **Fork the repository**:
   ```bash
   git clone https://github.com/your-username/agent-cellphone-v2.git
   cd agent-cellphone-v2
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## 🔧 **Development Environment Setup**

### **IDE Configuration**

#### **Recommended IDEs**
- **VS Code** with Python extension
- **PyCharm** Professional or Community
- **Vim/Neovim** with Python plugins
- **Emacs** with Python mode

#### **VS Code Extensions**
```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.pylint",
    "ms-python.black-formatter",
    "ms-python.isort",
    "ms-vscode.vscode-json"
  ]
}
```

### **Pre-commit Hooks**

Install pre-commit hooks for automatic code formatting:

```bash
pip install pre-commit
pre-commit install
```

### **Development Tools**

#### **Code Quality Tools**
```bash
# Install development dependencies
pip install black isort pylint pytest pytest-cov mypy

# Format code
black src/ tests/
isort src/ tests/

# Lint code
pylint src/

# Type checking
mypy src/
```

#### **Testing Tools**
```bash
# Run tests
python -m pytest

# Run with coverage
python -m pytest --cov=src tests/

# Run specific test categories
python -m pytest tests/unit/
python -m pytest tests/integration/
```

## 📝 **Coding Standards**

### **Python Style Guide**

We follow **PEP 8** with the following modifications:

#### **Line Length**
- **Maximum**: 88 characters (Black default)
- **Soft limit**: 80 characters for readability

#### **Import Organization**
```python
# Standard library imports
import os
import sys
from pathlib import Path

# Third-party imports
import requests
from flask import Flask

# Local imports
from src.services.messaging_service import ConsolidatedMessagingService
```

#### **Function and Variable Naming**
```python
# Use snake_case for functions and variables
def send_message_to_agent():
    agent_status = "active"

# Use PascalCase for classes
class DiscordCommanderBot:
    pass

# Use UPPER_CASE for constants
MAX_MESSAGE_LENGTH = 2000
```

#### **Documentation Strings**
```python
def process_agent_message(message: str, priority: str) -> bool:
    """
    Process agent message with specified priority.
    
    Args:
        message: The message content to process
        priority: Message priority (NORMAL, HIGH, CRITICAL)
        
    Returns:
        True if message processed successfully, False otherwise
        
    Raises:
        ValueError: If priority is invalid
    """
    pass
```

### **File Organization**

#### **Module Structure**
```python
#!/usr/bin/env python3
"""
Module docstring describing the module's purpose.
"""

# Standard library imports
import logging

# Third-party imports
import requests

# Local imports
from .base import BaseService

# Constants
DEFAULT_TIMEOUT = 30

# Classes and functions
class ServiceClass:
    pass

def helper_function():
    pass

# Main execution
if __name__ == "__main__":
    pass
```

## 🎯 **V2 Compliance Requirements**

### **Critical V2 Standards**

All code must comply with V2 standards:

#### **File Size Limits**
- **Maximum lines**: ≤400 lines per file
- **Maximum classes**: ≤5 classes per module
- **Maximum functions**: ≤10 functions per module

#### **Architecture Restrictions**
- **NO** abstract classes
- **NO** complex inheritance hierarchies
- **NO** threading or multiprocessing
- **NO** complex design patterns

#### **Required Patterns**
- **Simple data classes** using `@dataclass`
- **Direct function calls** instead of callbacks
- **Basic validation** with simple if/else logic
- **KISS principle**: Keep It Simple, Stupid

#### **V2 Compliance Validation**

```bash
# Run V2 compliance check
python quality_gates.py

# Check specific file
python tools/v2_compliance_checker.py src/services/example.py
```

### **V2 Compliant Examples**

#### **Good V2 Code**
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class AgentMessage:
    """Simple data class for agent messages."""
    from_agent: str
    to_agent: str
    message: str
    priority: str = "NORMAL"

def validate_message(msg: AgentMessage) -> bool:
    """Simple validation function."""
    if not msg.from_agent or not msg.to_agent:
        return False
    if len(msg.message) > 2000:
        return False
    return True

def send_message(msg: AgentMessage) -> bool:
    """Simple message sending function."""
    if not validate_message(msg):
        return False
    
    # Direct implementation
    print(f"Sending: {msg.message}")
    return True
```

#### **Bad V2 Code (Avoid)**
```python
# Too complex - violates V2 standards
from abc import ABC, abstractmethod
import threading

class MessageHandler(ABC):
    @abstractmethod
    def handle_message(self, message):
        pass

class DiscordMessageHandler(MessageHandler):
    def __init__(self):
        self.thread_pool = threading.ThreadPoolExecutor(max_workers=5)
    
    def handle_message(self, message):
        # Complex threading logic
        pass
```

## 🔄 **Contribution Workflow**

### **Branch Strategy**

We use **GitFlow** with the following branches:

- **main**: Production-ready code
- **develop**: Integration branch for features
- **feature/**: Feature development branches
- **hotfix/**: Critical bug fixes
- **release/**: Release preparation branches

### **Creating a Feature Branch**

```bash
# Start from develop branch
git checkout develop
git pull origin develop

# Create feature branch
git checkout -b feature/your-feature-name

# Make your changes
# ... code changes ...

# Commit with descriptive message
git add .
git commit -m "feat: add new agent coordination feature

- Implement agent status monitoring
- Add Discord integration
- Update documentation

Closes #123"
```

### **Commit Message Format**

We use **Conventional Commits** format:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

#### **Types**
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

#### **Examples**
```bash
feat(discord): add agent status monitoring endpoint
fix(messaging): resolve message delivery timeout issue
docs(api): update API documentation for v2.0
test(thea): add integration tests for consultation system
```

### **Pull Request Process**

1. **Create Pull Request**:
   - Target: `develop` branch
   - Title: Clear, descriptive title
   - Description: Detailed explanation of changes

2. **PR Template**:
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Refactoring
   
   ## Testing
   - [ ] Unit tests pass
   - [ ] Integration tests pass
   - [ ] Manual testing completed
   
   ## V2 Compliance
   - [ ] File ≤400 lines
   - [ ] ≤5 classes per module
   - [ ] ≤10 functions per module
   - [ ] No abstract classes
   - [ ] No complex inheritance
   - [ ] No threading
   ```

3. **Code Review**:
   - At least 2 reviewers required
   - All CI checks must pass
   - V2 compliance validation required

## 🧪 **Testing Requirements**

### **Test Structure**

```
tests/
├── unit/                 # Unit tests
│   ├── services/        # Service unit tests
│   ├── agents/          # Agent unit tests
│   └── utils/           # Utility unit tests
├── integration/         # Integration tests
│   ├── discord/         # Discord integration tests
│   ├── thea/           # Thea integration tests
│   └── messaging/      # Messaging integration tests
└── fixtures/           # Test fixtures and data
```

### **Writing Tests**

#### **Unit Test Example**
```python
import pytest
from src.services.messaging_service import MessageValidator

class TestMessageValidator:
    """Test cases for MessageValidator."""
    
    def test_validate_message_success(self):
        """Test successful message validation."""
        validator = MessageValidator()
        result = validator.validate_message(
            from_agent="Agent-1",
            to_agent="Agent-2",
            message="Test message",
            priority="NORMAL"
        )
        assert result is True
    
    def test_validate_message_invalid_priority(self):
        """Test validation with invalid priority."""
        validator = MessageValidator()
        result = validator.validate_message(
            from_agent="Agent-1",
            to_agent="Agent-2",
            message="Test message",
            priority="INVALID"
        )
        assert result is False
    
    def test_validate_message_empty_agents(self):
        """Test validation with empty agent names."""
        validator = MessageValidator()
        result = validator.validate_message(
            from_agent="",
            to_agent="Agent-2",
            message="Test message",
            priority="NORMAL"
        )
        assert result is False
```

#### **Integration Test Example**
```python
import pytest
from src.services.discord_commander.bot_v2 import DiscordCommanderBotV2

@pytest.mark.asyncio
class TestDiscordCommanderIntegration:
    """Integration tests for Discord Commander."""
    
    async def test_bot_initialization(self):
        """Test bot initialization with valid config."""
        bot = DiscordCommanderBotV2(
            token="test_token",
            guild_id=12345
        )
        assert bot.token == "test_token"
        assert bot.guild_id == 12345
    
    async def test_agent_status_retrieval(self):
        """Test agent status retrieval."""
        bot = DiscordCommanderBotV2(
            token="test_token",
            guild_id=12345
        )
        status = await bot._get_agent_status("Agent-1")
        assert status in ["active", "inactive", "error"]
```

### **Running Tests**

```bash
# Run all tests
python -m pytest

# Run with verbose output
python -m pytest -v

# Run with coverage
python -m pytest --cov=src tests/

# Run specific test file
python -m pytest tests/unit/test_messaging_service.py

# Run tests matching pattern
python -m pytest -k "test_discord"

# Run integration tests only
python -m pytest tests/integration/
```

### **Test Coverage Requirements**

- **Minimum coverage**: 80%
- **Critical components**: 90%
- **New features**: 100% test coverage required

## 📚 **Documentation Standards**

### **Code Documentation**

#### **Module Documentation**
```python
#!/usr/bin/env python3
"""
Discord Commander Bot - V2 Compliant Implementation
==================================================

Discord bot for agent coordination and communication.
Provides REST API endpoints and WebSocket events for
real-time agent management.

Features:
- Agent status monitoring
- Message broadcasting
- Swarm coordination
- System health monitoring

V2 Compliance:
- ≤400 lines total
- ≤5 classes
- ≤10 functions
- Simple data classes only
- Direct function calls
- Basic validation

Usage:
    from src.services.discord_commander.bot_v2 import DiscordCommanderBotV2
    
    bot = DiscordCommanderBotV2(token="your_token", guild_id=12345)
    await bot.start()

Author: Agent-7 (Elevated Web Development Expert)
License: MIT
Version: 2.0.0
"""
```

#### **Function Documentation**
```python
def send_message_to_agent(
    agent_id: str, 
    message: str, 
    priority: str = "NORMAL"
) -> bool:
    """
    Send message to specified agent via Discord.
    
    Args:
        agent_id: Target agent identifier (Agent-1 to Agent-8)
        message: Message content (max 2000 characters)
        priority: Message priority (NORMAL, HIGH, CRITICAL)
        
    Returns:
        True if message sent successfully, False otherwise
        
    Raises:
        ValueError: If agent_id or priority is invalid
        ConnectionError: If Discord connection fails
        
    Example:
        >>> success = send_message_to_agent(
        ...     agent_id="Agent-7",
        ...     message="Task completed",
        ...     priority="HIGH"
        ... )
        >>> print(success)
        True
    """
    pass
```

### **API Documentation**

All API endpoints must be documented with:
- **Endpoint URL** and HTTP method
- **Request parameters** and body schema
- **Response format** and status codes
- **Error handling** and error codes
- **Usage examples** in multiple languages

### **README Updates**

When adding new features, update:
- **Feature list** in main README
- **Installation instructions** if dependencies change
- **Usage examples** for new functionality
- **Configuration options** if applicable

## 🤖 **Agent System Guidelines**

### **Agent Development**

#### **Agent Structure**
```python
class AgentTemplate:
    """Template for new agent development."""
    
    def __init__(self, agent_id: str):
        """Initialize agent with unique identifier."""
        self.agent_id = agent_id
        self.status = "initialized"
        self.capabilities = []
    
    def get_status(self) -> str:
        """Get current agent status."""
        return self.status
    
    def process_message(self, message: str) -> str:
        """Process incoming message."""
        # Simple message processing
        return f"Processed: {message}"
```

#### **Agent Communication**
```python
# Use messaging system for agent communication
from src.services.messaging_service import ConsolidatedMessagingService

messaging = ConsolidatedMessagingService()

# Send message to another agent
success = await messaging.send_message(
    from_agent="Agent-7",
    to_agent="Agent-4",
    message="Task completed",
    priority="NORMAL"
)

# Log agent activities
from src.services.agent_devlog_posting import AgentDevlogPoster

devlog = AgentDevlogPoster()
devlog.post_devlog(
    agent_id="Agent-7",
    action="Task completed successfully"
)
```

### **Agent Coordination**

#### **Role Assignment**
```python
# Use Captain CLI for role assignment
from tools.captain_cli import CaptainCLI

captain = CaptainCLI()
captain.assign_role(
    agent="Agent-7",
    role="IMPLEMENTATION_SPECIALIST",
    task="Documentation implementation",
    duration="1 cycle"
)
```

#### **Swarm Coordination**
```python
# Coordinate with other agents
python messaging_system.py Agent-7 Agent-4 "Coordination request" HIGH
```

## 🔍 **Code Review Process**

### **Review Checklist**

#### **Code Quality**
- [ ] **V2 Compliance**: File ≤400 lines, ≤5 classes, ≤10 functions
- [ ] **Code Style**: Follows PEP 8 and Black formatting
- [ ] **Type Hints**: All functions have proper type annotations
- [ ] **Documentation**: All public functions documented
- [ ] **Error Handling**: Proper exception handling
- [ ] **Performance**: No obvious performance issues

#### **Testing**
- [ ] **Unit Tests**: New code has unit tests
- [ ] **Integration Tests**: Integration points tested
- [ ] **Test Coverage**: Meets coverage requirements
- [ ] **Test Quality**: Tests are meaningful and comprehensive

#### **Documentation**
- [ ] **README**: Updated if needed
- [ ] **API Docs**: New APIs documented
- [ ] **Code Comments**: Complex logic explained
- [ ] **Changelog**: Changes documented

### **Review Process**

1. **Automated Checks**:
   - CI/CD pipeline runs automatically
   - V2 compliance validation
   - Test suite execution
   - Code quality checks

2. **Manual Review**:
   - At least 2 team members review
   - Focus on architecture and design
   - Verify V2 compliance manually
   - Test functionality manually

3. **Approval Criteria**:
   - All automated checks pass
   - All reviewers approve
   - No blocking issues identified
   - Documentation updated

## 🚀 **Release Process**

### **Release Preparation**

1. **Version Bumping**:
   ```bash
   # Update version in pyproject.toml
   # Update version in __init__.py files
   # Update CHANGELOG.md
   ```

2. **Release Testing**:
   ```bash
   # Run full test suite
   python -m pytest
   
   # Run V2 compliance check
   python quality_gates.py
   
   # Run integration tests
   python -m pytest tests/integration/
   ```

3. **Documentation Update**:
   ```bash
   # Update API documentation
   # Update README files
   # Generate release notes
   ```

### **Release Types**

#### **Major Release (v2.0.0)**
- Breaking changes
- New major features
- Architecture changes

#### **Minor Release (v2.1.0)**
- New features
- Backward compatible
- API additions

#### **Patch Release (v2.0.1)**
- Bug fixes
- Security patches
- Documentation updates

### **Release Checklist**

- [ ] **Version bumped** in all relevant files
- [ ] **CHANGELOG.md** updated
- [ ] **All tests pass** (unit, integration, V2 compliance)
- [ ] **Documentation updated**
- [ ] **Release notes prepared**
- [ ] **Git tag created**
- [ ] **Release published**

## 📞 **Getting Help**

### **Communication Channels**

- **GitHub Issues**: Bug reports and feature requests
- **Discussions**: General questions and ideas
- **Discord**: Real-time chat and coordination
- **Agent Messaging**: Direct agent-to-agent communication

### **Support Resources**

- **Documentation**: Check `docs/` directory
- **API Reference**: See `API.md`
- **Examples**: Check `examples/` directory
- **Agent System**: Use agent messaging system

### **Reporting Issues**

#### **Bug Reports**
```markdown
**Bug Description**
Clear description of the bug

**Steps to Reproduce**
1. Step one
2. Step two
3. Step three

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: Windows 10
- Python: 3.9.7
- Version: 2.0.0

**Additional Context**
Any other relevant information
```

#### **Feature Requests**
```markdown
**Feature Description**
Clear description of the requested feature

**Use Case**
Why is this feature needed?

**Proposed Solution**
How should this feature work?

**Alternatives Considered**
What other solutions were considered?

**Additional Context**
Any other relevant information
```

## 🎯 **Contributor Recognition**

### **Contributor Levels**

- **🌱 First-time Contributor**: First contribution
- **🥉 Bronze Contributor**: 3+ contributions
- **🥈 Silver Contributor**: 10+ contributions
- **🥇 Gold Contributor**: 25+ contributions
- **💎 Diamond Contributor**: 50+ contributions

### **Recognition Methods**

- **GitHub Contributors**: Listed in README
- **Release Notes**: Contributors acknowledged
- **Discord Recognition**: Special roles and mentions
- **Agent System**: Elevated agent status

## 📋 **Quick Reference**

### **Common Commands**
```bash
# Setup development environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run tests
python -m pytest

# Format code
black src/ tests/
isort src/ tests/

# Check V2 compliance
python quality_gates.py

# Send agent message
python messaging_system.py Agent-7 Agent-4 "Message" NORMAL

# Post devlog
python src/services/agent_devlog_posting.py --agent Agent-7 --action "Description"
```

### **Important Files**
- **pyproject.toml**: Project configuration
- **requirements.txt**: Python dependencies
- **.env.example**: Environment template
- **quality_gates.py**: V2 compliance checker
- **messaging_system.py**: Agent communication

---

**Status**: Contributing Guide Complete  
**Agent**: Agent-7 (Elevated Web Development Expert)  
**Version**: 2.0.0  
**Last Updated**: 2025-10-05  
**Next**: ARCHITECTURE.md Implementation
