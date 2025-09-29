#!/usr/bin/env python3
# V3-001: Cloud Infrastructure Setup - Deployment Validation
# Agent-1: Architecture Foundation Specialist
#
# Validation script for V2_SWARM cloud infrastructure deployment

import asyncio
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.database.distributed_db_manager import DistributedDatabaseManager
from src.core.security.security_manager import SecurityManager


class DeploymentValidator:
    """Deployment validation for V3-001 infrastructure."""

    def __init__(self):
        self.validation_results = {
            "timestamp": datetime.utcnow().isoformat(),
            "agent": "Agent-1",
            "contract": "V3-001",
            "status": "validation_started",
            "components": {},
        }

    async def validate_all_components(self) -> dict[str, Any]:
        """Validate all infrastructure components."""
        print("🔍 V3-001: Cloud Infrastructure Validation")
        print("Agent-1: Architecture Foundation Specialist")
        print("=" * 50)

        # Validate AWS infrastructure
        await self._validate_aws_infrastructure()

        # Validate Kubernetes deployment
        await self._validate_kubernetes_deployment()

        # Validate security components
        await self._validate_security_components()

        # Validate database connectivity
        await self._validate_database_connectivity()

        # Generate final report
        self._generate_validation_report()

        return self.validation_results

    async def _validate_aws_infrastructure(self) -> None:
        """Validate AWS infrastructure components."""
        print("\n🏗️  Validating AWS Infrastructure...")

        try:
            # Check AWS CLI
            result = subprocess.run(
                ["aws", "sts", "get-caller-identity"], capture_output=True, text=True
            )

            if result.returncode == 0:
                aws_info = json.loads(result.stdout)
                self.validation_results["components"]["aws"] = {
                    "status": "connected",
                    "account_id": aws_info.get("Account"),
                    "user_arn": aws_info.get("Arn"),
                    "region": aws_info.get("Region", "us-west-2"),
                }
                print("✅ AWS credentials validated")
            else:
                self.validation_results["components"]["aws"] = {
                    "status": "error",
                    "error": "AWS credentials not configured",
                }
                print("❌ AWS credentials not configured")

        except Exception as e:
            self.validation_results["components"]["aws"] = {"status": "error", "error": str(e)}
            print(f"❌ AWS validation failed: {e}")

    async def _validate_kubernetes_deployment(self) -> None:
        """Validate Kubernetes deployment."""
        print("\n☸️  Validating Kubernetes Deployment...")

        try:
            # Check kubectl
            result = subprocess.run(
                ["kubectl", "version", "--client"], capture_output=True, text=True
            )

            if result.returncode == 0:
                # Check cluster connection
                cluster_result = subprocess.run(
                    ["kubectl", "get", "nodes"], capture_output=True, text=True
                )

                if cluster_result.returncode == 0:
                    # Check namespace
                    ns_result = subprocess.run(
                        ["kubectl", "get", "namespace", "swarm-v3"], capture_output=True, text=True
                    )

                    if ns_result.returncode == 0:
                        # Check deployment
                        deploy_result = subprocess.run(
                            ["kubectl", "get", "deployment", "swarm-app", "-n", "swarm-v3"],
                            capture_output=True,
                            text=True,
                        )

                        if deploy_result.returncode == 0:
                            self.validation_results["components"]["kubernetes"] = {
                                "status": "deployed",
                                "namespace": "swarm-v3",
                                "deployment": "swarm-app",
                            }
                            print("✅ Kubernetes deployment validated")
                        else:
                            self.validation_results["components"]["kubernetes"] = {
                                "status": "error",
                                "error": "Deployment not found",
                            }
                            print("❌ Deployment not found")
                    else:
                        self.validation_results["components"]["kubernetes"] = {
                            "status": "error",
                            "error": "Namespace not found",
                        }
                        print("❌ Namespace not found")
                else:
                    self.validation_results["components"]["kubernetes"] = {
                        "status": "error",
                        "error": "Cluster not accessible",
                    }
                    print("❌ Cluster not accessible")
            else:
                self.validation_results["components"]["kubernetes"] = {
                    "status": "error",
                    "error": "kubectl not available",
                }
                print("❌ kubectl not available")

        except Exception as e:
            self.validation_results["components"]["kubernetes"] = {
                "status": "error",
                "error": str(e),
            }
            print(f"❌ Kubernetes validation failed: {e}")

    async def _validate_security_components(self) -> None:
        """Validate security components."""
        print("\n🔐 Validating Security Components...")

        try:
            # Initialize security manager
            security_manager = SecurityManager()

            # Test OAuth2 provider
            oauth2_client = security_manager.create_oauth2_client(
                "test-client", ["http://localhost:8000/callback"], ["read", "write"]
            )

            # Test JWT manager
            jwt_token = security_manager.jwt_manager.create_access_token(
                "test-user", "test-agent", ["agent"]
            )

            # Validate token
            token_info = security_manager.jwt_manager.verify_token(jwt_token)

            if token_info:
                self.validation_results["components"]["security"] = {
                    "status": "operational",
                    "oauth2_provider": "active",
                    "jwt_manager": "active",
                    "test_token": "valid",
                }
                print("✅ Security components validated")
            else:
                self.validation_results["components"]["security"] = {
                    "status": "error",
                    "error": "JWT validation failed",
                }
                print("❌ JWT validation failed")

        except Exception as e:
            self.validation_results["components"]["security"] = {"status": "error", "error": str(e)}
            print(f"❌ Security validation failed: {e}")

    async def _validate_database_connectivity(self) -> None:
        """Validate database connectivity."""
        print("\n🗄️  Validating Database Connectivity...")

        try:
            # Initialize database manager
            db_manager = DistributedDatabaseManager()

            # Initialize connections
            await db_manager.initialize_connections()

            # Get connection status
            status = await db_manager.get_connection_status()

            # Test PostgreSQL connection
            if "postgres" in status and status["postgres"]["status"] == "connected":
                # Test query
                result = await db_manager.execute_query("postgres", "SELECT version()")

                if result.success:
                    self.validation_results["components"]["database"] = {
                        "status": "connected",
                        "postgres": "operational",
                        "redis": status.get("redis", {}).get("status", "unknown"),
                    }
                    print("✅ Database connectivity validated")
                else:
                    self.validation_results["components"]["database"] = {
                        "status": "error",
                        "error": "Database query failed",
                    }
                    print("❌ Database query failed")
            else:
                self.validation_results["components"]["database"] = {
                    "status": "error",
                    "error": "Database not connected",
                }
                print("❌ Database not connected")

            # Close connections
            await db_manager.close_connections()

        except Exception as e:
            self.validation_results["components"]["database"] = {"status": "error", "error": str(e)}
            print(f"❌ Database validation failed: {e}")

    def _generate_validation_report(self) -> None:
        """Generate validation report."""
        print("\n📊 Generating Validation Report...")

        # Calculate overall status
        components = self.validation_results["components"]
        total_components = len(components)
        successful_components = sum(
            1
            for comp in components.values()
            if comp.get("status") in ["connected", "deployed", "operational"]
        )

        success_rate = (successful_components / total_components) * 100

        self.validation_results["overall_status"] = (
            "success" if success_rate >= 75 else "partial" if success_rate >= 50 else "failed"
        )
        self.validation_results["success_rate"] = success_rate
        self.validation_results["total_components"] = total_components
        self.validation_results["successful_components"] = successful_components

        # Save report
        report_file = project_root / "infrastructure" / "validation_report.json"
        with open(report_file, "w") as f:
            json.dump(self.validation_results, f, indent=2)

        print(f"✅ Validation report saved: {report_file}")

        # Print summary
        print("\n" + "=" * 50)
        print("📋 V3-001 VALIDATION SUMMARY")
        print("=" * 50)
        print(f"Overall Status: {self.validation_results['overall_status'].upper()}")
        print(f"Success Rate: {success_rate:.1f}%")
        print(f"Components: {successful_components}/{total_components}")
        print("\nComponent Status:")

        for name, status in components.items():
            status_icon = (
                "✅" if status.get("status") in ["connected", "deployed", "operational"] else "❌"
            )
            print(f"  {status_icon} {name}: {status.get('status', 'unknown')}")

        if self.validation_results["overall_status"] == "success":
            print("\n🎉 V3-001: Cloud Infrastructure Setup - VALIDATION SUCCESSFUL!")
        else:
            print(
                f"\n⚠️  V3-001: Cloud Infrastructure Setup - VALIDATION {self.validation_results['overall_status'].upper()}"
            )


async def main():
    """Main validation function."""
    validator = DeploymentValidator()
    await validator.validate_all_components()


if __name__ == "__main__":
    asyncio.run(main())
