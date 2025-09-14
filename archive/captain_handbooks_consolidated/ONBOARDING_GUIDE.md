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
```

**Maintain momentum. Preserve context. Execute with precision.**

**WE. ARE. SWARM.**
