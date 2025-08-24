#!/usr/bin/env python3
"""
Parallel Processor
=================

Handles parallel processing of repository scanning operations.
Manages ThreadPoolExecutor and concurrent scanning.

Author: Agent-1 (Performance & Health Systems)
License: MIT
"""

import logging

from src.utils.stability_improvements import stability_manager, safe_import
from typing import List, Callable, Any
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)


class ParallelProcessor:
    """Handles parallel processing of repository operations"""
    
    def __init__(self, max_workers: int = 4):
        """Initialize the parallel processor"""
        self.max_workers = max_workers
        logger.info(f"Parallel Processor initialized with {max_workers} workers")

    def process_repositories(self, repository_paths: List[str], 
                           scan_function: Callable[[str], Any]) -> List[Any]:
        """Process multiple repositories in parallel"""
        try:
            results = []
            
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                future_to_path = {
                    executor.submit(scan_function, path): path
                    for path in repository_paths
                }

                for future in future_to_path:
                    try:
                        result = future.result()
                        if result:
                            results.append(result)
                    except Exception as e:
                        path = future_to_path[future]
                        logger.error(f"Failed to process repository {path}: {e}")

            logger.info(f"Completed processing {len(results)} repositories")
            return results

        except Exception as e:
            logger.error(f"Failed to process repositories in parallel: {e}")
            return []

    def set_max_workers(self, max_workers: int):
        """Update the maximum number of workers"""
        self.max_workers = max_workers
        logger.info(f"Updated max workers to {max_workers}")

    def get_worker_info(self) -> dict:
        """Get information about the parallel processor"""
        return {
            "max_workers": self.max_workers,
            "status": "active"
        }

