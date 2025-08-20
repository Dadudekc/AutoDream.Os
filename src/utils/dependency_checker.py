#!/usr/bin/env python3
"""
Dependency Checker Module - Dependency Validation

This module provides dependency checking functionality.
Follows Single Responsibility Principle - only dependency validation.
Architecture: Single Responsibility Principle - dependency checking only
LOC: 80 lines (under 200 limit)
"""

import logging
from typing import Dict, List, Optional, Any


class DependencyChecker:
    """Dependency availability and validation checker"""
    
    @staticmethod
    def check_dependencies() -> Dict[str, bool]:
        """Check if required dependencies are available"""
        dependencies = {
            "psutil": False,
            "yaml": False,
            "pathlib": True,  # Built-in
            "logging": True,  # Built-in
            "json": True,     # Built-in
            "re": True        # Built-in
        }
        
        try:
            import psutil
            dependencies["psutil"] = True
        except ImportError:
            pass
        
        try:
            import yaml
            dependencies["yaml"] = True
        except ImportError:
            pass
        
        return dependencies
    
    @staticmethod
    def check_specific_dependency(module_name: str) -> bool:
        """Check if a specific dependency is available"""
        try:
            __import__(module_name)
            return True
        except ImportError:
            return False
    
    @staticmethod
    def get_missing_dependencies(required_deps: List[str]) -> List[str]:
        """Get list of missing required dependencies"""
        missing = []
        for dep in required_deps:
            if not DependencyChecker.check_specific_dependency(dep):
                missing.append(dep)
        return missing
    
    @staticmethod
    def validate_environment() -> Dict[str, Any]:
        """Validate the current environment for required dependencies"""
        try:
            deps = DependencyChecker.check_dependencies()
            
            # Check critical dependencies
            critical_deps = ["psutil", "yaml"]
            missing_critical = [dep for dep in critical_deps if not deps.get(dep, False)]
            
            validation_result = {
                "all_dependencies_available": all(deps.values()),
                "critical_dependencies_available": len(missing_critical) == 0,
                "missing_critical": missing_critical,
                "dependency_status": deps,
                "environment_ready": len(missing_critical) == 0
            }
            
            return validation_result
            
        except Exception as e:
            logging.error(f"Failed to validate environment: {e}")
            return {
                "all_dependencies_available": False,
                "critical_dependencies_available": False,
                "missing_critical": ["unknown"],
                "dependency_status": {},
                "environment_ready": False,
                "error": str(e)
            }


def run_smoke_test():
    """Run basic functionality test for DependencyChecker"""
    print("🧪 Running DependencyChecker Smoke Test...")
    
    try:
        # Test dependency checking
        deps = DependencyChecker.check_dependencies()
        assert isinstance(deps, dict)
        assert "psutil" in deps
        
        # Test specific dependency check
        pathlib_available = DependencyChecker.check_specific_dependency("pathlib")
        assert pathlib_available  # pathlib is built-in
        
        # Test missing dependencies
        missing = DependencyChecker.get_missing_dependencies(["nonexistent_module"])
        assert "nonexistent_module" in missing
        
        # Test environment validation
        validation = DependencyChecker.validate_environment()
        assert "environment_ready" in validation
        
        print("✅ DependencyChecker Smoke Test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ DependencyChecker Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for DependencyChecker testing"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Dependency Checker CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--check", action="store_true", help="Check all dependencies")
    parser.add_argument("--module", help="Check specific module")
    parser.add_argument("--required", nargs='+', help="Check required dependencies")
    parser.add_argument("--validate", action="store_true", help="Validate environment")
    
    args = parser.parse_args()
    
    if args.test:
        run_smoke_test()
        return
    
    if args.check:
        deps = DependencyChecker.check_dependencies()
        print("Dependencies:")
        for dep, available in deps.items():
            status = "✅" if available else "❌"
            print(f"  {status} {dep}")
    elif args.module:
        available = DependencyChecker.check_specific_dependency(args.module)
        status = "✅ Available" if available else "❌ Missing"
        print(f"Module '{args.module}': {status}")
    elif args.required:
        missing = DependencyChecker.get_missing_dependencies(args.required)
        if missing:
            print(f"❌ Missing dependencies: {missing}")
        else:
            print("✅ All required dependencies available")
    elif args.validate:
        validation = DependencyChecker.validate_environment()
        print("Environment Validation:")
        for key, value in validation.items():
            print(f"  {key}: {value}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
