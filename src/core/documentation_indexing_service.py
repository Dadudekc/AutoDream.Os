"""Documentation Indexing Service.

Handles indexing of project documentation into the vector database.
"""

logger = logging.getLogger(__name__)


class DocumentationIndexingService:
    """Service for indexing project documentation."""

    def __init__(self, vector_db, indexer):
        self.vector_db = vector_db
        self.indexer = indexer
        self.supported_extensions = {
            ".md",
            ".txt",
            ".py",
            ".js",
            ".ts",
            ".json",
            ".yaml",
            ".yml",
        }

    def index_project_documentation(self, project_root: str = ".") -> Dict[str, Any]:
        """Index all project documentation.

        Args:
            project_root: Root directory of the project

        Returns:
            Dictionary with indexing results
        """
        try:
            # Define directories to index
            directories_to_index = ["docs", "src", "scripts", "tests"]

            total_results = {"indexed": 0, "failed": 0, "skipped": 0, "errors": []}

            for directory in directories_to_index:
                dir_path = get_unified_utility().Path(project_root) / directory
                if dir_path.exists():
                    results = self.indexer.index_directory(str(dir_path))

                    # Merge results
                    total_results["indexed"] += results["indexed"]
                    total_results["failed"] += results["failed"]
                    total_results["skipped"] += results["skipped"]
                    total_results["errors"].extend(results["errors"])

                    get_logger(__name__).info(
                        f"Indexed {directory}: {results['indexed']} files"
                    )

            # Also index key files in root
            key_files = [
                "README.md",
                "AGENTS.md",
                "QUICK_START.md",
                "V2_COMPLIANCE_README.md",
                "CHANGELOG.md",
            ]

            for file_name in key_files:
                file_path = get_unified_utility().Path(project_root) / file_name
                if file_path.exists():
                    results = self.indexer.index_specific_files([str(file_path)])
                    total_results["indexed"] += results["indexed"]
                    total_results["failed"] += results["failed"]
                    total_results["errors"].extend(results["errors"])

            get_logger(__name__).info(f"Total indexing results: {total_results}")
            return total_results

        except Exception as e:
            get_logger(__name__).error(f"Error indexing project documentation: {e}")
            return {"error": str(e)}

    def index_specific_files(self, file_paths: List[str]) -> Dict[str, Any]:
        """Index specific files.

        Args:
            file_paths: List of file paths to index

        Returns:
            Dictionary with indexing results
        """
        results = {"indexed": 0, "failed": 0, "errors": []}

        for file_path in file_paths:
            try:
                path = get_unified_utility().Path(file_path)
                if not path.exists():
                    results["errors"].append(f"File not found: {file_path}")
                    results["failed"] += 1
                    continue

                if path.suffix not in self.supported_extensions:
                    results["errors"].append(f"Unsupported file type: {file_path}")
                    results["failed"] += 1
                    continue

                # Read file content
                content = path.read_text(encoding="utf-8", errors="ignore")

                # Prepare metadata
                metadata = {
                    "file_size": path.stat().st_size,
                    "last_modified": (
                        datetime.fromtimestamp(path.stat().st_mtime).isoformat()
                    ),
                    "directory": str(path.parent),
                }

                # Add to vector database
                if self.vector_db.add_document(str(path), content, metadata):
                    results["indexed"] += 1
                else:
                    results["failed"] += 1

            except Exception as e:
                results["failed"] += 1
                results["errors"].append(f"Error indexing {file_path}: {e}")

        return results

    def index_directory(
        self, directory_path: str, recursive: bool = True
    ) -> Dict[str, Any]:
        """Index all supported files in a directory.

        Args:
            directory_path: Path to directory to index
            recursive: Whether to index subdirectories

        Returns:
            Dictionary with indexing results
        """
        return self.indexer.index_directory(directory_path, recursive)

    def reindex_file(self, file_path: str) -> bool:
        """Re-index a specific file (remove and re-add).

        Args:
            file_path: Path to the file to re-index

        Returns:
            True if successful, False otherwise
        """
        try:
            # Remove existing document
            self.vector_db.delete_document(file_path)

            # Re-index the file
            results = self.index_specific_files([file_path])

            if results["indexed"] > 0:
                get_logger(__name__).info(f"Re-indexed file: {file_path}")
                return True
            else:
                get_logger(__name__).error(f"Failed to re-index file: {file_path}")
                return False

        except Exception as e:
            get_logger(__name__).error(f"Error re-indexing file {file_path}: {e}")
            return False

    def get_indexing_status(self) -> Dict[str, Any]:
        """Get current indexing status.

        Returns:
            Dictionary with indexing statistics
        """
        try:
            stats = self.vector_db.get_collection_stats()
            return {
                "collection_stats": stats,
                "supported_extensions": list(self.supported_extensions),
                "last_indexing_attempt": datetime.now().isoformat(),
            }
        except Exception as e:
            get_logger(__name__).error(f"Error getting indexing status: {e}")
            return {"error": str(e)}
