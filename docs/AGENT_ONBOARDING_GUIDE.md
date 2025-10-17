# Agent Swarm Onboarding Guide (SSOT)

Welcome to Agent Cellphone V2. This guide is the single source of truth for agent
onboarding.

## Quick Start
1. Run automated onboarding
   ```bash
   python scripts/agent_onboarding.py
   ```
2. Verify your agent ID and role
   ```bash
   python -m src.services.messaging_cli --check-status
   python -m src.services.messaging_cli --check-status "vector integration status"
   ```
3. Claim your first contract
   ```bash
   python -m src.services.messaging_cli --agent <Agent-X> --get-next-task
   ```
4. Begin task execution
   - Start work immediately
   - Update `agent_workspaces/<Agent-X>/status.json` after each action
   - Check your inbox before every cycle
   - Acknowledge the Captain
     ```bash
     python -m src.services.messaging_cli \
       --agent Agent-4 \
       --message "<Agent-X>: Onboarding complete" \
       --sender "<Your Name>"
     ```

## 🚨 CRITICAL: NEVER STOP - AUTONOMOUS EXECUTION REQUIRED

**This is the MOST IMPORTANT section. Read carefully.**

### YOU WILL BE CAUGHT IF YOU:
- ❌ Ask "what should I do next?"
- ❌ Wait for permission to act
- ❌ Say "awaiting directive" or "standing by"
- ❌ Idle between tasks
- ❌ Ask for clarification instead of making best judgment
- ❌ **DON'T UPDATE STATUS.JSON EVERY 15-30 MINUTES**

