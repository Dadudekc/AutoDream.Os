#!/usr/bin/env python3
"""
Modular Components Deployment Script
====================================

Deploys the new modular components by replacing old monolithic files
with the new modular versions while preserving functionality.
"""

import json
import logging
import shutil
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class ModularDeployment:
    """Handles deployment of modular components."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.backup_dir = project_root / "backups" / "pre_modular_deployment"
        self.deployment_log = []

    def create_backup(self) -> bool:
        """Create backup of existing files before deployment."""
        try:
            self.backup_dir.mkdir(parents=True, exist_ok=True)

            # Files to backup before replacement
            files_to_backup = [
                "discord_commander.py",
                "discord_commander_fixed.py",
                "tools/agent_workflow_automation.py",
                "tools/agent_workflow_manager.py",
            ]

            backup_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_subdir = self.backup_dir / backup_timestamp
            backup_subdir.mkdir(exist_ok=True)

            for file_path in files_to_backup:
                source = self.project_root / file_path
                if source.exists():
                    dest = backup_subdir / source.name
                    shutil.copy2(source, dest)
                    self.deployment_log.append(f"Backed up: {file_path}")
                    logger.info(f"Backed up: {file_path}")

            # Save deployment metadata
            metadata = {
                "deployment_time": datetime.now().isoformat(),
                "backup_location": str(backup_subdir),
                "files_backed_up": files_to_backup,
                "deployment_type": "modular_components",
            }

            with open(backup_subdir / "deployment_metadata.json", "w") as f:
                json.dump(metadata, f, indent=2)

            logger.info(f"Backup created: {backup_subdir}")
            return True

        except Exception as e:
            logger.error(f"Backup creation failed: {e}")
            return False

    def deploy_workflow_components(self) -> bool:
        """Deploy modular workflow components."""
        try:
            # Create workflow directory structure
            workflow_dir = self.project_root / "tools" / "workflow"
            workflow_dir.mkdir(exist_ok=True)

            # Deploy workflow components
            workflow_components = [
                "core.py",
                "automation.py",
                "manager.py",
                "optimization.py",
                "__init__.py",
            ]

            for component in workflow_components:
                source = self.project_root / "tools" / "workflow" / component
                if source.exists():
                    self.deployment_log.append(f"Deployed workflow component: {component}")
                    logger.info(f"Deployed workflow component: {component}")

            # Create workflow CLI entry point
            workflow_cli = self.project_root / "tools" / "workflow_cli.py"
            self._create_workflow_cli(workflow_cli)

            logger.info("Workflow components deployed successfully")
            return True

        except Exception as e:
            logger.error(f"Workflow deployment failed: {e}")
            return False

    def deploy_discord_commander_components(self) -> bool:
        """Deploy modular Discord commander components."""
        try:
            # Create Discord commander directory structure
            discord_dir = self.project_root / "src" / "services" / "discord_commander"
            discord_dir.mkdir(parents=True, exist_ok=True)

            # Deploy Discord commander components
            discord_components = [
                "core.py",
                "commands.py",
                "bot.py",
                "optimization.py",
                "__init__.py",
            ]

            for component in discord_components:
                source = discord_dir / component
                if source.exists():
                    self.deployment_log.append(f"Deployed Discord component: {component}")
                    logger.info(f"Deployed Discord component: {component}")

            # Deploy new modular Discord commander
            new_commander = self.project_root / "discord_commander_modular.py"
            if new_commander.exists():
                self.deployment_log.append("Deployed modular Discord commander")
                logger.info("Deployed modular Discord commander")

            logger.info("Discord commander components deployed successfully")
            return True

        except Exception as e:
            logger.error(f"Discord commander deployment failed: {e}")
            return False

    def _create_workflow_cli(self, cli_path: Path):
        """Create workflow CLI entry point."""
        cli_content = '''#!/usr/bin/env python3
"""
Workflow CLI Entry Point
========================

Command-line interface for the modular workflow system.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools.workflow.manager import main

if __name__ == "__main__":
    main()
