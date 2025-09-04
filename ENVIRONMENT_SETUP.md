# Environment Setup - Agent Cellphone V2

## 🔒 Security Notice
This project uses sensitive tokens and API keys that must be kept secure. Never commit these to git!

## 📋 Required Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
# Discord Configuration - KEEP SECRET
DISCORD_WEBHOOK_URL=your_discord_webhook_url_here
DISCORD_BOT_TOKEN=your_bot_token_here
DISCORD_CHANNEL_ID=your_channel_id_here

# OpenAI Configuration (if used)
OPENAI_API_KEY=your_openai_api_key_here

# Other sensitive configurations
DATABASE_URL=your_database_url_here
API_SECRET_KEY=your_api_secret_key_here

# Environment settings
ENVIRONMENT=development
DEBUG=true
```

## 🚀 Setup Instructions

1. **Copy the example config:**
   ```bash
   cp config/devlog_config.example.json config/devlog_config.json
   ```

2. **Create your .env file:**
   ```bash
   # Create .env file with your actual values
   echo "DISCORD_WEBHOOK_URL=your_webhook_url" > .env
   echo "DISCORD_BOT_TOKEN=your_bot_token" >> .env
   ```

3. **Update Discord configuration:**
   - Edit `config/devlog_config.json`
   - Set `enable_discord: true`
   - The system will automatically use the environment variable

## 🔧 Discord Webhook Setup

1. Go to your Discord server settings
2. Navigate to Integrations > Webhooks
3. Create a new webhook or copy existing one
4. Copy the webhook URL
5. Add it to your `.env` file

## 🛡️ Security Best Practices

- ✅ Never commit `.env` files
- ✅ Use environment variables for all secrets
- ✅ Use `.env.example` for documentation
- ✅ Keep tokens in secure password manager
- ❌ Never hardcode tokens in source code
- ❌ Never commit actual webhook URLs
- ❌ Never share tokens in chat/email

## 🔍 Verification

Run this to verify your setup:
```bash
python -c "import os; print('Discord configured:', bool(os.getenv('DISCORD_WEBHOOK_URL')))"
```

## 🚨 Security Incident Response

If tokens are accidentally committed:
1. Immediately revoke the exposed tokens
2. Generate new tokens
3. Update your `.env` file
4. Remove tokens from git history using git-filter-repo
5. Force push clean history

## 📞 Support

If you need help with environment setup, contact the Captain (Agent-4).

## 🔄 Git History Cleanup

This repository has been cleaned using `git-filter-repo` to remove all Discord tokens from git history. All previous instances of hardcoded tokens have been replaced with `***REMOVED_DISCORD_TOKEN***` placeholders.