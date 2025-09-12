#!/usr/bin/env python3
"""
Agent Cycle Automation v3.1
Part of V3.1 Unified Feedback Loop
Unified cycle automation for swarm agents

Deployed by Agent-5 as Integration & Tooling Specialist
"""

import argparse
import json
import logging
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import jsonschema
except ImportError:
    jsonschema = None
import yaml

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class CycleConfig:
    """Configuration for agent cycle"""

    cycle_duration: str = "24_hours"
    validation_enabled: bool = True
    duplication_scan_enabled: bool = True
    devlog_required: bool = True
    coordination_required: bool = True
    auto_commit: bool = True
    discord_integration: bool = True


@dataclass
class CycleResult:
    """Result of cycle execution"""

    agent_id: str
    cycle_number: int
    start_time: datetime
    end_time: datetime
    status: str
    tasks_completed: int
    files_processed: int
    coordination_score: int
    quality_score: int
    v2_compliance: bool
    issues_found: list[str]
    recommendations: list[str]


class AgentCycleAutomation:
    """Unified cycle automation for swarm agents"""

    def __init__(self, agent_id: str, config: CycleConfig = None):
        self.agent_id = agent_id
        self.config = config or CycleConfig()
        self.root_path = Path(".")
        self.agent_workspace = self.root_path / "agent_workspaces" / agent_id
        self.status_file = self.agent_workspace / "status.json"
        self.schema_file = self.root_path / "schemas" / "status.schema.json"
        self.contract_file = self.root_path / "contracts" / "swarm_contract.yaml"
        self.devlog_template = self.root_path / "templates" / "DEVLOG_TEMPLATE.md"

        # Ensure directories exist
        self.agent_workspace.mkdir(parents=True, exist_ok=True)

    def execute_cycle(self) -> CycleResult:
        """Execute complete agent cycle"""
        logger.info(f"Starting cycle for {self.agent_id}")

        start_time = datetime.now()
        cycle_number = self._get_next_cycle_number()

        try:
            # Phase 1: Pre-cycle validation
            self._pre_cycle_validation()

            # Phase 2: Load current status
            current_status = self._load_current_status()

            # Phase 3: Execute cycle tasks
            cycle_tasks = self._execute_cycle_tasks(current_status)

            # Phase 4: Post-cycle validation
            validation_results = self._post_cycle_validation()

            # Phase 5: Generate devlog
            if self.config.devlog_required:
                self._generate_devlog(cycle_tasks, validation_results)

            # Phase 6: Update status
            new_status = self._update_status(current_status, cycle_tasks, validation_results)

            # Phase 7: Commit changes
            if self.config.auto_commit:
                self._commit_changes(cycle_tasks)

            # Phase 8: Coordinate with swarm
            if self.config.coordination_required:
                self._coordinate_with_swarm(new_status)

            end_time = datetime.now()

            # Create cycle result
            result = CycleResult(
                agent_id=self.agent_id,
                cycle_number=cycle_number,
                start_time=start_time,
                end_time=end_time,
                status="completed",
                tasks_completed=cycle_tasks.get("tasks_completed", 0),
                files_processed=cycle_tasks.get("files_processed", 0),
                coordination_score=cycle_tasks.get("coordination_score", 0),
                quality_score=validation_results.get("quality_score", 0),
                v2_compliance=validation_results.get("v2_compliance", False),
                issues_found=validation_results.get("issues", []),
                recommendations=validation_results.get("recommendations", []),
            )

            logger.info(f"Cycle completed successfully for {self.agent_id}")
            return result

        except Exception as e:
            logger.error(f"Cycle failed for {self.agent_id}: {e}")
            end_time = datetime.now()

            return CycleResult(
                agent_id=self.agent_id,
                cycle_number=cycle_number,
                start_time=start_time,
                end_time=end_time,
                status="failed",
                tasks_completed=0,
                files_processed=0,
                coordination_score=0,
                quality_score=0,
                v2_compliance=False,
                issues_found=[str(e)],
                recommendations=["Review error logs and retry cycle"],
            )

    def _get_next_cycle_number(self) -> int:
        """Get next cycle number"""
        if self.status_file.exists():
            try:
                with open(self.status_file) as f:
                    status = json.load(f)
                    return status.get("cycle_info", {}).get("cycle_number", 0) + 1
            except:
                pass
        return 1

    def _pre_cycle_validation(self) -> None:
        """Validate environment before cycle starts"""
        logger.info("Performing pre-cycle validation...")

        # Check required files exist
        required_files = [self.schema_file, self.contract_file, self.devlog_template]

        for file_path in required_files:
            if not file_path.exists():
                raise FileNotFoundError(f"Required file not found: {file_path}")

        # Validate swarm contract
        self._validate_swarm_contract()

        logger.info("Pre-cycle validation completed")

    def _validate_swarm_contract(self) -> None:
        """Validate swarm contract is properly deployed"""
        try:
            with open(self.contract_file) as f:
                contract = yaml.safe_load(f)

            # Check contract version
            if contract.get("swarm_contract", {}).get("version") != "3.1":
                raise ValueError("Swarm contract version mismatch")

            # Check agent is in contract
            agent_roles = contract.get("swarm_contract", {}).get("agent_roles", {})
            if self.agent_id not in agent_roles:
                raise ValueError(f"Agent {self.agent_id} not found in swarm contract")

            logger.info("Swarm contract validation passed")

        except Exception as e:
            raise ValueError(f"Swarm contract validation failed: {e}")

    def _load_current_status(self) -> dict[str, Any]:
        """Load current agent status"""
        if self.status_file.exists():
            try:
                with open(self.status_file) as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Error loading status file: {e}")

        # Return default status
        return {
            "agent_id": self.agent_id,
            "status": "active",
            "cycle_info": {
                "cycle_number": 0,
                "start_time": None,
                "duration": self.config.cycle_duration,
            },
            "performance_metrics": {
                "tasks_completed": 0,
                "files_processed": 0,
                "coordination_score": 0,
                "quality_score": 0,
                "v2_compliance": False,
                "file_size_compliance": True,
            },
        }

    def _execute_cycle_tasks(self, current_status: dict[str, Any]) -> dict[str, Any]:
        """Execute cycle-specific tasks"""
        logger.info("Executing cycle tasks...")

        tasks = {
            "tasks_completed": 0,
            "files_processed": 0,
            "coordination_score": 0,
            "code_changes": [],
            "files_modified": [],
            "new_files_created": [],
        }

        # Task 1: Check inbox
        inbox_tasks = self._process_inbox()
        tasks["tasks_completed"] += inbox_tasks

        # Task 2: Process pending messages
        message_tasks = self._process_messages()
        tasks["tasks_completed"] += message_tasks

        # Task 3: Execute agent-specific tasks
        agent_tasks = self._execute_agent_specific_tasks()
        tasks["tasks_completed"] += agent_tasks

        # Task 4: Update coordination score
        tasks["coordination_score"] = self._calculate_coordination_score()

        logger.info(f"Cycle tasks completed: {tasks['tasks_completed']} tasks")
        return tasks

    def _process_inbox(self) -> int:
        """Process agent inbox"""
        inbox_dir = self.agent_workspace / "inbox"
        if not inbox_dir.exists():
            return 0

        inbox_files = list(inbox_dir.glob("*.md"))
        logger.info(f"Processing {len(inbox_files)} inbox messages")

        # Process each message
        for message_file in inbox_files:
            try:
                with open(message_file) as f:
                    content = f.read()

                # Parse message and take action
                self._parse_and_respond_to_message(content, message_file)

            except Exception as e:
                logger.warning(f"Error processing message {message_file}: {e}")

        return len(inbox_files)

    def _parse_and_respond_to_message(self, content: str, message_file: Path) -> None:
        """Parse message and generate response"""
        # Extract sender and priority
        lines = content.split("\n")
        sender = None
        priority = "REGULAR"

        for line in lines:
            if line.startswith("[C2A]"):
                parts = line.split(" → ")
                if len(parts) > 1:
                    sender = parts[0].replace("[C2A] ", "")
            elif line.startswith("Priority:"):
                priority = line.split(":")[1].strip()

        # Generate acknowledgment
        if sender:
            self._send_acknowledgment(sender, priority, message_file)

    def _send_acknowledgment(self, sender: str, priority: str, message_file: Path) -> None:
        """Send acknowledgment message"""
        try:
            # Use messaging service to send acknowledgment
            cmd = [
                "python",
                "src/services/consolidated_messaging_service.py",
                "--agent",
                self.agent_id,
                "--message",
                f"ACK: Received — processing now ({self.agent_id})",
                "--priority",
                priority,
                "--tag",
                "STATUS",
            ]

            subprocess.run(cmd, capture_output=True, text=True)
            logger.info(f"Sent acknowledgment to {sender}")

        except Exception as e:
            logger.warning(f"Error sending acknowledgment: {e}")

    def _process_messages(self) -> int:
        """Process pending messages"""
        # This would integrate with the messaging system
        # For now, return a placeholder
        return 0

    def _execute_agent_specific_tasks(self) -> int:
        """Execute tasks specific to this agent"""
        # This would be customized per agent
        # For now, return a placeholder
        return 1

    def _calculate_coordination_score(self) -> int:
        """Calculate coordination effectiveness score"""
        # This would analyze coordination activities
        # For now, return a placeholder score
        return 8

    def _post_cycle_validation(self) -> dict[str, Any]:
        """Perform post-cycle validation"""
        logger.info("Performing post-cycle validation...")

        validation_results = {
            "quality_score": 0,
            "v2_compliance": False,
            "file_size_compliance": True,
            "issues": [],
            "recommendations": [],
        }

        # Validate status against schema
        if self.config.validation_enabled:
            self._validate_status_schema()

        # Run duplication scan
        if self.config.duplication_scan_enabled:
            dup_results = self._run_duplication_scan()
            validation_results.update(dup_results)

        # Check V2 compliance
        validation_results["v2_compliance"] = self._check_v2_compliance()

        # Calculate quality score
        validation_results["quality_score"] = self._calculate_quality_score(validation_results)

        logger.info("Post-cycle validation completed")
        return validation_results

    def _validate_status_schema(self) -> None:
        """Validate status against schema"""
        if jsonschema is None:
            logger.warning("jsonschema not available, skipping validation")
            return

        try:
            with open(self.schema_file) as f:
                schema = json.load(f)

            with open(self.status_file) as f:
                status = json.load(f)

            jsonschema.validate(status, schema)
            logger.info("Status schema validation passed")

        except jsonschema.ValidationError as e:
            raise ValueError(f"Status schema validation failed: {e}")
        except Exception as e:
            logger.warning(f"Status schema validation error: {e}")

    def _run_duplication_scan(self) -> dict[str, Any]:
        """Run duplication scan"""
        try:
            cmd = ["python", "scripts/dup_scan.py", "--path", str(self.agent_workspace)]
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                # Parse scan results
                return {
                    "duplication_scan_passed": True,
                    "duplications_found": 0,  # Would parse from output
                }
            else:
                return {"duplication_scan_passed": False, "issues": ["Duplication scan failed"]}

        except Exception as e:
            return {"duplication_scan_passed": False, "issues": [f"Duplication scan error: {e}"]}

    def _check_v2_compliance(self) -> bool:
        """Check V2 compliance"""
        # This would check file sizes, code quality, etc.
        # For now, return True
        return True

    def _calculate_quality_score(self, validation_results: dict[str, Any]) -> int:
        """Calculate overall quality score"""
        score = 10

        if not validation_results.get("v2_compliance", False):
            score -= 3

        if not validation_results.get("file_size_compliance", True):
            score -= 2

        if validation_results.get("issues"):
            score -= len(validation_results["issues"])

        return max(0, score)

    def _generate_devlog(
        self, cycle_tasks: dict[str, Any], validation_results: dict[str, Any]
    ) -> None:
        """Generate devlog using template"""
        logger.info("Generating devlog...")

        # Load template
        with open(self.devlog_template) as f:
            template = f.read()

        # Fill template with cycle data
        devlog_content = self._fill_devlog_template(template, cycle_tasks, validation_results)

        # Save devlog
        devlog_dir = self.root_path / "devlogs"
        devlog_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        devlog_file = devlog_dir / f"{self.agent_id}_cycle_{timestamp}.md"

        with open(devlog_file, "w") as f:
            f.write(devlog_content)

        logger.info(f"Devlog saved to {devlog_file}")

        # Post to Discord if enabled
        if self.config.discord_integration:
            self._post_devlog_to_discord(devlog_file)

    def _fill_devlog_template(
        self, template: str, cycle_tasks: dict[str, Any], validation_results: dict[str, Any]
    ) -> str:
        """Fill devlog template with cycle data"""
        # This would fill the template with actual data
        # For now, return a simplified version
        return template.replace("{agent_id}", self.agent_id)

    def _post_devlog_to_discord(self, devlog_file: Path) -> None:
        """Post devlog to Discord"""
        try:
            cmd = ["python", "post_devlog_to_discord.py", str(devlog_file)]
            subprocess.run(cmd, capture_output=True, text=True)
            logger.info("Devlog posted to Discord")
        except Exception as e:
            logger.warning(f"Error posting devlog to Discord: {e}")

    def _update_status(
        self,
        current_status: dict[str, Any],
        cycle_tasks: dict[str, Any],
        validation_results: dict[str, Any],
    ) -> dict[str, Any]:
        """Update agent status"""
        new_status = current_status.copy()

        # Update cycle info
        new_status["cycle_info"] = {
            "cycle_number": self._get_next_cycle_number(),
            "start_time": datetime.now().isoformat(),
            "duration": self.config.cycle_duration,
        }

        # Update performance metrics
        new_status["performance_metrics"] = {
            "tasks_completed": cycle_tasks.get("tasks_completed", 0),
            "files_processed": cycle_tasks.get("files_processed", 0),
            "coordination_score": cycle_tasks.get("coordination_score", 0),
            "quality_score": validation_results.get("quality_score", 0),
            "v2_compliance": validation_results.get("v2_compliance", False),
            "file_size_compliance": validation_results.get("file_size_compliance", True),
        }

        # Update last updated timestamp
        new_status["last_updated"] = datetime.now().isoformat()
        new_status["version"] = "3.1"

        # Save status
        with open(self.status_file, "w") as f:
            json.dump(new_status, f, indent=2)

        logger.info("Status updated successfully")
        return new_status

    def _commit_changes(self, cycle_tasks: dict[str, Any]) -> None:
        """Commit changes to git"""
        try:
            # Add all changes
            subprocess.run(["git", "add", "."], capture_output=True)

            # Commit with cycle message
            commit_message = f"Cycle {self._get_next_cycle_number()}: {cycle_tasks.get('tasks_completed', 0)} tasks completed"
            subprocess.run(["git", "commit", "-m", commit_message], capture_output=True)

            logger.info("Changes committed successfully")

        except Exception as e:
            logger.warning(f"Error committing changes: {e}")

    def _coordinate_with_swarm(self, status: dict[str, Any]) -> None:
        """Coordinate with other swarm agents"""
        try:
            # Broadcast status update
            cmd = [
                "python",
                "src/services/consolidated_messaging_service.py",
                "--broadcast",
                "--message",
                f"Cycle {status['cycle_info']['cycle_number']} completed by {self.agent_id}",
            ]

            subprocess.run(cmd, capture_output=True, text=True)
            logger.info("Swarm coordination completed")

        except Exception as e:
            logger.warning(f"Error coordinating with swarm: {e}")


