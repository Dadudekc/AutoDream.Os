from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import List

from .agents.agent1 import Agent1Contracts
from .agents.agent2 import Agent2Contracts
from .agents.agent3 import Agent3Contracts
from .agents.agent4 import Agent4Contracts
from .models import TaskContract

logger = logging.getLogger(__name__)


class CaptainTaskDistributor:
    """Distribute captain task contracts to agents."""

    def __init__(self, output_dir: Path | None = None) -> None:
        self.output_dir = output_dir or Path("logs")
        self.output_dir.mkdir(exist_ok=True)
        self.tasks_distributed = 0

    def create_all_contracts(self) -> List[TaskContract]:
        """Collect contracts for all agents."""
        contracts: List[TaskContract] = []
        contracts.extend(Agent1Contracts.build())
        contracts.extend(Agent2Contracts.build())
        contracts.extend(Agent3Contracts.build())
        contracts.extend(Agent4Contracts.build())
        return contracts

    def save_contracts(self) -> bool:
        """Save all generated contracts to files."""
        logger.info("🚀 Starting comprehensive task contract creation")
        contracts = self.create_all_contracts()
        success_count = 0
        for contract in contracts:
            try:
                agent_dir = self.output_dir / f"contracts_{contract.agent.lower().replace('-', '_')}"
                agent_dir.mkdir(exist_ok=True)
                contract_file = agent_dir / f"{contract.task_id.lower().replace(' ', '_')}.md"
                contract_file.write_text(contract.content, encoding="utf-8")
                success_count += 1
                self.tasks_distributed += 1
                logger.info(
                    "✅ %s contract saved for %s: %s",
                    contract.task_id,
                    contract.agent,
                    contract_file,
                )
            except Exception as exc:  # pylint: disable=broad-except
                logger.error("❌ Error saving %s contract for %s: %s", contract.task_id, contract.agent, exc)
        self._create_master_summary(contracts)
        logger.info("📊 Contract creation complete: %s/%s successful", success_count, len(contracts))
        return success_count == len(contracts)

    def _create_master_summary(self, contracts: List[TaskContract]) -> None:
        """Create a simple summary markdown file."""
        summary_lines = [
            "# 🎯 CAPTAIN TASK DISTRIBUTION SUMMARY",
            f"Generated: {datetime.now().isoformat()}",
            "",
            "## Tasks by Agent",
        ]
        by_agent: dict[str, list[str]] = {}
        for contract in contracts:
            by_agent.setdefault(contract.agent, []).append(contract.task_id)
        for agent, tasks in by_agent.items():
            summary_lines.append(f"### {agent}")
            for task in tasks:
                summary_lines.append(f"- {task}")
            summary_lines.append("")
        summary_file = self.output_dir / "CAPTAIN_TASK_DISTRIBUTION_SUMMARY.md"
        summary_file.write_text("\n".join(summary_lines), encoding="utf-8")
        logger.info("📊 Master summary created: %s", summary_file)

    def get_distribution_summary(self) -> dict:
        """Return simple distribution stats."""
        # Count distributed tasks by finding contract files on disk
        distributed_files = list(self.output_dir.glob("contracts_*/*.md"))
        tasks_distributed = len(distributed_files)

        # Dynamically determine the total number of tasks
        total_tasks = len(self.create_all_contracts())

        # Calculate distribution rate, handling division by zero
        distribution_rate = (tasks_distributed / total_tasks) * 100 if total_tasks > 0 else 0.0

        return {
            "total_tasks": total_tasks,
            "tasks_distributed": tasks_distributed,
            "distribution_rate": f"{distribution_rate:.1f}%",
            "agents_covered": ["Agent-1", "Agent-2", "Agent-3", "Agent-4"],
            "output_directory": str(self.output_dir),
        }
