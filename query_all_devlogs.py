#!/usr/bin/env python3
"""
Query All Devlogs
================

This script queries and displays all devlogs currently in the system.
"""

from datetime import datetime

import requests


def query_all_devlogs():
    """Query and display all devlogs in the system."""
    print("🤖 Querying all devlogs...")

    try:
        # Get all devlogs
        response = requests.get("http://localhost:8002/api/devlogs")
        data = response.json()

        if data["success"]:
            devlogs = data["data"]
            print(f"📊 Found {len(devlogs)} devlogs in the system")
            print("=" * 60)

            for i, devlog in enumerate(devlogs, 1):
                metadata = devlog.get("metadata", {})
                print(f'{i}. Agent: {metadata.get("agent_id", "Unknown")}')
                print(f'   Action: {metadata.get("action", "Unknown")}')
                print(f'   Status: {metadata.get("status", "Unknown")}')
                print(f'   Timestamp: {metadata.get("timestamp", "Unknown")}')
                details = metadata.get("details", "Unknown")
                if len(details) > 100:
                    details = details[:100] + "..."
                print(f"   Details: {details}")
                print()

            return devlogs
        else:
            print(f'❌ Error: {data.get("error", "Unknown error")}')
            return []

    except Exception as e:
        print(f"❌ Error querying devlogs: {e}")
        return []


def export_all_devlogs():
    """Export all devlogs to JSON file."""
    print("📤 Exporting all devlogs to JSON...")

    try:
        # Export as JSON
        response = requests.get("http://localhost:8002/api/devlogs/export/json")

        if response.status_code == 200:
            # Save to file
            filename = f"all_devlogs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, "w") as f:
                f.write(response.text)

            print(f"✅ Devlogs exported to: {filename}")
            print(f"📊 File size: {len(response.text)} characters")
            return filename
        else:
            print(f"❌ Export failed with status: {response.status_code}")
            return None

    except Exception as e:
        print(f"❌ Error exporting devlogs: {e}")
        return None


if __name__ == "__main__":
    # Query all devlogs
    devlogs = query_all_devlogs()

    if devlogs:
        print("💾 Export Options:")
        print("1. Export to JSON file")
        print("2. View analytics summary")

        choice = input("\nChoose an option (1-2): ").strip()

        if choice == "1":
            export_all_devlogs()
        elif choice == "2":
            # Get analytics
            try:
                analytics_response = requests.get("http://localhost:8002/api/devlogs/analytics")
                analytics_data = analytics_response.json()
                if analytics_data["success"]:
                    summary = analytics_data["data"]["summary"]
                    print("📈 Analytics Summary:")
                    print(f"  Total Devlogs: {summary['total_devlogs']}")
                    print(f"  Unique Agents: {summary['unique_agents']}")
                    print(f"  Status Distribution: {summary['status_distribution']}")
                else:
                    print(f"❌ Analytics error: {analytics_data.get('error', 'Unknown error')}")
            except Exception as e:
                print(f"❌ Error getting analytics: {e}")
    else:
        print("❌ No devlogs found to process")
