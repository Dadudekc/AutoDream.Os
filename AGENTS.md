# Project Instructions (AGENTS.md)

This repository is primarily a **Python** project. Unless explicitly noted, all new code should be written in Python and follow the guidelines below.

## Code Style
- Follow **PEP 8** and include type hints.
- Keep line length ≤100 characters.
- Use **snake_case** for database columns and API fields.
- Prefer class-based design for complex logic.
- **Monitoring component** (`src/core/health/monitoring/`) is exempt from the Python-only rule and may use alternative technologies if required.

## Architecture
- Apply the **repository pattern** for data access.
- Keep **business logic** inside service layers.
- Use dependency injection for shared utilities.
- Avoid circular dependencies across modules.
- Maintain a **Single Source of Truth (SSOT)** across configuration, constants, and documentation.

## Testing
- All new features require unit tests using **pytest**.
- Mock external APIs and database calls.
- Keep coverage above **85%**.
- Run `pre-commit run --files <file>` and `pytest` before committing.

## Documentation
- Document public functions and classes with docstrings.
- Provide usage examples for new utilities.
- Update `README.md` when adding new features.
- Record significant updates in `CHANGELOG.md`.

## Workflow
- Commit messages must follow the convention:
  `feat: short description` | `fix: short description` | `docs: short description`.
- Pull requests must pass code review and CI checks before merge.
- Split large features into smaller, incremental PRs.

## V2 Compliance
- Write **clean, tested, reusable, scalable** code.
- File-size policy:
  - ≤400 lines: compliant
  - 401–600 lines: **MAJOR VIOLATION** requiring refactor
  - >600 lines: immediate refactor
- Use object-oriented design for complex domain logic.
- Ensure comprehensive error handling and logging.
- Prioritize modular design and clear boundaries between modules.
