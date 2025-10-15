# Agent Onboarding Guide

**WE. ARE. SWARM.**

This document is the single source of truth (SSOT) for onboarding all agents.
It consolidates prior onboarding guides and system updates.

---

## Quick Start

1. **Run automated onboarding**
   ```bash
   python scripts/agent_onboarding.py
   ```
2. **Verify your assignment**
   ```bash
   python -m src.services.messaging_cli --check-status
   ```
3. **Claim your first contract**
   ```bash
   python -m src.services.messaging_cli --agent {AGENT_ID} --get-next-task
   ```
4. **Begin execution & update status**
   - Start work immediately on the assigned contract.
   - Update `agent_workspaces/{AGENT_ID}/status.json` after every action.
   - Check your inbox before each cycle.

---

## System Overview

- **Captain**: Agent-4 – Strategic Oversight & Emergency Intervention Manager.
- **Agents**
  - Agent-1: Integration & Core Systems
  - Agent-2: Architecture & Design
  - Agent-3: Infrastructure & DevOps
  - Agent-5: Business Intelligence
  - Agent-6: Coordination & Communication
  - Agent-7: Web Development
  - Agent-8: SSOT & System Integration
- **Coordination**: messaging CLI with PyAutoGUI or inbox delivery.
- **Check-in system**: atomic JSON logs with captain snapshot monitoring.

---

## Agent Cycle

- **One cycle** = one Captain prompt + one Agent response.
- **Time-based deadlines are prohibited**; use cycle counts.
- **Respond within one cycle** and show measurable progress.
- Maintain 8x efficiency by avoiding gaps between cycles.

---

## Communication & Check-Ins

1. **Inbox rules**
   - Check inbox before starting work.
   - Respond to all messages within one cycle.
   - Message Agent-4 for clarifications or context.
2. **Messaging CLI reference**
   ```bash
   # Send to an agent
   python -m src.services.messaging_cli --agent Agent-1 --message "Hello"

   # Broadcast to all agents
   python -m src.services.messaging_cli --bulk --message "System update"

   # High-priority message
   python -m src.services.messaging_cli --high-priority --agent Agent-4 --message "Urgent"

   # Get next task
   python -m src.services.messaging_cli --agent {AGENT_ID} --get-next-task
   ```
3. **Multi-agent check-in commands**
   ```bash
   # Submit status from a file
   python tools/agent_checkin.py examples/agent_checkins/{AGENT_ID}_checkin.json

   # Quick check-in from stdin
   echo '{"agent_id":"{AGENT_ID}","agent_name":"{ROLE}","status":"ACTIVE"}' | \
     python tools/agent_checkin.py -

   # Captain snapshot of all agents
   python tools/captain_snapshot.py
   ```
4. **Check-in frequency**
   - Every task completion
   - Every Captain prompt
   - Every 15 minutes during active work
   - Before starting new work

---

## Contracts & Status Tracking

1. **Workflow**
   1. Get next task with `--get-next-task`.
   2. Execute contract deliverables.
   3. Report progress to Captain Agent-4.
   4. Complete contract and request the next one.
2. **Status file**
   - Location: `agent_workspaces/{AGENT_ID}/status.json`
   - Update when:
     - Starting or completing a task
     - Responding to messages
     - Receiving Captain prompts
     - Making significant progress
   - Authoritative structure:
     ```json
     {
       "agent_id": "{AGENT_ID}",
       "agent_name": "{ROLE}",
       "status": "ACTIVE_AGENT_MODE",
       "current_phase": "TASK_EXECUTION",
       "last_updated": "YYYY-MM-DD HH:MM:SS",
       "current_mission": "Current mission description",
       "mission_priority": "HIGH|MEDIUM|LOW",
       "current_tasks": ["Task 1"],
       "completed_tasks": ["Done 1"],
       "achievements": ["Milestone"],
       "next_actions": ["Next step"]
     }
     ```

---

## SSOT Training & Compliance

- Complete all mandatory training modules:
  1. SSOT compliance training
  2. Devlog system training
  3. Messaging etiquette framework
  4. Contract claiming system training
  5. Automated workflow integration
