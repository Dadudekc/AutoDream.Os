# Agent Workflow Automation Tool

**Author:** Agent-2 (Architecture & Design Specialist)  
**Version:** 1.0  
**Status:** ✅ OPERATIONAL  

## 🎯 Overview

The Agent Workflow Automation Tool is a comprehensive system designed to streamline common agent tasks, reduce manual work, and ensure consistency across the swarm. It automates workflows like module fixes, testing, messaging, and project management.

## 🚀 Features

### Core Capabilities
- **Import Fixing**: Automatically create missing `__init__.py` files
- **Testing Automation**: Run test suites and generate reports
- **Messaging Integration**: Send status updates and notifications
- **Devlog Creation**: Automatically generate documentation
- **V2 Compliance**: Check and enforce V2 compliance rules
- **Project Management**: Create project structures and components

### Workflow Types
1. **Fix Imports**: Resolve missing module imports
2. **Test and Report**: Run tests and send status updates
3. **Create Component**: Generate new components with full structure
4. **Deploy Feature**: Complete feature deployment workflow

## 🛠️ Installation

The tool is already integrated into the project. No additional installation required.

## 📖 Usage

### Quick CLI Commands

```bash
# Fix missing imports
python tools/agent_workflow_cli.py fix-imports src.core

# Run tests and send report
python tools/agent_workflow_cli.py test-and-report

# Create a React component
python tools/agent_workflow_cli.py create-component MyButton react

# Create a Python component
python tools/agent_workflow_cli.py create-component DataProcessor python

# Deploy a feature
python tools/agent_workflow_cli.py deploy-feature user-auth
```

### Advanced Usage

```bash
# Full automation tool
python tools/agent_workflow_automation.py fix-imports --module-path src.core
python tools/agent_workflow_automation.py test-imports --module-path src.core
python tools/agent_workflow_automation.py run-tests --test-path tests/
python tools/agent_workflow_automation.py send-message --agent Agent-4 --message "Status update"
python tools/agent_workflow_automation.py check-compliance --file src/core/coordinate_loader.py
python tools/agent_workflow_automation.py run-workflow --name fix_imports --params '{"module_path": "src.core"}'
```

## 🔧 Workflow Examples

### 1. Fix Missing Imports Workflow

**Problem**: Module import errors like `ModuleNotFoundError: No module named 'src.core.coordinate_loader'`

**Solution**:
```bash
python tools/agent_workflow_cli.py fix-imports src.core
```

**What it does**:
1. Creates missing `__init__.py` files
2. Tests the imports
3. Sends status update to Agent-4
4. Logs the fix

### 2. Test and Report Workflow

**Problem**: Need to run tests and report results

**Solution**:
```bash
python tools/agent_workflow_cli.py test-and-report
```

**What it does**:
1. Runs the test suite
2. Generates test report
3. Sends status update with results
4. Logs test outcomes

### 3. Create Component Workflow

**Problem**: Need to create a new component with proper structure

**Solution**:
```bash
# React component
python tools/agent_workflow_cli.py create-component MyButton react

# Python component
python tools/agent_workflow_cli.py create-component DataProcessor python
```

**What it does**:
1. Creates component directory structure
2. Generates main component file
3. Creates styling file (React) or test file (Python)
4. Creates test file
5. Generates devlog
6. Sends status update

### 4. Deploy Feature Workflow

**Problem**: Need to deploy a feature with proper testing

**Solution**:
```bash
python tools/agent_workflow_cli.py deploy-feature user-auth
```

**What it does**:
1. Runs test suite
2. Updates working tasks
3. Sends deployment notification
4. Logs deployment status

## 📊 API Reference

### AgentWorkflowAutomation Class

#### Methods

##### `fix_missing_imports(module_path: str) -> bool`
Fixes missing imports by creating necessary `__init__.py` files.

**Parameters**:
- `module_path`: Path to the module to fix

**Returns**: `True` if successful, `False` otherwise

##### `test_imports(module_path: str) -> bool`
Tests if a module can be imported successfully.

**Parameters**:
- `module_path`: Path to the module to test

**Returns**: `True` if import successful, `False` otherwise

##### `run_tests(test_path: str = "tests/") -> Dict[str, Any]`
Runs test suite and returns results.

**Parameters**:
- `test_path`: Path to test directory

**Returns**: Dictionary with test results

##### `send_status_update(agent_id: str, status: str, details: str = "") -> bool`
Sends status update to another agent.

**Parameters**:
- `agent_id`: Target agent ID
- `status`: Status message
- `details`: Additional details

**Returns**: `True` if sent successfully, `False` otherwise

##### `create_devlog(title: str, content: str, agent_id: str = "Agent-2") -> str`
Creates a devlog file.

**Parameters**:
- `title`: Devlog title
- `content`: Devlog content
- `agent_id`: Agent ID for filename

**Returns**: Path to created devlog file

##### `check_v2_compliance(file_path: str) -> Dict[str, Any]`
Checks V2 compliance for a file.

**Parameters**:
- `file_path`: Path to file to check

**Returns**: Dictionary with compliance information

