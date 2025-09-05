#!/usr/bin/env python3
"""
TSLA ATR Pullback Backtest Orchestrator
=======================================

Main orchestrator for TSLA ATR Pullback strategy backtesting.
Coordinates all backtest components and provides unified interface.
V2 COMPLIANT: Focused orchestration under 300 lines.

@version 1.0.0 - V2 COMPLIANCE MODULAR ORCHESTRATOR
@license MIT
"""

import pandas as pd
from typing import Dict, Any, Optional
from datetime import datetime

from .data_management_engine import DataManagementEngine, BacktestConfig, create_data_management_engine
from .technical_indicators_engine import TechnicalIndicatorsEngine, IndicatorConfig, create_technical_indicators_engine
from .signal_detection_engine import SignalDetectionEngine, SignalConfig, TradeSide, create_signal_detection_engine
from .position_management_engine import PositionManagementEngine, PositionConfig, create_position_management_engine
from .performance_analytics_engine import PerformanceAnalyticsEngine, AnalyticsConfig, create_performance_analytics_engine


class TSLAATRBacktestOrchestrator:
    """Main orchestrator for TSLA ATR Pullback strategy backtesting"""
    
    def __init__(self, config: Optional[BacktestConfig] = None):
        """Initialize backtest orchestrator with configuration"""
        self.config = config or BacktestConfig()
        
        # Create indicator and signal configs from main config
        indicator_config = IndicatorConfig(
            ma_short_len=self.config.ma_short_len,
            ma_long_len=self.config.ma_long_len,
            rsi_period=self.config.rsi_period,
            rsi_ob=self.config.rsi_ob,
            rsi_os=self.config.rsi_os,
            atr_period=self.config.atr_period,
            atr_mult=self.config.atr_mult,
            min_vol=self.config.min_vol
        )
        
        signal_config = SignalConfig(
            rsi_ob=self.config.rsi_ob,
            rsi_os=self.config.rsi_os,
            atr_mult=self.config.atr_mult,
            rr_ratio=self.config.rr_ratio,
            cooldown_bars=self.config.cooldown_bars,
            use_rth=self.config.use_rth,
            vol_gate=self.config.vol_gate,
            min_vol=self.config.min_vol
        )
        
        position_config = PositionConfig(
            initial_capital=self.config.initial_capital,
            risk_percent=self.config.risk_percent,
            commission_bps=self.config.commission_bps,
            slippage_ticks=self.config.slippage_ticks
        )
        
        analytics_config = AnalyticsConfig(
            initial_capital=self.config.initial_capital
        )
        
        # Initialize all engines
        self.data_engine = create_data_management_engine(self.config)
        self.indicators_engine = create_technical_indicators_engine(indicator_config)
        self.signal_engine = create_signal_detection_engine(signal_config)
        self.position_engine = create_position_management_engine(position_config)
        self.analytics_engine = create_performance_analytics_engine(analytics_config)
        
        # Backtest state
        self.data: pd.DataFrame = pd.DataFrame()
        self.equity_curve: list = []
        self.bar_index = 0
    
    def run_backtest(self) -> Dict[str, Any]:
        """Run the complete backtest"""
        print("Starting TSLA ATR Pullback backtest...")
        
        try:
            # Load and prepare data
            print("Loading data...")
            self.data = self.data_engine.load_data()
            
            if not self.data_engine.validate_data(self.data):
                return {"error": "Data validation failed"}
            
            # Calculate technical indicators
            print("Calculating technical indicators...")
            self.data = self.indicators_engine.calculate_all_indicators(self.data)
            
            if not self.indicators_engine.validate_indicators(self.data):
                return {"error": "Indicator validation failed"}
            
            # Initialize equity curve
            self.equity_curve = [self.config.initial_capital]
            
            # Run through each bar
            print("Running backtest simulation...")
            for idx, row in self.data.iterrows():
                self.bar_index = idx
                self.signal_engine.update_bar_index(idx)
                
                # Check for exits first
                if self.position_engine.position_size != 0:
                    exit_reason = self.signal_engine.check_exit_signals(
                        row, 
                        self.position_engine.position_side,
                        self.position_engine.position_avg_price,
                        self.position_engine.current_trade.stop_price if self.position_engine.current_trade else 0,
                        self.position_engine.current_trade.target_price if self.position_engine.current_trade else 0
                    )
                    
                    if exit_reason:
                        self.position_engine.exit_position(row['close'], exit_reason, idx)
                        self.signal_engine.record_exit(idx)
                
                # Check for entries
                else:
                    long_sig, short_sig = self.signal_engine.check_entry_signals(row)
                    
                    if long_sig:
                        stop_dist = self.signal_engine.calculate_stop_distance(row)
                        target_dist = stop_dist * self.config.rr_ratio
                        self.position_engine.enter_position(
                            TradeSide.LONG, row['close'], stop_dist, target_dist, idx
                        )
                    
                    elif short_sig:
                        stop_dist = self.signal_engine.calculate_stop_distance(row)
                        target_dist = stop_dist * self.config.rr_ratio
                        self.position_engine.enter_position(
                            TradeSide.SHORT, row['close'], stop_dist, target_dist, idx
                        )
                
                # Record equity
                self.equity_curve.append(self.position_engine.current_capital)
            
            # Close any remaining position
            if self.position_engine.position_size != 0:
                self.position_engine.exit_position(
                    self.data.iloc[-1]['close'], "end_of_data", len(self.data) - 1
                )
            
            # Calculate final metrics
            print("Calculating performance metrics...")
            results = self.analytics_engine.calculate_comprehensive_metrics(
                self.position_engine.trades, self.equity_curve
            )
            
            # Add additional backtest info
            results.update({
                "backtest_config": {
                    "symbol": self.config.symbol,
                    "start_date": self.config.start_date,
                    "end_date": self.config.end_date,
                    "initial_capital": self.config.initial_capital
                },
                "data_summary": self.data_engine.get_data_summary(),
                "final_capital": self.position_engine.current_capital,
                "total_return_pct": ((self.position_engine.current_capital - self.config.initial_capital) / self.config.initial_capital) * 100
            })
            
            print("Backtest completed successfully!")
            return results
            
        except Exception as e:
            print(f"Error during backtest: {e}")
            return {"error": str(e)}
    
    def get_backtest_summary(self) -> Dict[str, Any]:
        """Get backtest summary information"""
        return {
            "config": {
                "symbol": self.config.symbol,
                "start_date": self.config.start_date,
                "end_date": self.config.end_date,
                "initial_capital": self.config.initial_capital,
                "risk_percent": self.config.risk_percent
            },
            "data_status": {
                "loaded": self.data_engine.is_data_loaded(),
                "rows": len(self.data) if not self.data.empty else 0,
                "columns": len(self.data.columns) if not self.data.empty else 0
            },
            "position_status": self.position_engine.get_position_status(),
            "signal_status": self.signal_engine.get_cooldown_status()
        }
    
    def get_trade_log(self) -> list:
        """Get detailed trade log"""
        return self.position_engine.get_trade_log()
    
    def get_equity_curve(self) -> list:
        """Get equity curve data"""
        return self.equity_curve
    
    def generate_performance_report(self) -> str:
        """Generate formatted performance report"""
        return self.analytics_engine.generate_performance_report(
            self.position_engine.trades, self.equity_curve
        )
    
    def export_results(self, filename: str = "backtest_results.csv") -> bool:
        """Export backtest results to CSV"""
        return self.analytics_engine.export_metrics_to_csv(
            self.position_engine.trades, self.equity_curve, filename
        )
    
    def reset_backtest(self):
        """Reset backtest state"""
        self.data = pd.DataFrame()
        self.equity_curve = []
        self.bar_index = 0
        self.position_engine.clear_trades()
        self.signal_engine.reset_cooldown()
        self.data_engine.data = pd.DataFrame()
    
    def update_config(self, new_config: BacktestConfig):
        """Update backtest configuration"""
        self.config = new_config
        # Note: In a full implementation, you'd need to reinitialize engines with new config


# Factory function for dependency injection
def create_tsla_atr_backtest_orchestrator(config: Optional[BacktestConfig] = None) -> TSLAATRBacktestOrchestrator:
    """Factory function to create TSLA ATR backtest orchestrator with optional configuration"""
    return TSLAATRBacktestOrchestrator(config)


# Export for DI
__all__ = ['TSLAATRBacktestOrchestrator', 'create_tsla_atr_backtest_orchestrator']
