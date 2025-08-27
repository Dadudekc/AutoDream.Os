# Session Manager Migration

## Legacy Implementations

- `src/security/session_manager.py`
  - SQLite-backed persistence
  - Supports validation, invalidation, and cleanup of sessions
  - Maintains in-memory cache for active sessions

- `src/services_v2/auth/session_manager.py`
  - Store-backed design using pluggable backends via `SessionStore`
  - Focused on session creation with metadata for V2 features

## Unified Session Manager

The new module `src/session_management` provides a single
`SessionManager` class with pluggable backends (`MemorySessionBackend`
and `SQLiteSessionBackend`). It combines validation, invalidation and
expiration handling while remaining extensible through the backend
interface.

## Migration Guide

- Replace imports of `src.security.session_manager` and
  `src.services_v2.auth.session_manager` with
  `src.session_management.session_manager`.
- Use backends from `src.session_management.backends` directly instead of
  the deprecated `session_store` and `session_backend` wrappers.
- The legacy modules remain as shims and will be removed in a future
  version.
