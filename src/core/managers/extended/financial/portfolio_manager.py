#!/usr/bin/env python3
"""
Extended Portfolio Manager - Agent Cellphone V2
==============================================

Consolidated PortfolioManager inheriting from BaseManager.
Follows V2 standards: OOP, SRP, clean production-grade code.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from decimal import Decimal

from src.core.base_manager import BaseManager


class ExtendedPortfolioManager(BaseManager):
    """Extended Portfolio Manager - inherits from BaseManager for unified functionality"""
    
    def __init__(self, config_path: str = "config/financial/portfolio_manager.json"):
        super().__init__(
            manager_name="ExtendedPortfolioManager",
            config_path=config_path,
            enable_metrics=True,
            enable_events=True,
            enable_persistence=True
        )
        
        # Initialize portfolio-specific functionality
        self.portfolios: Dict[str, Dict[str, Any]] = {}
        self.assets: Dict[str, Dict[str, Any]] = {}
        self.transactions: Dict[str, List[Dict[str, Any]]] = {}
        self.performance_metrics: Dict[str, Dict[str, Any]] = {}
        
        # Load portfolio configuration
        self._load_portfolio_config()
        
        logger.info("ExtendedPortfolioManager initialized successfully")
    
    def _load_portfolio_config(self):
        """Load portfolio-specific configuration"""
        try:
            if self.config:
                portfolio_config = self.config.get("portfolios", {})
                self.portfolios = portfolio_config.get("portfolio_list", {})
                self.assets = portfolio_config.get("assets", {})
                
                # Emit configuration loaded event
                self.emit_event("portfolio_config_loaded", {
                    "portfolios_count": len(self.portfolios),
                    "assets_count": len(self.assets)
                })
        except Exception as e:
            logger.error(f"Error loading portfolio config: {e}")
    
    def create_portfolio(self, portfolio_id: str, name: str, description: str = "", 
                        initial_capital: Decimal = Decimal('0')) -> bool:
        """Create a new portfolio"""
        try:
            if portfolio_id in self.portfolios:
                logger.warning(f"Portfolio {portfolio_id} already exists")
                return False
            
            portfolio = {
                "portfolio_id": portfolio_id,
                "name": name,
                "description": description,
                "created_at": self.last_activity.isoformat(),
                "initial_capital": float(initial_capital),
                "current_value": float(initial_capital),
                "cash_balance": float(initial_capital),
                "assets": [],
                "status": "active",
                "risk_profile": "moderate",
                "rebalancing_frequency": "monthly"
            }
            
            self.portfolios[portfolio_id] = portfolio
            self.transactions[portfolio_id] = []
            self.performance_metrics[portfolio_id] = {
                "total_return": 0.0,
                "daily_return": 0.0,
                "volatility": 0.0,
                "sharpe_ratio": 0.0,
                "max_drawdown": 0.0,
                "last_updated": self.last_activity.isoformat()
            }
            
            # Update metrics
            self.metrics.total_operations += 1
            self.metrics.successful_operations += 1
            
            # Emit portfolio created event
            self.emit_event("portfolio_created", {
                "portfolio_id": portfolio_id,
                "name": name,
                "initial_capital": float(initial_capital)
            })
            
            logger.info(f"Created portfolio: {portfolio_id} ({name})")
            return True
            
        except Exception as e:
            logger.error(f"Error creating portfolio {portfolio_id}: {e}")
            self.metrics.failed_operations += 1
            return False
    
    def add_asset_to_portfolio(self, portfolio_id: str, asset_id: str, 
                              quantity: Decimal, price: Decimal) -> bool:
        """Add an asset to a portfolio"""
        try:
            if portfolio_id not in self.portfolios:
                logger.error(f"Portfolio {portfolio_id} not found")
                return False
            
            portfolio = self.portfolios[portfolio_id]
            asset_value = float(quantity * price)
            
            # Check if we have enough cash
            if asset_value > portfolio["cash_balance"]:
                logger.error(f"Insufficient cash balance for asset purchase")
                return False
            
            # Create asset record
            asset_record = {
                "asset_id": asset_id,
                "quantity": float(quantity),
                "average_price": float(price),
                "current_price": float(price),
                "total_value": asset_value,
                "added_at": self.last_activity.isoformat(),
                "last_updated": self.last_activity.isoformat()
            }
            
            # Add to portfolio assets
            portfolio["assets"].append(asset_record)
            portfolio["cash_balance"] -= asset_value
            portfolio["current_value"] = portfolio["cash_balance"] + sum(
                asset["total_value"] for asset in portfolio["assets"]
            )
            
            # Record transaction
            transaction = {
                "transaction_id": f"tx_{len(self.transactions[portfolio_id]) + 1}",
                "type": "buy",
                "asset_id": asset_id,
                "quantity": float(quantity),
                "price": float(price),
                "total_value": asset_value,
                "timestamp": self.last_activity.isoformat(),
                "portfolio_id": portfolio_id
            }
            self.transactions[portfolio_id].append(transaction)
            
            # Update metrics
            self.metrics.total_operations += 1
            self.metrics.successful_operations += 1
            
            # Emit asset added event
            self.emit_event("asset_added_to_portfolio", {
                "portfolio_id": portfolio_id,
                "asset_id": asset_id,
                "quantity": float(quantity),
                "price": float(price)
            })
            
            logger.info(f"Added asset {asset_id} to portfolio {portfolio_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding asset to portfolio: {e}")
            self.metrics.failed_operations += 1
            return False
    
    def remove_asset_from_portfolio(self, portfolio_id: str, asset_id: str, 
                                   quantity: Decimal, price: Decimal) -> bool:
        """Remove an asset from a portfolio"""
        try:
            if portfolio_id not in self.portfolios:
                logger.error(f"Portfolio {portfolio_id} not found")
                return False
            
            portfolio = self.portfolios[portfolio_id]
            
            # Find the asset
            asset_index = None
            for i, asset in enumerate(portfolio["assets"]):
                if asset["asset_id"] == asset_id:
                    asset_index = i
                    break
            
            if asset_index is None:
                logger.error(f"Asset {asset_id} not found in portfolio {portfolio_id}")
                return False
            
            asset = portfolio["assets"][asset_index]
            if asset["quantity"] < float(quantity):
                logger.error(f"Insufficient quantity of asset {asset_id}")
                return False
            
            # Calculate sale value
            sale_value = float(quantity * price)
            
            # Update asset quantity
            asset["quantity"] -= float(quantity)
            asset["total_value"] = asset["quantity"] * asset["current_price"]
            asset["last_updated"] = self.last_activity.isoformat()
            
            # Remove asset if quantity is zero
            if asset["quantity"] <= 0:
                portfolio["assets"].pop(asset_index)
            
            # Update portfolio values
            portfolio["cash_balance"] += sale_value
            portfolio["current_value"] = portfolio["cash_balance"] + sum(
                asset["total_value"] for asset in portfolio["assets"]
            )
            
            # Record transaction
            transaction = {
                "transaction_id": f"tx_{len(self.transactions[portfolio_id]) + 1}",
                "type": "sell",
                "asset_id": asset_id,
                "quantity": float(quantity),
                "price": float(price),
                "total_value": sale_value,
                "timestamp": self.last_activity.isoformat(),
                "portfolio_id": portfolio_id
            }
            self.transactions[portfolio_id].append(transaction)
            
            # Update metrics
            self.metrics.total_operations += 1
            self.metrics.successful_operations += 1
            
            # Emit asset removed event
            self.emit_event("asset_removed_from_portfolio", {
                "portfolio_id": portfolio_id,
                "asset_id": asset_id,
                "quantity": float(quantity),
                "price": float(price)
            })
            
            logger.info(f"Removed asset {asset_id} from portfolio {portfolio_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error removing asset from portfolio: {e}")
            self.metrics.failed_operations += 1
            return False
    
    def get_portfolio_value(self, portfolio_id: str) -> Optional[float]:
        """Get current portfolio value"""
        if portfolio_id not in self.portfolios:
            return None
        
        portfolio = self.portfolios[portfolio_id]
        return portfolio["current_value"]
    
    def get_portfolio_performance(self, portfolio_id: str) -> Optional[Dict[str, Any]]:
        """Get portfolio performance metrics"""
        if portfolio_id not in self.performance_metrics:
            return None
        
        return self.performance_metrics[portfolio_id].copy()
    
    def get_portfolio_transactions(self, portfolio_id: str, 
                                 limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get portfolio transaction history"""
        if portfolio_id not in self.transactions:
            return []
        
        transactions = self.transactions[portfolio_id]
        if limit:
            transactions = transactions[-limit:]
        
        return transactions.copy()
    
    def get_manager_status(self) -> Dict[str, Any]:
        """Get extended manager status including portfolio metrics"""
        base_status = super().get_manager_status()
        
        # Add portfolio-specific status
        portfolio_status = {
            "total_portfolios": len(self.portfolios),
            "active_portfolios": len([p for p in self.portfolios.values() if p.get("status") == "active"]),
            "total_assets": sum(len(p.get("assets", [])) for p in self.portfolios.values()),
            "total_transactions": sum(len(txs) for txs in self.transactions.values()),
            "total_portfolio_value": sum(p.get("current_value", 0) for p in self.portfolios.values())
        }
        
        base_status.update(portfolio_status)
        return base_status

