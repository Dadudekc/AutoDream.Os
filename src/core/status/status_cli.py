#!/usr/bin/env python3
"""
Status CLI - Agent Cellphone V2
================================

CLI interface for live status system.
Follows V2 standards: ≤100 LOC, SRP, OOP principles.
"""

import time
import argparse
from .status_types import UpdateFrequency
from .status_core import LiveStatusSystem


def main():
    """CLI interface for Live Status System"""
    parser = argparse.ArgumentParser(description="Live Status System CLI")
    parser.add_argument("--start", "-s", action="store_true", help="Start live status system")
    parser.add_argument("--frequency", "-f", default="high", help="Update frequency (real_time/high/medium/low)")
    parser.add_argument("--status", action="store_true", help="Show live status")
    parser.add_argument("--events", "-e", type=int, default=10, help="Show recent events (default: 10)")
    parser.add_argument("--change-frequency", "-c", help="Change update frequency")
    
    args = parser.parse_args()
    
    system = LiveStatusSystem()
    
    if args.start:
        # Set frequency if specified
        if args.frequency:
            try:
                frequency = UpdateFrequency(args.frequency)
                system.change_update_frequency(frequency)
            except ValueError:
                print(f"❌ Invalid frequency: {args.frequency}")
                return
        
        print("🚀 STARTING LIVE STATUS SYSTEM")
        print("📊 Real-time agent visibility activated!")
        system.start_live_updates()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n⏹️ Stopping live status system...")
            system.stop_live_updates()
    
    elif args.change_frequency:
        try:
            frequency = UpdateFrequency(args.change_frequency)
            system.change_update_frequency(frequency)
            print(f"✅ Update frequency changed to {frequency.value}")
        except ValueError:
            print(f"❌ Invalid frequency: {args.change_frequency}")
    
    elif args.status:
        status = system.get_live_status()
        print("📊 Live Status System Status:")
        for key, value in status.items():
            print(f"  {key}: {value}")
    
    elif args.events:
        events = system.get_status_events(limit=args.events)
        print(f"📊 Recent Status Events (Last {args.events}):")
        for i, event in enumerate(events):
            print(f"  Event {i+1}: {event['event_type']} for {event['agent_id']}")
            print(f"    Priority: {event['priority']}")
            print(f"    Time: {event['timestamp']}")
    
    else:
        print("Live Status System - Use --help for options")


if __name__ == "__main__":
    main()
