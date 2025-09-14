# Messaging System API Specifications

Authoritative reference for interacting with the unified messaging system.

## Core Components

- `src/services/messaging_core.py` – message creation, validation, delivery.
- `src/services/messaging_cli.py` – CLI interface for sending and utility commands.
- Delivery backends:
  - `src/services/messaging_pyautogui.py`
  - `agent_workspaces/<Agent-X>/inbox` for inbox mode.
- Models: `src/services/models/messaging_models.py` defines enums:
  - `UnifiedMessageType`: text, broadcast, onboarding, agent_to_agent, system_to_agent, human_to_agent.
  - `UnifiedMessagePriority`: normal, urgent.
  - `UnifiedMessageTag`: captain, onboarding, wrapup.
  - `UnifiedSenderType` and `UnifiedRecipientType`: agent, system, human.

## Message Structure

```python
from src.services.models.messaging_models import UnifiedMessage
UnifiedMessage(
    content="Hello",
    sender="Captain Agent-4",
    recipient="Agent-1",
    message_type="text",
    priority="normal",
)
```

## CLI Usage

The CLI is the primary API surface.

```bash
python -m src.services.messaging_cli --agent Agent-7 --message "Hello"
python -m src.services.messaging_cli --bulk --wrapup
python -m src.services.messaging_cli --list-agents
```

Flags:

- `--agent/-a` or `--bulk`
- `--message/-m` (required unless using utility commands)
- `--sender/-s` (default `Captain Agent-4`)
- `--type/-t` (`text|broadcast|onboarding`)
- `--priority/-p` (`normal|urgent` or `--high-priority`)
- `--mode` (`pyautogui|inbox`)
- Utilities: `--coordinates`, `--history`, `--check-status`,
  `--get-next-task` (requires `--agent`)

## Error Handling

- Validation performed via `src/core/simple_validation_system.py`.
- Errors raise structured exceptions with helpful messages.

## Cross-References

- Deployment instructions: [MESSAGING_DEPLOYMENT_STRATEGY.md](MESSAGING_DEPLOYMENT_STRATEGY.md)
- Testing approach: [MESSAGING_TEST_PLAN.md](MESSAGING_TEST_PLAN.md)
- Channel rules: [CHANNEL_RESTRICTION_FEATURES.md](CHANNEL_RESTRICTION_FEATURES.md)
- Enhanced types: [MESSAGING_SYSTEM_V2_ENHANCED_TYPES.md](MESSAGING_SYSTEM_V2_ENHANCED_TYPES.md)

This document is the single source of truth for messaging API behavior.
