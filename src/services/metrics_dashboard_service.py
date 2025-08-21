#!/usr/bin/env python3
"""
Simple Metrics Dashboard Service for testing
"""

import json
import time
from datetime import datetime

class MetricsDashboardService:
    def __init__(self):
        self.metrics = {}
        print("Metrics Dashboard Service initialized")
    
    def record_metric(self, name, value):
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append({"timestamp": time.time(), "value": value})
        print(f"Recorded metric {name}: {value}")
    
    def get_summary(self):
        return {
            "total_metrics": sum(len(values) for values in self.metrics.values()),
            "metrics_tracked": len(self.metrics),
            "timestamp": datetime.now().isoformat()
        }

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Simple Metrics Dashboard Service")
    parser.add_argument("--test", action="store_true", help="Run test mode")
    
    args = parser.parse_args()
    
    if args.test:
        print("Running Metrics Dashboard Service in test mode...")
        
        dashboard = MetricsDashboardService()
        
        # Record some test metrics
        dashboard.record_metric("test.counter", 42)
        dashboard.record_metric("test.gauge", 75.5)
        dashboard.record_metric("system.cpu", 45.2)
        
        # Show summary
        summary = dashboard.get_summary()
        print(f"\\nSummary: {json.dumps(summary, indent=2)}")
        print("Test completed successfully!")
        
        return
    
    print("Use --test to run test mode")

if __name__ == "__main__":
    main()
