#!/usr/bin/env python3
"""
Code Archaeologist CLI Tool
==========================

Command-line interface for the code archaeology system.
V2 Compliant: ≤400 lines, focused CLI functionality.

Author: Agent-2 (Architecture Specialist & Code Archaeologist)
License: MIT
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Add project root to Python path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

try:
    from src.services.code_archaeology import CodeArchaeologyService, conduct_code_archaeology
except ImportError:
    print("❌ Code archaeology service not available. Please ensure all dependencies are installed.")
    sys.exit(1)

logger = logging.getLogger(__name__)


class CodeArchaeologistCLI:
    """Command-line interface for code archaeology tools."""
    
    def __init__(self):
        """Initialize the CLI."""
        self.service = CodeArchaeologyService()
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging for the CLI."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def conduct_dig(self, target_path: str, analysis_depth: str = "comprehensive") -> bool:
        """Conduct archaeological dig on target path."""
        try:
            print(f"🔍 Conducting archaeological dig on: {target_path}")
            print(f"📊 Analysis depth: {analysis_depth}")
            
            result = conduct_code_archaeology(target_path, analysis_depth)
            
            if result["status"] == "success":
                findings = result["findings_summary"]
                print(f"✅ Archaeological dig completed successfully!")
                print(f"📈 Evolution stages discovered: {findings['evolution_stages']}")
                print(f"🎯 Patterns discovered: {findings['patterns_discovered']}")
                print(f"💸 Technical debt items mapped: {findings['debt_items_mapped']}")
                print(f"💀 Dead code fragments found: {findings['dead_code_fragments']}")
                
                # Save report
                report_path = f"archaeology_reports/{Path(target_path).name}_dig_report.json"
                Path("archaeology_reports").mkdir(exist_ok=True)
                
                with open(report_path, 'w') as f:
                    json.dump(result["archaeological_report"], f, indent=2)
                
                print(f"📄 Archaeological report saved to: {report_path}")
                return True
            else:
                print(f"❌ Archaeological dig failed: {result.get('message', 'Unknown error')}")
                return False
                
        except Exception as e:
            print(f"❌ Failed to conduct archaeological dig: {e}")
            logger.error(f"Archaeological dig failed: {e}")
            return False
    
    def analyze_evolution(self, target_path: str) -> None:
        """Analyze code evolution over time."""
        try:
            print(f"📈 Analyzing code evolution for: {target_path}")
            
            evolution_analysis = self.service.evolution_tracker.track_evolution(target_path)
            
            if evolution_analysis:
                stages = evolution_analysis.get("stages", [])
                print(f"✅ Evolution analysis completed!")
                print(f"📊 Evolution stages found: {len(stages)}")
                
                for i, stage in enumerate(stages[:5]):  # Show first 5 stages
                    print(f"  Stage {i+1}: {stage.get('description', 'Unknown')} ({stage.get('date', 'Unknown date')})")
                
                if len(stages) > 5:
                    print(f"  ... and {len(stages) - 5} more stages")
                    
        except Exception as e:
            print(f"❌ Evolution analysis failed: {e}")
    
    def discover_patterns(self, target_path: str) -> None:
        """Discover code patterns in target path."""
        try:
            print(f"🎯 Discovering patterns in: {target_path}")
            
            pattern_discoveries = self.service.pattern_discoverer.discover_patterns(target_path)
            
            if pattern_discoveries:
                patterns = pattern_discoveries.get("patterns", [])
                print(f"✅ Pattern discovery completed!")
                print(f"🎭 Patterns discovered: {len(patterns)}")
                
                pattern_types = {}
                for pattern in patterns:
                    pattern_type = pattern.get("type", "unknown")
                    pattern_types[pattern_type] = pattern_types.get(pattern_type, 0) + 1
                
                for pattern_type, count in pattern_types.items():
                    print(f"  {pattern_type}: {count} patterns")
                    
        except Exception as e:
            print(f"❌ Pattern discovery failed: {e}")
    
    def map_technical_debt(self, target_path: str) -> None:
        """Map technical debt in target path."""
        try:
            print(f"💸 Mapping technical debt in: {target_path}")
            
            debt_mapping = self.service.debt_mapper.map_technical_debt(target_path)
            
            if debt_mapping:
                debt_items = debt_mapping.get("debt_items", [])
                print(f"✅ Technical debt mapping completed!")
                print(f"💸 Debt items found: {len(debt_items)}")
                
                debt_categories = {}
                for item in debt_items:
                    category = item.get("category", "unknown")
                    debt_categories[category] = debt_categories.get(category, 0) + 1
                
                for category, count in debt_categories.items():
                    print(f"  {category}: {count} items")
                    
        except Exception as e:
            print(f"❌ Technical debt mapping failed: {e}")
    
    def detect_dead_code(self, target_path: str) -> None:
        """Detect dead code in target path."""
        try:
            print(f"💀 Detecting dead code in: {target_path}")
            
            dead_code_findings = self.service.dead_code_detector.detect_dead_code(target_path)
            
            if dead_code_findings:
                dead_fragments = dead_code_findings.get("dead_fragments", [])
                print(f"✅ Dead code detection completed!")
                print(f"💀 Dead code fragments found: {len(dead_fragments)}")
                
                for fragment in dead_fragments[:5]:  # Show first 5
                    print(f"  {fragment.get('file_path', 'Unknown file')}: {fragment.get('description', 'Unknown')}")
                
                if len(dead_fragments) > 5:
                    print(f"  ... and {len(dead_fragments) - 5} more fragments")
                    
        except Exception as e:
            print(f"❌ Dead code detection failed: {e}")
    
    def show_tools(self) -> None:
        """Show available archaeology tools."""
        try:
            from src.services.code_archaeology import get_archaeology_tools
            tools = get_archaeology_tools()
            
            print("🔍 Available Code Archaeology Tools:")
            print("\n📦 Main Service:")
            print(f"  • {tools['main_service']}")
            
            print("\n🔧 Core Tools:")
            for tool in tools["core_tools"]:
                print(f"  • {tool}")
            
            print("\n🔬 Analyzer Tools:")
            for tool in tools["analyzer_tools"]:
                print(f"  • {tool}")
            
            print("\n📊 Reporter Tools:")
            for tool in tools["reporter_tools"]:
                print(f"  • {tool}")
            
            print("\n🔗 Integration Tools:")
            for tool in tools["integration_tools"]:
                print(f"  • {tool}")
            
            print("\n💡 Convenience Functions:")
            for func in tools["convenience_functions"]:
                print(f"  • {func}")
                
        except Exception as e:
            print(f"❌ Failed to show tools: {e}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Code Archaeologist CLI Tool")
    parser.add_argument("--conduct-dig", metavar="PATH", help="Conduct archaeological dig on target path")
    parser.add_argument("--analysis-depth", choices=["quick", "standard", "comprehensive"], default="comprehensive", help="Analysis depth")
    parser.add_argument("--analyze-evolution", metavar="PATH", help="Analyze code evolution over time")
    parser.add_argument("--discover-patterns", metavar="PATH", help="Discover code patterns")
    parser.add_argument("--map-debt", metavar="PATH", help="Map technical debt")
    parser.add_argument("--detect-dead-code", metavar="PATH", help="Detect dead code")
    parser.add_argument("--show-tools", action="store_true", help="Show available archaeology tools")
    
    args = parser.parse_args()
    
    cli = CodeArchaeologistCLI()
    
    if args.conduct_dig:
        success = cli.conduct_dig(args.conduct_dig, args.analysis_depth)
        sys.exit(0 if success else 1)
    elif args.analyze_evolution:
        cli.analyze_evolution(args.analyze_evolution)
    elif args.discover_patterns:
        cli.discover_patterns(args.discover_patterns)
    elif args.map_debt:
        cli.map_debt(args.map_debt)
    elif args.detect_dead_code:
        cli.detect_dead_code(args.detect_dead_code)
    elif args.show_tools:
        cli.show_tools()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
