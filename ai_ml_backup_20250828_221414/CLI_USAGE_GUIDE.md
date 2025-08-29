# AI/ML CLI Usage Guide for Agents 🚀

## Overview

This guide provides comprehensive instructions for agents to use the new AI/ML CLI system, which integrates all modularized AI/ML functionality with the agent contract system.

## Quick Start

### 1. Basic Usage

```bash
# Show help
python -m src.ai_ml.cli --help

# Use simplified agent CLI
python -m src.ai_ml.agent_cli --help
```

### 2. Check System Status

```bash
# Quick system overview
python -m src.ai_ml.agent_cli system-status

# Detailed system status
python -m src.ai_ml.cli system --status

# Health check
python -m src.ai_ml.agent_cli health-check
```

## Contract Management 📋

### View Available Contracts

```bash
# List all available contracts
python -m src.ai_ml.cli contracts --list

# List contracts by category
python -m src.ai_ml.cli contracts --list --category emergency_system_restoration

# Quick contract view
python -m src.ai_ml.agent_cli contracts
```

### Claim Contracts

```bash
# Claim a specific contract
python -m src.ai_ml.cli contracts --claim --contract-id CONTRACT-001 --agent-id Agent-7

# Check contract status
python -m src.ai_ml.cli contracts --status --contract-id CONTRACT-001
```

## AI Management 🤖

### AI Models

```bash
# List all AI models
python -m src.ai_ml.cli ai --models --list

# Register a new AI model
python -m src.ai_ml.cli ai --models --register \
    --model-id "gpt-4-model" \
    --name "GPT-4 Integration" \
    --provider "OpenAI" \
    --model-type "language-model" \
    --version "1.0.0"

# Quick AI status
python -m src.ai_ml.agent_cli ai-status
```

### AI Workflows

```bash
# List AI workflows
python -m src.ai_ml.cli ai --workflows --list

# Create a new workflow
python -m src.ai_ml.cli ai --workflows --create \
    --name "Data Processing Pipeline" \
    --description "Automated data processing workflow"

# Execute a workflow
python -m src.ai_ml.cli ai --execute --workflow-name "Data Processing Pipeline"

# Quick workflow creation
python -m src.ai_ml.agent_cli workflow-create "My Workflow" --description "Description"
```

## ML Operations 🔧

### ML Frameworks

```bash
# List ML frameworks
python -m src.ai_ml.cli ml --frameworks --list

# Quick ML status
python -m src.ai_ml.agent_cli ml-status
```

### ML Models

```bash
# List ML models
python -m src.ai_ml.cli ml --models --list

# Search for models
python -m src.ai_ml.cli ml --models --search --query "bert"

# Get model information
python -m src.ai_ml.cli models --info --model-id "bert-model"

# Validate a model
python -m src.ai_ml.cli models --validate --model-id "bert-model"
```

## Workflow Automation ⚡

### Automation Rules

```bash
# List automation rules
python -m src.ai_ml.cli workflows --rules --list

# Add automation rule
python -m src.ai_ml.cli workflows --rules --add --rule-name "auto-workflow"

# Process automation rules
python -m src.ai_ml.cli automation --process

# Get automation statistics
python -m src.ai_ml.cli automation --stats
```

### Scheduled Tasks

```bash
# List scheduled tasks
python -m src.ai_ml.cli workflows --tasks --list
```

## Advanced Usage

### Complete AI/ML System Creation

```python
# Python script example
from src.ai_ml import create_ai_ml_system

# Create complete system
ai_manager, model_manager, workflow_automation = create_ai_ml_system()

# Use the system
ai_manager.register_model(...)
model_manager.register_framework(...)
workflow_automation.add_automation_rule(...)
```

### Integration with Contract System

```python
# Python script example
from src.ai_ml.cli import AIMLCLI

# Initialize CLI with contract integration
cli = AIMLCLI()

# Check available contracts
contracts = cli.contract_system.list_available_contracts()

# Claim a contract
result = cli.contract_system.claim_contract("CONTRACT-001", "Agent-7")

# Complete contract work using AI/ML capabilities
# ... perform AI/ML operations ...

# Update contract progress
cli.contract_system.update_contract_progress("CONTRACT-001", "Agent-7", "50% Complete")
```

## Common Workflows for Agents

### 1. Contract Discovery and Claiming

```bash
# 1. Check system status
python -m src.ai_ml.agent_cli system-status

# 2. View available contracts
python -m src.ai_ml.agent_cli contracts

# 3. Claim a contract
python -m src.ai_ml.cli contracts --claim --contract-id CONTRACT-001 --agent-id Agent-7
```

