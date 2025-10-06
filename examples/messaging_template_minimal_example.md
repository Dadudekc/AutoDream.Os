# 📱 Minimal Messaging Template Example

**Use Case**: Space-critical communications, quick acknowledgments, or when message length is limited.

**Template Stats**: 16 lines, 775 characters

---

## 📋 **Example Message**

```
============================================================
[A2A] MESSAGE
============================================================
📤 FROM: Agent-4
📥 TO: Agent-3
Priority: NORMAL
Tags: GENERAL
-------------------------------------------------------------
Agent-3, please begin your autonomous cycle. Check inbox for new tasks.
🎯 QUALITY GATES: V2 compliance • Run quality_gates.py
📝 DEVLOG: agent_devlog_posting.py --agent <flag> --action <desc>
🗃️ DATABASES: Swarm Brain (r.search) • Unified (sqlite3) • Vector (VectorDatabaseIntegration)
🔄 AGENT CYCLE: CHECK_INBOX → EVALUATE_TASKS → EXECUTE_ROLE → QUALITY_GATES → CYCLE_DONE
🚀 KICKOFF: Start with PHASE 1 (CHECK_INBOX) to begin autonomous cycle!
============================================================
-------------------------------------------------------------
```

## 🎯 **When to Use Minimal Template**

- ✅ **Quick Acknowledgments**: Fast responses that don't need extensive guidance
- ✅ **Space-Limited Scenarios**: When message length is constrained
- ✅ **High-Frequency Messages**: Regular status updates or confirmations
- ✅ **Emergency Communications**: When speed is more important than detail

## 📊 **Features Included**

- **Core Quality Gates**: Essential V2 compliance reminders
- **Basic Devlog**: Simple devlog posting command
- **Database Essentials**: Key database commands (Swarm Brain, Unified, Vector)
- **Cycle Execution**: Complete 5-phase cycle order with kickoff instruction

## 🔧 **Usage Example**

```python
from src.services.messaging_service_utils import MessageFormatter

formatter = MessageFormatter()
message = formatter.format_a2a_message(
    from_agent="Agent-4",
    to_agent="Agent-3", 
    content="Begin autonomous cycle - check inbox for tasks",
    priority="NORMAL",
    minimal=True  # Use minimal template
)
```

## 💡 **Benefits**

- **Ultra-Compact**: Minimal space usage while maintaining essential information
- **Fast Processing**: Quick to read and understand
- **Complete Cycle Info**: Still includes full agent cycle execution order
- **Database Integration**: Core database commands for autonomous operation

---

**Perfect for**: Quick task assignments, status confirmations, and space-constrained communications where agents need the essential information to begin autonomous operation.
