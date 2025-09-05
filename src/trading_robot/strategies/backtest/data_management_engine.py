#!/usr/bin/env python3
"""
Trading Backtest Data Management Engine
======================================

Data management engine for trading strategy backtesting.
Handles data loading, caching, preparation, and validation.
V2 COMPLIANT: Focused data management under 300 lines.

@version 1.0.0 - V2 COMPLIANCE MODULAR DATA MANAGEMENT
@license MIT
"""

import os
import pandas as pd
import yfinance as yf
from typing import Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class BacktestConfig:
    """Backtest configuration parameters"""
    symbol: str = "TSLA"
    start_date: str = "2022-01-01"
    end_date: str = "2024-09-01"
    initial_capital: float = 100000.0
    risk_percent: float = 0.5
    commission_bps: float = 2.0  # 2 basis points
    slippage_ticks: int = 1

    # Strategy parameters
    ma_short_len: int = 20
    ma_long_len: int = 50
    rsi_period: int = 14
    rsi_ob: int = 70
    rsi_os: int = 30
    atr_period: int = 14
    atr_mult: float = 2.0
    rr_ratio: float = 2.0
    cooldown_bars: int = 5

    # Filters
    use_rth: bool = True
    vol_gate: bool = True
    min_vol: float = 0.004  # 0.4%

    # Exit mode
    use_trailing: bool = False
    trail_k: float = 1.0


class DataManagementEngine:
    """Data management engine for trading backtesting"""
    
    def __init__(self, config: BacktestConfig):
        """Initialize data management engine with configuration"""
        self.config = config
        self.data: pd.DataFrame = pd.DataFrame()
        self.cache_dir = "data_cache"
        self._ensure_cache_dir()
    
    def _ensure_cache_dir(self):
        """Ensure cache directory exists"""
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
    
    def load_data(self) -> pd.DataFrame:
        """Load historical data for backtesting"""
        print(f"Loading {self.config.symbol} data from {self.config.start_date} to {self.config.end_date}")

        # Try to load from local cache first
        cache_file = self._get_cache_file_path()
        
        try:
            if os.path.exists(cache_file):
                print(f"Loading data from cache: {cache_file}")
                df = pd.read_csv(cache_file, index_col=0, parse_dates=True)
                print(f"Loaded {len(df)} rows from cache")
                self.data = df
                return df
        except Exception as e:
            print(f"Error loading from cache: {e}")
        
        # Download fresh data
        print("Downloading fresh data from Yahoo Finance...")
        try:
            ticker = yf.Ticker(self.config.symbol)
            df = ticker.history(
                start=self.config.start_date,
                end=self.config.end_date,
                interval="1d"
            )
            
            if df.empty:
                raise ValueError(f"No data found for {self.config.symbol}")
            
            # Clean and prepare data
            df = self._clean_data(df)
            
            # Save to cache
            self._save_to_cache(df, cache_file)
            
            self.data = df
            print(f"Downloaded and cached {len(df)} rows")
            return df
            
        except Exception as e:
            print(f"Error downloading data: {e}")
            raise
    
    def _get_cache_file_path(self) -> str:
        """Get cache file path for the current configuration"""
        return os.path.join(
            self.cache_dir,
            f"{self.config.symbol}_{self.config.start_date}_{self.config.end_date}.csv"
        )
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and prepare raw data"""
        # Ensure we have required columns
        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")
        
        # Rename columns to lowercase
        df.columns = [col.lower() for col in df.columns]
        
        # Remove any rows with NaN values
        df = df.dropna()
        
        # Ensure data is sorted by date
        df = df.sort_index()
        
        # Add point value for futures (default to 1 for stocks)
        df['pointvalue'] = 1.0
        
        return df
    
    def _save_to_cache(self, df: pd.DataFrame, cache_file: str):
        """Save data to cache file"""
        try:
            df.to_csv(cache_file)
            print(f"Data saved to cache: {cache_file}")
        except Exception as e:
            print(f"Error saving to cache: {e}")
    
    def validate_data(self, df: pd.DataFrame) -> bool:
        """Validate data quality and completeness"""
        if df.empty:
            print("Error: Data is empty")
            return False
        
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        for col in required_columns:
            if col not in df.columns:
                print(f"Error: Missing required column: {col}")
                return False
        
        # Check for sufficient data
        if len(df) < 50:
            print(f"Error: Insufficient data ({len(df)} rows, need at least 50)")
            return False
        
        # Check for data quality issues
        if df['close'].isna().any():
            print("Error: Found NaN values in close prices")
            return False
        
        if (df['high'] < df['low']).any():
            print("Error: Found high < low prices")
            return False
        
        if (df['close'] < 0).any():
            print("Error: Found negative prices")
            return False
        
        print(f"Data validation passed: {len(df)} rows, {len(df.columns)} columns")
        return True
    
    def get_data_summary(self) -> Dict[str, Any]:
        """Get summary statistics of loaded data"""
        if self.data.empty:
            return {"error": "No data loaded"}
        
        return {
            "symbol": self.config.symbol,
            "start_date": self.data.index[0].strftime("%Y-%m-%d"),
            "end_date": self.data.index[-1].strftime("%Y-%m-%d"),
            "total_rows": len(self.data),
            "total_columns": len(self.data.columns),
            "date_range_days": (self.data.index[-1] - self.data.index[0]).days,
            "price_range": {
                "min_close": float(self.data['close'].min()),
                "max_close": float(self.data['close'].max()),
                "avg_close": float(self.data['close'].mean())
            },
            "volume_stats": {
                "min_volume": int(self.data['volume'].min()),
                "max_volume": int(self.data['volume'].max()),
                "avg_volume": int(self.data['volume'].mean())
            }
        }
    
    def get_data_slice(self, start_idx: int, end_idx: int) -> pd.DataFrame:
        """Get a slice of data by index"""
        if self.data.empty:
            return pd.DataFrame()
        
        return self.data.iloc[start_idx:end_idx].copy()
    
    def get_latest_data(self, n_rows: int = 1) -> pd.DataFrame:
        """Get the latest n rows of data"""
        if self.data.empty:
            return pd.DataFrame()
        
        return self.data.tail(n_rows).copy()
    
    def clear_cache(self):
        """Clear all cached data files"""
        try:
            for file in os.listdir(self.cache_dir):
                if file.endswith('.csv'):
                    os.remove(os.path.join(self.cache_dir, file))
            print("Cache cleared successfully")
        except Exception as e:
            print(f"Error clearing cache: {e}")
    
    def is_data_loaded(self) -> bool:
        """Check if data is loaded"""
        return not self.data.empty
    
    def get_data_info(self) -> Dict[str, Any]:
        """Get detailed data information"""
        if self.data.empty:
            return {"status": "no_data"}
        
        return {
            "status": "loaded",
            "shape": self.data.shape,
            "columns": list(self.data.columns),
            "index_type": type(self.data.index).__name__,
            "memory_usage": f"{self.data.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB",
            "dtypes": self.data.dtypes.to_dict()
        }


# Factory function for dependency injection
def create_data_management_engine(config: BacktestConfig) -> DataManagementEngine:
    """Factory function to create data management engine with configuration"""
    return DataManagementEngine(config)


# Export for DI
__all__ = ['DataManagementEngine', 'BacktestConfig', 'create_data_management_engine']
