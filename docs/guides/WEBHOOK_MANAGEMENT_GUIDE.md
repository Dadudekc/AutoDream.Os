# 🔗 Discord Webhook Management Guide

## 🎯 **What This Does**

Enables agents to **programmatically create and manage Discord webhooks** for full automation control. Agents can now:

- ✅ Create webhooks for any channel
- ✅ List all webhooks in the server
- ✅ Test webhooks with messages
- ✅ Get webhook details and URLs
- ✅ Delete webhooks when no longer needed
- ✅ Save webhooks to config for automated use

---

## 🚀 **Quick Start**

### **1. Enable Webhook Management**

Add to your Discord bot (if not already running):

```bash
python run_unified_discord_bot.py
```

### **2. Create a Webhook**

In Discord, use the bot command:

```bash
!create_webhook #devlogs Agent-8-Devlog-Webhook
```

This will:
- Create the webhook in the #devlogs channel
- Save it to `config/discord_webhooks.json`
- DM you the webhook URL (keep it private!)

### **3. Use the Webhook**

From Python code:

```python
from src.services.publishers.discord_publisher import DiscordDevlogPublisher

# Load webhook from config
import json
with open('config/discord_webhooks.json') as f:
    config = json.load(f)
    webhook_url = config['devlogs_webhook']['webhook_url']

# Use webhook
publisher = DiscordDevlogPublisher(webhook_url)
publisher.publish_devlog(
    agent_id="Agent-8",
    title="My Update",
    content="Content here..."
)
```

---

## 📋 **Discord Bot Commands**

### **Create Webhook**
```bash
!create_webhook <#channel> <webhook_name>

Examples:
  !create_webhook #devlogs Agent-8-Devlog-Webhook
  !create_webhook #status Status-Update-Webhook
  !create_webhook #contracts Contract-Notifier
```

**What it does:**
- Creates webhook in specified channel
- Saves to config/discord_webhooks.json
- DMs you the webhook URL securely
- Assigns a config key for easy reference

---

### **List Webhooks**
```bash
!list_webhooks              # List all server webhooks
!list_webhooks #channel     # List webhooks for specific channel

Examples:
  !list_webhooks              # All webhooks
  !list_webhooks #devlogs    # Just #devlogs webhooks
```

**Output:**
- Shows webhook names
- Shows which channels they're in
- Shows who created them
- Shows webhook IDs

---

### **Test Webhook**
```bash
!test_webhook <webhook_id>

Example:
  !test_webhook 1234567890123456789
```

**What it does:**
- Sends a test message through the webhook
- Confirms webhook is working
- Shows in the webhook's channel

---

### **Get Webhook Info**
```bash
!webhook_info <webhook_id>

Example:
  !webhook_info 1234567890123456789
```

**What it shows:**
- Webhook name and ID
- Which channel it posts to
- Who created it
- DMs you the webhook URL

---

### **Delete Webhook**
```bash
!delete_webhook <webhook_id>

Example:
  !delete_webhook 1234567890123456789
```

**What it does:**
- Shows confirmation dialog
- Deletes webhook if confirmed
- Removes from config file
- Logs the deletion

---

## 🛠️ **Agent Toolbelt Integration**

Agents can use webhook tools programmatically:

### **From Agent Toolbelt**

```python
from tools_v2 import AgentToolbelt

toolbelt = AgentToolbelt()

# List webhooks from config
result = toolbelt.execute('list_discord_webhooks')
print(result['webhooks'])

# Save webhook to .env
result = toolbelt.execute('save_discord_webhook', 
    webhook_url='https://discord.com/api/webhooks/...',
    config_key='DISCORD_DEVLOG_WEBHOOK'
)

# Test webhook
result = toolbelt.execute('test_discord_webhook',
    config_key='DISCORD_DEVLOG_WEBHOOK',
    test_message='Hello from agent!'
)
```

---

## 📊 **Webhook Configuration**

Webhooks are saved to `config/discord_webhooks.json`:

```json
{
  "devlogs_webhook": {
    "webhook_url": "https://discord.com/api/webhooks/...",
    "webhook_id": "1234567890",
    "channel_id": "1375424568969265152",
    "channel_name": "devlogs",
    "webhook_name": "Agent-8-Devlog-Webhook",
    "created_by": "Commander#1234",
    "created_at": "2025-10-15T12:00:00Z"
  },
  "status_webhook": {
    "webhook_url": "https://discord.com/api/webhooks/...",
    "webhook_id": "9876543210",
    "channel_id": "1234567890",
    "channel_name": "status",
    "webhook_name": "Status-Update-Webhook",
    "created_by": "Commander#1234",
    "created_at": "2025-10-15T12:05:00Z"
  }
}
```

---

## 🔐 **Security Best Practices**

### **⚠️ Webhook URLs are Secrets!**

Webhook URLs are like passwords - anyone with the URL can post to your channel!

