"""Deployment utilities for CodeCrafter."""

from pathlib import Path


class CodeDeployer:
    """Write generated code to disk."""

    def deploy(self, code: str, destination: Path) -> Path:
        """Persist *code* to *destination* and return the resulting path."""

        destination = Path(destination)
        destination.write_text(code, encoding="utf-8")
        return destination

