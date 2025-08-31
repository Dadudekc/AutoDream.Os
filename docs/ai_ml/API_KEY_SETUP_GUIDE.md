# 🔑 API Key Setup Guide
**Agent-2: AI & ML Framework Integration**
**TDD Integration Project - Agent_Cellphone_V2_Repository**

This guide will walk you through setting up API keys and configuring your AI/ML development environment.

## 📋 Prerequisites

Before you begin, ensure you have:
- ✅ Python 3.8+ installed
- ✅ Access to the Agent_Cellphone_V2_Repository
- ✅ OpenAI API key (optional but recommended)
- ✅ Anthropic Claude API key (optional but recommended)

## 🚀 Quick Setup

### Option 1: Interactive Configuration (Recommended)

Run the configuration script to set up everything interactively:

```bash
python configure_ai_ml_environment.py
```

This will:
- 🔧 Set up environment variables
- 📁 Create directory structure
- 🔑 Configure API keys interactively
- ✅ Validate your configuration
- 📊 Generate a detailed report

### Option 2: Manual Configuration

If you prefer to configure manually, follow these steps:

#### Step 1: Set Environment Variables

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="your_openai_api_key_here"
$env:ANTHROPIC_API_KEY="your_anthropic_api_key_here"
$env:OPENAI_ORGANIZATION="your_openai_organization_id_here"
```

**Windows (Command Prompt):**
```cmd
set OPENAI_API_KEY=your_openai_api_key_here
set ANTHROPIC_API_KEY=your_anthropic_api_key_here
set OPENAI_ORGANIZATION=your_openai_organization_id_here
```

**Linux/macOS:**
```bash
export OPENAI_API_KEY="your_openai_api_key_here"
export ANTHROPIC_API_KEY="your_anthropic_api_key_here"
export OPENAI_ORGANIZATION="your_openai_organization_id_here"
```

#### Step 2: Create Configuration File

Copy the template and add your keys:

```bash
cp config/ai_ml/api_keys.template.json config/ai_ml/api_keys.json
```

Edit `config/ai_ml/api_keys.json` and replace the placeholder values with your actual API keys.

#### Step 3: Install Dependencies

```bash
pip install -r requirements.txt  # Includes optional AI/ML extras
```

## 🔑 Getting API Keys

### OpenAI API Key

1. **Visit**: [OpenAI Platform](https://platform.openai.com/)
2. **Sign up/Login**: Create an account or sign in
3. **API Keys**: Go to "API Keys" section
4. **Create Key**: Click "Create new secret key"
5. **Copy Key**: Copy the generated key (starts with `sk-`)
6. **Organization ID**: Note your organization ID if you have one

### Anthropic Claude API Key

1. **Visit**: [Anthropic Console](https://console.anthropic.com/)
2. **Sign up/Login**: Create an account or sign in
3. **API Keys**: Go to "API Keys" section
4. **Create Key**: Click "Create Key"
5. **Copy Key**: Copy the generated key (starts with `sk-ant-`)

## ⚙️ Configuration Details

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | Yes (for OpenAI features) |
| `ANTHROPIC_API_KEY` | Your Anthropic API key | Yes (for Claude features) |
| `OPENAI_ORGANIZATION` | Your OpenAI organization ID | No (optional) |

### Configuration Files

- **`config/ai_ml/ai_ml_config.json`**: Main configuration (safe to commit)
- **`config/ai_ml/api_keys.template.json`**: Template for API keys (safe to commit)
- **`config/ai_ml/api_keys.json`**: Your actual API keys (NEVER commit!)

### Directory Structure

```
Agent_Cellphone_V2_Repository/
├── config/ai_ml/
│   ├── ai_ml_config.json          # Main configuration
│   ├── api_keys.template.json     # Template (safe)
│   └── api_keys.json              # Your keys (private)
├── src/ai_ml/                     # AI/ML source code
├── logs/                          # Log files
├── models/                        # Model storage
└── saved_models/                  # Saved model files
```

## 🔒 Security Best Practices

### ✅ DO:
- Use environment variables for sensitive data
- Add `api_keys.json` to `.gitignore`
- Use the interactive configuration script
- Validate your configuration regularly

### ❌ DON'T:
- Commit API keys to version control
- Share API keys in public repositories
- Use placeholder values in production
- Store keys in plain text files

## 🧪 Testing Your Configuration

### Test API Key Loading

```python
from src.ai_ml.api_key_manager import get_api_key_manager

# Get the API key manager
manager = get_api_key_manager()

# Check configuration
print(manager.get_configuration_summary())

# Validate keys
validation_results = manager.validate_api_keys()
print("Validation results:", validation_results)
```

### Test OpenAI Integration

```python
from src.ai_ml.integrations import OpenAIIntegration

# Test OpenAI connection
openai_integration = OpenAIIntegration()
if openai_integration.is_configured():
    print("✅ OpenAI integration configured")
else:
    print("❌ OpenAI integration not configured")
```

### Test Anthropic Integration

```python
from src.ai_ml.integrations import AnthropicIntegration

# Test Anthropic connection
anthropic_integration = AnthropicIntegration()
if anthropic_integration.is_configured():
    print("✅ Anthropic integration configured")
else:
    print("❌ Anthropic integration not configured")
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Import Errors
**Problem**: `ModuleNotFoundError` when importing AI/ML modules
**Solution**: Ensure you're in the repository root and Python path is set correctly

#### 2. API Key Not Found
**Problem**: "API key not configured" errors
**Solution**: Check environment variables or run interactive configuration

#### 3. Permission Denied
**Problem**: Cannot create configuration files
**Solution**: Check file permissions and ensure you have write access

#### 4. Dependencies Missing
**Problem**: Package import errors
**Solution**: Run `pip install -r requirements.txt`

### Getting Help

1. **Check Logs**: Look at `ai_ml_configuration.log`
2. **Run Validation**: Use the configuration script to validate
3. **Check Report**: Review `AI_ML_CONFIGURATION_REPORT.md`
4. **Verify Environment**: Ensure all environment variables are set

## 📚 Next Steps

After configuring your API keys:

1. **Run Tests**: `python -m pytest tests/ai_ml/`
2. **Explore Examples**: Check `examples/ai_ml/` directory
3. **Start Development**: Begin using the AI/ML modules
4. **Read Documentation**: Review other AI/ML documentation files

## 🔄 Updating Configuration

To update your configuration:

1. **Modify Environment Variables**: Update system environment variables
2. **Edit Config Files**: Modify `ai_ml_config.json` for non-sensitive settings
3. **Re-run Configuration**: Use the configuration script to validate changes
4. **Test Integration**: Verify that your changes work correctly

---

**Need Help?** Check the configuration report or run the interactive configuration script for assistance.