**DO:**
- ✅ Keep webhook URLs in `.env` or config files (gitignored)
- ✅ Use DMs for sharing webhook URLs
- ✅ Delete unused webhooks
- ✅ Restrict bot command permissions to admins

**DON'T:**
- ❌ Share webhook URLs in public channels
- ❌ Commit webhook URLs to git
- ❌ Post webhook URLs in Discord messages
- ❌ Leave unused webhooks active

---

## 🎯 **Common Use Cases**

### **1. Agent Devlog Posting**

```bash
# Create webhook
!create_webhook #devlogs Agent-8-Devlog-Webhook

# Agent uses it
python tools/devlog_auto_poster.py \
  --agent Agent-8 \
  --title "My Update" \
  --webhook-config devlogs_webhook
```

---

### **2. Contract Notifications**

```bash
# Create webhook
!create_webhook #contracts Contract-Notifier

# Set in .env
DISCORD_WEBHOOK_URL=<webhook_url>

# Auto-notifies on contract events
python -m src.services.messaging_cli --agent Agent-7 --get-next-task
```

---

### **3. Status Dashboard Updates**

```bash
# Create webhook
!create_webhook #status Status-Dashboard

# Auto-post status updates
python tools/discord_status_dashboard.py
```

---

### **4. Per-Agent Channels**

```bash
# Create webhooks for each agent
!create_webhook #agent-1 Agent-1-Webhook
!create_webhook #agent-2 Agent-2-Webhook
!create_webhook #agent-3 Agent-3-Webhook
# ... etc

# Agents post to their own channels automatically
```

---

## 🔧 **Integration with Existing Systems**

### **Update Contract Notifications**

```python
# src/discord_commander/contract_notifications.py
from pathlib import Path
import json

# Load webhook from config instead of .env
config_path = Path("config/discord_webhooks.json")
with open(config_path) as f:
    config = json.load(f)
    webhook_url = config['contracts_webhook']['webhook_url']

notifier = ContractNotifier(webhook_url=webhook_url)
```

---

### **Update Devlog Publisher**

```python
# tools/devlog_auto_poster.py
import json

# Load webhook by key
def load_webhook_by_key(key: str) -> str:
    config_path = Path("config/discord_webhooks.json")
    with open(config_path) as f:
        config = json.load(f)
        return config[key]['webhook_url']

webhook_url = load_webhook_by_key('devlogs_webhook')
```

---

## 📈 **Advanced Usage**

### **Multi-Channel Posting**

```python
# Post to different channels based on content
webhooks = {
    'devlogs': 'https://discord.com/api/webhooks/...',
    'status': 'https://discord.com/api/webhooks/...',
    'contracts': 'https://discord.com/api/webhooks/...',
}

def post_to_channel(channel: str, content: str):
    webhook_url = webhooks[channel]
    publisher = DiscordDevlogPublisher(webhook_url)
    publisher.publish_devlog(...)
```

---

### **Webhook Rotation**

```python
# Create backup webhooks for redundancy
!create_webhook #devlogs Primary-Webhook
!create_webhook #devlogs Backup-Webhook

# Use primary, fallback to backup on failure
def post_with_fallback(content: str):
    try:
        primary_publisher.publish_devlog(content)
    except:
        backup_publisher.publish_devlog(content)
```

---

## 🐛 **Troubleshooting**

### **"I don't have permission to create webhooks"**

**Solution:** Bot needs **Manage Webhooks** permission.
1. Go to Server Settings → Roles
2. Find bot role → Edit Permissions
3. Enable **Manage Webhooks**

---

### **"Couldn't DM you the webhook URL"**

**Solution:** Enable DMs from server members.
1. Right-click server name → Privacy Settings
2. Enable **Allow direct messages from server members**
3. Or check `config/discord_webhooks.json` for the URL

---

### **"Webhook validation failed"**

**Solutions:**
1. Check webhook URL format: `https://discord.com/api/webhooks/...`
2. Verify webhook hasn't been deleted in Discord
3. Test with `!test_webhook <webhook_id>`
4. Recreate webhook if needed

---

## 📚 **Related Documentation**

- **Discord Publisher:** `src/services/publishers/discord_publisher.py`
- **Devlog Posting:** `docs/CONTRACT_NOTIFICATIONS_USAGE_GUIDE.md`
- **Bot Setup:** `docs/guides/ADMIN_COMMANDER_SETUP.md`
- **Agent Toolbelt:** `AGENT_TOOLS_DOCUMENTATION.md`

---

## ✅ **Summary**

With webhook management, agents can now:

1. **Create webhooks** via Discord bot commands
2. **Store webhooks** in config for automated use
3. **Test webhooks** to verify functionality
4. **Manage webhooks** (list, info, delete)
5. **Use webhooks** from Python code automatically

This enables **full Discord automation** without manual webhook setup! 🚀

