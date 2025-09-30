#!/usr/bin/env python3
"""
Technical Analyzer Main
=======================

CLI interface and main function for technical analysis tool.

Author: Agent-7 (Implementation Specialist)
License: MIT
"""

import argparse
import json
import sys

from .technical_analyzer_core import TechnicalAnalyzer


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Advanced Technical Analysis Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python technical_analyzer.py --symbol TSLA --days 30
  python technical_analyzer.py --symbol AAPL --days 60 --output analysis.json
  python technical_analyzer.py --symbol MSFT --days 90 --format json
        """,
    )

    parser.add_argument(
        "--symbol",
        default="TSLA",
        help="Stock symbol to analyze (default: TSLA)",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=30,
        help="Number of days of historical data (default: 30)",
    )
    parser.add_argument(
        "--output",
        help="Output file for analysis results (JSON format)",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output",
    )

    args = parser.parse_args()

    if args.verbose:
        print(f"[INFO] Starting technical analysis for {args.symbol}")
        print(f"[INFO] Analyzing {args.days} days of data")
        print(f"[INFO] Output format: {args.format}")

    try:
        # Initialize analyzer
        analyzer = TechnicalAnalyzer()

        # Perform analysis
        analysis = analyzer.analyze_technical(args.symbol, args.days)

        if "error" in analysis:
            print(f"[ERROR] Analysis failed: {analysis['error']}")
            sys.exit(1)

        # Output results
        if args.format == "json":
            output_data = {
                "symbol": analysis["symbol"],
                "analysis_date": analysis["analysis_date"],
                "current_price": analysis["current_price"],
                "technical_indicators": analysis["technical_indicators"],
                "trading_signals": analysis["trading_signals"],
                "summary": analysis["summary"],
            }

            if args.output:
                with open(args.output, "w") as f:
                    json.dump(output_data, f, indent=2)
                print(f"[SUCCESS] Analysis saved to {args.output}")
            else:
                print(json.dumps(output_data, indent=2))

        else:  # text format
            analyzer.display_technical_analysis(analysis)

            if args.output:
                # Save text output to file
                with open(args.output, "w") as f:
                    f.write(f"Technical Analysis: {analysis['symbol']}\n")
                    f.write(f"Analysis Date: {analysis['analysis_date']}\n")
                    f.write(f"Current Price: ${analysis['current_price']:.2f}\n\n")

                    # Write technical indicators
                    indicators = analysis["technical_indicators"]
                    f.write("Technical Indicators:\n")
                    f.write(f"  SMA (20): ${indicators['sma_20']:.2f}\n")
                    f.write(f"  EMA (12): ${indicators['ema_12']:.2f}\n")
                    f.write(f"  RSI (14): {indicators['rsi_14']:.2f}\n")
                    f.write(f"  MACD: {indicators['macd']['macd']:.4f}\n")
                    f.write(f"  MACD Signal: {indicators['macd']['signal']:.4f}\n")
                    f.write(f"  MACD Histogram: {indicators['macd']['histogram']:.4f}\n\n")

                    # Write Bollinger Bands
                    bb = indicators["bollinger_bands"]
                    f.write("Bollinger Bands:\n")
                    f.write(f"  Upper Band: ${bb['upper']:.2f}\n")
                    f.write(f"  Middle Band: ${bb['middle']:.2f}\n")
                    f.write(f"  Lower Band: ${bb['lower']:.2f}\n\n")

                    # Write Stochastic
                    stoch = indicators["stochastic"]
                    f.write("Stochastic Oscillator:\n")
                    f.write(f"  %K: {stoch['k_percent']:.2f}\n")
                    f.write(f"  %D: {stoch['d_percent']:.2f}\n\n")

                    # Write trading signals
                    signals = analysis["trading_signals"]
                    f.write("Trading Signals:\n")
                    f.write(f"  Overall Signal: {signals['overall_signal']}\n")
                    f.write(f"  Signal Strength: {signals['signal_strength']}\n")
                    f.write(f"  Trend Direction: {signals['trend_direction']}\n\n")

                    # Write summary
                    f.write("Analysis Summary:\n")
                    f.write(f"  {analysis['summary']}\n")

                print(f"[SUCCESS] Analysis saved to {args.output}")

        if args.verbose:
            print(f"[INFO] Analysis completed successfully for {args.symbol}")

    except KeyboardInterrupt:
        print("\n[INFO] Analysis interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        if args.verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


# For direct execution
if __name__ == "__main__":
    main()
