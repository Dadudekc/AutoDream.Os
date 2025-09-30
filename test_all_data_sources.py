#!/usr/bin/env python3
"""
Test All Data Sources
====================

Test all available data sources to see which ones work
"""

from datetime import datetime
from test_all_data_sources_core import (
    test_yahoo_finance,
    test_alpha_vantage,
    test_polygon,
    test_finnhub,
    test_news_api,
    test_alpaca,
    check_env_file,
)


def main():
    """Test all data sources"""
    print("🚀 TESTING ALL DATA SOURCES")
    print("=" * 50)
    print(f"Test started at: {datetime.now().isoformat()}")
    print()

    # Check .env file
    check_env_file()
    print()

    # Test all sources
    results = []

    results.append(test_yahoo_finance())
    print()

    results.append(test_alpha_vantage())
    print()

    results.append(test_polygon())
    print()

    results.append(test_finnhub())
    print()

    results.append(test_news_api())
    print()

    results.append(test_alpaca())
    print()

    # Summary
    print("📊 TEST SUMMARY")
    print("=" * 30)

    working = []
    failed = []
    no_keys = []

    for result in results:
        if result["status"] == "working":
            working.append(result["source"])
        elif result["status"] in ["no_api_key", "no_credentials"]:
            no_keys.append(result["source"])
        else:
            failed.append(result["source"])

    print(f"✅ Working: {', '.join(working) if working else 'None'}")
    print(f"❌ Failed: {', '.join(failed) if failed else 'None'}")
    print(f"🔑 No API Keys: {', '.join(no_keys) if no_keys else 'None'}")

    print(f"\n🎯 Total Sources: {len(results)}")
    print(f"✅ Working: {len(working)}")
    print(f"❌ Failed: {len(failed)}")
    print(f"🔑 No Keys: {len(no_keys)}")


if __name__ == "__main__":
    main()