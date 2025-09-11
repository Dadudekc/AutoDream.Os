# 🔧 **CAPTAIN'S HANDBOOK - UTILITIES & MAINTENANCE**

## **Comprehensive System Utilities & Maintenance Tools**
**V2 Compliance**: Essential maintenance and utility operations toolkit

**Author**: Agent-3 - Infrastructure & DevOps Specialist
**Last Updated**: 2025-09-09
**Status**: ACTIVE - Complete Utilities Documentation

---

## 🎯 **OVERVIEW**

The Utilities system provides essential maintenance, file operations, and system management tools for the swarm infrastructure. These utilities ensure smooth operation, maintenance, and optimization of the entire system.

**Utility Categories**:
- **File Operations**: File management, cleanup, and organization
- **System Maintenance**: Infrastructure monitoring and optimization
- **Workspace Management**: Agent workspace coordination and validation
- **Development Tools**: Development workflow enhancement utilities

---

## 📁 **FILE OPERATIONS UTILITIES**

### **1. Find Large Files**
```bash
python scripts/utilities/find_large_files.py
```

**Description**: Utility script for identifying large files that may need refactoring or optimization.

**Analysis Features**:
- **Size Threshold Scanning**: Identify files exceeding specified size limits
- **File Type Filtering**: Focus on relevant file types (Python, JavaScript, etc.)
- **Directory Recursion**: Comprehensive directory traversal and analysis
- **Sorting Options**: Sort results by size, modification date, or file type
- **Export Capabilities**: Export analysis results to various formats

**Size Categories**:
- **Critical**: Files > 1MB (immediate review required)
- **Large**: Files 500KB - 1MB (optimization candidates)
- **Medium**: Files 100KB - 500KB (monitoring required)
- **Small**: Files < 100KB (typically acceptable)

**Example Usage**:
```bash
# Find all Python files over 50KB
python scripts/utilities/find_large_files.py --type py --size 50KB

# Find largest files in src directory
python scripts/utilities/find_large_files.py --directory src/ --sort size --limit 10

# Export results to CSV
python scripts/utilities/find_large_files.py --export results.csv --format csv
```

**Analysis Output**:
```
📊 Large Files Analysis Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📁 Directory: /project/src
🔍 File Type: Python files
📏 Size Threshold: 50KB

📋 Large Files Found (8 files):
┌─────────────────────────────────────┬─────────┬────────────┐
│ File Path                           │ Size    │ Modified   │
├─────────────────────────────────────┼─────────┼────────────┤
│ src/services/messaging_core.py      │ 245KB   │ 2025-09-09 │
│ src/core/unified_system.py          │ 189KB   │ 2025-09-08 │
│ src/architecture/design_patterns.py │ 156KB   │ 2025-09-07 │
│ tools/analysis_cli.py               │ 98KB    │ 2025-09-06 │
│ src/core/performance_cli.py         │ 87KB    │ 2025-09-05 │
└─────────────────────────────────────┴─────────┴────────────┘

💡 Recommendations:
• 3 files exceed V2 compliance limits (>400 lines)
• Consider refactoring large architectural files
• Review analysis tools for optimization opportunities
```

---

## 🏗️ **SYSTEM MAINTENANCE UTILITIES**

### **2. Auto Remediation**
```bash
python tools/auto_remediate_loc.py
```

**Description**: Automated remediation tool for lines of code (LOC) violations and V2 compliance issues.

**Remediation Features**:
- **Automatic Refactoring**: Intelligent code splitting and reorganization
- **V2 Compliance**: Ensure all files meet V2 architectural standards
- **Backup Creation**: Automatic backup before any modifications
- **Rollback Capability**: Ability to revert changes if issues occur
- **Progress Tracking**: Detailed progress reporting and status updates

**Remediation Categories**:
- **File Splitting**: Split large files into smaller, focused modules
- **Function Extraction**: Extract complex functions into separate utilities
- **Class Decomposition**: Break down large classes into smaller components
- **Import Optimization**: Clean up and optimize import statements

**Safety Features**:
- **Pre-remediation Backup**: Complete backup of all modified files
- **Syntax Validation**: Ensure all changes maintain Python syntax validity
- **Import Resolution**: Verify all imports remain functional after changes
- **Test Validation**: Run existing tests to ensure functionality preservation

