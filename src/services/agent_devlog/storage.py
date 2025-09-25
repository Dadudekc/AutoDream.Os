#!/usr/bin/env python3
"""
Agent Devlog Storage
===================

Storage management for Agent Devlog Posting Service
V2 Compliant: ≤400 lines, focused storage logic
"""

import json
import os
import gzip
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from .models import DevlogEntry, DevlogStatus, DevlogType, DevlogStats


class DevlogStorage:
    """Agent devlog storage management"""

    def __init__(self, devlogs_dir: str = "devlogs"):
        """Initialize devlog storage"""
        self.devlogs_dir = Path(devlogs_dir)
        self.devlogs_dir.mkdir(exist_ok=True)
        self.current_file = self._get_current_file()

    def _get_current_file(self) -> Path:
        """Get current devlog file based on date"""
        today = datetime.now().strftime("%Y%m%d")
        return self.devlogs_dir / f"devlogs_{today}.json"

    def save_devlog(self, devlog_entry: DevlogEntry) -> bool:
        """Save devlog entry to file"""
        try:
            # Convert to dictionary
            devlog_data = {
                "agent_id": devlog_entry.agent_id,
                "action": devlog_entry.action,
                "status": devlog_entry.status.value,
                "details": devlog_entry.details,
                "timestamp": devlog_entry.timestamp,
                "devlog_type": devlog_entry.devlog_type.value,
                "metadata": devlog_entry.metadata
            }

            # Load existing devlogs
            devlogs = self._load_devlogs()

            # Add new devlog
            devlogs.append(devlog_data)

            # Save back to file
            self._save_devlogs(devlogs)

            return True

        except Exception as e:
            print(f"❌ Failed to save devlog: {e}")
            return False

    def _load_devlogs(self) -> List[Dict[str, Any]]:
        """Load devlogs from file"""
        try:
            if self.current_file.exists():
                with open(self.current_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"❌ Failed to load devlogs: {e}")
            return []

    def _save_devlogs(self, devlogs: List[Dict[str, Any]]) -> None:
        """Save devlogs to file"""
        try:
            with open(self.current_file, 'w', encoding='utf-8') as f:
                json.dump(devlogs, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Failed to save devlogs: {e}")

    def search_devlogs(self, query: str, agent_id: Optional[str] = None, 
                      status: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Search devlogs by query"""
        try:
            devlogs = self._load_devlogs()
            results = []

            for devlog in devlogs:
                # Apply filters
                if agent_id and devlog.get("agent_id") != agent_id:
                    continue
                if status and devlog.get("status") != status:
                    continue

                # Search in content
                content = f"{devlog.get('action', '')} {devlog.get('details', '')}".lower()
                if query.lower() in content:
                    results.append(devlog)

                if len(results) >= limit:
                    break

            return results

        except Exception as e:
            print(f"❌ Failed to search devlogs: {e}")
            return []

    def get_devlog_stats(self) -> DevlogStats:
        """Get devlog statistics"""
        try:
            devlogs = self._load_devlogs()

            # Count by agent
            agent_counts = {}
            status_counts = {}
            type_counts = {}

            for devlog in devlogs:
                agent_id = devlog.get("agent_id", "unknown")
                status = devlog.get("status", "unknown")
                devlog_type = devlog.get("devlog_type", "unknown")

                agent_counts[agent_id] = agent_counts.get(agent_id, 0) + 1
                status_counts[status] = status_counts.get(status, 0) + 1
                type_counts[devlog_type] = type_counts.get(devlog_type, 0) + 1

            # Get recent activity
            recent_activity = []
            for devlog in devlogs[-10:]:  # Last 10 entries
                recent_activity.append(f"{devlog.get('agent_id')}: {devlog.get('action')}")

            return DevlogStats(
                total_devlogs=len(devlogs),
                agent_counts=agent_counts,
                status_counts=status_counts,
                type_counts=type_counts,
                recent_activity=recent_activity
            )

        except Exception as e:
            print(f"❌ Failed to get devlog stats: {e}")
            return DevlogStats(0, {}, {}, {}, [])

    def cleanup_old_files(self, days_to_keep: int = 30) -> int:
        """Cleanup old devlog files"""
        try:
            cutoff_date = datetime.now().timestamp() - (days_to_keep * 24 * 60 * 60)
            deleted_count = 0

            for file_path in self.devlogs_dir.glob("devlogs_*.json"):
                if file_path.stat().st_mtime < cutoff_date:
                    file_path.unlink()
                    deleted_count += 1

            return deleted_count

        except Exception as e:
            print(f"❌ Failed to cleanup old files: {e}")
            return 0

    def compress_file(self, file_path: Path) -> bool:
        """Compress devlog file"""
        try:
            compressed_path = file_path.with_suffix('.json.gz')
            
            with open(file_path, 'rb') as f_in:
                with gzip.open(compressed_path, 'wb') as f_out:
                    f_out.writelines(f_in)

            # Remove original file
            file_path.unlink()
            return True

        except Exception as e:
            print(f"❌ Failed to compress file: {e}")
            return False

    def get_file_info(self) -> Dict[str, Any]:
        """Get current file information"""
        try:
            if self.current_file.exists():
                stat = self.current_file.stat()
                return {
                    "file_path": str(self.current_file),
                    "file_size": stat.st_size,
                    "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "exists": True
                }
            else:
                return {
                    "file_path": str(self.current_file),
                    "file_size": 0,
                    "last_modified": None,
                    "exists": False
                }
        except Exception as e:
            return {
                "file_path": str(self.current_file),
                "error": str(e),
                "exists": False
            }