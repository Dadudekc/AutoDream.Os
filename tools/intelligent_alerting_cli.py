"""
Intelligent Alerting System CLI
==============================

Command-line interface for the Intelligent Alerting System.
Provides alert management, rule configuration, and analytics.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from src.services.alerting.intelligent_alerting_system import (
    IntelligentAlertingSystem, AlertSeverity, AlertStatus, NotificationChannel
)

def create_sample_alert(system: IntelligentAlertingSystem, title: str, 
                       severity: str, source: str, category: str) -> str:
    """Create a sample alert for testing."""
    severity_enum = AlertSeverity(severity.lower())
    alert_id = system.create_alert(
        title=title,
        description=f"Sample alert for {category} from {source}",
        severity=severity_enum,
        source=source,
        category=category,
        metadata={"test": True, "created_by": "cli"}
    )
    return alert_id

def display_alerts(alerts, limit: int = 10):
    """Display alerts in a formatted table."""
    if not alerts:
        print("No alerts found.")
        return
    
    print(f"\n📊 ALERTS (showing {min(len(alerts), limit)} of {len(alerts)}):")
    print("-" * 80)
    print(f"{'ID':<15} {'Title':<25} {'Severity':<10} {'Status':<12} {'Created':<20}")
    print("-" * 80)
    
    for alert in alerts[:limit]:
        created_str = alert.created_at.strftime("%Y-%m-%d %H:%M:%S")
        print(f"{alert.id:<15} {alert.title[:24]:<25} {alert.severity.value:<10} "
              f"{alert.status.value:<12} {created_str:<20}")

def display_analytics(system: IntelligentAlertingSystem):
    """Display alert analytics."""
    analytics = system.get_alert_analytics()
    
    print("\n📈 ALERT ANALYTICS:")
    print("=" * 50)
    print(f"Total Alerts:     {analytics['total_alerts']}")
    print(f"Active Alerts:    {analytics['active_alerts']}")
    print(f"Resolved Alerts:  {analytics['resolved_alerts']}")
    print(f"Resolution Rate:  {analytics['resolution_rate']:.1%}")
    
    print("\nSeverity Distribution:")
    for severity, count in analytics['severity_distribution'].items():
        print(f"  {severity.capitalize()}: {count}")

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Intelligent Alerting System CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create a test alert
  python tools/intelligent_alerting_cli.py create --title "Test Alert" --severity high --source "test" --category "system"
  
  # List active alerts
  python tools/intelligent_alerting_cli.py list --status active
  
  # Show analytics
  python tools/intelligent_alerting_cli.py analytics
  
  # Acknowledge an alert
  python tools/intelligent_alerting_cli.py acknowledge --alert-id alert_20250117_200000_0 --user "Agent-2"
  
  # Resolve an alert
  python tools/intelligent_alerting_cli.py resolve --alert-id alert_20250117_200000_0
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create alert command
    create_parser = subparsers.add_parser('create', help='Create a new alert')
    create_parser.add_argument('--title', required=True, help='Alert title')
    create_parser.add_argument('--severity', required=True, 
                             choices=['low', 'medium', 'high', 'critical'],
                             help='Alert severity')
    create_parser.add_argument('--source', required=True, help='Alert source')
    create_parser.add_argument('--category', required=True, help='Alert category')
    create_parser.add_argument('--description', help='Alert description')
    
    # List alerts command
    list_parser = subparsers.add_parser('list', help='List alerts')
    list_parser.add_argument('--status', choices=['active', 'acknowledged', 'resolved', 'suppressed'],
                            help='Filter by status')
    list_parser.add_argument('--severity', choices=['low', 'medium', 'high', 'critical'],
                            help='Filter by severity')
    list_parser.add_argument('--limit', type=int, default=10, help='Limit number of results')
    
    # Acknowledge alert command
    ack_parser = subparsers.add_parser('acknowledge', help='Acknowledge an alert')
    ack_parser.add_argument('--alert-id', required=True, help='Alert ID')
    ack_parser.add_argument('--user', required=True, help='User acknowledging the alert')
    
    # Resolve alert command
    resolve_parser = subparsers.add_parser('resolve', help='Resolve an alert')
    resolve_parser.add_argument('--alert-id', required=True, help='Alert ID')
    
    # Analytics command
    analytics_parser = subparsers.add_parser('analytics', help='Show alert analytics')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Create test alerts')
    test_parser.add_argument('--count', type=int, default=5, help='Number of test alerts to create')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export alerts to JSON')
    export_parser.add_argument('--file', required=True, help='Output file path')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize alerting system
    try:
        system = IntelligentAlertingSystem()
    except Exception as e:
        print(f"❌ Error initializing alerting system: {e}")
        return 1
    
    try:
        if args.command == 'create':
            alert_id = create_sample_alert(
                system, args.title, args.severity, args.source, args.category
            )
            print(f"✅ Created alert: {alert_id}")
        
        elif args.command == 'list':
            status = AlertStatus(args.status) if args.status else None
            severity = AlertSeverity(args.severity) if args.severity else None
            
            alerts = system.get_alerts(status=status, severity=severity)
            display_alerts(alerts, args.limit)
        
        elif args.command == 'acknowledge':
            success = system.acknowledge_alert(args.alert_id, args.user)
            if success:
                print(f"✅ Alert {args.alert_id} acknowledged by {args.user}")
            else:
                print(f"❌ Alert {args.alert_id} not found")
        
        elif args.command == 'resolve':
            success = system.resolve_alert(args.alert_id)
            if success:
                print(f"✅ Alert {args.alert_id} resolved")
            else:
                print(f"❌ Alert {args.alert_id} not found")
        
        elif args.command == 'analytics':
            display_analytics(system)
        
        elif args.command == 'test':
            print(f"Creating {args.count} test alerts...")
            for i in range(args.count):
                severity = ['low', 'medium', 'high', 'critical'][i % 4]
                source = f"test_source_{i+1}"
                category = f"test_category_{i+1}"
                title = f"Test Alert {i+1}"
                
                alert_id = create_sample_alert(system, title, severity, source, category)
                print(f"  Created: {alert_id}")
            
            print(f"✅ Created {args.count} test alerts")
        
        elif args.command == 'export':
            system.export_alerts(args.file)
            print(f"✅ Exported alerts to {args.file}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())


