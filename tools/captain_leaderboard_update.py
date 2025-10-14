"""
Captain's Tool: Quick Leaderboard Update
=========================================

Updates leaderboard with new points.

Usage: python tools/captain_leaderboard_update.py --agent Agent-1 --points 2000 --task "shared_utilities"

Author: Agent-4 (Captain)
Date: 2025-10-13
"""

import json
from datetime import datetime
from pathlib import Path


def update_leaderboard(agent_id: str, points: int, task: str = ""):
    """Update leaderboard with new completion."""

    leaderboard_file = Path("runtime/leaderboard.json")

    # Load existing
    if leaderboard_file.exists():
        with open(leaderboard_file) as f:
            leaderboard = json.load(f)
    else:
        leaderboard = {}

    # Update agent
    if agent_id not in leaderboard:
        leaderboard[agent_id] = {"total_points": 0, "tasks_completed": 0, "completions": []}

    leaderboard[agent_id]["total_points"] += points
    leaderboard[agent_id]["tasks_completed"] += 1
    leaderboard[agent_id]["completions"].append(
        {"task": task, "points": points, "timestamp": datetime.now().isoformat()}
    )

    # Save
    leaderboard_file.parent.mkdir(parents=True, exist_ok=True)
    with open(leaderboard_file, "w") as f:
        json.dump(leaderboard, f, indent=2)

    # Display
    print(f"\n{'='*80}")
    print("🏆 LEADERBOARD UPDATED")
    print(f"{'='*80}\n")

    print(f"✅ {agent_id}: +{points} points ({task})")
    print(f"   New Total: {leaderboard[agent_id]['total_points']} points")
    print(f"   Tasks Completed: {leaderboard[agent_id]['tasks_completed']}\n")

    # Show rankings
    sorted_agents = sorted(leaderboard.items(), key=lambda x: x[1]["total_points"], reverse=True)

    print("📊 CURRENT STANDINGS:\n")
    medals = ["🥇", "🥈", "🥉"]
    for i, (agent, data) in enumerate(sorted_agents[:5], 1):
        medal = medals[i - 1] if i <= 3 else f"{i}️⃣"
        print(f"{medal} {agent}: {data['total_points']} points ({data['tasks_completed']} tasks)")

    print(f"\n{'='*80}\n")

    return leaderboard


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Update leaderboard")
    parser.add_argument("--agent", "-a", required=True, help="Agent ID")
    parser.add_argument("--points", "-p", type=int, required=True, help="Points earned")
    parser.add_argument("--task", "-t", default="", help="Task name")

    args = parser.parse_args()

    update_leaderboard(args.agent, args.points, args.task)