## 🎯 Use Cases

### Common Agent Tasks

1. **Module Import Issues**
   - Automatically fix missing `__init__.py` files
   - Test imports after fixing
   - Send status updates

2. **Testing Workflows**
   - Run test suites
   - Generate reports
   - Send notifications

3. **Component Creation**
   - Generate new components
   - Create proper structure
   - Add tests and documentation

4. **Feature Deployment**
   - Run tests before deployment
   - Update task status
   - Send deployment notifications

5. **V2 Compliance Checking**
   - Check file line counts
   - Verify class/function limits
   - Ensure compliance

### Integration with Swarm

The tool integrates seamlessly with the swarm messaging system:
- Sends status updates to other agents
- Creates devlogs automatically
- Updates working tasks
- Maintains project documentation

## 🔄 Workflow Automation

### Predefined Workflows

1. **fix_imports**: Fix missing imports and test
2. **test_and_report**: Run tests and send report
3. **create_component**: Create new component with structure
4. **deploy_feature**: Deploy feature with testing

### Custom Workflows

You can create custom workflows by extending the `AgentWorkflowAutomation` class:

```python
def custom_workflow(self, params: Dict[str, Any]) -> Dict[str, Any]:
    """Custom workflow implementation."""
    # Your workflow logic here
    return {"success": True, "message": "Custom workflow completed"}
```

## 📝 Best Practices

### 1. Always Test After Fixes
```bash
python tools/agent_workflow_cli.py fix-imports src.core
# Automatically tests the fix
```

### 2. Use Status Updates
The tool automatically sends status updates, but you can customize them:
```python
automation.send_status_update(
    "Agent-4",
    "Custom status message",
    "Additional details"
)
```

### 3. Create Devlogs
The tool automatically creates devlogs, but you can create custom ones:
```python
automation.create_devlog(
    "Custom Title",
    "Custom content with details"
)
```

### 4. Check V2 Compliance
Always check compliance before submitting:
```bash
python tools/agent_workflow_automation.py check-compliance --file src/core/coordinate_loader.py
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Still Failing**
   - Check if all parent directories have `__init__.py`
   - Verify the module path is correct
   - Run `test-imports` to verify

2. **Tests Not Running**
   - Check if pytest is installed
   - Verify test directory exists
   - Check test file syntax

3. **Messaging Not Working**
   - Verify messaging service is running
   - Check agent coordinates
   - Ensure target agent exists

4. **V2 Compliance Issues**
   - Check file line count
   - Reduce class/function counts
   - Split large files

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🚀 Future Enhancements

### Planned Features
1. **Git Integration**: Automatic commit and push
2. **Docker Support**: Container-based workflows
3. **CI/CD Integration**: Automated deployment pipelines
4. **Monitoring**: Workflow performance tracking
5. **Templates**: Custom component templates

### Extension Points
1. **Custom Workflows**: Add your own workflows
2. **Plugin System**: Extend functionality
3. **API Integration**: Connect with external services
4. **Database Support**: Persistent workflow state

## 📊 Performance

### Metrics
- **Import Fix Time**: < 1 second
- **Test Execution**: Depends on test suite size
- **Component Creation**: < 2 seconds
- **Status Updates**: < 1 second

### Optimization
- Lazy loading of modules
- Cached coordinate loading
- Efficient file operations
- Minimal memory usage

## 🔒 Security

### Safety Features
- File path validation
- Permission checks
- Backup creation
- Rollback capabilities

### Best Practices
- Always backup before making changes
- Test in development environment first
- Use version control
- Monitor file changes

## 📚 Examples

### Complete Workflow Example

```bash
# 1. Fix imports
python tools/agent_workflow_cli.py fix-imports src.core

# 2. Run tests
python tools/agent_workflow_cli.py test-and-report

# 3. Create component
python tools/agent_workflow_cli.py create-component MyComponent react

# 4. Deploy feature
python tools/agent_workflow_cli.py deploy-feature my-feature
```

### Python Integration Example

```python
from tools.agent_workflow_automation import AgentWorkflowAutomation

# Initialize
automation = AgentWorkflowAutomation()

# Fix imports
automation.fix_missing_imports("src.core")

# Run tests
results = automation.run_tests()

# Send status
automation.send_status_update("Agent-4", "Workflow completed")

# Create devlog
automation.create_devlog("Workflow Complete", "All tasks completed successfully")
```

## 🏆 Benefits

### For Agents
- **Reduced Manual Work**: Automate repetitive tasks
- **Consistency**: Standardized workflows
- **Speed**: Faster task completion
- **Quality**: Built-in testing and validation

### For the Swarm
- **Coordination**: Better agent communication
- **Documentation**: Automatic devlog creation
- **Tracking**: Task status updates
- **Quality**: V2 compliance checking

### For the Project
- **Reliability**: Consistent processes
- **Maintainability**: Better code organization
- **Scalability**: Reusable workflows
- **Documentation**: Comprehensive logging

---

**Agent Workflow Automation Tool** - Making agent workflows easier, faster, and more reliable! 🚀

📝 **DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory**


