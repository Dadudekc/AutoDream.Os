#!/usr/bin/env python3
"""
Options Market Data Module - Agent Cellphone V2
===============================================

Market data handling and options chain management functionality.
Follows V2 standards: ≤300 LOC, SRP, OOP principles.
"""

import logging
import json
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from src.utils.stability_improvements import stability_manager, safe_import
from .pricing import OptionType


@dataclass
class OptionContract:
    """Individual option contract data"""

    symbol: str
    strike: float
    expiration: datetime
    option_type: OptionType
    last_price: float
    bid: float
    ask: float
    volume: int
    open_interest: int
    implied_volatility: float
    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float
    underlying_price: float
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

    @property
    def mid_price(self) -> float:
        """Calculate mid price"""
        return (self.bid + self.ask) / 2

    @property
    def bid_ask_spread(self) -> float:
        """Calculate bid-ask spread"""
        return self.ask - self.bid

    @property
    def time_to_expiration(self) -> float:
        """Calculate time to expiration in years"""
        return (self.expiration - datetime.now()).days / 365.25


@dataclass
class OptionsChain:
    """Complete options chain for a symbol"""

    symbol: str
    underlying_price: float
    expiration_dates: List[datetime]
    call_options: Dict[float, OptionContract]
    put_options: Dict[float, OptionContract]
    last_updated: datetime = None

    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.now()

    def get_atm_options(
        self, expiration: datetime = None
    ) -> Tuple[Optional[OptionContract], Optional[OptionContract]]:
        """Get at-the-money call and put options"""
        if expiration is None:
            expiration = min(self.expiration_dates)

        # Find closest strike to underlying price
        strikes = list(self.call_options.keys())
        if not strikes:
            return None, None

        atm_strike = min(strikes, key=lambda x: abs(x - self.underlying_price))

        call = self.call_options.get(atm_strike)
        put = self.put_options.get(atm_strike)

        return call, put

    def get_implied_volatility_smile(
        self, expiration: datetime = None
    ) -> Dict[str, List[float]]:
        """Get implied volatility smile data"""
        if expiration is None:
            expiration = min(self.expiration_dates)

        strikes = []
        call_ivs = []
        put_ivs = []

        for strike in sorted(self.call_options.keys()):
            if strike in self.call_options and strike in self.put_options:
                call = self.call_options[strike]
                put = self.put_options[strike]

                if call.expiration == expiration and put.expiration == expiration:
                    strikes.append(strike)
                    call_ivs.append(call.implied_volatility)
                    put_ivs.append(put.implied_volatility)

        return {"strikes": strikes, "call_ivs": call_ivs, "put_ivs": put_ivs}


