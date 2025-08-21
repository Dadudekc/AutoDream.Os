"""
🌐 Web Package - Agent_Cellphone_V2

This package contains web components for the Agent_Cellphone_V2 system:
- Web interfaces
- API endpoints
- Health monitoring web
- Dashboard web components

Following V2 coding standards: ≤300 LOC per file, OOP design, SRP.
"""

__version__ = "2.0.0"
__author__ = "Web & Frontend Team"
__status__ = "ACTIVE"

import argparse
import sys

# Web component imports
try:
    from .health_monitor_web import HealthMonitorWeb
    
    __all__ = [
        'HealthMonitorWeb'
    ]
    
except ImportError as e:
    print(f"⚠️ Warning: Some web components not available: {e}")
    __all__ = []

def main():
    """CLI interface for web module"""
    parser = argparse.ArgumentParser(
        description="Agent_Cellphone_V2 Web Module",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python -m src.web --test                    # Run web tests
    python -m src.web --status                 # Show web status
    python -m src.web --demo                   # Run web demo
    python -m src.web --start                  # Start web server
        """
    )
    
    parser.add_argument("--test", action="store_true", 
                       help="Run web module tests")
    parser.add_argument("--status", action="store_true", 
                       help="Show web module status")
    parser.add_argument("--demo", action="store_true", 
                       help="Run web module demo")
    parser.add_argument("--list", action="store_true", 
                       help="List available web components")
    parser.add_argument("--start", action="store_true", 
                       help="Start web server")
    
    args = parser.parse_args()
    
    if args.test:
        print("🧪 Running web module tests...")
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
        print("📊 Web Module Status")
        print("=" * 22)
        print(f"Version: {__version__}")
        print(f"Status: {__status__}")
        print(f"Components: {len(__all__)}")
        print("\n🌐 Available Web Components:")
        for component in __all__:
            print(f"  ✅ {component}")
        return 0
    
    elif args.demo:
        print("🚀 Starting web module demo...")
        try:
            # Create instances and demonstrate functionality
            if 'HealthMonitorWeb' in __all__:
                web = HealthMonitorWeb()
                print("✅ HealthMonitorWeb created")
            
            print("🎯 Web module demo completed")
            return 0
        except Exception as e:
            print(f"❌ Demo failed: {e}")
            return 1
    
    elif args.start:
        print("🌐 Starting web server...")
        try:
            if 'HealthMonitorWeb' in __all__:
                web = HealthMonitorWeb()
                web.start_server()
                print("✅ Web server started successfully")
                return 0
            else:
                print("❌ HealthMonitorWeb not available")
                return 1
        except Exception as e:
            print(f"❌ Web server start failed: {e}")
            return 1
    
    elif args.list:
        print("📋 Available Web Components:")
        for component in __all__:
            print(f"  🌐 {component}")
        return 0
    
    else:
        parser.print_help()
        print(f"\n🌐 Web Module {__version__} - {__status__}")
        print("Use --help for more options!")
        return 0

if __name__ == "__main__":
    sys.exit(main())
