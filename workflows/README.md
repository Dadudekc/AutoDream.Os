# Agent Workflow Manager

## 🎯 **AUTOMATED WORKFLOW COORDINATION SYSTEM**

The Agent Workflow Manager automates complex multi-agent workflows with:
- **Dependency Management** - Automatic step sequencing based on dependencies
- **Timeout Handling** - Automatic timeout detection and error handling
- **Status Tracking** - Real-time workflow progress monitoring
- **Agent Coordination** - Automated task distribution to agents
- **Error Recovery** - Failed step handling and retry mechanisms

## 🚀 **QUICK START**

### **1. Create a Workflow**
```bash
# Create sample workflow
python tools/agent_workflow_manager.py create-sample --output workflows/my_workflow.json

# Or create custom workflow JSON file
```

### **2. Run a Workflow**
```bash
# Run workflow with default settings
python tools/agent_workflow_manager.py --workflow workflows/my_workflow.json run

# Run with custom concurrency
python tools/agent_workflow_manager.py --workflow workflows/my_workflow.json run --max-concurrent 3
```

### **3. Monitor Workflow**
```bash
# Check workflow status
python tools/agent_workflow_manager.py --workflow workflows/my_workflow.json status

# Mark step as completed
python tools/agent_workflow_manager.py --workflow workflows/my_workflow.json complete --step-id step_1 --result "Task completed successfully"

# Mark step as failed
python tools/agent_workflow_manager.py --workflow workflows/my_workflow.json fail --step-id step_1 --error "Task failed due to timeout"
```

## 📋 **WORKFLOW CONFIGURATION**

### **Workflow JSON Structure**
```json
{
  "name": "Workflow Name",
  "description": "Workflow description",
  "created_at": "2025-01-15T20:00:00Z",
  "steps": [
    {
      "step_id": "unique_step_identifier",
      "agent_id": "Agent-1",
      "task": "Task description for agent",
      "dependencies": ["step_id_1", "step_id_2"],
      "timeout_minutes": 30
    }
  ]
}
```

### **Step Configuration**
- **step_id**: Unique identifier for the step
- **agent_id**: Target agent (Agent-1 through Agent-8)
- **task**: Task description sent to agent
- **dependencies**: List of step IDs that must complete first
- **timeout_minutes**: Maximum time allowed for step completion

## 🔧 **FEATURES**

### **Automated Coordination**
- **Dependency Resolution** - Steps execute only when dependencies are satisfied
- **Concurrent Execution** - Multiple steps can run simultaneously (configurable)
- **Timeout Management** - Automatic timeout detection and handling
- **Error Recovery** - Failed step handling and workflow continuation

### **Real-time Monitoring**
- **Status Tracking** - Real-time step status updates
- **Progress Reporting** - Workflow completion percentage
- **Agent Communication** - Direct task assignment to agents
- **Logging** - Comprehensive workflow execution logs

### **Integration**
- **Messaging System** - Uses consolidated messaging service
- **Coordinate System** - Agent position tracking
- **PyAutoGUI** - UI automation for agent interaction
- **JSON Configuration** - Easy workflow definition and modification

## 📊 **WORKFLOW EXAMPLES**

### **Tesla Stock Forecast App Development**
```bash
# Create the workflow
python tools/agent_workflow_manager.py create-sample --output workflows/tesla_workflow.json

# Run the workflow
python tools/agent_workflow_manager.py --workflow workflows/tesla_workflow.json run

# Monitor progress
python tools/agent_workflow_manager.py --workflow workflows/tesla_workflow.json status
```

### **Custom Workflow Example**
```json
{
  "name": "Custom Development Workflow",
  "description": "Example custom workflow",
  "created_at": "2025-01-15T20:00:00Z",
  "steps": [
    {
      "step_id": "setup",
      "agent_id": "Agent-4",
      "task": "Set up project infrastructure",
      "dependencies": [],
      "timeout_minutes": 15
    },
    {
      "step_id": "backend",
      "agent_id": "Agent-1",
      "task": "Develop backend API",
      "dependencies": ["setup"],
      "timeout_minutes": 45
    },
    {
      "step_id": "frontend",
      "agent_id": "Agent-2",
      "task": "Create frontend interface",
      "dependencies": ["backend"],
      "timeout_minutes": 60
    },
    {
      "step_id": "testing",
      "agent_id": "Agent-4",
      "task": "Perform integration testing",
      "dependencies": ["backend", "frontend"],
      "timeout_minutes": 30
    }
  ]
}
```

## 🐝 **SWARM COORDINATION**

The workflow manager integrates with the swarm coordination system:
- **Agent Registry** - All 8 agents available for task assignment
- **Real-time Communication** - Direct agent-to-agent messaging
- **Coordinate Tracking** - Agent position monitoring
- **Status Synchronization** - Workflow status across all agents

**WE. ARE. SWARM. - AUTOMATED WORKFLOW COORDINATION!**






