# Cursor Rules - Agent Cellphone V2

This directory contains Cursor IDE rules that enforce V2 compliance standards and Swarm protocol requirements across the Agent Cellphone V2 project.

## 📋 Available Rules

### **Core Rules** (Always Applied)
- **`architecture.mdc`** - Core V2 architecture conventions
- **`code-style.mdc`** - Consistent code style standards
- **`workflow.mdc`** - Git workflow and collaboration standards
- **`messaging.mdc`** - Messaging system standards and protocols
- **`swarm-protocol.mdc`** - Agent Swarm communication protocols
- **`v2-compliance.mdc`** - V2 compliance guardrails and standards

### **Scoped Rules** (Context-Specific)
- **`messaging/pyautogui-operations.mdc`** - PyAutoGUI delivery operations
- **`messaging/cli-flags.mdc`** - CLI flag validation and combinations
- **`agent-workspaces.mdc`** - Agent workspace management

### **Conditional Rules** (Applied When Relevant)
- **`testing.mdc`** - Testing standards and requirements
- **`documentation.mdc`** - Documentation standards

## 🎯 Rule Structure

Each rule file uses MDC (Markdown with frontmatter) format:

```mdc
---
description: Brief description of the rule
globs: ["**/pattern1", "**/pattern2"]  # File patterns to apply to
alwaysApply: true|false               # Whether to always apply this rule
---

# Rule content in Markdown format
- Rule 1
- Rule 2
- Examples and explanations
```

## 🚀 Key Standards Enforced

### **V2 Compliance**
- Repository pattern for data access
- Dependency injection for utilities
- Object-oriented code for complex logic
- Function size limits and complexity constraints

### **Code Quality**
- TypeScript for new files
- snake_case for API fields
- Functional React components
- JSDoc documentation requirements

### **Testing Standards**
- Unit tests for all features
- Jest for JavaScript/TypeScript
- 85% minimum coverage
- Mock external dependencies

### **Swarm Protocol**
- Agent hierarchy and roles
- Communication cycle standards
- Status tracking requirements
- Emergency protocols

### **Messaging System**
- Message type and priority standards
- Delivery mode specifications
- Agent processing order (Agent-4 last)
- CLI flag validation rules

## ⚙️ How Cursor Uses These Rules

1. **Context Awareness**: Cursor reads the `globs` patterns to determine which rules apply to each file
2. **Always Applied**: Rules with `alwaysApply: true` are enforced regardless of file type
3. **Conditional Application**: Rules with `alwaysApply: false` are applied based on context
4. **Scoped Rules**: Subdirectories allow for more specific rule application

## 🔧 Customization

### **Adding New Rules**
1. Create new `.mdc` file in appropriate location
2. Use frontmatter to define scope and behavior
3. Write clear, actionable rules in Markdown
4. Test rule application in relevant files

### **Modifying Existing Rules**
1. Edit the `.mdc` file directly
2. Update frontmatter if scope changes
3. Ensure backward compatibility
4. Test changes across affected files

## 📚 Related Documentation

- **`AGENTS.md`** - Complete project guidelines
- **`ONBOARDING_GUIDE.md`** - Agent onboarding process
- **`docs/onboarding/README.md`** - Onboarding documentation
- **Project README** - General project information

## 🎖️ Compliance Benefits

These rules ensure:
- **Consistency** across all codebase contributions
- **Quality** through enforced standards
- **Efficiency** through established patterns
- **Reliability** through testing requirements
- **Maintainability** through documentation standards

## 🚨 Important Notes

- **Agent-4 Last**: All messaging operations must process Agent-4 (Captain) LAST
- **V2 Standards**: Follow existing architecture before proposing changes
- **SSOT Principle**: Maintain single source of truth across configurations
- **8x Efficiency**: One communication cycle = measurable progress
