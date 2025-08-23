#!/usr/bin/env python3
"""
Scanner Cache Service - Agent Cellphone V2
==========================================

Caches scanner results for improved performance.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.
"""

import json
import time
import hashlib
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime, timedelta


class ScannerCacheService:
    """
    Caches scanner results for improved performance.

    Responsibilities:
    - Cache file analysis results
    - Manage cache expiration and cleanup
    - Provide cache statistics and monitoring
    - Optimize memory usage
    """

    def __init__(
        self,
        cache_dir: Path = None,
        max_cache_size: int = 1000,
        cache_ttl_hours: int = 24,
    ):
        self.cache_dir = cache_dir or Path("scanner_cache")
        self.cache_dir.mkdir(exist_ok=True)
        self.max_cache_size = max_cache_size
        self.cache_ttl_hours = cache_ttl_hours
        self.cache_stats = {"hits": 0, "misses": 0, "evictions": 0, "total_requests": 0}

    def get_cached_result(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Get cached result for a file if it exists and is valid"""
        try:
            cache_key = self._generate_cache_key(file_path)
            cache_file = self.cache_dir / f"{cache_key}.json"

            if not cache_file.exists():
                self.cache_stats["misses"] += 1
                self.cache_stats["total_requests"] += 1
                return None

            # Check if cache is expired
            if self._is_cache_expired(cache_file):
                cache_file.unlink()
                self.cache_stats["misses"] += 1
                self.cache_stats["total_requests"] += 1
                return None

            # Load cached result
            with open(cache_file, "r") as f:
                cached_data = json.load(f)

            self.cache_stats["hits"] += 1
            self.cache_stats["total_requests"] += 1
            return cached_data

        except Exception:
            self.cache_stats["misses"] += 1
            self.cache_stats["total_requests"] += 1
            return None

    def cache_result(self, file_path: Path, analysis_result: Dict[str, Any]) -> bool:
        """Cache analysis result for a file"""
        try:
            # Check cache size limit
            if self._get_cache_size() >= self.max_cache_size:
                self._evict_oldest_cache()

            # Prepare cache data
            cache_data = {
                "file_path": str(file_path),
                "file_hash": self._calculate_file_hash(file_path),
                "analysis_result": analysis_result,
                "cached_at": time.time(),
                "expires_at": time.time() + (self.cache_ttl_hours * 3600),
            }

            # Save to cache
            cache_key = self._generate_cache_key(file_path)
            cache_file = self.cache_dir / f"{cache_key}.json"

            with open(cache_file, "w") as f:
                json.dump(cache_data, f, indent=2, default=str)

            return True

        except Exception:
            return False

    def invalidate_cache(self, file_path: Path) -> bool:
        """Invalidate cache for a specific file"""
        try:
            cache_key = self._generate_cache_key(file_path)
            cache_file = self.cache_dir / f"{cache_key}.json"

            if cache_file.exists():
                cache_file.unlink()
                return True

            return False

        except Exception:
            return False

    def clear_cache(self) -> bool:
        """Clear all cached data"""
        try:
            for cache_file in self.cache_dir.glob("*.json"):
                cache_file.unlink()

            self.cache_stats["evictions"] += 1
            return True

        except Exception:
            return False

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get comprehensive cache statistics"""
        try:
            cache_files = list(self.cache_dir.glob("*.json"))
            current_size = len(cache_files)

            # Calculate cache hit rate
            hit_rate = 0.0
            if self.cache_stats["total_requests"] > 0:
                hit_rate = (
                    self.cache_stats["hits"] / self.cache_stats["total_requests"]
                ) * 100

            # Calculate cache size in bytes
            total_size_bytes = sum(f.stat().st_size for f in cache_files)

            # Get oldest and newest cache entries
            cache_ages = []
            for cache_file in cache_files:
                try:
                    with open(cache_file, "r") as f:
                        data = json.load(f)
                        cached_at = data.get("cached_at", 0)
                        cache_ages.append(time.time() - cached_at)
                except:
                    continue

            stats = {
                "cache_size": current_size,
                "max_cache_size": self.max_cache_size,
                "cache_usage_percent": (current_size / self.max_cache_size) * 100
                if self.max_cache_size > 0
                else 0,
                "total_size_bytes": total_size_bytes,
                "hit_rate": round(hit_rate, 2),
                "hits": self.cache_stats["hits"],
                "misses": self.cache_stats["misses"],
                "evictions": self.cache_stats["evictions"],
                "total_requests": self.cache_stats["total_requests"],
                "cache_ttl_hours": self.cache_ttl_hours,
            }

            if cache_ages:
                stats["oldest_cache_age_hours"] = round(max(cache_ages) / 3600, 2)
                stats["newest_cache_age_hours"] = round(min(cache_ages) / 3600, 2)
                stats["average_cache_age_hours"] = round(
                    sum(cache_ages) / len(cache_ages) / 3600, 2
                )

            return stats

        except Exception as e:
            return {"error": str(e), "status": "failed"}

    def cleanup_expired_cache(self) -> int:
        """Remove expired cache entries and return count of cleaned entries"""
        try:
            cleaned_count = 0
            current_time = time.time()

            for cache_file in self.cache_dir.glob("*.json"):
                try:
                    with open(cache_file, "r") as f:
                        data = json.load(f)
                        expires_at = data.get("expires_at", 0)

                        if current_time > expires_at:
                            cache_file.unlink()
                            cleaned_count += 1

                except Exception:
                    # Remove corrupted cache files
                    cache_file.unlink()
                    cleaned_count += 1

            return cleaned_count

        except Exception:
            return 0

    def _generate_cache_key(self, file_path: Path) -> str:
        """Generate unique cache key for a file"""
        # Use file path and modification time for cache key
        file_stat = file_path.stat()
        key_string = f"{file_path}_{file_stat.st_mtime}_{file_stat.st_size}"
        return hashlib.md5(key_string.encode()).hexdigest()

    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of file content"""
        try:
            with open(file_path, "rb") as f:
                content = f.read()
                return hashlib.sha256(content).hexdigest()
        except Exception:
            return "unknown"

    def _is_cache_expired(self, cache_file: Path) -> bool:
        """Check if cache file is expired"""
        try:
            with open(cache_file, "r") as f:
                data = json.load(f)
                expires_at = data.get("expires_at", 0)
                return time.time() > expires_at
        except Exception:
            return True

    def _get_cache_size(self) -> int:
        """Get current number of cache files"""
        try:
            return len(list(self.cache_dir.glob("*.json")))
        except Exception:
            return 0

    def _evict_oldest_cache(self) -> bool:
        """Remove oldest cache entry to make room for new ones"""
        try:
            cache_files = []

            # Get all cache files with their ages
            for cache_file in self.cache_dir.glob("*.json"):
                try:
                    with open(cache_file, "r") as f:
                        data = json.load(f)
                        cached_at = data.get("cached_at", 0)
                        cache_files.append((cache_file, cached_at))
                except Exception:
                    # Remove corrupted files
                    cache_file.unlink()
                    continue

            if not cache_files:
                return False

            # Find oldest cache file
            oldest_cache = min(cache_files, key=lambda x: x[1])
            oldest_cache[0].unlink()

            self.cache_stats["evictions"] += 1
            return True

        except Exception:
            return False

    def get_cache_info(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Get detailed cache information for a specific file"""
        try:
            cache_key = self._generate_cache_key(file_path)
            cache_file = self.cache_dir / f"{cache_key}.json"

            if not cache_file.exists():
                return None

            with open(cache_file, "r") as f:
                data = json.load(f)

            # Calculate age and time until expiration
            current_time = time.time()
            cached_at = data.get("cached_at", 0)
            expires_at = data.get("expires_at", 0)

            age_hours = (current_time - cached_at) / 3600
            ttl_hours = (expires_at - current_time) / 3600

            return {
                "file_path": str(file_path),
                "cached_at": datetime.fromtimestamp(cached_at).isoformat(),
                "expires_at": datetime.fromtimestamp(expires_at).isoformat(),
                "age_hours": round(age_hours, 2),
                "ttl_hours": round(ttl_hours, 2),
                "is_expired": ttl_hours <= 0,
                "file_hash": data.get("file_hash", "unknown"),
            }

        except Exception:
            return None
