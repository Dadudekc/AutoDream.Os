"""
Captain's Tool: Quick ROI Calculator
=====================================

Quickly calculate ROI for a task to decide priority.

Usage: python tools/captain_roi_quick_calc.py --points 1000 --complexity 50 --autonomy 2

Author: Agent-4 (Captain)
Date: 2025-10-13
"""

import argparse


def calculate_task_roi(points: int, complexity: int, v2_impact: int = 0, autonomy_impact: int = 0):
    """
    Calculate ROI for a task.

    ROI = (Reward) / (Difficulty)

    Reward = points + (v2_impact * 100) + (autonomy_impact * 200)
    Difficulty = complexity

    Autonomy weighted 2x because long-term goal!
    """
    reward = points + (v2_impact * 100) + (autonomy_impact * 200)
    difficulty = max(complexity, 1)
    roi = reward / difficulty

    print(f"\n{'='*60}")
    print("ROI CALCULATION")
    print(f"{'='*60}")
    print("\n📊 INPUTS:")
    print(f"  Base Points: {points}")
    print(f"  Complexity: {complexity}")
    print(f"  V2 Impact: {v2_impact} violations fixed")
    print(f"  Autonomy Impact: {autonomy_impact}/3")

    print("\n💰 REWARD CALCULATION:")
    print(f"  Base: {points}")
    if v2_impact > 0:
        print(f"  + V2 bonus: {v2_impact * 100} ({v2_impact} × 100)")
    if autonomy_impact > 0:
        print(f"  + Autonomy bonus: {autonomy_impact * 200} ({autonomy_impact} × 200)")
    print(f"  = Total Reward: {reward}")

    print("\n📈 ROI:")
    print(f"  ROI = {reward} / {difficulty}")
    print(f"  ROI = {roi:.2f}")

    # Interpret
    print("\n🎯 INTERPRETATION:")
    if roi >= 30:
        print("  🏆 EXCELLENT! (ROI ≥30) - TOP PRIORITY!")
    elif roi >= 20:
        print("  ✅ VERY GOOD (ROI 20-30) - HIGH PRIORITY")
    elif roi >= 15:
        print("  👍 GOOD (ROI 15-20) - GOOD PRIORITY")
    elif roi >= 10:
        print("  📊 ACCEPTABLE (ROI 10-15) - MEDIUM PRIORITY")
    else:
        print("  ⚠️  LOW (ROI <10) - Consider if strategic value high")

    print(f"\n{'='*60}\n")

    return roi


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate task ROI")
    parser.add_argument("--points", "-p", type=int, required=True, help="Task points")
    parser.add_argument(
        "--complexity", "-c", type=int, required=True, help="Task complexity (1-100)"
    )
    parser.add_argument("--v2", type=int, default=0, help="V2 violations fixed (0-5)")
    parser.add_argument("--autonomy", "-a", type=int, default=0, help="Autonomy impact (0-3)")

    args = parser.parse_args()

    roi = calculate_task_roi(args.points, args.complexity, args.v2, args.autonomy)

    print(f"Final ROI: {roi:.2f}")
