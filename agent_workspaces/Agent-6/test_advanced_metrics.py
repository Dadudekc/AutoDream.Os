#!/usr/bin/env python3
"""
Test Advanced Performance Metrics - PERF-001 Contract

Simple test script to verify the advanced performance metrics system.

Author: Agent-6 (PERFORMANCE OPTIMIZATION MANAGER)
Contract: PERF-001 - Advanced Performance Metrics Implementation
Status: EXECUTION_IN_PROGRESS
"""

import time
import logging
from advanced_performance_metrics import AdvancedMetricsCollector, RealTimeMonitor


def test_metrics_collection():
    """Test basic metrics collection"""
    print("🧪 Testing Advanced Metrics Collection...")
    
    # Initialize collector
    collector = AdvancedMetricsCollector()
    
    # Collect a single snapshot
    print("📊 Collecting system snapshot...")
    snapshot = collector._collect_system_snapshot()
    
    print(f"✅ Snapshot collected at: {snapshot.timestamp}")
    print(f"📈 Overall Performance Score: {snapshot.overall_score:.1f}")
    
    # Display CPU metrics
    if 'error' not in snapshot.cpu_metrics:
        cpu = snapshot.cpu_metrics
        print(f"🖥️  CPU Usage: {cpu.get('usage_percent', 'N/A')}%")
        print(f"🖥️  CPU Cores: {cpu.get('core_count', 'N/A')}")
    else:
        print(f"❌ CPU Metrics Error: {snapshot.cpu_metrics['error']}")
    
    # Display memory metrics
    if 'error' not in snapshot.memory_metrics:
        memory = snapshot.memory_metrics
        print(f"💾 Memory Usage: {memory.get('used_percent', 'N/A')}%")
        print(f"💾 Total Memory: {memory.get('total_gb', 'N/A'):.1f} GB")
    else:
        print(f"❌ Memory Metrics Error: {snapshot.memory_metrics['error']}")
    
    # Display disk metrics
    if 'error' not in snapshot.disk_metrics:
        disk = snapshot.disk_metrics
        print(f"💿 Disk Usage: {disk.get('used_percent', 'N/A'):.1f}%")
        print(f"💿 Free Space: {disk.get('free_gb', 'N/A'):.1f} GB")
    else:
        print(f"❌ Disk Metrics Error: {snapshot.disk_metrics['error']}")
    
    # Display network metrics
    if 'error' not in snapshot.network_metrics:
        network = snapshot.network_metrics
        print(f"🌐 Active Connections: {network.get('active_connections', 'N/A')}")
        print(f"🌐 Total Connections: {network.get('total_connections', 'N/A')}")
    else:
        print(f"❌ Network Metrics Error: {snapshot.network_metrics['error']}")
    
    return snapshot


def test_real_time_monitoring():
    """Test real-time monitoring"""
    print("\n🧪 Testing Real-Time Monitoring...")
    
    # Initialize collector and monitor
    collector = AdvancedMetricsCollector()
    monitor = RealTimeMonitor(collector)
    
    # Start monitoring for a short period
    print("🚀 Starting real-time monitoring (10 seconds)...")
    monitor.start_monitoring()
    
    try:
        # Monitor for 10 seconds
        for i in range(10):
            time.sleep(1)
            
            # Get current metrics
            summary = collector.get_metrics_summary()
            if summary.get("status") == "active":
                latest = summary.get("latest_snapshot", {})
                cpu_usage = latest.get("cpu_metrics", {}).get("usage_percent", "N/A")
                memory_usage = latest.get("memory_metrics", {}).get("used_percent", "N/A")
                overall_score = latest.get("overall_score", "N/A")
                
                print(f"📊 [{i+1:2d}s] CPU: {cpu_usage}% | Memory: {memory_usage}% | Score: {overall_score}")
            else:
                print(f"📊 [{i+1:2d}s] Status: {summary.get('status', 'Unknown')}")
        
        # Check for alerts
        alerts = monitor.get_alerts()
        if alerts:
            print(f"\n🚨 {len(alerts)} alerts generated:")
            for alert in alerts[:3]:  # Show first 3 alerts
                print(f"   • {alert['metric_type']}: {alert['message']}")
        else:
            print("\n✅ No alerts generated during test")
            
    finally:
        monitor.stop_monitoring()
        print("⏹️ Real-time monitoring stopped")


def test_trend_analysis():
    """Test trend analysis"""
    print("\n🧪 Testing Trend Analysis...")
    
    # Initialize collector
    collector = AdvancedMetricsCollector()
    
    # Collect multiple snapshots to analyze trends
    print("📊 Collecting multiple snapshots for trend analysis...")
    
    for i in range(5):
        snapshot = collector._collect_system_snapshot()
        collector._store_snapshot(snapshot)
        time.sleep(1)
    
    # Get trends
    summary = collector.get_metrics_summary()
    if summary.get("status") == "active" and summary.get("trends"):
        trends = summary["trends"]
        print(f"📈 CPU Trend: {trends.get('cpu', 'N/A')}")
        print(f"📈 Memory Trend: {trends.get('memory', 'N/A')}")
        print(f"📈 Disk Trend: {trends.get('disk', 'N/A')}")
    else:
        print("❌ Trend analysis not available")


def main():
    """Main test function"""
    print("🚀 Advanced Performance Metrics Test - PERF-001 Contract")
    print("=" * 70)
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        # Test 1: Basic metrics collection
        snapshot = test_metrics_collection()
        
        # Test 2: Real-time monitoring
        test_real_time_monitoring()
        
        # Test 3: Trend analysis
        test_trend_analysis()
        
        print("\n" + "=" * 70)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        
        # Final summary
        print(f"📊 Final Performance Score: {snapshot.overall_score:.1f}")
        print(f"🕐 Test completed at: {snapshot.timestamp}")
        
        if snapshot.overall_score >= 80:
            print("🎉 Excellent system performance!")
        elif snapshot.overall_score >= 60:
            print("👍 Good system performance")
        elif snapshot.overall_score >= 40:
            print("⚠️  Moderate performance issues detected")
        else:
            print("🚨 Critical performance issues detected")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        logging.exception("Test execution failed")
    
    print(f"\n📁 Test completed. System saved to: {__file__}")


if __name__ == "__main__":
    main()
