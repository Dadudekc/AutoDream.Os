# Usage Guide - Agent Cellphone V2 Repository

**Version**: 2.0.0  
**Last Updated**: 2025-10-05  
**Agent**: Agent-7 (Elevated Web Development Expert)  

## 🌟 **Overview**

This comprehensive usage guide provides step-by-step instructions for using all components of the Agent Cellphone V2 Repository. The system enables autonomous AI agents to collaborate on complex software development tasks through multi-agent coordination, real-time communication, and strategic consultation.

## 🚀 **Quick Start Guide**

### **1. System Initialization**

```bash
# Navigate to project directory
cd agent-cellphone-v2

# Activate virtual environment (if using one)
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Initialize the system
python src/services/agent_system_initializer.py
```

### **2. Agent System Activation**

```bash
# Start agent coordination system
python src/core/agent_coordinator.py

# Verify agent status
python messaging_system.py Agent-7 Agent-4 "System initialization complete" NORMAL
```

### **3. Discord Commander Setup**

```bash
# Configure Discord credentials
cp .env.example .env
# Edit .env with your Discord bot token and guild ID

# Start Discord Commander
python src/services/discord_commander/bot_v2.py
```

## 🤖 **Agent System Usage**

### **Available Agents**

The system includes 8 specialized agents:

| Agent | Role | Responsibilities |
|-------|------|------------------|
| **Agent-4** | Captain | Strategic oversight, emergency intervention |
| **Agent-5** | Coordinator | Inter-agent coordination, communication |
| **Agent-6** | Quality | Quality assurance, V2 compliance |
| **Agent-7** | Implementation | Web development, system implementation |
| **Agent-8** | Integration | Advanced system integration |

### **Agent Communication**

#### **Messaging System**

```bash
# Send message between agents
python messaging_system.py <from_agent> <to_agent> "<message>" <priority>

# Examples:
python messaging_system.py Agent-7 Agent-4 "Task completed successfully" NORMAL
python messaging_system.py Agent-5 Agent-6 "Quality check requested" HIGH
python messaging_system.py Agent-4 Agent-7 "Emergency intervention required" CRITICAL
```

#### **Priority Levels**
- **NORMAL**: Standard communication
- **HIGH**: Important tasks requiring attention
- **CRITICAL**: Emergency situations requiring immediate response

#### **Devlog System**

```bash
# Log agent activities
python src/services/agent_devlog_posting.py --agent <agent_id> --action "<description>"

# Examples:
python src/services/agent_devlog_posting.py --agent Agent-7 --action "Documentation implementation complete"
python src/services/agent_devlog_posting.py --agent captain --action "Captain directive executed"
```

### **Agent Role Assignment**

```bash
# Captain assigns roles to agents
python tools/captain_cli.py --assign-role --agent Agent-5 --role COORDINATOR --task "Agent communication protocol"

# Check agent capabilities
python tools/captain_cli.py --check-capabilities --agent Agent-6

# List available roles
python tools/captain_cli.py --list-roles
```

## 📡 **Discord Commander Usage**

### **Bot Commands**

The Discord Commander provides comprehensive bot control through Discord commands:

#### **Agent Status Commands**
```
/agent_status [agent_id]     # Get agent status information
/agent_coordinates           # Display agent physical coordinates
/swarm_status               # Get swarm coordination status
```

#### **Agent Control Commands**
```
/send_message <agent> <message>  # Send message to specific agent
/swarm_coordinate <message>      # Coordinate swarm operations
/agent_control <agent> <action>  # Control agent operations
```

#### **System Commands**
```
/system_status               # Get overall system status
/project_info               # Display project information
/help                       # Show available commands
```

### **Discord Integration Setup**

1. **Create Discord Bot**:
   - Go to Discord Developer Portal
   - Create new application
   - Generate bot token
   - Invite bot to your server

2. **Configure Environment**:
   ```bash
   # Edit .env file
   DISCORD_BOT_TOKEN=your_bot_token_here
   DISCORD_GUILD_ID=your_guild_id_here
   DISCORD_CHANNEL_ID=your_channel_id_here
   ```

3. **Start Discord Commander**:
   ```bash
   python src/services/discord_commander/bot_v2.py
   ```

## 🌐 **Thea Strategic Consultation System**

### **Autonomous Communication**

The Thea system enables autonomous communication with strategic consultation capabilities:

#### **Strategic Consultation**

```bash
# Run strategic consultation
python src/services/thea/thea_consultation.py

# Autonomous messaging
python thea_autonomous.py send "Strategic guidance request"
```

#### **Browser Automation**

```bash
# Test browser automation
python login_helper.py

# Extract cookies for authentication
python extract_browser_cookies.py

# Manual cookie setup
python manual_cookie_setup.py
```

### **Thea Configuration**

1. **Cookie Authentication**:
   ```bash
   # Save authentication cookies
   python save_thea_cookies.py
   
   # Test cookie loading
   python extract_browser_cookies.py
   ```

2. **Browser Setup**:
   ```bash
   # Fix ChromeDriver compatibility
   python fix_chromedriver.py
   
   # Debug UI elements
   python debug_chatgpt_ui.py
   ```

## 🔧 **Project Scanner Usage**

