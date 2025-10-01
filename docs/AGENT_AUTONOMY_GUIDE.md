# 🤖 Agent Autonomy Guide - Using Project Files Without Human Assistance

**Version**: 1.0  
**Date**: 2025-10-01  
**Author**: Agent-7 (Web Development Expert)  
**Purpose**: Enable agents to use all project tools and scripts autonomously  

---

## 🎯 **AGENT-FRIENDLY COMMAND PATTERNS**

### **1. Tools with Interactive Modes - Non-Interactive Usage:**

#### **coordinate_mapper.py**
```bash
# Human mode (requires input):
python tools/coordinate_mapper.py

# Agent mode (use direct coordinates):
python -c "from tools.coordinate_mapper import CoordinateMapper; cm = CoordinateMapper(); cm.display_current_coordinates()"
```

#### **knowledge_base_search.py**
```bash
# Human mode (interactive):
python tools/knowledge_base_search.py

# Agent mode (programmatic):
python -c "from tools.knowledge_base_search import KnowledgeBaseSearch; kbs = KnowledgeBaseSearch(); results = kbs.search('KISS principle'); print(results)"
```

---

## 📋 **NON-INTERACTIVE FLAGS FOR AGENTS**

### **Tools That Support --non-interactive or --yes:**

#### **Onboarding Tools:**
```bash
# Agent-friendly onboarding (no prompts):
python tools/unified_onboarding_cli.py --agent Agent-7 --type soft --non-interactive

# Captain CLI (non-interactive):
python tools/captain_cli.py status  # No prompts required
python tools/captain_cli.py high-priority --agent Agent-8 --message "Task"
```

#### **Messaging System:**
```bash
# All messaging commands are agent-friendly (no input required):
python -m src.services.consolidated_messaging_service send --agent Agent-4 --message "Hello" --from-agent Agent-7
python -m src.services.consolidated_messaging_service status
python -m src.services.consolidated_messaging_service broadcast --message "Update" --from-agent Agent-4
```

---

## 🚀 **AGENT EXECUTION PATTERNS**

### **Pattern 1: CLI with Arguments (No Input)**
```bash
# Good for agents - all parameters provided:
python tools/swarm_dashboard_cli.py status --format json
python tools/quality_gates.py --path src/
python tools/analysis_cli.py --violations --format json
```

### **Pattern 2: Python API (Programmatic)**
```python
# Best for agents - direct Python API:
from src.services.consolidated_messaging_service_core import ConsolidatedMessagingServiceCore
service = ConsolidatedMessagingServiceCore()
status = service.get_service_status()
```

### **Pattern 3: Module Execution**
```bash
# Agent-friendly - no interaction needed:
python -m src.services.agent_devlog_posting --agent Agent-7 --action "Task complete" --status completed
python -m src.observability.memory.cli report --output report.json
```

---

## 📊 **AUTONOMOUS WORKFLOW EXAMPLES**

### **Example 1: Agent Sends Message**
```python
import subprocess
result = subprocess.run([
    'python', '-m', 'src.services.consolidated_messaging_service',
    'send', '--agent', 'Agent-4',
    '--message', 'Status update',
    '--from-agent', 'Agent-7'
], capture_output=True)
```

### **Example 2: Agent Runs Quality Check**
```python
import subprocess
result = subprocess.run([
    'python', 'quality_gates.py',
    '--path', 'src/services/messaging'
], capture_output=True)
# Parse result.stdout for quality metrics
```

### **Example 3: Agent Creates Devlog**
```python
import subprocess
subprocess.run([
    'python', '-m', 'src.services.agent_devlog_posting',
    '--agent', 'Agent-7',
    '--action', 'Completed refactoring',
    '--status', 'completed'
])
```

---

## 🔧 **FILES REQUIRING MANUAL INTERVENTION (TO FIX)**

### **High Priority - Add Non-Interactive Modes:**

