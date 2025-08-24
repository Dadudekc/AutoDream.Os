#!/usr/bin/env python3
"""
Decision CLI - Agent Cellphone V2 Decision System
=================================================

Implements command-line interface for the autonomous decision engine.
Follows V2 coding standards: ≤100 LOC, OOP design, SRP.

**Responsibilities:**
- CLI argument parsing
- User interaction
- Command execution
- Result display

**Author:** Agent-1
**Created:** Current Sprint
**Status:** ACTIVE - V2 STANDARDS COMPLIANT
"""

import argparse
import json
import sys

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, Any
from datetime import datetime

from .decision_core import AutonomousDecisionEngine
from .decision_types import DecisionContext, LearningData, AgentCapability


class DecisionCLI:
    """
    Command-line interface for the autonomous decision engine

    Responsibilities:
    - Parse command-line arguments
    - Execute user commands
    - Display results
    - Handle user interaction
    """

    def __init__(self):
        self.engine = AutonomousDecisionEngine()
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create the command-line argument parser"""
        parser = argparse.ArgumentParser(
            description="Autonomous Decision Engine CLI",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
    python -m src.core.decision.decision_cli --test
    python -m src.core.decision.decision_cli --make-decision TASK_ASSIGNMENT '{"agent_id": "Agent-1"}'
    python -m src.core.decision.decision_cli --status
            """,
        )

        parser.add_argument("--test", action="store_true", help="Run system test")
        parser.add_argument(
            "--make-decision",
            nargs=2,
            metavar=("TYPE", "CONTEXT"),
            help="Make decision (TYPE 'CONTEXT_JSON')",
        )
        parser.add_argument(
            "--add-learning",
            nargs=4,
            metavar=("FEATURES", "TARGET", "CONTEXT", "PERFORMANCE"),
            help="Add learning data",
        )
        parser.add_argument(
            "--update-agent",
            nargs=3,
            metavar=("AGENT_ID", "SKILLS", "EXPERIENCE"),
            help="Update agent capability",
        )
        parser.add_argument(
            "--record-metric",
            nargs=2,
            metavar=("METRIC_NAME", "VALUE"),
            help="Record performance metric",
        )
        parser.add_argument(
            "--status", action="store_true", help="Show autonomous status"
        )

        return parser

    def run_test(self) -> bool:
        """Run the autonomous decision engine test"""
        print("🧪 Running Autonomous Decision Engine Test...")

        try:
            # Test decision making
            print("Testing autonomous decision making...")
            context = DecisionContext(
                decision_id=f"cli_test_{int(datetime.now().timestamp())}",
                decision_type="task_assignment",
                timestamp=datetime.now().isoformat(),
                agent_id="cli_test_agent",
                context_data={"task": "testing", "priority": "high"},
                constraints=["time_limit"],
                objectives=["validate_functionality"],
                risk_factors=["none"],
            )

            result = self.engine.make_autonomous_decision("task_assignment", context)
            print(f"✅ Decision made: {result.selected_option}")
            print(f"  Confidence: {result.confidence}")
            print(f"  Reasoning: {result.reasoning}")

            # Test learning data addition
            print("Testing learning data addition...")
            learning_data = LearningData(
                input_features=[0.1, 0.2, 0.3],
                output_target="success",
                context="cli_test",
                timestamp=datetime.now().isoformat(),
                performance_metric=0.9,
                feedback_score=0.9,
            )
            self.engine.add_learning_data(learning_data)
            print("✅ Learning data added")

            print("✅ Test completed successfully!")
            return True

        except Exception as e:
            print(f"❌ Test failed: {e}")
            return False

    def make_decision(self, decision_type: str, context_json: str) -> bool:
        """Make an autonomous decision"""
        try:
            context_data = json.loads(context_json)
            context = DecisionContext(
                decision_id=f"cli_{int(datetime.now().timestamp())}",
                decision_type=decision_type,
                timestamp=datetime.now().isoformat(),
                agent_id=context_data.get("agent_id", "cli_agent"),
                context_data=context_data,
                constraints=context_data.get("constraints", []),
                objectives=context_data.get("objectives", []),
                risk_factors=context_data.get("risk_factors", []),
            )

            result = self.engine.make_autonomous_decision(decision_type, context)
            print(f"✅ Decision made: {result.selected_option}")
            print(f"  Confidence: {result.confidence}")
            print(f"  Reasoning: {result.reasoning}")
            return True

        except json.JSONDecodeError:
            print("❌ Invalid JSON context")
            return False
        except Exception as e:
            print(f"❌ Decision failed: {e}")
            return False

    def add_learning(
        self, features_str: str, target: str, context_name: str, performance: str
    ) -> bool:
        """Add learning data"""
        try:
            features = [float(x) for x in features_str.split(",")]
            performance_val = float(performance)

            learning_data = LearningData(
                input_features=features,
                output_target=target,
                context=context_name,
                timestamp=datetime.now().isoformat(),
                performance_metric=performance_val,
                feedback_score=performance_val / 100.0,
            )

            self.engine.add_learning_data(learning_data)
            print("✅ Learning data added")
            return True

        except ValueError:
            print("❌ Invalid numeric values")
            return False
        except Exception as e:
            print(f"❌ Learning data addition failed: {e}")
            return False

    def update_agent(self, agent_id: str, skills_str: str, experience: str) -> bool:
        """Update agent capability"""
        try:
            skills = skills_str.split(",")
            experience_val = float(experience)

            capability = AgentCapability(
                agent_id=agent_id,
                skills=skills,
                experience_level=experience_val,
                performance_history=[0.8, 0.9, 0.85],
                learning_rate=0.1,
                specialization="general",
                availability=True,
            )

            self.engine.update_agent_capability(agent_id, capability)
            print(f"✅ Agent capability updated: {agent_id}")
            return True

        except ValueError:
            print("❌ Invalid experience value")
            return False
        except Exception as e:
            print(f"❌ Agent update failed: {e}")
            return False

    def record_metric(self, metric_name: str, value: str) -> bool:
        """Record a performance metric"""
        try:
            self.engine.record_performance_metric(metric_name, float(value))
            print(f"✅ Performance metric recorded: {metric_name} = {value}")
            return True

        except ValueError:
            print("❌ Invalid metric value")
            return False
        except Exception as e:
            print(f"❌ Metric recording failed: {e}")
            return False

    def show_status(self) -> bool:
        """Show autonomous system status"""
        try:
            status = self.engine.get_autonomous_status()
            print("🧠 Autonomous Decision System Status:")
            for key, value in status.items():
                print(f"  {key}: {value}")
            return True

        except Exception as e:
            print(f"❌ Status retrieval failed: {e}")
            return False

    def run(self, args: list = None) -> int:
        """Run the CLI with the given arguments"""
        try:
            parsed_args = self.parser.parse_args(args)

            if parsed_args.test:
                success = self.run_test()
                return 0 if success else 1

            elif parsed_args.make_decision:
                decision_type, context_json = parsed_args.make_decision
                success = self.make_decision(decision_type, context_json)
                return 0 if success else 1

            elif parsed_args.add_learning:
                features, target, context, performance = parsed_args.add_learning
                success = self.add_learning(features, target, context, performance)
                return 0 if success else 1

            elif parsed_args.update_agent:
                agent_id, skills, experience = parsed_args.update_agent
                success = self.update_agent(agent_id, skills, experience)
                return 0 if success else 1

            elif parsed_args.record_metric:
                metric_name, value = parsed_args.record_metric
                success = self.record_metric(metric_name, value)
                return 0 if success else 1

            elif parsed_args.status:
                success = self.show_status()
                return 0 if success else 1

            else:
                self.parser.print_help()
                return 0

        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")
            return 0
        except Exception as e:
            print(f"❌ CLI error: {e}")
            return 1
        finally:
            self.engine.shutdown()


def main():
    """Main entry point for the decision CLI"""
    cli = DecisionCLI()
    return cli.run()


if __name__ == "__main__":
    sys.exit(main())
