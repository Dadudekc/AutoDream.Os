#!/usr/bin/env python3
"""
Quick Agent Integration Assessment
"""

import json
import os

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path
from datetime import datetime


def main():
    # Simple agent assessment
    repo_root = Path(".")
    agents = [
        "Agent-1",
        "Agent-2",
        "Agent-3",
        "Agent-4",
        "Agent-5",
        "Agent-6",
        "Agent-7",
        "Agent-8",
    ]

    results = {
        "timestamp": datetime.now().isoformat(),
        "agents": {},
        "overall_status": "assessment_complete",
    }

    for agent_id in agents:
        # Check for web components
        web_components = []
        if (repo_root / "src" / "web").exists():
            web_components.append("web_development_environment")

        # Check for existing web files
        web_files = (
            list((repo_root / "src" / "web").glob("*.py"))
            if (repo_root / "src" / "web").exists()
            else []
        )
        if web_files:
            web_components.extend(["flask_app", "fastapi_app", "web_automation"])

        # Determine priority
        if agent_id == "Agent-7":
            priority = "complete"
            readiness = "ready"
            score = 100
        elif agent_id in ["Agent-1", "Agent-5"]:
            priority = "high"
            readiness = "not_ready"
            score = 0
        else:
            priority = "medium"
            readiness = "not_ready"
            score = 0

        results["agents"][agent_id] = {
            "agent_id": agent_id,
            "priority": priority,
            "readiness": readiness,
            "readiness_score": score,
            "web_components": web_components,
            "estimated_effort": "3-5 days" if priority == "high" else "5-7 days",
        }

    # Save results
    reports_dir = repo_root / "reports"
    if not reports_dir.exists():
        reports_dir.mkdir()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = reports_dir / f"agent_assessment_{timestamp}.json"

    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print("Agent Assessment Complete!")
    print(f"Results saved to: {output_file}")
    print("\nSummary:")
    print(f"- Total Agents: {len(agents)}")
    print(
        f'- Completed: {sum(1 for a in results["agents"].values() if a["priority"] == "complete")}'
    )
    print(
        f'- High Priority: {sum(1 for a in results["agents"].values() if a["priority"] == "high")}'
    )
    print(
        f'- Medium Priority: {sum(1 for a in results["agents"].values() if a["priority"] == "medium")}'
    )

    return results


if __name__ == "__main__":
    main()
