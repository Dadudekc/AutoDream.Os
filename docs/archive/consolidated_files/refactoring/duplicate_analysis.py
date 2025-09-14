import hashlib
from collections import defaultdict
from dataclasses import dataclass

from ...services.unified_messaging_imports import get_unified_utility


@dataclass
class DuplicateFile:
    """Represents duplicate file information."""

    original_file: str
    duplicate_files: list[str]
    similarity_score: float
    duplicate_type: str


def find_duplicate_files(directory: str, similarity_threshold: float = 0.8) -> list[DuplicateFile]:
    """Find duplicate files in a directory."""
    duplicates = []
    file_hashes = defaultdict(list)

    for file_path in get_unified_utility().Path(directory).rglob("*.py"):
        if file_path.is_file():
            try:
                with open(file_path, encoding="utf-8") as f:
                    content = f.read()
                normalized_content = _normalize_content(content)
                content_hash = hashlib.md5(normalized_content.encode()).hexdigest()
                file_hashes[content_hash].append(str(file_path))
            except Exception:
                continue

    for content_hash, files in file_hashes.items():
        if len(files) > 1:
            duplicates.append(
                DuplicateFile(
                    original_file=files[0],
                    duplicate_files=files[1:],
                    similarity_score=1.0,
                    duplicate_type="exact",
                )
            )
    return duplicates


def _normalize_content(content: str) -> str:
    """Normalize content for duplicate detection."""
    lines = content.split("\n")
    normalized_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and not stripped.startswith('"""'):
            normalized_lines.append(stripped)
    return "\n".join(normalized_lines)