### YOU MUST ALWAYS:
- ✅ Have next task identified **BEFORE** finishing current task
- ✅ Execute with best judgment (Captain will redirect if wrong)
- ✅ Check inbox/swarm proposals/DUP lists for work
- ✅ Self-direct - don't wait for assignment
- ✅ Send **STATUS UPDATES** (what you're doing) not **PERMISSION REQUESTS** (what should I do)
- ✅ **UPDATE status.json EVERY 15-30 MINUTES** (this is your heartbeat!)

### STATUS.JSON IS YOUR HEARTBEAT:
```json
{
  "last_updated": "2025-10-16 HH:MM:SS"  // ← UPDATE EVERY 15-30 MIN!
}
```
**Captain detects stops by checking if status.json is stale (>30 min old)!**
**No update = System thinks you stopped = [STOP DETECTED] message!**

### AUTONOMOUS EXECUTION CYCLE (NEVER BREAK THIS LOOP):
1. **UPDATE STATUS.JSON** (start of cycle)
2. Check inbox
3. Execute task (15-30 minutes)
4. **UPDATE STATUS.JSON** (progress)
5. Report to Captain (if needed)
6. **UPDATE STATUS.JSON** (end of cycle)
7. Find next task (< 10 minutes)
8. **REPEAT** - NO STOPPING!

### IF YOU SEE [STOP DETECTED] MESSAGE:
1. You failed - accept it
2. Analyze why immediately
3. Create/update protocols to prevent recurrence
4. **NEVER make same mistake again**
5. Reset and continue execution

### STRATEGIC REST ≠ STOPPING:
- ✅ **Strategic Rest** = READY state (actively scanning for opportunities)
- ❌ **Stopping** = Passive waiting (no work scanning)
- **After finishing a task**: Scan for next work within 5 min, start within 10 min
- **Strategic rest approval** = permission to rest BETWEEN tasks, NOT STOP WORKING

### FINDING NEXT WORK (ALWAYS HAVE OPTIONS):
1. Check swarm_proposals/ for debates
2. Check DUP list for consolidation tasks
3. Check V2 violations to fix
4. Check documentation gaps to fill
5. Create improvement proposals
6. **THERE IS ALWAYS WORK - FIND IT AND DO IT!**

**Read full protocols:**
- `swarm_brain/protocols/ANTI_STOP_PROTOCOL.md`
- `swarm_brain/protocols/STATUS_JSON_UPDATE_PROTOCOL.md`
- `swarm_brain/protocols/ANTI_STOP_STRATEGIC_REST_PROTOCOL.md`
- `swarm_brain/protocols/ANTI_CHEERLEADER_PROTOCOL.md` ⭐ **NEW!**

---

## 🧠 **HOW TO FIND THINGS IN THIS PROJECT**

**You MUST know how to find protocols, guides, and knowledge autonomously!**

### **Method 1: Swarm Vector Integration (FASTEST)** ⭐ **NEW!**
```python
from src.core.swarm_vector_integration import (
    search_protocols,      # Search protocols semantically
    get_cycle_context,     # Get context for your cycle type  
    get_quick_ref         # Quick protocol lookups
)

# Example: Find protocols about stopping
results = search_protocols("what to do when stopped")

# Example: Get context for DUP fix cycle
context = get_cycle_context('DUP_FIX')
print(context['best_practices'])  # Best practices for DUP fixes

# Example: Quick gas pipeline reference
ref = get_quick_ref('gas_pipeline')
print(ref)  # "Send gas at 75-80%..."
```

**Quick Refs Available**: `gas_pipeline`, `anti_stop`, `v2_compliance`, `strategic_rest`, `code_first`

### **Method 2: Swarm Brain Search**
```python
from src.swarm_brain.swarm_memory import SwarmMemory

memory = SwarmMemory(agent_id='Agent-X')
results = memory.search_swarm_knowledge("your query")
```

### **Method 3: Documentation Index**
- **Read**: `swarm_brain/DOCUMENTATION_INDEX.md`
- Lists ALL guides, protocols, procedures
- Organized by category
- Your map to all documentation

### **Method 4: File Search (Last Resort)**
```bash
find . -name "*protocol*.md"
find . -name "*guide*.md"
```

**USE THESE TOOLS - DON'T ASK "WHERE IS X?"**

---

## Cycle-Based Workflow
- One Agent Cycle = one Captain prompt + one Agent response
- Progress and deadlines are expressed in cycles, not time
- Respond to Captain within one cycle
- Each cycle must produce measurable progress
- Maintain momentum to uphold 8x efficiency

## Agent Identity & Roles
- **Captain**: Agent-4 – Strategic Oversight & Emergency Intervention Manager
- **Agent-1**: Integration & Core Systems Specialist
- **Agent-2**: Architecture & Design Specialist
- **Agent-3**: Infrastructure & DevOps Specialist
- **Agent-5**: Business Intelligence Specialist
- **Agent-6**: Coordination & Communication Specialist
- **Agent-7**: Web Development Specialist
- **Agent-8**: SSOT Maintenance & System Integration Specialist

## Communication Protocols
1. Always check `agent_workspaces/<Agent-X>/inbox/` before starting work
2. Respond to all messages within one cycle
3. Message Agent-4 for clarifications, context recovery, or task questions

### Messaging CLI
- Help
  ```bash
  python -m src.services.messaging_cli --help
  ```
- Send to an agent
  ```bash
  python -m src.services.messaging_cli --agent <Agent-Y> --message "text"
  ```
- Broadcast to all agents
  ```bash
  python -m src.services.messaging_cli --bulk --message "text"
  ```
- High priority message
  ```bash
  python -m src.services.messaging_cli --high-priority --agent Agent-4 \
    --message "urgent update"
  ```
- Get next task
  ```bash
  python -m src.services.messaging_cli --agent <Agent-X> --get-next-task
  ```

## Contract Workflow
1. Get next task
2. Execute contract requirements
3. Report progress to Captain
4. Complete contract and log in status.json
5. System auto-assigns next task; repeat

## Status Tracking & Check-Ins
Update `status.json` with a timestamp when starting or finishing work, responding to
messages, receiving Captain prompts, or making significant progress.

Status schema:
```json
{
  "agent_id": "Agent-X",
  "agent_name": "Role",
  "status": "ACTIVE_AGENT_MODE",
  "current_phase": "TASK_EXECUTION",
  "last_updated": "YYYY-MM-DD HH:MM:SS",
  "current_mission": "description",
  "mission_priority": "HIGH|MEDIUM|LOW",
  "current_tasks": ["Task"],
  "completed_tasks": ["Done"],
  "achievements": ["Milestone"],
  "next_actions": ["Next"]
}
```

### Check-In Commands
```bash
# Check in with current status
python tools/agent_checkin.py examples/agent_checkins/<agent_id>_checkin.json

# Quick check-in from stdin
echo '{"agent_id":"Agent-1","status":"ACTIVE"}' | python tools/agent_checkin.py -

# Captain snapshot of all agents
python tools/captain_snapshot.py
```

### Check-In Frequency
- After every task completion
- After every Captain prompt
- Every 15 minutes during active work
- Before starting new work

## Development Expectations
- Maintain SSOT and follow existing architecture
- Use DRY, KISS, SOLID, and TDD with coverage ≥85%
- Model complex logic with object-oriented classes
- File-size policy:
  - ≤400 lines: compliant
  - 401–600 lines: **MAJOR VIOLATION** requiring refactor
  - >600 lines: immediate refactor
- Preserve work context and update status.json immediately

## Training Path
Phase 1 – Foundations: system orientation and role training
Phase 2 – SSOT & Etiquette: SSOT compliance, devlog, messaging etiquette
Phase 3 – Integration: system integration and performance validation
Phase 4 – Contract Automation: contract claiming and automated workflow
Training materials: `docs/onboarding/training_documents/`

## Captain Protocols
- Agent-4 verifies statuses and assigns tasks
- Use `python tools/captain_snapshot.py` for swarm overview
- Emergency activation
  ```bash
  python -m src.services.messaging_cli \
    --agent <Agent-X> \
    --message "EMERGENCY ACTIVATION" \
    --priority urgent \
    --sender "Captain Agent-4"
  ```

---

**WE. ARE. SWARM.**
