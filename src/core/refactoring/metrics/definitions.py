"""Metric definitions for refactoring processes."""



@dataclass
class RefactoringMetrics:
    """Refactoring performance metrics."""

    total_files_processed: int = 0
    total_lines_reduced: int = 0
    total_time_saved: float = 0.0
    duplication_eliminated: float = 0.0
    architecture_improvements: int = 0
    quality_score: float = 0.0
    efficiency_gain: float = 0.0
