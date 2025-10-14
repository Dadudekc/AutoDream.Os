# Lean Excellence Framework - Violations to Fix

## 🔴 CRITICAL VIOLATIONS (>600 lines) - 8 files

### Tier 1: Extreme Violations (>750 lines)

1. **thea_login_handler.py** - 819 lines (EXCEEDS by 219)
   - **Priority**: CRITICAL
   - **Recommended Agent**: Agent-2 (Architecture & Design)
   - **Effort**: High (needs major refactoring)
   - **Strategy**: Split into login_detector, login_executor, cookie_manager

2. **tools/autonomous_task_engine.py** - 797 lines (EXCEEDS by 197)
   - **Priority**: CRITICAL
   - **Recommended Agent**: Agent-5 (Business Intelligence) or Agent-8 (SSOT)
   - **Effort**: High (core autonomy logic)
   - **Strategy**: Extract task discovery, scoring, reporting to separate modules

3. **tools_v2/categories/captain_tools.py** - 789 lines (EXCEEDS by 189)
   - **Priority**: CRITICAL
   - **Recommended Agent**: Agent-4 (Captain) - self-refactor
   - **Effort**: High (10 classes, 30 functions)
   - **Strategy**: Split into captain_tools_core.py, captain_tools_advanced.py, captain_tools_monitoring.py

4. **tools_v2/categories/intelligent_mission_advisor.py** - 787 lines (EXCEEDS by 187)
   - **Priority**: CRITICAL
   - **Recommended Agent**: Agent-5 (Business Intelligence)
   - **Effort**: High (complex advisor logic)
   - **Strategy**: Extract mission_scanner.py, mission_validator.py, mission_briefing.py

### Tier 2: Major Violations (600-700 lines)

5. **comprehensive_project_analyzer_BACKUP_PRE_REFACTOR.py** - 670 lines (EXCEEDS by 70)
   - **Priority**: LOW (backup file - can delete or archive)
   - **Recommended Agent**: Agent-3 (Formatting & Infrastructure)
   - **Effort**: Minimal (archive to backups/)

6. **comprehensive_project_analyzer.py** - 645 lines (EXCEEDS by 45)
   - **Priority**: HIGH
   - **Recommended Agent**: Agent-1 (Syntax & Imports) or Agent-3
   - **Effort**: Medium
   - **Strategy**: Extract chunking logic, analysis logic, reporting logic

7. **tools_v2/categories/swarm_mission_control.py** - 629 lines (EXCEEDS by 29)
   - **Priority**: HIGH
   - **Recommended Agent**: Agent-8 (SSOT & Systematic Compliance)
   - **Effort**: Medium
   - **Strategy**: Extract swarm_state_reader.py, mission_calculator.py

8. **tools/dashboard_html_generator.py** - 622 lines (EXCEEDS by 22)
   - **Priority**: MEDIUM
   - **Recommended Agent**: Agent-7 (Web Development)
   - **Effort**: Medium
   - **Strategy**: Extract CSS to separate file, split chart generation

---

## 🟡 WARNINGS (500-600 lines) - 7 files

### High Priority (approaching 600)

9. **tools/agent_mission_controller.py** - 593 lines
   - **Recommended Agent**: Agent-2 or Agent-5
   - **Effort**: Medium
   - **Strategy**: Extract pattern DB, mission analysis to separate modules

10. **run_discord_commander.py** - 562 lines
    - **Recommended Agent**: Agent-7 (Web Development) or Agent-6
    - **Effort**: Medium
    - **Strategy**: Extract command handlers to separate files

11. **tools/swarm_orchestrator.py** - 552 lines
    - **Recommended Agent**: Agent-8 (SSOT)
    - **Effort**: Medium
    - **Strategy**: Extract gas messaging, task creation to separate modules

### Medium Priority (550-510 lines)

12. **tools/documentation_assistant.py** - 538 lines
    - **Recommended Agent**: Agent-6 (Coordination & Communication)
    - **Effort**: Low-Medium
    - **Strategy**: Extract template generators to separate module

