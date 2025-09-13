#!/usr/bin/env python3
"""
Consolidated Utility Manager
============================

Unified utility system for file management, cleanup, and system operations.
Consolidates functionality from multiple utility-related scripts.

Author: Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

import argparse
import json
import logging
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class FileInfo:
    """Information about a file."""

    path: str
    size: int
    lines: int
    modified: float
    type: str


class UtilityManager:
    """Unified utility manager for system operations."""

    def __init__(self):
        """Initialize the utility manager."""
        self.project_root = Path(".")
        self.large_file_threshold = 400  # V2 compliance limit

    def find_large_files(self, threshold: int = None) -> List[FileInfo]:
        """Find files exceeding size threshold."""
        if threshold is None:
            threshold = self.large_file_threshold

        large_files = []

        for file_path in self.project_root.rglob("*.py"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                line_count = len(lines)
                if line_count > threshold:
                    stat = file_path.stat()
                    large_files.append(FileInfo(
                        path=str(file_path),
                        size=stat.st_size,
                        lines=line_count,
                        modified=stat.st_mtime,
                        type="python"
                    ))
            except Exception as e:
                logger.warning(f"Could not analyze {file_path}: {e}")

        return sorted(large_files, key=lambda x: x.lines, reverse=True)

    def cleanup_v2_compliance(self, dry_run: bool = True) -> Dict[str, Any]:
        """Clean up V2 compliance violations."""
        results = {
            "files_checked": 0,
            "violations_found": 0,
            "files_to_refactor": [],
            "recommendations": []
        }

        large_files = self.find_large_files()
        results["files_checked"] = len(large_files)
        results["violations_found"] = len(large_files)

        for file_info in large_files:
            results["files_to_refactor"].append({
                "path": file_info.path,
                "lines": file_info.lines,
                "violation": "FILE_TOO_LONG"
            })

            if file_info.lines > 600:
                results["recommendations"].append(f"URGENT: {file_info.path} ({file_info.lines} lines) - immediate refactor required")
            elif file_info.lines > 400:
                results["recommendations"].append(f"HIGH: {file_info.path} ({file_info.lines} lines) - major violation, refactor needed")

        return results

    def setup_discord_bot(self, token: str = None, channel_id: str = None) -> bool:
        """Setup Discord bot configuration."""
        try:
            config_dir = Path("config")
            config_dir.mkdir(exist_ok=True)

            config = {
                "discord": {
                    "token": token or os.getenv("DISCORD_TOKEN", ""),
                    "channel_id": channel_id or os.getenv("DISCORD_CHANNEL_ID", ""),
                    "enabled": True
                }
            }

            config_file = config_dir / "discord.json"
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)

            logger.info(f"Discord configuration saved to {config_file}")
            return True

        except Exception as e:
            logger.error(f"Failed to setup Discord bot: {e}")
            return False

    def run_duplication_scan(self) -> Dict[str, Any]:
        """Run duplication scan to find duplicate code."""
        results = {
            "duplicates_found": 0,
            "duplicate_groups": [],
            "recommendations": []
        }

        # Simple duplication detection based on file content similarity
        python_files = list(self.project_root.rglob("*.py"))
        file_contents = {}

        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                file_contents[str(file_path)] = content
            except Exception as e:
                logger.warning(f"Could not read {file_path}: {e}")

        # Find similar files (simplified approach)
        similar_groups = []
        processed = set()

        for file1, content1 in file_contents.items():
            if file1 in processed:
                continue

            similar_files = [file1]
            for file2, content2 in file_contents.items():
                if file1 != file2 and file2 not in processed:
                    # Simple similarity check (could be improved)
                    if len(content1) > 100 and len(content2) > 100:
                        similarity = len(set(content1.split()) & set(content2.split())) / max(len(content1.split()), len(content2.split()))
                        if similarity > 0.7:  # 70% similarity threshold
                            similar_files.append(file2)
                            processed.add(file2)

            if len(similar_files) > 1:
                similar_groups.append(similar_files)
                processed.add(file1)

        results["duplicate_groups"] = similar_groups
        results["duplicates_found"] = len(similar_groups)

        for group in similar_groups:
            results["recommendations"].append(f"Consider consolidating: {', '.join(group)}")

        return results

    def validate_workspace_coords(self) -> Dict[str, Any]:
        """Validate workspace coordinates for swarm agents."""
        results = {
            "valid": True,
            "agents_found": 0,
            "missing_coords": [],
            "invalid_coords": []
        }

        # Check for coordinate files
        coord_files = [
            "agent_coordinates.json",
            "src/core/agent_coordinates.json",
            "config/agent_coordinates.json"
        ]

        coords_found = False
        for coord_file in coord_files:
            if Path(coord_file).exists():
                coords_found = True
                try:
                    with open(coord_file, 'r') as f:
                        coords = json.load(f)

                    for agent_id, coord_data in coords.items():
                        results["agents_found"] += 1

                        if "onboarding" not in coord_data or "chat" not in coord_data:
                            results["missing_coords"].append(agent_id)
                            results["valid"] = False

                        # Validate coordinate format
                        for coord_type, coords in coord_data.items():
                            if isinstance(coords, dict) and "x" in coords and "y" in coords:
                                if not (isinstance(coords["x"], (int, float)) and isinstance(coords["y"], (int, float))):
                                    results["invalid_coords"].append(f"{agent_id}.{coord_type}")
                                    results["valid"] = False

                except Exception as e:
                    logger.error(f"Failed to parse {coord_file}: {e}")
                    results["valid"] = False

        if not coords_found:
            results["valid"] = False
            results["missing_coords"].append("No coordinate files found")

        return results

    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status."""
        status = {
            "v2_compliance": {},
            "duplication": {},
            "coordinates": {},
            "discord": {},
            "overall_health": "unknown"
        }

        # Check V2 compliance
        v2_results = self.cleanup_v2_compliance()
        status["v2_compliance"] = {
            "violations": v2_results["violations_found"],
            "files_checked": v2_results["files_checked"],
            "healthy": v2_results["violations_found"] == 0
        }

        # Check duplication
        dup_results = self.run_duplication_scan()
        status["duplication"] = {
            "duplicates": dup_results["duplicates_found"],
            "healthy": dup_results["duplicates_found"] == 0
        }

        # Check coordinates
        coord_results = self.validate_workspace_coords()
        status["coordinates"] = {
            "valid": coord_results["valid"],
            "agents": coord_results["agents_found"],
            "healthy": coord_results["valid"]
        }

        # Check Discord
        discord_config = Path("config/discord.json")
        status["discord"] = {
            "configured": discord_config.exists(),
            "healthy": discord_config.exists()
        }

        # Overall health
        all_healthy = all([
            status["v2_compliance"]["healthy"],
            status["duplication"]["healthy"],
            status["coordinates"]["healthy"],
            status["discord"]["healthy"]
        ])

        status["overall_health"] = "healthy" if all_healthy else "issues_found"

        return status


