"""V2 Compliant TestUnifiedTestUtilities_part_2 - class_section_split"""

# Standard library imports
import os
import sys
import unittest

            required_status="completed"
        )
        
        # Invalid test results (missing key)
        invalid_results = {"total": 5, "passed": 4}
        
        with self.assertRaises(AssertionError):
            self.utilities.assert_test_results(
                invalid_results,
                expected_keys=["total", "passed", "failed"]
            )
    
    def test_assert_mock_called_with(self):
        """Test mock assertion functionality."""
        mock_obj = Mock()
        mock_obj.test_method = Mock(return_value=True)
        
        # Call the method
        mock_obj.test_method("arg1", "arg2", kwarg1="value1")
        
        # Should not raise exception
        self.utilities.assert_mock_called_with(
            mock_obj,
            "test_method",
            expected_args=("arg1", "arg2"),
            expected_kwargs={"kwarg1": "value1"}
        )
        
        # Test with wrong arguments
        with self.assertRaises(AssertionError):
            self.utilities.assert_mock_called_with(
                mock_obj,
                "test_method",
                expected_args=("wrong", "args")
            )
    
    def test_file_assertions(self):
        """Test file and directory assertions."""
        # Create test file
        test_file = self.temp_dir / "test_file.txt"
        test_file.touch()
        
        # Create test directory
        test_dir = self.temp_dir / "test_dir"
        test_dir.mkdir()
        
        # Should not raise exceptions
        self.utilities.assert_file_exists(test_file)
        self.utilities.assert_directory_exists(test_dir)
        
        # Test non-existent file/directory
        non_existent_file = self.temp_dir / "non_existent.txt"
        non_existent_dir = self.temp_dir / "non_existent"
        
        with self.assertRaises(AssertionError):
            self.utilities.assert_file_exists(non_existent_file)
        
        with self.assertRaises(AssertionError):
            self.utilities.assert_directory_exists(non_existent_dir)
    
    def test_cleanup_utilities(self):
        """Test cleanup utilities."""
        # Create test files and directories
        test_file = self.temp_dir / "cleanup_test.txt"
        test_file.touch()
        
        test_dir = self.temp_dir / "cleanup_test_dir"
        test_dir.mkdir()
        (test_dir / "nested_file.txt").touch()
        
        # Verify they exist
        self.assertTrue(test_file.exists())
        self.assertTrue(test_dir.exists())
        
        # Clean up
        self.utilities.cleanup_test_files([test_file])
        self.utilities.cleanup_test_directories([test_dir])
        
        # Verify they were removed
        self.assertFalse(test_file.exists())
        self.assertFalse(test_dir.exists())
    
    def test_mock_reset(self):
        """Test mock object reset functionality."""
        mock_obj = Mock()
        mock_obj.test_method = Mock(return_value=True)
        
        # Call the method
        mock_obj.test_method()
        
        # Verify it was called
        self.assertEqual(mock_obj.test_method.call_count, 1)
        
        # Reset
        self.utilities.reset_mock_objects([mock_obj])
        
        # Verify it was reset
        self.assertEqual(mock_obj.test_method.call_count, 0)
    
    def test_environment_utilities(self):
        """Test environment setup and restore utilities."""
        # Setup test environment
        env_state = self.utilities.setup_test_environment(
            env_vars={"TEST_VAR": "test_value"},
            working_dir=self.temp_dir
        )
        
        # Verify environment was set
        self.assertEqual(os.environ.get("TEST_VAR"), "test_value")
        self.assertEqual(os.getcwd(), self.temp_dir)
        
        # Restore environment
        self.utilities.restore_test_environment(env_state)
        
        # Verify environment was restored
        self.assertNotIn("TEST_VAR", os.environ)
    
    def test_command_execution(self):
        """Test command execution utilities."""
        # Test successful command
        return_code, stdout, stderr = self.utilities.run_command_with_timeout(
            ["echo", "test output"],
            timeout=5
        )
        
        self.assertEqual(return_code, 0)
        self.assertIn("test output", stdout)
        self.assertEqual(stderr, "")
        
        # Test command timeout
        return_code, stdout, stderr = self.utilities.run_command_with_timeout(
            ["sleep", "10"],
            timeout=1
        )
        
        self.assertEqual(return_code, -1)
        self.assertIn("timed out", stderr)
    
    def test_condition_waiting(self):
        """Test condition waiting utilities."""
        # Test successful condition
        start_time = time.time()
        result = self.utilities.wait_for_condition(
            lambda: time.time() - start_time > 0.1,
            timeout=1,
            interval=0.05
        )
        
        self.assertTrue(result)
        
        # Test timeout condition
        result = self.utilities.wait_for_condition(
            lambda: False,
            timeout=0.1,
            interval=0.01
        )
        
        self.assertFalse(result)
    
    def test_test_summary_generation(self):
        """Test test summary generation."""
        test_results = [
            {"status": "passed"},
            {"status": "passed"},
            {"status": "failed"},
            {"status": "error"}
        ]
        
        summary = self.utilities.generate_test_summary(test_results)
        
        self.assertEqual(summary["total"], 4)
        self.assertEqual(summary["passed"], 2)
        self.assertEqual(summary["failed"], 1)
        self.assertEqual(summary["errors"], 1)
        self.assertEqual(summary["success_rate"], 50.0)
        self.assertIn("details", summary)
        
        # Test without details
        summary_no_details = self.utilities.generate_test_summary(
            test_results, include_details=False
        )
        
        self.assertNotIn("details", summary_no_details)
    
    def test_test_report_saving(self):
        """Test test report saving functionality."""
        report_data = {
            "summary": {"total": 10, "passed": 8, "failed": 2},
            "details": ["detail1", "detail2"]
        }
        
        report_file = self.temp_dir / "test_report.json"
        
        self.utilities.save_test_report(report_data, report_file, "json")
        
        # Verify file was created
        self.assertTrue(report_file.exists())
        
        # Verify content
        with open(report_file, 'r') as f:
            saved_report = json.load(f)
        
        self.assertEqual(saved_report["summary"]["total"], 10)
        self.assertEqual(saved_report["summary"]["passed"], 8)
        self.assertEqual(saved_report["summary"]["failed"], 2)
        self.assertEqual(saved_report["details"], ["detail1", "detail2"])


# ============================================================================
# TEST INTEGRATION BETWEEN SYSTEMS
# ============================================================================

