#!/usr/bin/env python3
"""
Repository System Consolidation Integration Test
==============================================

Tests the consolidated RepositorySystemManager to ensure all functionality
from the 16 deleted files is properly integrated.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import unittest
import tempfile
import shutil
import os
from pathlib import Path
from unittest.mock import Mock, patch

from src.core.managers.repository_system_manager import (
    RepositorySystemManager,
    RepositoryMetadata,
    TechnologyStack,
    AnalysisResult,
    DiscoveryConfig,
    DiscoveryStatus,
    TechnologyType
)


class TestRepositorySystemConsolidation(unittest.TestCase):
    """Test consolidated repository system functionality."""

    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.repo_manager = RepositorySystemManager()
        
        # Create test repository structure
        self.test_repo_path = os.path.join(self.temp_dir, "test_repo")
        os.makedirs(self.test_repo_path)
        
        # Create test files
        self._create_test_repository()

    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
        if hasattr(self.repo_manager, 'cleanup'):
            self.repo_manager.cleanup()

    def _create_test_repository(self):
        """Create a test repository with various file types."""
        # Create Python files
        with open(os.path.join(self.test_repo_path, "main.py"), "w") as f:
            f.write("# Test Python file")
        
        with open(os.path.join(self.test_repo_path, "requirements.txt"), "w") as f:
            f.write("pytest==7.0.0\nrequests==2.28.0")
        
        # Create JavaScript files
        with open(os.path.join(self.test_repo_path, "app.js"), "w") as f:
            f.write("// Test JavaScript file")
        
        with open(os.path.join(self.test_repo_path, "package.json"), "w") as f:
            f.write('{"name": "test-app", "version": "1.0.0"}')
        
        # Create directory structure
        os.makedirs(os.path.join(self.test_repo_path, "src"))
        os.makedirs(os.path.join(self.test_repo_path, "tests"))
        os.makedirs(os.path.join(self.test_repo_path, "config"))
        
        # Create security file
        with open(os.path.join(self.test_repo_path, "SECURITY.md"), "w") as f:
            f.write("# Security Policy")
        
        # Create git directory
        os.makedirs(os.path.join(self.test_repo_path, ".git"))

    def test_repository_discovery(self):
        """Test repository discovery functionality."""
        # Test discovery
        repo_id = self.repo_manager.discover_repository(self.test_repo_path)
        self.assertIsNotNone(repo_id)
        self.assertIn(repo_id, self.repo_manager._repositories)
        
        # Verify metadata
        repo = self.repo_manager._repositories[repo_id]
        self.assertEqual(repo.name, "test_repo")
        self.assertEqual(repo.path, self.test_repo_path)
        self.assertEqual(repo.analysis_status, "discovered")
        self.assertGreater(repo.size_bytes, 0)
        self.assertGreater(repo.file_count, 0)

    def test_repository_analysis(self):
        """Test repository analysis functionality."""
        # Discover repository first
        repo_id = self.repo_manager.discover_repository(self.test_repo_path)
        
        # Analyze repository
        analysis_id = self.repo_manager.analyze_repository(repo_id)
        self.assertIsNotNone(analysis_id)
        
        # Verify analysis results
        repo = self.repo_manager._repositories[repo_id]
        self.assertEqual(repo.analysis_status, "analyzed")
        self.assertGreater(len(repo.technology_stack), 0)
        self.assertGreater(len(repo.architecture_patterns), 0)
        self.assertGreater(repo.security_score, 0)
        self.assertIsInstance(repo.performance_metrics, dict)

    def test_technology_detection(self):
        """Test technology detection functionality."""
        # Test technology detection directly
        technologies = self.repo_manager._detect_technologies(self.test_repo_path)
        self.assertGreater(len(technologies), 0)
        
        # Check for expected technologies
        tech_names = [tech.name for tech in technologies]
        self.assertIn("Python", tech_names)
        self.assertIn("JavaScript", tech_names)

    def test_architecture_pattern_detection(self):
        """Test architecture pattern detection."""
        patterns = self.repo_manager._detect_architecture_patterns(self.test_repo_path)
        self.assertGreater(len(patterns), 0)
        self.assertIn("src_tests_separation", patterns)

    def test_security_score_calculation(self):
        """Test security score calculation."""
        technologies = self.repo_manager._detect_technologies(self.test_repo_path)
        security_score = self.repo_manager._calculate_security_score(self.test_repo_path, technologies)
        self.assertGreater(security_score, 0.5)  # Should be higher due to security files and git

    def test_performance_metrics_generation(self):
        """Test performance metrics generation."""
        metrics = self.repo_manager._generate_performance_metrics(self.test_repo_path)
        self.assertIsInstance(metrics, dict)
        self.assertIn("file_count", metrics)
        self.assertIn("total_size_mb", metrics)

    def test_repository_scanning(self):
        """Test bulk repository scanning."""
        # Create another test repo
        test_repo_2 = os.path.join(self.temp_dir, "test_repo_2")
        os.makedirs(test_repo_2)
        with open(os.path.join(test_repo_2, "main.py"), "w") as f:
            f.write("# Another test repo")
        
        # Scan multiple repositories
        results = self.repo_manager.scan_repositories([self.test_repo_path, test_repo_2])
        self.assertEqual(len(results), 2)
        
        # Check results
        for path, result in results.items():
            self.assertIn("repo_id", result)
            self.assertIn("analysis_id", result)
            self.assertEqual(result["status"], "completed")

    def test_discovery_config(self):
        """Test discovery configuration."""
        config = DiscoveryConfig(
            scan_depth=5,
            include_hidden=True,
            max_file_size=5 * 1024 * 1024,
            parallel_workers=8
        )
        
        self.assertEqual(config.scan_depth, 5)
        self.assertTrue(config.include_hidden)
        self.assertEqual(config.max_file_size, 5 * 1024 * 1024)
        self.assertEqual(config.parallel_workers, 8)

    def test_performance_analysis(self):
        """Test performance analysis functionality."""
        # Add some test data
        self.repo_manager._discovery_history.append({
            "timestamp": 1234567890,
            "duration": 15.5,
            "status": "completed"
        })
        
        # Test performance analysis
        analysis = self.repo_manager.analyze_repository_performance_patterns(24)
        self.assertIsInstance(analysis, dict)
        self.assertIn("total_repositories", analysis)
        self.assertIn("discovery_performance", analysis)

    def test_intelligent_strategy_creation(self):
        """Test intelligent strategy creation."""
        strategy_id = self.repo_manager.create_intelligent_repository_strategy(
            "adaptive_discovery",
            {"custom_param": "value"}
        )
        self.assertIsNotNone(strategy_id)
        self.assertIn(strategy_id, self.repo_manager.intelligent_strategies)

    def test_needs_prediction(self):
        """Test repository needs prediction."""
        predictions = self.repo_manager.predict_repository_needs(30)
        self.assertIsInstance(predictions, list)

    def test_automatic_optimization(self):
        """Test automatic optimization."""
        optimization_result = self.repo_manager.optimize_repository_operations_automatically()
        self.assertIsInstance(optimization_result, dict)
        self.assertIn("optimizations_applied", optimization_result)

    def test_report_generation(self):
        """Test report generation."""
        # Add some test data first
        self.repo_manager.discover_repository(self.test_repo_path)
        
        report = self.repo_manager.generate_repository_report("comprehensive")
        self.assertIsInstance(report, dict)
        self.assertIn("report_id", report)
        self.assertIn("summary", report)
        self.assertIn("recommendations", report)

    def test_cleanup_functionality(self):
        """Test cleanup functionality."""
        # Test old repository cleanup
        self.repo_manager._cleanup_old_repositories()
        # Should not raise any exceptions

    def test_base_manager_inheritance(self):
        """Test that RepositorySystemManager inherits from BaseManager."""
        self.assertTrue(hasattr(self.repo_manager, 'status'))
        self.assertTrue(hasattr(self.repo_manager, 'priority'))
        self.assertTrue(hasattr(self.repo_manager, 'metrics'))
        self.assertTrue(hasattr(self.repo_manager, 'events'))

    def test_consolidation_completeness(self):
        """Test that all functionality from deleted files is present."""
        # Test discovery functionality (from discovery_engine.py)
        self.assertTrue(hasattr(self.repo_manager, 'discover_repository'))
        
        # Test technology detection (from technology_detector.py)
        self.assertTrue(hasattr(self.repo_manager, '_detect_technologies'))
        
        # Test analysis (from analysis_engine.py)
        self.assertTrue(hasattr(self.repo_manager, 'analyze_repository'))
        
        # Test scanning (from repository_scanner.py)
        self.assertTrue(hasattr(self.repo_manager, 'scan_repositories'))
        
        # Test reporting (from report_generator.py)
        self.assertTrue(hasattr(self.repo_manager, 'generate_repository_report'))
        
        # Test configuration (from discovery_config.py)
        self.assertTrue(hasattr(self.repo_manager, '_discovery_config'))


if __name__ == "__main__":
    unittest.main()
