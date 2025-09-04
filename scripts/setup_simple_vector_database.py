from ..core.unified_entry_point_system import main
#!/usr/bin/env python3
"""
Simple Vector Database Setup Script

This script initializes a lightweight vector database and indexes all project documentation
for AI agent access using TF-IDF similarity search.
"""

from ..core.unified_import_system import logging

# Add src to path
sys.path.insert(0, str(get_unified_utility().Path(__file__).parent.parent / "src"))


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SimpleDocumentationIndexer:
    """
    Indexes project documentation into the simple vector database.
    """
    
    def __init__(self, vector_db):
        self.vector_db = vector_db
        self.supported_extensions = {'.md', '.txt', '.py', '.js', '.ts', '.json', '.yaml', '.yml'}
    
    def index_directory(self, directory_path: str, recursive: bool = True) -> dict:
        """
        Index all supported files in a directory.
        
        Args:
            directory_path: Path to directory to index
            recursive: Whether to index subdirectories
            
        Returns:
            Dictionary with indexing results
        """
        results = {
            "indexed": 0,
            "failed": 0,
            "skipped": 0,
            "errors": []
        }
        
        directory = get_unified_utility().Path(directory_path)
        if not directory.exists():
            results["errors"].append(f"Directory not found: {directory_path}")
            return results
        
        # Get all files to index
        files = []
        try:
            if recursive:
                for f in directory.rglob('*'):
                    try:
                        if f.is_file() and f.suffix in self.supported_extensions:
                            files.append(f)
                    except (OSError, PermissionError):
                        # Skip corrupted or inaccessible files
                        continue
            else:
                for f in directory.iterdir():
                    try:
                        if f.is_file() and f.suffix in self.supported_extensions:
                            files.append(f)
                    except (OSError, PermissionError):
                        # Skip corrupted or inaccessible files
                        continue
        except Exception as e:
            results["errors"].append(f"Error scanning directory {directory_path}: {e}")
            return results
        
        for file_path in files:
            try:
                # Skip if file is too large (>1MB)
                if file_path.stat().st_size > 1024 * 1024:
                    results["skipped"] += 1
                    continue
                
                # Read file content
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                
                # Prepare metadata
                metadata = {
                    "file_size": file_path.stat().st_size,
                    "last_modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                    "directory": str(file_path.parent)
                }
                
                # Add to vector database
                if self.vector_db.add_document(str(file_path), content, metadata):
                    results["indexed"] += 1
                else:
                    results["failed"] += 1
                    
            except Exception as e:
                results["failed"] += 1
                results["errors"].append(f"Error indexing {file_path}: {e}")
        
        return results


if __name__ == "__main__":
    main()
