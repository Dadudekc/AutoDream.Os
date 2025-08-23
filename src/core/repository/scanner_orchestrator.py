#!/usr/bin/env python3
"""
Scanner Orchestrator
====================

Handles core scanning coordination and orchestration.
Keeps the main scanner focused on high-level operations.

Author: Agent-1 (Performance & Health Systems)
License: MIT
"""

import time
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from .discovery_engine import RepositoryDiscoveryEngine
from .technology_detector import TechnologyDetector
from .analysis_engine import RepositoryAnalysisEngine
from .report_generator import RepositoryReportGenerator, RepositoryMetadata

logger = logging.getLogger(__name__)


class ScannerOrchestrator:
    """Handles core scanning coordination and orchestration"""
    
    def __init__(self, discovery_engine: RepositoryDiscoveryEngine,
                 technology_detector: TechnologyDetector,
                 analysis_engine: RepositoryAnalysisEngine,
                 report_generator: RepositoryReportGenerator):
        """Initialize the orchestrator"""
        self.discovery_engine = discovery_engine
        self.technology_detector = technology_detector
        self.analysis_engine = analysis_engine
        self.report_generator = report_generator
        
        logger.info("Scanner Orchestrator initialized")

    def scan_repository(self, repository_path: str, deep_scan: bool = False,
                       scan_cache: Dict[str, Any] = None) -> Optional[RepositoryMetadata]:
        """Perform comprehensive repository scanning"""
        try:
            repo_path = Path(repository_path)
            if not repo_path.exists():
                logger.error(f"Repository path does not exist: {repository_path}")
                return None

            # Check cache first
            cache_key = f"{repository_path}_{deep_scan}"
            if scan_cache and cache_key in scan_cache:
                logger.info(f"Using cached scan results for {repository_path}")
                return scan_cache[cache_key]

            logger.info(f"Scanning repository: {repository_path}")
            start_time = time.time()

            # Create repository metadata
            metadata = RepositoryMetadata(
                repository_id=f"repo_{hash(str(repository_path))}",
                name=repo_path.name,
                path=str(repository_path),
            )

            # Basic repository analysis
            self._analyze_basic_metadata(metadata, repo_path)

            # Technology stack detection
            tech_stack = self.technology_detector.detect_technology_stack(
                repo_path, self.discovery_engine.should_exclude_file
            )
            metadata.technology_stack = {
                "language": tech_stack.language,
                "framework": tech_stack.framework,
                "database": tech_stack.database,
                "confidence": tech_stack.confidence,
            }

            # Comprehensive analysis
            analysis_result = self.analysis_engine.analyze_repository(
                repo_path, self.discovery_engine.should_exclude_file
            )
            
            # Update metadata with analysis results
            metadata.dependencies = analysis_result.dependencies
            metadata.architecture_patterns = analysis_result.architecture_patterns
            metadata.performance_metrics = analysis_result.performance_metrics
            metadata.security_analysis = analysis_result.security_analysis
            metadata.health_score = analysis_result.health_score
            metadata.market_readiness = analysis_result.market_readiness
            metadata.recommendations = analysis_result.recommendations

            # Cache results
            if scan_cache is not None:
                scan_cache[cache_key] = metadata

            # Add to report generator
            self.report_generator.add_repository(metadata)

            # Record scan
            scan_duration = time.time() - start_time
            self.report_generator.record_scan(
                metadata.repository_id, 
                "deep" if deep_scan else "basic", 
                scan_duration
            )

            logger.info(f"Repository scan completed: {repository_path}")
            return metadata

        except Exception as e:
            logger.error(f"Failed to scan repository {repository_path}: {e}")
            return None

    def _analyze_basic_metadata(self, metadata: RepositoryMetadata, repo_path: Path):
        """Analyze basic repository metadata"""
        try:
            # Calculate repository size
            total_size = 0
            file_count = 0
            language_files = {}

            for file_path in repo_path.rglob("*"):
                if file_path.is_file():
                    # Check if file should be excluded
                    if self.discovery_engine.should_exclude_file(file_path):
                        continue

                    # Check file size
                    try:
                        file_size = file_path.stat().st_size
                        total_size += file_size
                        file_count += 1

                        # Count files by extension
                        ext = file_path.suffix.lower()
                        if ext in ['.py', '.js', '.java', '.cpp', '.c', '.cs', '.go', '.rs']:
                            language_files[ext] = language_files.get(ext, 0) + 1
                    except (OSError, PermissionError):
                        continue

            metadata.size_bytes = total_size
            metadata.file_count = file_count
            metadata.language_count = len(language_files)

            # Get last modified time
            try:
                metadata.last_modified = datetime.fromtimestamp(
                    repo_path.stat().st_mtime
                )
            except (OSError, PermissionError):
                pass

            logger.debug(
                f"Basic metadata: size={total_size}, files={file_count}, languages={len(language_files)}"
            )

        except Exception as e:
            logger.error(f"Failed to analyze basic metadata: {e}")

    def discover_and_scan(self, root_path: str, recursive: bool = True) -> List[RepositoryMetadata]:
        """Discover repositories and scan them automatically"""
        try:
            logger.info(f"Starting discovery and scan in: {root_path}")
            
            # Discover repositories
            discovered_paths = self.discovery_engine.discover_repositories(root_path, recursive)
            
            if not discovered_paths:
                logger.warning(f"No repositories discovered in: {root_path}")
                return []
            
            # Scan discovered repositories
            logger.info(f"Scanning {len(discovered_paths)} discovered repositories")
            results = []
            
            for path in discovered_paths:
                metadata = self.scan_repository(path, deep_scan=True)
                if metadata:
                    results.append(metadata)
            
            logger.info(f"Discovery and scan completed: {len(results)} repositories processed")
            return results
            
        except Exception as e:
            logger.error(f"Failed to discover and scan: {e}")
            return []

