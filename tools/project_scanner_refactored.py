"""Refactored Project Scanner - V2 Compliant Version

This is a modular, V2-compliant version of the project scanner that breaks down
the original 1,154-line file into focused, single-responsibility modules.

Author: Agent-1 (System Recovery Specialist)
V2 Compliance: < 300 lines, modular design, single responsibility
"""

import json
import logging
import os
import queue
import threading
from pathlib import Path
from typing import Any

from .scanner.file_processor import FileProcessor
from .scanner.language_analyzer import LanguageAnalyzer

logger = logging.getLogger(__name__)

# Cache file configuration
CACHE_FILE = "dependency_cache.json"


class ProjectScanner:
    """Main project scanner class - V2 compliant version."""

    def __init__(self, project_root: str = "."):
        """Initialize the project scanner."""
        self.project_root = Path(project_root).resolve()
        self.language_analyzer = LanguageAnalyzer()
        self.file_processor = FileProcessor(self.language_analyzer)
        self.results = {
            'files': [],
            'statistics': {},
            'analysis': {}
        }

    def scan_project(self) -> dict[str, Any]:
        """
        Scan the entire project and return analysis results.

        Returns:
            Dictionary containing project analysis results
        """
        logger.info(f"Starting project scan of {self.project_root}")
        
        # Find all files to process
        files_to_process = self._find_files()
        logger.info(f"Found {len(files_to_process)} files to process")

        # Process files
        processed_files = []
        for file_path in files_to_process:
            if not self.file_processor.should_skip_file(file_path):
                file_data = self.file_processor.process_file(file_path)
                if file_data:
                    processed_files.append(file_data)

        # Generate statistics
        statistics = self._generate_statistics(processed_files)
        
        # Store results
        self.results = {
            'files': processed_files,
            'statistics': statistics,
            'analysis': self._analyze_project(processed_files)
        }

        logger.info(f"Project scan completed. Processed {len(processed_files)} files")
        return self.results

    def _find_files(self) -> list[Path]:
        """Find all relevant files in the project."""
        files = []
        
        # Common source file extensions
        source_extensions = {
            '.py', '.js', '.ts', '.tsx', '.jsx', '.rs', '.go', '.java',
            '.cpp', '.c', '.h', '.hpp', '.json', '.yaml', '.yml', '.toml',
            '.md', '.txt', '.html', '.css', '.scss', '.sql', '.sh', '.bat', '.ps1'
        }

        for file_path in self.project_root.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in source_extensions:
                files.append(file_path)

        return files

    def _generate_statistics(self, files: list[dict[str, Any]]) -> dict[str, Any]:
        """Generate project statistics from processed files."""
        if not files:
            return {}

        total_lines = sum(f.get('lines', 0) for f in files)
        total_size = sum(f.get('size', 0) for f in files)
        
        # Language distribution
        languages = {}
        for file_data in files:
            lang = file_data.get('language', 'unknown')
            languages[lang] = languages.get(lang, 0) + 1

        # File type distribution
        file_types = {}
        for file_data in files:
            file_path = Path(file_data['path'])
            file_type = self.file_processor.get_file_type(file_path)
            file_types[file_type] = file_types.get(file_type, 0) + 1

        return {
            'total_files': len(files),
            'total_lines': total_lines,
            'total_size_bytes': total_size,
            'languages': languages,
            'file_types': file_types,
            'average_lines_per_file': total_lines / len(files) if files else 0,
        }

    def _analyze_project(self, files: list[dict[str, Any]]) -> dict[str, Any]:
        """Perform project-level analysis."""
        analysis = {
            'complexity': {
                'total_functions': 0,
                'total_classes': 0,
                'total_routes': 0,
                'average_complexity': 0
            },
            'architecture': {
                'has_web_framework': False,
                'has_api_routes': False,
                'has_tests': False
            }
        }

        if not files:
            return analysis

        # Calculate complexity metrics
        total_functions = sum(len(f.get('functions', [])) for f in files)
        total_classes = sum(len(f.get('classes', {})) for f in files)
        total_routes = sum(len(f.get('routes', [])) for f in files)
        total_complexity = sum(f.get('complexity', 0) for f in files)

        analysis['complexity'] = {
            'total_functions': total_functions,
            'total_classes': total_classes,
            'total_routes': total_routes,
            'average_complexity': total_complexity / len(files) if files else 0
        }

        # Detect architecture patterns
        for file_data in files:
            if file_data.get('routes'):
                analysis['architecture']['has_web_framework'] = True
                analysis['architecture']['has_api_routes'] = True
            
            if 'test' in file_data['path'].lower():
                analysis['architecture']['has_tests'] = True

        return analysis

    def save_results(self, output_file: str = "project_analysis.json") -> None:
        """Save scan results to a JSON file."""
        output_path = self.project_root / output_file
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        logger.info(f"Results saved to {output_path}")

    def load_cache(self) -> dict[str, Any]:
        """Load cached results if available."""
        cache_path = self.project_root / CACHE_FILE
        if cache_path.exists():
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Could not load cache: {e}")
        return {}

    def save_cache(self, data: dict[str, Any]) -> None:
        """Save data to cache file."""
        cache_path = self.project_root / CACHE_FILE
        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            logger.warning(f"Could not save cache: {e}")


def main():
    """Main entry point for the project scanner."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Scan project for code analysis")
    parser.add_argument("--root", default=".", help="Project root directory")
    parser.add_argument("--output", default="project_analysis.json", help="Output file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    
    scanner = ProjectScanner(args.root)
    results = scanner.scan_project()
    scanner.save_results(args.output)
    
    print(f"Project scan completed. Results saved to {args.output}")
    print(f"Processed {results['statistics']['total_files']} files")
    print(f"Total lines: {results['statistics']['total_lines']}")


if __name__ == "__main__":
    main()