### **3. Cleanup Guard**
```bash
python tools/cleanup_guarded.sh
# or
python tools/cleanup_guarded.ps1
```

**Description**: Cross-platform cleanup utility with safety guards and validation.

**Cleanup Operations**:
- **Safe File Removal**: Remove temporary and cache files safely
- **Directory Cleanup**: Clean up build artifacts and generated files
- **Permission Validation**: Ensure proper permissions for cleanup operations
- **Dry Run Mode**: Preview cleanup operations before execution
- **Rollback Preparation**: Prepare for cleanup reversal if needed

**Cleanup Categories**:
- **Cache Files**: Python cache files (__pycache__, *.pyc)
- **Build Artifacts**: Distribution and build directories
- **Temporary Files**: Temporary files and directories
- **Log Archives**: Compress and archive old log files
- **Dependency Cleanup**: Remove unused dependency files

---

## 🖥️ **WORKSPACE MANAGEMENT UTILITIES**

### **4. Workspace Coordinate Validation**
```bash
python scripts/validate_workspace_coords.py
```

**Description**: Validation script for agent workspace coordinates and PyAutoGUI integration setup.

**Validation Operations**:
- **Coordinate Verification**: Validate all agent coordinates are within screen bounds
- **Multi-Monitor Support**: Ensure compatibility with multi-monitor configurations
- **PyAutoGUI Integration**: Test coordinate accessibility and click accuracy
- **Configuration Backup**: Create backups before coordinate modifications

**Validation Checks**:
- **Screen Boundaries**: Ensure coordinates are within display area
- **Monitor Configuration**: Detect and validate multi-monitor setups
- **Coordinate Accessibility**: Verify PyAutoGUI can reach target coordinates
- **Configuration Integrity**: Validate coordinate configuration file structure

**Multi-Monitor Support**:
```bash
# Validate coordinates for dual-monitor setup
python scripts/validate_workspace_coords.py --monitors 2

# Test specific agent coordinate
python scripts/validate_workspace_coords.py --agent Agent-1 --test

# Export validation report
python scripts/validate_workspace_coords.py --export validation_report.json
```

### **5. Status Embedding Refresh**
```bash
python scripts/status_embedding_refresh.py
```

**Description**: Status embedding system refresh and synchronization utility.

**Refresh Operations**:
- **Embedding Updates**: Refresh all status embeddings in vector database
- **Synchronization**: Ensure consistency between status files and embeddings
- **Performance Optimization**: Optimize embedding retrieval and search performance
- **Integrity Validation**: Validate embedding accuracy and completeness
- **Cache Management**: Manage embedding cache and memory usage

**Refresh Options**:
```bash
# Full embedding refresh
python scripts/status_embedding_refresh.py --full

# Incremental refresh (only changed files)
python scripts/status_embedding_refresh.py --incremental

# Refresh specific agent embeddings
python scripts/status_embedding_refresh.py --agent Agent-2

# Performance optimization
python scripts/status_embedding_refresh.py --optimize
```

---

## 📊 **DEVELOPMENT WORKFLOW UTILITIES**

### **6. Terminal Completion Monitor**
```bash
python scripts/terminal_completion_monitor.py
```

**Description**: Terminal command completion monitoring and validation system.

**Monitoring Features**:
- **Command Tracking**: Monitor terminal command execution and completion
- **Success Validation**: Validate command execution success rates
- **Error Detection**: Identify and report command failures
- **Performance Metrics**: Track command execution times and resource usage
- **Log Analysis**: Analyze command execution patterns and anomalies

**Monitoring Capabilities**:
- **Real-time Tracking**: Live monitoring of command execution
- **Success Rate Analysis**: Calculate command success percentages
- **Performance Profiling**: Track execution time and resource consumption
- **Error Pattern Detection**: Identify recurring command failures
- **Historical Analysis**: Analyze command execution trends over time

### **7. Snapshot Management**
```bash
python tools/captain_snapshot.py
```

**Description**: System snapshot creation and management utility for Captain's oversight.