class OptionsMarketDataManager:
    """
    Advanced market data management for options trading
    """

    def __init__(self, data_dir: str = "options_market_data"):
        self.logger = logging.getLogger(f"{__name__}.OptionsMarketDataManager")
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

        self.options_chains: Dict[str, OptionsChain] = {}
        self.market_data_cache: Dict[str, Dict[str, Any]] = {}
        
        # Data files
        self.chains_file = self.data_dir / "options_chains.json"
        self.market_data_file = self.data_dir / "market_data_cache.json"

    def update_options_chain(
        self,
        symbol: str,
        chain_data: Dict[str, Any],
    ) -> bool:
        """Update options chain for a symbol"""
        try:
            # Parse chain data
            underlying_price = chain_data.get("underlying_price", 0.0)
            expiration_dates = [
                datetime.fromisoformat(date_str) 
                for date_str in chain_data.get("expiration_dates", [])
            ]
            
            call_options = {}
            put_options = {}
            
            # Process call options
            for call_data in chain_data.get("call_options", []):
                contract = self._create_option_contract(call_data, OptionType.CALL, underlying_price)
                if contract:
                    call_options[contract.strike] = contract
            
            # Process put options
            for put_data in chain_data.get("put_options", []):
                contract = self._create_option_contract(put_data, OptionType.PUT, underlying_price)
                if contract:
                    put_options[contract.strike] = contract
            
            # Create options chain
            chain = OptionsChain(
                symbol=symbol,
                underlying_price=underlying_price,
                expiration_dates=expiration_dates,
                call_options=call_options,
                put_options=put_options,
            )
            
            self.options_chains[symbol] = chain
            self.logger.info(f"Updated options chain for {symbol}: {len(call_options)} calls, {len(put_options)} puts")
            
            return True

        except Exception as e:
            self.logger.error(f"Error updating options chain for {symbol}: {e}")
            return False

    def _create_option_contract(
        self,
        contract_data: Dict[str, Any],
        option_type: OptionType,
        underlying_price: float,
    ) -> Optional[OptionContract]:
        """Create option contract from data"""
        try:
            return OptionContract(
                symbol=contract_data.get("symbol", ""),
                strike=float(contract_data.get("strike", 0)),
                expiration=datetime.fromisoformat(contract_data.get("expiration", "")),
                option_type=option_type,
                last_price=float(contract_data.get("last_price", 0)),
                bid=float(contract_data.get("bid", 0)),
                ask=float(contract_data.get("ask", 0)),
                volume=int(contract_data.get("volume", 0)),
                open_interest=int(contract_data.get("open_interest", 0)),
                implied_volatility=float(contract_data.get("implied_volatility", 0)),
                delta=float(contract_data.get("delta", 0)),
                gamma=float(contract_data.get("gamma", 0)),
                theta=float(contract_data.get("theta", 0)),
                vega=float(contract_data.get("vega", 0)),
                rho=float(contract_data.get("rho", 0)),
                underlying_price=underlying_price,
            )
        except Exception as e:
            self.logger.error(f"Error creating option contract: {e}")
            return None

    def get_options_chain(self, symbol: str) -> Optional[OptionsChain]:
        """Get options chain for a symbol"""
        return self.options_chains.get(symbol)

    def get_expiration_dates(self, symbol: str) -> List[datetime]:
        """Get available expiration dates for a symbol"""
        chain = self.get_options_chain(symbol)
        if chain:
            return chain.expiration_dates
        return []

    def get_strikes(self, symbol: str, expiration: datetime = None) -> List[float]:
        """Get available strikes for a symbol and expiration"""
        chain = self.get_options_chain(symbol)
        if not chain:
            return []
        
        if expiration is None:
            expiration = min(chain.expiration_dates)
        
        strikes = set()
        
        # Get strikes from call options
        for strike, contract in chain.call_options.items():
            if contract.expiration == expiration:
                strikes.add(strike)
        
        # Get strikes from put options
        for strike, contract in chain.put_options.items():
            if contract.expiration == expiration:
                strikes.add(strike)
        
        return sorted(list(strikes))

    def get_option_contract(
        self,
        symbol: str,
        strike: float,
        expiration: datetime,
        option_type: OptionType,
    ) -> Optional[OptionContract]:
        """Get specific option contract"""
        chain = self.get_options_chain(symbol)
        if not chain:
            return None
        
        if option_type == OptionType.CALL:
            return chain.call_options.get(strike)
        else:
            return chain.put_options.get(strike)

    def get_atm_options(
        self,
        symbol: str,
        expiration: datetime = None,
    ) -> Tuple[Optional[OptionContract], Optional[OptionContract]]:
        """Get at-the-money options for a symbol"""
        chain = self.get_options_chain(symbol)
        if chain:
            return chain.get_atm_options(expiration)
        return None, None

    def get_implied_volatility_smile(
        self,
        symbol: str,
        expiration: datetime = None,
    ) -> Dict[str, List[float]]:
        """Get implied volatility smile for a symbol"""
        chain = self.get_options_chain(symbol)
        if chain:
            return chain.get_implied_volatility_smile(expiration)
        return {"strikes": [], "call_ivs": [], "put_ivs": []}

    def update_market_data(
        self,
        symbol: str,
        market_data: Dict[str, Any],
    ) -> bool:
        """Update market data for a symbol"""
        try:
            self.market_data_cache[symbol] = {
                **market_data,
                "last_updated": datetime.now().isoformat(),
            }
            
            self.logger.info(f"Updated market data for {symbol}")
            return True

        except Exception as e:
            self.logger.error(f"Error updating market data for {symbol}: {e}")
            return False

    def get_market_data(self, symbol: str) -> Dict[str, Any]:
        """Get market data for a symbol"""
        return self.market_data_cache.get(symbol, {})

    def save_data(self) -> bool:
        """Save all data to files"""
        try:
            # Save options chains
            chains_data = {}
            for symbol, chain in self.options_chains.items():
                chains_data[symbol] = {
                    "symbol": chain.symbol,
                    "underlying_price": chain.underlying_price,
                    "expiration_dates": [date.isoformat() for date in chain.expiration_dates],
                    "call_options": {
                        str(strike): {
                            "symbol": contract.symbol,
                            "strike": contract.strike,
                            "expiration": contract.expiration.isoformat(),
                            "option_type": contract.option_type.value,
                            "last_price": contract.last_price,
                            "bid": contract.bid,
                            "ask": contract.ask,
                            "volume": contract.volume,
                            "open_interest": contract.open_interest,
                            "implied_volatility": contract.implied_volatility,
                            "delta": contract.delta,
                            "gamma": contract.gamma,
                            "theta": contract.theta,
                            "vega": contract.vega,
                            "rho": contract.rho,
                        }
                        for strike, contract in chain.call_options.items()
                    },
                    "put_options": {
                        str(strike): {
                            "symbol": contract.symbol,
                            "strike": contract.strike,
                            "expiration": contract.expiration.isoformat(),
                            "option_type": contract.option_type.value,
                            "last_price": contract.last_price,
                            "bid": contract.bid,
                            "ask": contract.ask,
                            "volume": contract.volume,
                            "open_interest": contract.open_interest,
                            "implied_volatility": contract.implied_volatility,
                            "delta": contract.delta,
                            "gamma": contract.gamma,
                            "theta": contract.theta,
                            "vega": contract.vega,
                            "rho": contract.rho,
                        }
                        for strike, contract in chain.put_options.items()
                    },
                }
            
            with open(self.chains_file, 'w') as f:
                json.dump(chains_data, f, indent=2)
            
            # Save market data cache
            with open(self.market_data_file, 'w') as f:
                json.dump(self.market_data_cache, f, indent=2)
            
            self.logger.info("Saved options market data to files")
            return True

        except Exception as e:
            self.logger.error(f"Error saving data: {e}")
            return False

    def load_data(self) -> bool:
        """Load data from files"""
        try:
            # Load options chains
            if self.chains_file.exists():
                with open(self.chains_file, 'r') as f:
                    chains_data = json.load(f)
                
                for symbol, chain_data in chains_data.items():
                    self.update_options_chain(symbol, chain_data)
            
            # Load market data cache
            if self.market_data_file.exists():
                with open(self.market_data_file, 'r') as f:
                    self.market_data_cache = json.load(f)
            
            self.logger.info("Loaded options market data from files")
            return True

        except Exception as e:
            self.logger.error(f"Error loading data: {e}")
            return False

    def get_data_summary(self) -> Dict[str, Any]:
        """Get summary of all market data"""
        try:
            summary = {
                "total_symbols": len(self.options_chains),
                "total_contracts": 0,
                "symbols": [],
                "last_updated": None,
            }
            
            for symbol, chain in self.options_chains.items():
                total_contracts = len(chain.call_options) + len(chain.put_options)
                summary["total_contracts"] += total_contracts
                summary["symbols"].append({
                    "symbol": symbol,
                    "contracts": total_contracts,
                    "expirations": len(chain.expiration_dates),
                    "underlying_price": chain.underlying_price,
                })
                
                if summary["last_updated"] is None or chain.last_updated > summary["last_updated"]:
                    summary["last_updated"] = chain.last_updated
            
            return summary

        except Exception as e:
            self.logger.error(f"Error generating data summary: {e}")
            return {}



