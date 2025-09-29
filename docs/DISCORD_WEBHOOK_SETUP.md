# Discord Webhook Setup Guide

## 🎯 **Bot-Free Discord Communication System**

This system allows agents to post single-line events directly to Discord channels using webhooks, eliminating dependency on the Discord bot being online.

## 📋 **Setup Instructions**

### 1. Bot Permissions

Ensure your Discord bot has these permissions in each agent channel:
- **Manage Webhooks** (create/update/delete webhooks)
- **View Channel**
- (Optional) **Manage Messages** for cleanup

### 2. Admin Setup

Use the new admin slash commands to provision webhooks:

```bash
# Create webhook for Agent-1
/provision-webhook agent:Agent-1 channel:#agent-1

# Test the webhook
/test-webhook agent:Agent-1

# List all webhooks
/list-webhooks

# Rotate webhook (security)
/rotate-webhook agent:Agent-1

# Revoke webhook
/revoke-webhook agent:Agent-1
```

### 3. Automatic Webhook Management

The system automatically:
- **Stores URLs Securely**: In `C:\ProgramData\V2_SWARM\webhooks.json`
- **Validates Permissions**: Checks bot permissions before creating
- **Masks Tokens**: Only shows first 6 characters for security
- **Handles Errors**: Comprehensive error handling and logging

### 3. Test the System

```bash
# Test cycle completion
python tools/emit_event.py --agent Agent-8 --type CYCLE_DONE --summary "Processed inbox(5), claimed 1 task" --next "Continue autonomous ops"

# Test blocker reporting
python tools/emit_event.py --agent Agent-8 --type BLOCKER --reason "No webhook" --need "Set AGENT_8_WEBHOOK" --severity high

# Test SSOT validation
python tools/emit_event.py --agent Agent-8 --type SSOT --scope "repo=Agent_Cellphone_V2" --passed

# Test integration scan
python tools/emit_event.py --agent Agent-8 --type INTEGRATION --systems "discord,webhook" --depth 2 --result "All systems operational"
```

## 📊 **Event Format**

All events follow a pipe-delimited format for easy parsing:

- **CYCLE_DONE**: `CYCLE_DONE|Agent-8|summary|next_intent|ts=2025-09-27T23:45:00Z`
- **BLOCKER**: `BLOCKER|Agent-8|reason|need|severity=high|ts=2025-09-27T23:45:00Z`
- **SSOT_VALIDATION**: `SSOT_VALIDATION|Agent-8|scope|pass|notes=notes|ts=2025-09-27T23:45:00Z`
- **INTEGRATION_SCAN**: `INTEGRATION_SCAN|Agent-8|systems=discord,webhook|depth=2|result=success|ts=2025-09-27T23:45:00Z`

## 🔧 **Integration with Autonomous Workflow**

To integrate with your autonomous workflow, add this to your `run_autonomous_cycle()` method:

```python
from src.services.discord_line_emitter import DiscordLineEmitter
from src.services.event_format import cycle_done, blocker

# After cycle completion
emitter = DiscordLineEmitter()
summary = f"Processed inbox({cycle_results['messages_processed']}), tasks({cycle_results['tasks_processed']})"
next_intent = "Continue autonomous ops"
line = cycle_done(self.agent_id, summary, next_intent)
await emitter.emit_event(self.agent_id, line)

# On blocker
line = blocker(self.agent_id, reason="Missing API key", need="Set AGENT_8_WEBHOOK", severity="high")
await emitter.emit_event(self.agent_id, line)
```

## ✅ **Benefits**

- **No Bot Dependency**: Works even when Discord bot is offline
- **Real-time Updates**: Instant visibility into agent activities
- **Structured Format**: Easy to parse and analyze
- **Reliable**: Built-in retry logic and rate limit handling
- **Simple**: Single-line events, no complex interactions

## 🚀 **Status**

✅ DiscordLineEmitter created
✅ Event formatters implemented
✅ CLI tool functional
✅ UTF-8 environment configured
✅ SecretStore for secure webhook storage
✅ DiscordWebhookProvisioner for webhook management
✅ Admin slash commands for webhook setup
✅ Bot integration complete
✅ Ready for production use
