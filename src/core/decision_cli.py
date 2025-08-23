#!/usr/bin/env python3
"""
Decision CLI - Agent Cellphone V2
=================================

CLI interface for autonomous decision engine testing.
Follows V2 standards: ≤100 LOC, single responsibility, clean CLI design.
"""

import argparse
import json
import time
from datetime import datetime

from .decision_types import (
    DecisionType, create_decision_context, create_learning_data, create_agent_capability
)
from .decision_core import DecisionCore
from .learning_engine import LearningEngine
from .persistent_data_storage import PersistentDataStorage


class DecisionCLI:
    """CLI interface for autonomous decision engine"""
    
    def __init__(self):
        """Initialize the CLI interface"""
        self.storage = PersistentDataStorage()
        self.decision_core = DecisionCore(self.storage)
        self.learning_engine = LearningEngine(self.storage)
        
        # Setup argument parser
        self.parser = self._setup_argument_parser()
    
    def _setup_argument_parser(self) -> argparse.ArgumentParser:
        """Setup the argument parser with all commands"""
        parser = argparse.ArgumentParser(description="Autonomous Decision Engine CLI")
        parser.add_argument("--test", action="store_true", help="Run system test")
        parser.add_argument("--make-decision", nargs=2, metavar=("TYPE", "CONTEXT"), help="Make decision")
        parser.add_argument("--add-learning", nargs=4, metavar=("FEATURES", "TARGET", "CONTEXT", "PERFORMANCE"), help="Add learning data")
        parser.add_argument("--update-agent", nargs=3, metavar=("AGENT_ID", "SKILLS", "EXPERIENCE"), help="Update agent capability")
        parser.add_argument("--record-metric", nargs=2, metavar=("METRIC_NAME", "VALUE"), help="Record performance metric")
        parser.add_argument("--status", action="store_true", help="Show system status")
        return parser
    
    def run_test(self):
        """Run comprehensive system test"""
        print("🧪 Running Autonomous Decision Engine Test...")
        
        try:
            context = create_decision_context("task_assignment", "test_agent", {"task_requirements": ["python", "ai"]})
            result = self.decision_core.make_autonomous_decision(DecisionType.TASK_ASSIGNMENT.value, context)
            print(f"✅ Decision made: {result.selected_option}")
            
            learning_data = create_learning_data([0.8, 0.6, 0.9], "success", "task_assignment", 0.85, 0.9)
            self.learning_engine.add_learning_data(learning_data)
            print("✅ Learning data added")
            
            capability = create_agent_capability("test_agent", ["python", "ai"], 0.8, 0.1, "ai_specialist")
            self.decision_core.update_agent_capability("test_agent", capability)
            self.learning_engine.update_agent_capability("test_agent", capability)
            print("✅ Agent capability updated")
            
            self.learning_engine.record_performance_metric("test_accuracy", 0.92)
            print("✅ Performance metric recorded")
            
            print("✅ Test completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
            return False
    
    def make_decision(self, decision_type: str, context_json: str):
        """Make an autonomous decision"""
        try:
            context_data = json.loads(context_json)
            context = create_decision_context(
                decision_type,
                context_data.get("agent_id", "cli_agent"),
                context_data,
                context_data.get("constraints", []),
                context_data.get("objectives", []),
                context_data.get("risk_factors", [])
            )
            
            result = self.decision_core.make_autonomous_decision(decision_type, context)
            print(f"✅ Decision made: {result.selected_option}")
            print(f"  Confidence: {result.confidence}")
            print(f"  Reasoning: {result.reasoning}")
            print(f"  Expected Outcome: {result.expected_outcome}")
            print(f"  Risk Assessment: {result.risk_assessment}")
            
            # Add decision pattern to learning engine
            self.learning_engine.add_decision_pattern(decision_type, result.decision_id)
            
        except json.JSONDecodeError:
            print("❌ Invalid JSON context")
        except Exception as e:
            print(f"❌ Decision failed: {e}")
    
    def add_learning_data(self, features_str: str, target: str, context_name: str, performance: str):
        """Add learning data for continuous improvement"""
        try:
            features = [float(x) for x in features_str.split(",")]
            performance_val = float(performance)
            
            learning_data = create_learning_data(
                features, target, context_name, performance_val, performance_val / 100.0
            )
            
            self.learning_engine.add_learning_data(learning_data)
            print("✅ Learning data added")
            print(f"  Features: {len(features)} dimensions")
            print(f"  Target: {target}")
            print(f"  Context: {context_name}")
            print(f"  Performance: {performance_val}")
            
        except ValueError:
            print("❌ Invalid numeric values")
        except Exception as e:
            print(f"❌ Failed to add learning data: {e}")
    
    def update_agent(self, agent_id: str, skills_str: str, experience: str):
        """Update agent capability information"""
        try:
            skills = skills_str.split(",")
            experience_val = float(experience)
            
            capability = create_agent_capability(
                agent_id, skills, experience_val, 0.1, "general"
            )
            
            self.decision_core.update_agent_capability(agent_id, capability)
            self.learning_engine.update_agent_capability(agent_id, capability)
            
            print(f"✅ Agent capability updated: {agent_id}")
            print(f"  Skills: {', '.join(skills)}")
            print(f"  Experience: {experience_val}")
            
        except ValueError:
            print("❌ Invalid experience value")
        except Exception as e:
            print(f"❌ Failed to update agent: {e}")
    
    def record_metric(self, metric_name: str, value: str):
        """Record a performance metric for learning"""
        try:
            metric_value = float(value)
            self.learning_engine.record_performance_metric(metric_name, metric_value)
            print(f"✅ Performance metric recorded: {metric_name} = {metric_value}")
            
        except ValueError:
            print("❌ Invalid metric value")
        except Exception as e:
            print(f"❌ Failed to record metric: {e}")
    
    def show_status(self):
        """Show comprehensive system status"""
        print("🧠 Autonomous Decision System Status:")
        print("=" * 50)
        
        # Decision core status
        decision_status = self.decision_core.get_decision_status()
        print("📊 Decision Core:")
        for key, value in decision_status.items():
            print(f"  {key}: {value}")
        
        print()
        
        # Learning engine status
        learning_status = self.learning_engine.get_learning_status()
        print("🧠 Learning Engine:")
        for key, value in learning_status.items():
            print(f"  {key}: {value}")
    
    def run(self, args=None):
        """Run the CLI with provided arguments"""
        if args is None:
            args = self.parser.parse_args()
        
        try:
            if args.test:
                self.run_test()
            elif args.make_decision:
                decision_type, context_json = args.make_decision
                self.make_decision(decision_type, context_json)
            elif args.add_learning:
                features, target, context, performance = args.add_learning
                self.add_learning_data(features, target, context, performance)
            elif args.update_agent:
                agent_id, skills, experience = args.update_agent
                self.update_agent(agent_id, skills, experience)
            elif args.record_metric:
                metric_name, value = args.record_metric
                self.record_metric(metric_name, value)
            elif args.status:
                self.show_status()
            else:
                self.parser.print_help()
                
        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")
        except Exception as e:
            print(f"❌ CLI error: {e}")
        finally:
            self.decision_core.shutdown()
            self.learning_engine.shutdown()


def main():
    """Main CLI entry point"""
    cli = DecisionCLI()
    cli.run()


if __name__ == "__main__":
    main()