### 2. AI/ML Task Execution

```bash
# 1. Check AI/ML capabilities
python -m src.ai_ml.agent_cli ai-status
python -m src.ai_ml.agent_cli ml-status

# 2. Create workflow for the task
python -m src.ai_ml.agent_cli workflow-create "Contract Task" --description "Task description"

# 3. Execute the workflow
python -m src.ai_ml.cli ai --execute --workflow-name "Contract Task"
```

### 3. System Monitoring and Health

```bash
# 1. Regular health check
python -m src.ai_ml.agent_cli health-check

# 2. Monitor system status
python -m src.ai_ml.agent_cli system-status

# 3. Check automation status
python -m src.ai_ml.cli automation --stats
```

## Error Handling and Troubleshooting

### Common Issues

1. **Contract System Not Available**
   ```bash
   # Check if task_list.json exists
   ls agent_workspaces/meeting/task_list.json
   
   # Verify contract system path
   python -m src.ai_ml.cli system --status
   ```

2. **AI/ML System Initialization Errors**
   ```bash
   # Run health check
   python -m src.ai_ml.agent_cli health-check
   
   # Check system status
   python -m src.ai_ml.cli system --status
   ```

3. **Import Errors**
   ```bash
   # Ensure you're in the correct directory
   cd /path/to/Agent_Cellphone_V2_Repository
   
   # Check Python path
   python -c "import sys; print(sys.path)"
   ```

### Debug Mode

```bash
# Enable verbose output
python -m src.ai_ml.cli --verbose system --status

# Check specific component
python -m src.ai_ml.cli system --health
```

## Best Practices

### 1. Regular System Checks
- Run `health-check` before starting complex tasks
- Monitor `system-status` regularly
- Check for available contracts frequently

### 2. Workflow Management
- Create descriptive workflow names
- Use automation rules for repetitive tasks
- Monitor workflow execution status

### 3. Contract Integration
- Always check contract status before starting work
- Update progress regularly
- Complete contracts with proper deliverables

### 4. Resource Management
- Monitor model and framework usage
- Clean up unused resources
- Use automation for resource optimization

## Examples by Use Case

### Emergency Restoration Contracts

```bash
# 1. Check emergency contracts
python -m src.ai_ml.cli contracts --list --category emergency_system_restoration

# 2. Claim emergency contract
python -m src.ai_ml.cli contracts --claim --contract-id EMERGENCY-RESTORE-008 --agent-id Agent-7

# 3. Use AI/ML for restoration
python -m src.ai_ml.agent_cli workflow-create "Emergency Restoration" --description "System restoration workflow"

# 4. Execute restoration
python -m src.ai_ml.cli ai --execute --workflow-name "Emergency Restoration"
```

### AI/ML Development Contracts

```bash
# 1. Check development contracts
python -m src.ai_ml.cli contracts --list --category ai_ml_development

# 2. Set up development environment
python -m src.ai_ml.agent_cli system-status

# 3. Create development workflow
python -m src.ai_ml.agent_cli workflow-create "AI Development" --description "AI/ML development pipeline"

# 4. Monitor development progress
python -m src.ai_ml.cli automation --stats
```

### Performance Optimization Contracts

```bash
# 1. Check performance contracts
python -m src.ai_ml.cli contracts --list --category performance_optimization

# 2. Analyze current performance
python -m src.ai_ml.agent_cli health-check

# 3. Create optimization workflow
python -m src.ai_ml.agent_cli workflow-create "Performance Optimization" --description "System optimization workflow"

# 4. Execute optimization
python -m src.ai_ml.cli ai --execute --workflow-name "Performance Optimization"
```

## Integration with Existing Systems

### Contract System Integration
- Seamless contract claiming and management
- Progress tracking and updates
- Deliverable submission

### AI/ML System Integration
- Model registration and management
- Workflow creation and execution
- Framework integration
- Automation rule processing

### Monitoring and Reporting
- System health monitoring
- Performance metrics
- Error tracking and reporting
- Resource utilization

## Conclusion

The new AI/ML CLI system provides agents with comprehensive access to all modularized AI/ML functionality while maintaining seamless integration with the contract system. This enables agents to:

- Efficiently manage contracts and track progress
- Access advanced AI/ML capabilities through simple commands
- Automate workflows and optimize performance
- Monitor system health and status
- Integrate AI/ML operations with contract completion

Use the simplified `agent_cli.py` for quick operations and the full `cli.py` for advanced functionality. Regular system monitoring and health checks will ensure optimal performance and contract completion success.
