# Consolidation Scan Report (Scoped: onboarding + discord)

- **Files scanned**: 126
- **Exact duplicate groups**: 0
- **Near-duplicate pairs**: 1
- **Total duplicates found**: 1

## Exact Duplicate Groups:


## Top Near-Duplicate Pairs (similarity ≥ 86%):

1. **96.8%** similarity:
   - `src\services\messaging\providers\discord_provider_core.py`
   - `src\services\messaging\providers\discord_provider_operations.py`


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
