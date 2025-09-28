## Summary

Describe the change and its purpose.

## Checklist (Merge Gates)

- [ ] Invariants documented in PR description
- [ ] Database migrations linked (if any)
- [ ] Tests linked/added and passing
- [ ] Canonical coordinates SSOT used (`config/canonical_coordinates.json`)
- [ ] MODE_SWITCH_GUARD invariants covered by tests

## CI

This PR should pass:

```bash
pytest -k "mode or roles or coordinates or onboarding" -q
```

