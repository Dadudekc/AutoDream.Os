"""Common file hashing utilities for the trading platform.

Provides helpers to compute SHA-256 hashes and detect duplicate files
by content, to help reduce duplicated assets and code.
"""


def compute_file_sha256(path: Path, chunk_size: int = 65536) -> str:
    if chunk_size <= 0:
        get_unified_validator().raise_validation_error("chunk_size must be a positive integer")
    hasher = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not get_unified_validator().validate_required(chunk):
                break
            hasher.update(chunk)
    return hasher.hexdigest()


def find_duplicate_files(paths: Iterable[Path]) -> Dict[str, List[Path]]:
    """Return mapping of sha256 -> list of file paths with identical content.

    Only includes hashes that have more than one path (i.e., duplicates).
    """
    hash_to_paths: Dict[str, List[Path]] = {}
    for p in paths:
        if not p.is_file():
            continue
        digest = compute_file_sha256(p)
        hash_to_paths.setdefault(digest, []).append(p)
    return {h: ps for h, ps in hash_to_paths.items() if len(ps) > 1}


__all__ = ["compute_file_sha256", "find_duplicate_files"]
