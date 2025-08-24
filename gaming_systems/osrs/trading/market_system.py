#!/usr/bin/env python3
"""
OSRS Market System - Agent Cellphone V2
======================================

OSRS Grand Exchange and market functionality.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import time

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from ..core.enums import OSRSSkill


@dataclass
class MarketItem:
    """Market item data"""
    item_id: int
    name: str
    current_price: int
    high_alch: int
    low_alch: int
    buy_limit: int
    members: bool
    last_updated: float


@dataclass
class MarketOrder:
    """Market order data"""
    order_id: str
    item_id: int
    quantity: int
    price: int
    order_type: str  # 'buy' or 'sell'
    status: str  # 'pending', 'completed', 'cancelled'
    timestamp: float


class OSRSMarketSystem:
    """OSRS Grand Exchange market system"""
    
    def __init__(self):
        self.items: Dict[int, MarketItem] = {}
        self.orders: Dict[str, MarketOrder] = {}
        self.order_counter = 0
        self._initialize_market_data()
    
    def _initialize_market_data(self):
        """Initialize market with sample data"""
        sample_items = [
            (1, "Rune scimitar", 15000, 19200, 12800, 100, True),
            (2, "Dragon dagger", 18000, 21600, 14400, 50, True),
            (3, "Abyssal whip", 3000000, 3600000, 2400000, 10, True),
            (4, "Bandos chestplate", 15000000, 18000000, 12000000, 5, True),
            (5, "Dragon bones", 3000, 3600, 2400, 1000, False)
        ]
        
        for item_id, name, price, high_alch, low_alch, buy_limit, members in sample_items:
            self.items[item_id] = MarketItem(
                item_id=item_id,
                name=name,
                current_price=price,
                high_alch=high_alch,
                low_alch=low_alch,
                buy_limit=buy_limit,
                members=members,
                last_updated=time.time()
            )
    
    def get_item_info(self, item_id: int) -> Optional[MarketItem]:
        """Get market information for an item"""
        return self.items.get(item_id)
    
    def search_items(self, query: str) -> List[MarketItem]:
        """Search for items by name"""
        query_lower = query.lower()
        return [
            item for item in self.items.values()
            if query_lower in item.name.lower()
        ]
    
    def get_price_history(self, item_id: int, days: int = 30) -> List[Tuple[float, int]]:
        """Get price history for an item (simulated)"""
        if item_id not in self.items:
            return []
        
        item = self.items[item_id]
        history = []
        current_time = time.time()
        
        # Simulate price history
        for i in range(days):
            timestamp = current_time - (i * 24 * 3600)
            # Simulate price variation (±10%)
            variation = 1 + (0.1 * (i % 7 - 3) / 7)
            price = int(item.current_price * variation)
            history.append((timestamp, price))
        
        return history[::-1]  # Reverse to show oldest first
    
    def place_buy_order(self, item_id: int, quantity: int, price: int) -> Optional[str]:
        """Place a buy order"""
        if item_id not in self.items:
            return None
        
        item = self.items[item_id]
        if quantity > item.buy_limit:
            return None
        
        order_id = f"buy_{self.order_counter}"
        self.order_counter += 1
        
        order = MarketOrder(
            order_id=order_id,
            item_id=item_id,
            quantity=quantity,
            price=price,
            order_type="buy",
            status="pending",
            timestamp=time.time()
        )
        
        self.orders[order_id] = order
        return order_id
    
    def place_sell_order(self, item_id: int, quantity: int, price: int) -> Optional[str]:
        """Place a sell order"""
        if item_id not in self.items:
            return None
        
        order_id = f"sell_{self.order_counter}"
        self.order_counter += 1
        
        order = MarketOrder(
            order_id=order_id,
            item_id=item_id,
            quantity=quantity,
            price=price,
            order_type="sell",
            status="pending",
            timestamp=time.time()
        )
        
        self.orders[order_id] = order
        return order_id
    
    def cancel_order(self, order_id: str) -> bool:
        """Cancel an order"""
        if order_id not in self.orders:
            return False
        
        order = self.orders[order_id]
        if order.status != "pending":
            return False
        
        order.status = "cancelled"
        return True
    
    def get_order_status(self, order_id: str) -> Optional[MarketOrder]:
        """Get status of an order"""
        return self.orders.get(order_id)
    
    def get_active_orders(self, order_type: Optional[str] = None) -> List[MarketOrder]:
        """Get active orders, optionally filtered by type"""
        active = [order for order in self.orders.values() if order.status == "pending"]
        
        if order_type:
            active = [order for order in active if order.order_type == order_type]
        
        return active
    
    def update_prices(self):
        """Update market prices (simulated)"""
        current_time = time.time()
        
        for item in self.items.values():
            # Simulate price fluctuations
            if current_time - item.last_updated > 3600:  # 1 hour
                # Random price change ±5%
                import random
                change = 1 + (random.uniform(-0.05, 0.05))
                item.current_price = int(item.current_price * change)
                item.last_updated = current_time
    
    def get_market_summary(self) -> Dict[str, any]:
        """Get market summary statistics"""
        total_items = len(self.items)
        total_orders = len(self.orders)
        active_orders = len([o for o in self.orders.values() if o.status == "pending"])
        
        total_value = sum(item.current_price for item in self.items.values())
        
        return {
            "total_items": total_items,
            "total_orders": total_orders,
            "active_orders": active_orders,
            "total_market_value": total_value,
            "last_updated": time.time()
        }
