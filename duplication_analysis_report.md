# 🔍 DUPLICATION ANALYSIS REPORT
**Generated:** 2025-09-15T21:37:08.320330

## 📊 SCAN SUMMARY
- Total Python files: 929
- Files processed: 929
- Function groups found: 3584
- Class groups found: 866
- Potential duplicates: 276

## 🔍 DETAILED ANALYSIS
- **True Duplicates:** 274 (SAFE to consolidate)
- **Similar Functions:** 2 (REVIEW required)
- **False Duplicates:** 0 (DO NOT touch)

## 🎯 CONSOLIDATION PLAN
- **Safe Consolidations:** 274
- **Risky Consolidations:** 2
- **Manual Review Required:** 0

### ✅ SAFE CONSOLIDATIONS (LOW RISK)
1. **__init__**
   - Target: `src\core\coordination\contract_system.py`
   - Sources: 4 files
   - Risk: LOW

2. **to_dict**
   - Target: `src\core\coordination\contract_system.py`
   - Sources: 4 files
   - Risk: LOW

3. **__init__**
   - Target: `src\core\coordination\fsm_system.py`
   - Sources: 3 files
   - Risk: LOW

4. **transition_to**
   - Target: `src\core\coordination\fsm_system.py`
   - Sources: 3 files
   - Risk: LOW

5. **get_state_info**
   - Target: `src\core\coordination\fsm_system.py`
   - Sources: 3 files
   - Risk: LOW

6. **get_chat_coordinates**
   - Target: `src\core\coordination\onboarding_coordinator.py`
   - Sources: 2 files
   - Risk: LOW

7. **__init__**
   - Target: `tests\swarm_testing_framework_core.py`
   - Sources: 2 files
   - Risk: LOW

8. **setup_method**
   - Target: `tests\test_consolidated_messaging_service_core.py`
   - Sources: 2 files
   - Risk: LOW

9. **teardown_method**
   - Target: `tests\test_consolidated_messaging_service_core.py`
   - Sources: 2 files
   - Risk: LOW

10. **__init__**
   - Target: `tests\test_consolidated_messaging_service_core.py`
   - Sources: 2 files
   - Risk: LOW

### ⚠️ RISKY CONSOLIDATIONS (REVIEW REQUIRED)
1. **create_onboarding_contract**
   - Similarity: 98.4%
   - Files: 2
   - Risk: MEDIUM

2. **__init__**
   - Similarity: 91.0%
   - Files: 4
   - Risk: MEDIUM

## 🎯 RECOMMENDATIONS
1. **Start with Safe Consolidations** - Low risk, immediate benefits
2. **Review Risky Consolidations Carefully** - Manual verification required
3. **Leave False Duplicates Alone** - Different purposes despite similar code
4. **Test After Each Consolidation** - Use verification tools
5. **Maintain Rollback Capability** - Keep consolidation-safety-net branch