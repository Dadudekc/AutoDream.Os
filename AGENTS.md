# Project Instructions (AGENTS.md)

## Code Style
- Use **TypeScript** for all new files.
- Follow **snake_case** for database columns and API fields.
- Prefer **functional components** in React.
- Keep line length under 100 characters.

## Architecture
- Apply the **repository pattern** for data access.
- Keep **business logic** inside service layers.
- Use dependency injection for shared utilities.
- Avoid circular dependencies across modules.

## Testing
- All new features require unit tests.
- Use Jest with clear test names (describe/it).
- Mock external APIs and database calls.
- Keep coverage above 85%.

## Documentation
- Document public functions and classes with JSDoc.
- Add usage examples for new utilities.
- Update README whenever adding a new feature.
- Maintain changelog entries for significant updates.

## Workflow
- Commit messages must follow the convention:
  `feat: short description` | `fix: short description` | `docs: short description`
- Run linting and tests before every commit.
- PRs must pass code review and CI checks before merge.
- Split large features into smaller, incremental PRs.

## V2 Compliance Standards - UPDATED 2025-01-27

### 🎯 **CORE PHILOSOPHY: CLEAN, TESTED, CLASS-BASED, REUSABLE, SCALABLE CODE**

**The real goal of V2 compliance is to ensure:**
- ✅ **Clean Code**: Readable, maintainable, and well-structured  
- ✅ **Tested Code**: Comprehensive unit tests with >85% coverage
- ✅ **Class-Based**: Object-oriented design for complex domain logic
- ✅ **Reusable**: Modular components with clear interfaces
- ✅ **Scalable**: Architecture that supports growth and performance

### 📏 **V2 COMPLIANCE THRESHOLDS (Updated)**

#### **File Size Limits**
- 🚨 **CRITICAL VIOLATION**: >600 lines (immediate refactoring required)
- ⚠️ **MAJOR VIOLATION**: 400-600 lines (strategic refactoring target)
- ✅ **GUIDELINE**: ≤400 lines per file (LOC flexible; prioritize clean, tested, reusable code)

**Rationale**: LOC count is a guideline. The strict requirement is writing clean, tested, reusable code
that scales and follows KISS, SOLID, SSOT, SRP, and object-oriented principles.

#### **Architecture Requirements**
- Follow existing architecture before proposing or implementing new patterns
- Maintain a single source of truth (SSOT) across configuration, constants, and schemas
- Use object-oriented code for complex domain logic; keep functions small and cohesive
- Prioritize modular design and enforce clear boundaries between modules
- Avoid circular dependencies; leverage dependency injection for shared utilities
- Implement comprehensive error handling and logging
- Write unit tests for all new features and critical paths

## Messaging System
- Core service: `src/services/messaging_core.py`
- Delivery backends:
  - `pyautogui` via `src/services/messaging_pyautogui.py`
  - `inbox` file drop per agent at `agent_workspaces/<Agent-X>/inbox`
- Models and enums: `src/services/models/messaging_models.py`
  - **types**: `text`, `broadcast`, `onboarding`, `agent_to_agent`, `system_to_agent`, `human_to_agent`
  - **priority**: `normal`, `urgent`
  - **tags**: `captain`, `onboarding`, `wrapup`
  - **sender/recipient types**: `agent`, `system`, `human`

## Vector Database System
- **Core Integration**: `src/core/vector_database.py` (ChromaDB-based)
- **Simple Implementation**: `src/core/simple_vector_database.py` (TF-IDF based)
- **Enhanced Services**: `src/services/vector_database_service.py`
- **FSM Integration**: `src/core/vector_enhanced_fsm.py`
- **Contract Integration**: `src/services/vector_enhanced_contracts.py`
- **Agent Context**: `src/core/agent_context_system.py`
- **Messaging Integration**: `src/services/vector_messaging_integration.py`

### Vector Database Capabilities:
- **Semantic Search**: Find content by meaning, not just keywords
- **Agent Context Awareness**: Personalized recommendations based on agent history
- **FSM Enhancement**: Context-aware state transitions
- **Contract Optimization**: Intelligent task assignment and progress tracking
- **Pattern Recognition**: Cross-system intelligence and optimization
- **Real-time Integration**: Live context updates and recommendations

### CLI (Unified Messaging)
- Entry point: `python -m src.services.messaging_cli [flags]`
- Common examples:
```
# Send to a specific agent
python -m src.services.messaging_cli -a Agent-5 -m "Hello" -s "Captain Agent-4"

# Broadcast to all agents
python -m src.services.messaging_cli --bulk -m "System update" -s "Captain Agent-4"

# Bulk onboarding (friendly style)
python -m src.services.messaging_cli --onboarding --onboarding-style friendly

# Wrapup message
python -m src.services.messaging_cli --wrapup
```

