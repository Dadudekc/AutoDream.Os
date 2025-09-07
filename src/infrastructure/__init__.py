"""
Infrastructure Layer - Adapters
===============================

Contains concrete implementations (adapters) of the domain ports.
This layer implements the external dependencies defined by the domain.

Adapters included:
- Persistence: SQLite repositories for tasks and agents
- Messaging: Message bus implementations
- Time: System clock implementation
- Logging: Standard library logger implementation
"""

__version__ = "1.0.0"
