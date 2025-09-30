#!/usr/bin/env python3
"""
Create Combined Devlog Export Core
==================================

Core functionality for creating combined devlog exports.

Author: Agent-4 (Captain & Operations Coordinator)
V2 Compliance: ≤400 lines, focused export functionality
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set

import requests


class CombinedExportCore:
    """Core functionality for creating combined devlog exports."""

    def __init__(self):
        """Initialize the export core."""
        self.combined_data: Dict = {
            "export_timestamp": datetime.now().isoformat(),
            "database_devlogs": [],
            "file_devlogs": [],
            "summary": {
                "total_database": 0,
                "total_files": 0,
                "total_combined": 0,
                "agents": set()
            },
        }

    def create_combined_export(self) -> str:
        """Create a combined export with both database and file devlogs."""
        print("🔄 Creating combined devlog export...")

        # Get database devlogs
        self._get_database_devlogs()

        # Get file devlogs
        self._get_file_devlogs()

        # Update summary
        self._update_summary()

        # Save combined export
        filename = self._save_export()

        # Print summary
        self._print_summary(filename)

        return filename

    def _get_database_devlogs(self):
        """Get devlogs from database."""
        try:
            response = requests.get("http://localhost:8002/api/devlogs/export/json")
            if response.status_code == 200:
                db_devlogs = response.json()
                self.combined_data["database_devlogs"] = db_devlogs
                self.combined_data["summary"]["total_database"] = len(db_devlogs)

                # Extract agents from database devlogs
                for devlog in db_devlogs:
                    metadata = devlog.get("metadata", {})
                    agent = metadata.get("agent_id", "Unknown")
                    if agent != "Unknown":
                        self.combined_data["summary"]["agents"].add(agent)
                print(f"✅ Loaded {len(db_devlogs)} database devlogs")
        except Exception as e:
            print(f"❌ Error getting database devlogs: {e}")

    def _get_file_devlogs(self):
        """Get devlogs from file system."""
        file_devlogs = []
        devlogs_dir = Path("devlogs")
        if devlogs_dir.exists():
            md_files = list(devlogs_dir.glob("*.md"))
            archive_files = (
                list((devlogs_dir / "archive").glob("*.md"))
                if (devlogs_dir / "archive").exists()
                else []
            )

            processed_count = 0
            for file_path in md_files + archive_files:
                try:
                    filename = file_path.name
                    content = file_path.read_text(encoding="utf-8", errors="replace")

                    if "_" in filename:
                        parts = filename.split("_")
                        if len(parts) >= 3:
                            agent_part = parts[1]
                            title_part = "_".join(parts[2:]).replace(".md", "")

                            file_devlogs.append(
                                {
                                    "id": filename,
                                    "source": "file",
                                    "filename": filename,
                                    "agent_id": agent_part,
                                    "title": title_part,
                                    "content": content,
                                    "file_path": str(file_path),
                                }
                            )

                            if agent_part.startswith("Agent-"):
                                self.combined_data["summary"]["agents"].add(agent_part)

                            processed_count += 1

                except Exception as e:
                    print(f"❌ Error reading {filename}: {e}")

            print(f"✅ Processed {processed_count} file devlogs")

        self.combined_data["file_devlogs"] = file_devlogs
        self.combined_data["summary"]["total_files"] = len(file_devlogs)

    def _update_summary(self):
        """Update summary statistics."""
        self.combined_data["summary"]["total_combined"] = (
            self.combined_data["summary"]["total_database"] +
            self.combined_data["summary"]["total_files"]
        )
        self.combined_data["summary"]["agents"] = sorted(
            list(self.combined_data["summary"]["agents"])
        )

    def _save_export(self) -> str:
        """Save the combined export to file."""
        filename = f"complete_devlog_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w") as f:
            json.dump(self.combined_data, f, indent=2)
        return filename

    def _print_summary(self, filename: str):
        """Print export summary."""
        print(f"✅ Complete export created: {filename}")
        print("📊 Summary:")
        print(f"  Database devlogs: {self.combined_data['summary']['total_database']}")
        print(f"  File devlogs: {self.combined_data['summary']['total_files']}")
        print(f"  Total: {self.combined_data['summary']['total_combined']}")
        print(f"  Unique agents: {len(self.combined_data['summary']['agents'])}")

        # Show file size
        file_size = Path(filename).stat().st_size
        print(f"  File size: {file_size} bytes")
