#!/usr/bin/env python3
"""
Content Hash-Based Deduplication System
======================================
Anti-Slop Protocol: Prevent duplicate file generation
V2 Compliant: ≤400 lines, focused deduplication logic
"""

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


@dataclass
class ContentHash:
    """Content hash data structure"""

    hash_value: str
    file_path: str
    content_size: int
    created_at: str
    accessed_count: int = 0
    last_accessed: str = ""

    def __post_init__(self):
        if not self.last_accessed:
            self.last_accessed = self.created_at


@dataclass
class DuplicateGroup:
    """Duplicate content group"""

    hash_value: str
    files: list[str]
    primary_file: str
    duplicate_count: int
    total_size: int


class ContentDeduplicationSystem:
    """Content hash-based deduplication system to prevent duplicate file generation"""

    def __init__(self, registry_file: str = "content_registry.json"):
        self.registry_file = Path(registry_file)
        self.content_registry: dict[str, ContentHash] = {}
        self.duplicate_groups: dict[str, DuplicateGroup] = {}

        # Anti-slop settings
        self.similarity_threshold = 0.95  # 95% similarity considered duplicate
        self.min_content_size = 100  # Minimum 100 characters to hash
        self.max_duplicate_ratio = 0.8  # Maximum 80% duplicate content allowed

        self.load_registry()

    def load_registry(self) -> None:
        """Load content registry from disk"""
        if self.registry_file.exists():
            try:
                with open(self.registry_file) as f:
                    data = json.load(f)

                # Load content registry
                for hash_value, hash_data in data.get("registry", {}).items():
                    self.content_registry[hash_value] = ContentHash(**hash_data)

                # Load duplicate groups
                for hash_value, group_data in data.get("duplicates", {}).items():
                    self.duplicate_groups[hash_value] = DuplicateGroup(**group_data)

            except Exception as e:
                print(f"Warning: Failed to load content registry: {e}")

    def save_registry(self) -> None:
        """Save content registry to disk"""
        try:
            data = {
                "registry": {k: asdict(v) for k, v in self.content_registry.items()},
                "duplicates": {k: asdict(v) for k, v in self.duplicate_groups.items()},
                "last_updated": datetime.now().isoformat(),
            }

            with open(self.registry_file, "w") as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"Error saving content registry: {e}")

    def calculate_content_hash(self, content: str) -> str:
        """Calculate SHA-256 hash of content"""
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def normalize_content(self, content: str) -> str:
        """Normalize content for comparison"""
        # Remove whitespace differences, normalize line endings
        normalized = content.strip()
        normalized = "\n".join(line.strip() for line in normalized.split("\n"))
        return normalized

    def calculate_similarity(self, content1: str, content2: str) -> float:
        """Calculate similarity ratio between two content strings"""
        if not content1 or not content2:
            return 0.0

        # Normalize content
        norm1 = self.normalize_content(content1)
        norm2 = self.normalize_content(content2)

        if norm1 == norm2:
            return 1.0

        # Calculate Jaccard similarity using character n-grams
        def get_ngrams(text: str, n: int = 3) -> set[str]:
            return set(text[i : i + n] for i in range(len(text) - n + 1))

        ngrams1 = get_ngrams(norm1)
        ngrams2 = get_ngrams(norm2)

        if not ngrams1 and not ngrams2:
            return 1.0
        if not ngrams1 or not ngrams2:
            return 0.0

        intersection = len(ngrams1.intersection(ngrams2))
        union = len(ngrams1.union(ngrams2))

        return intersection / union if union > 0 else 0.0

    def check_duplicate(
        self, content: str, file_path: str = ""
    ) -> tuple[bool, str | None, float]:
        """Check if content is duplicate or similar to existing content"""
        if len(content) < self.min_content_size:
            return False, None, 0.0

        content_hash = self.calculate_content_hash(content)

        # Check exact hash match
        if content_hash in self.content_registry:
            existing = self.content_registry[content_hash]
            existing.access_count += 1
            existing.last_accessed = datetime.now().isoformat()

            return True, existing.file_path, 1.0

        # Check similarity with existing content
        best_match = None
        best_similarity = 0.0

        for hash_value, content_hash_obj in self.content_registry.items():
            try:
                with open(content_hash_obj.file_path, encoding="utf-8") as f:
                    existing_content = f.read()

                similarity = self.calculate_similarity(content, existing_content)

                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match = content_hash_obj.file_path

            except Exception as e:
                print(f"Error reading file {content_hash_obj.file_path}: {e}")
                continue

        # Check if similarity exceeds threshold
        if best_similarity >= self.similarity_threshold:
            return True, best_match, best_similarity

        return False, None, best_similarity

    def register_content(self, content: str, file_path: str) -> bool:
        """Register new content in the deduplication system"""
        if len(content) < self.min_content_size:
            return True  # Skip small content

        content_hash = self.calculate_content_hash(content)
        now = datetime.now().isoformat()

        # Create content hash entry
        content_hash_obj = ContentHash(
            hash_value=content_hash,
            file_path=file_path,
            content_size=len(content),
            created_at=now,
            last_accessed=now,
        )

        self.content_registry[content_hash] = content_hash_obj

        # Update duplicate groups if this is a duplicate
        if content_hash in self.duplicate_groups:
            group = self.duplicate_groups[content_hash]
            group.files.append(file_path)
            group.duplicate_count += 1
            group.total_size += len(content)
        else:
            # Check if this content already exists elsewhere
            for existing_hash, existing_obj in self.content_registry.items():
                if existing_hash != content_hash and existing_obj.file_path != file_path:
                    try:
                        with open(existing_obj.file_path, encoding="utf-8") as f:
                            existing_content = f.read()

                        if (
                            self.calculate_similarity(content, existing_content)
                            >= self.similarity_threshold
                        ):
                            # Found duplicate, create group
                            self.duplicate_groups[existing_hash] = DuplicateGroup(
                                hash_value=existing_hash,
                                files=[existing_obj.file_path, file_path],
                                primary_file=existing_obj.file_path,
                                duplicate_count=2,
                                total_size=existing_obj.content_size + len(content),
                            )
                            break
                    except Exception as e:
                        print(f"Error reading file {existing_obj.file_path}: {e}")
                        continue

        self.save_registry()
        return True

    def get_duplicate_report(self) -> dict[str, Any]:
        """Generate duplicate content report"""
        report = {
            "total_files": len(self.content_registry),
            "duplicate_groups": len(self.duplicate_groups),
            "total_duplicates": 0,
            "wasted_space": 0,
            "groups": [],
        }

        for hash_value, group in self.duplicate_groups.items():
            duplicate_count = group.duplicate_count - 1  # Exclude primary file
            wasted_space = group.total_size - group.total_size // group.duplicate_count

            report["total_duplicates"] += duplicate_count
            report["wasted_space"] += wasted_space

            report["groups"].append(
                {
                    "hash": hash_value,
                    "primary_file": group.primary_file,
                    "duplicate_count": duplicate_count,
                    "wasted_space": wasted_space,
                    "files": group.files,
                }
            )

        return report

    def cleanup_duplicates(self, dry_run: bool = True) -> dict[str, Any]:
        """Clean up duplicate files, keeping primary files"""
        cleanup_report = {
            "files_removed": 0,
            "space_saved": 0,
            "removed_files": [],
            "dry_run": dry_run,
        }

        for hash_value, group in self.duplicate_groups.items():
            primary_file = group.primary_file
            duplicate_files = [f for f in group.files if f != primary_file]

            for duplicate_file in duplicate_files:
                try:
                    file_path = Path(duplicate_file)
                    if file_path.exists():
                        file_size = file_path.stat().st_size

                        if not dry_run:
                            file_path.unlink()  # Delete file

                        cleanup_report["files_removed"] += 1
                        cleanup_report["space_saved"] += file_size
                        cleanup_report["removed_files"].append(duplicate_file)

                        # Remove from registry
                        if hash_value in self.content_registry:
                            del self.content_registry[hash_value]

                except Exception as e:
                    print(f"Error removing duplicate file {duplicate_file}: {e}")

        if not dry_run:
            # Clean up duplicate groups
            self.duplicate_groups.clear()
            self.save_registry()

        return cleanup_report

    def check_anti_slop_compliance(self, new_content: str, agent_id: str) -> tuple[bool, str]:
        """Check if new content violates anti-slop protocol"""
        is_duplicate, existing_file, similarity = self.check_duplicate(new_content)

        if is_duplicate:
            if similarity >= 0.99:  # Nearly identical
                return False, f"Content is 99%+ identical to {existing_file}"
            elif similarity >= self.similarity_threshold:
                return False, f"Content is {similarity:.1%} similar to {existing_file}"

        # Check for excessive content generation by agent
        agent_files = [
            h.file_path
            for h in self.content_registry.values()
            if agent_id in h.file_path
            and h.created_at > (datetime.now() - timedelta(hours=24)).isoformat()
        ]

        if len(agent_files) > 10:  # More than 10 files in 24 hours
            return False, f"Agent {agent_id} has created {len(agent_files)} files in 24 hours"

        return True, "Content is compliant"

    def get_statistics(self) -> dict[str, Any]:
        """Get deduplication system statistics"""
        total_size = sum(h.content_size for h in self.content_registry.values())
        unique_size = sum(
            h.content_size
            for h in self.content_registry.values()
            if h.hash_value not in self.duplicate_groups
        )

        return {
            "total_files": len(self.content_registry),
            "duplicate_groups": len(self.duplicate_groups),
            "total_size": total_size,
            "unique_size": unique_size,
            "duplicate_size": total_size - unique_size,
            "deduplication_ratio": (total_size - unique_size) / total_size if total_size > 0 else 0,
            "last_updated": datetime.now().isoformat(),
        }


def main():
    """Main function for testing"""
    dedup = ContentDeduplicationSystem()

    # Test content
    test_content = "This is a test content for deduplication system."
    test_content2 = "This is a test content for deduplication system."  # Exact duplicate

    # Test duplicate detection
    is_dup, existing, similarity = dedup.check_duplicate(test_content)
    print(f"First check - Duplicate: {is_dup}, Similarity: {similarity}")

    # Register content
    dedup.register_content(test_content, "test_file1.txt")

    # Test duplicate detection again
    is_dup, existing, similarity = dedup.check_duplicate(test_content2)
    print(f"Second check - Duplicate: {is_dup}, Existing: {existing}, Similarity: {similarity}")

    # Get statistics
    stats = dedup.get_statistics()
    print(f"Statistics: {stats}")

    # Get duplicate report
    report = dedup.get_duplicate_report()
    print(f"Duplicate report: {report}")


if __name__ == "__main__":
    main()
