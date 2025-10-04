# Consolidation Scan Report (Scoped: onboarding + discord)

- **Files scanned**: 122
- **Exact duplicate groups**: 1
- **Near-duplicate pairs**: 1
- **Total duplicates found**: 2

## Exact Duplicate Groups:

1. src\services\messaging_service_utils.py, src\services\consolidated_messaging_service_utils.py

## Top Near-Duplicate Pairs (similarity ≥ 86%):

1. **100.0%** similarity:
   - `src\services\messaging_service_utils.py`
   - `src\services\consolidated_messaging_service_utils.py`


## Consolidation Recommendations:

### High Priority (Exact Duplicates):
- Remove duplicate files, keep canonical versions
- Update imports to point to canonical modules

### Medium Priority (Near Duplicates):
- Review similar files for merge opportunities
- Consider creating shim modules for backward compatibility

### Canonical Modules Identified:
- **Onboarding**: `src/services/agent_hard_onboarding.py`
- **Discord**: `src/services/discord_commander/discord_post_client.py`
