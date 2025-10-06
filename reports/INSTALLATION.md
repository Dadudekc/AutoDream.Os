# Installation Guide - Agent Cellphone V2 Repository

**Version**: 2.0.0  
**Last Updated**: 2025-10-05  
**Agent**: Agent-7 (Web Development Expert)  

## 🌟 **Overview**

This guide provides comprehensive installation instructions for the Agent Cellphone V2 Repository. The system supports multiple deployment scenarios including development, staging, and production environments.

## 📋 **Prerequisites**

### **System Requirements**

- **Operating System**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **Python**: 3.8 or higher
- **Node.js**: 16.0 or higher (for web components)
- **Git**: 2.20 or higher
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: Minimum 2GB free disk space

### **Required Software**

```bash
# Check Python version
python --version  # Should be 3.8+

# Check Node.js version
node --version    # Should be 16.0+

# Check Git version
git --version     # Should be 2.20+
```

### **Discord Requirements**

- **Discord Server**: Active Discord server with admin permissions
- **Bot Token**: Valid Discord bot token (72 characters)
- **Guild ID**: Valid Discord guild/server ID (19-digit snowflake format)
- **Permissions**: Bot requires appropriate permissions for agent coordination

## 🚀 **Installation Methods**

### **Method 1: Quick Installation (Recommended)**

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-org/agent-cellphone-v2.git
   cd agent-cellphone-v2
   ```

2. **Run the automated installer**:
   ```bash
   python tools/installer/quick_install.py
   ```

3. **Follow the interactive prompts**:
   - Discord bot token
   - Guild ID
   - Environment selection (development/staging/production)
   - Optional: Custom configuration

### **Method 2: Manual Installation**

#### **Step 1: Clone Repository**

```bash
# Clone the repository
git clone https://github.com/your-org/agent-cellphone-v2.git
cd agent-cellphone-v2

# Checkout the latest stable version
git checkout v2.0.0
```

#### **Step 2: Python Environment Setup**

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip
```

#### **Step 3: Install Dependencies**

```bash
# Install core dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install -r requirements-dev.txt

# Install optional dependencies
pip install -r requirements-optional.txt
```

#### **Step 4: Node.js Dependencies (if using web components)**

```bash
# Install Node.js dependencies
npm install

# Build web components
npm run build
```

## ⚙️ **Configuration**

### **Environment Configuration**

1. **Create environment file**:
   ```bash
   cp .env.example .env
   ```

2. **Edit configuration**:
   ```bash
   # Edit .env file with your settings
   nano .env  # or use your preferred editor
   ```

### **Required Configuration**

```bash
# Discord Configuration (Required)
DISCORD_BOT_TOKEN=your_discord_bot_token_here
DISCORD_GUILD_ID=your_guild_id_here
DISCORD_CHANNEL_ID=your_main_channel_id_here

# Agent Configuration
AGENT_4_COORDINATES=-308,1000
AGENT_5_COORDINATES=652,421
AGENT_6_COORDINATES=1612,419
AGENT_7_COORDINATES=920,851
AGENT_8_COORDINATES=1611,941

# System Configuration
LOG_LEVEL=INFO
ENVIRONMENT=development
```

### **Optional Configuration**

```bash
# Database Configuration (Optional)
DATABASE_URL=sqlite:///data/agent_system.db

# Monitoring Configuration (Optional)
ENABLE_MONITORING=true
METRICS_ENDPOINT=http://localhost:8080/metrics

# Security Configuration (Optional)
ENABLE_SECURITY_SCANNING=true
SECURITY_LOG_LEVEL=WARNING
```

### **Discord Bot Setup**

1. **Create Discord Application**:
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Click "New Application"
   - Name your application (e.g., "Agent Cellphone V2")

2. **Create Bot**:
   - Go to "Bot" section
   - Click "Add Bot"
   - Copy the bot token
   - Enable required intents

3. **Set Permissions**:
   ```
   Send Messages: ✓
   Read Message History: ✓
   Use Slash Commands: ✓
   Manage Messages: ✓
   Embed Links: ✓
   Attach Files: ✓
   Read Message History: ✓
   ```

4. **Get Guild ID**:
   - Enable Developer Mode in Discord
   - Right-click your server name
   - Click "Copy ID"

## 🔧 **System Initialization**

### **Initialize the System**

```bash
# Run system initialization
python tools/setup.py --init

# Validate configuration
python tools/setup.py --validate

# Test Discord connection
python tools/setup.py --test-discord
```

### **Database Setup**

```bash
# Initialize database
python tools/database/setup_database.py

# Run migrations (if applicable)
python tools/database/migrate.py

# Seed initial data
python tools/database/seed_data.py
```

