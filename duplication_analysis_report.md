# 🔍 DUPLICATION ANALYSIS REPORT
**Generated:** 2025-09-14T00:48:00.825576

## 📊 SCAN SUMMARY
- Total Python files: 1049
- Files processed: 1049
- Function groups found: 5635
- Class groups found: 1456
- Potential duplicates: 138

## 🔍 DETAILED ANALYSIS
- **True Duplicates:** 136 (SAFE to consolidate)
- **Similar Functions:** 2 (REVIEW required)
- **False Duplicates:** 0 (DO NOT touch)

## 🎯 CONSOLIDATION PLAN
- **Safe Consolidations:** 136
- **Risky Consolidations:** 2
- **Manual Review Required:** 0

### ✅ SAFE CONSOLIDATIONS (LOW RISK)
1. **__init__**
   - Target: `src\core\contracts\agent_contract.py`
   - Sources: 2 files
   - Risk: LOW

2. **get_onboarding_coordinates**
   - Target: `src\services\onboarding\onboarding_service.py`
   - Sources: 2 files
   - Risk: LOW

3. **create_onboarding_contract**
   - Target: `src\services\onboarding\onboarding_service.py`
   - Sources: 2 files
   - Risk: LOW

4. **send_enhanced_cycle_message**
   - Target: `src\core\coordination\coordination_system.py`
   - Sources: 2 files
   - Risk: LOW

5. **run_enhanced_cycle**
   - Target: `src\core\coordination\coordination_system.py`
   - Sources: 2 files
   - Risk: LOW

6. **validate_system_performance**
   - Target: `archive\captain_handbooks_consolidated\archive\agent_scripts\agent5_core_consolidation_validator.py`
   - Sources: 2 files
   - Risk: LOW

7. **get_status**
   - Target: `archive\captain_handbooks_consolidated\archive\consolidated_files\coordination_unified.py`
   - Sources: 2 files
   - Risk: LOW

8. **info**
   - Target: `archive\captain_handbooks_consolidated\archive\consolidated_files\coordinator_interfaces.py`
   - Sources: 2 files
   - Risk: LOW

9. **warning**
   - Target: `archive\captain_handbooks_consolidated\archive\consolidated_files\coordinator_interfaces.py`
   - Sources: 2 files
   - Risk: LOW

10. **error**
   - Target: `archive\captain_handbooks_consolidated\archive\consolidated_files\coordinator_interfaces.py`
   - Sources: 2 files
   - Risk: LOW

### ⚠️ RISKY CONSOLIDATIONS (REVIEW REQUIRED)
1. **_notify_alert**
   - Similarity: 94.6%
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