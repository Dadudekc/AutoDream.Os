# Quick Cleanup Commands

## 1) Run the audit (safe: will abort if Python files look dangerously low)
```bash
python tools/audit_cleanup.py
```

## 2) If you expect large deletions and want to see report anyway:
```bash
python tools/audit_cleanup.py --force
```

## 3) Show last commit and name-status (sanity check)
```bash
git log -1 --name-status
```

## 4) Show working tree delta vs HEAD
```bash
git status --porcelain
git diff --stat
```

## 5) (If needed) Roll back accidental mass deletions in working tree
```bash
git restore --staged -A 2>/dev/null || true
git checkout -- .
```

## 6) (If already committed) Revert the cleanup commit
# Replace <sha> with the cleanup commit hash shown by `git log -1`
```bash
git revert <sha>
```

## 7) Check current file counts
```bash
# Total files
Get-ChildItem -Recurse -File | Measure-Object | Select-Object -ExpandProperty Count

# Python files
Get-ChildItem -Recurse -File -Name "*.py" | Measure-Object | Select-Object -ExpandProperty Count
```

## Auditor Integration

- Install local guard:  
  ```bash
  make hooks
  ```

* Run audit (safe):
  ```bash
  make audit
  ```
* Force report even if risky (does **not** change guard thresholds):
  ```bash
  make audit-force
  ```
* CI runs automatically on PRs/commits (`.github/workflows/cleanup-audit.yml`).

### Onboarding Gate

Append `--audit-cleanup` to your onboarding command to fail early if a risky deletion slipped in:

```bash
python -m src.services.messaging_cli --hard-onboarding --mode quality-suite --proof --audit-cleanup --yes
```
