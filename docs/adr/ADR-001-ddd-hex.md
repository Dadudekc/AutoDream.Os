# ADR-001: Adopt Domain-Driven Design with Hexagonal Architecture

## Status
Accepted

## Context
The AutoDream OS project requires a scalable, maintainable architecture that can support:
- Complex agent coordination workflows
- Multiple external integrations (CLI, HTTP, messaging)
- Evolutionary changes to business requirements
- Testability and separation of concerns
- Long-term maintainability across multiple developers

The existing architecture had grown organically with tight coupling between business logic and infrastructure concerns, making changes difficult and testing challenging.

## Decision
We will adopt **Domain-Driven Design (DDD)** combined with **Hexagonal Architecture (Ports & Adapters)** to structure the codebase. This architectural pattern provides:

### Domain-Driven Design (DDD)
- **Domain Layer**: Pure business logic with zero framework dependencies
- **Entities**: Core business objects with identity and behavior
- **Value Objects**: Immutable objects representing domain concepts
- **Domain Services**: Business logic not belonging to individual entities
- **Domain Events**: Business events that occur within the domain

### Hexagonal Architecture (Ports & Adapters)
- **Ports**: Abstract interfaces (Python Protocols) defining external dependencies
- **Adapters**: Concrete implementations of ports for external systems
- **Dependency Inversion**: Domain depends on abstractions, not concretions
- **Technology Agnostic**: Domain layer is independent of frameworks

### Layer Structure
```
src/
├── domain/                    # Pure domain logic
│   ├── entities/             # Business objects with identity
│   ├── value_objects/        # Immutable domain concepts
│   ├── services/            # Domain services
│   ├── ports/               # Abstract interfaces (Protocols)
│   └── domain_events.py     # Business events
├── application/              # Use cases & orchestration
│   ├── use_cases/           # Application-specific operations
│   └── dto/                 # Data Transfer Objects
├── infrastructure/           # Adapters for external systems
│   ├── persistence/         # Database adapters
│   ├── messaging/           # Message bus adapters
│   ├── time/               # Clock adapters
│   └── logging/            # Logger adapters
├── interfaces/              # Driving adapters (HTTP/CLI)
│   ├── http/               # Web controllers
│   ├── cli/                # Command-line interfaces
│   └── events/             # Event consumers
└── shared/                  # Cross-cutting utilities
```

## Consequences

### Positive
- **Testability**: Domain logic can be tested without external dependencies
- **Maintainability**: Clear separation of concerns and single responsibility
- **Flexibility**: Easy to swap implementations (SQLite → PostgreSQL, etc.)
- **Evolutionary**: Safe to evolve business requirements independently
- **Technology Independence**: Domain logic is framework-agnostic
- **Parallel Development**: Teams can work on different layers simultaneously

### Negative
- **Initial Complexity**: Higher initial setup and learning curve
- **Boilerplate**: More interfaces and adapter classes required
- **Refactoring Cost**: Migration from existing coupled code requires effort

### Mitigations
- **Incremental Adoption**: Start with core domain concepts, expand gradually
- **Template Creation**: Develop reusable templates for ports and adapters
- **Training**: Team education on DDD and hexagonal concepts
- **Import Linting**: Automated enforcement of architectural boundaries

## Implementation Strategy

### Phase 1: Core Domain (Week 1-2)
- Define core entities (Task, Agent)
- Create value objects (IDs, domain concepts)
- Establish domain services (AssignmentService)
- Define domain events

### Phase 2: Ports & Interfaces (Week 2-3)
- Define repository ports (TaskRepository, AgentRepository)
- Define infrastructure ports (MessageBus, Clock, Logger)
- Create domain service interfaces
- Establish protocol contracts

### Phase 3: Application Layer (Week 3-4)
- Implement use cases (AssignTask, CompleteTask)
- Create DTOs for external communication
- Establish application service orchestration
- Define application boundaries

### Phase 4: Infrastructure Adapters (Week 4-5)
- Implement SQLite repositories
- Create system clock adapter
- Implement standard logger adapter
- Develop message bus adapter (Redis/in-memory)

### Phase 5: Interface Adapters (Week 5-6)
- Create HTTP REST controllers
- Implement CLI command handlers
- Develop event consumers
- Establish API contracts

### Phase 6: Testing & Validation (Week 6-7)
- Unit tests for domain layer (100% coverage target)
- Integration tests for adapters
- End-to-end tests for use cases
- Import linting and architectural validation

## Architectural Principles

### Dependency Direction
```
Interfaces → Application → Domain ← Infrastructure
    ↓           ↓           ↑           ↑
   HTTP/CLI   Use Cases   Entities   Adapters
```

### Import Rules
- Domain layer: No imports from application/infrastructure/interfaces
- Application layer: Can import from domain only
- Infrastructure layer: Can import from domain only
- Interfaces layer: Can import from application and domain

### Testing Strategy
- **Unit Tests**: Domain layer (entities, services, ports)
- **Integration Tests**: Infrastructure adapters
- **End-to-End Tests**: Complete use case flows
- **Contract Tests**: Port implementations

## Success Metrics
- [ ] Domain layer has zero external framework imports
- [ ] All ports are defined as Python protocols
- [ ] Import linter passes with zero violations
- [ ] Domain layer unit test coverage ≥ 95%
- [ ] Application layer integration test coverage ≥ 85%
- [ ] Existing FSM flows remain functional
- [ ] New adapters can be swapped without domain changes

## Related Documents
- [Hexagonal Architecture Overview](../diagrams/hex-overview.md)
- [Domain Model Documentation](../domain/README.md)
- [Import Linter Configuration](../../../importlinter.ini)

## Notes
This ADR establishes the foundational architecture for the AutoDream OS project. Future ADRs may refine specific aspects of the domain model or introduce new architectural patterns as the system evolves.
