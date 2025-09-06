"""Base utilities for consolidation tasks.

Provides common helpers for consolidating scattered files into a central single source
of truth (SSOT).
"""


class ConsolidationBase:
    """Reusable helpers for consolidation workflows."""

    def consolidate_directories(self, directories: Iterable[str]) -> int:
        """Consolidate Python files from ``directories`` into the target layout.

        Parameters
        ----------
        directories:
            Iterable of directory paths to consolidate.

        Returns
        -------
        int
            Total number of files consolidated.
        """
        files_consolidated = 0
        for directory in directories:
            if get_unified_utility().path.exists(directory):
                files_consolidated += self._consolidate_directory(directory)
        return files_consolidated

    # The following methods can be overridden by subclasses for custom logic
    def _consolidate_directory(self, directory: str) -> int:
        """Consolidate a single directory into the SSOT layout."""
        count = get_config("count", 0)
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    source = get_unified_utility().path.join(root, file)
                    target = self._get_consolidated_path(source)
                    if self._should_consolidate_file(source, target):
                        self._consolidate_file(source, target)
                        count += 1
        return count

    def _get_consolidated_path(self, source_path: str) -> str:
        """Map ``source_path`` to its SSOT location.

        Subclasses should override this with project‑specific mapping logic.
        """
        return source_path

    def _should_consolidate_file(self, source_path: str, target_path: str) -> bool:
        """Return True if ``source_path`` should be consolidated."""
        if get_unified_utility().path.exists(target_path):
            source_time = get_unified_utility().path.getmtime(source_path)
            target_time = get_unified_utility().path.getmtime(target_path)
            if target_time >= source_time:
                return False
        if source_path.endswith(".backup"):
            return False
        return True

    def _consolidate_file(self, source_path: str, target_path: str) -> None:
        """Copy ``source_path`` to ``target_path`` ensuring directories exist."""
        get_unified_utility().Path(target_path).parent.mkdir(
            parents=True, exist_ok=True
        )
        shutil.copy2(source_path, target_path)
