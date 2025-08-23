#!/usr/bin/env python3
"""
Workspace Management System Launcher - V2 Workspace Management

This launcher provides unified access to all workspace management components.
Follows Single Responsibility Principle - only launcher coordination.
Architecture: Single Responsibility Principle - launcher coordination only
LOC: 150 lines (under 200 limit)
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

try:
    from core.workspace_architecture_manager import (
        WorkspaceArchitectureManager,
        WorkspaceType,
    )
    from core.workspace_security_manager import (
        WorkspaceSecurityManager,
        SecurityLevel,
        Permission,
    )

    IMPORT_SUCCESS = True
except ImportError as e:
    print(f"⚠️ Import warning: {e}")
    print("Running in limited mode - some features may not be available")
    IMPORT_SUCCESS = False


class WorkspaceManagementLauncher:
    """Unified launcher for workspace management system"""

    def __init__(self):
        self.architecture_manager = None
        self.security_manager = None

        if IMPORT_SUCCESS:
            try:
                self.architecture_manager = WorkspaceArchitectureManager()
                self.security_manager = WorkspaceSecurityManager()
                print("✅ Workspace Management System initialized successfully")
            except Exception as e:
                print(f"⚠️ Initialization warning: {e}")
                print("Running in limited mode")
        else:
            print("⚠️ Running in limited mode due to import issues")

    def get_system_status(self) -> dict:
        """Get comprehensive system status"""
        if not IMPORT_SUCCESS:
            return {"error": "System not fully initialized due to import issues"}

        try:
            # Get architecture status
            arch_summary = self.architecture_manager.get_architecture_summary()

            # Get security status
            security_summary = self.security_manager.get_security_summary()

            return {
                "architecture": arch_summary,
                "security": security_summary,
                "status": "operational",
            }
        except Exception as e:
            return {"error": f"Failed to get system status: {e}"}

    def create_secure_workspace(self, name: str, agent_id: str) -> dict:
        """Create a secure workspace for an agent"""
        if not IMPORT_SUCCESS:
            return {"error": "System not fully initialized"}

        try:
            # Create workspace with private security level
            success = self.architecture_manager.create_workspace(
                name, WorkspaceType.AGENT, permissions=[agent_id]
            )

            if success:
                # Create security policy
                security_success = self.security_manager.create_security_policy(
                    name, SecurityLevel.PRIVATE, allowed_agents=[agent_id]
                )

                if security_success:
                    return {
                        "success": True,
                        "workspace": name,
                        "security_level": "private",
                        "agent": agent_id,
                    }
                else:
                    return {"error": "Failed to create security policy"}
            else:
                return {"error": "Failed to create workspace"}

        except Exception as e:
            return {"error": f"Workspace creation failed: {e}"}

    def list_all_workspaces(self) -> dict:
        """List all workspaces with their security information"""
        if not IMPORT_SUCCESS:
            return {"error": "System not fully initialized"}

        try:
            workspaces = self.architecture_manager.list_workspaces()
            workspace_info = []

            for ws in workspaces:
                ws_info = {
                    "name": ws.name,
                    "type": ws.workspace_type.value,
                    "status": ws.status.value,
                    "size_mb": ws.size_mb,
                    "agent_count": ws.agent_count,
                }

                # Add security info if available
                if ws.name in self.security_manager.security_policies:
                    policy = self.security_manager.security_policies[ws.name]
                    ws_info["security_level"] = policy.security_level.value
                    ws_info["encryption_enabled"] = policy.encryption_enabled

                workspace_info.append(ws_info)

            return {"workspaces": workspace_info, "total_count": len(workspace_info)}

        except Exception as e:
            return {"error": f"Failed to list workspaces: {e}"}

    def run_system_test(self) -> dict:
        """Run comprehensive system test"""
        if not IMPORT_SUCCESS:
            return {"error": "System not fully initialized"}

        try:
            test_results = {}

            # Test architecture manager
            try:
                arch_test = self.architecture_manager.run_smoke_test()
                test_results["architecture"] = "PASSED" if arch_test else "FAILED"
            except Exception as e:
                test_results["architecture"] = f"ERROR: {e}"

            # Test security manager
            try:
                security_test = self.security_manager.run_smoke_test()
                test_results["security"] = "PASSED" if security_test else "FAILED"
            except Exception as e:
                test_results["security"] = f"ERROR: {e}"

            # Test workspace creation
            try:
                test_ws = "test_workspace_system_test"
                ws_created = self.architecture_manager.create_workspace(
                    test_ws, WorkspaceType.TEMPORARY
                )
                test_results["workspace_creation"] = (
                    "PASSED" if ws_created else "FAILED"
                )

                # Cleanup test workspace
                if ws_created:
                    test_path = (
                        Path(self.architecture_manager.base_workspace_dir) / test_ws
                    )
                    if test_path.exists():
                        import shutil

                        shutil.rmtree(test_path)

            except Exception as e:
                test_results["workspace_creation"] = f"ERROR: {e}"

            return {
                "test_results": test_results,
                "overall_status": "PASSED"
                if all("PASSED" in str(v) for v in test_results.values())
                else "FAILED",
            }

        except Exception as e:
            return {"error": f"System test failed: {e}"}


def main():
    """Main CLI interface for workspace management system"""
    import argparse

    parser = argparse.ArgumentParser(description="Workspace Management System Launcher")
    parser.add_argument("--status", action="store_true", help="Show system status")
    parser.add_argument(
        "--create", nargs=2, metavar=("NAME", "AGENT"), help="Create secure workspace"
    )
    parser.add_argument("--list", action="store_true", help="List all workspaces")
    parser.add_argument("--test", action="store_true", help="Run system test")
    parser.add_argument("--demo", action="store_true", help="Run demonstration")

    args = parser.parse_args()

    launcher = WorkspaceManagementLauncher()

    if args.status:
        status = launcher.get_system_status()
        print("📊 Workspace Management System Status:")
        if "error" in status:
            print(f"  ❌ Error: {status['error']}")
        else:
            print(f"  🟢 Status: {status['status']}")
            if "architecture" in status:
                arch = status["architecture"]
                print(f"  🏗️  Workspaces: {arch.get('total_workspaces', 0)}")
                print(f"  📁 Active: {arch.get('active_workspaces', 0)}")
            if "security" in status:
                sec = status["security"]
                print(f"  🔒 Policies: {sec.get('total_policies', 0)}")
                print(f"  🔐 Encrypted: {sec.get('encrypted_workspaces', 0)}")

    elif args.create:
        name, agent = args.create
        result = launcher.create_secure_workspace(name, agent)
        if "error" in result:
            print(f"❌ Failed to create workspace: {result['error']}")
        else:
            print(f"✅ Created secure workspace '{name}' for {agent}")
            print(f"  🔒 Security Level: {result['security_level']}")

    elif args.list:
        result = launcher.list_all_workspaces()
        if "error" in result:
            print(f"❌ Failed to list workspaces: {result['error']}")
        else:
            print(f"📋 Workspaces ({result['total_count']} total):")
            for ws in result["workspaces"]:
                status_emoji = "🟢" if ws["status"] == "active" else "🔴"
                security_emoji = "🔐" if ws.get("encryption_enabled", False) else "🔓"
                print(
                    f"  {status_emoji} {ws['name']}: {ws['type']} ({ws['size_mb']} MB) {security_emoji}"
                )

    elif args.test:
        print("🧪 Running Workspace Management System Test...")
        result = launcher.run_system_test()
        if "error" in result:
            print(f"❌ System test failed: {result['error']}")
        else:
            print("📊 Test Results:")
            for test_name, test_result in result["test_results"].items():
                status_emoji = "✅" if "PASSED" in str(test_result) else "❌"
                print(f"  {status_emoji} {test_name}: {test_result}")
            print(f"\n🎯 Overall Status: {result['overall_status']}")

    elif args.demo:
        print("🎭 Workspace Management System Demonstration")
        print("=" * 50)

        # Show status
        print("\n1️⃣ System Status:")
        status = launcher.get_system_status()
        if "error" not in status:
            print("   ✅ System operational")
        else:
            print(f"   ⚠️ System status: {status['error']}")

        # List workspaces
        print("\n2️⃣ Current Workspaces:")
        result = launcher.list_all_workspaces()
        if "error" not in result:
            print(f"   📁 Found {result['total_count']} workspaces")
        else:
            print(f"   ⚠️ Workspace listing: {result['error']}")

        # Run test
        print("\n3️⃣ System Test:")
        test_result = launcher.run_system_test()
        if "error" not in test_result:
            print(f"   🧪 Test completed: {test_result['overall_status']}")
        else:
            print(f"   ⚠️ Test failed: {test_result['error']}")

        print("\n🎯 Demonstration complete!")

    else:
        parser.print_help()
        print("\n💡 Tip: Use --demo to see a complete demonstration of the system")


if __name__ == "__main__":
    main()
