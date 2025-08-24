import os


def test_launcher_script_standalone():
    """Test launcher script availability and structure."""
    print("\n🚀 Testing Launcher Script Standalone")
    print("=" * 35)

    try:
        launcher_path = "scripts/launch_performance_monitoring.py"

        if os.path.exists(launcher_path):
            print("✅ Launcher script found")

            with open(launcher_path, "r") as f:
                content = f.read()

            checks = [
                ("Main launcher class", "PerformanceMonitoringLauncher" in content),
                ("CLI interface", "argparse" in content),
                ("Async support", "asyncio" in content),
                ("Configuration loading", "load_config" in content),
                ("Component setup", "setup_performance_monitor" in content),
                ("Dashboard setup", "setup_dashboard" in content),
                ("Alerting setup", "setup_alerting_system" in content),
                ("Signal handling", "signal_handler" in content),
                ("Main entry point", "if __name__" in content),
            ]

            all_passed = True
            for check_name, check_result in checks:
                status = "✅" if check_result else "❌"
                print(f"   - {check_name}: {status}")
                if not check_result:
                    all_passed = False

            if all_passed:
                print("✅ Launcher script structure is complete")
            else:
                print("❌ Launcher script missing some components")
                return False

            lines = len(content.split("\n"))
            print(f"✅ Launcher script size: {lines} lines")

            return True
        else:
            print("❌ Launcher script not found")
            return False

    except Exception as e:
        print(f"❌ Launcher script test failed: {e}")
        return False
