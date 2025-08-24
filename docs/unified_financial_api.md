# Unified Financial API

The Unified Financial API now delegates persistence and background duties to
separate modules:

- `api_background_tasks.py` – manages heartbeat monitoring, performance updates
  and data cleanup.
- `api_persistence.py` – saves and loads agent registrations, requests and
  metrics.
- `unified_financial_api.py` – orchestration layer that coordinates services
  and exposes the public facade.

This modular structure keeps individual files under the V2 line limits and makes
key responsibilities easier to maintain and test.