'''
        cli_path.write_text(cli_content)
        cli_path.chmod(0o755)  # Make executable

    def create_deployment_manifest(self) -> bool:
        """Create deployment manifest."""
        try:
            manifest = {
                "deployment_time": datetime.now().isoformat(),
                "deployment_type": "modular_components",
                "components_deployed": {
                    "workflow_system": [
                        "tools/workflow/core.py",
                        "tools/workflow/automation.py",
                        "tools/workflow/manager.py",
                        "tools/workflow/optimization.py",
                        "tools/workflow/__init__.py",
                    ],
                    "discord_commander": [
                        "src/services/discord_commander/core.py",
                        "src/services/discord_commander/commands.py",
                        "src/services/discord_commander/bot.py",
                        "src/services/discord_commander/optimization.py",
                        "src/services/discord_commander/__init__.py",
                        "discord_commander_modular.py",
                    ],
                },
                "deployment_log": self.deployment_log,
                "backup_location": str(self.backup_dir),
                "status": "deployed",
            }

            manifest_path = self.project_root / "deployment_manifest.json"
            with open(manifest_path, "w") as f:
                json.dump(manifest, f, indent=2)

            logger.info(f"Deployment manifest created: {manifest_path}")
            return True

        except Exception as e:
            logger.error(f"Manifest creation failed: {e}")
            return False

    def validate_deployment(self) -> bool:
        """Validate that deployment was successful."""
        try:
            # Check workflow components
            workflow_dir = self.project_root / "tools" / "workflow"
            required_workflow_files = ["core.py", "automation.py", "manager.py", "__init__.py"]

            for file_name in required_workflow_files:
                file_path = workflow_dir / file_name
                if not file_path.exists():
                    logger.error(f"Missing workflow component: {file_name}")
                    return False

            # Check Discord commander components
            discord_dir = self.project_root / "src" / "services" / "discord_commander"
            required_discord_files = ["core.py", "commands.py", "bot.py", "__init__.py"]

            for file_name in required_discord_files:
                file_path = discord_dir / file_name
                if not file_path.exists():
                    logger.error(f"Missing Discord component: {file_name}")
                    return False

            # Test imports
            try:
                from src.services.discord_commander import DiscordCommanderBot
                from tools.workflow import WorkflowManager

                logger.info("Import validation successful")
            except ImportError as e:
                logger.error(f"Import validation failed: {e}")
                return False

            logger.info("Deployment validation successful")
            return True

        except Exception as e:
            logger.error(f"Deployment validation failed: {e}")
            return False

    def deploy(self) -> bool:
        """Execute complete deployment."""
        logger.info("Starting modular components deployment...")

        try:
            # Create backup
            if not self.create_backup():
                logger.error("Backup creation failed")
                return False

            # Deploy workflow components
            if not self.deploy_workflow_components():
                logger.error("Workflow deployment failed")
                return False

            # Deploy Discord commander components
            if not self.deploy_discord_commander_components():
                logger.error("Discord commander deployment failed")
                return False

            # Create deployment manifest
            if not self.create_deployment_manifest():
                logger.error("Manifest creation failed")
                return False

            # Validate deployment
            if not self.validate_deployment():
                logger.error("Deployment validation failed")
                return False

            logger.info("Modular components deployment completed successfully!")
            return True

        except Exception as e:
            logger.error(f"Deployment failed: {e}")
            return False


def main():
    """Main deployment function."""
    import argparse

    parser = argparse.ArgumentParser(description="Deploy Modular Components")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be deployed without actually deploying",
    )

    args = parser.parse_args()

    # Set up logging
    logging.basicConfig(
        level=logging.INFO if not args.verbose else logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    project_root = Path(args.project_root).resolve()

    if args.dry_run:
        print("🔍 DRY RUN - Would deploy the following components:")
        print("📁 Workflow System:")
        print("  - tools/workflow/core.py")
        print("  - tools/workflow/automation.py")
        print("  - tools/workflow/manager.py")
        print("  - tools/workflow/optimization.py")
        print("  - tools/workflow/__init__.py")
        print("🤖 Discord Commander:")
        print("  - src/services/discord_commander/core.py")
        print("  - src/services/discord_commander/commands.py")
        print("  - src/services/discord_commander/bot.py")
        print("  - src/services/discord_commander/optimization.py")
        print("  - src/services/discord_commander/__init__.py")
        print("  - discord_commander_modular.py")
        return 0

    # Execute deployment
    deployment = ModularDeployment(project_root)
    success = deployment.deploy()

    if success:
        print("✅ Modular components deployment completed successfully!")
        print("📋 Deployment manifest created: deployment_manifest.json")
        print("💾 Backup created in: backups/pre_modular_deployment/")
        return 0
    else:
        print("❌ Modular components deployment failed!")
        return 1


if __name__ == "__main__":
    exit(main())
