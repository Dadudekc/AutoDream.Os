# 🎯 AutoDream.OS Coherent Collaboration System

## Overview

The Coherent Collaboration System transforms AutoDream.OS from a swarm of talented individuals into a **well-organized development organization**. This system solves the core challenge of maintaining consistent design sensibility across multiple agents.

## 🏗️ System Architecture

### 1. **Single Source of Truth Registry** (`project_registry.py`)
- **Purpose**: Centralized project manifest and component ownership
- **Prevents**: Duplication by checking existing components before creation
- **Enforces**: Design patterns and component relationships

### 2. **Design Authority Agent** (`design_authority.py`)
- **Purpose**: Enforces simplicity and prevents overcomplication
- **Reviews**: Component plans and code complexity
- **Applies**: KISS, YAGNI, and Single Responsibility principles

### 3. **Vibe Check CI/CD Gate** (`vibe_check.py`)
- **Purpose**: Automated validation of design principles
- **Checks**: Complexity, duplication, anti-patterns, file limits
- **Enforces**: V2 compliance standards (300 LOC files, 30 LOC functions, etc.)

### 4. **Agent-to-Agent PR Review Protocol** (`pr_review_protocol.py`)
- **Purpose**: Peer review system for agent collaboration
- **Process**: No direct commits to main, all changes reviewed
- **Ensures**: Quality gates and duplication prevention

### 5. **Shared Knowledge Base** (`knowledge_base.py`)
- **Purpose**: Centralized design principles and best practices
- **Contains**: Required patterns, anti-patterns, project guidelines
- **Guides**: Consistent decision-making across all agents

## 🚀 Quick Start

### Installation
```bash
# Install pre-commit hooks
pre-commit install

# Verify installation
python -m src.core.coherent_collaboration_cli --help
```

### Basic Workflow

#### 1. Check Before Creating Components
```bash
# Check if component already exists
python -m src.core.coherent_collaboration_cli registry check-component ollama_client

# If not found, register new component
python -m src.core.coherent_collaboration_cli registry register-component \
  --name ollama_client \
  --path src/ollama_client.py \
  --purpose "Handles Ollama API communication" \
  --owner Agent-7
```

#### 2. Get Design Authority Approval
```bash
# Review component plan
python -m src.core.coherent_collaboration_cli design review-plan \
  Agent-7 ollama_client "Create simple HTTP client with error handling"

# Review code complexity
python -m src.core.coherent_collaboration_cli design review-code \
  Agent-7 ollama_client --file src/ollama_client.py
```

#### 3. Run Vibe Check
```bash
# Check single file
python -m src.core.coherent_collaboration_cli vibe check-file src/ollama_client.py --agent Agent-7

# Check entire directory
python -m src.core.coherent_collaboration_cli vibe check-directory src/ --agent Agent-7

# Strict check (fails on warnings)
python -m src.core.coherent_collaboration_cli vibe check-strict src/ollama_client.py --agent Agent-7
```

#### 4. Create Pull Request
```bash
# Create PR for review
python -m src.core.coherent_collaboration_cli pr create \
  --author Agent-7 \
  --title "Add Ollama HTTP client" \
  --description "Simple HTTP client for Ollama API with error handling" \
  --files src/ollama_client.py
```

#### 5. Review Pull Request
```bash
# Get pending reviews
python -m src.core.coherent_collaboration_cli pr pending --reviewer Agent-5

# Review specific PR
python -m src.core.coherent_collaboration_cli pr review PR_Agent-7_20241201_143022 --reviewer Agent-5
```

## 📋 Design Principles

### Required Principles
1. **KISS (Keep It Simple, Stupid)**
   - Prefer simple solutions over complex ones
   - Use built-in types when possible
   - Avoid premature abstractions

