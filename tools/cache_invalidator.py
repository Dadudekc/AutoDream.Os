#!/usr/bin/env python3
"""
Cache Invalidator Tool - Project Scanner Cache Management
==========================================================

Clears outdated cache data to force fresh project scans.
Based on Agent-1 session learning: Outdated cache causes repeated false assignments!

Usage:
    python tools/cache_invalidator.py --clear-all
    python tools/cache_invalidator.py --clear dependency_cache.json
    python tools/cache_invalidator.py --clear-analysis-chunks
    python tools/cache_invalidator.py --verify

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-10-13
License: MIT
"""

import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class CacheInvalidator:
    """Manages project scanner cache invalidation."""

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or PROJECT_ROOT
        self.cache_files = {
            "dependency_cache": self.project_root / "dependency_cache.json",
            "project_analysis": self.project_root / "project_analysis.json",
            "test_analysis": self.project_root / "test_analysis.json",
            "chatgpt_context": self.project_root / "chatgpt_project_context.json",
        }
        self.cache_dirs = {
            "analysis_chunks": self.project_root / "analysis_chunks",
            "analysis": self.project_root / "analysis",
        }

    def check_cache_age(self) -> dict:
        """Check age of all cache files."""
        results = {}

        for name, path in self.cache_files.items():
            if path.exists():
                mtime = datetime.fromtimestamp(path.stat().st_mtime)
                age_days = (datetime.now() - mtime).days
                results[name] = {
                    "path": str(path),
                    "exists": True,
                    "modified": mtime.isoformat(),
                    "age_days": age_days,
                    "status": "🔴 OLD" if age_days > 1 else "🟢 RECENT",
                }
            else:
                results[name] = {"path": str(path), "exists": False}

        return results

    def clear_cache_file(self, cache_name: str) -> bool:
        """Clear a specific cache file."""
        if cache_name not in self.cache_files:
            print(f"❌ Unknown cache: {cache_name}")
            return False

        cache_path = self.cache_files[cache_name]
        if cache_path.exists():
            backup_path = cache_path.with_suffix(".json.backup")
            shutil.copy2(cache_path, backup_path)
            cache_path.unlink()
            print(f"✅ Cleared {cache_name}: {cache_path}")
            print(f"📦 Backup saved: {backup_path}")
            return True
        else:
            print(f"⚠️  Cache file doesn't exist: {cache_path}")
            return False

    def clear_all_caches(self, backup: bool = True) -> dict:
        """Clear all cache files."""
        results = {}

        print("🗑️  Clearing all cache files...\n")

        for name, path in self.cache_files.items():
            if path.exists():
                if backup:
                    backup_path = path.with_suffix(
                        f'.json.backup.{datetime.now().strftime("%Y%m%d_%H%M%S")}'
                    )
                    shutil.copy2(path, backup_path)
                    print(f"📦 Backup: {backup_path}")

                path.unlink()
                print(f"✅ Cleared: {path}")
                results[name] = "CLEARED"
            else:
                print(f"⚠️  Not found: {path}")
                results[name] = "NOT_FOUND"

        return results

    def clear_analysis_chunks(self) -> bool:
        """Clear analysis chunks directory."""
        chunks_dir = self.cache_dirs["analysis_chunks"]

        if not chunks_dir.exists():
            print(f"⚠️  Analysis chunks directory doesn't exist: {chunks_dir}")
            return False

        # Backup first
        backup_dir = chunks_dir.with_name(
            f"analysis_chunks_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        shutil.copytree(chunks_dir, backup_dir)
        print(f"📦 Backup: {backup_dir}")

        # Clear chunks
        shutil.rmtree(chunks_dir)
        chunks_dir.mkdir()
        print(f"✅ Cleared analysis chunks: {chunks_dir}")
        return True

    def verify_caches(self) -> dict:
        """Verify cache state and provide recommendations."""
        cache_ages = self.check_cache_age()

        print("\n📊 CACHE STATUS REPORT")
        print("=" * 70)

        needs_refresh = []
        for name, info in cache_ages.items():
            if info["exists"]:
                age_days = info["age_days"]
                status = info["status"]
                print(f"\n{status} {name}:")
                print(f"  Age: {age_days} days")
                print(f"  Modified: {info['modified']}")

                if age_days > 1:
                    needs_refresh.append(name)
            else:
                print(f"\n⚪ {name}: NOT FOUND")

        print("\n" + "=" * 70)

        if needs_refresh:
            print(f"\n⚠️  RECOMMENDATION: Refresh {len(needs_refresh)} old cache(s):")
            for name in needs_refresh:
                print(f"  - {name}")
            print("\nRun: python tools/cache_invalidator.py --clear-all")
        else:
            print("\n✅ All caches are recent!")

        return cache_ages


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="🗑️ Clear outdated project scanner caches",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Verify cache status
  python tools/cache_invalidator.py --verify
  
  # Clear all caches (with backup)
  python tools/cache_invalidator.py --clear-all
  
  # Clear specific cache
  python tools/cache_invalidator.py --clear dependency_cache
  
  # Clear analysis chunks
  python tools/cache_invalidator.py --clear-analysis-chunks
  
  # Nuclear option (clear everything, no backup)
  python tools/cache_invalidator.py --clear-all --no-backup

⚠️  USE WHEN: Getting outdated task assignments or scan data is weeks old!
        """,
    )

    parser.add_argument("--verify", action="store_true", help="Verify cache status")
    parser.add_argument("--clear-all", action="store_true", help="Clear all cache files")
    parser.add_argument(
        "--clear", type=str, help="Clear specific cache (dependency_cache, project_analysis, etc)"
    )
    parser.add_argument(
        "--clear-analysis-chunks", action="store_true", help="Clear analysis chunks directory"
    )
    parser.add_argument("--no-backup", action="store_true", help="Skip backup before clearing")

    args = parser.parse_args()

    invalidator = CacheInvalidator()

    if args.verify or not any([args.clear_all, args.clear, args.clear_analysis_chunks]):
        invalidator.verify_caches()
        return 0

    if args.clear_all:
        backup = not args.no_backup
        invalidator.clear_all_caches(backup=backup)
        print("\n✅ All caches cleared!")
        print("📝 Run: python tools/run_project_scan.py (to regenerate)")
        return 0

    if args.clear:
        invalidator.clear_cache_file(args.clear)
        return 0

    if args.clear_analysis_chunks:
        invalidator.clear_analysis_chunks()
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