**Snapshot Features**:
- **System State Capture**: Capture complete system state and configuration
- **Agent Status Snapshot**: Record all agent statuses and activities
- **Configuration Backup**: Backup all system configurations
- **Change Tracking**: Track system changes between snapshots
- **Recovery Preparation**: Prepare for system recovery if needed

**Snapshot Types**:
- **Full System Snapshot**: Complete system state capture
- **Agent Status Snapshot**: Agent-specific status and configuration
- **Configuration Snapshot**: System configuration backup
- **Change Snapshot**: Track modifications between snapshots

### **8. Check Snapshot Update**
```bash
python tools/check_snapshot_up_to_date.py
```

**Description**: Validation utility to check if system snapshots are current and valid.

**Validation Operations**:
- **Snapshot Freshness**: Verify snapshots are up-to-date
- **Integrity Checking**: Validate snapshot file integrity
- **Configuration Comparison**: Compare current configuration with snapshots
- **Change Detection**: Identify changes since last snapshot
- **Update Recommendations**: Suggest when snapshots should be updated

---

## 🔄 **MAINTENANCE WORKFLOWS**

### **Complete System Maintenance Workflow**
```bash
# 1. Validate workspace coordinates
python scripts/validate_workspace_coords.py --monitors 2

# 2. Find and analyze large files
python scripts/utilities/find_large_files.py --type py --size 100KB

# 3. Auto-remediate LOC violations
python tools/auto_remediate_loc.py --backup --dry-run

# 4. Refresh status embeddings
python scripts/status_embedding_refresh.py --incremental

# 5. Monitor terminal completion
python scripts/terminal_completion_monitor.py --background

# 6. Create system snapshot
python tools/captain_snapshot.py --full

# 7. Validate snapshot integrity
python tools/check_snapshot_up_to_date.py

# 8. Safe cleanup
python tools/cleanup_guarded.sh --dry-run
```

### **Daily Maintenance Workflow**
```bash
# 1. Coordinate validation
python scripts/validate_workspace_coords.py --quick

# 2. Status embedding refresh
python scripts/status_embedding_refresh.py --incremental

# 3. Terminal monitoring
python scripts/terminal_completion_monitor.py --daily-report

# 4. Quick cleanup
python tools/cleanup_guarded.sh --cache-only
```

### **Pre-Deployment Maintenance Workflow**
```bash
# 1. Full system validation
python scripts/validate_workspace_coords.py --full

# 2. Large file analysis
python scripts/utilities/find_large_files.py --critical-only

# 3. LOC compliance check
python tools/auto_remediate_loc.py --check-only

# 4. System snapshot
python tools/captain_snapshot.py --pre-deploy

# 5. Configuration backup
python tools/check_snapshot_up_to_date.py --backup-config
```

---

## 📋 **UTILITY QUICK REFERENCE**

| Utility Category | Primary Command | Purpose | Key Options |
|------------------|-----------------|---------|-------------|
| **File Analysis** | `scripts/utilities/find_large_files.py` | Large file detection | `--type`, `--size`, `--directory` |
| **Auto Remediation** | `tools/auto_remediate_loc.py` | LOC violation fixes | `--backup`, `--dry-run` |
| **System Cleanup** | `tools/cleanup_guarded.sh` | Safe cleanup | `--dry-run`, `--cache-only` |
| **Coordinate Validation** | `scripts/validate_workspace_coords.py` | Workspace validation | `--monitors`, `--agent` |
| **Embedding Refresh** | `scripts/status_embedding_refresh.py` | Status sync | `--full`, `--incremental` |
| **Terminal Monitor** | `scripts/terminal_completion_monitor.py` | Command monitoring | `--background`, `--daily-report` |
| **Snapshot Creation** | `tools/captain_snapshot.py` | System snapshots | `--full`, `--agent` |
| **Snapshot Validation** | `tools/check_snapshot_up_to_date.py` | Snapshot checking | `--backup-config` |

---

## ⚙️ **CONFIGURATION & CUSTOMIZATION**

