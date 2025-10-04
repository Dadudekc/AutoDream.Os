# Discord Channel Routing Fix
============================

## Issue Diagnosis
Discord devlogs are routing to "dreamscape devlog" channel instead of proper Agent-7 channel (ID: 1415916665283022980).

## Root Cause
The webhook URL is configured to point to the wrong Discord channel. Webhooks are tied to specific channels and cannot be redirected.

## Solution Options

### Option 1: Create New Webhook for Agent-7 Channel (Recommended)
1. Go to Discord Server Settings → Integrations → Webhooks
2. Create new webhook for Agent-7 channel (ID: 1415916665283022980)
3. Copy the new webhook URL
4. Update environment variable:
   ```bash
   DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/NEW_AGENT7_WEBHOOK_URL
   ```

### Option 2: Use Agent-Specific Webhook Configuration
1. Create webhook for Agent-7 channel
2. Set agent-specific webhook in .env:
   ```bash
   DISCORD_WEBHOOK_AGENT_7=https://discord.com/api/webhooks/AGENT7_WEBHOOK_URL
   ```

### Option 3: Update Default Channel ID
1. Set the default channel to Agent-7 channel:
   ```bash
   DISCORD_CHANNEL_ID=1415916665283022980
   ```

## Agent-7 Channel Information
- **Channel ID**: 1415916665283022980
- **Current Issue**: Webhook pointing to "dreamscape devlog" channel
- **Solution**: Create new webhook specifically for Agent-7 channel

## Testing
After fixing the webhook URL:
```bash
python src/services/discord_devlog_bypass.py "Test message for Agent-7 channel" captain
```

## Verification
Check Discord to confirm messages are now routing to Agent-7 channel instead of dreamscape devlog.

## Environment Variables Needed
```bash
# Primary webhook (should point to Agent-7 channel)
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/AGENT7_WEBHOOK_URL

# Or use agent-specific webhook
DISCORD_WEBHOOK_AGENT_7=https://discord.com/api/webhooks/AGENT7_WEBHOOK_URL

# Default channel ID
DISCORD_CHANNEL_ID=1415916665283022980
```

## Current Status
- ❌ Webhook pointing to wrong channel (dreamscape devlog)
- ✅ Agent-7 channel ID identified (1415916665283022980)
- ⚠️ Need to create new webhook for correct channel
