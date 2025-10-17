#!/usr/bin/env python3
"""
Tests for Validation Analytics Processor
=========================================

Author: Agent-5
Date: 2025-10-17
"""

import pytest
from datetime import datetime
from src.core.analytics.validation_analytics_processor import (
    ValidationMetric,
    ValidationAnalyticsProcessor,
    get_analytics_processor,
    record_validation_metric,
)


class TestValidationMetric:
    """Tests for ValidationMetric dataclass."""
    
    def test_create_metric(self):
        """Test creating validation metric."""
        metric = ValidationMetric(
            function_name='validate_config',
            success=True,
            execution_time_ms=15.5
        )
        assert metric.function_name == 'validate_config'
        assert metric.success is True
        assert metric.execution_time_ms == 15.5
    
    def test_metric_with_error(self):
        """Test metric with error message."""
        metric = ValidationMetric(
            function_name='validate_session',
            success=False,
            error_message='Session expired'
        )
        assert metric.success is False
        assert metric.error_message == 'Session expired'


class TestValidationAnalyticsProcessor:
    """Tests for ValidationAnalyticsProcessor."""
    
    @pytest.fixture
    def processor(self):
        """Create fresh processor for each test."""
        return ValidationAnalyticsProcessor()
    
    def test_record_validation_success(self, processor):
        """Test recording successful validation."""
        metric = ValidationMetric(function_name='test_func', success=True)
        processor.record_validation(metric)
        
        assert len(processor.metrics) == 1
        stats = processor.get_function_stats('test_func')
        assert stats['total_calls'] == 1
        assert stats['successes'] == 1
        assert stats['failures'] == 0
    
    def test_record_validation_failure(self, processor):
        """Test recording failed validation."""
        metric = ValidationMetric(
            function_name='test_func',
            success=False,
            error_message='Test error'
        )
        processor.record_validation(metric)
        
        stats = processor.get_function_stats('test_func')
        assert stats['failures'] == 1
        assert 'Test error' in stats['errors']
    
    def test_success_rate_single_function(self, processor):
        """Test success rate calculation for single function."""
        # Record 7 successes, 3 failures
        for i in range(7):
            processor.record_validation(
                ValidationMetric(function_name='test_func', success=True)
            )
        for i in range(3):
            processor.record_validation(
                ValidationMetric(function_name='test_func', success=False)
            )
        
        success_rate = processor.get_success_rate('test_func')
        assert success_rate == 70.0  # 7/10 = 70%
    
    def test_success_rate_overall(self, processor):
        """Test overall success rate across functions."""
        # Function 1: 8/10 success (80%)
        for i in range(8):
            processor.record_validation(
                ValidationMetric(function_name='func1', success=True)
            )
        for i in range(2):
            processor.record_validation(
                ValidationMetric(function_name='func1', success=False)
            )
        
        # Function 2: 6/10 success (60%)
        for i in range(6):
            processor.record_validation(
                ValidationMetric(function_name='func2', success=True)
            )
        for i in range(4):
            processor.record_validation(
                ValidationMetric(function_name='func2', success=False)
            )
        
        # Overall: 14/20 = 70%
        overall = processor.get_success_rate()
        assert overall == 70.0
    
    def test_average_execution_time(self, processor):
        """Test average execution time calculation."""
        processor.record_validation(
            ValidationMetric(function_name='test_func', success=True, execution_time_ms=10.0)
        )
        processor.record_validation(
            ValidationMetric(function_name='test_func', success=True, execution_time_ms=20.0)
        )
        processor.record_validation(
            ValidationMetric(function_name='test_func', success=True, execution_time_ms=30.0)
        )
        
        stats = processor.get_function_stats('test_func')
        assert stats['avg_time_ms'] == 20.0  # (10+20+30)/3 = 20
    
    def test_get_top_failures(self, processor):
        """Test getting functions with most failures."""
        # Func1: 5 failures
        for i in range(5):
            processor.record_validation(
                ValidationMetric(function_name='func1', success=False)
            )
        
        # Func2: 10 failures
        for i in range(10):
            processor.record_validation(
                ValidationMetric(function_name='func2', success=False)
            )
        
        # Func3: 2 failures
        for i in range(2):
            processor.record_validation(
                ValidationMetric(function_name='func3', success=False)
            )
        
        top_failures = processor.get_top_failures(2)
        assert len(top_failures) == 2
        assert top_failures[0] == ('func2', 10)  # Most failures
        assert top_failures[1] == ('func1', 5)   # Second most
    
    def test_get_slowest_functions(self, processor):
        """Test getting slowest functions."""
        processor.record_validation(
            ValidationMetric(function_name='fast_func', success=True, execution_time_ms=5.0)
        )
        processor.record_validation(
            ValidationMetric(function_name='medium_func', success=True, execution_time_ms=50.0)
        )
        processor.record_validation(
            ValidationMetric(function_name='slow_func', success=True, execution_time_ms=200.0)
        )
        
        slowest = processor.get_slowest_functions(2)
        assert len(slowest) == 2
        assert slowest[0][0] == 'slow_func'  # Slowest
        assert slowest[1][0] == 'medium_func'  # Second slowest
    
    def test_generate_insights_low_success(self, processor):
        """Test insights for low success rate."""
        # 60% success rate
        for i in range(6):
            processor.record_validation(
                ValidationMetric(function_name='test_func', success=True)
            )
        for i in range(4):
            processor.record_validation(
                ValidationMetric(function_name='test_func', success=False)
            )
        
        insights = processor.generate_insights()
        assert any('60.0%' in insight for insight in insights)
        assert any('target: 80%' in insight for insight in insights)
    
    def test_generate_insights_high_success(self, processor):
        """Test insights for high success rate."""
        # 98% success rate
        for i in range(98):
            processor.record_validation(
                ValidationMetric(function_name='test_func', success=True)
            )
        for i in range(2):
            processor.record_validation(
                ValidationMetric(function_name='test_func', success=False)
            )
        
        insights = processor.generate_insights()
        assert any('Excellent' in insight or '98.0%' in insight for insight in insights)
    
    def test_summary_report(self, processor):
        """Test comprehensive summary report."""
        # Add some test data
        for i in range(10):
            processor.record_validation(
                ValidationMetric(function_name='test_func', success=True, execution_time_ms=10.0)
            )
        
        report = processor.get_summary_report()
        
        assert 'overall_success_rate' in report
        assert 'total_validations' in report
        assert 'unique_functions' in report
        assert 'insights' in report
        assert report['overall_success_rate'] == 100.0
        assert report['total_validations'] == 10


class TestGlobalInterface:
    """Tests for global interface functions."""
    
    def test_get_analytics_processor(self):
        """Test getting global processor."""
        processor = get_analytics_processor()
        assert isinstance(processor, ValidationAnalyticsProcessor)
    
    def test_record_validation_metric_convenience(self):
        """Test convenience function for recording metrics."""
        record_validation_metric(
            function_name='test_func',
            success=True,
            execution_time_ms=15.0,
            file='test.py',
            line=42
        )
        
        processor = get_analytics_processor()
        stats = processor.get_function_stats('test_func')
        assert stats['total_calls'] > 0  # Should have recorded

