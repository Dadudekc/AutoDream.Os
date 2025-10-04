# Discord Devlog Setup Guide
==========================

## Issue Diagnosis
The Discord devlog system has two main issues:
1. **Routing Issue**: All devlogs routing to 'dreamscape devlog' instead of proper Discord channels
2. **Missing Configuration**: No Discord webhook URL configured in environment variables (.env file missing)
3. **Spam Filter Active**: The system has anti-spam filtering that blocks certain message patterns

## Current Status
- ✅ Discord devlog service initialized
- ✅ Spam filtering system active (working as designed)
- ❌ No Discord webhook URL configured
- ❌ Messages being filtered due to spam detection

## Solution Options

### Option 1: Configure Discord Webhook (Recommended)
1. Create a Discord webhook in your server:
   - Go to Server Settings → Integrations → Webhooks
   - Create new webhook
   - Copy the webhook URL

2. Create .env file:
   ```bash
   # Copy the template
   cp discord_env_template.txt .env

   # Edit .env file and add your webhook URL
   DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_URL
   ```

3. Or set environment variable directly:
   ```bash
   export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/YOUR_WEBHOOK_URL"
   ```

3. Test the connection:
   ```bash
   python src/services/discord_devlog_bypass.py "Test message" captain
   ```

### Option 2: Use Bypass Service (Temporary)
The bypass service removes spam-filtered content:
```bash
python src/services/discord_devlog_bypass.py "Your message here" captain
```

### Option 3: Disable Spam Filtering (Not Recommended)
Edit `src/services/discord_devlog_service.py` line 317:
```python
# Comment out the spam filter
# if "📝 DISCORD DEVLOG REMINDER:" in content and "devlogs/ directory" in content:
#     return None  # Suppress automated Discord reminder spam
```

## Spam Filter Rules
The current spam filter blocks:
1. **Automated Reminders**: Messages containing "📝 DISCORD DEVLOG REMINDER:"
2. **Coordination Theater**: Circular acknowledgment patterns
3. **Ultimate Loops**: Messages with 3+ "ultimate" references

## Environment Variables Needed
```bash
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_URL
DISCORD_BOT_TOKEN=your_bot_token_here
DISCORD_CHANNEL_ID=your_channel_id_here
DISCORD_GUILD_ID=your_guild_id_here
```

## Testing
1. Test webhook connection:
   ```bash
   python src/services/discord_devlog_bypass.py "Test message" captain
   ```

2. Test devlog service:
   ```bash
   python src/services/agent_devlog_posting.py --agent captain --action "Test devlog entry"
   ```

## Current Workaround
The system is working correctly - the spam filter is preventing spam, but you need to configure a Discord webhook to see messages. Local file devlogs are still being created successfully.
