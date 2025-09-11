# 📜 **CAPTAIN'S HANDBOOK - SCRIPTS COMMANDS SECTION**

## **Agent Management & Onboarding Scripts**

### **1. Agent Onboarding (`scripts/agent_onboarding.py`)**
```bash
# Automated agent onboarding for new swarm members
python scripts/agent_onboarding.py

# Features:
# - Automated workspace creation
# - Agent role assignment
# - Initial configuration setup
# - Inbox and status initialization
# - Integration with swarm messaging
```

### **2. Agent Documentation CLI (`scripts/agent_documentation_cli.py`)**
```bash
# Agent documentation generation and management
python scripts/agent_documentation_cli.py

# Features:
# - Generates agent documentation
# - Updates role descriptions
# - Maintains agent capability records
# - Creates searchable documentation index
```

## **Discord Integration Scripts**

### **3. Setup Enhanced Discord (`scripts/setup_enhanced_discord.py`)**
```bash
# Enhanced Discord integration setup
python scripts/setup_enhanced_discord.py

# Features:
# - Configures Discord bot integration
# - Sets up individual agent channels
# - Initializes devlog posting system
# - Configures webhook authentication
```

### **4. Test Enhanced Discord (`scripts/test_enhanced_discord.py`)**
```bash
# Discord integration testing and validation
python scripts/test_enhanced_discord.py

# Features:
# - Tests Discord connectivity
# - Validates webhook functionality
# - Verifies devlog posting
# - Checks agent channel access
```

## **Code Quality & Compliance Scripts**

### **5. Cleanup V2 Compliance (`scripts/cleanup_v2_compliance.py`)**
```bash
# V2 compliance cleanup and enforcement
python scripts/cleanup_v2_compliance.py

# Features:
# - Identifies V2 compliance violations
# - Reports files exceeding 400-line limit
# - Suggests code splitting strategies
# - Generates compliance reports
```

### **6. Enforce Python Standards (`scripts/enforce_python_standards.py`)**
```bash
# Python code standards enforcement
python scripts/enforce_python_standards.py

# Features:
# - PEP 8 compliance checking
# - Code style standardization
# - Import organization
# - Type hint validation
```

## **System Integration & Setup Scripts**

### **7. Activate Vector Database Integration (`scripts/activate_vector_database_integration.py`)**
```bash
# Vector database integration activation
python scripts/activate_vector_database_integration.py

# Features:
# - Activates vector database functionality
# - Configures embedding services
# - Sets up vector search capabilities
# - Initializes database connections
```

### **8. Fix and Ingest Vector Database (`scripts/fix_and_ingest_vector_database.py`)**
```bash
# Vector database repair and data ingestion
python scripts/fix_and_ingest_vector_database.py

# Features:
# - Repairs vector database issues
# - Ingests new data into vector store
# - Updates embeddings
# - Validates database integrity
```

### **9. Index V2 Refactoring (`scripts/index_v2_refactoring.py`)**
```bash
# V2 refactoring indexing and tracking
python scripts/index_v2_refactoring.py

# Features:
# - Indexes refactoring progress
# - Tracks V2 compliance improvements
# - Generates refactoring reports
# - Monitors consolidation status
```

## **Status & Monitoring Scripts**

### **10. Status Embedding Refresh (`scripts/status_embedding_refresh.py`)**
```bash
# Status embedding system refresh
python scripts/status_embedding_refresh.py

# Features:
# - Refreshes status embeddings
# - Updates status indexes
# - Synchronizes status data
# - Validates embedding accuracy
```

### **11. Validate Workspace Coords (`scripts/validate_workspace_coords.py`)**
```bash
# Workspace coordinate validation
python scripts/validate_workspace_coords.py

# Features:
# - Validates agent coordinates
# - Checks coordinate consistency
- Verifies workspace positioning
# - Reports coordinate conflicts
```

### **12. V2 Release Summary (`scripts/v2_release_summary.py`)**
```bash
# V2 release summary generation
python scripts/v2_release_summary.py

# Features:
# - Generates release summaries
# - Documents V2 improvements
# - Creates changelog entries
# - Summarizes consolidation progress
```

## **Advanced System Scripts**

