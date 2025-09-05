# Messaging System Deployment Strategy

Authoritative guide for installing and operating the messaging system.

## Prerequisites

- Python 3.11+
- Node 18+ for linting and tests
- `pip install -r requirements.txt`
- GUI access for PyAutoGUI mode or writable `agent_workspaces/<Agent-X>/inbox` directories for inbox mode

## Local Setup

1. Clone the repository and install dependencies.
2. Run `npm run lint:v2` and project tests to verify environment.
3. Populate `agent_workspaces/<Agent-X>/inbox` for each agent if using inbox delivery.
4. Confirm coordinates with `python -m src.services.messaging_cli --coordinates` when using PyAutoGUI.

## Deployment Steps

1. Ensure environment variables and screen settings match team conventions.
2. Start messaging interactions using `python -m src.services.messaging_cli`.
3. Use `--check-status` to verify system readiness before sending messages.
4. Monitor logs in `logs/` for delivery issues or errors.

## Rollout Considerations

- Prefer incremental feature rollout; validate each change in staging.
- Maintain backups of `agent_workspaces` before upgrades.
- Keep messaging modules synchronized with the `main` branch to preserve SSOT.

## Monitoring and Maintenance

- Use `--history` to review recent messages.
- Schedule periodic runs of `npm run v2:audit` to enforce lint rules and file size checks.
- Update documentation after any deployment change.

## Cross-References

- API usage details: [MESSAGING_API_SPECIFICATIONS.md](MESSAGING_API_SPECIFICATIONS.md)
- Testing approach: [MESSAGING_TEST_PLAN.md](MESSAGING_TEST_PLAN.md)
- Channel rules: [CHANNEL_RESTRICTION_FEATURES.md](CHANNEL_RESTRICTION_FEATURES.md)
- Enhanced types: [MESSAGING_SYSTEM_V2_ENHANCED_TYPES.md](MESSAGING_SYSTEM_V2_ENHANCED_TYPES.md)

This document is the single source of truth for messaging deployment.
