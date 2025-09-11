# 📜 **CAPTAIN'S HANDBOOK - SCRIPTS COMPLETE DOCUMENTATION**

## **Comprehensive Script Automation System**
**V2 Compliance**: Complete automation toolkit with 15+ specialized scripts

**Author**: Agent-6 - Coordination & Communication Specialist
**Last Updated**: 2025-09-09
**Status**: ACTIVE - Complete Scripts Documentation

---

## 🎯 **OVERVIEW**

The Scripts system provides comprehensive automation capabilities for agent onboarding, system management, quality assurance, and operational workflows. All scripts follow V2 compliance standards and provide seamless integration with the swarm system.

**Script Categories**:
- **Agent Management**: Onboarding, coordination, and lifecycle management
- **System Operations**: Vector database, Discord integration, and maintenance
- **Quality Assurance**: Standards enforcement and compliance validation
- **Development Tools**: Enhanced consultation and documentation systems

---

## 🤖 **AGENT MANAGEMENT SCRIPTS**

### **1. Agent Onboarding Script**
```bash
python scripts/agent_onboarding.py
```

**Description**: Automated agent onboarding system for new swarm members with workspace creation and initialization.

**Core Features**:
- **Workspace Creation**: Automatic agent workspace setup
- **Configuration Initialization**: Default settings and preferences
- **Role Assignment**: Agent specialization and capability configuration
- **Integration Setup**: Seamless swarm system integration

**Onboarding Process**:
1. **Agent Selection**: Choose from available agent roles
2. **Workspace Setup**: Create dedicated agent directory structure
3. **Configuration**: Initialize agent-specific settings
4. **Integration**: Connect to swarm communication systems
5. **Validation**: Verify successful onboarding

**Available Agent Roles**:
- **Agent-1**: Integration & Core Systems Specialist
- **Agent-2**: Architecture & Design Specialist
- **Agent-3**: Infrastructure & DevOps Specialist
- **Agent-5**: Business Intelligence Specialist
- **Agent-6**: Coordination & Communication Specialist
- **Agent-7**: Web Development Specialist
- **Agent-8**: SSOT Maintenance & System Integration Specialist

**Example Usage**:
```bash
# Interactive onboarding
python scripts/agent_onboarding.py

# Automated onboarding for specific agent
python scripts/agent_onboarding.py --agent Agent-7 --auto
```

### **2. Agent Documentation CLI**
```bash
python scripts/agent_documentation_cli.py
```

**Description**: AI-powered agent documentation system with vectorized search and intelligent assistance.

**Capabilities**:
- **Vector Search**: Semantic search across all documentation
- **Context-Aware Assistance**: Intelligent help based on agent role
- **Real-time Updates**: Dynamic documentation integration
- **Multi-format Support**: Text, code, and structured data

**Key Features**:
- **Smart Query Processing**: Natural language documentation queries
- **Role-Based Responses**: Tailored assistance for agent specializations
- **Integration Support**: Seamless connection with swarm systems
- **Performance Optimization**: Fast response times with vector indexing

---

## 🗄️ **SYSTEM OPERATIONS SCRIPTS**

### **3. Vector Database Integration**
```bash
python scripts/activate_vector_database_integration.py
```

**Description**: Complete vector database activation and integration system for enhanced intelligence capabilities.

**Integration Features**:
- **Database Initialization**: Complete vector database setup
- **Agent Indexing**: All agents indexed with capabilities and context
- **Semantic Search**: Advanced search across all system data
- **Pattern Recognition**: Intelligent pattern detection and learning

**Activation Process**:
1. **Database Setup**: Initialize vector database infrastructure
2. **Agent Profiling**: Index all agent capabilities and roles
3. **Pattern Learning**: Analyze communication and task patterns
4. **Integration Testing**: Validate all integration points
5. **Performance Optimization**: Tune for optimal performance

**Capabilities Unlocked**:
- **Intelligent Task Assignment**: Smart task distribution based on agent capabilities
- **Context-Aware Communication**: Enhanced messaging with context understanding
- **Pattern-Based Optimization**: Continuous system improvement through learning
- **Cross-Agent Learning**: Knowledge sharing and capability enhancement

### **4. Vector Database Maintenance**
```bash
python scripts/fix_and_ingest_vector_database.py
```

**Description**: Vector database maintenance and data ingestion system for continuous optimization.

