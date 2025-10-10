# 🔧 Technical Debt Scan Report

**Scan Path:** .
**Total Markers Found:** 315

## 📊 Summary

| Marker Type | Count | Priority |
|-------------|-------|----------|
| BUG | 79 | P0 - Critical |
| REFACTOR | 71 | P3 - Low |
| DEPRECATED | 55 | P2 - Medium |
| XXX | 50 | P1 - High |
| TODO | 43 | P1 - High |
| FIXME | 17 | P0 - Critical |

## BUG (79 instances)

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

### `PRIORITY_4_TECHNICAL_DEBT_SUMMARY.md` (18 instances)

**Line 7:**
```
- **80 BUG markers** (P0 - Critical)
```

**Line 17:**
```
- **80 BUG markers** - Need immediate review
```

**Line 34:**
```
3. ✅ **TECHNICAL_DEBT_REPORT.md** - Detailed BUG report (auto-generated)
```

**Line 52:**
```
# Scan for BUG markers only
```

**Line 53:**
```
python scan_technical_debt.py --type BUG
```

*... and 13 more*

### `WEEK_1_CHAT_MATE_IMPLEMENTATION_PLAN.md` (1 instances)

**Line 376:**
```
- Remove any debug code
```

### `agent_workspaces\Captain\AGENT-1_C004-C009_COMPLETION_REPORT.md` (3 instances)

**Line 19:**
```
- Fixed critical bug in Discord agent communication (path.join issue)
```

**Line 77:**
```
Bugs Fixed:            1 (production bug in Discord)
```

**Line 120:**
```
- `src/discord_commander/discord_agent_communication.py` (bug fix)
```

### `agent_workspaces\Captain\AGENT-1_VECTOR_CONSOLIDATION_COMPLETE.md` (1 instances)

**Line 182:**
```
1. ✅ C-004: Discord Commands Testing & Bug Fix
```

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

### `src\domain\ports\logger.py` (3 instances)

**Line 16:**
```
DEBUG = "DEBUG"
```

**Line 27:**
```
This protocol allows domain objects to log events and debug information
```

**Line 33:**
```
Log debug message.
```

### `src\infrastructure\logging\std_logger.py` (2 instances)

**Line 33:**
```
LogLevel.DEBUG: logging.DEBUG,
```

**Line 43:**
```
Log debug message.
```

### `src\infrastructure\unified_logging_time.py` (7 instances)

**Line 35:**
```
DEBUG = "DEBUG"
```

**Line 70:**
```
"""Log debug message."""
```

**Line 164:**
```
LogLevel.DEBUG: logging.DEBUG,
```

**Line 211:**
```
LogLevel.DEBUG: logging.DEBUG,
```

**Line 220:**
```
"""Log debug message."""
```

*... and 2 more*

*... and 8 more files*

## REFACTOR (71 instances)

### `.analysis\consolidation_opportunities.md` (5 instances)

**Line 380:**
```
| 3a | Refactor `core_monitoring_manager.py` | High | Medium | High | 8-12 |
```

**Line 381:**
```
| 3b | Refactor `core_resource_manager.py` | High | Medium | High | 8-12 |
```

**Line 382:**
```
| 3c | Refactor `base_execution_manager.py` | High | Medium | High | 8-12 |
```

**Line 383:**
```
| 3d | Refactor `base_monitoring_manager.py` | High | Medium | High | 8-12 |
```

**Line 428:**
```
1. Refactor large manager files one by one
```

### `AGENTS.md` (2 instances)

**Line 104:**
```
- 401–600 lines: **MAJOR VIOLATION** requiring refactor
```

**Line 105:**
```
- >600 lines: immediate refactor
```

### `PRIORITY_4_TECHNICAL_DEBT_CLEANUP_REPORT.md` (2 instances)

**Line 241:**
```
**Action:** Refactor when browser automation needs change
```

**Line 367:**
```
2. Refactor browser session management when time permits
```

### `PRIORITY_4_TECHNICAL_DEBT_SUMMARY.md` (4 instances)

**Line 10:**
```
- **45 REFACTOR markers** (P3 - Low, historical)
```

**Line 28:**
```
- **45 REFACTOR markers** - Historical documentation
```

**Line 107:**
```
### **Phase 4: REFACTOR - Update Docs**
```

**Line 109:**
```
# Most REFACTOR markers are historical
```

### `README.md` (2 instances)

**Line 398:**
```
- **Agent-2 (SOLID Marshal)**: Refactor to SOLID; enforce sub-300 LOC files
```

**Line 401:**
```
- **Agent-5 (TDD Architect)**: Red/Green/Refactor loop; seed smoke/e2e
```

