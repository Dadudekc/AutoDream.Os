# AutoDream OS

AutoDream OS is a modular, V2 standards compliant platform for building agent-driven applications.
It enforces strict coding standards and provides convenient command line interfaces for development and testing.

## Features
- **V2 coding standards** with line-count limits and object-oriented design
- **Modular architecture** for core systems, services, launchers, utilities and web components
- **CLI interfaces** for every module to assist quick experimentation
- **Smoke tests and test suites** to validate components
- **Structured logging and error handling**
- **CI/CD templates** for Jenkins, GitLab CI and Docker

## Getting Started
### Installation
```bash
pip install -r requirements.txt
```

### Quick status check
```bash
python -m src --status
```

### Launch web module
```bash
python -m src.web --start
```

## Running Tests
```bash
pytest
```

## Repository Structure
```
src/      # application source
tests/    # test suites
docs/     # additional documentation
examples/ # examples and demos
```

## Contributing
- Follow the [V2 coding standards](V2_CODING_STANDARDS.md)
- Keep files within the specified line-count limits
- Provide CLI entrypoints and smoke tests for new modules

## Links
- [Examples](examples/)
- [Tests](tests/)
- [Configuration](config/)

---
This repository is the single source of truth for AutoDream OS. It maintains V2 standards to ensure high-quality, agent-friendly code.
