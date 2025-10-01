"""
Memory Monitoring CLI - Phase 4
================================

Comprehensive CLI interface for memory leak detection, monitoring, and reporting.
Integrates with existing memory leak infrastructure from Agent-5.

Author: Agent-8 (SSOT & System Integration Specialist)
License: MIT
V2 Compliance: ≤400 lines, simple data classes, basic validation
"""

import argparse
import json
import logging
import sys
import time
from pathlib import Path
from typing import Dict, Any, Optional

# Import existing memory leak infrastructure
from src.services.messaging.memory_leak_analyzer import MessagingSystemMemoryAnalyzer
from src.services.messaging.memory_leak_fixes import MemoryLeakFixer
from src.services.messaging.memory_leak_analysis_report import MemoryLeakAnalysisReport

logger = logging.getLogger(__name__)


class MemoryMonitorCLI:
    """CLI interface for memory monitoring and leak detection"""
    
    def __init__(self):
        """Initialize memory monitor CLI"""
        self.analyzer = MessagingSystemMemoryAnalyzer()
        self.fixer = MemoryLeakFixer()
        self.report_generator = MemoryLeakAnalysisReport()
    
    def report_command(self, output_file: Optional[str] = None, format: str = 'json') -> int:
        """Generate memory leak analysis report"""
        logger.info("Generating memory leak analysis report")
        
        try:
            # Run comprehensive analysis
            analysis = self.analyzer.analyze_messaging_system()
            
            # Generate detailed report
            report = self.report_generator.generate_report()
            
            # Combine analysis and report
            full_report = {
                'analysis': analysis,
                'detailed_report': report,
                'timestamp': time.time()
            }
            
            # Output report
            if output_file:
                self._write_report(full_report, output_file, format)
                print(f"✅ Report saved to: {output_file}")
            else:
                self._print_report(full_report, format)
            
            return 0
            
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            print(f"❌ Error: {e}")
            return 1
    
    def watch_command(self, interval: int = 60, duration: int = 0) -> int:
        """Watch memory usage in real-time"""
        logger.info(f"Starting memory watch (interval: {interval}s)")
        
        try:
            # Start cleanup service
            self.fixer.start_cleanup_service()
            
            start_time = time.time()
            iterations = 0
            
            print("🔍 Memory Watch Started")
            print(f"Interval: {interval}s | Duration: {'infinite' if duration == 0 else f'{duration}s'}")
            print("-" * 80)
            
            while True:
                # Check if duration limit reached
                if duration > 0 and (time.time() - start_time) > duration:
                    break
                
                # Take snapshot and analyze
                snapshot = self.analyzer.leak_detector.take_snapshot(f"watch_{iterations}")
                
                # Get current stats
                resource_stats = self.analyzer.resource_manager.get_resource_stats()
                file_stats = self.analyzer.file_manager.get_handle_stats()
                
                # Display current status
                print(f"\n📊 Iteration {iterations} ({time.strftime('%H:%M:%S')})")
                print(f"  Memory: {snapshot['memory_usage'] / (1024*1024):.2f} MB")
                print(f"  Objects: {snapshot['object_count']}")
                print(f"  Resources: {resource_stats['total_resources']}")
                print(f"  File Handles: {file_stats['total_handles']}")
                
                # Detect leaks
                leaks = self.analyzer.leak_detector.detect_leaks()
                if leaks:
                    print(f"  ⚠️ Potential Leaks: {len(leaks)}")
                
                iterations += 1
                time.sleep(interval)
            
            # Stop cleanup service
            self.fixer.stop_cleanup_service()
            
            print(f"\n✅ Memory watch completed ({iterations} iterations)")
            return 0
            
        except KeyboardInterrupt:
            print("\n\n⏸️ Memory watch stopped by user")
            self.fixer.stop_cleanup_service()
            return 0
        except Exception as e:
            logger.error(f"Error during watch: {e}")
            print(f"❌ Error: {e}")
            self.fixer.stop_cleanup_service()
            return 1
    
    def cleanup_command(self) -> int:
        """Run manual cleanup of memory resources"""
        logger.info("Running manual memory cleanup")
        
        try:
            # Cleanup coordination requests
            coord_cleaned = self.fixer.coordination_manager.cleanup_old_requests(max_age_hours=1)
            
            # Cleanup PyAutoGUI resources
            pyautogui_cleaned = self.fixer.pyautogui_manager.cleanup_stale_sessions(max_age_seconds=300)
            
            # Cleanup file resources
            file_cleaned = self.fixer.file_manager.cleanup_stale_files(max_age_seconds=60)
            
            # Cleanup expired resources
            resource_cleaned = self.analyzer.resource_manager.cleanup_expired_resources(max_age_seconds=3600)
            
            print("🧹 Memory Cleanup Complete")
            print(f"  Coordination Requests: {coord_cleaned} cleaned")
            print(f"  PyAutoGUI Sessions: {pyautogui_cleaned} cleaned")
            print(f"  File Resources: {file_cleaned} cleaned")
            print(f"  Expired Resources: {resource_cleaned} cleaned")
            print(f"  Total Cleaned: {coord_cleaned + pyautogui_cleaned + file_cleaned + resource_cleaned}")
            
            return 0
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
            print(f"❌ Error: {e}")
            return 1
    
    def status_command(self) -> int:
        """Show current memory status"""
        logger.info("Getting memory status")
        
        try:
            # Take current snapshot
            snapshot = self.analyzer.leak_detector.take_snapshot("status_check")
            
            # Get stats
            resource_stats = self.analyzer.resource_manager.get_resource_stats()
            file_stats = self.analyzer.file_manager.get_handle_stats()
            
            print("📊 Current Memory Status")
            print("-" * 80)
            print(f"Memory Usage: {snapshot['memory_usage'] / (1024*1024):.2f} MB")
            print(f"Object Count: {snapshot['object_count']}")
            print(f"GC Counts: {snapshot['gc_counts']}")
            print(f"\nResource Stats:")
            print(f"  Total Resources: {resource_stats['total_resources']}")
            print(f"  Active Resources: {resource_stats['active_count']}")
            print(f"\nFile Handle Stats:")
            print(f"  Total Handles: {file_stats['total_handles']}")
            print(f"  Open Handles: {file_stats['open_count']}")
            
            # Check for leaks
            leaks = self.analyzer.leak_detector.detect_leaks()
            if leaks:
                print(f"\n⚠️ Potential Memory Leaks Detected: {len(leaks)}")
                for leak in leaks[:3]:  # Show first 3
                    print(f"  - {leak['message']}")
            else:
                print(f"\n✅ No Memory Leaks Detected")
            
            return 0
            
        except Exception as e:
            logger.error(f"Error getting status: {e}")
            print(f"❌ Error: {e}")
            return 1
    
    def _write_report(self, report: Dict[str, Any], output_file: str, format: str) -> None:
        """Write report to file"""
        output_path = Path(output_file)
        
        if format == 'json':
            with open(output_path, 'w') as f:
                json.dump(report, f, indent=2)
        else:  # text format
            with open(output_path, 'w') as f:
                f.write("Memory Leak Analysis Report\n")
                f.write("=" * 80 + "\n\n")
                f.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(report['timestamp']))}\n\n")
                
                # Write analysis summary
                analysis = report['analysis']
                f.write(f"Memory Usage: {analysis['baseline_memory'] / (1024*1024):.2f} MB\n")
                f.write(f"Detected Leaks: {len(analysis['detected_leaks'])}\n\n")
                
                # Write detailed report
                detailed = report['detailed_report']
                f.write(f"Critical Issues: {len(detailed['critical_issues'])}\n")
                f.write(f"Moderate Issues: {len(detailed['moderate_issues'])}\n")
                f.write(f"Minor Issues: {len(detailed['minor_issues'])}\n\n")
                
                # Write recommendations
                f.write("Recommendations:\n")
                for rec in analysis['recommendations']:
                    f.write(f"  - {rec}\n")
    
    def _print_report(self, report: Dict[str, Any], format: str) -> None:
        """Print report to console"""
        if format == 'json':
            print(json.dumps(report, indent=2))
        else:
            print("📊 Memory Leak Analysis Report")
            print("=" * 80)
            print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(report['timestamp']))}\n")
            
            analysis = report['analysis']
            print(f"Memory Usage: {analysis['baseline_memory'] / (1024*1024):.2f} MB")
            print(f"Detected Leaks: {len(analysis['detected_leaks'])}\n")
            
            detailed = report['detailed_report']
            print(f"Critical Issues: {len(detailed['critical_issues'])}")
            print(f"Moderate Issues: {len(detailed['moderate_issues'])}")
            print(f"Minor Issues: {len(detailed['minor_issues'])}\n")
            
            print("Recommendations:")
            for rec in analysis['recommendations']:
                print(f"  - {rec}")


