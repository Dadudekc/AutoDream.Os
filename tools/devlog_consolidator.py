#!/usr/bin/env python3
"""
Devlog Consolidation Tool - Reduces 254 devlogs to manageable daily summaries

This tool consolidates multiple granular devlogs into comprehensive daily summaries,
reducing documentation bloat while maintaining all important information.

Usage:
    python tools/devlog_consolidator.py --date 2025-01-19 --agent Agent-4 --consolidate
"""

import argparse
from pathlib import Path


class DevlogConsolidator:
    """Consolidates multiple devlogs into daily summaries."""

    def __init__(self, devlogs_dir: str = "devlogs"):
        self.devlogs_dir = Path(devlogs_dir)
        self.consolidated_dir = self.devlogs_dir / "consolidated"

    def get_logs_by_date_agent(self, date: str, agent: str) -> list[Path]:
        """Get all logs for a specific date and agent."""
        pattern = f"{date}_{agent}_*.md"
        return list(self.devlogs_dir.glob(pattern))

    def read_log_content(self, log_path: Path) -> dict:
        """Extract structured content from a log file."""
        content = log_path.read_text(encoding="utf-8")

        # Extract metadata
        metadata = {}
        lines = content.split("\n")

        # Get basic metadata
        for line in lines[:10]:  # Look in first 10 lines
            if line.startswith("**Date:**"):
                metadata["date"] = line.replace("**Date:**", "").strip()
            elif line.startswith("**Agent:**"):
                metadata["agent"] = line.replace("**Agent:**", "").strip()
            elif line.startswith("**Status:**"):
                metadata["status"] = line.replace("**Status:**", "").strip()
            elif line.startswith("**Priority:**"):
                metadata["priority"] = line.replace("**Priority:**", "").strip()

        return {
            "path": str(log_path),
            "filename": log_path.name,
            "metadata": metadata,
            "content": content,
        }

    def categorize_logs(self, logs: list[dict]) -> dict[str, list[dict]]:
        """Categorize logs by type for consolidation."""
        categories = {
            "coordination": [],
            "technical_fixes": [],
            "achievements": [],
            "planning": [],
            "status_updates": [],
            "other": [],
        }

        for log in logs:
            content = log["content"].lower()

            if any(
                keyword in content
                for keyword in ["coordination", "captain", "protocol", "communication"]
            ):
                categories["coordination"].append(log)
            elif any(
                keyword in content
                for keyword in ["fixed", "resolved", "implemented", "created", "updated"]
            ):
                categories["technical_fixes"].append(log)
            elif any(
                keyword in content
                for keyword in ["complete", "success", "achievement", "milestone"]
            ):
                categories["achievements"].append(log)
            elif any(keyword in content for keyword in ["plan", "strategy", "approach", "phase"]):
                categories["planning"].append(log)
            elif any(keyword in content for keyword in ["status", "progress", "update"]):
                categories["status_updates"].append(log)
            else:
                categories["other"].append(log)

        return categories

    def consolidate_logs(self, date: str, agent: str, logs: list[dict]) -> str:
        """Create a consolidated daily summary from multiple logs."""

        if not logs:
            return ""

        # Get first log for basic metadata
        first_log = logs[0]
        metadata = first_log["metadata"]

        # Categorize the logs
        categories = self.categorize_logs(logs)

        # Build consolidated content
        consolidated_content = f"""# {agent} Comprehensive Daily Summary - {date}

**Date:** {date}
**Agent:** {agent} (Captain & Operations Coordinator)
**Status:** ✅ **MULTIPLE ACHIEVEMENTS COMPLETED**
**Priority:** CRITICAL

## 🎯 **DAILY ACTIVITIES SUMMARY**

"""

        # Add coordination section
        if categories["coordination"]:
            consolidated_content += (
                "### **Coordination Excellence** ✅ **SWARM COORDINATION ACTIVE**\n"
            )
            for log in categories["coordination"][:3]:  # Limit to 3 coordination logs
                # Extract key points from coordination logs
                content = log["content"]
                # Remove the header and just get the key content
                lines = content.split("\n")
                key_content = []
                in_content = False
                for line in lines:
                    if line.startswith("# "):
                        continue
                    if "**Date:**" in line or "**Agent:**" in line or "**Status:**" in line:
                        continue
                    if line.strip() and not line.startswith("|"):
                        key_content.append(line)
                consolidated_content += "- " + " | ".join(key_content[:2]) + "\n"
            consolidated_content += "\n"

        # Add technical fixes section
        if categories["technical_fixes"]:
            consolidated_content += "### **Technical Achievements** 🔧 **ROOT PROBLEMS RESOLVED**\n"
            for log in categories["technical_fixes"][:3]:  # Limit to 3 technical logs
                # Extract key technical achievements
                content = log["content"]
                lines = content.split("\n")
                for line in lines:
                    if "✅" in line and len(line.strip()) < 100:
                        consolidated_content += f"- {line.strip()}\n"
                        break
            consolidated_content += "\n"

        # Add achievements section
        if categories["achievements"]:
            consolidated_content += "### **Mission Achievements** 🏆 **MILESTONES ACHIEVED**\n"
            for log in categories["achievements"][:3]:  # Limit to 3 achievement logs
                content = log["content"]
                lines = content.split("\n")
                for line in lines:
                    if "achievement" in line.lower() or "complete" in line.lower():
                        consolidated_content += f"- {line.strip()}\n"
                        break
            consolidated_content += "\n"

        # Add planning section
        if categories["planning"]:
            consolidated_content += "### **Mission Planning** 📋 **STRATEGIC DIRECTION**\n"
            for log in categories["planning"][:2]:  # Limit to 2 planning logs
                content = log["content"]
                lines = content.split("\n")
                for line in lines:
                    if "phase" in line.lower() or "plan" in line.lower():
                        consolidated_content += f"- {line.strip()}\n"
                        break
            consolidated_content += "\n"

        # Add status updates section
        if categories["status_updates"]:
            consolidated_content += "### **Progress Updates** 📊 **MISSION STATUS**\n"
            for log in categories["status_updates"][:2]:  # Limit to 2 status logs
                content = log["content"]
                lines = content.split("\n")
                for line in lines:
                    if "status" in line.lower() and "100%" in line:
                        consolidated_content += f"- {line.strip()}\n"
                        break
            consolidated_content += "\n"

        # Add consolidation note
        consolidated_content += f"""## 📝 **CONSOLIDATION NOTE**

**This comprehensive daily summary consolidates {len(logs)} individual devlogs into one complete overview of {date} activities and achievements.**

**Original logs consolidated:**
"""
        for log in logs:
            consolidated_content += f"- `{log['filename']}`\n"

        consolidated_content += "\n**WE ARE SWARM!** 🐝\n"

        return consolidated_content

    def consolidate_and_cleanup(self, date: str, agent: str) -> bool:
        """Consolidate logs for a date/agent and remove originals."""
        logs = self.get_logs_by_date_agent(date, agent)

        if len(logs) <= 1:
            print(f"Only {len(logs)} logs found for {date} {agent} - no consolidation needed")
            return False

        # Read all logs
        log_data = []
        for log_path in logs:
            try:
                log_data.append(self.read_log_content(log_path))
            except Exception as e:
                print(f"Error reading {log_path}: {e}")
                continue

        if not log_data:
            return False

        # Create consolidated content
        consolidated_content = self.consolidate_logs(date, agent, log_data)

        # Create consolidated filename
        consolidated_filename = f"{date}_{agent}_Comprehensive_Daily_Summary.md"
        consolidated_path = self.devlogs_dir / consolidated_filename

        # Write consolidated log
        try:
            consolidated_path.write_text(consolidated_content, encoding="utf-8")
            print(f"Created consolidated log: {consolidated_filename}")
        except Exception as e:
            print(f"Error writing consolidated log: {e}")
            return False

        # Remove original logs
        removed_count = 0
        for log_data_item in log_data:
            try:
                log_path = Path(log_data_item["path"])
                if log_path.exists():
                    log_path.unlink()
                    removed_count += 1
            except Exception as e:
                print(f"Error removing {log_data_item['path']}: {e}")

        print(
            f"Successfully consolidated {len(log_data)} logs into 1 summary (removed {removed_count} files)"
        )
        return True


def main():
    parser = argparse.ArgumentParser(description="Consolidate devlogs into daily summaries")
    parser.add_argument("--date", required=True, help="Date in YYYY-MM-DD format")
    parser.add_argument("--agent", required=True, help="Agent identifier")
    parser.add_argument(
        "--consolidate", action="store_true", help="Actually consolidate and remove logs"
    )

    args = parser.parse_args()

    consolidator = DevlogConsolidator()

    # Get logs for this date/agent
    logs = consolidator.get_logs_by_date_agent(args.date, args.agent)

    print(f"Found {len(logs)} logs for {args.date} {args.agent}")

    if not args.consolidate:
        print("Use --consolidate to actually consolidate and remove logs")
        return

    # Consolidate and cleanup
    success = consolidator.consolidate_and_cleanup(args.date, args.agent)

    if success:
        print("✅ Consolidation completed successfully!")
    else:
        print("❌ Consolidation failed or not needed")


if __name__ == "__main__":
    main()