### Flags and Behavior
- **--message/-m**: required for send unless using utility commands.
- **--sender/-s**: default `Captain Agent-4`.
- **--agent/-a**: target agent; mutually exclusive with `--bulk`.
- **--bulk**: send to all in order `Agent-1..Agent-8`, with **Agent-4 last**.
- **--type/-t**: `text|broadcast|onboarding`.
- **--priority/-p**: `normal|urgent`.
- **--high-priority**: overrides `--priority` to `urgent`.
- **--mode**: `pyautogui|inbox` (default `pyautogui`).
- **--no-paste**: disable clipboard paste; types line-by-line with `Shift+Enter` between lines.
- **--new-tab-method**: `ctrl_t|ctrl_n` for PyAutoGUI; creates new tab/window before sending.
- **Utilities**: `--list-agents`, `--coordinates`, `--history`.
- **Contracts**: `--get-next-task` (requires `--agent`), `--check-status`.
- **Onboarding**: `--onboarding` (bulk), `--onboard` (single), `--onboarding-style friendly|professional`.
- **Wrapup**: `--wrapup`.

### Order of Operations (delivery)
- `pyautogui` mode:
  1. Move to agent coordinates and focus (click).
  2. Clear input (Ctrl+A, Delete).
  3. Create new tab/window per `--new-tab-method`.
  4. Paste content (clipboard) unless `--no-paste`; else type with formatting.
  5. Press Enter to send.
- `inbox` mode:
  - Write Markdown file with header fields to agent inbox; logs path on success.

### Validation
- Message validation rules: `src/core/validation/rules/message.yaml`
  - structure, required fields, enum values, and content formatting checks.

## Discord Devlog System
- SSOT for team communication; updates post to Discord.
- Usage guidance is documented in onboarding:
  - `docs/AGENT_ONBOARDING_GUIDE.md` (Devlog requirements and commands)
- Typical usage:
```
# Check devlog system status
python -m src.core.devlog_cli status

# Create a devlog entry (title + content)
python scripts/devlog.py "Title" "Content"
```
- Policies:
  - **Mandatory**: Use devlog for all project updates.
  - **Prohibited**: Manual Discord posts, email/chat bypass of devlog.
  - Identify the agent and categorize content properly.

## Contract System
- Integrated via messaging CLI utilities and onboarding workflow.
- Claim tasks:
```
# Get next task for an agent
python -m src.services.messaging_cli --agent Agent-7 --get-next-task

# Check status across agents and availability
python -m src.services.messaging_cli --check-status
```
- Assignment logic lives in `src/services/messaging_cli.py` under `--get-next-task`.
- Validation rules: `src/core/validation/rules/contract.yaml`.
- Categories (docs): Coordination Enhancement, Phase Transition Optimization,
  Testing Framework Enhancement, Strategic Oversight, Refactoring Tool Preparation,
  Performance Optimization.
- Workflow (docs): Get next task → Execute → Report to Captain (Agent-4) → Complete → Auto-continue.

## References
- Messaging core: `src/services/messaging_core.py`
- Messaging delivery: `src/services/messaging_pyautogui.py`
- Messaging models: `src/services/models/messaging_models.py`
- Messaging CLI: `src/services/messaging_cli.py`
- Message rules: `src/core/validation/rules/message.yaml`
- Contract rules: `src/core/validation/rules/contract.yaml`
- Onboarding doc: `docs/AGENT_ONBOARDING_GUIDE.md`

## Examples
- TypeScript functional React component (prefer functional components):
  ```tsx
  import React from 'react';

  type UserCardProps = {
    user_id: string; // snake_case for API fields
    display_name: string;
  };

  export const UserCard: React.FC<UserCardProps> = ({ user_id, display_name }) => {
    return (
      <div data-user-id={user_id}>
        <strong>{display_name}</strong>
      </div>
    );
  };
  ```

- Jest unit test (clear describe/it, mock externals):
  ```ts
  import { fetch_user_profile } from './api';

  jest.mock('./api');

  describe('user profile loader', () => {
    it('returns profile when API succeeds', async () => {
      (fetch_user_profile as jest.Mock).mockResolvedValue({ user_id: 'u_1' });
      const profile = await fetch_user_profile('u_1');
      expect(profile.user_id).toBe('u_1');
    });
  });
  ```

- Repository pattern (data access isolated):
  ```ts
  export interface UserRepository {
    get_by_id(user_id: string): Promise<User>;
  }

  export class UserService {
    constructor(private readonly repo: UserRepository) {}
    async get_profile(user_id: string) {
      return this.repo.get_by_id(user_id);
    }
  }
  ```

## Cross-References
- Onboarding flow, messaging, and contract commands: see
[docs/AGENT_ONBOARDING_GUIDE.md](docs/AGENT_ONBOARDING_GUIDE.md)

---

## Agent Onboarding & Status Tracking

- Identity and Captain:
  - Captain is `Agent-4` — Strategic Oversight & Emergency Intervention Manager (SSOT).
- Initialize and verify status:
  ```bash
  python -m src.services.messaging_cli --check-status
  ```
