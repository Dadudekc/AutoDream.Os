# Consolidation Scan Report (Scoped: onboarding + discord)

- **Files scanned**: 146
- **Exact duplicate groups**: 0
- **Near-duplicate pairs**: 1
- **Total duplicates found**: 1

## Exact Duplicate Groups:


## Top Near-Duplicate Pairs (similarity ≥ 86%):

1. **97.8%** similarity:
   - `tools\discord_commander_launcher_core.py`
   - `discord_commander_launcher_core.py`


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