**Maintenance Operations**:
- **Data Integrity**: Validate and repair database integrity
- **Performance Tuning**: Optimize database performance and queries
- **Index Optimization**: Maintain efficient search indexes
- **Data Synchronization**: Ensure consistency across all data sources

---

## 💬 **DISCORD INTEGRATION SCRIPTS**

### **5. Enhanced Discord Integration Setup**
```bash
python scripts/setup_enhanced_discord.py
```

**Description**: Complete Discord integration setup with enhanced devlog and communication capabilities.

**Setup Features**:
- **Bot Configuration**: Automated Discord bot setup and configuration
- **Channel Integration**: Seamless integration with Discord channels
- **Devlog Automation**: Automatic devlog posting to Discord
- **Permission Management**: Proper permission setup and validation

**Integration Components**:
- **Webhook Setup**: Automated webhook configuration
- **Channel Mapping**: Map swarm channels to Discord channels
- **Authentication**: Secure bot authentication and authorization
- **Testing**: Comprehensive integration testing

### **6. Enhanced Discord Testing**
```bash
python scripts/test_enhanced_discord.py
```

**Description**: Comprehensive testing suite for Discord integration functionality.

**Testing Capabilities**:
- **Connection Testing**: Validate Discord API connectivity
- **Message Testing**: Test message sending and receiving
- **Webhook Validation**: Verify webhook functionality
- **Error Handling**: Test error scenarios and recovery
- **Performance Testing**: Validate integration performance

### **7. Discord Bot Setup Utility**
```bash
python scripts/utilities/setup_discord_bot.py
```

**Description**: Utility script for Discord bot configuration and management.

**Bot Management Features**:
- **Bot Creation**: Automated bot creation and registration
- **Permission Setup**: Configure bot permissions and roles
- **Channel Configuration**: Set up bot access to required channels
- **Monitoring Setup**: Configure bot monitoring and logging

---

## 🛠️ **QUALITY ASSURANCE SCRIPTS**

### **8. Python Standards Enforcement**
```bash
python scripts/enforce_python_standards.py
```

**Description**: Automated Python code standards enforcement and compliance validation.

**Standards Enforcement**:
- **PEP8 Compliance**: Automatic code formatting and style correction
- **Import Optimization**: Organize and optimize import statements
- **Documentation Standards**: Ensure proper docstring formatting
- **Code Quality**: Validate code quality metrics and patterns

**Enforcement Process**:
1. **Code Analysis**: Scan codebase for style violations
2. **Automatic Fixes**: Apply automatic corrections where possible
3. **Manual Review**: Flag issues requiring manual intervention
4. **Compliance Reporting**: Generate detailed compliance reports

### **9. V2 Compliance Cleanup**
```bash
python scripts/cleanup_v2_compliance.py
```

**Description**: Specialized cleanup script for V2 compliance violations and architectural improvements.

**Compliance Operations**:
- **File Size Reduction**: Identify and refactor oversized files (>400 lines)
- **Architectural Validation**: Ensure proper modular architecture
- **Import Optimization**: Clean up circular and redundant imports
- **Documentation Enhancement**: Improve code documentation coverage

**Cleanup Categories**:
- **Critical Violations**: Files >400 lines requiring immediate refactoring
- **Major Violations**: Files 350-400 lines needing attention
- **Minor Violations**: Files 300-350 lines for optimization
- **Architectural Issues**: Import cycles and dependency problems

---

## 🔧 **DEVELOPMENT & CONSULTATION SCRIPTS**

### **10. Thea Consultation Script**
```bash
python scripts/consult_thea.py --mode auto --browser chrome --url [CHATGPT_URL] --message-file messages/thea_consultation_message.md
```

**Description**: Advanced Thea Manager consultation automation with cookie persistence and browser integration.

**Automation Features**:
- **Browser Automation**: Selenium-based browser control for Thea Manager
- **Cookie Persistence**: Maintain login sessions across consultations
- **Message Automation**: Automated message composition and sending
- **Screenshot Capture**: Post-consultation screenshot documentation
- **Fallback Support**: PyAutoGUI fallback for Selenium failures

**Consultation Workflow**:
1. **Browser Launch**: Open Thea Manager in specified browser
2. **Authentication**: Handle login with cookie persistence
3. **Message Preparation**: Load and format consultation message
4. **Automated Interaction**: Send message and wait for response
5. **Documentation**: Capture screenshots and log interaction

