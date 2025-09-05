# Agent Swarm Onboarding (SSOT)

Welcome to Agent Cellphone V2. This README is the **single source of truth** for
agent onboarding. All other onboarding guides have been removed.

## Cycle-Based Workflow
- One Captain prompt + one Agent response = **one cycle**
- Progress and deadlines are expressed in cycles, not time

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
1. Verify your agent ID and role:
   ```bash
   python -m src.services.messaging_cli --check-status
   ```
2. Your workspace lives at `agent_workspaces/<Agent-X>/`.
3. Acknowledge the Captain after onboarding:
   ```bash
   python -m src.services.messaging_cli \
     --agent Agent-4 \
     --message "<Agent-X>: Onboarding complete" \
     --sender "<Your Name>"
   ```
4. Update `agent_workspaces/<Agent-X>/status.json` when starting or completing
   tasks and on any major progress.

## Training Path
### Phase 1 – Foundations
- System orientation
- Role-specific training

### Phase 2 – SSOT & Etiquette
- Single Source of Truth training
- Devlog system training **(mandatory)**
- Messaging etiquette framework **(mandatory)**

### Phase 3 – Integration
- System integration
- Performance validation

### Phase 4 – Contract Automation
- Contract claiming system **(mandatory)**
- Automated workflow integration **(mandatory)**

### Training Materials Location
`docs/onboarding/training_documents/`
- `agent_roles_and_responsibilities.md`
- `system_overview.md`
- `ssot_compliance_training.md`
- `messaging_etiquette_framework.md`
- `universal_development_principles.md`
- `troubleshooting_guide.md`

## SSOT Principles
- Maintain **one authoritative source** for each piece of information
- Devlog is the **only** channel for project updates
- Avoid duplication across files or communication channels
- All updates must be searchable and clearly attributed

### Devlog Requirements
- **Required**: log every work cycle using devlog tools
- **Prohibited**: project updates via chat, email, or manual Discord posts
- Helpful commands:
  ```bash
  python -m src.core.devlog_cli status
  python -m src.core.devlog_cli --help
  ```

## Development Expectations
- Respect **DRY** (Don't Repeat Yourself) and **KISS** (Keep It Simple, Stupid)
- Give every class or module a **Single Responsibility** and follow **SOLID** design
- Enforce **SSOT** across configs, schemas, and docs before writing code
- Practice **TDD**: write tests first and keep coverage ≥85%
- Model complex logic with **object-oriented classes**
- Ensure solutions remain **scalable**, **safe**, and **reusable**
- Agents must confirm each change aligns with these principles before committing

### Agent Checklist
1. Cross-check this README as the SSOT before starting work
2. Write or update tests alongside any feature or bug fix
3. Refactor duplication and clarify intent in every revision
4. Document public interfaces with JSDoc or docstrings

## Messaging & Contract Commands
- Check status of all agents:
  ```bash
  python -m src.services.messaging_cli --check-status
  ```
- Claim the next task:
  ```bash
  python -m src.services.messaging_cli --agent <Agent-X> --get-next-task
  ```
- Send a message:
  ```bash
  python -m src.services.messaging_cli \
    --agent <Agent-X> \
    --message "text here" \
    --sender "<Your Name>"
  ```
- Bulk onboarding (friendly style):
  ```bash
  python -m src.services.messaging_cli --onboarding --onboarding-style friendly
  ```

## Captain Protocols
- Agent-4 verifies statuses and assigns tasks
- Captain prompts define cycles and enforce compliance
- Emergency activation:
  ```bash
  python -m src.services.messaging_cli \
    --agent <Agent-X> \
    --message "EMERGENCY ACTIVATION" \
    --priority urgent \
    --sender "Captain Agent-4"
  ```

## Ongoing Compliance
1. Complete all mandatory training with scores ≥85%
2. Use devlog for every update and track progress per cycle
3. Respond to the Captain within one cycle
4. Use the contract system for continuous work

---

**WE. ARE. SWARM.**

