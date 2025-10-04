# Consolidation Scan Report (Scoped: onboarding + discord)

- **Files scanned**: 138
- **Exact duplicate groups**: 3
- **Near-duplicate pairs**: 89
- **Total duplicates found**: 92

## Exact Duplicate Groups:

1. src\services\messaging_core.py, src\services\messaging\message_validator.py, src\services\messaging\messaging_core.py, src\services\messaging\providers\discord_provider_operations.py, src\services\messaging\providers\discord_provider_core.py
2. src\services\messaging\core\__init__.py, src\services\messaging\cli\__init__.py, src\services\messaging\delivery\__init__.py, src\services\messaging\providers\__init__.py, src\services\messaging\onboarding\__init__.py, src\services\messaging\status\__init__.py, src\services\discord_bot\commands\__init__.py, src\services\discord_bot\commands\agent_coordination\__init__.py, src\services\discord_bot\core\__init__.py, src\services\discord_bot\core\commands\__init__.py, src\services\discord_bot\ui\__init__.py, src\services\discord_bot\tools\__init__.py, src\services\devlog_storytelling\integration\__init__.py
3. src\services\messaging\onboarding\onboarding_service.py, tools\agent_onboard_cli.py

## Top Near-Duplicate Pairs (similarity ≥ 86%):

1. **100.0%** similarity:
   - `src\services\messaging_core.py`
   - `src\services\messaging\message_validator.py`

2. **100.0%** similarity:
   - `src\services\messaging_core.py`
   - `src\services\messaging\messaging_core.py`

3. **100.0%** similarity:
   - `src\services\messaging_core.py`
   - `src\services\messaging\providers\discord_provider_operations.py`

4. **100.0%** similarity:
   - `src\services\messaging_core.py`
   - `src\services\messaging\providers\discord_provider_core.py`

5. **100.0%** similarity:
   - `src\services\messaging\message_validator.py`
   - `src\services\messaging\messaging_core.py`

6. **100.0%** similarity:
   - `src\services\messaging\message_validator.py`
   - `src\services\messaging\providers\discord_provider_operations.py`

7. **100.0%** similarity:
   - `src\services\messaging\message_validator.py`
   - `src\services\messaging\providers\discord_provider_core.py`

8. **100.0%** similarity:
   - `src\services\messaging\messaging_core.py`
   - `src\services\messaging\providers\discord_provider_operations.py`

9. **100.0%** similarity:
   - `src\services\messaging\messaging_core.py`
   - `src\services\messaging\providers\discord_provider_core.py`

10. **100.0%** similarity:
   - `src\services\messaging\core\__init__.py`
   - `src\services\messaging\cli\__init__.py`

11. **100.0%** similarity:
   - `src\services\messaging\core\__init__.py`
   - `src\services\messaging\delivery\__init__.py`

12. **100.0%** similarity:
   - `src\services\messaging\core\__init__.py`
   - `src\services\messaging\providers\__init__.py`

13. **100.0%** similarity:
   - `src\services\messaging\core\__init__.py`
   - `src\services\messaging\onboarding\__init__.py`

14. **100.0%** similarity:
   - `src\services\messaging\core\__init__.py`
   - `src\services\messaging\status\__init__.py`

15. **100.0%** similarity:
   - `src\services\messaging\core\__init__.py`
   - `src\services\discord_bot\commands\__init__.py`

16. **100.0%** similarity:
   - `src\services\messaging\core\__init__.py`
   - `src\services\discord_bot\commands\agent_coordination\__init__.py`

17. **100.0%** similarity:
   - `src\services\messaging\core\__init__.py`
   - `src\services\discord_bot\core\__init__.py`

18. **100.0%** similarity:
   - `src\services\messaging\core\__init__.py`
   - `src\services\discord_bot\core\commands\__init__.py`

19. **100.0%** similarity:
   - `src\services\messaging\core\__init__.py`
   - `src\services\discord_bot\ui\__init__.py`

20. **100.0%** similarity:
   - `src\services\messaging\core\__init__.py`
   - `src\services\discord_bot\tools\__init__.py`

... and 69 more pairs

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