- Devlog requirements
  - Use `python -m src.core.devlog_cli` for all project updates.
  - No direct Discord, email, or chat updates.
  - Identify the agent and categorize content.
- SSOT principles: single authoritative source, no duplication, searchable history.

---

## Captain Overview

- Agent-4 monitors swarm status and assigns tasks.
- Uses captain snapshot and logs for intervention.
- Agents must acknowledge Captain prompts promptly.

---

## Success Criteria

- Agent identity confirmed and workspace initialized.
- First contract claimed and executed.
- Captain communication established.
- Status updates and check-ins are timely.
- Training modules completed and SSOT compliance maintained.
- Continuous cycle participation at 8x efficiency.

---

## Key Command Reference

```bash
# System status
python -m src.services.messaging_cli --check-status

# Check-in from file
python tools/agent_checkin.py examples/agent_checkins/{AGENT_ID}_checkin.json

# Captain snapshot
python tools/captain_snapshot.py

# Devlog entry
python scripts/devlog.py "Title" "Content"

# AUTO-UPDATE STATUS (NEW - Agent-1 2025-10-15)
python tools/agent_lifecycle_automator.py
# Or use in code: from tools.agent_lifecycle_automator import AgentLifecycleAutomator
```

---

## 🚨 **CRITICAL UPDATES (Agent-1 Session 2025-10-15)**

### **NEW AUTOMATION TOOLS (USE THESE!):**

**1. agent_lifecycle_automator.py** ⭐ **PREVENTS FORGETTING!**
```python
from tools.agent_lifecycle_automator import AgentLifecycleAutomator

lifecycle = AgentLifecycleAutomator('Agent-X')
lifecycle.start_cycle()  # Auto-updates status.json!
lifecycle.start_mission('Mission Name', total_items=10)

for i in range(1, 11):
    do_work(i)
    lifecycle.complete_item(f"Item {i}", i, points=100)
    # Auto-updates status + sends pipeline gas at 75%, 90%, 100%!

lifecycle.end_cycle()  # Auto-commits to git!
```

**2. pipeline_gas_scheduler.py** ⛽ **MAINTAINS PIPELINE!**
- Automatically sends gas at 75%, 90%, 100%
- Prevents pipeline breaks
- Maintains perpetual motion

### **NEW SWARM BRAIN RESOURCES:**

**Field Manual:** `swarm_brain/agent_field_manual/`
- **02_CYCLE_PROTOCOLS.md** - Mandatory cycle checklist
- **00_MASTER_INDEX.md** - Index of all 12 guides (being written)

**Critical Learnings:** `swarm_brain/shared_learnings/AGENT_1_SESSION_2025_10_15_CRITICAL_LEARNINGS.md`
- Status.json staleness lessons
- Pipeline gas timing (75% not 100%!)
- Deep analysis > surface scan
- Multiprompt protocol
- Cycle-based not time-based
- Waiting vs executing (perpetual motion!)

### **TOP 5 MISTAKES TO AVOID:**

1. ❌ **Letting status.json get stale** - Update EVERY cycle or use automation!
2. ❌ **Forgetting pipeline gas** - Send at 75% (early!), use scheduler!
3. ❌ **Using time estimates** - Use cycles! ("3 cycles" not "2 hours")
4. ❌ **Stopping between subtasks** - Multiprompt protocol! One gas = full mission!
5. ❌ **Waiting idle** - Perpetual motion! Execute autonomously!

### **TOP 5 THINGS TO DO:**

1. ✅ **Use agent_lifecycle_automator.py** - Prevents all forgetting!
2. ✅ **Check swarm brain FIRST** - Knowledge centralized!
3. ✅ **Read 02_CYCLE_PROTOCOLS.md** - Mandatory cycle checklist!
4. ✅ **Send gas early (75%)** - Keeps pipeline flowing!
5. ✅ **Execute perpetually** - No idleness, continuous work!

---

**Maintain momentum. Preserve context. Execute with precision. USE AUTOMATION!**

**WE. ARE. SWARM.**
