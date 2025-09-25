#!/usr/bin/env python3
"""
Trading Flags System
====================

Flag-based trading prediction system for agent coordination
V2 Compliant: ≤400 lines, focused trading flag logic
"""

import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class FlagType(Enum):
    """Trading flag types"""
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"
    STRONG_BUY = "strong_buy"
    STRONG_SELL = "strong_sell"


class FlagStrength(Enum):
    """Flag strength levels"""
    WEAK = "weak"
    MODERATE = "moderate"
    STRONG = "strong"
    VERY_STRONG = "very_strong"


class AgentFlag(Enum):
    """Agent-specific flags"""
    AGENT_1 = "agent_1"
    AGENT_2 = "agent_2"
    AGENT_3 = "agent_3"
    AGENT_4 = "agent_4"
    AGENT_5 = "agent_5"
    AGENT_6 = "agent_6"
    AGENT_7 = "agent_7"
    AGENT_8 = "agent_8"


@dataclass
class TradingFlag:
    """Trading flag structure"""
    flag_id: str
    flag_type: FlagType
    strength: FlagStrength
    agent_id: AgentFlag
    price_target: float
    confidence: float
    reasoning: str
    timestamp: str
    expires_at: str
    metadata: Dict[str, Any]


@dataclass
class MarketAnalysis:
    """Market analysis structure"""
    current_price: float
    price_change: float
    volume: int
    volatility: float
    trend_direction: str
    support_level: float
    resistance_level: float
    technical_indicators: Dict[str, Any]


