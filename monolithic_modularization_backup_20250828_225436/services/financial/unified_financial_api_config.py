from dataclasses import dataclass
from pathlib import Path


@dataclass
class UnifiedFinancialAPIConfig:
    """Configuration for UnifiedFinancialAPI paths."""

    data_dir: Path = Path("unified_financial_api")

    def __post_init__(self) -> None:
        self.data_dir = Path(self.data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.agents_file = self.data_dir / "registered_agents.json"
        self.requests_file = self.data_dir / "request_history.json"
        self.performance_file = self.data_dir / "performance_metrics.json"
