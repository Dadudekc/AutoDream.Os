
import time
import json
from pathlib import Path
from datetime import datetime

print("Agent DevLog Watcher Started")
print("Monitoring for new agent activity...")

last_check = {}
while True:
    agents_dir = Path("agent_workspaces")

    for agent_dir in agents_dir.glob("Agent-*"):
        agent_id = agent_dir.name

        # Check inbox for new messages
        inbox_dir = agent_dir / "inbox"
        if inbox_dir.exists():
            current_files = list(inbox_dir.glob("*.md"))
            previous_count = last_check.get(agent_id, 0)

            if len(current_files) > previous_count:
                print(f"[NEW] {agent_id}: {len(current_files) - previous_count} new messages!")
                last_check[agent_id] = len(current_files)

        # Check for new reports
        reports = list(agent_dir.glob("*.md"))
        if reports:
            latest_report = max(reports, key=lambda x: x.stat().st_mtime)
            print(f"[REPORT] {agent_id}: Latest activity - {latest_report.name}")

    time.sleep(60)  # Check every minute