class TradingFlagEngine:
    """Trading flag analysis engine"""

    def __init__(self):
        """Initialize trading flag engine"""
        self.active_flags: List[TradingFlag] = []
        self.flag_history: List[TradingFlag] = []
        self.agent_preferences = self._initialize_agent_preferences()

    def _initialize_agent_preferences(self) -> Dict[AgentFlag, Dict[str, Any]]:
        """Initialize agent trading preferences"""
        return {
            AgentFlag.AGENT_1: {
                "risk_tolerance": "moderate",
                "time_horizon": "short_term",
                "specialization": "technical_analysis"
            },
            AgentFlag.AGENT_2: {
                "risk_tolerance": "conservative",
                "time_horizon": "long_term",
                "specialization": "fundamental_analysis"
            },
            AgentFlag.AGENT_3: {
                "risk_tolerance": "aggressive",
                "time_horizon": "medium_term",
                "specialization": "momentum_trading"
            },
            AgentFlag.AGENT_4: {
                "risk_tolerance": "moderate",
                "time_horizon": "short_term",
                "specialization": "quality_assurance"
            },
            AgentFlag.AGENT_5: {
                "risk_tolerance": "conservative",
                "time_horizon": "long_term",
                "specialization": "business_intelligence"
            },
            AgentFlag.AGENT_6: {
                "risk_tolerance": "moderate",
                "time_horizon": "medium_term",
                "specialization": "coordination"
            },
            AgentFlag.AGENT_7: {
                "risk_tolerance": "aggressive",
                "time_horizon": "short_term",
                "specialization": "testing_validation"
            },
            AgentFlag.AGENT_8: {
                "risk_tolerance": "conservative",
                "time_horizon": "long_term",
                "specialization": "operations"
            }
        }

    def analyze_market_data(self, stock_data: Dict[str, Any]) -> MarketAnalysis:
        """Analyze market data for trading signals"""
        current_price = stock_data.get('price', 0)
        price_change = stock_data.get('change', 0)
        volume = stock_data.get('volume', 0)
        
        # Calculate volatility (simplified)
        volatility = abs(price_change) / current_price if current_price > 0 else 0
        
        # Determine trend direction
        if price_change > 0:
            trend_direction = "bullish"
        elif price_change < 0:
            trend_direction = "bearish"
        else:
            trend_direction = "neutral"
        
        # Calculate support and resistance levels (simplified)
        support_level = current_price * 0.95  # 5% below current price
        resistance_level = current_price * 1.05  # 5% above current price
        
        # Technical indicators (simplified)
        technical_indicators = {
            "rsi": self._calculate_rsi(current_price),
            "macd": self._calculate_macd(current_price),
            "moving_average": self._calculate_moving_average(current_price),
            "volume_trend": "high" if volume > 10000000 else "normal"
        }
        
        return MarketAnalysis(
            current_price=current_price,
            price_change=price_change,
            volume=volume,
            volatility=volatility,
            trend_direction=trend_direction,
            support_level=support_level,
            resistance_level=resistance_level,
            technical_indicators=technical_indicators
        )

    def _calculate_rsi(self, price: float) -> float:
        """Calculate RSI (simplified)"""
        # Mock RSI calculation
        return random.uniform(30, 70)

    def _calculate_macd(self, price: float) -> float:
        """Calculate MACD (simplified)"""
        # Mock MACD calculation
        return random.uniform(-2, 2)

    def _calculate_moving_average(self, price: float) -> float:
        """Calculate moving average (simplified)"""
        # Mock moving average calculation
        return price * random.uniform(0.98, 1.02)

    def generate_agent_flag(self, agent_id: AgentFlag, market_analysis: MarketAnalysis) -> TradingFlag:
        """Generate trading flag for specific agent"""
        agent_prefs = self.agent_preferences[agent_id]
        
        # Determine flag type based on agent specialization and market conditions
        flag_type = self._determine_flag_type(agent_prefs, market_analysis)
        strength = self._determine_flag_strength(market_analysis)
        confidence = self._calculate_confidence(agent_prefs, market_analysis)
        
        # Calculate price target
        price_target = self._calculate_price_target(market_analysis, flag_type)
        
        # Generate reasoning
        reasoning = self._generate_reasoning(agent_prefs, market_analysis, flag_type)
        
        # Create flag
        flag = TradingFlag(
            flag_id=f"{agent_id.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            flag_type=flag_type,
            strength=strength,
            agent_id=agent_id,
            price_target=price_target,
            confidence=confidence,
            reasoning=reasoning,
            timestamp=datetime.now().isoformat(),
            expires_at=(datetime.now() + timedelta(hours=24)).isoformat(),
            metadata={
                "agent_specialization": agent_prefs["specialization"],
                "risk_tolerance": agent_prefs["risk_tolerance"],
                "time_horizon": agent_prefs["time_horizon"]
            }
        )
        
        return flag

    def _determine_flag_type(self, agent_prefs: Dict[str, Any], market_analysis: MarketAnalysis) -> FlagType:
        """Determine flag type based on agent preferences and market analysis"""
        specialization = agent_prefs["specialization"]
        trend = market_analysis.trend_direction
        volatility = market_analysis.volatility
        
        # Agent-specific logic
        if specialization == "technical_analysis":
            if trend == "bullish" and volatility < 0.05:
                return FlagType.BUY
            elif trend == "bearish" and volatility > 0.03:
                return FlagType.SELL
            else:
                return FlagType.HOLD
                
        elif specialization == "fundamental_analysis":
            if market_analysis.current_price < market_analysis.support_level:
                return FlagType.STRONG_BUY
            elif market_analysis.current_price > market_analysis.resistance_level:
                return FlagType.STRONG_SELL
            else:
                return FlagType.HOLD
                
        elif specialization == "momentum_trading":
            if trend == "bullish":
                return FlagType.STRONG_BUY
            elif trend == "bearish":
                return FlagType.STRONG_SELL
            else:
                return FlagType.HOLD
                
        else:
            # Default logic
            if trend == "bullish":
                return FlagType.BUY
            elif trend == "bearish":
                return FlagType.SELL
            else:
                return FlagType.HOLD

    def _determine_flag_strength(self, market_analysis: MarketAnalysis) -> FlagStrength:
        """Determine flag strength based on market conditions"""
        volatility = market_analysis.volatility
        volume = market_analysis.volume
        
        if volatility > 0.05 and volume > 20000000:
            return FlagStrength.VERY_STRONG
        elif volatility > 0.03 and volume > 10000000:
            return FlagStrength.STRONG
        elif volatility > 0.02:
            return FlagStrength.MODERATE
        else:
            return FlagStrength.WEAK

    def _calculate_confidence(self, agent_prefs: Dict[str, Any], market_analysis: MarketAnalysis) -> float:
        """Calculate confidence level for the flag"""
        base_confidence = 0.7
        
        # Adjust based on agent specialization
        specialization = agent_prefs["specialization"]
        if specialization in ["technical_analysis", "fundamental_analysis"]:
            base_confidence += 0.1
        elif specialization == "momentum_trading":
            base_confidence += 0.05
        
        # Adjust based on market conditions
        if market_analysis.volatility < 0.03:
            base_confidence += 0.1
        elif market_analysis.volatility > 0.05:
            base_confidence -= 0.1
        
        return min(0.95, max(0.5, base_confidence))

    def _calculate_price_target(self, market_analysis: MarketAnalysis, flag_type: FlagType) -> float:
        """Calculate price target based on flag type"""
        current_price = market_analysis.current_price
        
        if flag_type in [FlagType.BUY, FlagType.STRONG_BUY]:
            return current_price * 1.08  # 8% upside target
        elif flag_type in [FlagType.SELL, FlagType.STRONG_SELL]:
            return current_price * 0.92  # 8% downside target
        else:
            return current_price  # Hold - no target

    def _generate_reasoning(self, agent_prefs: Dict[str, Any], market_analysis: MarketAnalysis, flag_type: FlagType) -> str:
        """Generate reasoning for the flag"""
        specialization = agent_prefs["specialization"]
        trend = market_analysis.trend_direction
        volatility = market_analysis.volatility
        
        reasoning_parts = []
        
        # Add specialization-based reasoning
        if specialization == "technical_analysis":
            reasoning_parts.append("Technical indicators show")
        elif specialization == "fundamental_analysis":
            reasoning_parts.append("Fundamental analysis indicates")
        elif specialization == "momentum_trading":
            reasoning_parts.append("Momentum analysis suggests")
        else:
            reasoning_parts.append("Market analysis shows")
        
        # Add trend reasoning
        if trend == "bullish":
            reasoning_parts.append("bullish momentum with")
        elif trend == "bearish":
            reasoning_parts.append("bearish pressure with")
        else:
            reasoning_parts.append("neutral conditions with")
        
        # Add volatility reasoning
        if volatility > 0.05:
            reasoning_parts.append("high volatility")
        elif volatility > 0.03:
            reasoning_parts.append("moderate volatility")
        else:
            reasoning_parts.append("low volatility")
        
        # Add flag type reasoning
        if flag_type == FlagType.STRONG_BUY:
            reasoning_parts.append("- Strong buy signal")
        elif flag_type == FlagType.BUY:
            reasoning_parts.append("- Buy signal")
        elif flag_type == FlagType.STRONG_SELL:
            reasoning_parts.append("- Strong sell signal")
        elif flag_type == FlagType.SELL:
            reasoning_parts.append("- Sell signal")
        else:
            reasoning_parts.append("- Hold position")
        
        return " ".join(reasoning_parts)

    def generate_all_agent_flags(self, market_analysis: MarketAnalysis) -> List[TradingFlag]:
        """Generate trading flags for all agents"""
        flags = []
        
        for agent_id in AgentFlag:
            flag = self.generate_agent_flag(agent_id, market_analysis)
            flags.append(flag)
            self.active_flags.append(flag)
        
        return flags

    def get_consensus_flag(self, flags: List[TradingFlag]) -> TradingFlag:
        """Get consensus flag from all agent flags"""
        if not flags:
            return None
        
        # Count flag types
        flag_counts = {}
        for flag in flags:
            flag_type = flag.flag_type
            flag_counts[flag_type] = flag_counts.get(flag_type, 0) + 1
        
        # Find most common flag type
        consensus_type = max(flag_counts, key=flag_counts.get)
        
        # Calculate average confidence and price target
        avg_confidence = sum(flag.confidence for flag in flags) / len(flags)
        avg_price_target = sum(flag.price_target for flag in flags) / len(flags)
        
        # Generate consensus reasoning
        reasoning = f"Consensus from {len(flags)} agents: {consensus_type.value.upper()} signal with {avg_confidence:.1%} confidence"
        
        # Create consensus flag
        consensus_flag = TradingFlag(
            flag_id=f"consensus_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            flag_type=consensus_type,
            strength=FlagStrength.STRONG,  # Consensus is always strong
            agent_id=AgentFlag.AGENT_4,  # Captain agent
            price_target=avg_price_target,
            confidence=avg_confidence,
            reasoning=reasoning,
            timestamp=datetime.now().isoformat(),
            expires_at=(datetime.now() + timedelta(hours=24)).isoformat(),
            metadata={
                "consensus": True,
                "participating_agents": len(flags),
                "flag_distribution": flag_counts
            }
        )
        
        return consensus_flag

    def get_active_flags(self) -> List[TradingFlag]:
        """Get all active trading flags"""
        return self.active_flags

    def get_agent_flags(self, agent_id: AgentFlag) -> List[TradingFlag]:
        """Get flags for specific agent"""
        return [flag for flag in self.active_flags if flag.agent_id == agent_id]

    def expire_old_flags(self):
        """Remove expired flags"""
        current_time = datetime.now()
        self.active_flags = [
            flag for flag in self.active_flags 
            if datetime.fromisoformat(flag.expires_at) > current_time
        ]

    def save_flags_to_file(self, filename: str = None):
        """Save flags to JSON file"""
        if filename is None:
            filename = f"trading_flags_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        flags_data = []
        for flag in self.active_flags:
            flags_data.append({
                "flag_id": flag.flag_id,
                "flag_type": flag.flag_type.value,
                "strength": flag.strength.value,
                "agent_id": flag.agent_id.value,
                "price_target": flag.price_target,
                "confidence": flag.confidence,
                "reasoning": flag.reasoning,
                "timestamp": flag.timestamp,
                "expires_at": flag.expires_at,
                "metadata": flag.metadata
            })
        
        with open(filename, 'w') as f:
            json.dump(flags_data, f, indent=2)
        
        return filename