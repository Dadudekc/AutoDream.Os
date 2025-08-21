# AutoDream.Os – Quickstart

## TL;DR
```bash
python -m src --status
python -m src --demo
python -m src --test
python -m src --validate
```

CI
- Every PR must be green in GitHub Actions (ci workflow).
- --test maps to repo tests; add new tests under tests/.

Local Dev
- make status|demo|test|validate|fmt
- Add your demos to scripts/ or top-level demo_* scripts and --demo will auto-run them.
