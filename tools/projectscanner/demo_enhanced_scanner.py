#!/usr/bin/env python3
"""
Enhanced Project Scanner Demo
============================

Demonstrates the enhanced project scanner capabilities with advanced
language analysis, agent categorization, and swarm intelligence features.
"""

import logging
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from tools.projectscanner import EnhancedProjectScanner

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)


def demo_enhanced_scanner():
    """Demonstrate enhanced scanner capabilities."""
    logger.info("🚀 Enhanced Project Scanner Demo Starting...")
    
    # Initialize enhanced scanner
    scanner = EnhancedProjectScanner(project_root=project_root)
    
    # Add some ignore directories for demo
    scanner.add_ignore_directory("temp")
    scanner.add_ignore_directory("logs")
    
    # Progress callback for demo
    def progress_callback(percent: int):
        if percent % 25 == 0:  # Log every 25%
            logger.info(f"📊 Demo scan progress: {percent}%")
    
    logger.info("🔍 Running enhanced project scan...")
    
    # Run enhanced scan
    scanner.scan_project(
        progress_callback=progress_callback,
        num_workers=4,
        file_extensions={'.py', '.md', '.json'}  # Limited for demo
    )
    
    logger.info("📝 Generating enhanced reports...")
    
    # Generate additional outputs
    scanner.generate_init_files(overwrite=False)  # Don't overwrite existing
    scanner.export_chatgpt_context()
    
    # Get and display analysis summary
    logger.info("📊 Analysis Summary:")
    summary = scanner.get_analysis_summary()
    
    if "error" not in summary:
        logger.info(f"  📁 Total files analyzed: {summary['total_files']}")
        logger.info(f"  🌐 Languages found: {list(summary['languages'].keys())}")
        logger.info(f"  🤖 Agent types: {list(summary['agent_types'].keys())}")
        logger.info(f"  📈 Maturity levels: {list(summary['maturity_levels'].keys())}")
        logger.info(f"  ✅ V2 Compliance: {summary['v2_compliance']['compliance_rate']:.1f}%")
        logger.info(f"  🔧 Total complexity: {summary['total_complexity']}")
        logger.info(f"  📏 Average complexity: {summary['average_complexity']:.1f}")
    else:
        logger.error(f"Analysis error: {summary['error']}")
    
    # Display cache statistics
    logger.info("💾 Cache Statistics:")
    cache_stats = scanner.get_cache_stats()
    logger.info(f"  📦 Cache size: {cache_stats['cache_size']} files")
    logger.info(f"  📄 Cache file: {cache_stats['cache_file']}")
    logger.info(f"  🗂️ Ignored directories: {len(cache_stats['ignored_directories'])}")
    
    # Show some example analysis results
    logger.info("🔍 Sample Analysis Results:")
    sample_files = list(scanner.analysis.keys())[:3]  # Show first 3 files
    
    for file_path in sample_files:
        analysis = scanner.analysis[file_path]
        logger.info(f"  📄 {file_path}:")
        logger.info(f"    Language: {analysis.get('language', 'unknown')}")
        logger.info(f"    Complexity: {analysis.get('complexity', 0)}")
        logger.info(f"    Functions: {len(analysis.get('functions', []))}")
        logger.info(f"    Classes: {len(analysis.get('classes', {}))}")
        logger.info(f"    Routes: {len(analysis.get('routes', []))}")
        logger.info(f"    Maturity: {analysis.get('maturity', 'Unknown')}")
        logger.info(f"    Agent Type: {analysis.get('agent_type', 'Unknown')}")
    
    logger.info("🎉 Enhanced Project Scanner Demo Complete!")
    logger.info("🐝 WE. ARE. SWARM. Enhanced scanner demonstration successful! ⚡️🔥")


if __name__ == "__main__":
    try:
        demo_enhanced_scanner()
    except KeyboardInterrupt:
        logger.info("⏹️ Demo interrupted by user")
    except Exception as e:
        logger.error(f"❌ Demo failed: {e}")
        sys.exit(1)

