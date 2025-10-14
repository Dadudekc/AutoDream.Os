"""
Captain's Tool: Next Task Picker (Markov + ROI)
================================================

Uses Markov optimizer to pick the next optimal task for an agent.

Usage: python tools/captain_next_task_picker.py --agent Agent-1

Author: Agent-4 (Captain)
Date: 2025-10-13
"""

import argparse
import json


def calculate_roi(points: int, complexity: int, v2: int, autonomy: int):
    """Calculate ROI."""
    reward = points + (v2 * 100) + (autonomy * 200)
    return reward / max(complexity, 1)


def get_next_task_for_agent(agent_id: str, specialty_match_only: bool = False):
    """Get next optimal task for specific agent using ROI."""

    # Load violations from scanner
    with open("project_analysis.json") as f:
        data = json.load(f)

    # Find violations
    violations = []
    for filepath, info in data.items():
        if info.get("language") != ".py":
            continue

        functions = len(info.get("functions", []))
        classes = len(info.get("classes", {}))
        complexity = info.get("complexity", 0)

        if functions > 10 or classes > 5:
            # Estimate points
            points = 100
            if functions > 30:
                points += 300
            elif functions > 20:
                points += 200
            elif functions > 10:
                points += 100

            if classes > 10:
                points += 300
            elif classes > 5:
                points += 150

            # Estimate autonomy (simplified)
            autonomy = 0
            if "error" in filepath.lower() or "autonomous" in filepath.lower():
                autonomy = 2
            elif "config" in filepath.lower() or "manager" in filepath.lower():
                autonomy = 1

            # Calculate ROI
            roi = calculate_roi(points, complexity, 1, autonomy)

            violations.append(
                {
                    "file": filepath,
                    "functions": functions,
                    "classes": classes,
                    "complexity": complexity,
                    "points": points,
                    "autonomy": autonomy,
                    "roi": roi,
                }
            )

    # Sort by ROI
    violations.sort(key=lambda x: x["roi"], reverse=True)

    print(f"\n{'='*80}")
    print(f"🎯 NEXT TASK RECOMMENDATION FOR {agent_id}")
    print(f"{'='*80}\n")

    print("TOP 5 BY ROI:\n")
    for i, v in enumerate(violations[:5], 1):
        filename = v["file"].split("\\")[-1]
        print(f"{i}. {filename}")
        print(f"   ROI: {v['roi']:.2f} | Points: {v['points']} | Complexity: {v['complexity']}")
        print(f"   Violations: {v['functions']}f/{v['classes']}c | Autonomy: {v['autonomy']}/3")
        print()

    # Recommend top
    if violations:
        best = violations[0]
        print(f"🏆 RECOMMENDED: {best['file'].split(chr(92))[-1]}")
        print(f"   ROI: {best['roi']:.2f} (BEST!)")
        print(f"   Points: {best['points']}")
        print(f"   Complexity: {best['complexity']}")
        print(f"   Autonomy Impact: {best['autonomy']}/3")
        print()

        return best

    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find next optimal task for agent")
    parser.add_argument("--agent", "-a", required=True, help="Agent ID (e.g., Agent-1)")
    parser.add_argument(
        "--specialty-only", action="store_true", help="Only show tasks matching agent specialty"
    )

    args = parser.parse_args()

    get_next_task_for_agent(args.agent, args.specialty_only)