### `__init__.py` (1 instances)

**Line 40:**
```
from . import test_solid_refactor  # noqa: F401
```

### `agent_workspaces\Agent-5\AGENT-2_ANALYTICS_REVIEW.md` (2 instances)

**Line 108:**
```
- ⚠️ **>600 lines** = IMMEDIATE REFACTOR required
```

**Line 238:**
```
- >600 lines = IMMEDIATE REFACTOR
```

### `agent_workspaces\Agent-6\V2_COMPLIANCE_IMPLEMENTATION_PLAN.md` (1 instances)

**Line 52:**
```
- Refactor to maintain under 300-line limit
```

### `archive\onboarding\README_onboarding.md` (1 instances)

**Line 116:**
```
3. Refactor duplication and clarify intent in every revision
```

### `docs\AGENTS_FIRST_CYCLE_COMPLETION_REPORT.md` (1 instances)

**Line 236:**
```
- V2 refactored modules: 8 (resource ops, config, refactor helpers)
```

### `docs\AGENT_ONBOARDING_GUIDE.md` (2 instances)

**Line 129:**
```
- 401–600 lines: **MAJOR VIOLATION** requiring refactor
```

**Line 130:**
```
- >600 lines: immediate refactor
```

### `docs\COMPREHENSIVE_PROJECT_TASK_LIST.md` (1 instances)

**Line 78:**
```
- **Action**: Refactor all violations
```

### `docs\CYCLE_TIMELINE.md` (2 instances)

**Line 86:**
```
| C-023 | Agent-5 | **CYCLE 2/3**: Refactor to V2: Create persistent_memory_core.py + _storage.py (≤400 lines each). #DONE-C023 | Agent-5 continues C-024 | CRITICAL-COMPLEX |
```

**Line 99:**
```
| C-027 | Agent-5 | **CYCLE 2/2**: Refactor to V2: ml_pipeline_core.py + processors.py (≤400 each). Test pipeline. #DONE-C027 | Agent-8 documents C-034 | MEDIUM |
```

### `docs\REFACTORING_SUGGESTIONS_GUIDE.md` (2 instances)

**Line 237:**
```
Before starting to refactor a large file:
```

**Line 245:**
```
During code review, check if new code needs refactoring:
```

### `docs\V2_COMPLIANCE_CHECKER_GUIDE.md` (4 instances)

**Line 149:**
```
| **CRITICAL** | 🔴 | File >600 lines | Immediate refactor |
```

**Line 150:**
```
| **MAJOR** | 🟡 | File >400 lines or rule violation | Refactor required |
```

**Line 382:**
```
- Don't refactor all at once
```

**Line 384:**
```
- Test after each refactor
```

### `docs\V2_COMPLIANCE_EXCEPTIONS.md` (1 instances)

**Line 61:**
```
4. Approve or refactor
```

### `docs\architecture\orchestrator-pattern.md` (2 instances)

**Line 314:**
```
- **Migration**: Existing orchestrators would need refactoring
```

**Line 431:**
```
**Solution**: Refactor to single orchestrator or component hierarchy
```

### `docs\consolidation\WEEK_1-2_CONSOLIDATION_TRACKING.md` (1 instances)

**Line 487:**
```
- **V2 Compliance Status**: ~60% compliant, 40% needs refactoring
```

### `docs\reports\AGENT-7_WEB_INTERFACE_ANALYSIS.md` (1 instances)

**Line 17:**
```
- **V2 Compliance Status**: ~60% compliant, 40% needs refactoring
```

### `docs\sprints\AGENT-1_SPRINT.md` (2 instances)

**Line 95:**
```
- [ ] Refactor to V2 compliance (≤400 lines each)
```

**Line 121:**
```
- [ ] Refactor to V2 compliance (≤400 lines each)
```

*... and 24 more files*

## DEPRECATED (55 instances)

### `EMPTY_SUBDIRECTORIES_INVESTIGATION_REPORT.md` (1 instances)

**Line 248:**
```
- Removed 50+ deprecated files
```

### `PRIORITY_4_TECHNICAL_DEBT_CLEANUP_REPORT.md` (14 instances)

**Line 17:**
```
| **Phase 1: Deprecated Stubs** | ✅ **COMPLETE** | Removed 2 stub files, updated all imports |
```

**Line 24:**
```
## ✅ Phase 1: Deprecated Stub Files (COMPLETE)
```

**Line 27:**
```
1. ✅ `src/utils/config_core.py` - Deprecated stub file
```

**Line 28:**
```
2. ✅ `src/services/messaging_core.py` - Deprecated stub file
```

