# 📱 Full Messaging Template Example

**Use Case**: Comprehensive agent communications with complete system integration guidance.

**Template Stats**: 48 lines, 2560 characters

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
Agent-3, you are assigned the INTEGRATION_SPECIALIST role for the next development cycle. Your mission is to analyze the current system architecture, identify integration opportunities, and provide comprehensive recommendations for improving database connectivity and tool discovery mechanisms. Use all available databases and tools to conduct a thorough analysis.
🎯 QUALITY GATES REMINDER
============================================================
📋 V2 COMPLIANCE: ≤400 lines • ≤5 classes • ≤10 functions
🚫 NO: Abstract classes • Complex inheritance • Threading
✅ USE: Simple data classes • Direct calls • Basic validation
🎯 KISS: Keep it simple! • Run `python quality_gates.py`
============================================================
📝 DEVLOG: Use 'python src/services/agent_devlog_posting.py --agent <flag> --action <desc>'
============================================================
🗃️ DATABASE INTEGRATION REMINDERS:
🧠 Swarm Brain: from swarm_brain import Retriever; r = Retriever(); r.search("query", k=5)
🔧 Unified DB: import sqlite3; conn = sqlite3.connect("unified.db")
🧠 Vector DB: from src.services.vector_database import VectorDatabaseIntegration
🤖 ML Model: Automated SSOT violation prevention via PredictiveSSOTEngine
============================================================
🔄 DYNAMIC TOOL DISCOVERY:
📁 Scan Tools: python tools/scan_tools.py
🔍 Find Tools: python tools/find_tool.py --query "need"
📊 Project Analysis: python tools/run_project_scan.py
🎯 Captain Tools: python tools/captain_cli.py
📈 Analysis Tools: python tools/analysis_cli.py
============================================================
🚀 MESSAGING & COORDINATION:
📨 Messaging Service: src/services/messaging_service.py
🤖 Discord Bot: python run_discord_messaging.py
📋 Captain Directives: tools/captain_directive_manager.py
🔄 Workflow Manager: tools/agent_workflow_manager.py
============================================================
💡 REMEMBER: Query databases every cycle phase for patterns, tasks, and knowledge!
============================================================
🔄 AGENT CYCLE EXECUTION ORDER (2-5 min cycles):
PHASE 1: CHECK_INBOX → Query Swarm Brain + Vector DB for patterns
PHASE 2: EVALUATE_TASKS → Check task status in Unified DB  
PHASE 3: EXECUTE_ROLE → Store work in databases + run project scanner
PHASE 4: QUALITY_GATES → Store results in databases + run quality_gates.py
PHASE 5: CYCLE_DONE → Update all databases + report to Captain
🚀 KICKOFF: Start with PHASE 1 (CHECK_INBOX) to begin autonomous cycle!
============================================================
-------------------------------------------------------------
```

## 🎯 **When to Use Full Template**

- ✅ **Complex Task Assignments**: Multi-faceted missions requiring comprehensive guidance
- ✅ **Role Onboarding**: New agent role assignments with detailed instructions
- ✅ **System Integration**: Projects requiring full database and tool integration
- ✅ **Training Scenarios**: Educational communications with complete context
- ✅ **Strategic Planning**: High-level coordination requiring full system awareness

## 📊 **Features Included**

### **Complete Quality Gates:**
- Full V2 compliance guidelines with detailed restrictions
- KISS principles and best practices
- Quality gates execution command

### **Comprehensive Database Integration:**
- 🧠 **Swarm Brain**: Complete usage with `Retriever` class and search patterns
- 🔧 **Unified Database**: SQLite operations for task management
- 🧠 **Vector Database**: Full integration with `VectorDatabaseIntegration`
- 🤖 **ML Model**: Automated SSOT violation prevention system

### **Dynamic Tool Discovery:**
- 📁 **Tool Scanning**: Complete tool discovery system
- 🔍 **Tool Finding**: Intelligent tool search capabilities
- 📊 **Project Analysis**: Comprehensive project scanning
- 🎯 **Captain Tools**: Coordination and directive management
- 📈 **Analysis Tools**: Code analysis and quality assessment

### **Messaging & Coordination:**
- 📨 **Messaging Service**: Core communication infrastructure
- 🤖 **Discord Bot**: Discord integration and automation
- 📋 **Captain Directives**: Directive management system
- 🔄 **Workflow Manager**: Workflow automation and coordination

### **Detailed Cycle Execution:**
- **PHASE 1**: CHECK_INBOX with database query instructions
- **PHASE 2**: EVALUATE_TASKS with task status checking
- **PHASE 3**: EXECUTE_ROLE with database storage and project scanning
- **PHASE 4**: QUALITY_GATES with result storage and validation
- **PHASE 5**: CYCLE_DONE with complete database updates and reporting

## 🔧 **Usage Example**

```python
from src.services.messaging_service_utils import MessageFormatter

formatter = MessageFormatter()
message = formatter.format_a2a_message(
    from_agent="Agent-4",
    to_agent="Agent-3",
    content="Complex integration analysis mission with full system utilization",
    priority="CRITICAL"
    # compact=False is default for full template
)
```

## 🚀 **Complete System Integration**

### **Database Operations:**
```python
# Swarm Brain Pattern Recognition
from swarm_brain import Retriever
r = Retriever()
patterns = r.search("integration challenges", k=5)

# Unified Database Task Management
import sqlite3
conn = sqlite3.connect("unified.db")
# Task operations...

# Vector Database Semantic Search
from src.services.vector_database import VectorDatabaseIntegration
vdb = VectorDatabaseIntegration()
similar = vdb.search_similar("system architecture", k=5)
```

### **Tool Discovery Commands:**
```bash
# Discover all available tools
python tools/scan_tools.py

# Find specific functionality
python tools/find_tool.py --query "integration analysis"

# Run comprehensive project analysis
python tools/run_project_scan.py
```

### **Cycle Phase Integration:**
- **Every Phase**: Database query and update operations
- **Tool Integration**: Specific tools for each phase
- **Quality Assurance**: Continuous validation and compliance
- **Knowledge Storage**: Persistent learning and pattern recognition

## 💡 **Benefits**

- **Complete Autonomy**: Agents have all information needed for independent operation
- **System Mastery**: Full understanding of all available tools and databases
- **Comprehensive Guidance**: Every aspect of agent operation covered
- **Learning Integration**: Continuous knowledge capture and pattern recognition
- **Quality Assurance**: Built-in compliance and validation throughout

---

**Perfect for**: Complex missions, role onboarding, system integration projects, and any scenario requiring comprehensive agent guidance with full system utilization.