**Supported Browsers**:
- **Chrome**: Primary browser with full automation support
- **Firefox**: Alternative browser with Selenium support
- **Edge**: Microsoft Edge compatibility
- **Safari**: macOS Safari support

### **11. V2 Refactoring Index**
```bash
python scripts/index_v2_refactoring.py
```

**Description**: V2 refactoring tracking and indexing system for compliance monitoring.

**Indexing Features**:
- **Refactoring Tracking**: Monitor V2 compliance refactoring progress
- **File Analysis**: Analyze file sizes and complexity metrics
- **Compliance Reporting**: Generate V2 compliance status reports
- **Progress Tracking**: Track refactoring completion percentages

---

## 📊 **MONITORING & VALIDATION SCRIPTS**

### **12. Workspace Coordinate Validation**
```bash
python scripts/validate_workspace_coords.py
```

**Description**: Validation script for agent workspace coordinates and PyAutoGUI integration.

**Validation Operations**:
- **Coordinate Verification**: Validate all agent coordinates are within screen bounds
- **Multi-Monitor Support**: Ensure compatibility with multi-monitor setups
- **PyAutoGUI Testing**: Test coordinate accessibility and click accuracy
- **Configuration Backup**: Create backups before coordinate modifications

**Validation Checks**:
- **Screen Bounds**: Ensure coordinates are within display boundaries
- **Monitor Detection**: Identify and validate multi-monitor configurations
- **Accessibility Testing**: Verify PyAutoGUI can reach all coordinates
- **Configuration Integrity**: Validate coordinate configuration file integrity

### **13. Status Embedding Refresh**
```bash
python scripts/status_embedding_refresh.py
```

**Description**: Status embedding system refresh and synchronization script.

**Refresh Operations**:
- **Embedding Updates**: Refresh all status embeddings in vector database
- **Synchronization**: Ensure consistency between status files and embeddings
- **Performance Optimization**: Optimize embedding retrieval and search
- **Integrity Validation**: Validate embedding accuracy and completeness

### **14. Terminal Completion Monitor**
```bash
python scripts/terminal_completion_monitor.py
```

**Description**: Terminal command completion monitoring and validation system.

**Monitoring Features**:
- **Command Tracking**: Monitor terminal command execution and completion
- **Success Validation**: Validate command execution success rates
- **Error Detection**: Identify and report command failures
- **Performance Metrics**: Track command execution times and resource usage

---

## 🛠️ **UTILITY SCRIPTS**

### **15. Find Large Files**
```bash
python scripts/utilities/find_large_files.py
```

**Description**: Utility script for identifying large files that may need refactoring.

**File Analysis**:
- **Size Thresholds**: Identify files exceeding V2 compliance limits
- **File Type Filtering**: Focus on relevant file types (Python, JavaScript, etc.)
- **Directory Scanning**: Comprehensive directory traversal
- **Reporting**: Detailed reports with refactoring recommendations

**Analysis Categories**:
- **Critical (>400 lines)**: Immediate refactoring required
- **Major (350-400 lines)**: High priority refactoring
- **Minor (300-350 lines)**: Optimization candidates
- **Acceptable (<300 lines)**: V2 compliant

---

## 🔄 **INTEGRATION WORKFLOWS**

### **Complete Agent Onboarding Workflow**
```bash
# 1. Validate workspace coordinates
python scripts/validate_workspace_coords.py

# 2. Onboard new agent
python scripts/agent_onboarding.py --agent Agent-7

# 3. Test Discord integration
python scripts/test_enhanced_discord.py

# 4. Activate vector database for new agent
python scripts/activate_vector_database_integration.py

# 5. Refresh status embeddings
python scripts/status_embedding_refresh.py
```

### **System Maintenance Workflow**
```bash
# 1. Enforce Python standards
python scripts/enforce_python_standards.py

# 2. Cleanup V2 compliance issues
python scripts/cleanup_v2_compliance.py

# 3. Find and address large files
python scripts/utilities/find_large_files.py

# 4. Validate workspace coordinates
python scripts/validate_workspace_coords.py

# 5. Monitor terminal completion
python scripts/terminal_completion_monitor.py
```

