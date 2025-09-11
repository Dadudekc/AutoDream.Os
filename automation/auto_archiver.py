#!/usr/bin/env python3
"""
🐝 SWARM Auto Archiver

Automated system for archiving old files based on age thresholds.
Compresses and organizes archived files for long-term storage.

Features:
- Age-based archiving (>30 days by default)
- Intelligent file type detection
- Compression support
- Archive organization and indexing
- Integration with maintenance orchestrator

Author: Agent-7 (Web Development Specialist)
Position: Monitor 2 (920, 851)
Created: 2025-09-11
"""

import gzip
import json
import logging
import os
import shutil
import zipfile
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class AutoArchiver:
    """Intelligent file archiving system."""

    def __init__(self, config_path: str = "automation/maintenance_config.json"):
        self.config_path = Path(config_path)
        self.root_path = Path.cwd()
        self.archive_base = self.root_path / "automated_archives"
        self.index_file = self.archive_base / "archive_index.json"

        # Load configuration
        self.config = self._load_config()

        # Setup logging
        self._setup_logging()

        # Load archive index
        self.archive_index = self._load_archive_index()

    def _load_config(self) -> Dict:
        """Load configuration from file."""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return {}

    def _setup_logging(self):
        """Setup logging for archiving operations."""
        logs_dir = Path("automation_logs")
        logs_dir.mkdir(exist_ok=True)

        logging.basicConfig(
            filename=logs_dir / f"archiver_{datetime.now().strftime('%Y%m%d')}.log",
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def _load_archive_index(self) -> Dict:
        """Load archive index for tracking archived files."""
        if self.index_file.exists():
            try:
                with open(self.index_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return {"archives": {}, "files": {}}

    def _save_archive_index(self):
        """Save archive index."""
        with open(self.index_file, 'w') as f:
            json.dump(self.archive_index, f, indent=2)

    def identify_archivable_files(self) -> List[Path]:
        """Identify files that should be archived based on configuration."""
        self.logger.info("Identifying files for archiving...")

        archivable_files = []
        archiving_config = self.config.get("archiving", {})
        age_threshold = datetime.now() - timedelta(days=archiving_config.get("age_threshold_days", 30))

        # File extensions to archive
        archive_extensions = set(archiving_config.get("archive_extensions", []))
        exclude_patterns = set(archiving_config.get("exclude_patterns", []))

        exclusions = self.config.get("exclusions", {}).get("skip_directories", [])

        for file_path in self.root_path.rglob("*"):
            if file_path.is_file():
                # Skip excluded directories
                if any(skip in str(file_path) for skip in exclusions):
                    continue

                try:
                    # Check file age
                    file_age = datetime.fromtimestamp(file_path.stat().st_mtime)

                    # Check if file should be archived
                    should_archive = (
                        file_age < age_threshold and
                        (file_path.suffix in archive_extensions or
                         file_path.suffix not in exclude_patterns)
                    )

                    if should_archive and str(file_path) not in self.archive_index.get("files", {}):
                        archivable_files.append(file_path)

                except Exception as e:
                    self.logger.error(f"Error checking file {file_path}: {e}")

        return archivable_files

    def create_archive_batch(self, files: List[Path], batch_name: str) -> Path:
        """Create a compressed archive batch."""
        archiving_config = self.config.get("archiving", {})

        # Create archive directory structure
        archive_date = datetime.now().strftime("%Y%m%d")
        archive_dir = self.archive_base / archive_date
        archive_dir.mkdir(parents=True, exist_ok=True)

        # Archive file path
        if archiving_config.get("archive_compression", True):
            archive_path = archive_dir / f"{batch_name}_{archive_date}.zip"
            return self._create_zip_archive(files, archive_path)
        else:
            archive_path = archive_dir / f"{batch_name}_{archive_date}"
            archive_path.mkdir(exist_ok=True)
            return self._create_directory_archive(files, archive_path)

    def _create_zip_archive(self, files: List[Path], archive_path: Path) -> Path:
        """Create a ZIP archive of the files."""
        self.logger.info(f"Creating ZIP archive: {archive_path}")

        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file_path in files:
                try:
                    # Add file to archive with relative path
                    arcname = file_path.relative_to(self.root_path)
                    zip_file.write(str(file_path), str(arcname))

                    # Track in index
                    self.archive_index["files"][str(file_path)] = {
                        "archive": str(archive_path),
                        "original_path": str(file_path),
                        "archived_date": datetime.now().isoformat(),
                        "size_bytes": file_path.stat().st_size
                    }

                except Exception as e:
                    self.logger.error(f"Error adding {file_path} to archive: {e}")

        return archive_path

    def _create_directory_archive(self, files: List[Path], archive_path: Path) -> Path:
        """Create a directory-based archive (no compression)."""
        self.logger.info(f"Creating directory archive: {archive_path}")

        for file_path in files:
            try:
                # Copy file to archive directory
                relative_path = file_path.relative_to(self.root_path)
                archive_file_path = archive_path / relative_path
                archive_file_path.parent.mkdir(parents=True, exist_ok=True)

                shutil.copy2(str(file_path), str(archive_file_path))

                # Track in index
                self.archive_index["files"][str(file_path)] = {
                    "archive": str(archive_path),
                    "original_path": str(file_path),
                    "archived_date": datetime.now().isoformat(),
                    "size_bytes": file_path.stat().st_size
                }

            except Exception as e:
                self.logger.error(f"Error copying {file_path} to archive: {e}")

        return archive_path

    def remove_archived_files(self, files: List[Path]) -> Dict[str, int]:
        """Remove successfully archived files from original location."""
        removal_stats = {"removed": 0, "errors": 0}

        for file_path in files:
            try:
                if file_path.exists():
                    file_path.unlink()
                    removal_stats["removed"] += 1
                    self.logger.info(f"Removed archived file: {file_path}")
            except Exception as e:
                self.logger.error(f"Error removing {file_path}: {e}")
                removal_stats["errors"] += 1

        return removal_stats

    def cleanup_old_archives(self) -> Dict[str, int]:
        """Clean up archives older than the maximum age."""
        self.logger.info("Cleaning up old archives...")

        cleanup_stats = {"removed": 0, "errors": 0}
        archiving_config = self.config.get("archiving", {})
        max_age = archiving_config.get("max_archive_age_days", 365)
        age_threshold = datetime.now() - timedelta(days=max_age)

        if not self.archive_base.exists():
            return cleanup_stats

        for archive_path in self.archive_base.rglob("*"):
            if archive_path.is_file():
                try:
                    archive_age = datetime.fromtimestamp(archive_path.stat().st_mtime)

                    if archive_age < age_threshold:
                        archive_path.unlink()
                        cleanup_stats["removed"] += 1
                        self.logger.info(f"Removed old archive: {archive_path}")

                        # Remove from index
                        archive_str = str(archive_path)
                        if archive_str in self.archive_index.get("archives", {}):
                            del self.archive_index["archives"][archive_str]

                except Exception as e:
                    self.logger.error(f"Error cleaning up {archive_path}: {e}")
                    cleanup_stats["errors"] += 1

        return cleanup_stats

    def generate_archive_report(self, archivable_files: List[Path],
                               archive_path: Path, removal_stats: Dict[str, int],
                               cleanup_stats: Dict[str, int]) -> Path:
        """Generate comprehensive archive report."""
        reports_dir = Path("automation_reports")
        reports_dir.mkdir(exist_ok=True)

        report_path = reports_dir / f"archive_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        content = [
            "# 🐝 SWARM Archive Report\n\n",
            f"**Report Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
            f"**Agent:** Agent-7 (Web Development Specialist)\n",
            f"**Position:** Monitor 2 (920, 851)\n\n",
            "---\n\n"
        ]

        # Summary
        content.append("## 📊 Archive Summary\n\n")
        content.append(f"- **Files Identified:** {len(archivable_files)}\n")
        content.append(f"- **Archive Created:** {archive_path}\n")
        content.append(f"- **Files Removed:** {removal_stats['removed']}\n")
        if removal_stats['errors'] > 0:
            content.append(f"- **Removal Errors:** {removal_stats['errors']}\n")
        content.append(f"- **Old Archives Cleaned:** {cleanup_stats['removed']}\n\n")

        # Configuration
        archiving_config = self.config.get("archiving", {})
        content.append("## ⚙️ Archive Configuration\n\n")
        content.append(f"- **Age Threshold:** {archiving_config.get('age_threshold_days', 30)} days\n")
        content.append(f"- **Archive Extensions:** {', '.join(archiving_config.get('archive_extensions', []))}\n")
        content.append(f"- **Excluded Patterns:** {', '.join(archiving_config.get('exclude_patterns', []))}\n")
        content.append(f"- **Compression:** {'Enabled' if archiving_config.get('archive_compression', True) else 'Disabled'}\n")
        content.append(f"- **Max Archive Age:** {archiving_config.get('max_archive_age_days', 365)} days\n\n")

        # Archived files list (first 20)
        if archivable_files:
            content.append("## 📦 Archived Files\n\n")
            for i, file_path in enumerate(archivable_files[:20]):
                content.append(f"{i+1}. `{file_path.relative_to(self.root_path)}`\n")

            if len(archivable_files) > 20:
                content.append(f"\n... and {len(archivable_files) - 20} more files\n")

            content.append("\n")

        # Archive storage info
        content.append("## 🗂️ Archive Storage\n\n")
        content.append(f"- **Archive Location:** `{self.archive_base}`\n")
        content.append(f"- **Total Archives:** {len(list(self.archive_base.rglob('*')))}\n")
        content.append(f"- **Index File:** `{self.index_file}`\n\n")

        # Recommendations
        content.append("## 💡 Recommendations\n\n")

        if len(archivable_files) > 100:
            content.append("⚠️ **High Volume Alert:** Consider reducing the age threshold or increasing archiving frequency.\n\n")

        if removal_stats['errors'] > 0:
            content.append("⚠️ **Removal Errors:** Some archived files could not be removed from original location.\n\n")

        content.append("### Maintenance Tips:\n")
        content.append("- Regularly review archive contents\n")
        content.append("- Consider backup strategies for archives\n")
        content.append("- Monitor archive storage usage\n")
        content.append("- Update archiving rules as needed\n\n")

        content.append("**🐝 WE ARE SWARM - ARCHIVING COMPLETE**\n")

        with open(report_path, 'w', encoding='utf-8') as f:
            f.writelines(content)

        return report_path

    def run_archiving_cycle(self) -> Dict[str, any]:
        """Run complete archiving cycle."""
        self.logger.info("Starting archiving cycle...")

        # 1. Identify files to archive
        archivable_files = self.identify_archivable_files()
        self.logger.info(f"Found {len(archivable_files)} files to archive")

        if not archivable_files:
            self.logger.info("No files to archive")
            return {"archived_files": 0, "archives_created": 0}

        # 2. Create archive batch
        batch_name = f"archive_batch_{datetime.now().strftime('%H%M%S')}"
        archive_path = self.create_archive_batch(archivable_files, batch_name)

        # 3. Remove archived files
        removal_stats = self.remove_archived_files(archivable_files)

        # 4. Clean up old archives
        cleanup_stats = self.cleanup_old_archives()

        # 5. Generate report
        report_path = self.generate_archive_report(
            archivable_files, archive_path, removal_stats, cleanup_stats
        )

        # 6. Update archive index
        self.archive_index["archives"][str(archive_path)] = {
            "created_date": datetime.now().isoformat(),
            "file_count": len(archivable_files),
            "total_size_bytes": sum(f.stat().st_size for f in archivable_files if f.exists()),
            "compression": self.config.get("archiving", {}).get("archive_compression", True)
        }
        self._save_archive_index()

        results = {
            "archived_files": len(archivable_files),
            "archives_created": 1,
            "archive_path": str(archive_path),
            "removal_stats": removal_stats,
            "cleanup_stats": cleanup_stats,
            "report_path": str(report_path),
            "timestamp": datetime.now().isoformat()
        }

        self.logger.info(f"Archiving cycle complete. Archived {len(archivable_files)} files")
        return results

def main():
    """Main entry point for auto archiver."""
    import argparse

    parser = argparse.ArgumentParser(description="SWARM Auto Archiver")
    parser.add_argument("--config", default="automation/maintenance_config.json",
                       help="Path to configuration file")
    parser.add_argument("--dry-run", action="store_true",
                       help="Show what would be archived without actually doing it")
    parser.add_argument("--cleanup-only", action="store_true",
                       help="Only clean up old archives")

    args = parser.parse_args()

    archiver = AutoArchiver(args.config)

    if args.cleanup_only:
        cleanup_stats = archiver.cleanup_old_archives()
        print(f"🧹 Cleaned up {cleanup_stats['removed']} old archives")
        return

    if args.dry_run:
        archivable_files = archiver.identify_archivable_files()
        print(f"📦 Would archive {len(archivable_files)} files:")
        for file_path in archivable_files[:10]:
            print(f"  - {file_path}")
        if len(archivable_files) > 10:
            print(f"  ... and {len(archivable_files) - 10} more")
        return

    # Run full archiving cycle
    results = archiver.run_archiving_cycle()
    print("📦 Archiving complete!"    print(f"  Files archived: {results['archived_files']}")
    print(f"  Archives created: {results['archives_created']}")
    print(f"  Archive location: {results['archive_path']}")
    print(f"  Report: {results['report_path']}")

if __name__ == "__main__":
    main()
