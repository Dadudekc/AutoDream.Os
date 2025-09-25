#!/usr/bin/env python3
"""
Master CLI Tool for Trading Predictions
========================================

Master command-line interface for all trading prediction tools
V2 Compliant: ≤400 lines, focused CLI coordination
"""

import argparse
import subprocess
import sys
import os
from datetime import datetime
from typing import Dict, List, Any

# Add the project root to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))


class MasterCLI:
    """Master CLI for trading prediction tools"""

    def __init__(self):
        """Initialize master CLI"""
        self.tools = {
            'market': 'market_analyzer.py',
            'news': 'news_analyzer.py',
            'technical': 'technical_analyzer.py',
            'coordinator': 'agent_coordinator.py',
            'tracker': 'prediction_tracker.py'
        }

    def run_tool(self, tool_name: str, args: List[str]) -> bool:
        """Run a specific tool with arguments"""
        if tool_name not in self.tools:
            print(f"❌ Unknown tool: {tool_name}")
            print(f"Available tools: {', '.join(self.tools.keys())}")
            return False
        
        tool_path = os.path.join(os.path.dirname(__file__), self.tools[tool_name])
        
        try:
            cmd = [sys.executable, tool_path] + args
            result = subprocess.run(cmd, timeout=300)  # 5 minute timeout
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            print(f"⏰ Tool {tool_name} timed out")
            return False
        except Exception as e:
            print(f"❌ Error running {tool_name}: {e}")
            return False

    def run_comprehensive_analysis(self, symbol: str = "TSLA", output_dir: str = None):
        """Run comprehensive analysis using all tools"""
        print(f"🚀 Running comprehensive analysis for {symbol}...")
        print("=" * 60)
        
        if not output_dir:
            output_dir = f"analysis_{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        os.makedirs(output_dir, exist_ok=True)
        
        results = {}
        
        # Run market analysis
        print("📊 Running market analysis...")
        success = self.run_tool('market', ['--symbol', symbol, '--output', f'{output_dir}/market_analysis.json'])
        results['market'] = success
        
        # Run news analysis
        print("📰 Running news analysis...")
        success = self.run_tool('news', ['--symbol', symbol, '--output', f'{output_dir}/news_analysis.json'])
        results['news'] = success
        
        # Run technical analysis
        print("📈 Running technical analysis...")
        success = self.run_tool('technical', ['--symbol', symbol, '--output', f'{output_dir}/technical_analysis.json'])
        results['technical'] = success
        
        # Run agent coordination
        print("🤖 Running agent coordination...")
        success = self.run_tool('coordinator', ['--symbol', symbol, '--output', f'{output_dir}/agent_coordination.json'])
        results['coordinator'] = success
        
        # Display results summary
        print(f"\n📋 ANALYSIS SUMMARY:")
        print("=" * 30)
        for tool, success in results.items():
            status = "✅" if success else "❌"
            print(f"  {status} {tool.title()} Analysis")
        
        successful_tools = sum(results.values())
        total_tools = len(results)
        
        print(f"\n🎯 Overall Success: {successful_tools}/{total_tools} tools completed")
        print(f"📁 Results saved to: {output_dir}/")
        
        return results

    def run_quick_analysis(self, symbol: str = "TSLA"):
        """Run quick analysis using coordinator tool"""
        print(f"⚡ Running quick analysis for {symbol}...")
        return self.run_tool('coordinator', ['--symbol', symbol])

    def show_help(self):
        """Show comprehensive help"""
        print("🚀 MASTER CLI TOOL FOR TRADING PREDICTIONS")
        print("=" * 50)
        print()
        print("📋 AVAILABLE COMMANDS:")
        print("  comprehensive <symbol>  - Run full analysis with all tools")
        print("  quick <symbol>          - Run quick analysis")
        print("  market <symbol>         - Run market analysis only")
        print("  news <symbol>           - Run news sentiment analysis")
        print("  technical <symbol>      - Run technical analysis")
        print("  coordinator <symbol>    - Run agent coordination")
        print("  tracker <symbol>       - Show prediction accuracy")
        print("  help                    - Show this help")
        print()
        print("📊 AVAILABLE TOOLS:")
        for tool, script in self.tools.items():
            print(f"  {tool:<12} - {script}")
        print()
        print("💡 EXAMPLES:")
        print("  python master_cli.py comprehensive TSLA")
        print("  python master_cli.py quick AAPL")
        print("  python master_cli.py market TSLA")
        print("  python master_cli.py tracker TSLA")
        print()
        print("🔧 TOOL-SPECIFIC OPTIONS:")
        print("  Use --help with any tool to see its specific options")
        print("  Example: python market_analyzer.py --help")

    def interactive_mode(self):
        """Run interactive mode"""
        print("🚀 MASTER CLI - INTERACTIVE MODE")
        print("=" * 40)
        print("Type 'help' for commands, 'quit' to exit")
        print()
        
        while True:
            try:
                command = input("master_cli> ").strip().split()
                
                if not command:
                    continue
                
                if command[0].lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                elif command[0].lower() == 'help':
                    self.show_help()
                
                elif command[0].lower() == 'comprehensive':
                    symbol = command[1] if len(command) > 1 else "TSLA"
                    self.run_comprehensive_analysis(symbol)
                
                elif command[0].lower() == 'quick':
                    symbol = command[1] if len(command) > 1 else "TSLA"
                    self.run_quick_analysis(symbol)
                
                elif command[0].lower() in self.tools:
                    tool = command[0].lower()
                    args = command[1:] if len(command) > 1 else []
                    self.run_tool(tool, args)
                
                else:
                    print(f"❌ Unknown command: {command[0]}")
                    print("Type 'help' for available commands")
                
                print()  # Add spacing
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(description="Master CLI for Trading Predictions")
    parser.add_argument("command", nargs="?", help="Command to run")
    parser.add_argument("symbol", nargs="?", default="TSLA", help="Stock symbol")
    parser.add_argument("--interactive", "-i", action="store_true", help="Run in interactive mode")
    parser.add_argument("--output", "-o", help="Output directory for comprehensive analysis")
    
    args = parser.parse_args()
    
    # Create master CLI
    master = MasterCLI()
    
    if args.interactive:
        # Run interactive mode
        master.interactive_mode()
    
    elif args.command:
        # Run specific command
        if args.command.lower() == 'comprehensive':
            master.run_comprehensive_analysis(args.symbol, args.output)
        elif args.command.lower() == 'quick':
            master.run_quick_analysis(args.symbol)
        elif args.command.lower() in master.tools:
            master.run_tool(args.command.lower(), ['--symbol', args.symbol])
        elif args.command.lower() == 'help':
            master.show_help()
        else:
            print(f"❌ Unknown command: {args.command}")
            master.show_help()
    
    else:
        # Show help
        master.show_help()


if __name__ == "__main__":
    main()