**Line 51:**
```
053c96e8d - chore(technical-debt): remove deprecated stub files and update imports
```

*... and 9 more*

### `PRIORITY_4_TECHNICAL_DEBT_SUMMARY.md` (11 instances)

**Line 11:**
```
- **39 DEPRECATED markers** (P2 - Medium)
```

**Line 25:**
```
- **39 DEPRECATED markers** - Old code to clean up
```

**Line 96:**
```
### **Phase 3: DEPRECATED - 1-2 hours**
```

**Line 98:**
```
# 1. Generate DEPRECATED report
```

**Line 99:**
```
python scan_technical_debt.py --type DEPRECATED
```

*... and 6 more*

### `SRC_REDUNDANCY_ANALYSIS_REPORT.md` (1 instances)

**Line 319:**
```
- **Files removed:** 50+ deprecated files (_v2, _refactored, etc.)
```

### `scan_technical_debt.py` (1 instances)

**Line 28:**
```
'DEPRECATED': r'DEPRECATED[:\s]|@deprecated',
```

### `src\core\ssot\DEPRECATION_NOTICE.md` (4 instances)

**Line 22:**
```
## 🗑️ **Deprecated Files (Do Not Use)**
```

**Line 80:**
```
- **Version 4.0.0** (Future): Deprecated files removed
```

**Line 88:**
```
### **Files Removed**: 50+ deprecated files
```

**Line 103:**
```
1. **Identify deprecated imports** in your code
```

### `src\core\ssot\NAMING_CONVENTIONS.md` (7 instances)

**Line 10:**
```
- **Legacy/deprecated files**: `{system_name}_{status}.py` (e.g., `ssot_execution_coordinator_legacy.py`)
```

**Line 15:**
```
- `_legacy.py` - Legacy/deprecated implementations
```

**Line 97:**
```
## 🚫 **Deprecated Naming Patterns**
```

**Line 106:**
```
- **Mark deprecated files** with `_deprecated.py` suffix
```

**Line 108:**
```
- **Create migration guides** for deprecated functionality
```

*... and 2 more*

### `src\infrastructure\browser\unified\legacy_driver.py` (2 instances)

**Line 4:**
```
DEPRECATED: Use UnifiedDriverManager directly.
```

**Line 20:**
```
DEPRECATED: This class is provided for backward compatibility only.
```

### `src\web\static\js\architecture\dependency-injection-framework.js` (4 instances)

**Line 28:**
```
* @deprecated Use DIFrameworkOrchestrator directly
```

**Line 43:**
```
* @deprecated Use DIFrameworkOrchestrator directly
```

**Line 54:**
```
* @deprecated Use DIFrameworkOrchestrator directly
```

**Line 65:**
```
* @deprecated Use DIFrameworkOrchestrator directly
```

### `src\web\static\js\architecture\di-framework-orchestrator.js` (4 instances)

**Line 133:**
```
* @deprecated Use DIFrameworkOrchestrator instead
```

**Line 144:**
```
* @deprecated Use DIFrameworkOrchestrator instead
```

**Line 155:**
```
* @deprecated Use DIFrameworkOrchestrator instead
```

**Line 166:**
```
* @deprecated Use DIFrameworkOrchestrator instead
```

### `src\web\static\js\dashboard\dom-utils-orchestrator.js` (1 instances)

**Line 259:**
```
* @deprecated Use DOMUtilsOrchestrator instead
```

### `src\web\static\js\performance\performance-optimization-orchestrator.js` (1 instances)

**Line 165:**
```
* @deprecated Use PerformanceOptimizationOrchestrator instead
```

### `src\web\static\js\performance\performance-optimization-report.js` (1 instances)

**Line 165:**
```
* @deprecated Use PerformanceOptimizationOrchestrator instead
```

### `src\web\static\js\services-orchestrator.js` (1 instances)

**Line 334:**
```
* @deprecated Use new ServicesOrchestrator class directly
```

### `src\web\static\js\trading-robot\chart-navigation-module.js` (1 instances)

**Line 40:**
```
* @deprecated Use ChartNavigationModule instead
```

### `src\web\static\js\trading-robot\chart-state-module.js` (1 instances)

**Line 42:**
```
* @deprecated Use ChartStateModule instead
```

## XXX (50 instances)

### `PRIORITY_4_TECHNICAL_DEBT_SUMMARY.md` (2 instances)

**Line 12:**
```
- **1 XXX marker** (P1 - High)
```

**Line 22:**
```
- **1 XXX marker** - Critical review needed
```