### **13. Terminal Completion Monitor (`scripts/terminal_completion_monitor.py`)**
```bash
# Terminal command completion monitoring
python scripts/terminal_completion_monitor.py

# Features:
# - Monitors terminal command execution
# - Tracks command completion status
# - Logs command performance
# - Identifies failed commands
```

### **14. Execution Scripts (Multiple)**
```bash
# Run Admin Commander
python scripts/execution/run_admin_commander.py

# Run Discord Bot
python scripts/execution/run_discord_bot.py

# Features:
# - Administrative command execution
# - Discord bot management
# - System administration tools
```

### **15. Utilities Scripts**
```bash
# Find Large Files
python scripts/utilities/find_large_files.py

# Setup Discord Bot
python scripts/utilities/setup_discord_bot.py

# Features:
# - File system analysis
# - Discord bot configuration
# - Utility functions for system management
```

---

## **Scripts Commands Quick Reference**

```bash
# 🤖 AGENT MANAGEMENT
python scripts/agent_onboarding.py              # New agent onboarding
python scripts/agent_documentation_cli.py      # Agent documentation

# 🤝 DISCORD INTEGRATION
python scripts/setup_enhanced_discord.py       # Discord setup
python scripts/test_enhanced_discord.py        # Discord testing

# 📏 CODE QUALITY
python scripts/cleanup_v2_compliance.py        # V2 compliance cleanup
python scripts/enforce_python_standards.py     # Code standards

# 🗄️ VECTOR DATABASE
python scripts/activate_vector_database_integration.py  # Vector DB activation
python scripts/fix_and_ingest_vector_database.py       # Vector DB repair

# 📊 SYSTEM MONITORING
python scripts/status_embedding_refresh.py     # Status refresh
python scripts/validate_workspace_coords.py    # Coordinate validation
python scripts/v2_release_summary.py           # Release summary
python scripts/terminal_completion_monitor.py  # Terminal monitoring

# ⚙️ ADVANCED UTILITIES
python scripts/execution/run_admin_commander.py # Admin commands
python scripts/execution/run_discord_bot.py     # Discord bot
python scripts/utilities/find_large_files.py    # File analysis
python scripts/index_v2_refactoring.py          # Refactoring tracking
```

---

## **Script Integration Notes**

### **Captain Workflow Integration**
```bash
# Recommended Captain onboarding workflow:
1. python scripts/agent_onboarding.py        # Onboard new agents
2. python scripts/validate_workspace_coords.py # Validate coordinates
3. python scripts/setup_enhanced_discord.py   # Setup Discord
4. python scripts/test_enhanced_discord.py    # Test integration

# Quality assurance workflow:
1. python scripts/cleanup_v2_compliance.py    # Check compliance
2. python scripts/enforce_python_standards.py # Enforce standards
3. python scripts/v2_release_summary.py       # Generate summary
```

### **System Maintenance**
```bash
# Regular maintenance:
python scripts/status_embedding_refresh.py     # Refresh status
python scripts/terminal_completion_monitor.py  # Monitor commands
python scripts/index_v2_refactoring.py         # Track progress

# Emergency recovery:
python scripts/fix_and_ingest_vector_database.py # Repair vector DB
python scripts/activate_vector_database_integration.py # Reactivate DB
```

### **Quality Gates**
```bash
# Pre-deployment checks:
python scripts/cleanup_v2_compliance.py        # Compliance check
python scripts/enforce_python_standards.py     # Standards check
python scripts/validate_workspace_coords.py    # Coordinate validation
python scripts/test_enhanced_discord.py        # Discord validation
```

---

## **Script Dependencies & Requirements**

### **Required Packages**
```bash
# Core dependencies (usually pre-installed):
pip install discord.py pyautogui pyperclip

# Vector database dependencies:
pip install faiss-cpu sentence-transformers

# Development dependencies:
pip install black flake8 mypy
```

### **System Requirements**
```bash
# Directory permissions:
chmod +x scripts/*.py
chmod +x scripts/utilities/*.py
chmod +x scripts/execution/*.py

# Configuration files required:
config/coordinates.json
config/discord_config.json
agent_workspaces/*/status.json
```

---

**🐝 SWARM SCRIPTS - COMPREHENSIVE CAPTAIN TOOLKIT!** ⚡🚀