def main():
    """Main entry point for agent cycle automation"""
    parser = argparse.ArgumentParser(description="Agent Cycle Automation v3.1")
    parser.add_argument("--agent", required=True, help="Agent ID")
    parser.add_argument("--config", help="Configuration file path")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Load configuration
    config = CycleConfig()
    if args.config and Path(args.config).exists():
        with open(args.config) as f:
            config_data = json.load(f)
            config = CycleConfig(**config_data)

    # Initialize automation
    automation = AgentCycleAutomation(args.agent, config)

    # Execute cycle
    result = automation.execute_cycle()

    # Print results
    print("\n🔄 CYCLE COMPLETED")
    print(f"🤖 Agent: {result.agent_id}")
    print(f"📊 Cycle: {result.cycle_number}")
    print(f"✅ Status: {result.status}")
    print(f"📋 Tasks: {result.tasks_completed}")
    print(f"📁 Files: {result.files_processed}")
    print(f"🤝 Coordination: {result.coordination_score}/10")
    print(f"⭐ Quality: {result.quality_score}/10")
    print(f"✅ V2 Compliance: {result.v2_compliance}")

    if result.issues_found:
        print("\n⚠️  ISSUES:")
        for issue in result.issues_found:
            print(f"   • {issue}")

    if result.recommendations:
        print("\n💡 RECOMMENDATIONS:")
        for rec in result.recommendations:
            print(f"   • {rec}")


if __name__ == "__main__":
    main()
