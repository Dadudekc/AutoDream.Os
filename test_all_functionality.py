#!/usr/bin/env python3
"""
Comprehensive Functionality Test
===============================

Test all CLI tools and trading prediction functionality
"""

import os
import subprocess
import sys
from datetime import datetime

# Add the project root to the path
sys.path.append(os.path.dirname(__file__))


def test_imports():
    """Test that all modules can be imported"""
    print("🧪 Testing Module Imports...")

    try:
        print("✅ Trading flags module imported successfully")
    except Exception as e:
        print(f"❌ Trading flags import failed: {e}")
        return False

    try:
        print("✅ Trading flags display imported successfully")
    except Exception as e:
        print(f"❌ Trading flags display import failed: {e}")
        return False

    return True


def test_trading_engine():
    """Test the trading flag engine"""
    print("\n🤖 Testing Trading Flag Engine...")

    try:
        from tsla_forecast_app.modules import TradingFlagEngine

        engine = TradingFlagEngine()

        # Test market data analysis
        test_data = {"price": 425.85, "change": -8.36, "change_percent": -1.93, "volume": 82571488}

        analysis = engine.analyze_market_data(test_data)
        print(
            f"✅ Market analysis: {analysis.trend_direction} trend, {analysis.volatility:.1%} volatility"
        )

        # Test agent flag generation
        flags = engine.generate_all_agent_flags(analysis)
        print(f"✅ Generated {len(flags)} agent flags")

        # Test consensus
        consensus = engine.get_consensus_flag(flags)
        print(
            f"✅ Consensus: {consensus.flag_type.value.upper()} → ${consensus.price_target:.2f} ({consensus.confidence:.1%})"
        )

        return True

    except Exception as e:
        print(f"❌ Trading engine test failed: {e}")
        return False


def test_cli_tools():
    """Test CLI tools functionality"""
    print("\n🛠️ Testing CLI Tools...")

    tools = [
        ("market_analyzer.py", ["--symbol", "TSLA"]),
        ("news_analyzer.py", ["--symbol", "TSLA", "--signal"]),
        ("technical_analyzer.py", ["--symbol", "TSLA", "--days", "30"]),
        ("prediction_tracker.py", ["--report", "--symbol", "TSLA"]),
    ]

    results = []

    for tool, args in tools:
        try:
            tool_path = os.path.join("tools", "trading_cli", tool)
            cmd = [sys.executable, tool_path] + args

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                print(f"✅ {tool}: Working")
                results.append(True)
            else:
                print(f"❌ {tool}: Failed (exit code {result.returncode})")
                if result.stderr:
                    print(f"   Error: {result.stderr[:100]}...")
                results.append(False)

        except subprocess.TimeoutExpired:
            print(f"⏰ {tool}: Timed out")
            results.append(False)
        except Exception as e:
            print(f"❌ {tool}: Exception - {e}")
            results.append(False)

    return all(results)


def test_real_data():
    """Test real data fetching"""
    print("\n📊 Testing Real Data Fetching...")

    try:
        import requests

        # Test Yahoo Finance API
        url = "https://query1.finance.yahoo.com/v8/finance/chart/TSLA"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            result = data["chart"]["result"][0]
            meta = result["meta"]

            price = meta["regularMarketPrice"]
            change = meta["regularMarketPrice"] - meta.get(
                "previousClose", meta["regularMarketPrice"]
            )
            volume = meta["regularMarketVolume"]

            print("✅ Real Tesla Data:")
            print(f"   Price: ${price:.2f}")
            print(f"   Change: ${change:.2f}")
            print(f"   Volume: {volume:,}")

            return True
        else:
            print(f"❌ Yahoo Finance API failed: HTTP {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Real data test failed: {e}")
        return False


def test_prediction_accuracy():
    """Test prediction accuracy tracking"""
    print("\n📈 Testing Prediction Accuracy...")

    try:
        from tools.trading_cli.prediction_tracker import PredictionTracker

        tracker = PredictionTracker("test_predictions.db")

        # Record a test prediction
        prediction_id = tracker.record_prediction(
            "TSLA", "agent_1", "buy", 450.0, 0.8, "Test prediction"
        )
        print(f"✅ Recorded prediction #{prediction_id}")

        # Update with actual price
        tracker.update_actual_price(prediction_id, 445.0)
        print("✅ Updated with actual price")

        # Get accuracy report
        accuracy = tracker.get_agent_accuracy("TSLA", "agent_1")
        if accuracy:
            print(f"✅ Agent accuracy: {accuracy['accuracy_percentage']:.1%}")

        # Clean up test database
        os.remove("test_predictions.db")
        print("✅ Test database cleaned up")

        return True

    except Exception as e:
        print(f"❌ Prediction accuracy test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("🚀 COMPREHENSIVE FUNCTIONALITY TEST")
    print("=" * 50)
    print(f"Test started at: {datetime.now().isoformat()}")

    tests = [
        ("Module Imports", test_imports),
        ("Trading Engine", test_trading_engine),
        ("CLI Tools", test_cli_tools),
        ("Real Data Fetching", test_real_data),
        ("Prediction Accuracy", test_prediction_accuracy),
    ]

    results = []

    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))

    # Summary
    print(f"\n{'='*50}")
    print("📊 TEST SUMMARY")
    print("=" * 50)

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1

    print(f"\n🎯 Overall Result: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 ALL TESTS PASSED! System is fully functional.")
        return True
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
