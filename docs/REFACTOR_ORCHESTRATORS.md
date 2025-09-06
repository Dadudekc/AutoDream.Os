# Phase-1 Orchestrator Consolidation

**Goals:** SRP/OCP/DIP, DRY reduction, SSOT for config, V2 line limits.

## Steps
1. Introduce contracts/registry and 3 core orchestrators.
2. Add legacy adapter; populate `runtime/migrations/orchestrator-map.json`.
3. Run codemod (dry-run), review diff, then `--write`.
4. Run tests + unified proof + cleanup audit.
5. Deprecate legacy classes behind adapter; remove after grace period.

## Commands
```bash
# dry-run codemod
python tools/codemods/migrate_orchestrators.py
# apply
python tools/codemods/migrate_orchestrators.py --write
# tests + proof + audit
pytest -q || true
python tools/audit_cleanup.py || true
python -m src.services.messaging_cli --hard-onboarding --mode quality-suite --proof --audit-cleanup --yes
```