### `agent_workspaces\Agent-2\inbox\C2A_CAPTAIN_WEEK_1-2_EXECUTION_AUTHORIZATION.md` (2 instances)

**Line 205:**
```
CYCLE: C-XXX
```

**Line 211:**
```
#DONE-CXXX
```

### `agent_workspaces\Agent-3\C-003_STATUS_REPORT.md` (2 instances)

**Line 66:**
```
CYCLE: C-XXX | OWNER: Agent-3
```

**Line 68:**
```
#DONE-CXXX
```

### `docs\AGENTS_FIRST_CYCLE_COMPLETION_REPORT.md` (2 instances)

**Line 322:**
```
4. ✅ #DONE-Cxxx tags enabled progress tracking
```

**Line 348:**
```
- #DONE-Cxxx tags used consistently
```

### `docs\CAPTAIN_REVIEW_COMPLETION_REPORT.md` (4 instances)

**Line 91:**
```
- ✅ **Anti-loop safeguards** (#DONE-Cxxx tags)
```

**Line 248:**
```
- ✅ #DONE-Cxxx tag system implemented
```

**Line 299:**
```
5. ✅ Respond to #BLOCKED-Cxxx immediately
```

**Line 360:**
```
- **Anti-loop safeguards** (#DONE-Cxxx tags)
```

### `docs\CAPTAIN_TRACKING_SUMMARY.md` (4 instances)

**Line 533:**
```
2. **Use #DONE-Cxxx tag**: Every cycle must end with this tag
```

**Line 536:**
```
5. **Blocked protocol**: Use #BLOCKED-Cxxx for immediate escalation
```

**Line 540:**
```
CYCLE: C-XXX
```

**Line 545:**
```
#DONE-CXXX
```

### `docs\CUSTOM_AGENT_ONBOARDING_COMPLETE.md` (3 instances)

**Line 128:**
```
- #DONE-Cxxx tag requirements
```

**Line 143:**
```
CYCLE: C-XXX | OWNER: Agent-X
```

**Line 145:**
```
#DONE-CXXX
```

### `docs\CYCLE_TIMELINE.md` (11 instances)

**Line 33:**
```
CYCLE: C-XXX
```

**Line 38:**
```
#DONE-CXXX
```

**Line 342:**
```
✅ CYCLE: C-XXX
```

**Line 348:**
```
✅ #DONE-CXXX
```

**Line 378:**
```
- Use #DONE-Cxxx tag consistently
```

*... and 6 more*

### `docs\CYCLE_TIMELINE_IMPLEMENTATION.md` (9 instances)

**Line 43:**
```
- Clear #BLOCKED-Cxxx format
```

**Line 116:**
```
### Rule 2: Use #DONE-Cxxx Tag
```

**Line 126:**
```
Use #BLOCKED-Cxxx for immediate escalation, don't wait for checkpoint.
```

**Line 172:**
```
- **Measure**: Count #DONE-Cxxx tags vs total responses
```

**Line 197:**
```
CYCLE: C-XXX
```

*... and 4 more*

### `docs\FIRST_CYCLE_VALIDATION_COMPLETE.md` (4 instances)

**Line 34:**
```
✅ **#DONE-Cxxx Tags**: Consistent use prevented acknowledgment loops
```

**Line 44:**
```
3. ✅ Anti-loop safeguards working (#DONE-Cxxx tags)
```

**Line 169:**
```
1. ✅ **Cycle-based execution prevents loops**: #DONE-Cxxx tags essential
```

**Line 178:**
```
1. ✅ Cycle-based execution with #DONE-Cxxx tags
```

### `docs\SPRINT_DISTRIBUTION_COMPLETE.md` (7 instances)

**Line 38:**
```
- Anti-loop safeguards (#DONE-Cxxx tags)
```

**Line 134:**
```
### 2. Use #DONE-Cxxx Tag
```

**Line 144:**
```
Use #BLOCKED-Cxxx for immediate escalation (don't wait for checkpoint).
```

**Line 153:**
```
CYCLE: C-XXX
```

**Line 158:**
```
#DONE-CXXX
```

*... and 2 more*

## TODO (43 instances)

### `PRIORITY_4_TECHNICAL_DEBT_CLEANUP_REPORT.md` (7 instances)

**Line 79:**
```
- Line 150: `optimized_content = f"# TODO: {rule}\n{optimized_content}"`
```

**Line 81:**
```
- This dynamically generates TODO comments as part of code optimization suggestions
```

**Line 82:**
```
- Not a real TODO for us to fix - it's the tool's output format
```

**Line 120:**
```
- TODO comments for unfinished features
```

