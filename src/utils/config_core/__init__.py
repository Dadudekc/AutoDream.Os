# AUTO-GENERATED __init__.py
# DO NOT EDIT MANUALLY - changes may be overwritten

from __future__ import annotations

from . import fsm_config

from pathlib import Path
from typing import Any

__all__ = [
    'fsm_config',
    'get_config',
]


def get_config(key: str | None = None, default: Any | None = None, path: str | None = None) -> Any:
    """Lightweight config accessor used by tests and core.

    Behaviors:
    - If key is None: returns merged config dict from known files.
    - If key is provided: returns env var ACV2_{KEY} (if set), else value from merged config,
      else the provided default.
    """
    try:
        # Load file-based config
        candidate_paths: list[Path] = []
        if path:
            candidate_paths.append(Path(path))
        candidate_paths.extend(
            [
                Path('config/production.yaml'),
                Path('config/messaging.yml'),
                Path('config/devlog_config.json'),
            ]
        )

        merged: dict[str, Any] = {}
        for p in candidate_paths:
            if not p.exists():
                continue
            text = p.read_text(encoding='utf-8')
            # Try YAML
            try:
                import yaml  # type: ignore
                loaded = yaml.safe_load(text)
                if isinstance(loaded, dict):
                    merged.update(loaded)
                continue
            except Exception:
                pass
            # Try JSON
            try:
                import json
                loaded = json.loads(text)
                if isinstance(loaded, dict):
                    merged.update(loaded)
            except Exception:
                pass

        if key is None:
            return merged

        # Env override (prefix ACV2_)
        import os
        env_key = f"ACV2_{key}"
        if env_key in os.environ:
            return os.environ[env_key]

        # Config file value
        return merged.get(key, default)
    except Exception:
        return default if key is not None else {}