def main():
    """Main entry point for the utility manager."""
    parser = argparse.ArgumentParser(description="Consolidated Utility Manager")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Find large files command
    large_parser = subparsers.add_parser("large-files", help="Find large files")
    large_parser.add_argument("--threshold", type=int, default=400, help="Line count threshold")

    # V2 compliance command
    v2_parser = subparsers.add_parser("v2-compliance", help="Check V2 compliance")
    v2_parser.add_argument("--dry-run", action="store_true", default=True, help="Dry run mode")

    # Setup Discord command
    discord_parser = subparsers.add_parser("setup-discord", help="Setup Discord bot")
    discord_parser.add_argument("--token", help="Discord bot token")
    discord_parser.add_argument("--channel-id", help="Discord channel ID")

    # Duplication scan command
    dup_parser = subparsers.add_parser("dup-scan", help="Run duplication scan")

    # Validate coordinates command
    coords_parser = subparsers.add_parser("validate-coords", help="Validate workspace coordinates")

    # Status command
    status_parser = subparsers.add_parser("status", help="Get system status")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    manager = UtilityManager()

    try:
        if args.command == "large-files":
            large_files = manager.find_large_files(args.threshold)
            print(f"Found {len(large_files)} files exceeding {args.threshold} lines:")
            for file_info in large_files:
                print(f"  {file_info.path}: {file_info.lines} lines")

        elif args.command == "v2-compliance":
            results = manager.cleanup_v2_compliance(args.dry_run)
            print(f"V2 Compliance Check:")
            print(f"  Files checked: {results['files_checked']}")
            print(f"  Violations found: {results['violations_found']}")

            if results["recommendations"]:
                print("\nRecommendations:")
                for rec in results["recommendations"]:
                    print(f"  - {rec}")

        elif args.command == "setup-discord":
            if manager.setup_discord_bot(args.token, args.channel_id):
                print("✅ Discord bot setup completed")
            else:
                print("❌ Discord bot setup failed")
                return 1

        elif args.command == "dup-scan":
            results = manager.run_duplication_scan()
            print(f"Duplication Scan Results:")
            print(f"  Duplicate groups found: {results['duplicates_found']}")

            if results["recommendations"]:
                print("\nRecommendations:")
                for rec in results["recommendations"]:
                    print(f"  - {rec}")

        elif args.command == "validate-coords":
            results = manager.validate_workspace_coords()
            status = "✅ Valid" if results["valid"] else "❌ Invalid"
            print(f"Workspace Coordinates: {status}")
            print(f"  Agents found: {results['agents_found']}")

            if results["missing_coords"]:
                print(f"  Missing coordinates: {results['missing_coords']}")
            if results["invalid_coords"]:
                print(f"  Invalid coordinates: {results['invalid_coords']}")

        elif args.command == "status":
            status = manager.get_system_status()
            print("System Status:")
            print(f"  Overall Health: {status['overall_health'].upper()}")
            print(f"  V2 Compliance: {'✅' if status['v2_compliance']['healthy'] else '❌'} ({status['v2_compliance']['violations']} violations)")
            print(f"  Duplication: {'✅' if status['duplication']['healthy'] else '❌'} ({status['duplication']['duplicates']} duplicates)")
            print(f"  Coordinates: {'✅' if status['coordinates']['healthy'] else '❌'} ({status['coordinates']['agents']} agents)")
            print(f"  Discord: {'✅' if status['discord']['healthy'] else '❌'}")

        return 0

    except Exception as e:
        logger.error(f"Command failed: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())
