"""
🔧 Core Package - Agent_Cellphone_V2

This package contains the core components for the Agent_Cellphone_V2 system:
- Performance monitoring and tracking
- API gateway and communication
- Health monitoring and alerting
- Agent communication protocols

Following V2 coding standards: ≤300 LOC per file, OOP design, SRP.
"""

__version__ = "2.0.0"
__author__ = "Integration & Performance Optimization Captain"
__status__ = "ACTIVE"

import argparse
import sys

# Core component imports
try:
    from .performance_tracker import PerformanceTracker
    from .health_score_calculator import HealthScoreCalculator
    
    # Decision system components
    from .decision import AutonomousDecisionEngine, LearningEngine
    
    # FSM system components
    from .fsm_core_v2 import FSMCoreV2
    from .fsm_discord_bridge import FSMDiscordBridge
    
    __all__ = [
        'PerformanceTracker',
        'HealthScoreCalculator',
        'AutonomousDecisionEngine',
        'LearningEngine',
        'FSMCoreV2',
        'FSMDiscordBridge'
    ]
except ImportError as e:
    print(f"⚠️ Warning: Some core components not available: {e}")
    __all__ = []

def main():
    """CLI interface for core module"""
    parser = argparse.ArgumentParser(
        description="Agent_Cellphone_V2 Core Module",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python -m src.core --test                    # Run core tests
    python -m src.core --status                 # Show core status
    python -m src.core --demo                   # Run core demo
        """
    )
    
    parser.add_argument("--test", action="store_true", 
                       help="Run core module tests")
    parser.add_argument("--status", action="store_true", 
                       help="Show core module status")
    parser.add_argument("--demo", action="store_true", 
                       help="Run core module demo")
    parser.add_argument("--list", action="store_true", 
                       help="List available core components")
    
    args = parser.parse_args()
    
    if args.test:
        print("🧪 Running core module tests...")
        # Run tests for each component
        test_results = {}
        for component in __all__:
            try:
                component_class = globals()[component]
                if hasattr(component_class, 'run_smoke_test'):
                    print(f"  Testing {component}...")
                    success = component_class().run_smoke_test()
                    test_results[component] = success
                    print(f"    {'✅ PASS' if success else '❌ FAIL'}")
                else:
                    print(f"  ⚠️ {component} has no smoke test")
                    test_results[component] = False
            except Exception as e:
                print(f"  ❌ {component} test failed: {e}")
                test_results[component] = False
        
        passed = sum(test_results.values())
        total = len(test_results)
        print(f"\n📊 Test Results: {passed}/{total} passed")
        return 0 if passed == total else 1
    
    elif args.status:
        print("📊 Core Module Status")
        print("=" * 25)
        print(f"Version: {__version__}")
        print(f"Status: {__status__}")
        print(f"Components: {len(__all__)}")
        print("\n🔧 Available Components:")
        for component in __all__:
            print(f"  ✅ {component}")
        return 0
    
    elif args.demo:
        print("🚀 Starting core module demo...")
        try:
            # Create instances and demonstrate functionality
            if 'PerformanceTracker' in __all__:
                tracker = PerformanceTracker()
                print("✅ PerformanceTracker created")
            
            if 'HealthScoreCalculator' in __all__:
                calculator = HealthScoreCalculator()
                print("✅ HealthScoreCalculator created")
            
            print("🎯 Core module demo completed")
            return 0
        except Exception as e:
            print(f"❌ Demo failed: {e}")
            return 1
    
    elif args.list:
        print("📋 Available Core Components:")
        for component in __all__:
            print(f"  🔧 {component}")
        return 0
    
    else:
        parser.print_help()
        print(f"\n🔧 Core Module {__version__} - {__status__}")
        print("Use --help for more options!")
        return 0

if __name__ == "__main__":
    sys.exit(main())
