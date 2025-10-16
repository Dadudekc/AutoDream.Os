# 🔍 TOOL RUNTIME AUDIT REPORT

**Date:** 2025-10-16T09:45:46.837365Z  
**Audited By:** Agent-3 (Infrastructure & DevOps)

## 📊 SUMMARY

**CLI Tools Tested:** 124  
**Working:** 78 (62.9%)  
**Broken:** 46 (37.1%)

---

## ❌ BROKEN TOOLS (46 total)

### `duplication_analyzer.py`
**Path:** tools\duplication_analyzer.py  
**Error:** Traceback (most recent call last):
  File "D:\Agent_Cellphone_V2_Repository\tools\duplication_analyzer.py", line 24, in <module>
    from tools.duplication_analysis import DuplicationAnalysis
  File "  

### `projectscanner.py`
**Path:** tools\projectscanner.py  
**Error:** Timeout (>5s)  

### `analyze_init_files.py`
**Path:** tools\analyze_init_files.py  
**Error:** Timeout (>5s)  

### `refactoring_suggestion_engine.py`
**Path:** tools\refactoring_suggestion_engine.py  
**Error:** Timeout (>5s)  

### `complexity_analyzer.py`
**Path:** tools\complexity_analyzer.py  
**Error:** Traceback (most recent call last):
  File "D:\Agent_Cellphone_V2_Repository\tools\complexity_analyzer.py", line 14, in <module>
    from .complexity_analyzer_cli import main
ImportError: attempted rel  

### `complexity_analyzer_cli.py`
**Path:** tools\complexity_analyzer_cli.py  
**Error:** Timeout (>5s)  

### `refactoring_cli.py`
**Path:** tools\refactoring_cli.py  
**Error:** Timeout (>5s)  

### `cleanup_documentation_refactored.py`
**Path:** tools\cleanup_documentation_refactored.py  
**Error:** Timeout (>5s)  

### `toolbelt.py`
**Path:** tools\toolbelt.py  
**Error:** Timeout (>5s)  

### `__main__.py`
**Path:** tools\__main__.py  
**Error:** Timeout (>5s)  

### `soft_onboard_cli.py`
**Path:** tools\soft_onboard_cli.py  
**Error:** Timeout (>5s)  

### `validate_imports.py`
**Path:** tools\validate_imports.py  
**Error:** Timeout (>5s)  

### `markov_task_optimizer.py`
**Path:** tools\markov_task_optimizer.py  
**Error:** Timeout (>5s)  

### `markov_cycle_simulator.py`
**Path:** tools\markov_cycle_simulator.py  
**Error:** Timeout (>5s)  

### `markov_8agent_roi_optimizer.py`
**Path:** tools\markov_8agent_roi_optimizer.py  
**Error:** Timeout (>5s)  

### `browser_pool_manager.py`
**Path:** tools\browser_pool_manager.py  
**Error:** Timeout (>5s)  

### `memory_leak_scanner.py`
**Path:** tools\memory_leak_scanner.py  
**Error:** Unknown  

### `git_commit_verifier.py`
**Path:** tools\git_commit_verifier.py  
**Error:** Unknown  

### `v2_compliance_batch_checker.py`
**Path:** tools\v2_compliance_batch_checker.py  
**Error:** Unknown  

### `coverage_validator.py`
**Path:** tools\coverage_validator.py  
**Error:** Unknown  

### `captain_gas_check.py`
**Path:** tools\captain_gas_check.py  
**Error:** Traceback (most recent call last):
  File "D:\Agent_Cellphone_V2_Repository\tools\captain_gas_check.py", line 91, in <module>
    check_agent_gas_levels()
  File "D:\Agent_Cellphone_V2_Repository\tool  

### `audit_cleanup.py`
**Path:** tools\audit_cleanup.py  
**Error:** File "D:\Agent_Cellphone_V2_Repository\tools\audit_cleanup.py", line 11
    from __future__ import annotations
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
SyntaxError: from __future__ imports must occur at  

### `auto_remediate_loc.py`
**Path:** tools\auto_remediate_loc.py  
**Error:** File "D:\Agent_Cellphone_V2_Repository\tools\auto_remediate_loc.py", line 16
    from __future__ import annotations
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
SyntaxError: from __future__ imports must occ  

### `generate_utils_catalog_enhanced.py`
**Path:** tools\generate_utils_catalog_enhanced.py  
**Error:** Timeout (>5s)  

### `integrity_validator.py`
**Path:** tools\integrity_validator.py  
**Error:** Traceback (most recent call last):
  File "D:\Agent_Cellphone_V2_Repository\tools\integrity_validator.py", line 15, in <module>
    from work_attribution_tool import WorkAttributionTool
  File "D:\Age  

### `v2_checker_formatters.py`
**Path:** tools\v2_checker_formatters.py  
**Error:** Traceback (most recent call last):
  File "D:\Agent_Cellphone_V2_Repository\tools\v2_checker_formatters.py", line 173, in <module>
    main()
    ^^^^
NameError: name 'main' is not defined. Did you me  

### `work_attribution_tool.py`
**Path:** tools\work_attribution_tool.py  
**Error:** Traceback (most recent call last):
  File "D:\Agent_Cellphone_V2_Repository\tools\work_attribution_tool.py", line 30, in <module>
    class WorkAttributionTool:
  File "D:\Agent_Cellphone_V2_Repositor  

