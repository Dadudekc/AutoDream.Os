#!/usr/bin/env python3
"""
Data Organization System for Agent Cellphone V2 Repository
==========================================================

Organizes and optimizes data directory structure.
Implements data cleanup, compression, and organization.

Author: Agent-5 (Data Organization Specialist)
Mission: DATA-ORGANIZE-001
License: MIT
"""

import json
import logging
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class DataOrganizer:
    """Organizes and optimizes data directory structure."""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.backup_dir = self.data_dir / "backups"
        self.archive_dir = self.data_dir / "archive"

    def create_directory_structure(self):
        """Create organized directory structure."""
        directories = [
            self.data_dir / "databases",
            self.data_dir / "vector_data",
            self.data_dir / "semantic_data",
            self.data_dir / "cookies",
            self.data_dir / "backups",
            self.data_dir / "archive",
            self.data_dir / "temp",
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {directory}")

    def organize_databases(self):
        """Organize database files."""
        db_files = list(self.data_dir.glob("*.db"))

        for db_file in db_files:
            target_dir = self.data_dir / "databases"
            target_path = target_dir / db_file.name

            if not target_path.exists():
                shutil.move(str(db_file), str(target_path))
                logger.info(f"Moved database: {db_file.name} -> databases/")

    def organize_vector_data(self):
        """Organize vector database files."""
        vector_dir = self.data_dir / "vector_db"
        if vector_dir.exists():
            target_dir = self.data_dir / "vector_data"
            target_dir.mkdir(exist_ok=True)

            # Move vector database files
            for item in vector_dir.iterdir():
                target_path = target_dir / item.name
                if not target_path.exists():
                    shutil.move(str(item), str(target_path))
                    logger.info(f"Moved vector data: {item.name} -> vector_data/")

            # Remove empty vector_db directory
            if not any(vector_dir.iterdir()):
                vector_dir.rmdir()
                logger.info("Removed empty vector_db directory")

    def organize_semantic_data(self):
        """Organize semantic seed data."""
        semantic_dir = self.data_dir / "semantic_seed"
        if semantic_dir.exists():
            target_dir = self.data_dir / "semantic_data"
            target_dir.mkdir(exist_ok=True)

            # Move semantic data
            for item in semantic_dir.iterdir():
                target_path = target_dir / item.name
                if not target_path.exists():
                    shutil.move(str(item), str(target_path))
                    logger.info(f"Moved semantic data: {item.name} -> semantic_data/")

            # Remove empty semantic_seed directory
            if not any(semantic_dir.iterdir()):
                semantic_dir.rmdir()
                logger.info("Removed empty semantic_seed directory")

    def organize_cookies(self):
        """Organize cookie files."""
        cookie_files = list(self.data_dir.glob("*cookies*.json"))

        for cookie_file in cookie_files:
            target_dir = self.data_dir / "cookies"
            target_path = target_dir / cookie_file.name

            if not target_path.exists():
                shutil.move(str(cookie_file), str(target_path))
                logger.info(f"Moved cookie file: {cookie_file.name} -> cookies/")

    def optimize_databases(self):
        """Optimize database files."""
        db_dir = self.data_dir / "databases"

        for db_file in db_dir.glob("*.db"):
            try:
                # Connect to database and run VACUUM
                conn = sqlite3.connect(str(db_file))
                conn.execute("VACUUM")
                conn.close()
                logger.info(f"Optimized database: {db_file.name}")
            except Exception as e:
                logger.error(f"Failed to optimize database {db_file.name}: {e}")

    def create_data_index(self):
        """Create an index of all data files."""
        index_data = {
            "created": datetime.now().isoformat(),
            "directories": {},
            "files": {},
            "total_size": 0,
        }

        # Index directories
        for item in self.data_dir.rglob("*"):
            if item.is_dir():
                rel_path = item.relative_to(self.data_dir)
                index_data["directories"][str(rel_path)] = {
                    "path": str(rel_path),
                    "created": datetime.fromtimestamp(item.stat().st_ctime).isoformat(),
                }
            elif item.is_file():
                rel_path = item.relative_to(self.data_dir)
                file_size = item.stat().st_size
                index_data["files"][str(rel_path)] = {
                    "path": str(rel_path),
                    "size": file_size,
                    "modified": datetime.fromtimestamp(item.stat().st_mtime).isoformat(),
                }
                index_data["total_size"] += file_size

        # Save index
        index_file = self.data_dir / "data_index.json"
        with open(index_file, "w") as f:
            json.dump(index_data, f, indent=2)

        logger.info(f"Created data index: {index_file}")
        return index_data

    def organize_all(self):
        """Run complete data organization."""
        logger.info("Starting data organization...")

        # Create directory structure
        self.create_directory_structure()

        # Organize different data types
        self.organize_databases()
        self.organize_vector_data()
        self.organize_semantic_data()
        self.organize_cookies()

        # Optimize databases
        self.optimize_databases()

        # Create data index
        index_data = self.create_data_index()

        logger.info("Data organization completed!")
        return index_data


def main():
    """Main entry point for data organization."""
    import argparse

    parser = argparse.ArgumentParser(description="Data Organization System")
    parser.add_argument("--data-dir", default="data", help="Data directory to organize")
    parser.add_argument(
        "--dry-run", action="store_true", help="Show what would be done without making changes"
    )

    args = parser.parse_args()

    # Setup logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # Create data organizer
    organizer = DataOrganizer(args.data_dir)

    if args.dry_run:
        print("DRY RUN: Data organization would:")
        print("  - Create organized directory structure")
        print("  - Move database files to databases/")
        print("  - Move vector data to vector_data/")
        print("  - Move semantic data to semantic_data/")
        print("  - Move cookie files to cookies/")
        print("  - Optimize database files")
        print("  - Create data index")
    else:
        # Run organization
        index_data = organizer.organize_all()

        print("Data organization completed!")
        print(f"Total data size: {index_data['total_size'] / 1024 / 1024:.2f} MB")
        print(f"Files organized: {len(index_data['files'])}")
        print(f"Directories created: {len(index_data['directories'])}")


if __name__ == "__main__":
    main()
