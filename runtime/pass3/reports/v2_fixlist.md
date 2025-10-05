# V2 Fixlist (from Project Scanner + LOC Analysis)

**Current Status**: 9 files violate V2 compliance (>400 LOC)

## Files Requiring V2 Compliance Fixes

1. `thea_login_handler.py` — LOC:793 classes:? funcs:?
   - Action: split or refactor to ≤400 LOC / ≤5 classes / ≤10 funcs

2. `thea_login_handler_working.py` — LOC:788 classes:? funcs:?
   - Action: split or refactor to ≤400 LOC / ≤5 classes / ≤10 funcs

3. `simple_thea_communication.py` — LOC:722 classes:? funcs:?
   - Action: split or refactor to ≤400 LOC / ≤5 classes / ≤10 funcs

4. `simple_thea_communication_working.py` — LOC:717 classes:? funcs:?
   - Action: split or refactor to ≤400 LOC / ≤5 classes / ≤10 funcs

5. `src\infrastructure\unified_browser_service.py` — LOC:657 classes:? funcs:?
   - Action: split or refactor to ≤400 LOC / ≤5 classes / ≤10 funcs

6. `src\services\discord_devlog_service.py` — LOC:581 classes:? funcs:?
   - Action: split or refactor to ≤400 LOC / ≤5 classes / ≤10 funcs

7. `src\services\discord_commander\web_controller_templates.py` — LOC:540 classes:? funcs:?
   - Action: split or refactor to ≤400 LOC / ≤5 classes / ≤10 funcs

8. `tools\simple_workflow_automation.py` — LOC:532 classes:? funcs:?
   - Action: split or refactor to ≤400 LOC / ≤5 classes / ≤10 funcs

9. `src\services\discord_commander\bot.py` — LOC:521 classes:? funcs:?
   - Action: split or refactor to ≤400 LOC / ≤5 classes / ≤10 funcs

## Strategy

**Priority 1**: Files with duplicate patterns (thea_login_handler vs working versions)
**Priority 2**: Large service files that can be split by functionality
**Priority 3**: Template and automation files that can be modularized

## Target Metrics

- **Current**: 672 Python files, 9 V2 violations
- **Target**: ≤600 Python files, 0 V2 violations
- **Reduction needed**: ~72 files, 9 V2 fixes