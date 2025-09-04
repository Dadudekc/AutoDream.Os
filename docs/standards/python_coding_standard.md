# Dream.OS Python Coding Standard (v1.0)

## 0) Scope & Goals
- **Closure-first**: small, composable modules. **≤ 400 LOC per file**, **≤ 100 LOC per class**, **≤ 50 LOC per function** (hard guide; refactor if violated).
- **Typed by default**: no untyped public APIs.
- **Deterministic builds**, enforce via `pre-commit`.

## 1) Style & Formatting
- **Black** (line length 100), **isort** (profile=black), **UTF-8**, Unix EOL.
- One import per line; stdlib → third-party → local, separated by blank lines.

## 2) Naming
- Modules/packages: `snake_case`. Classes: `CapWords`. Functions/vars: `snake_case`.
- Constants: `UPPER_SNAKE`. Private internals: `_leading_underscore`.

## 3) Types
- All public functions/classes have annotations. Use `typing`/`collections.abc`.
- Favor `TypedDict`, `Protocol`, `dataclass(frozen=True)` for schemas.
- `Any` only behind an adapter boundary with TODO to tighten.

## 4) Docstrings (Google style)
- Module, class, and public functions require docstrings.
- Include Args/Returns/Raises/Examples. One-line summary ≤ 80 chars.

## 5) Errors & Logging
- Raise precise exceptions; no blanket `except Exception`.
- Log with `logging` (module-level logger). No prints in lib code.
- Each log line should be action-oriented and include correlation ids when relevant.

## 6) Concurrency
- Prefer `asyncio` with explicit timeouts.
- Never block the event loop; offload CPU-bound to threads/processes.

## 7) I/O & Config
- No hardcoded paths/secrets. Use env + `.env` loader or typed config objects.
- Pure functions for logic; side-effects isolated at edges.

## 8) Testing
- **pytest**; **≥ 80% coverage** module-level; critical paths ≥ 90%.
- Unit tests are deterministic; integration tests use fakes or containers.
- Test names: `test_<unitOfWork>__<scenario>__<expected>()`.

## 9) Security
- Bandit clean (no B* HIGH). Secrets scanning enabled.
- Validate untrusted input; serialize with safe libraries.

## 10) Performance
- Avoid quadratic loops on hot paths; prefer generators.
- Profile before micro-opt. Document complexity on N^2 sections.

## 11) Layout
```
repo/
src/<pkg>/
**init**.py <module>.py
tests/
unit/
integration/
docs/
pyproject.toml
.pre-commit-config.yaml
```

## 12) Reviews & CI Gates
- CI must pass: black, isort, flake8, mypy, bandit, pytest, coverage threshold.
- PR must include: summary, risks, test evidence.
