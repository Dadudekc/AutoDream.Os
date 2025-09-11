# 🛠️ **CAPTAIN'S HANDBOOK - TOOLS COMMANDS SECTION**

## **Project Analysis & Scanning Tools**

### **1. Project Scanner (`tools/projectscanner.py`)**
```bash
# Comprehensive project analysis and snapshot generation
python tools/projectscanner.py

# Features:
# - Scans entire project structure
# - Generates project_analysis.json
# - Creates chatgpt_project_context.json
# - Builds dependency_cache.json
# - Categorizes agents and modules
# - Generates modular reports
```

### **2. Run Project Scan (`tools/run_project_scan.py`)**
```bash
# Automated project scanning with git staging
python tools/run_project_scan.py

# Features:
# - Runs ProjectScanner from repo root
# - Stages snapshot artifacts automatically
# - Safe for pre-commit hooks
# - Generates all analysis files
```

### **3. Captain Snapshot (`tools/captain_snapshot.py`)**
```bash
# Multi-agent status overview with staleness detection
python tools/captain_snapshot.py

# Features:
# - Aggregated view of all 8 agent statuses
# - Staleness detection (< 5 min = FRESH, 5-15 min = RECENT, > 15 min = STALE)
# - Reads from runtime/agents_index.json
# - Concise status table presentation
```

### **4. Agent Check-in (`tools/agent_checkin.py`)**
```bash
# Agent status check-in system
python tools/agent_checkin.py

# Features:
# - Agent status reporting
# - Check-in timestamp tracking
# - Status validation and verification
```

## **Code Quality & Analysis Tools**

### **5. Analysis CLI (`tools/analysis_cli.py`)**
```bash
# Comprehensive code analysis interface
python tools/analysis_cli.py

# Features:
# - Code quality analysis
# - Complexity assessment
# - Dependency analysis
# - Architecture pattern detection
```

### **6. Duplication Analyzer (`tools/duplication_analyzer.py`)**
```bash
# Code duplication detection and analysis
python tools/duplication_analyzer.py

# Features:
# - Identifies duplicate code patterns
# - Generates duplication reports
# - Suggests consolidation opportunities
```

### **7. Functionality Verification (`tools/functionality_verification.py`)**
```bash
# Feature and functionality verification
python tools/functionality_verification.py

# Features:
# - Verifies system functionality
# - Tests feature completeness
- Validates implementation against requirements
```

## **Automation & Remediation Tools**

### **8. Auto Remediate LOC (`tools/auto_remediate_loc.py`)**
```bash
# Automated code remediation for Lines of Code violations
python tools/auto_remediate_loc.py

# Features:
# - V2 compliance enforcement (< 400 lines per file)
# - Automatic code splitting for large files
# - Remediation suggestions and implementation
```

### **9. Generate Utils Catalog (`tools/generate_utils_catalog.py`)**
```bash
# Utility catalog generation
python tools/generate_utils_catalog.py

# Features:
# - Catalogs all utility functions
# - Generates comprehensive documentation
# - Creates searchable utility index
```

## **Development & Quality Assurance Tools**

### **10. Audit Cleanup (`tools/audit_cleanup.py`)**
```bash
# Audit and cleanup automation
python tools/audit_cleanup.py

# Features:
# - Automated audit processes
# - Cleanup of temporary files
# - System health verification
```

### **11. Check Snapshot Up-to-Date (`tools/check_snapshot_up_to_date.py`)**
```bash
# Snapshot freshness verification
python tools/check_snapshot_up_to_date.py

# Features:
# - Verifies snapshot currency
- Checks analysis file freshness
- Reports outdated snapshots
```

---

## **Tool Commands Quick Reference**

```bash
# 🔍 ANALYSIS & SCANNING
python tools/run_project_scan.py          # Full project scan + git staging
python tools/projectscanner.py            # Core project analysis
python tools/captain_snapshot.py          # Agent status overview
python tools/analysis_cli.py              # Code analysis interface

# 🔧 QUALITY & VERIFICATION
python tools/duplication_analyzer.py      # Code duplication detection
python tools/functionality_verification.py # Feature verification
python tools/auto_remediate_loc.py        # V2 compliance remediation

# 📊 CATALOGS & REPORTS
python tools/generate_utils_catalog.py    # Utility catalog generation

# 🔄 MAINTENANCE & CLEANUP
python tools/audit_cleanup.py             # Audit and cleanup
python tools/check_snapshot_up_to_date.py # Snapshot verification
python tools/agent_checkin.py             # Agent status check-in
```

---

## **Tool Integration Notes**

### **Pre-commit Integration**
```bash
# These tools are designed for pre-commit integration:
python tools/run_project_scan.py    # Safe for pre-commit hooks
python tools/auto_remediate_loc.py  # V2 compliance enforcement
```

### **Automated Workflows**
```bash
# Recommended Captain workflow:
1. python tools/captain_snapshot.py     # Check agent statuses
2. python tools/run_project_scan.py     # Update project analysis
3. python tools/analysis_cli.py         # Review code quality
4. python tools/auto_remediate_loc.py   # Fix V2 violations
```

### **Emergency Response**
```bash
# For system issues:
python tools/audit_cleanup.py           # Clean up system
python tools/functionality_verification.py # Verify functionality
python tools/captain_snapshot.py        # Check agent health
```

---

**🐝 SWARM TOOLS - READY FOR CAPTAIN USE!** ⚡🚀
