# Architecture Pattern: Dependency Injection

**Category:** structural  
**Description:** Provide dependencies to objects rather than having them create dependencies  

## Problem

Tight coupling between classes makes code hard to test and maintain

## Solution

Inject dependencies through constructor or setter methods

## Benefits

- Reduces coupling between classes
- Makes code easier to test
- Improves flexibility and reusability
- Enables better separation of concerns

## Drawbacks

- Increases complexity of object creation
- Requires dependency injection container for complex scenarios
- May make code harder to understand for beginners

## Examples

- Constructor injection: def __init__(self, dependency): ...
- Setter injection: def set_dependency(self, dependency): ...

## Implementation Guidelines

- Use constructor injection for required dependencies
- Use setter injection for optional dependencies
- Prefer interfaces over concrete implementations
- Keep dependency injection simple and explicit
