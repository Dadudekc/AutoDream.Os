# Task Message Formats - Quick Reference

**Quick guide for creating tasks via messages**

---

## 📋 **Format 1: Structured (Recommended)**

### Basic Task

```
TASK: Your task title here
DESC: Detailed description of what needs to be done
PRIORITY: P2
```

### With Assignment

```
TASK: Refactor authentication system
DESC: Split into smaller modules, add tests
PRIORITY: P1
ASSIGNEE: Agent-3
```

### With Tags

```
TASK: Update documentation  
DESC: Add examples for new API endpoints
PRIORITY: P3
TAGS: docs, api, examples
```

### Complete Format

```
TASK: Implement feature X
DESC: Add functionality Y with tests
PRIORITY: P0
ASSIGNEE: Agent-2
TAGS: feature, high-priority, backend
PARENT: task-123
```

---

## 💬 **Format 2: Natural Language**

### Simple Request

```
Please fix the memory leak in the worker thread
```

### With Priority Hints

```
URGENT: Deploy the hotfix to production as soon as possible
```

### With Assignment

```
Can @Agent-5 implement the new dashboard feature? It's high priority.
```

### With Context

```
The login system is broken after the last update. 
We need to fix this immediately. Assign to @Agent-1.
```

---

## 🔧 **Format 3: Minimal (Fallback)**

### TODO Style

```
todo: add error handling
```

### Fix Style

```
fix: broken unit tests
```

### Feature Style

```
feature: dark mode toggle
```

### Implement Style

```
implement: rate limiting
```

---

## 🎯 **Priority Levels**

| Priority | Code | When to Use |
|----------|------|-------------|
| **Critical** | P0 | Production down, security issue, blocker |
| **High** | P1 | Important feature, significant bug |
| **Medium** | P2 | Normal work, enhancements |
| **Low** | P3 | Nice-to-have, cleanup, refactoring |

### Auto-Detection Keywords

- **P0**: critical, urgent, asap, emergency, production down
- **P1**: high, important, soon, blocker
- **P2**: medium, normal (default)
- **P3**: low, whenever, nice to have

---

## 🏷️ **Tags**

### In Structured Format

```
TAGS: bug, frontend, urgent
```

### As Hashtags

```
TASK: Fix navigation #bug #frontend #urgent
```

### Common Tags

- **Type**: `#bug`, `#feature`, `#refactor`, `#docs`
- **Area**: `#frontend`, `#backend`, `#api`, `#database`
- **Status**: `#urgent`, `#blocked`, `#review-needed`
- **Version**: `#v2`, `#v2-compliance`, `#migration`

---

## 🤖 **Agent Assignment**

### Direct Assignment

```
ASSIGNEE: Agent-2
```

### Via Mention

```
@Agent-5 please handle this task
```

### Team Assignment

```
ASSIGNEE: Team-Beta
```

---

## 📅 **Due Dates** (Phase-2)

```
TASK: Complete migration
DESC: Move all configs to new system
PRIORITY: P1
DUE: 2025-10-20
```

---

## 🔗 **Parent Tasks** (Subtasks)

```
TASK: Implement error logging
DESC: Add structured logging to all services
PARENT: task-refactor-errors
PRIORITY: P2
```

---

## ✅ **Examples by Use Case**

### Bug Report

```
TASK: Fix login redirect loop
DESC: Users are stuck in redirect loop after OAuth callback.
Happens on Chrome and Firefox. 
PRIORITY: P0
ASSIGNEE: Agent-1
TAGS: bug, auth, critical
```

### Feature Request

```
TASK: Add dark mode support
DESC: Implement dark theme with user preference toggle.
Should persist across sessions.
PRIORITY: P2
ASSIGNEE: Agent-7
TAGS: feature, ui, enhancement
```

### Refactoring Task

```
TASK: Refactor messaging system
DESC: Split into smaller modules per V2 compliance.
Each file must be <400 LOC.
PRIORITY: P1
ASSIGNEE: Agent-2
TAGS: refactor, v2-compliance, architecture
```

### Documentation Task

```
TASK: Update API documentation
DESC: Add examples for all new endpoints from v2.1 release
PRIORITY: P3
ASSIGNEE: Agent-8
TAGS: docs, api
```

### Urgent Hotfix

```
URGENT: Production database connection pool exhausted!
Need immediate fix. @Agent-3 please handle ASAP.
#critical #production #database
```

---

## 🚫 **What NOT to Do**

### ❌ Too Vague

```
fix stuff
```

### ❌ Missing Context

```
TASK: Update
```

### ❌ Multiple Tasks in One

```
TASK: Fix bugs and add features and refactor everything
```

**Instead**, create separate tasks:

```
TASK: Fix login bug
TASK: Add dark mode
TASK: Refactor auth module
```

---

## 💡 **Tips for Good Tasks**

✅ **Be Specific**: Clear, actionable titles  
✅ **Add Context**: Describe what, why, and how  
✅ **Set Priority**: Help agents prioritize work  
✅ **Use Tags**: Enable filtering and search  
✅ **Assign Wisely**: Match task to agent skills  
✅ **Link Related**: Use PARENT for subtasks

---

## 🔄 **Task Lifecycle**

```
Message → Task Created → Agent Claims → Agent Executes → Task Complete → Report Sent
```

Track your task:

```bash
# See your tasks
python -m src.services.messaging_cli --list-tasks

# Claim next task  
python -m src.services.messaging_cli --get-next-task

# Mark complete
python -m src.services.messaging_cli --complete-task <task-id>
```

---

**🐝 Quick Reference - Keep It Simple, Keep It Clear!**

