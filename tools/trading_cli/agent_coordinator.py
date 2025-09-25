#!/usr/bin/env python3
"""
Agent Coordination CLI Tool
===========================

Coordinate multiple agents for better trading predictions
V2 Compliant: ≤400 lines, focused agent coordination
"""

import argparse
import json
import subprocess
import sys
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

# Add the project root to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from tsla_forecast_app.modules import TradingFlagEngine, TradingFlag, AgentFlag, FlagType, FlagStrength


class AgentCoordinator:
    """Coordinate multiple agents for trading predictions"""

    def __init__(self):
        """Initialize agent coordinator"""
        self.flag_engine = TradingFlagEngine()
        self.agent_weights = self._load_agent_weights()

    def _load_agent_weights(self) -> Dict[str, float]:
        """Load agent weights for consensus calculation"""
        return {
            'agent_1': 1.0,  # Equal weight for all agents
            'agent_2': 1.0,
            'agent_3': 1.0,
            'agent_4': 1.0,
            'agent_5': 1.0,
            'agent_6': 1.0,
            'agent_7': 1.0,
            'agent_8': 1.0
        }

    def run_market_analysis(self, symbol: str = "TSLA") -> Dict[str, Any]:
        """Run market analysis using the market analyzer tool"""
        try:
            print(f"🔍 Running market analysis for {symbol}...")
            
            # Run market analyzer
            cmd = [
                sys.executable, 
                os.path.join(os.path.dirname(__file__), 'market_analyzer.py'),
                '--symbol', symbol,
                '--output', f'/tmp/market_analysis_{symbol}.json'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                # Read the analysis results
                with open(f'/tmp/market_analysis_{symbol}.json', 'r') as f:
                    return json.load(f)
            else:
                print(f"Market analysis failed: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"Error running market analysis: {e}")
            return None

    def run_news_analysis(self, symbol: str = "TSLA") -> Dict[str, Any]:
        """Run news sentiment analysis"""
        try:
            print(f"📰 Running news analysis for {symbol}...")
            
            # Run news analyzer
            cmd = [
                sys.executable,
                os.path.join(os.path.dirname(__file__), 'news_analyzer.py'),
                '--symbol', symbol,
                '--output', f'/tmp/news_analysis_{symbol}.json'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                # Read the analysis results
                with open(f'/tmp/news_analysis_{symbol}.json', 'r') as f:
                    return json.load(f)
            else:
                print(f"News analysis failed: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"Error running news analysis: {e}")
            return None

    def run_technical_analysis(self, symbol: str = "TSLA") -> Dict[str, Any]:
        """Run technical analysis"""
        try:
            print(f"📊 Running technical analysis for {symbol}...")
            
            # Run technical analyzer
            cmd = [
                sys.executable,
                os.path.join(os.path.dirname(__file__), 'technical_analyzer.py'),
                '--symbol', symbol,
                '--output', f'/tmp/technical_analysis_{symbol}.json'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                # Read the analysis results
                with open(f'/tmp/technical_analysis_{symbol}.json', 'r') as f:
                    return json.load(f)
            else:
                print(f"Technical analysis failed: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"Error running technical analysis: {e}")
            return None

    def generate_agent_predictions(self, analyses: Dict[str, Any]) -> List[TradingFlag]:
        """Generate predictions from all agents based on comprehensive analysis"""
        print("🤖 Generating agent predictions...")
        
        # Extract data from analyses
        market_data = analyses.get('market_analysis', {})
        news_data = analyses.get('news_analysis', {})
        technical_data = analyses.get('technical_analysis', {})
        
        # Create enhanced market analysis
        enhanced_analysis = self._create_enhanced_analysis(market_data, news_data, technical_data)
        
        # Generate agent flags
        flags = self.flag_engine.generate_all_agent_flags(enhanced_analysis)
        
        return flags

    def _create_enhanced_analysis(self, market_data: Dict, news_data: Dict, technical_data: Dict) -> Any:
        """Create enhanced market analysis from multiple sources"""
        # This would create a more sophisticated analysis combining all data sources
        # For now, we'll use the market data as the base
        
        if market_data and 'market_data' in market_data:
            return self.flag_engine.analyze_market_data(market_data['market_data']['stock'])
        
        # Fallback to basic analysis
        return self.flag_engine.analyze_market_data({
            'price': 200.0,
            'change': 0.0,
            'change_percent': 0.0,
            'volume': 1000000
        })

    def calculate_weighted_consensus(self, flags: List[TradingFlag]) -> TradingFlag:
        """Calculate weighted consensus from agent predictions"""
        print("⚖️ Calculating weighted consensus...")
        
        if not flags:
            return None
        
        # Group flags by type
        flag_groups = {}
        for flag in flags:
            flag_type = flag.flag_type.value
            if flag_type not in flag_groups:
                flag_groups[flag_type] = []
            flag_groups[flag_type].append(flag)
        
        # Calculate weighted averages for each flag type
        weighted_flags = {}
        for flag_type, flag_list in flag_groups.items():
            total_weight = 0
            weighted_price = 0
            weighted_confidence = 0
            
            for flag in flag_list:
                weight = self.agent_weights.get(flag.agent_id.value, 1.0)
                total_weight += weight
                weighted_price += flag.price_target * weight
                weighted_confidence += flag.confidence * weight
            
            if total_weight > 0:
                weighted_flags[flag_type] = {
                    'price_target': weighted_price / total_weight,
                    'confidence': weighted_confidence / total_weight,
                    'weight': total_weight
                }
        
        # Find the flag type with highest weight
        if not weighted_flags:
            return flags[0]  # Fallback to first flag
        
        best_flag_type = max(weighted_flags.keys(), key=lambda x: weighted_flags[x]['weight'])
        best_data = weighted_flags[best_flag_type]
        
        # Create consensus flag
        consensus = TradingFlag(
            flag_id=f"consensus_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            flag_type=FlagType(best_flag_type),
            strength=FlagStrength.STRONG,
            agent_id=flags[0].agent_id,  # Use first agent's ID for consensus
            price_target=best_data['price_target'],
            confidence=best_data['confidence'],
            reasoning=f"Weighted consensus from {len(flags)} agents: {best_flag_type.upper()} signal with {best_data['confidence']:.1%} confidence",
            timestamp=datetime.now().isoformat(),
            expires_at=(datetime.now() + timedelta(hours=24)).isoformat(),
            metadata={'consensus': True, 'agent_count': len(flags)}
        )
        
        return consensus

    def run_comprehensive_analysis(self, symbol: str = "TSLA") -> Dict[str, Any]:
        """Run comprehensive analysis using all tools"""
        print(f"🚀 Running comprehensive analysis for {symbol}...")
        print("=" * 60)
        
        # Run all analyses
        market_analysis = self.run_market_analysis(symbol)
        news_analysis = self.run_news_analysis(symbol)
        technical_analysis = self.run_technical_analysis(symbol)
        
        # Combine analyses
        combined_analyses = {
            'market_analysis': market_analysis,
            'news_analysis': news_analysis,
            'technical_analysis': technical_analysis,
            'timestamp': datetime.now().isoformat(),
            'symbol': symbol
        }
        
        # Generate agent predictions
        agent_flags = self.generate_agent_predictions(combined_analyses)
        
        # Calculate weighted consensus
        consensus = self.calculate_weighted_consensus(agent_flags)
        
        # Create final result
        result = {
            'symbol': symbol,
            'timestamp': datetime.now().isoformat(),
            'analyses': combined_analyses,
            'agent_predictions': [
                {
                    'agent': flag.agent_id.value,
                    'action': flag.flag_type.value,
                    'target': flag.price_target,
                    'confidence': flag.confidence,
                    'reasoning': flag.reasoning
                }
                for flag in agent_flags
            ],
            'consensus': {
                'action': consensus.flag_type.value if consensus else 'hold',
                'target': consensus.price_target if consensus else 0,
                'confidence': consensus.confidence if consensus else 0,
                'reasoning': consensus.reasoning if consensus else 'No consensus available'
            }
        }
        
        return result

    def display_comprehensive_results(self, result: Dict[str, Any]):
        """Display comprehensive analysis results"""
        if not result:
            print("❌ No analysis results available")
            return
        
        print(f"\n🚀 COMPREHENSIVE ANALYSIS: {result['symbol']}")
        print("=" * 60)
        
        # Market Analysis Summary
        market = result['analyses'].get('market_analysis', {})
        if market and 'market_data' in market:
            stock = market['market_data']['stock']
            print(f"📊 Current Price: ${stock['price']:.2f}")
            print(f"📈 Change: ${stock['change']:.2f} ({stock['change_percent']:.2f}%)")
            print(f"📊 Volume: {stock['volume']:,}")
        
        # News Analysis Summary
        news = result['analyses'].get('news_analysis', {})
        if news:
            print(f"\n📰 News Sentiment: {news.get('overall_sentiment', 'unknown').upper()}")
            print(f"📈 Sentiment Score: {news.get('sentiment_score', 0):.3f}")
            print(f"📰 Articles Analyzed: {news.get('total_articles', 0)}")
        
        # Technical Analysis Summary
        technical = result['analyses'].get('technical_analysis', {})
        if technical:
            indicators = technical.get('indicators', {})
            print(f"\n📊 Technical Indicators:")
            print(f"  RSI: {indicators.get('rsi', 0):.1f}")
            print(f"  MACD: {indicators.get('macd', 0):.3f}")
            print(f"  SMA 20: ${indicators.get('sma_20', 0):.2f}")
            
            signals = technical.get('signals', {})
            print(f"  Trading Signals: {signals.get('total_signals', 0)}")
            print(f"  Buy Signals: {signals.get('buy_signals', 0)}")
            print(f"  Sell Signals: {signals.get('sell_signals', 0)}")
        
        # Agent Predictions
        print(f"\n🤖 AGENT PREDICTIONS:")
        for i, pred in enumerate(result['agent_predictions'], 1):
            print(f"  {i}. {pred['agent']}: {pred['action'].upper()} → ${pred['target']:.2f} ({pred['confidence']:.1%})")
        
        # Final Consensus
        consensus = result['consensus']
        print(f"\n🎯 FINAL CONSENSUS:")
        print(f"  Action: {consensus['action'].upper()}")
        print(f"  Target: ${consensus['target']:.2f}")
        print(f"  Confidence: {consensus['confidence']:.1%}")
        print(f"  Reasoning: {consensus['reasoning']}")


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(description="Agent Coordination Tool")
    parser.add_argument("--symbol", "-s", default="TSLA", help="Stock symbol to analyze")
    parser.add_argument("--output", "-o", help="Output file for analysis results")
    parser.add_argument("--quick", action="store_true", help="Quick analysis (skip some tools)")
    
    args = parser.parse_args()
    
    # Create coordinator
    coordinator = AgentCoordinator()
    
    # Run comprehensive analysis
    result = coordinator.run_comprehensive_analysis(args.symbol)
    
    if result:
        # Display results
        coordinator.display_comprehensive_results(result)
        
        # Save to file if requested
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\n💾 Analysis saved to {args.output}")
    else:
        print(f"❌ Could not complete analysis for {args.symbol}")
        sys.exit(1)


if __name__ == "__main__":
    main()