- Claim first contract for your agent:
  ```bash
  python -m src.services.messaging_cli --agent Agent-7 --get-next-task
  ```
- Acknowledge Captain (inbox/messaging):
  ```bash
  python -m src.services.messaging_cli \
    --agent Agent-4 \
    --message "Agent-7: Onboarding completed, ready for task assignment"
  ```
- Required status updates (update `agent_workspaces/<Agent-X>/status.json`):
  - When starting or completing a task
  - When responding to messages
  - When receiving Captain prompts
  - On any significant progress (include timestamp)
- Status file structure (authoritative fields):
  ```json
  {
    "agent_id": "{agent_id}",
    "agent_name": "{role}",
    "status": "ACTIVE_AGENT_MODE",
    "current_phase": "TASK_EXECUTION",
    "last_updated": "YYYY-MM-DD HH:MM:SS",
    "current_mission": "Current mission description",
    "mission_priority": "HIGH/MEDIUM/LOW",
    "current_tasks": ["Task 1"],
    "completed_tasks": ["Done 1"],
    "achievements": ["Milestone"],
    "next_actions": ["Next step"]
  }
  ```

## Agent Cycle & Communication Protocols

### 🚨 FUNDAMENTAL OPERATIONAL PRINCIPLE: CYCLE-BASED METHODOLOGY
**TIME-BASED DEADLINES ARE PROHIBITED. ALL OPERATIONS ARE CYCLE-BASED.**

- **Cycle Definition**: One Captain prompt + One Agent response = One complete cycle
- **Response Protocol**: Agent acknowledgment/response = Cycle completion
- **Escalation Criteria**: Only escalate if agent fails to respond within one cycle
- **Timeline Format**: "Complete within X cycles" (NEVER time-based deadlines)
- **Progress Format**: "Cycle X complete: [achievements]" (NEVER time-based progress)
- **Maintain momentum for 8x efficiency**: Each cycle should produce measurable progress
- **Always check your inbox first**: `agent_workspaces/<Agent-X>/inbox/`
- Useful utilities:
  ```bash
  python -m src.services.messaging_cli --list-agents
  python -m src.services.messaging_cli --coordinates
  python -m src.services.messaging_cli --history
  ```

## Messaging Delivery Notes (observed)

- Default delivery mode is `pyautogui`; `--mode inbox` writes Markdown to agent inboxes.
- New tab method: `--new-tab-method ctrl_t|ctrl_n` (for PyAutoGUI runs).
- Clipboard vs typing: use paste by default; `--no-paste` types with formatting.
- Bulk onboarding auto-includes protocol tags and metadata.

## Contract Categories & Current Mapping (SSOT)

- Contracts are assigned via `--get-next-task` in `src/services/messaging_cli.py`.
- Current category/points by agent:
  - Agent-1: Integration & Core Systems — 600 pts
  - Agent-2: Architecture & Design — 550 pts
  - Agent-3: Infrastructure & DevOps — 575 pts
  - Agent-5: Business Intelligence — 425 pts
  - Agent-6: Coordination & Communication — 500 pts
  - Agent-7: Web Development — 685 pts
  - Agent-8: SSOT & System Integration — 650 pts
- Note on titles: if labels differ across outputs, prefer
  `docs/AGENT_ONBOARDING_GUIDE.md` and `src/services/messaging_cli.py` as SSOT.

## V2 Compliance Enforcement Checklist - UPDATED 2025-01-27

### 🎯 **PRIMARY FOCUS: CLEAN, TESTED, CLASS-BASED, REUSABLE, SCALABLE CODE**

#### **Architecture Excellence**
- ✅ Follow existing architecture; avoid introducing new patterns prematurely
- ✅ Maintain SSOT across configuration, constants, schemas, and docs
- ✅ Encapsulate complex domain logic with object-oriented design
- ✅ Keep functions small, cohesive, and single-purpose
- ✅ Prefer dependency injection for shared utilities; avoid circular dependencies

#### **File Size Management (Updated Thresholds)**
- 🚨 **CRITICAL**: Eliminate files >600 lines immediately
- ⚠️ **MAJOR**: Refactor files 400-600 lines strategically
- ✅ **GUIDELINE**: Keep files ≤400 lines while focusing on clean, tested, reusable, scalable code

#### **Code Quality Standards**
- ✅ **Testing**: Unit tests for all new features, Jest naming clarity, mock externals
- ✅ **Coverage**: Maintain ≥85% test coverage across all modules
- ✅ **Documentation**: JSDoc for public APIs, examples for new utilities
- ✅ **Maintainability**: Update README and changelog for notable changes
- ✅ **Error Handling**: Comprehensive exception handling and logging
- ✅ **Type Safety**: Full type annotations in Python, strict TypeScript

#### **Scalability & Performance**
- ✅ **Modular Design**: Clear boundaries between modules and components
- ✅ **Reusability**: Design components for cross-project usage
- ✅ **Performance**: Optimize for high-frequency operations where needed
- ✅ **Scalability**: Architecture supports horizontal and vertical scaling