def main(argv=None):
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Memory Monitoring CLI - Phase 4",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Report command
    report_parser = subparsers.add_parser('report', help='Generate memory leak report')
    report_parser.add_argument('--output', '-o', help='Output file path')
    report_parser.add_argument('--format', '-f', choices=['json', 'text'], default='json', help='Output format')
    
    # Watch command
    watch_parser = subparsers.add_parser('watch', help='Watch memory usage in real-time')
    watch_parser.add_argument('--interval', '-i', type=int, default=60, help='Check interval in seconds')
    watch_parser.add_argument('--duration', '-d', type=int, default=0, help='Total duration in seconds (0 = infinite)')
    
    # Cleanup command
    subparsers.add_parser('cleanup', help='Run manual memory cleanup')
    
    # Status command
    subparsers.add_parser('status', help='Show current memory status')
    
    args = parser.parse_args(argv)
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Initialize CLI
    cli = MemoryMonitorCLI()
    
    # Execute command
    if args.command == 'report':
        return cli.report_command(args.output, args.format)
    elif args.command == 'watch':
        return cli.watch_command(args.interval, args.duration)
    elif args.command == 'cleanup':
        return cli.cleanup_command()
    elif args.command == 'status':
        return cli.status_command()
    
    return 0


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    sys.exit(main())

