
# MIGRATED: This file has been migrated to the centralized configuration system
import json
from pathlib import Path
from typing import Any, Dict, Union

try:
    import yaml
except Exception:  # pragma: no cover - optional dependency
    yaml = None


class ConfigLoader:
    """Utility for loading JSON/YAML configuration files with defaults."""

    @staticmethod
    def load(path: Union[str, Path], defaults: Dict[str, Any]) -> Dict[str, Any]:
        """Load configuration from *path*.

        If the file does not exist it will be created with *defaults*.
        Returns the loaded configuration or *defaults* on failure.
        """
        cfg_path = Path(path)
        try:
            if cfg_path.exists():
                with open(cfg_path, "r", encoding="utf-8") as f:
                    suffix = cfg_path.suffix.lower()
                    if suffix in {".yaml", ".yml"}:
                        if yaml is None:
                            return defaults.copy()
                        return yaml.safe_load(f) or {}
                    return json.load(f)

            cfg_path.parent.mkdir(parents=True, exist_ok=True)
            with open(cfg_path, "w", encoding="utf-8") as f:
                suffix = cfg_path.suffix.lower()
                if suffix in {".yaml", ".yml"} and yaml is not None:
                    yaml.safe_dump(defaults, f)
                else:
                    json.dump(defaults, f, indent=2)
            return defaults.copy()
        except Exception:
            return defaults.copy()
