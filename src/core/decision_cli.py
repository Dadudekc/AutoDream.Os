#!/usr/bin/env python3
"""Decision CLI - Agent Cellphone V2 - ≤100 LOC V2 compliant"""

import argparse
import json
import time

from src.utils.stability_improvements import stability_manager, safe_import
from datetime import datetime

from .decision_types import (
    DecisionType, create_decision_context, create_learning_data, create_agent_capability
)
from .decision_core import DecisionCore
from .learning_engine import LearningEngine
from .persistent_data_storage import PersistentDataStorage


class DecisionCLI:
    def __init__(self):
        self.storage = PersistentDataStorage()
        self.decision_core = DecisionCore(self.storage)
        self.learning_engine = LearningEngine(self.storage)
        self.parser = self._setup_argument_parser()
    
    def _setup_argument_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(description="Autonomous Decision Engine CLI")
        parser.add_argument("--test", action="store_true", help="Run system test")
        parser.add_argument("--make-decision", nargs=2, metavar=("TYPE", "CONTEXT"), help="Make decision")
        parser.add_argument("--add-learning", nargs=4, metavar=("FEATURES", "TARGET", "CONTEXT", "PERFORMANCE"), help="Add learning data")
        parser.add_argument("--update-agent", nargs=3, metavar=("AGENT_ID", "SKILLS", "EXPERIENCE"), help="Update agent capability")
        parser.add_argument("--record-metric", nargs=2, metavar=("METRIC_NAME", "VALUE"), help="Record performance metric")
        parser.add_argument("--status", action="store_true", help="Show system status")
        return parser
    
    def run_test(self):
        print("🧪 Running Autonomous Decision Engine Test...")
        try:
            context = create_decision_context("task_assignment", "test_agent", {"task_requirements": ["python", "ai"]})
            result = self.decision_core.make_autonomous_decision(DecisionType.TASK_ASSIGNMENT.value, context)
            print(f"✅ Decision made: {result.selected_option}")
            self.learning_engine.add_learning_data(create_learning_data([0.8, 0.6, 0.9], "success", "task_assignment", 0.85, 0.9))
            print("✅ Learning data added")
            capability = create_agent_capability("test_agent", ["python", "ai"], 0.8, 0.1, "ai_specialist")
            self.decision_core.update_agent_capability("test_agent", capability); self.learning_engine.update_agent_capability("test_agent", capability)
            print("✅ Agent capability updated")
            self.learning_engine.record_performance_metric("test_accuracy", 0.92)
            print("✅ Performance metric recorded"); print("✅ Test completed successfully!")
            return True
        except Exception as e:
            print(f"❌ Test failed: {e}"); return False
    
    def make_decision(self, decision_type: str, context_json: str):
        try:
            context_data = json.loads(context_json)
            context = create_decision_context(decision_type, context_data.get("agent_id", "cli_agent"), context_data)
            result = self.decision_core.make_autonomous_decision(decision_type, context)
            print(f"✅ Decision made: {result.selected_option} (confidence: {result.confidence})")
            self.learning_engine.add_decision_pattern(decision_type, result.decision_id)
        except json.JSONDecodeError: print("❌ Invalid JSON context")
        except Exception as e: print(f"❌ Decision failed: {e}")
    
    def add_learning_data(self, features_str: str, target: str, context_name: str, performance: str):
        try:
            features = [float(x) for x in features_str.split(",")]; performance_val = float(performance)
            self.learning_engine.add_learning_data(create_learning_data(features, target, context_name, performance_val, performance_val / 100.0))
            print(f"✅ Learning data added: {len(features)} features, target: {target}")
        except Exception as e: print(f"❌ Failed to add learning data: {e}")
    
    def update_agent(self, agent_id: str, skills_str: str, experience: str):
        try:
            skills = skills_str.split(","); experience_val = float(experience)
            capability = create_agent_capability(agent_id, skills, experience_val, 0.1, "general")
            self.decision_core.update_agent_capability(agent_id, capability); self.learning_engine.update_agent_capability(agent_id, capability)
            print(f"✅ Agent capability updated: {agent_id} with {len(skills)} skills")
        except Exception as e: print(f"❌ Failed to update agent: {e}")
    
    def record_metric(self, metric_name: str, value: str):
        try:
            self.learning_engine.record_performance_metric(metric_name, float(value))
            print(f"✅ Performance metric recorded: {metric_name} = {value}")
        except Exception as e: print(f"❌ Failed to record metric: {e}")
    
    def show_status(self):
        print("🧠 Autonomous Decision System Status:")
        decision_status = self.decision_core.get_decision_status(); learning_status = self.learning_engine.get_learning_status()
        print(f"📊 Decision Core: {decision_status['total_decisions']} decisions, {decision_status['total_agents']} agents")
        print(f"🧠 Learning Engine: {learning_status['total_learning_data']} learning data, intelligence: {learning_status['intelligence_level']}")
    
    def run(self, args=None):
        if args is None: args = self.parser.parse_args()
        try:
            if args.test: self.run_test()
            elif args.make_decision: self.make_decision(*args.make_decision)
            elif args.add_learning: self.add_learning_data(*args.add_learning)
            elif args.update_agent: self.update_agent(*args.update_agent)
            elif args.record_metric: self.record_metric(*args.record_metric)
            elif args.status: self.show_status()
            else: self.parser.print_help()
        except KeyboardInterrupt: print("\n🛑 Shutting down...")
        except Exception as e: print(f"❌ CLI error: {e}")
        finally: self.decision_core.shutdown(); self.learning_engine.shutdown()


def main():
    cli = DecisionCLI(); cli.run()


if __name__ == "__main__": main()
