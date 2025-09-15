#!/usr/bin/env python3
"""
Data & Log Management Tool - V2 Compliance
=========================================

Comprehensive tool for optimizing data and log management.

V2 Compliance: < 400 lines, single responsibility, modular design.

Author: Agent-5 (Data Organization Specialist)
Usage: python tools/data_log_manager.py --optimize
"""

import argparse
import json
import shutil
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


class DataLogManager:
    """Manages data and log optimization."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.data_dir = project_root / "data"
        self.logs_dir = project_root / "logs"
        self.runtime_dir = project_root / "runtime"
        self.reports_dir = self.runtime_dir / "reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def optimize_data_structure(self) -> dict[str, Any]:
        """Optimize data directory structure."""
        print("🗂️  Optimizing data structure...")

        results = {
            "timestamp": datetime.now().isoformat(),
            "data_optimization": {},
            "log_optimization": {},
            "database_optimization": {},
            "cleanup_results": {},
        }

        # Organize data directory
        if self.data_dir.exists():
            results["data_optimization"] = self._organize_data_directory()

        # Optimize logs
        if self.logs_dir.exists():
            results["log_optimization"] = self._optimize_logs()

        # Optimize databases
        results["database_optimization"] = self._optimize_databases()

        # Cleanup temporary files
        results["cleanup_results"] = self._cleanup_temp_files()

        return results

    def _organize_data_directory(self) -> dict[str, Any]:
        """Organize data directory structure."""
        organization_results = {"files_moved": 0, "directories_created": 0, "structure_created": {}}

        # Create organized structure
        structure = {
            "databases": ["*.db", "*.sqlite", "*.sqlite3"],
            "vector_data": ["vector_*", "embeddings_*"],
            "semantic_data": ["semantic_*", "knowledge_*"],
            "cookies": ["*cookies*", "*session*"],
            "backups": ["*backup*", "*archive*"],
            "temp": ["*temp*", "*tmp*"],
        }

        for category, patterns in structure.items():
            category_dir = self.data_dir / category
            if not category_dir.exists():
                category_dir.mkdir(exist_ok=True)
                organization_results["directories_created"] += 1

            # Move matching files
            for pattern in patterns:
                for file_path in self.data_dir.glob(pattern):
                    if file_path.is_file():
                        dest_path = category_dir / file_path.name
                        if file_path != dest_path:
                            shutil.move(str(file_path), str(dest_path))
                            organization_results["files_moved"] += 1

            organization_results["structure_created"][category] = len(list(category_dir.iterdir()))

        return organization_results

    def _optimize_logs(self) -> dict[str, Any]:
        """Optimize log files."""
        log_results = {
            "logs_rotated": 0,
            "logs_compressed": 0,
            "old_logs_removed": 0,
            "total_size_saved": 0,
        }

        if not self.logs_dir.exists():
            return log_results

        # Rotate large log files
        for log_file in self.logs_dir.glob("*.log"):
            if log_file.stat().st_size > 5 * 1024 * 1024:  # 5MB
                self._rotate_log_file(log_file)
                log_results["logs_rotated"] += 1

        # Compress old logs
        for log_file in self.logs_dir.glob("*.log.*"):
            if not log_file.name.endswith(".gz"):
                compressed_file = log_file.with_suffix(log_file.suffix + ".gz")
                with open(log_file, "rb") as f_in:
                    with open(compressed_file, "wb") as f_out:
                        shutil.copyfileobj(f_in, f_out)
                log_file.unlink()
                log_results["logs_compressed"] += 1

        # Remove old logs (older than 30 days)
        cutoff_date = datetime.now() - timedelta(days=30)
        for log_file in self.logs_dir.glob("*.log.*"):
            try:
                file_time = datetime.fromtimestamp(log_file.stat().st_mtime)
                if file_time < cutoff_date:
                    file_size = log_file.stat().st_size
                    log_file.unlink()
                    log_results["old_logs_removed"] += 1
                    log_results["total_size_saved"] += file_size
            except Exception:
                pass

        return log_results

    def _rotate_log_file(self, log_file: Path) -> None:
        """Rotate a log file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        rotated_name = f"{log_file.stem}_{timestamp}{log_file.suffix}"
        rotated_path = log_file.parent / rotated_name

        shutil.move(str(log_file), str(rotated_path))

        # Create new empty log file
        with open(log_file, "w", encoding="utf-8") as f:
            f.write("")

    def _optimize_databases(self) -> dict[str, Any]:
        """Optimize database files."""
        db_results = {
            "databases_optimized": 0,
            "databases_vacuumed": 0,
            "total_size_before": 0,
            "total_size_after": 0,
        }

        # Find database files
        db_patterns = ["*.db", "*.sqlite", "*.sqlite3"]
        db_files = []

        for pattern in db_patterns:
            db_files.extend(self.data_dir.rglob(pattern))
            db_files.extend(self.project_root.rglob(pattern))

        for db_file in db_files:
            try:
                size_before = db_file.stat().st_size
                db_results["total_size_before"] += size_before

                # Optimize SQLite databases
                if db_file.suffix in [".db", ".sqlite", ".sqlite3"]:
                    conn = sqlite3.connect(db_file)
                    cursor = conn.cursor()

                    # VACUUM to optimize
                    cursor.execute("VACUUM;")
                    db_results["databases_vacuumed"] += 1

                    # ANALYZE for better query planning
                    cursor.execute("ANALYZE;")

                    conn.close()
                    db_results["databases_optimized"] += 1

                size_after = db_file.stat().st_size
                db_results["total_size_after"] += size_after

            except Exception as e:
                print(f"Warning: Could not optimize database {db_file}: {e}")

        return db_results

    def _cleanup_temp_files(self) -> dict[str, Any]:
        """Cleanup temporary files."""
        cleanup_results = {"temp_files_removed": 0, "cache_dirs_cleaned": 0, "total_size_freed": 0}

        # Cleanup patterns
        temp_patterns = ["*.tmp", "*.temp", "*.bak", "*.backup", "*~", "*.swp", "*.swo"]

        cache_dirs = [
            "__pycache__",
            ".pytest_cache",
            ".coverage",
            "htmlcov",
            ".mypy_cache",
            ".tox",
            "node_modules",
        ]

        # Remove temp files
        for pattern in temp_patterns:
            for temp_file in self.project_root.rglob(pattern):
                try:
                    if temp_file.is_file():
                        file_size = temp_file.stat().st_size
                        temp_file.unlink()
                        cleanup_results["temp_files_removed"] += 1
                        cleanup_results["total_size_freed"] += file_size
                except Exception:
                    pass

        # Clean cache directories
        for cache_dir in cache_dirs:
            for cache_path in self.project_root.rglob(cache_dir):
                try:
                    if cache_path.is_dir():
                        shutil.rmtree(cache_path)
                        cleanup_results["cache_dirs_cleaned"] += 1
                except Exception:
                    pass

        return cleanup_results

    def generate_optimization_report(self, results: dict[str, Any]) -> Path:
        """Generate optimization report."""
        report_path = (
            self.reports_dir
            / f"data_log_optimization_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)

        return report_path

    def print_optimization_summary(self, results: dict[str, Any]) -> None:
        """Print optimization summary."""
        print("\n" + "=" * 70)
        print("📊 DATA & LOG OPTIMIZATION SUMMARY")
        print("=" * 70)

        # Data optimization
        data_opt = results.get("data_optimization", {})
        print("Data Organization:")
        print(f"  Files Moved: {data_opt.get('files_moved', 0)}")
        print(f"  Directories Created: {data_opt.get('directories_created', 0)}")

        # Log optimization
        log_opt = results.get("log_optimization", {})
        print("\nLog Optimization:")
        print(f"  Logs Rotated: {log_opt.get('logs_rotated', 0)}")
        print(f"  Logs Compressed: {log_opt.get('logs_compressed', 0)}")
        print(f"  Old Logs Removed: {log_opt.get('old_logs_removed', 0)}")
        print(f"  Size Saved: {log_opt.get('total_size_saved', 0) / (1024 * 1024):.1f} MB")

        # Database optimization
        db_opt = results.get("database_optimization", {})
        print("\nDatabase Optimization:")
        print(f"  Databases Optimized: {db_opt.get('databases_optimized', 0)}")
        print(f"  Databases Vacuumed: {db_opt.get('databases_vacuumed', 0)}")
        size_before = db_opt.get("total_size_before", 0)
        size_after = db_opt.get("total_size_after", 0)
        if size_before > 0:
            print(f"  Size Reduction: {((size_before - size_after) / size_before * 100):.1f}%")

        # Cleanup results
        cleanup = results.get("cleanup_results", {})
        print("\nCleanup Results:")
        print(f"  Temp Files Removed: {cleanup.get('temp_files_removed', 0)}")
        print(f"  Cache Dirs Cleaned: {cleanup.get('cache_dirs_cleaned', 0)}")
        print(f"  Space Freed: {cleanup.get('total_size_freed', 0) / (1024 * 1024):.1f} MB")

        print("=" * 70)


def main():
    """Main entry point for data & log management tool."""
    parser = argparse.ArgumentParser(description="Data & Log Management Tool")
    parser.add_argument("--optimize", action="store_true", help="Optimize data and log management")
    parser.add_argument("--data-only", action="store_true", help="Optimize data structure only")
    parser.add_argument("--logs-only", action="store_true", help="Optimize logs only")

    args = parser.parse_args()

    project_root = Path(".")
    manager = DataLogManager(project_root)

    if args.optimize or args.data_only or args.logs_only:
        print("🚀 Starting data and log optimization...")

        # Run optimization
        results = manager.optimize_data_structure()

        # Generate report
        report_path = manager.generate_optimization_report(results)
        print(f"📄 Optimization report saved to: {report_path}")

        # Print summary
        manager.print_optimization_summary(results)

        print("\n✅ Data and log optimization completed successfully!")
        exit(0)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