2. **YAGNI (You Aren't Gonna Need It)**
   - Build only what you need right now
   - Avoid speculative features
   - Start simple, add complexity when required

3. **Single Responsibility**
   - Each component has one clear purpose
   - Separate concerns clearly
   - Avoid god classes or functions

4. **Consistent Error Handling**
   - Use specific exception types
   - Provide meaningful error messages
   - Log errors with sufficient context

### Code Quality Limits
- **Files**: Maximum 300 lines
- **Classes**: Maximum 100 lines  
- **Functions**: Maximum 30 lines
- **Nesting Depth**: Maximum 3 levels
- **Function Parameters**: Maximum 5 parameters

## 🎯 Agent Workflow

### Before Starting Any Task
1. **Check Registry**: Verify component doesn't already exist
2. **Plan Review**: Get Design Authority approval for approach
3. **Follow Principles**: Apply KISS, YAGNI, Single Responsibility

### During Development
1. **Frequent Vibe Checks**: Run vibe check during development
2. **Registry Updates**: Update component information as needed
3. **Documentation**: Keep registry and code documentation current

### Before Committing
1. **Pre-commit Hooks**: Automatic vibe check runs
2. **Create PR**: Never commit directly to main
3. **Peer Review**: Another agent must review changes

### Review Process
1. **Check Duplication**: Verify no existing similar components
2. **Run Vibe Check**: Ensure code meets quality standards
3. **Design Compliance**: Verify adherence to design principles
4. **Approve/Reject**: Provide feedback and approval decision

## 🛠️ CLI Commands Reference

### Registry Commands
```bash
# Check component existence
registry check-component <name>

# Register new component
registry register-component <name> <path> <purpose> <owner> [--dependencies ...]

# List all components
registry list-components [--owner <agent>]

# Get registry summary
registry summary
```

### Design Authority Commands
```bash
# Review component plan
design review-plan <requester> <component_name> <plan> [--context <context>]

# Review code complexity
design review-code <requester> <component_name> [--file <path>|--code <snippet>]

# Get knowledge summary
design knowledge
```

### Vibe Check Commands
```bash
# Check single file
vibe check-file <file_path> [--agent <agent>] [--strict]

# Check directory
vibe check-directory <directory> [--agent <agent>] [--strict] [--patterns ...]

# Strict check (fails on warnings)
vibe check-strict <file_paths...> [--agent <agent>]
```

### PR Review Commands
```bash
# Create pull request
pr create --author <agent> --title <title> --description <desc> [--files ...] [--priority <level>]

# Review pull request
pr review <pr_id> --reviewer <agent>

# Get pending reviews
pr pending --reviewer <agent>

# List PRs
pr list [--author <agent>] [--status <status>]
```

### Knowledge Base Commands
```bash
# List design principles
knowledge principles

# List code patterns
knowledge patterns

# List anti-patterns
knowledge anti-patterns

# Show project guidelines
knowledge guidelines
```

## 🔧 Integration with Existing Tools

### Pre-commit Hooks
The system integrates with pre-commit to automatically run vibe checks:
```yaml
# .pre-commit-config.yaml includes custom vibe check
- id: vibe-check
  entry: python -m src.core.vibe_check
  args: [--strict]
```

### IDE Integration
Add to your IDE configuration:
```json
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "python.sortImports.args": ["--profile", "black"]
}
```

### CI/CD Integration
Add to your CI pipeline:
```yaml
- name: Run Vibe Check
  run: python -m src.core.vibe_check --strict src/

- name: Check Registry Consistency
  run: python -m src.core.coherent_collaboration_cli registry summary
```

## 📊 Monitoring and Metrics

### Registry Metrics
- Total components by agent
- Component status breakdown
- Last update timestamps

### Review Metrics
- Approval rates by agent
- Common violation types
- Average review times

### Vibe Check Metrics
- Violation frequency by type
- Files with most issues
- Improvement trends over time

## 🚨 Troubleshooting

### Common Issues

**"Component already exists"**
- Check registry: `registry list-components`
- Consider reusing existing component
- Transfer ownership if appropriate

**"Vibe check failed"**
- Run locally: `vibe check-file <file>`
- Fix violations before committing
- Use `--strict` for detailed feedback

**"Design Authority rejected"**
- Review feedback carefully
- Consider simpler alternatives
- Apply suggested patterns

**"No reviewer assigned"**
- Check agent availability
- Assign specific reviewer manually
- Review agent workload distribution

### Getting Help
```bash
# Get help for any command
python -m src.core.coherent_collaboration_cli <command> --help

# Check system status
python -m src.core.coherent_collaboration_cli registry summary
python -m src.core.coherent_collaboration_cli design knowledge
```

## 🎉 Success Metrics

### Before (Swarm Mode)
- ❌ Duplicate components created
- ❌ Overcomplicated solutions
- ❌ Inconsistent design patterns
- ❌ No peer review process

### After (Coherent Collaboration)
- ✅ Zero duplication through registry
- ✅ Simple solutions via Design Authority
- ✅ Consistent patterns via Knowledge Base
- ✅ Quality assured via PR reviews
- ✅ Automated enforcement via Vibe Check

---

## 🚀 Next Steps

1. **Train Agents**: Ensure all agents understand the new workflow
2. **Migrate Existing Code**: Register existing components in registry
3. **Establish Review Culture**: Make PR reviews standard practice
4. **Monitor Metrics**: Track improvement in code quality
5. **Iterate and Improve**: Refine based on usage patterns

This system transforms AutoDream.OS from a promising multi-agent system into a **truly reliable, production-grade development organization** with consistent design sensibility and quality standards.