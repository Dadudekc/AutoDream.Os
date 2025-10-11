from __future__ import annotations

import hashlib
from collections.abc import Iterable
from pathlib import Path


def compute_file_sha256(path: Path, chunk_size: int = 65536) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def find_duplicate_files(paths: Iterable[Path]) -> dict[str, list[Path]]:
    mapping: dict[str, list[Path]] = {}
    for p in paths:
        if not p.is_file():
            continue
        digest = compute_file_sha256(p)
        mapping.setdefault(digest, []).append(p)
    return {d: ps for d, ps in mapping.items() if len(ps) > 1}


__all__ = ["compute_file_sha256", "find_duplicate_files"]