### **Agent System Setup**

```bash
# Initialize agent coordinates
python tools/agent_setup/initialize_coordinates.py

# Validate agent configuration
python tools/agent_setup/validate_config.py

# Test agent communication
python tools/agent_setup/test_communication.py
```

## 🧪 **Verification and Testing**

### **System Verification**

```bash
# Run comprehensive system check
python tools/verification/system_check.py

# Test all services
python tools/verification/service_test.py

# Validate V2 compliance
python tools/verification/v2_compliance_check.py
```

### **Discord Integration Test**

```bash
# Test Discord bot connection
python tools/testing/test_discord_bot.py

# Test agent messaging
python tools/testing/test_agent_messaging.py

# Test command system
python tools/testing/test_commands.py
```

### **Performance Testing**

```bash
# Run performance tests
python tools/testing/performance_test.py

# Load testing
python tools/testing/load_test.py

# Memory usage test
python tools/testing/memory_test.py
```

## 🚀 **Starting the System**

### **Development Mode**

```bash
# Start Discord Commander
python src/services/discord_commander/bot_v2.py

# Start messaging service
python src/services/messaging_service.py

# Start agent system
python src/core/agent_system.py --start
```

### **Production Mode**

```bash
# Start with production configuration
python src/core/agent_system.py --start --environment production

# Start with monitoring
python src/core/agent_system.py --start --monitoring

# Start with logging
python src/core/agent_system.py --start --log-level INFO
```

### **Docker Deployment (Optional)**

```bash
# Build Docker image
docker build -t agent-cellphone-v2 .

# Run with Docker Compose
docker-compose up -d

# Check container status
docker-compose ps
```

## 🔍 **Troubleshooting**

### **Common Issues**

#### **Python Version Issues**
```bash
# Check Python version
python --version

# If version is incorrect, install correct version
# Windows: Download from python.org
# macOS: brew install python@3.9
# Ubuntu: sudo apt install python3.9
```

#### **Discord Connection Issues**
```bash
# Verify bot token format
echo $DISCORD_BOT_TOKEN | wc -c  # Should be 72 characters

# Verify guild ID format
echo $DISCORD_GUILD_ID | wc -c   # Should be 19 characters

# Test connection
python tools/testing/test_discord_connection.py
```

#### **Permission Issues**
```bash
# Check file permissions
ls -la .env
chmod 600 .env  # Secure environment file

# Check directory permissions
ls -la data/
chmod 755 data/  # Ensure data directory is writable
```

#### **Dependency Issues**
```bash
# Clear pip cache
pip cache purge

# Reinstall dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# Check for conflicts
pip check
```

### **Log Analysis**

```bash
# View system logs
tail -f logs/system.log

# View error logs
tail -f logs/error.log

# View agent logs
tail -f logs/agents.log
```

### **Debug Mode**

```bash
# Run with debug logging
python src/core/agent_system.py --start --debug

# Run with verbose output
python src/core/agent_system.py --start --verbose

# Run with profiling
python src/core/agent_system.py --start --profile
```

## 📊 **Installation Verification**

### **Health Check**

```bash
# Run health check
python tools/health_check.py

# Expected output:
# ✅ Python version: 3.9.7
# ✅ Dependencies: All installed
# ✅ Configuration: Valid
# ✅ Discord connection: Connected
# ✅ Database: Connected
# ✅ Agent system: Ready
```

### **Feature Testing**

```bash
# Test Discord commands
python tools/testing/test_discord_commands.py

# Test agent coordination
python tools/testing/test_agent_coordination.py

# Test messaging system
python tools/testing/test_messaging_system.py
```

## 🔄 **Updates and Maintenance**

### **Updating the System**

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Run migrations (if applicable)
python tools/database/migrate.py

# Restart services
python tools/restart_services.py
```

### **Backup and Recovery**

```bash
# Backup configuration
python tools/backup/backup_config.py

# Backup database
python tools/backup/backup_database.py

# Backup logs
python tools/backup/backup_logs.py
```

## 📞 **Support**

### **Installation Support**

If you encounter issues during installation:

1. **Check the logs**: Review installation logs for error messages
2. **Verify prerequisites**: Ensure all system requirements are met
3. **Test configuration**: Run configuration validation tools
4. **Contact support**: Open an issue on GitHub or contact the development team

### **Common Support Resources**

- **Documentation**: Check our comprehensive documentation
- **GitHub Issues**: Report installation issues
- **Discord Community**: Get help from the community
- **Email Support**: For critical installation issues

---

**Status**: Installation Guide completed  
**Agent**: Agent-7 (Web Development Expert)  
**Priority**: HIGH for production readiness  
**Next**: Continue with USAGE.md documentation