### `hard_onboard_captain.py`
**Path:** tools\hard_onboard_captain.py  
**Error:** Timeout (>5s)  

### `find_file_size_violations.py`
**Path:** tools\find_file_size_violations.py  
**Error:** Timeout (>5s)  

### `swarm_orchestrator.py`
**Path:** tools\swarm_orchestrator.py  
**Error:** Traceback (most recent call last):
  File "D:\Agent_Cellphone_V2_Repository\tools\swarm_orchestrator.py", line 37, in <module>
    from .gas_messaging import send_gas_message
ImportError: attempted re  

### `captain_hard_onboard_agent.py`
**Path:** tools\captain_hard_onboard_agent.py  
**Error:** Unknown  

### `captain_import_validator.py`
**Path:** tools\captain_import_validator.py  
**Error:** Unknown  

### `captain_completion_processor.py`
**Path:** tools\captain_completion_processor.py  
**Error:** Unknown  

### `captain_architectural_checker.py`
**Path:** tools\captain_architectural_checker.py  
**Error:** Unknown  

### `workspace_auto_cleaner.py`
**Path:** tools\workspace_auto_cleaner.py  
**Error:** Traceback (most recent call last):
  File "D:\Agent_Cellphone_V2_Repository\tools\workspace_auto_cleaner.py", line 136, in <module>
    def generate_cleanup_report(agent_id: str) -> Dict[str, Any]:
    

### `discord_status_dashboard.py`
**Path:** tools\discord_status_dashboard.py  
**Error:** Timeout (>5s)  

### `post_devlog_to_discord.py`
**Path:** tools\post_devlog_to_discord.py  
**Error:** Unknown  

### `agent_checkin.py`
**Path:** tools\agent_checkin.py  
**Error:** Traceback (most recent call last):
  File "D:\Agent_Cellphone_V2_Repository\tools\agent_checkin.py", line 11, in <module>
    from core.unified_utilities import (
ModuleNotFoundError: No module named   

### `captain_snapshot.py`
**Path:** tools\captain_snapshot.py  
**Error:** Traceback (most recent call last):
  File "D:\Agent_Cellphone_V2_Repository\tools\captain_snapshot.py", line 15, in <module>
    from core.unified_utilities import get_logger, read_json
ModuleNotFound  

### `audit_project_components.py`
**Path:** tools\audit_project_components.py  
**Error:** Timeout (>5s)  

### `audit_imports.py`
**Path:** tools\audit_imports.py  
**Error:** Timeout (>5s)  

### `comprehensive_tool_runtime_audit.py`
**Path:** tools\comprehensive_tool_runtime_audit.py  
**Error:** Timeout (>5s)  

### `replace_prints_with_logger.py`
**Path:** tools\codemods\replace_prints_with_logger.py  
**Error:** Traceback (most recent call last):
  File "D:\Agent_Cellphone_V2_Repository\tools\codemods\replace_prints_with_logger.py", line 144, in <module>
    main()
  File "D:\Agent_Cellphone_V2_Repository\too  

### `migrate_managers.py`
**Path:** tools\codemods\migrate_managers.py  
**Error:** File "D:\Agent_Cellphone_V2_Repository\tools\codemods\migrate_managers.py", line 15
    from __future__ import annotations
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
SyntaxError: from __future__ imports m  

### `migrate_orchestrators.py`
**Path:** tools\codemods\migrate_orchestrators.py  
**Error:** File "D:\Agent_Cellphone_V2_Repository\tools\codemods\migrate_orchestrators.py", line 9
    from __future__ import annotations
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
SyntaxError: from __future__ impor  

### `demo_swarm_pulse.py`
**Path:** tools_v2\demo_swarm_pulse.py  
**Error:** Traceback (most recent call last):
  File "D:\Agent_Cellphone_V2_Repository\tools_v2\demo_swarm_pulse.py", line 14, in <module>
    from tools_v2 import get_toolbelt_core
ImportError: cannot import na  



---

## ✅ WORKING TOOLS (78 total)

- `add_remaining_swarm_knowledge.py`
- `agent_fuel_monitor.py`
- `agent_lifecycle_automator.py`
- `agent_message_history.py`
- `agent_mission_controller.py`
- `agent_orient.py`
- `agent_status_quick_check.py`
- `agent_task_finder.py`
- `agent_toolbelt.py`
- `analysis_cli.py`
- `arch_pattern_validator.py`
- `architecture_review.py`
- `audit_broken_tools.py`
- `auto_inbox_processor.py`
- `auto_status_updater.py`
- `auto_workspace_cleanup.py`
- `autonomous_leaderboard.py`
- `autonomous_task_engine.py`
- `cache_invalidator.py`
- `captain_check_agent_status.py`
- `captain_coordinate_validator.py`
- `captain_find_idle_agents.py`
- `captain_leaderboard_update.py`
- `captain_message_all_agents.py`
- `captain_morning_briefing.py`
- `captain_next_task_picker.py`
- `captain_roi_quick_calc.py`
- `captain_self_message.py`
- `captain_toolbelt_help.py`
- `captain_update_log.py`

... and 48 more

---

## 🎯 RECOMMENDATION

Move 46 broken tools to `tools_quarantine/` for systematic fixing.
