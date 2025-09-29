"""
Enhanced Project Scanner Caching System
======================================

Caching system with file movement detection and hash-based tracking.
"""

import hashlib
import json
import logging
import threading
import time
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class EnhancedCachingSystem:
    """Enhanced caching system with file movement detection and hash-based tracking."""

    def __init__(self, cache_file: str = "dependency_cache.json"):
        """Initialize caching system."""
        self.cache_file = Path(cache_file)
        self.cache = self.load_cache()
        self.cache_lock = threading.Lock()

    def load_cache(self) -> dict[str, Any]:
        """Load cache from disk."""
        if self.cache_file.exists():
            try:
                with self.cache_file.open("r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, Exception) as e:
                logger.warning(f"Failed to load cache: {e}")
        return {}

    def save_cache(self):
        """Save cache to disk."""
        try:
            with self.cache_lock:
                with self.cache_file.open("w", encoding="utf-8") as f:
                    json.dump(self.cache, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to save cache: {e}")

    def get_file_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of file content."""
        try:
            with file_path.open("rb") as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return ""

    def is_file_cached(self, file_path: Path, relative_path: str) -> bool:
        """Check if file is cached and unchanged."""
        current_hash = self.get_file_hash(file_path)
        cached_hash = self.cache.get(relative_path, {}).get("hash")
        return cached_hash == current_hash

    def update_file_cache(
        self, file_path: Path, relative_path: str, analysis_result: dict[str, Any]
    ):
        """Update cache with new analysis result."""
        current_hash = self.get_file_hash(file_path)
        with self.cache_lock:
            self.cache[relative_path] = {
                "hash": current_hash,
                "last_analyzed": time.time(),
                "analysis": analysis_result,
            }

    def get_cached_analysis(self, relative_path: str) -> dict[str, Any]:
        """Get cached analysis result."""
        with self.cache_lock:
            cached_data = self.cache.get(relative_path, {})
            return cached_data.get("analysis", {})

    def detect_moved_files(self, current_files: set[Path], project_root: Path) -> dict[str, str]:
        """Detect files that have been moved by comparing hashes."""
        moved_files = {}
        current_hashes = {}

        # Calculate hashes for current files
        for file_path in current_files:
            file_hash = self.get_file_hash(file_path)
            if file_hash:
                current_hashes[file_hash] = str(file_path.relative_to(project_root))

        # Find matches in cache
        with self.cache_lock:
            for cached_path, cached_data in self.cache.items():
                cached_hash = cached_data.get("hash")
                if cached_hash and cached_hash in current_hashes:
                    new_path = current_hashes[cached_hash]
                    if cached_path != new_path:
                        moved_files[cached_path] = new_path

        return moved_files

    def cleanup_missing_files(self, current_files: set[Path], project_root: Path):
        """Remove cache entries for files that no longer exist."""
        current_paths = {str(f.relative_to(project_root)) for f in current_files}

        with self.cache_lock:
            missing_files = [path for path in self.cache.keys() if path not in current_paths]
            for missing_file in missing_files:
                del self.cache[missing_file]
                logger.debug(f"Removed cache entry for missing file: {missing_file}")

    def get_cache_stats(self) -> dict[str, Any]:
        """Get cache statistics."""
        with self.cache_lock:
            total_entries = len(self.cache)
            total_size = sum(len(str(entry)) for entry in self.cache.values())

            return {
                "total_entries": total_entries,
                "total_size_bytes": total_size,
                "cache_file": str(self.cache_file),
                "last_updated": max(
                    (entry.get("last_analyzed", 0) for entry in self.cache.values()), default=0
                ),
            }

    def clear_cache(self):
        """Clear all cache entries."""
        with self.cache_lock:
            self.cache.clear()
        logger.info("✅ Cache cleared")

    def invalidate_file(self, relative_path: str):
        """Invalidate cache entry for specific file."""
        with self.cache_lock:
            if relative_path in self.cache:
                del self.cache[relative_path]
                logger.debug(f"Invalidated cache for: {relative_path}")

    def batch_update_cache(self, updates: dict[str, dict[str, Any]]):
        """Batch update cache entries."""
        with self.cache_lock:
            for relative_path, analysis_result in updates.items():
                # Get file hash if we have the file path
                if "file_path" in analysis_result:
                    try:
                        file_path = Path(analysis_result["file_path"])
                        if file_path.exists():
                            current_hash = self.get_file_hash(file_path)
                            self.cache[relative_path] = {
                                "hash": current_hash,
                                "last_analyzed": time.time(),
                                "analysis": analysis_result,
                            }
                    except Exception as e:
                        logger.warning(f"Failed to update cache for {relative_path}: {e}")

        logger.info(f"✅ Batch updated {len(updates)} cache entries")