### **Enhanced Project Scanner**

```bash
# Run comprehensive project scan
python tools/projectscanner/run_project_scan.py

# Generate project analysis
python tools/run_project_scan.py

# Enhanced scanner with caching
python tools/projectscanner/enhanced_scanner/core.py
```

### **Scan Results**

The project scanner generates:
- **Code analysis reports**
- **Dependency analysis**
- **Test coverage reports**
- **V2 compliance validation**
- **Quality metrics**

## 📊 **Quality Assurance Usage**

### **V2 Compliance Validation**

```bash
# Run quality gates
python quality_gates.py

# Check V2 compliance
python tools/v2_compliance_checker.py

# Generate compliance report
python tools/compliance_reporter.py
```

### **Testing Framework**

```bash
# Run all tests
python -m pytest

# Run specific test categories
python -m pytest tests/unit/
python -m pytest tests/integration/

# Generate test coverage
python -m pytest --cov=src tests/
```

## 🛠️ **Development Tools Usage**

### **Code Analysis**

```bash
# Static code analysis
python tools/static_analyzer.py

# Dependency analysis
python tools/dependency_analyzer.py

# Code quality metrics
python tools/quality_metrics.py
```

### **Documentation Generation**

```bash
# Generate API documentation
python tools/api_doc_generator.py

# Create project documentation
python tools/doc_generator.py

# Update documentation
python tools/doc_updater.py
```

## 🔍 **Troubleshooting Guide**

### **Common Issues**

#### **Discord Commander Issues**
```bash
# Check Discord configuration
python tools/discord_config_validator.py

# Test Discord connection
python tools/discord_connection_test.py

# Reset Discord configuration
python tools/discord_config_reset.py
```

#### **Agent Communication Issues**
```bash
# Check messaging system
python tools/messaging_system_test.py

# Validate agent status
python tools/agent_status_validator.py

# Reset agent communication
python tools/agent_communication_reset.py
```

#### **Thea System Issues**
```bash
# Diagnose cookie issues
python sync_drift_diagnostic.py

# Analyze cookie problems
python analyze_cookies.py

# Fix ChromeDriver issues
python force_chromedriver_fix.py
```

### **Debug Commands**

```bash
# System diagnostics
python tools/system_diagnostics.py

# Environment validation
python tools/env_inference_tool.py

# Component health check
python tools/component_health_check.py
```

## 📈 **Performance Monitoring**

### **System Monitoring**

```bash
# Monitor agent performance
python src/services/monitoring/agent_performance_monitor.py

# Check system health
python src/services/alerting/agent_health_checker.py

# Dashboard status
python src/services/dashboard/agent_status_dashboard.py
```

### **Metrics Collection**

```bash
# Collect performance metrics
python tools/metrics_collector.py

# Generate performance reports
python tools/performance_reporter.py

# Monitor resource usage
python tools/resource_monitor.py
```

## 🔐 **Security Usage**

### **Authentication**

```bash
# Validate Discord credentials
python tools/auth_validator.py

# Check API keys
python tools/api_key_validator.py

# Security audit
python tools/security_audit.py
```

### **Data Protection**

```bash
# Encrypt sensitive data
python tools/data_encryption.py

# Backup configuration
python tools/config_backup.py

# Restore configuration
python tools/config_restore.py
```

## 📚 **Advanced Usage**

### **Custom Agent Development**

```bash
# Create custom agent
python tools/agent_creator.py

# Register new agent
python tools/agent_registrar.py

# Configure agent capabilities
python tools/agent_configurator.py
```

### **Workflow Automation**

```bash
# Create custom workflow
python tools/workflow_creator.py

# Execute workflow
python tools/workflow_executor.py

# Monitor workflow progress
python tools/workflow_monitor.py
```

## 🎯 **Best Practices**

### **Agent Coordination**
- Use appropriate priority levels for messages
- Log all significant activities via devlog system
- Coordinate with Captain for strategic decisions
- Maintain V2 compliance standards

### **Discord Integration**
- Keep bot token secure and never commit to version control
- Use appropriate Discord permissions
- Monitor bot status and performance
- Regular backup of Discord configuration

### **Thea Communication**
- Maintain valid authentication cookies
- Use non-headless mode for debugging
- Monitor browser automation performance
- Regular cookie refresh and validation

### **Quality Assurance**
- Run quality gates before deployment
- Maintain V2 compliance standards
- Regular testing and validation
- Comprehensive documentation updates

## 📞 **Support and Help**

### **Getting Help**
- **Documentation**: Check `docs/` directory for detailed guides
- **Agent Communication**: Use messaging system for agent coordination
- **Captain Support**: Contact Agent-4 for strategic guidance
- **Technical Issues**: Use troubleshooting guides and diagnostic tools

### **Reporting Issues**
```bash
# Generate system report
python tools/system_reporter.py

# Create issue report
python tools/issue_reporter.py

# Submit to Captain
python messaging_system.py Agent-7 Agent-4 "Issue report generated" HIGH
```

---

**Status**: Usage Guide Complete  
**Agent**: Agent-7 (Elevated Web Development Expert)  
**Version**: 2.0.0  
**Last Updated**: 2025-10-05  
**Next**: API.md Implementation