### **Utility Configuration File**
```json
{
  "utilities": {
    "file_analysis": {
      "default_size_threshold": "100KB",
      "excluded_directories": ["node_modules", ".git", "__pycache__"],
      "included_extensions": [".py", ".js", ".ts", ".java"],
      "export_formats": ["json", "csv", "text"]
    },
    "auto_remediation": {
      "backup_enabled": true,
      "dry_run_default": true,
      "max_file_size": "400KB",
      "safety_checks": true,
      "rollback_enabled": true
    },
    "cleanup": {
      "safe_mode": true,
      "excluded_patterns": ["*.log", "*.config"],
      "retention_days": 30,
      "compression_enabled": true
    },
    "workspace_validation": {
      "multi_monitor_support": true,
      "screen_bounds_check": true,
      "pyautogui_timeout": 5,
      "retry_attempts": 3
    }
  }
}
```

### **Performance Tuning**
```bash
# Optimize file analysis performance
export FILE_ANALYSIS_CHUNK_SIZE=1000
export FILE_ANALYSIS_MAX_WORKERS=4

# Configure cleanup safety
export CLEANUP_SAFETY_LEVEL=high
export CLEANUP_BACKUP_RETENTION=7

# Tune validation timeouts
export VALIDATION_TIMEOUT=10
export COORDINATE_RETRY_DELAY=1
```

---

## 🚨 **TROUBLESHOOTING & SAFETY**

### **Common Utility Issues & Solutions**

**Issue**: Auto-remediation fails with backup errors
**Solution**: Check disk space and permissions, clean up old backups
```bash
# Check disk space
df -h

# Clean old backups
find backups/ -name "*.bak" -mtime +30 -delete

# Retry with increased timeout
python tools/auto_remediate_loc.py --timeout 300
```

**Issue**: Coordinate validation fails on multi-monitor setup
**Solution**: Update monitor configuration and recalibrate coordinates
```bash
# Detect monitors
python scripts/validate_workspace_coords.py --detect-monitors

# Recalibrate coordinates
python scripts/validate_workspace_coords.py --recalibrate

# Update configuration
python scripts/validate_workspace_coords.py --update-config
```

**Issue**: Large file analysis is slow
**Solution**: Optimize analysis parameters and use parallel processing
```bash
# Use parallel processing
export FILE_ANALYSIS_WORKERS=8

# Limit analysis scope
python scripts/utilities/find_large_files.py --directory src/ --max-depth 3

# Use incremental analysis
python scripts/utilities/find_large_files.py --incremental
```

**Issue**: Status embedding refresh consumes too much memory
**Solution**: Use incremental refresh and memory optimization
```bash
# Incremental refresh
python scripts/status_embedding_refresh.py --incremental --batch-size 100

# Memory optimization
export EMBEDDING_BATCH_SIZE=50
export EMBEDDING_MEMORY_LIMIT=512MB
```

### **Safety Precautions**
- **Always Backup**: Create backups before running remediation tools
- **Dry Run First**: Use `--dry-run` flag to preview operations
- **Test Environment**: Test utilities in development environment first
- **Monitor Resources**: Watch system resources during intensive operations
- **Version Control**: Commit changes before running utilities

---

## 📈 **INTEGRATION WITH SWARM OPERATIONS**

### **Captain's Utility Oversight**
- **Daily Validation**: Run coordinate validation and status checks daily
- **Weekly Maintenance**: Execute cleanup and optimization weekly
- **Monthly Analysis**: Run comprehensive file analysis monthly
- **Pre-Deployment**: Execute full validation before deployments

### **Agent Integration Points**
- **Workspace Validation**: Agents validate their workspace coordinates
- **Status Synchronization**: Agents ensure status embeddings are current
- **File Management**: Agents use file analysis for code optimization
- **Maintenance Coordination**: Agents participate in coordinated maintenance

### **Automated Maintenance Integration**
- **Scheduled Tasks**: Automated execution of maintenance utilities
- **Health Monitoring**: Continuous monitoring of system health
- **Alert Integration**: Automated alerts for maintenance issues
- **Recovery Procedures**: Automated recovery from maintenance failures

---

**✅ UTILITIES SYSTEM COMPLETE**
**8 Utilities Documented | All Workflows Covered | System Maintenance Ready**

**Ready for comprehensive system maintenance and utility operations!** 🚀⚡
