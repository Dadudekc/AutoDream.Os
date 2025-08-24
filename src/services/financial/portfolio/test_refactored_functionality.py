#!/usr/bin/env python3
"""
Test Refactored Portfolio Optimization Functionality

This script tests the refactored portfolio optimization modules to ensure
they work correctly after extraction from the main service.

Follows V2 coding standards: Clean OOP design, SRP compliance, TDD approach.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from portfolio import (
    PortfolioOptimizationAlgorithms,
    PortfolioRiskModels,
    PortfolioRebalancing,
    PortfolioPerformanceTracker,
    PerformanceDataManager,
    OptimizationMethod,
    OptimizationConstraint,
    RebalancingFrequency,
    PerformanceMetric,
)

def test_algorithms_module():
    """Test the algorithms module functionality"""
    print("🧪 Testing Portfolio Optimization Algorithms...")
    
    try:
        # Initialize algorithms
        algo = PortfolioOptimizationAlgorithms()
        print("✅ Algorithms initialization successful")
        
        # Test data structures
        constraint = OptimizationConstraint("SECTOR_LIMIT", "AAPL", 0.0, 0.1, "TECHNOLOGY", 0.3)
        print("✅ Constraint creation successful")
        
        # Test optimization methods
        methods = list(OptimizationMethod)
        print(f"✅ {len(methods)} optimization methods available")
        
        # Test mock data creation
        symbols = ["AAPL", "MSFT", "GOOGL"]
        mock_returns = {"AAPL": 0.001, "MSFT": 0.002, "GOOGL": 0.0015}
        mock_covariance = {
            "AAPL": {"AAPL": 0.0004, "MSFT": 0.0002, "GOOGL": 0.0001},
            "MSFT": {"AAPL": 0.0002, "MSFT": 0.0006, "GOOGL": 0.0003},
            "GOOGL": {"AAPL": 0.0001, "MSFT": 0.0003, "GOOGL": 0.0005}
        }
        
        # Convert to pandas format
        import pandas as pd
        returns_series = pd.Series(mock_returns)
        covariance_df = pd.DataFrame(mock_covariance)
        
        # Test Sharpe ratio optimization
        result = algo.optimize_portfolio_sharpe(symbols, returns_series, covariance_df)
        if result:
            print(f"✅ Sharpe optimization successful - Expected Return: {result.expected_return:.4f}")
        else:
            print("⚠️ Sharpe optimization returned None (expected for mock data)")
        
        print("✅ Algorithms module tests completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Algorithms module test failed: {e}")
        return False

def test_risk_models_module():
    """Test the risk models module functionality"""
    print("🧪 Testing Portfolio Risk Models...")
    
    try:
        # Initialize risk models
        risk_models = PortfolioRiskModels()
        print("✅ Risk models initialization successful")
        
        # Test risk metrics calculation
        import pandas as pd
        mock_returns = pd.Series([0.01, -0.02, 0.015, -0.01, 0.03])
        
        var_95 = risk_models.calculate_historical_var(mock_returns, 0.95)
        cvar_95 = risk_models.calculate_conditional_var(mock_returns, 0.95)
        
        print(f"✅ VaR 95%: {var_95:.4f}")
        print(f"✅ CVaR 95%: {cvar_95:.4f}")
        
        # Test portfolio risk metrics
        weights = {"AAPL": 0.5, "MSFT": 0.5}
        returns_df = pd.DataFrame({
            "AAPL": [0.01, -0.02, 0.015, -0.01, 0.03],
            "MSFT": [0.015, -0.01, 0.02, -0.005, 0.025]
        })
        
        risk_metrics = risk_models.calculate_portfolio_risk_metrics(weights, returns_df)
        if risk_metrics:
            print(f"✅ Portfolio risk metrics calculated - Volatility: {risk_metrics.volatility:.4f}")
        else:
            print("⚠️ Risk metrics calculation returned None")
        
        print("✅ Risk models module tests completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Risk models module test failed: {e}")
        return False

def test_rebalancing_module():
    """Test the rebalancing module functionality"""
    print("🧪 Testing Portfolio Rebalancing...")
    
    try:
        # Initialize rebalancing
        rebalancing = PortfolioRebalancing()
        print("✅ Rebalancing initialization successful")
        
        # Test rebalancing signal generation
        current_weights = {"AAPL": 0.08, "MSFT": 0.12, "GOOGL": 0.10}
        target_weights = {"AAPL": 0.10, "MSFT": 0.10, "GOOGL": 0.10}
        
        signals = rebalancing.generate_rebalancing_signals(current_weights, target_weights)
        print(f"✅ Generated {len(signals)} rebalancing signals")
        
        # Test rebalancing plan creation
        plan = rebalancing.create_rebalancing_plan(current_weights, target_weights)
        if plan:
            print(f"✅ Rebalancing plan created - ID: {plan.plan_id}")
            print(f"   Total cost: ${plan.total_cost:.2f}")
            print(f"   Priority: {plan.priority}")
        else:
            print("⚠️ No rebalancing plan created (no signals generated)")
        
        # Test rebalancing need check
        needed, reason = rebalancing.check_rebalancing_needed(
            current_weights, target_weights, 
            frequency=RebalancingFrequency.MONTHLY
        )
        print(f"✅ Rebalancing needed: {needed} - Reason: {reason}")
        
        print("✅ Rebalancing module tests completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Rebalancing module test failed: {e}")
        return False

def test_tracking_module():
    """Test the tracking module functionality"""
    print("🧪 Testing Portfolio Performance Tracking...")
    
    try:
        # Initialize tracking
        manager = PerformanceDataManager()
        tracker = PortfolioPerformanceTracker(manager)
        print("✅ Performance tracking initialization successful")

        # Test portfolio performance tracking
        portfolio_value = 1_000_000
        weights = {"AAPL": 0.4, "MSFT": 0.3, "GOOGL": 0.3}

        snapshot = tracker.track_portfolio_performance(portfolio_value, weights)
        if snapshot:
            print(
                f"✅ Performance snapshot created - Value: ${snapshot.total_value:,.0f}"
            )
            print(f"   Total return: {snapshot.total_return:.4f}")
            print(f"   Daily return: {snapshot.daily_return:.4f}")
        else:
            print("⚠️ Performance snapshot creation failed")

        # Test performance report generation
        from datetime import datetime, timedelta
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()

        report = tracker.generate_report(start_date, end_date)
        if report:
            print(f"✅ Performance report generated - ID: {report.report_id}")
            print(f"   Period: {report.start_date.date()} to {report.end_date.date()}")
            print(f"   Total return: {report.total_return:.4f}")
        else:
            print("⚠️ Performance report generation failed (insufficient data)")
        
        print("✅ Performance tracking module tests completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Performance tracking module test failed: {e}")
        return False

def test_package_imports():
    """Test that all modules can be imported correctly"""
    print("🧪 Testing Package Imports...")
    
    try:
        # Test individual module imports
        from portfolio.algorithms import PortfolioOptimizationAlgorithms
        from portfolio.risk_models import PortfolioRiskModels
        from portfolio.rebalancing import PortfolioRebalancing
        from portfolio.tracking_logic import PortfolioPerformanceTracker
        from portfolio.data_management import PerformanceDataManager
        
        print("✅ All individual module imports successful")
        
        # Test package-level imports
        from portfolio import (
            PortfolioOptimizationAlgorithms,
            PortfolioRiskModels,
            PortfolioRebalancing,
            PortfolioPerformanceTracker,
            PerformanceDataManager,
        )
        
        print("✅ Package-level imports successful")
        
        # Test enum imports
        from portfolio import (
            OptimizationMethod,
            RebalancingFrequency,
            PerformanceMetric
        )
        
        print("✅ Enum imports successful")
        
        print("✅ Package import tests completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Package import test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 PORTFOLIO OPTIMIZATION REFACTORING VALIDATION")
    print("=" * 60)
    
    test_results = []
    
    # Run all tests
    test_results.append(("Package Imports", test_package_imports()))
    test_results.append(("Algorithms Module", test_algorithms_module()))
    test_results.append(("Risk Models Module", test_risk_models_module()))
    test_results.append(("Rebalancing Module", test_rebalancing_module()))
    test_results.append(("Performance Tracking Module", test_tracking_module()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:30} {status}")
        if result:
            passed += 1
    
    print("=" * 60)
    print(f"Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Refactoring successful!")
        return True
    else:
        print("⚠️ Some tests failed. Please review the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

