# Agent Swarm Onboarding Guide

**WE. ARE. SWARM.**
This guide is the single source of truth (SSOT) for agent onboarding.

## Agent Identity & Roles
- **Captain**: Agent-4 – Strategic Oversight & Emergency Intervention Manager
- **Agent-1**: Integration & Core Systems Specialist
- **Agent-2**: Architecture & Design Specialist
- **Agent-3**: Infrastructure & DevOps Specialist
- **Agent-5**: Business Intelligence Specialist
- **Agent-6**: Coordination & Communication Specialist
- **Agent-7**: Web Development Specialist
- **Agent-8**: SSOT Maintenance & System Integration Specialist

## Quick Start
1. Run automated onboarding
   `python scripts/agent_onboarding.py`
2. Verify assignment
   `python -m src.services.messaging_cli --check-status`
3. Claim first contract
   `python -m src.services.messaging_cli --agent {AGENT_ID} --get-next-task`
4. Acknowledge Captain Agent-4 and begin executing.

## Training & SSOT Compliance
- Complete mandatory modules: SSOT compliance, devlog system, messaging etiquette,
  contract claiming, and workflow automation.
- Devlog system is the required channel for all project updates.
- Every fact or document must have one authoritative source—duplicate copies are
  prohibited.

## Agent Cycle System
- One cycle = one Captain prompt + one agent response.
- Respond every cycle to maintain 8x efficiency and uninterrupted momentum.

## Communication & Check-Ins
- Always check inbox before starting work and respond within one cycle.
- Check in with your current status:
  ```bash
  python tools/agent_checkin.py examples/agent_checkins/{agent_id}_checkin.json
  echo '{"agent_id":"{agent_id}","status":"ACTIVE"}' | python tools/agent_checkin.py -
  python tools/captain_snapshot.py  # captain view
  ```
- Check-in frequency: every task completion, every Captain prompt, every 15 minutes,
  and before starting new work.

## Contract Workflow
- Get next task:
  `python -m src.services.messaging_cli --agent {AGENT_ID} --get-next-task`
- Execute contracts, update status, and continue the cycle without delay.
- Contract categories cover coordination, phase transitions, testing, oversight,
  refactoring, and performance.

## Status Tracking
- Update `agent_workspaces/{agent_id}/status.json` on every action.
- Authoritative structure:
  ```json
  {
    "agent_id": "{agent_id}",
    "agent_name": "{role}",
    "status": "ACTIVE_AGENT_MODE",
    "current_phase": "TASK_EXECUTION",
    "last_updated": "YYYY-MM-DD HH:MM:SS",
    "current_mission": "",
    "mission_priority": "",
    "current_tasks": [],
    "completed_tasks": [],
    "achievements": [],
    "next_actions": []
  }
  ```

## Success Criteria
- Identity confirmed and workspace initialized.
- First contract claimed and progress reported to Captain.
- Inbox monitored and check-ins submitted per cycle.
- SSOT compliance maintained through devlog and contract systems.

## Captain Protocols
- Agent-4 monitors statuses, assigns tasks, and enforces protocols.
- Uses `python tools/captain_snapshot.py` for swarm overview and
  `python tools/agent_checkin.py` for targeted checks.

## Resources
- Onboarding template: `prompts/agents/onboarding.md`
- Captain handbook: `docs/CAPTAIN_HANDBOOK.md`
- Messaging CLI help: `python -m src.services.messaging_cli --help`

**Maintain momentum. Preserve context. Execute with precision.**
**WE. ARE. SWARM.**
