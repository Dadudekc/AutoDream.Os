# Messaging System Test Plan

Canonical testing approach for the unified messaging system.

## Objectives

- Validate message creation and validation logic.
- Ensure CLI arguments map to correct handlers.
- Confirm delivery modes (PyAutoGUI and inbox) operate reliably.
- Maintain ≥85% coverage for new messaging features.

## Unit Tests

- `tests/test_messaging_cli_parser.py` covers CLI option parsing.
- `tests/test_file_lock.py::test_messaging_integration` ensures safe file access.
- `tests/test_messaging_system_tdd.py` tracks ongoing fixes.
- `tests/test_ctrl_t_onboarding_navigation.py` verifies onboarding flows.

Run with:

```bash
npm test
```

## Integration Tests

- `tests/test_pyautogui_mode.py` exercises PyAutoGUI delivery.
- `tests/test_discord_coordinate_messaging.py` checks coordinate-based messaging.

Run targeted suites with:

```bash
python -m pytest tests/test_pyautogui_mode.py
python -m pytest tests/test_discord_coordinate_messaging.py
```

## Manual Checks

1. `python -m src.services.messaging_cli --check-status`
2. Send a test message to an agent inbox and verify file creation.
3. Use `--history` to confirm logging.

## Cross-References

- API details: [MESSAGING_API_SPECIFICATIONS.md](MESSAGING_API_SPECIFICATIONS.md)
- Deployment steps: [MESSAGING_DEPLOYMENT_STRATEGY.md](MESSAGING_DEPLOYMENT_STRATEGY.md)
- Channel rules: [CHANNEL_RESTRICTION_FEATURES.md](CHANNEL_RESTRICTION_FEATURES.md)

This document is the single source of truth for messaging system testing.
