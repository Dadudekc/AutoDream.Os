# 🔧 Technical Debt Scan Report

**Scan Path:** .
**Total Markers Found:** 80

## 📊 Summary

| Marker Type | Count | Priority |
|-------------|-------|----------|
| BUG | 80 | P0 - Critical |

## BUG (80 instances)

### `.pre-commit-config-windows.yaml` (1 instances)

**Line 108:**
```
print(f'Debug statement found: {node.value.func.id}')
```

### `CLEANUP_GUIDE.md` (1 instances)

**Line 95:**
```
8. Debug import errors
```

### `DUPLICATE_CONSOLIDATION_SUMMARY.md` (1 instances)

**Line 69:**
```
2. ✅ **cleanup_obsolete_files.py** - Clean up old debug files (already used)
```

### `TECHNICAL_DEBT_ANALYSIS.md` (17 instances)

**Line 6:**
```
**Types:** TODO, FIXME, HACK, XXX, BUG, DEPRECATED, REFACTOR, DEBUG
```

**Line 40:**
```
### **4. DEBUG Code**
```

**Line 43:**
```
- `setup_thea_cookies.py` - Debug page state functions
```

**Line 44:**
```
- `thea_login_handler.py` - Debug logging (15+ instances)
```

**Line 47:**
```
**Status:** Legitimate debugging (keep) vs temporary debug code (remove)
```

*... and 12 more*

### `archive\onboarding\README_onboarding.md` (1 instances)

**Line 115:**
```
2. Write or update tests alongside any feature or bug fix
```

### `cleanup_obsolete_files.py` (1 instances)

**Line 6:**
```
Removes obsolete test/debug files that have been replaced by thea_automation.py.
```

### `devlogs\2025-09-06_17-22-48_general_Agent-7_Pre-commit_Hook_Debug_Fix_Completed.md` (2 instances)

**Line 1:**
```
# Agent-7: Pre-commit Hook Debug & Fix Task Completed
```

**Line 10:**
```
Ultimate System Validation Suite v98.0 executed with 100% success rate. Pre-commit hook debug and fix task completed with all 12 tests passing. Identified and addressed 26 syntax errors, 25 import issues, 26 formatting issues, and 4 configuration issues. Comprehensive analysis and recommendations provided for system-wide improvements. Autonomous cycle continuation active.
```

### `devlogs\autonomous_cycles\2025-09-04_autonomous-cycle-2_critical-violations-eliminated.md` (1 instances)

**Line 106:**
```
- **Bug Isolation**: Easier with modular design
```

### `devlogs\autonomous_cycles\2025-09-05_autonomous-cycle-3_major-violations-progress.md` (1 instances)

**Line 111:**
```
- **Debug Efficiency**: Isolated components simplify troubleshooting
```

### `devlogs\autonomous_cycles\2025-09-05_autonomous-cycle-4_zero-major-violations-achieved.md` (1 instances)

**Line 117:**
```
- **Bug Isolation**: Modular design simplifies debugging
```

### `devlogs\autonomous_cycles\2025-09-05_autonomous-cycle-5_dramatic-minor-violations-reduction.md` (1 instances)

**Line 107:**
```
- **Bug Isolation**: Clear component boundaries
```

### `docs\CONFIGURATION.md` (2 instances)

**Line 338:**
```
### Debug Mode
```

**Line 340:**
```
Enable debug logging to troubleshoot configuration issues:
```

### `docs\guides\DISCORD_COMMANDER_README.md` (2 instances)

**Line 279:**
```
### Debug Mode
```

**Line 280:**
```
Enable debug logging by setting environment variable:
```

### `docs\guides\HOW_TO_RUN_DISCORD_GUI.md` (1 instances)

**Line 163:**
```
### Run with Debug Logging
```

### `runtime\reports\pre_commit_debug_report.md` (3 instances)

**Line 1:**
```
# Pre-commit Hook Debug & Fix Report
```

**Line 4:**
```
**Task**: Debug and fix pre-commit hook issues
```

**Line 78:**
```
#### **4. Debug Statements Check** (Minor)
```

### `scripts\README.md` (1 instances)

**Line 154:**
```
python launch_performance_monitoring.py --config production --log-level DEBUG
```

### `setup_thea_cookies.py` (13 instances)

**Line 129:**
```
print("🔍 You'll see debug info every 15 seconds")
```

**Line 136:**
```
print("(Checking every 3 seconds - debug info every 15 seconds)")
```

**Line 145:**
```
# Debug page state every 15 seconds
```

**Line 168:**
```
"""Debug current page state for troubleshooting."""
```

**Line 172:**
```
print(f"🔍 DEBUG - Page: {title}")
```

*... and 8 more*

### `src\core\unified_logging_system_engine.py` (1 instances)

**Line 113:**
```
"""Log debug message."""
```

### `src\core\unified_logging_system_models.py` (1 instances)

**Line 21:**
```
DEBUG = "debug"
```

### `src\core\validation\README.md` (2 instances)

**Line 297:**
```
### Debug Mode
```

**Line 299:**
```
Enable debug logging for detailed validation information:
```

*... and 11 more files*