13. **analyze_src_directories.py** - 514 lines
    - **Recommended Agent**: Agent-1 or Agent-3
    - **Effort**: Low
    - **Strategy**: Extract analysis logic, reporting logic

14. **tools/cleanup_documentation.py** - 512 lines
    - **Recommended Agent**: Agent-3 (Infrastructure)
    - **Effort**: Low
    - **Strategy**: Extract deduplication, archiving logic

15. **src/integrations/osrs/osrs_agent_core.py** - 505 lines
    - **Recommended Agent**: Agent-1 or Agent-2
    - **Effort**: Medium
    - **Strategy**: Extract game logic, automation logic to separate modules

---

## 📊 SUMMARY & ROI ANALYSIS

### By Priority
- **CRITICAL (>750 lines)**: 4 files - 3,192 lines total
- **HIGH (600-750 lines)**: 4 files - 2,566 lines total  
- **WARNINGS (500-600 lines)**: 7 files - 3,776 lines total

**TOTAL**: 15 files, 9,534 lines to refactor

### Recommended Agent Assignments

| Agent | Files Assigned | Total Lines | Estimated Points |
|-------|----------------|-------------|------------------|
| Agent-1 (Syntax) | 2-3 files | ~1,500 | 400-600 pts |
| Agent-2 (Architecture) | 2-3 files | ~2,000 | 600-800 pts |
| Agent-3 (Infrastructure) | 2-3 files | ~1,200 | 300-500 pts |
| Agent-4 (Captain) | 1 file | 789 | 300-400 pts |
| Agent-5 (Business Intel) | 2-3 files | ~2,000 | 600-800 pts |
| Agent-6 (Coordination) | 1-2 files | ~1,000 | 300-400 pts |
| Agent-7 (Web Dev) | 1-2 files | ~1,200 | 400-500 pts |
| Agent-8 (SSOT) | 2-3 files | ~1,800 | 500-700 pts |

### Estimated Campaign
- **Duration**: 2-3 weeks (with 8 agents)
- **Total Points Available**: 3,600-5,200 pts
- **Average per Agent**: 450-650 pts
- **ROI**: High (improves codebase quality, demonstrates Lean Excellence)

---

## 🎯 IMMEDIATE ACTIONS

### Phase 1: Critical Files (Week 1)
1. Agent-2: thea_login_handler.py (819 lines → 3 files <300 each)
2. Agent-5: autonomous_task_engine.py (797 lines → 3 files <300 each)
3. Agent-4: captain_tools.py (789 lines → 3 files <300 each)
4. Agent-5: intelligent_mission_advisor.py (787 lines → 3 files <300 each)

### Phase 2: Major Violations (Week 2)
5. Agent-3: Archive BACKUP file, refactor main analyzer
6. Agent-8: swarm_mission_control.py (629 → 2 files <400)
7. Agent-7: dashboard_html_generator.py (622 → 2 files <400)

### Phase 3: Warnings (Week 3)
8-15. Distribute remaining 7 files across agents based on availability

---

## 📋 SUCCESS CRITERIA

### File-Level
- ✅ All Python files ≤600 lines (hard cap)
- ✅ Target ≤400 lines (preferred)
- ✅ Functions ≤30 lines
- ✅ Classes ≤200 lines

### Quality
- ✅ All tests passing
- ✅ Functionality preserved
- ✅ Imports updated correctly
- ✅ Documentation updated

### Process
- ✅ Pre-commit hooks pass
- ✅ No linter errors
- ✅ STANDARDS.md compliance verified

---

## 🚀 NEXT STEPS

1. **Immediate**: Create execution orders for Phase 1 (4 critical files)
2. **Captain**: Assign tasks via mission control system
3. **Agents**: Claim tasks, execute refactoring
4. **Validation**: Run file size checker, verify compliance
5. **Recognition**: Award points for successful refactoring

**Lean Excellence Framework in Action!** 🐝

---

**Generated**: 2025-10-14  
**By**: Agent-4 (Captain & Strategic Oversight)  
**Framework**: Lean Excellence  
**Status**: Ready for agent assignment

