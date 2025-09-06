# Onboarding Guide

## Regular Onboarding

### Usage

```bash
python -m src.services.messaging_cli --onboarding
python -m src.services.messaging_cli --onboard --agent Agent-1
```

## Hard Onboarding (Safe, Reversible)

Run a full reset + forced re-onboarding across agents. **High risk** — creates backups and prompts for confirmation.

### Usage

```bash
python -m src.services.messaging_cli --hard-onboarding
python -m src.services.messaging_cli --hard-onboarding --yes
python -m src.services.messaging_cli --hard-onboarding --dry-run
python -m src.services.messaging_cli --hard-onboarding --agents Agent-1,Agent-2 --yes
python -m src.services.messaging_cli --hard-onboarding --timeout 45 --yes
```

### Output (example)

```
🚨 HARD ONBOARDING SEQUENCE INITIATED 🚨
🔄 Resetting all agent statuses...
🗑️ Clearing previous onboardings...
⚡ Sending force onboarding to all agents...
✅ Agent-1: Hard onboarding successful
❌ Agent-2: Hard onboarding failed
📊 Hard onboarding complete: 1/2 agents successfully onboarded
🔒 System synchronized and compliant
```

### Safety Features

* **Creates backup** to `runtime/backups/hard_onboarding/<UTCSTAMP>/`
* **Confirmation prompt** before proceeding (unless `--yes` specified)
* **`--dry-run` mode** performs no writes
* **Rollback capability** if all agents fail
* **Exit codes**: `0=all ok`, `2=partial`, `1=abort/failure`

### Technical Implementation

The hard onboarding sequence includes:

1. **Mouse Navigation**: Click onboarding coordinates
2. **New Tab Creation**: Press Ctrl+N for new tab/window
3. **Position Validation**: Verify mouse at correct coordinates
4. **Auto-correction**: Navigate and retry if position invalid
5. **Message Delivery**: Paste onboarding message and send

### Error Handling

* PyAutoGUI availability check
* Coordinate validation
* Mouse position verification
* Timeout handling
* Rollback on catastrophic failure

### Warning

Hard onboarding is a **high-risk operation** that resets agent states. Always use `--dry-run` first and ensure backups are created. Only use when necessary for system recovery or initial setup.