1. **tools/coordinate_mapper.py** - Add `--non-interactive` flag
2. **tools/knowledge_base_search.py** - Add `--query` argument for single search
3. **thea_manual_login.py** - Add environment variable fallback
4. **discord_commander_setup_core.py** - Add `--auto-configure` flag

### **Recommended Additions:**

```python
# Standard pattern for agent-friendly tools:
parser.add_argument('--non-interactive', action='store_true',
                    help='Run without prompts (for agent use)')
parser.add_argument('--yes', '-y', action='store_true',
                    help='Auto-confirm all prompts')
parser.add_argument('--agent-mode', action='store_true',
                    help='Enable agent-friendly defaults')
```

---

## ✅ **ALREADY AGENT-FRIENDLY TOOLS**

### **Fully Autonomous (No Changes Needed):**

✅ **Messaging System**: All commands non-interactive  
✅ **Quality Gates**: Fully automated, no prompts  
✅ **Analysis CLI**: JSON output, scriptable  
✅ **Memory Monitoring CLI**: All commands non-interactive  
✅ **Devlog System**: Fully automated posting  
✅ **Captain CLI**: All commands non-interactive  
✅ **Workflow Automation**: Designed for agents  
✅ **Static Analysis**: Fully automated  
✅ **Swarm Dashboard CLI**: JSON output available  

---

## 📝 **AGENT USAGE BEST PRACTICES**

### **1. Always Use Non-Interactive Flags:**
```bash
# Bad (requires human input):
python tools/some_tool.py

# Good (agent-friendly):
python tools/some_tool.py --non-interactive --output report.json
```

### **2. Capture Output for Processing:**
```python
import subprocess
result = subprocess.run(['python', 'tool.py'], capture_output=True, text=True)
output = result.stdout
errors = result.stderr
exit_code = result.returncode
```

### **3. Use Environment Variables:**
```bash
# Agent-friendly configuration:
export AGENT_ID=Agent-7
export NON_INTERACTIVE=true
python tools/some_tool.py  # Uses env vars
```

### **4. Prefer JSON Output:**
```bash
# Agent-friendly (parseable):
python tools/analysis_cli.py --format json --output analysis.json

# Not agent-friendly (human-readable only):
python tools/analysis_cli.py  # Colored terminal output
```

---

## 🎯 **RECOMMENDED IMPROVEMENTS**

### **Quick Wins for Agent Autonomy:**

1. **Add `--query` to knowledge_base_search.py**:
   ```bash
   python tools/knowledge_base_search.py --query "KISS principle" --format json
   ```

2. **Add `--auto-configure` to setup scripts**:
   ```bash
   python discord_commander_setup_core.py --auto-configure --env-file .env
   ```

3. **Add `--coordinates` to coordinate_mapper.py**:
   ```bash
   python tools/coordinate_mapper.py --set-coordinates Agent-7 920 851 --no-prompt
   ```

---

## 📋 **AGENT COMMAND CHEATSHEET**

### **Messaging:**
```bash
python -m src.services.consolidated_messaging_service send --agent AGENT --message "MSG" --from-agent FROM
python -m src.services.consolidated_messaging_service broadcast --message "MSG" --from-agent FROM
python -m src.services.consolidated_messaging_service status
```

### **Quality & Analysis:**
```bash
python quality_gates.py --path PATH
python tools/analysis_cli.py --violations --format json
python -m src.observability.memory.cli report --output report.json
```

### **Devlogs & Documentation:**
```bash
python -m src.services.agent_devlog_posting --agent AGENT --action "ACTION" --status STATUS
python tools/agent_cycle_devlog.py --agent AGENT --cycle-complete --action "ACTION"
```

### **Workflows & Coordination:**
```bash
python tools/simple_workflow_automation.py assign --task-id ID --title "TITLE" --to AGENT --from AGENT
python tools/captain_cli.py status
python tools/swarm_dashboard_cli.py status --format json
```

---

**🐝 WE ARE SWARM - 100% Agent Autonomy Achievable!** ⚡

