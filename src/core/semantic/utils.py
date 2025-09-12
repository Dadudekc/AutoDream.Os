from __future__ import annotations

from collections.abc import Iterable
from typing import Any


def flatten_json(obj: Any, prefix: str = "", keep: Iterable[str] | None = None) -> list[str]:
    """Turn nested JSON/dicts/lists into a list of 'key: value' strings."""
    keep_set = set(keep or [])
    out: list[str] = []

    def _walk(x: Any, path: list[str]):
        if isinstance(x, dict):
            for k, v in x.items():
                if keep_set and len(path) == 0 and k not in keep_set:
                    # at root, respect 'fields_keep'
                    continue
                _walk(v, path + [str(k)])
        elif isinstance(x, list):
            for i, v in enumerate(x):
                _walk(v, path + [str(i)])
        else:
            key = "/".join(path)
            val = str(x)
            out.append(f"{key}: {val}")

    _walk(obj, [prefix] if prefix else [])
    return out


def json_to_text(obj: Any, keep: Iterable[str] | None = None) -> str:
    return "\n".join(flatten_json(obj, keep=keep))
