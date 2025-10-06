# 📱 Compact Messaging Template Example

**Use Case**: Standard agent communications with balanced detail and efficiency.

**Template Stats**: 26 lines, 1406 characters

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
Agent-3, please analyze the current project state and provide recommendations for the next development phase. Focus on V2 compliance and database integration improvements.
🎯 QUALITY GATES REMINDER
============================================================
📋 V2 COMPLIANCE: ≤400 lines • ≤5 classes • ≤10 functions
🚫 NO: Abstract classes • Complex inheritance • Threading
✅ USE: Simple data classes • Direct calls • Basic validation
🎯 KISS: Keep it simple! • Run `python quality_gates.py`
============================================================
📝 DEVLOG: 'python src/services/agent_devlog_posting.py --agent <flag> --action <desc>'
🗃️ DATABASES: Swarm Brain (r.search), Unified (sqlite3), Vector (VectorDatabaseIntegration)
🔄 TOOLS: Scan (scan_tools.py), Find (find_tool.py), Project (run_project_scan.py)
🚀 MESSAGING: messaging_service.py, Discord (run_discord_messaging.py)
💡 REMEMBER: Query databases every cycle phase for patterns and knowledge!
============================================================
🔄 AGENT CYCLE: CHECK_INBOX → EVALUATE_TASKS → EXECUTE_ROLE → QUALITY_GATES → CYCLE_DONE
🚀 KICKOFF: Start with PHASE 1 (CHECK_INBOX) to begin autonomous cycle!
============================================================
-------------------------------------------------------------
```

## 🎯 **When to Use Compact Template**

- ✅ **Standard Communications**: Regular agent-to-agent messaging
- ✅ **Task Assignments**: Detailed task instructions with tool guidance
- ✅ **Status Updates**: Comprehensive progress reports
- ✅ **Coordination Messages**: Multi-agent coordination and handoffs

## 📊 **Features Included**

- **Complete Quality Gates**: Full V2 compliance guidelines with KISS principles
- **Detailed Devlog**: Complete devlog posting command with parameters
- **Database Integration**: All three databases with access methods
- **Tool Discovery**: Key tool scanning and finding commands
- **Messaging Systems**: Core messaging and Discord integration
- **Cycle Execution**: Complete 5-phase cycle with kickoff instruction

## 🔧 **Usage Example**

```python
from src.services.messaging_service_utils import MessageFormatter

formatter = MessageFormatter()
message = formatter.format_a2a_message(
    from_agent="Agent-4",
    to_agent="Agent-3",
    content="Analyze project state and provide V2 compliance recommendations",
    priority="HIGH",
    compact=True  # Use compact template
)
```

## 🚀 **Tool Reminders Included**

### **Database Integration:**
- 🧠 **Swarm Brain**: `r.search()` for pattern recognition
- 🔧 **Unified DB**: `sqlite3` for task management
- 🧠 **Vector DB**: `VectorDatabaseIntegration` for semantic search

### **Tool Discovery:**
- 📁 **Scan Tools**: `python tools/scan_tools.py`
- 🔍 **Find Tools**: `python tools/find_tool.py --query "need"`
- 📊 **Project Analysis**: `python tools/run_project_scan.py`

### **Messaging & Coordination:**
- 📨 **Messaging Service**: `src/services/messaging_service.py`
- 🤖 **Discord Bot**: `python run_discord_messaging.py`

## 💡 **Benefits**

- **Balanced Detail**: Comprehensive guidance without overwhelming length
- **Tool Integration**: All major tools and databases covered
- **Autonomous Support**: Complete cycle execution instructions
- **Efficient**: Optimal balance of information density and readability

---

**Perfect for**: Standard agent communications, task assignments, and coordination where agents need comprehensive tool and database guidance for autonomous operation.
