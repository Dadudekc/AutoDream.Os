#!/usr/bin/env python3
"""
Learning & Decision CLI - Agent Cellphone V2
===========================================

CLI for the unified learning and decision system.
Follows V2 standards: 400 LOC, OOP design, SRP.

**Author:** V2 Consolidation Specialist
**Created:** Current Sprint
**Status:** ACTIVE - CONSOLIDATION IN PROGRESS
"""

import argparse
import logging
import sys
from typing import Dict, List, Any, Optional
from datetime import datetime

from .learning_manager import LearningManager
from .decision_manager import DecisionManager
from .unified_learning_engine import UnifiedLearningEngine
from .models import (
    LearningMode, IntelligenceLevel, LearningStatus, LearningEngineConfig
)
from .decision_models import (
    DecisionType, DecisionPriority, DecisionStatus, DecisionConfidence
)


class LearningDecisionCLI:
    """
    CLI for the unified learning and decision system
    
    This CLI provides access to all learning and decision functionality
    previously scattered across multiple implementations
    """
    
    def __init__(self):
        self.learning_manager: Optional[LearningManager] = None
        self.decision_manager: Optional[DecisionManager] = None
        self.learning_engine: Optional[UnifiedLearningEngine] = None
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Initialize managers
        self._initialize_managers()
    
    def _initialize_managers(self):
        """Initialize learning and decision managers"""
        try:
            # Initialize learning manager
            self.learning_manager = LearningManager(
                manager_id="cli_learning_manager",
                name="CLI Learning Manager",
                description="Learning manager for CLI operations"
            )
            
            # Initialize decision manager
            self.decision_manager = DecisionManager(
                manager_id="cli_decision_manager",
                name="CLI Decision Manager",
                description="Decision manager for CLI operations"
            )
            
            # Initialize learning engine
            engine_config = LearningEngineConfig()
            self.learning_engine = UnifiedLearningEngine(engine_config)
            
            # Start managers
            self.learning_manager.start()
            self.decision_manager.start()
            
            self.logger.info("Learning and Decision managers initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize managers: {e}")
            sys.exit(1)
    
    def run(self, args: Optional[List[str]] = None):
        """Run the CLI with the given arguments"""
        try:
            parser = self._create_parser()
            parsed_args = parser.parse_args(args)
            
            # Execute the appropriate command
            if parsed_args.command == "learning":
                self._handle_learning_command(parsed_args)
            elif parsed_args.command == "decision":
                self._handle_decision_command(parsed_args)
            elif parsed_args.command == "engine":
                self._handle_engine_command(parsed_args)
            elif parsed_args.command == "status":
                self._handle_status_command(parsed_args)
            else:
                parser.print_help()
                
        except KeyboardInterrupt:
            self.logger.info("CLI interrupted by user")
            self._cleanup()
        except Exception as e:
            self.logger.error(f"CLI error: {e}")
            self._cleanup()
            sys.exit(1)
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create the command line argument parser"""
        parser = argparse.ArgumentParser(
            description="Unified Learning & Decision System CLI",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  %(prog)s learning session start --agent agent-1 --goals "goal1,goal2" --strategies "adaptive,collaborative"
  %(prog)s learning session end --session-id <session_id>
  %(prog)s learning data add --session-id <session_id> --context "test_context" --score 85.5
  %(prog)s decision make --type task_assignment --requester agent-1 --priority 3
  %(prog)s engine status
  %(prog)s status --detailed
            """
        )
        
        # Main command
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Learning commands
        learning_parser = subparsers.add_parser('learning', help='Learning operations')
        learning_subparsers = learning_parser.add_subparsers(dest='learning_subcommand', help='Learning subcommands')
        
        # Learning session commands
        session_parser = learning_subparsers.add_parser('session', help='Learning session operations')
        session_subparsers = session_parser.add_subparsers(dest='session_subcommand', help='Session subcommands')
        
        # Start session
        start_session = session_subparsers.add_parser('start', help='Start a learning session')
        start_session.add_argument('--agent', required=True, help='Agent ID for the session')
        start_session.add_argument('--goals', required=True, help='Comma-separated learning goals')
        start_session.add_argument('--strategies', required=True, help='Comma-separated learning strategies')
        start_session.add_argument('--name', help='Optional session name')
        
        # End session
        end_session = session_subparsers.add_parser('end', help='End a learning session')
        end_session.add_argument('--session-id', required=True, help='Session ID to end')
        
        # Learning data commands
        data_parser = learning_subparsers.add_parser('data', help='Learning data operations')
        data_subparsers = data_parser.add_subparsers(dest='data_subcommand', help='Data subcommands')
        
        # Add data
        add_data = data_subparsers.add_parser('add', help='Add learning data to a session')
        add_data.add_argument('--session-id', required=True, help='Session ID to add data to')
        add_data.add_argument('--context', required=True, help='Learning context')
        add_data.add_argument('--input', help='Input data (JSON format)')
        add_data.add_argument('--output', help='Output data (JSON format)')
        add_data.add_argument('--score', type=float, required=True, help='Performance score (0-100)')
        add_data.add_argument('--mode', choices=[m.value for m in LearningMode], default='adaptive', help='Learning mode')
        
        # Learning goal commands
        goal_parser = learning_subparsers.add_parser('goal', help='Learning goal operations')
        goal_subparsers = goal_parser.add_subparsers(dest='goal_subcommand', help='Goal subcommands')
        
        # Create goal
        create_goal = goal_subparsers.add_parser('create', help='Create a learning goal')
        create_goal.add_argument('--title', required=True, help='Goal title')
        create_goal.add_argument('--description', required=True, help='Goal description')
        create_goal.add_argument('--target-metrics', help='Target metrics (JSON format)')
        create_goal.add_argument('--priority', type=int, choices=range(1, 6), default=1, help='Goal priority (1-5)')
        create_goal.add_argument('--deadline', help='Goal deadline (ISO format)')
        
        # Learning pattern commands
        pattern_parser = learning_subparsers.add_parser('pattern', help='Learning pattern operations')
        pattern_subparsers = pattern_parser.add_subparsers(dest='pattern_subcommand', help='Pattern subcommands')
        
        # Analyze patterns
        analyze_patterns = pattern_subparsers.add_parser('analyze', help='Analyze learning patterns')
        analyze_patterns.add_argument('--agent', required=True, help='Agent ID to analyze')
        
        # Learning performance commands
        performance_parser = learning_subparsers.add_parser('performance', help='Learning performance operations')
        performance_subparsers = performance_parser.add_subparsers(dest='performance_subcommand', help='Performance subcommands')
        
        # Get performance summary
        get_performance = performance_subparsers.add_parser('summary', help='Get learning performance summary')
        get_performance.add_argument('--agent', required=True, help='Agent ID to get summary for')
        
        # Decision commands
        decision_parser = subparsers.add_parser('decision', help='Decision operations')
        decision_subparsers = decision_parser.add_subparsers(dest='decision_subcommand', help='Decision subcommands')
        
        # Make decision
        make_decision = decision_subparsers.add_parser('make', help='Make a decision')
        make_decision.add_argument('--type', required=True, choices=[t.value for t in DecisionType], help='Decision type')
        make_decision.add_argument('--requester', required=True, help='Requester ID')
        make_decision.add_argument('--parameters', help='Decision parameters (JSON format)')
        make_decision.add_argument('--priority', type=int, choices=range(1, 6), default=2, help='Decision priority (1-5)')
        make_decision.add_argument('--algorithm', help='Specific algorithm ID to use')
        make_decision.add_argument('--workflow', help='Specific workflow ID to use')
        
        # Decision status commands
        decision_status = decision_subparsers.add_parser('status', help='Get decision status')
        decision_status.add_argument('--detailed', action='store_true', help='Show detailed status')
        
        # Engine commands
        engine_parser = subparsers.add_parser('engine', help='Learning engine operations')
        engine_subparsers = engine_parser.add_subparsers(dest='engine_subcommand', help='Engine subcommands')
        
        # Engine status
        engine_status = engine_subparsers.add_parser('status', help='Get engine status')
        
        # Status commands
        status_parser = subparsers.add_parser('status', help='System status operations')
        status_parser.add_argument('--detailed', action='store_true', help='Show detailed status')
        
        return parser
    
    def _handle_learning_command(self, args):
        """Handle learning-related commands"""
        if args.learning_subcommand == 'session':
            self._handle_session_command(args)
        elif args.learning_subcommand == 'data':
            self._handle_data_command(args)
        elif args.learning_subcommand == 'goal':
            self._handle_goal_command(args)
        elif args.learning_subcommand == 'pattern':
            self._handle_pattern_command(args)
        elif args.learning_subcommand == 'performance':
            self._handle_performance_command(args)
        else:
            print("Unknown learning subcommand. Use --help for available options.")
    
    def _handle_session_command(self, args):
        """Handle learning session commands"""
        if args.session_subcommand == 'start':
            self._start_learning_session(args)
        elif args.session_subcommand == 'end':
            self._end_learning_session(args)
        else:
            print("Unknown session subcommand. Use --help for available options.")
    
    def _start_learning_session(self, args):
        """Start a learning session"""
        try:
            # Parse goals and strategies
            goals = [g.strip() for g in args.goals.split(',')]
            strategies = [s.strip() for s in args.strategies.split(',')]
            
            # Start session
            session_id = self.learning_manager.start_learning_session(
                agent_id=args.agent,
                learning_goals=goals,
                strategies=strategies,
                session_name=args.name
            )
            
            print(f"✅ Learning session started successfully!")
            print(f"   Session ID: {session_id}")
            print(f"   Agent: {args.agent}")
            print(f"   Goals: {', '.join(goals)}")
            print(f"   Strategies: {', '.join(strategies)}")
            
        except Exception as e:
            print(f"❌ Failed to start learning session: {e}")
            self.logger.error(f"Failed to start learning session: {e}")
    
    def _end_learning_session(self, args):
        """End a learning session"""
        try:
            success = self.learning_manager.end_learning_session(args.session_id)
            
            if success:
                print(f"✅ Learning session ended successfully!")
                print(f"   Session ID: {args.session_id}")
            else:
                print(f"❌ Failed to end learning session")
                
        except Exception as e:
            print(f"❌ Failed to end learning session: {e}")
            self.logger.error(f"Failed to end learning session: {e}")
    
    def _handle_data_command(self, args):
        """Handle learning data commands"""
        if args.data_subcommand == 'add':
            self._add_learning_data(args)
        else:
            print("Unknown data subcommand. Use --help for available options.")
    
    def _add_learning_data(self, args):
        """Add learning data to a session"""
        try:
            # Parse input and output data
            input_data = {}
            output_data = {}
            
            if args.input:
                import json
                input_data = json.loads(args.input)
            
            if args.output:
                import json
                output_data = json.loads(args.output)
            
            # Determine learning mode
            learning_mode = LearningMode(args.mode)
            
            # Add data
            success = self.learning_manager.add_learning_data(
                session_id=args.session_id,
                context=args.context,
                input_data=input_data,
                output_data=output_data,
                performance_score=args.score,
                learning_mode=learning_mode
            )
            
            if success:
                print(f"✅ Learning data added successfully!")
                print(f"   Session ID: {args.session_id}")
                print(f"   Context: {args.context}")
                print(f"   Score: {args.score}")
                print(f"   Mode: {args.mode}")
            else:
                print(f"❌ Failed to add learning data")
                
        except Exception as e:
            print(f"❌ Failed to add learning data: {e}")
            self.logger.error(f"Failed to add learning data: {e}")
    
    def _handle_goal_command(self, args):
        """Handle learning goal commands"""
        if args.goal_subcommand == 'create':
            self._create_learning_goal(args)
        else:
            print("Unknown goal subcommand. Use --help for available options.")
    
    def _create_learning_goal(self, args):
        """Create a learning goal"""
        try:
            # Parse target metrics
            target_metrics = {}
            if args.target_metrics:
                import json
                target_metrics = json.loads(args.target_metrics)
            
            # Parse deadline
            deadline = None
            if args.deadline:
                deadline = datetime.fromisoformat(args.deadline)
            
            # Create goal
            goal_id = self.learning_manager.create_learning_goal(
                title=args.title,
                description=args.description,
                target_metrics=target_metrics,
                priority=args.priority,
                deadline=deadline
            )
            
            print(f"✅ Learning goal created successfully!")
            print(f"   Goal ID: {goal_id}")
            print(f"   Title: {args.title}")
            print(f"   Priority: {args.priority}")
            
        except Exception as e:
            print(f"❌ Failed to create learning goal: {e}")
            self.logger.error(f"Failed to create learning goal: {e}")
    
    def _handle_pattern_command(self, args):
        """Handle learning pattern commands"""
        if args.pattern_subcommand == 'analyze':
            self._analyze_learning_patterns(args)
        else:
            print("Unknown pattern subcommand. Use --help for available options.")
    
    def _analyze_learning_patterns(self, args):
        """Analyze learning patterns for an agent"""
        try:
            patterns = self.learning_manager.analyze_learning_patterns(args.agent)
            
            if patterns:
                print(f"✅ Found {len(patterns)} learning patterns for agent {args.agent}:")
                for pattern in patterns:
                    print(f"   • {pattern.pattern_type} (confidence: {pattern.confidence_score:.2f})")
                    if pattern.supporting_data:
                        for data in pattern.supporting_data:
                            print(f"     - {data}")
            else:
                print(f"ℹ️  No learning patterns found for agent {args.agent}")
                
        except Exception as e:
            print(f"❌ Failed to analyze learning patterns: {e}")
            self.logger.error(f"Failed to analyze learning patterns: {e}")
    
    def _handle_performance_command(self, args):
        """Handle learning performance commands"""
        if args.performance_subcommand == 'summary':
            self._get_learning_performance_summary(args)
        else:
            print("Unknown performance subcommand. Use --help for available options.")
    
    def _get_learning_performance_summary(self, args):
        """Get learning performance summary for an agent"""
        try:
            summary = self.learning_manager.get_learning_performance_summary(args.agent)
            
            if "error" not in summary:
                print(f"✅ Learning performance summary for agent {args.agent}:")
                print(f"   Total sessions: {summary.get('total_sessions', 0)}")
                print(f"   Active sessions: {summary.get('active_sessions', 0)}")
                print(f"   Total goals: {summary.get('total_learning_goals', 0)}")
                print(f"   Completed goals: {summary.get('completed_goals', 0)}")
                print(f"   Average performance: {summary.get('average_performance', 0):.2f}")
                
                patterns = summary.get('learning_patterns', [])
                if patterns:
                    print(f"   Learning patterns: {', '.join(patterns)}")
                
                recent_metrics = summary.get('recent_metrics', {})
                if recent_metrics:
                    print(f"   Recent metrics: {recent_metrics.get('metric_name', 'N/A')}")
                    print(f"     Average: {recent_metrics.get('average_value', 0):.2f}")
                    print(f"     Trend: {recent_metrics.get('trend', 'N/A')}")
            else:
                print(f"❌ Failed to get performance summary: {summary['error']}")
                
        except Exception as e:
            print(f"❌ Failed to get performance summary: {e}")
            self.logger.error(f"Failed to get performance summary: {e}")
    
    def _handle_decision_command(self, args):
        """Handle decision-related commands"""
        if args.decision_subcommand == 'make':
            self._make_decision(args)
        elif args.decision_subcommand == 'status':
            self._get_decision_status(args)
        else:
            print("Unknown decision subcommand. Use --help for available options.")
    
    def _make_decision(self, args):
        """Make a decision"""
        try:
            # Parse parameters
            parameters = {}
            if args.parameters:
                import json
                parameters = json.loads(args.parameters)
            
            # Determine decision type and priority
            decision_type = DecisionType(args.type)
            priority = DecisionPriority(args.priority)
            
            # Make decision
            result = self.decision_manager.make_decision(
                decision_type=decision_type,
                requester=args.requester,
                parameters=parameters,
                priority=priority,
                algorithm_id=args.algorithm,
                workflow_id=args.workflow
            )
            
            print(f"✅ Decision made successfully!")
            print(f"   Decision ID: {result.decision_id}")
            print(f"   Type: {args.type}")
            print(f"   Outcome: {result.outcome}")
            print(f"   Confidence: {result.confidence.value}")
            print(f"   Reasoning: {result.reasoning}")
            
        except Exception as e:
            print(f"❌ Failed to make decision: {e}")
            self.logger.error(f"Failed to make decision: {e}")
    
    def _get_decision_status(self, args):
        """Get decision status"""
        try:
            status = self.decision_manager.get_decision_status()
            
            print(f"✅ Decision Manager Status:")
            print(f"   Status: {status.get('status', 'N/A')}")
            print(f"   Decision algorithms: {status.get('decision_algorithms', 0)}")
            print(f"   Decision rules: {status.get('decision_rules', 0)}")
            print(f"   Decision workflows: {status.get('decision_workflows', 0)}")
            print(f"   Active decisions: {status.get('active_decisions', 0)}")
            print(f"   Decision history: {status.get('decision_history_size', 0)}")
            
            if args.detailed:
                operations = status.get('decision_operations', {})
                print(f"   Total decisions: {operations.get('total', 0)}")
                print(f"   Success rate: {operations.get('success_rate', 0):.2f}%")
                
        except Exception as e:
            print(f"❌ Failed to get decision status: {e}")
            self.logger.error(f"Failed to get decision status: {e}")
    
    def _handle_engine_command(self, args):
        """Handle learning engine commands"""
        if args.engine_subcommand == 'status':
            self._get_engine_status()
        else:
            print("Unknown engine subcommand. Use --help for available options.")
    
    def _get_engine_status(self):
        """Get learning engine status"""
        try:
            status = self.learning_engine.get_engine_status()
            
            print(f"✅ Learning Engine Status:")
            print(f"   Engine ID: {status.get('engine_id', 'N/A')}")
            print(f"   Status: {status.get('status', 'N/A')}")
            print(f"   Uptime: {status.get('uptime_seconds', 0):.1f} seconds")
            print(f"   Total operations: {status.get('total_operations', 0)}")
            print(f"   Success rate: {status.get('success_rate', 0):.2f}%")
            print(f"   Active sessions: {status.get('active_sessions', 0)}")
            print(f"   Learning goals: {status.get('learning_goals', 0)}")
            print(f"   Decision algorithms: {status.get('decision_algorithms', 0)}")
            print(f"   Learning strategies: {status.get('learning_strategies', 0)}")
            
        except Exception as e:
            print(f"❌ Failed to get engine status: {e}")
            self.logger.error(f"Failed to get engine status: {e}")
    
    def _handle_status_command(self, args):
        """Handle system status commands"""
        try:
            print(f"✅ Unified Learning & Decision System Status:")
            print()
            
            # Learning Manager Status
            learning_status = self.learning_manager.get_learning_status()
            print(f"📚 Learning Manager:")
            print(f"   Status: {learning_status.get('status', 'N/A')}")
            print(f"   Active learners: {learning_status.get('active_learners', 0)}")
            print(f"   Learning sessions: {learning_status.get('total_learning_sessions', 0)}")
            print(f"   Learning goals: {learning_status.get('total_learning_goals', 0)}")
            
            if args.detailed:
                operations = learning_status.get('learning_operations', {})
                print(f"   Total operations: {operations.get('total', 0)}")
                print(f"   Success rate: {operations.get('success_rate', 0):.2f}%")
            
            print()
            
            # Decision Manager Status
            decision_status = self.decision_manager.get_decision_status()
            print(f"🎯 Decision Manager:")
            print(f"   Status: {decision_status.get('status', 'N/A')}")
            print(f"   Decision algorithms: {decision_status.get('decision_algorithms', 0)}")
            print(f"   Active decisions: {decision_status.get('active_decisions', 0)}")
            print(f"   Decision history: {decision_status.get('decision_history_size', 0)}")
            
            if args.detailed:
                operations = decision_status.get('decision_operations', {})
                print(f"   Total decisions: {operations.get('total', 0)}")
                print(f"   Success rate: {operations.get('success_rate', 0):.2f}%")
            
            print()
            
            # Learning Engine Status
            engine_status = self.learning_engine.get_engine_status()
            print(f"🚀 Learning Engine:")
            print(f"   Status: {engine_status.get('status', 'N/A')}")
            print(f"   Uptime: {engine_status.get('uptime_seconds', 0):.1f} seconds")
            print(f"   Total operations: {engine_status.get('total_operations', 0)}")
            print(f"   Success rate: {engine_status.get('success_rate', 0):.2f}%")
            
        except Exception as e:
            print(f"❌ Failed to get system status: {e}")
            self.logger.error(f"Failed to get system status: {e}")
    
    def _cleanup(self):
        """Clean up resources before exit"""
        try:
            if self.learning_manager:
                self.learning_manager.stop()
            
            if self.decision_manager:
                self.decision_manager.stop()
                
            self.logger.info("CLI cleanup completed")
            
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")


def main():
    """Main entry point for the CLI"""
    cli = LearningDecisionCLI()
    cli.run()


if __name__ == "__main__":
    main()


