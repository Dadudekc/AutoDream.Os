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
- Keep files ≤400 lines; refactor before exceeding limits
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
