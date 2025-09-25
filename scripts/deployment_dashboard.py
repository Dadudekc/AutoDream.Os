#!/usr/bin/env python3
"""
Deployment and Monitoring Dashboard
===================================

Comprehensive dashboard for monitoring deployed modular components.
"""

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools.workflow import WorkflowManager
from tools.workflow.optimization import WorkflowOptimizer
from src.services.discord_commander import DiscordCommanderBot
from src.services.discord_commander.optimization import DiscordOptimizer
from src.monitoring.performance_monitor import RealTimePerformanceMonitor


class DeploymentDashboard:
    """Comprehensive deployment and monitoring dashboard."""
    
    def __init__(self):
        self.project_root = project_root
        self.components = {}
        self.monitoring_active = False
        
    def initialize_components(self):
        """Initialize all modular components."""
        try:
            # Initialize workflow components
            self.components['workflow_manager'] = WorkflowManager()
            self.components['workflow_optimizer'] = WorkflowOptimizer()
            
            # Initialize Discord commander components
            self.components['discord_bot'] = DiscordCommanderBot()
            self.components['discord_optimizer'] = DiscordOptimizer()
            
            # Initialize performance monitoring
            self.components['performance_monitor'] = RealTimePerformanceMonitor(self.project_root)
            
            print("✅ All modular components initialized successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Component initialization failed: {e}")
            return False
    
    def test_component_functionality(self) -> Dict[str, bool]:
        """Test functionality of all components."""
        results = {}
        
        try:
            # Test workflow manager
            manager = self.components['workflow_manager']
            workflows = manager.list_workflows()
            results['workflow_manager'] = True
            print("✅ Workflow Manager: Functional")
            
        except Exception as e:
            results['workflow_manager'] = False
            print(f"❌ Workflow Manager: Failed - {e}")
        
        try:
            # Test workflow optimizer
            optimizer = self.components['workflow_optimizer']
            stats = optimizer.get_optimization_stats()
            results['workflow_optimizer'] = True
            print("✅ Workflow Optimizer: Functional")
            
        except Exception as e:
            results['workflow_optimizer'] = False
            print(f"❌ Workflow Optimizer: Failed - {e}")
        
        try:
            # Test Discord bot
            bot = self.components['discord_bot']
            status = bot.get_status()
            results['discord_bot'] = True
            print("✅ Discord Bot: Functional")
            
        except Exception as e:
            results['discord_bot'] = False
            print(f"❌ Discord Bot: Failed - {e}")
        
        try:
            # Test Discord optimizer
            discord_optimizer = self.components['discord_optimizer']
            stats = discord_optimizer.get_optimization_stats()
            results['discord_optimizer'] = True
            print("✅ Discord Optimizer: Functional")
            
        except Exception as e:
            results['discord_optimizer'] = False
            print(f"❌ Discord Optimizer: Failed - {e}")
        
        try:
            # Test performance monitor
            monitor = self.components['performance_monitor']
            summary = monitor.get_performance_summary()
            results['performance_monitor'] = True
            print("✅ Performance Monitor: Functional")
            
        except Exception as e:
            results['performance_monitor'] = False
            print(f"❌ Performance Monitor: Failed - {e}")
        
        return results
    
    def get_deployment_status(self) -> Dict[str, Any]:
        """Get comprehensive deployment status."""
        status = {
            "deployment_time": datetime.now().isoformat(),
            "components": {},
            "overall_status": "healthy"
        }
        
        # Check component status
        for name, component in self.components.items():
            try:
                if hasattr(component, 'get_status'):
                    component_status = component.get_status()
                elif hasattr(component, 'get_optimization_stats'):
                    component_status = component.get_optimization_stats()
                else:
                    component_status = {"status": "initialized"}
                
                status["components"][name] = {
                    "status": "healthy",
                    "details": component_status
                }
                
            except Exception as e:
                status["components"][name] = {
                    "status": "error",
                    "error": str(e)
                }
                status["overall_status"] = "degraded"
        
        return status
    
    def display_dashboard(self):
        """Display comprehensive dashboard."""
        print("\n" + "="*80)
        print("🚀 MODULAR COMPONENTS DEPLOYMENT DASHBOARD")
        print("="*80)
        
        # Component status
        print("\n📊 COMPONENT STATUS:")
        print("-" * 40)
        
        status = self.get_deployment_status()
        for name, component_status in status["components"].items():
            status_icon = "✅" if component_status["status"] == "healthy" else "❌"
            print(f"{status_icon} {name.replace('_', ' ').title()}: {component_status['status'].upper()}")
        
        # Overall status
        overall_icon = "✅" if status["overall_status"] == "healthy" else "⚠️"
        print(f"\n{overall_icon} Overall Status: {status['overall_status'].upper()}")
        
        # Performance metrics
        print("\n⚡ PERFORMANCE METRICS:")
        print("-" * 40)
        
        try:
            workflow_stats = self.components['workflow_optimizer'].get_optimization_stats()
            discord_stats = self.components['discord_optimizer'].get_optimization_stats()
            
            print(f"Workflow Cache Hit Rate: {workflow_stats.get('cache', {}).get('hit_rate', 0):.1%}")
            print(f"Discord Cache Hit Rate: {discord_stats.get('cache', {}).get('hit_rate', 0):.1%}")
            print(f"Workflow Active Tasks: {workflow_stats.get('parallel_executor', {}).get('active_tasks', 0)}")
            print(f"Discord Active Tasks: {discord_stats.get('async_pool', {}).get('active_tasks', 0)}")
            
        except Exception as e:
            print(f"Performance metrics unavailable: {e}")
        
        # Monitoring status
        print("\n📈 MONITORING STATUS:")
        print("-" * 40)
        
        try:
            monitor = self.components['performance_monitor']
            summary = monitor.get_performance_summary()
            
            if summary.get("message"):
                print(f"Status: {summary['message']}")
            else:
                print(f"Monitoring Duration: {summary.get('monitoring_duration', 0):.1f} seconds")
                print(f"Total Snapshots: {summary.get('total_snapshots', 0)}")
                
                recent_avg = summary.get('recent_averages', {})
                print(f"Recent CPU Average: {recent_avg.get('cpu_percent', 0):.1f}%")
                print(f"Recent Memory Average: {recent_avg.get('memory_mb', 0):.1f}MB")
                print(f"Recent Response Time: {recent_avg.get('response_time_ms', 0):.1f}ms")
                
        except Exception as e:
            print(f"Monitoring status unavailable: {e}")
        
        print("\n" + "="*80)
    
    async def start_monitoring(self):
        """Start real-time monitoring."""
        try:
            monitor = self.components['performance_monitor']
            await monitor.start_monitoring()
            self.monitoring_active = True
            print("📈 Real-time monitoring started")
        except Exception as e:
            print(f"❌ Failed to start monitoring: {e}")
    
    async def stop_monitoring(self):
        """Stop real-time monitoring."""
        try:
            monitor = self.components['performance_monitor']
            await monitor.stop_monitoring()
            self.monitoring_active = False
            print("📈 Real-time monitoring stopped")
        except Exception as e:
            print(f"❌ Failed to stop monitoring: {e}")
    
    def save_deployment_report(self) -> bool:
        """Save comprehensive deployment report."""
        try:
            report = {
                "report_time": datetime.now().isoformat(),
                "deployment_status": self.get_deployment_status(),
                "component_tests": self.test_component_functionality(),
                "monitoring_active": self.monitoring_active
            }
            
            report_path = self.project_root / "deployment_dashboard_report.json"
            with open(report_path, 'w') as f:
                json.dump(report, f, indent=2)
            
            print(f"📋 Deployment report saved: {report_path}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to save deployment report: {e}")
            return False


async def main():
    """Main dashboard function."""
    dashboard = DeploymentDashboard()
    
    print("🚀 Initializing Modular Components Deployment Dashboard...")
    
    # Initialize components
    if not dashboard.initialize_components():
        print("❌ Dashboard initialization failed")
        return 1
    
    # Test component functionality
    print("\n🧪 Testing Component Functionality...")
    test_results = dashboard.test_component_functionality()
    
    # Display dashboard
    dashboard.display_dashboard()
    
    # Start monitoring
    print("\n📈 Starting Real-time Monitoring...")
    await dashboard.start_monitoring()
    
    # Save report
    dashboard.save_deployment_report()
    
    print("\n✅ Deployment Dashboard Ready!")
    print("Press Ctrl+C to stop monitoring and exit")
    
    try:
        # Keep monitoring running
        while True:
            await asyncio.sleep(30)  # Update every 30 seconds
            dashboard.display_dashboard()
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping monitoring...")
        await dashboard.stop_monitoring()
        print("✅ Dashboard stopped successfully")
    
    return 0


if __name__ == "__main__":
    exit(asyncio.run(main()))