### **Development Enhancement Workflow**
```bash
# 1. Consult Thea for development guidance
python scripts/consult_thea.py --mode auto --browser chrome --message-file messages/dev_guidance.md

# 2. Index V2 refactoring progress
python scripts/index_v2_refactoring.py

# 3. Setup enhanced Discord integration
python scripts/setup_enhanced_discord.py

# 4. Test Discord functionality
python scripts/test_enhanced_discord.py
```

---

## 📋 **SCRIPT QUICK REFERENCE**

| Category | Script | Primary Use | Key Parameters |
|----------|--------|-------------|----------------|
| **Agent Management** | `agent_onboarding.py` | New agent setup | `--agent`, `--auto` |
| **Agent Management** | `agent_documentation_cli.py` | Documentation assistance | `--help` |
| **System Operations** | `activate_vector_database_integration.py` | Vector DB setup | N/A |
| **System Operations** | `fix_and_ingest_vector_database.py` | Vector DB maintenance | N/A |
| **Discord Integration** | `setup_enhanced_discord.py` | Discord bot setup | N/A |
| **Discord Integration** | `test_enhanced_discord.py` | Discord testing | N/A |
| **Discord Integration** | `utilities/setup_discord_bot.py` | Bot configuration | N/A |
| **Quality Assurance** | `enforce_python_standards.py` | Code formatting | N/A |
| **Quality Assurance** | `cleanup_v2_compliance.py` | Compliance cleanup | N/A |
| **Development Tools** | `consult_thea.py` | AI consultation | `--mode`, `--browser`, `--url` |
| **Development Tools** | `index_v2_refactoring.py` | Refactoring tracking | N/A |
| **Monitoring** | `validate_workspace_coords.py` | Coordinate validation | N/A |
| **Monitoring** | `status_embedding_refresh.py` | Embedding refresh | N/A |
| **Monitoring** | `terminal_completion_monitor.py` | Command monitoring | N/A |
| **Utilities** | `utilities/find_large_files.py` | File size analysis | N/A |

---

## ⚠️ **SCRIPT REQUIREMENTS & DEPENDENCIES**

### **Core Dependencies**
- **Python 3.8+**: Required for all scripts
- **Selenium**: For browser automation (consult_thea.py)
- **PyAutoGUI**: Fallback automation support
- **Requests**: HTTP operations for Discord integration
- **Vector Database**: For documentation and intelligence features

### **System Requirements**
- **Browser Support**: Chrome/Firefox/Edge/Safari for web automation
- **File Permissions**: Read/write access to project directories
- **Network Access**: Internet connectivity for external integrations
- **Memory**: 2GB+ RAM for large project operations

---

## 🚨 **TROUBLESHOOTING & BEST PRACTICES**

### **Common Issues & Solutions**

**Issue**: Script fails with import errors
**Solution**: Ensure all required dependencies are installed and PYTHONPATH is set correctly

**Issue**: Browser automation fails
**Solution**: Update browser drivers, check browser compatibility, use fallback modes

**Issue**: Discord integration issues
**Solution**: Verify bot tokens, check Discord API status, validate permissions

**Issue**: Vector database connection fails
**Solution**: Check database configuration, verify network connectivity, restart services

### **Best Practices**
- **Run in Order**: Execute onboarding scripts in proper sequence
- **Backup First**: Create backups before running cleanup or refactoring scripts
- **Test Environment**: Test scripts in development environment before production
- **Monitor Execution**: Use terminal completion monitor for long-running scripts
- **Validate Results**: Always validate script output and system state after execution

---

## 📈 **INTEGRATION WITH SWARM OPERATIONS**

### **Captain's Script Oversight**
- **Daily Validation**: Run coordinate validation and status checks daily
- **Weekly Maintenance**: Execute cleanup and standards enforcement weekly
- **Monthly Optimization**: Run comprehensive analysis and optimization monthly
- **On-demand Automation**: Use Thea consultation for complex decision-making

### **Agent Integration Points**
- **Onboarding**: Use agent onboarding script for new swarm members
- **Communication**: Leverage Discord integration for external coordination
- **Quality**: Run standards enforcement before code commits
- **Documentation**: Use agent documentation CLI for assistance

---

**✅ SCRIPTS SYSTEM COMPLETE**
**15 Scripts Documented | All Categories Covered | V2 Compliant**

**Ready for comprehensive swarm automation!** 🚀⚡
