"""
Domain Layer - Pure Business Logic (DDD)
=========================================

This layer contains pure domain logic with zero dependencies on:
- External frameworks (Django, Flask, etc.)
- Infrastructure (databases, HTTP clients, etc.)
- Application frameworks (FastAPI, etc.)

Contains:
- Entities: Core business objects with identity
- Value Objects: Immutable objects without identity
- Domain Services: Business logic that doesn't belong to entities
- Domain Events: Events that occur within the domain
- Ports: Abstract interfaces (Protocols) for external dependencies
"""

__version__ = "1.0.0"
