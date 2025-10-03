"""
Workflow Bottleneck Eliminator - V2 Compliant
=============================================

Main interface for workflow bottleneck elimination.
V2 Compliance: ≤400 lines, single responsibility, KISS principle
"""

import argparse

from .workflow_bottleneck_core import WorkflowBottleneckCore
from .workflow_bottleneck_models import BottleneckElimination, BottleneckSummary


class WorkflowBottleneckEliminator:
    """Main workflow bottleneck eliminator interface."""

    def __init__(self):
        """Initialize bottleneck eliminator."""
        self.core = WorkflowBottleneckCore()

    def eliminate_all_bottlenecks(self) -> list[BottleneckElimination]:
        """Eliminate all identified bottlenecks."""
        return self.core.eliminate_all_bottlenecks()

    def get_elimination_summary(self) -> BottleneckSummary:
        """Get bottleneck elimination summary."""
        return self.core.get_elimination_summary()

    def eliminate_manual_inbox_scanning(self) -> BottleneckElimination:
        """Eliminate manual inbox scanning bottleneck."""
        return self.core.eliminate_manual_inbox_scanning()

    def eliminate_manual_task_evaluation(self) -> BottleneckElimination:
        """Eliminate manual task evaluation bottleneck."""
        return self.core.eliminate_manual_task_evaluation()

    def eliminate_manual_devlog_creation(self) -> BottleneckElimination:
        """Eliminate manual devlog creation bottleneck."""
        return self.core.eliminate_manual_devlog_creation()

    def eliminate_manual_compliance_checking(self) -> BottleneckElimination:
        """Eliminate manual compliance checking bottleneck."""
        return self.core.eliminate_manual_compliance_checking()

    def eliminate_manual_database_querying(self) -> BottleneckElimination:
        """Eliminate manual database querying bottleneck."""
        return self.core.eliminate_manual_database_querying()


def main():
    """CLI entry point for workflow bottleneck elimination."""
    parser = argparse.ArgumentParser(description="Workflow Bottleneck Eliminator")
    parser.add_argument("--eliminate-all", action="store_true", help="Eliminate all bottlenecks")
    parser.add_argument("--summary", action="store_true", help="Show elimination summary")
    parser.add_argument("--inbox", action="store_true", help="Eliminate inbox scanning bottleneck")
    parser.add_argument("--tasks", action="store_true", help="Eliminate task evaluation bottleneck")
    parser.add_argument(
        "--devlog", action="store_true", help="Eliminate devlog creation bottleneck"
    )
    parser.add_argument(
        "--compliance", action="store_true", help="Eliminate compliance checking bottleneck"
    )
    parser.add_argument(
        "--database", action="store_true", help="Eliminate database querying bottleneck"
    )

    args = parser.parse_args()

    eliminator = WorkflowBottleneckEliminator()

    if args.eliminate_all:
        eliminations = eliminator.eliminate_all_bottlenecks()
        print("Workflow Bottleneck Elimination Results:")
        for elimination in eliminations:
            print(f"  {elimination.bottleneck_type.value}: ELIMINATED")
            print(f"    Time Saved: {elimination.time_saved_per_cycle:.1f} seconds per cycle")
            print(f"    Steps Removed: {elimination.manual_steps_removed}")
            print(f"    Automation: {elimination.automation_created}")

    elif args.summary:
        eliminator.eliminate_all_bottlenecks()
        summary = eliminator.get_elimination_summary()
        print("Workflow Bottleneck Elimination Summary:")
        print(f"  Bottlenecks Eliminated: {summary.total_bottlenecks_eliminated}")
        print(f"  Total Time Saved: {summary.total_time_saved:.1f} seconds per cycle")
        print(f"  Manual Steps Removed: {summary.total_manual_steps_removed}")
        print(f"  Efficiency Gain: {summary.efficiency_gain_percentage:.1f}%")
        print(f"  Automation Scripts Created: {len(summary.automation_scripts_created)}")

    elif args.inbox:
        elimination = eliminator.eliminate_manual_inbox_scanning()
        print(
            f"Inbox scanning bottleneck eliminated: {elimination.time_saved_per_cycle:.1f}s saved"
        )

    elif args.tasks:
        elimination = eliminator.eliminate_manual_task_evaluation()
        print(
            f"Task evaluation bottleneck eliminated: {elimination.time_saved_per_cycle:.1f}s saved"
        )

    elif args.devlog:
        elimination = eliminator.eliminate_manual_devlog_creation()
        print(
            f"Devlog creation bottleneck eliminated: {elimination.time_saved_per_cycle:.1f}s saved"
        )

    elif args.compliance:
        elimination = eliminator.eliminate_manual_compliance_checking()
        print(
            f"Compliance checking bottleneck eliminated: {elimination.time_saved_per_cycle:.1f}s saved"
        )

    elif args.database:
        elimination = eliminator.eliminate_manual_database_querying()
        print(
            f"Database querying bottleneck eliminated: {elimination.time_saved_per_cycle:.1f}s saved"
        )

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
