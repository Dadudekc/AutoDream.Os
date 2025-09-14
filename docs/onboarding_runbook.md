# Hard Onboarding UI Sequence - Operator Runbook

## Overview
Hard onboarding uses PyAutoGUI to physically interact with the Cursor IDE, sending role-specific messages to agents through their coordinate positions.

## Prerequisites
- `cursor_agent_coords.json` exists with agent coordinates
- PyAutoGUI and Pyperclip installed
- Cursor IDE running with agents positioned at specified coordinates

## Usage

### Basic Hard Onboarding
```bash
python src/services/consolidated_messaging_service.py \
  --hard-onboarding \
  --agents "Agent-3" \
  --onboarding-mode cleanup \
  --assign-roles "Agent-3:CLEANUP_CORE" \
  --use-ui
```

### With Custom Settings
```bash
python src/services/consolidated_messaging_service.py \
  --hard-onboarding \
  --agents "Agent-5" \
  --onboarding-mode cleanup \
  --assign-roles "Agent-5:CLEANUP_SERVICES" \
  --use-ui \
  --ui-retries 3 \
  --ui-tolerance 200
```

### Dry Run (Safe Testing)
```bash
python src/services/consolidated_messaging_service.py \
  --hard-onboarding \
  --agents "Agent-3" \
  --assign-roles "Agent-3:CLEANUP_CORE" \
  --use-ui \
  --dry-run
```

## Sequence Details

1. **Click Chat Input**: Moves to `chat_input_coordinates` and clicks
2. **New Chat**: Presses `Ctrl+N` to open new chat window
3. **Click Onboarding Input**: Moves to `onboarding_input_coordinates` and clicks
4. **Type Message**: Pastes or types the role-specific onboarding message
5. **Send**: Presses `Enter` to send the message

## Coordinate Format

Expected in `cursor_agent_coords.json`:
```json
{
  "agents": {
    "Agent-3": {
      "chat_input_coordinates": [-1269, 481],
      "onboarding_coordinates": [-1265, 171],
      "active": true
    }
  }
}
```

## Troubleshooting

### PyAutoGUI Not Available
```
❌ UI mode unavailable: pyautogui unavailable
```
**Fix**: `pip install pyautogui pyperclip`

### Invalid Coordinates
```
❌ Invalid coords; expected chat_input + onboarding_input
```
**Fix**: Check `cursor_agent_coords.json` format

### UI Automation Fails
- Increase `--ui-tolerance` (default: 200ms)
- Increase `--ui-retries` (default: 2)
- Use `--dry-run` to test sequence without UI interaction

## Multi-Agent Support

Onboard multiple agents in one command:
```bash
python src/services/consolidated_messaging_service.py \
  --hard-onboarding \
  --agents "Agent-3,Agent-5,Agent-6" \
  --onboarding-mode cleanup \
  --assign-roles "Agent-3:CLEANUP_CORE,Agent-5:CLEANUP_SERVICES,Agent-6:SOLID" \
  --use-ui
```