**Line 127:**
```
- **Action:** Create GitHub issues for each TODO
```

*... and 2 more*

### `PRIORITY_4_TECHNICAL_DEBT_RESOLVED.md` (16 instances)

**Line 15:**
```
### 1. TODO Comments in Extraction Tools ✅
```

**Line 23:**
```
return "# TODO: Implement proper model extraction\n"
```

**Line 27:**
```
return "# TODO: Implement proper utility extraction\n"
```

**Line 31:**
```
return "# TODO: Implement proper core extraction\n"
```

**Line 47:**
```
### 2. TODO Comments in Consolidation Task ✅
```

*... and 11 more*

### `PRIORITY_4_TECHNICAL_DEBT_SUMMARY.md` (8 instances)

**Line 9:**
```
- **23 TODO markers** (P1 - High)
```

**Line 21:**
```
- **23 TODO markers** - Action items to complete
```

**Line 55:**
```
# Scan for TODO markers
```

**Line 56:**
```
python scan_technical_debt.py --type TODO
```

**Line 87:**
```
# 1. Generate TODO report
```

*... and 3 more*

### `SRC_REDUNDANCY_ANALYSIS_REPORT.md` (4 instances)

**Line 121:**
```
- ⚠️ `src/web/static/js/dashboard/dom-utils-orchestrator.js` - Has TODO comments
```

**Line 123:**
```
- ⚠️ `src/web/static/js/trading-robot/chart-navigation-module.js` - Has TODO
```

**Line 124:**
```
- ⚠️ `src/web/static/js/trading-robot/chart-state-module.js` - Has TODO
```

**Line 240:**
```
- Review JavaScript files with TODO markers
```

### `agent_workspaces\Captain\AGENT-1_ONBOARDING_CONSOLIDATION_COMPLETE.md` (1 instances)

**Line 89:**
```
- Updated TODO status
```

### `devlogs\2025-10-09_agent-7_c-064_chat_mate_integration_complete.md` (1 instances)

**Line 266:**
```
2. **TODO List**: All C-064 TODOs marked complete
```

### `docs\standards\python_coding_standard.md` (1 instances)

**Line 19:**
```
- `Any` only behind an adapter boundary with TODO to tighten.
```

### `scan_technical_debt.py` (2 instances)

**Line 10:**
```
python scan_technical_debt.py --type TODO
```

**Line 218:**
```
print("   3. Address TODO items")
```

### `scripts\enforce_python_standards.py` (3 instances)

**Line 196:**
```
# Check for TODO comments without assignee
```

**Line 198:**
```
if "TODO" in line and "TODO:" not in line:
```

**Line 204:**
```
message="TODO comment should be formatted as 'TODO: description'",
```

## FIXME (17 instances)

### `PRIORITY_4_TECHNICAL_DEBT_CLEANUP_REPORT.md` (1 instances)

**Line 59:**
```
Originally identified 5 formal TODO/FIXME comments requiring action:
```

### `PRIORITY_4_TECHNICAL_DEBT_RESOLVED.md` (5 instances)

**Line 9:**
```
All Priority 4 technical debt items (TODO/FIXME comments and improper file naming) have been resolved.
```

**Line 101:**
```
- ✅ **0 FIXME comments** remaining
```

**Line 264:**
```
- **FIXME Comments:** 0
```

**Line 270:**
```
- **FIXME Comments:** 0 ✅
```

**Line 280:**
```
All TODO/FIXME comments have been properly implemented, and all improperly named files have been deleted with their functionality absorbed into the proper module locations. The codebase now maintains 100% V2 compliance with zero technical debt markers.
```

### `PRIORITY_4_TECHNICAL_DEBT_SUMMARY.md` (7 instances)

**Line 8:**
```
- **13 FIXME markers** (P0 - Critical)
```

**Line 18:**
```
- **13 FIXME markers** - Need fixes
```

**Line 58:**
```
# Scan for FIXME markers
```

**Line 59:**
```
python scan_technical_debt.py --type FIXME
```

**Line 133:**
```
- **Active FIXME markers** in code (need review)
```

*... and 2 more*

### `SRC_REDUNDANCY_ANALYSIS_REPORT.md` (3 instances)

**Line 122:**
```
- ⚠️ `src/web/static/js/architecture/di-framework-orchestrator.js` - Has TODO/FIXME (4 instances)
```

**Line 239:**
```
#### 4.1 Address TODO/FIXME Comments
```

**Line 352:**
```
💡 Address TODO/FIXME comments
```

### `scan_technical_debt.py` (1 instances)

**Line 217:**
```
print("   2. Prioritize BUG/FIXME markers")
```
