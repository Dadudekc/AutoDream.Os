# 🔍 DUPLICATION ANALYSIS REPORT
**Generated:** 2025-09-15T15:25:12.012324

## 📊 SCAN SUMMARY
- Total Python files: 1070
- Files processed: 1070
- Function groups found: 3899
- Class groups found: 958
- Potential duplicates: 131

## 🔍 DETAILED ANALYSIS
- **True Duplicates:** 126 (SAFE to consolidate)
- **Similar Functions:** 5 (REVIEW required)
- **False Duplicates:** 0 (DO NOT touch)

## 🎯 CONSOLIDATION PLAN
- **Safe Consolidations:** 126
- **Risky Consolidations:** 5
- **Manual Review Required:** 0

### ✅ SAFE CONSOLIDATIONS (LOW RISK)
1. **__init__**
   - Target: `src\core\coordination\contract_system.py`
   - Sources: 2 files
   - Risk: LOW

2. **to_dict**
   - Target: `src\core\coordination\contract_system.py`
   - Sources: 2 files
   - Risk: LOW

3. **__init__**
   - Target: `src\core\coordination\fsm_system.py`
   - Sources: 2 files
   - Risk: LOW

4. **transition_to**
   - Target: `src\core\coordination\fsm_system.py`
   - Sources: 2 files
   - Risk: LOW

5. **get_state_info**
   - Target: `src\core\coordination\fsm_system.py`
   - Sources: 2 files
   - Risk: LOW

6. **get_chat_coordinates**
   - Target: `src\core\coordination\onboarding_coordinator.py`
   - Sources: 2 files
   - Risk: LOW

7. **get_status**
   - Target: `archive\captain_handbooks_consolidated\archive\consolidated_files\analytics\processors\insight_processor.py`
   - Sources: 2 files
   - Risk: LOW

8. **__init__**
   - Target: `archive\captain_handbooks_consolidated\archive\consolidated_files\emergency_intervention\unified_emergency\orchestrator.py`
   - Sources: 2 files
   - Risk: LOW

9. **_register_default_protocols**
   - Target: `archive\captain_handbooks_consolidated\archive\consolidated_files\emergency_intervention\unified_emergency\orchestrator.py`
   - Sources: 2 files
   - Risk: LOW

10. **detect_emergency**
   - Target: `archive\captain_handbooks_consolidated\archive\consolidated_files\emergency_intervention\unified_emergency\orchestrator.py`
   - Sources: 2 files
   - Risk: LOW

### ⚠️ RISKY CONSOLIDATIONS (REVIEW REQUIRED)
1. **get_onboarding_coordinates**
   - Similarity: 98.1%
   - Files: 2
   - Risk: MEDIUM

2. **create_onboarding_contract**
   - Similarity: 98.4%
   - Files: 2
   - Risk: MEDIUM

3. **_notify_alert**
   - Similarity: 94.6%
   - Files: 2
   - Risk: MEDIUM

4. **__init__**
   - Similarity: 96.5%
   - Files: 3
   - Risk: MEDIUM

5. **__init__**
   - Similarity: 91.0%
   - Files: 4
   - Risk: MEDIUM

## 🎯 RECOMMENDATIONS
1. **Start with Safe Consolidations** - Low risk, immediate benefits
2. **Review Risky Consolidations Carefully** - Manual verification required
3. **Leave False Duplicates Alone** - Different purposes despite similar code
4. **Test After Each Consolidation** - Use verification tools
5. **Maintain Rollback Capability** - Keep consolidation-safety-net branch
