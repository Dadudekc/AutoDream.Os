#!/usr/bin/env python3
"""
Extended Risk Manager - inherits from BaseManager for unified functionality

This manager consolidates financial risk management functionality
from src/services/financial/risk_management_service.py into a V2-compliant system.
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Tuple, Any, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from pathlib import Path
from enum import Enum
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor

from src.core.base_manager import BaseManager
from src.utils.stability_improvements import stability_manager, safe_import

# Configure logging
logger = logging.getLogger(__name__)


class RiskLevel(Enum):
    """Risk level classifications"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class RiskType(Enum):
    """Types of financial risk"""
    MARKET_RISK = "MARKET_RISK"
    CREDIT_RISK = "CREDIT_RISK"
    LIQUIDITY_RISK = "LIQUIDITY_RISK"
    OPERATIONAL_RISK = "OPERATIONAL_RISK"
    CONCENTRATION_RISK = "CONCENTRATION_RISK"
    VOLATILITY_RISK = "VOLATILITY_RISK"


@dataclass
class RiskMetric:
    """Individual risk metric data"""
    risk_type: RiskType
    value: float
    threshold: float
    risk_level: RiskLevel
    weight: float
    description: str
    last_updated: datetime = None

    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.now()
        self.calculate_risk_level()

    def calculate_risk_level(self):
        """Calculate risk level based on value vs threshold"""
        if self.value <= self.threshold * 0.5:
            self.risk_level = RiskLevel.LOW
        elif self.value <= self.threshold * 0.8:
            self.risk_level = RiskLevel.MEDIUM
        elif self.value <= self.threshold:
            self.risk_level = RiskLevel.HIGH
        else:
            self.risk_level = RiskLevel.CRITICAL


@dataclass
class RiskAlert:
    """Risk alert notification"""
    alert_id: str
    risk_type: RiskType
    risk_level: RiskLevel
    message: str
    current_value: float
    threshold: float
    timestamp: datetime
    acknowledged: bool = False
    acknowledged_by: str = ""
    acknowledged_at: datetime = None


@dataclass
class PortfolioRiskProfile:
    """Comprehensive portfolio risk profile"""
    total_risk_score: float
    risk_metrics: Dict[RiskType, RiskMetric]
    risk_alerts: List[RiskAlert]
    var_95: float  # Value at Risk (95% confidence)
    max_drawdown: float
    sharpe_ratio: float
    beta: float
    correlation_matrix: Dict[str, Dict[str, float]]
    last_updated: datetime = None

    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.now()


class ExtendedRiskManager(BaseManager):
    """Extended Risk Manager - inherits from BaseManager for unified functionality"""
    
    def __init__(self, config_path: str = "config/financial/risk_manager.json"):
        super().__init__(
            manager_name="ExtendedRiskManager",
            config_path=config_path,
            enable_metrics=True,
            enable_events=True,
            enable_persistence=True
        )
        
        # Risk management state
        self.risk_metrics: Dict[RiskType, RiskMetric] = {}
        self.risk_alerts: List[RiskAlert] = []
        self.portfolio_profiles: Dict[str, PortfolioRiskProfile] = {}
        self.risk_thresholds: Dict[RiskType, float] = {}
        self.alert_handlers: Dict[RiskLevel, List[Callable]] = {}
        
        # Risk calculation settings
        self.var_confidence_level = 0.95
        self.max_alert_history = 1000
        self.risk_update_interval = 300  # 5 minutes
        self.enable_real_time_monitoring = True
        
        # Threading for risk calculations
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.monitoring_active = False
        
        # Initialize risk management components
        self._initialize_risk_components()
        
        logger.info(f"ExtendedRiskManager initialized successfully")
    
    def _initialize_risk_components(self):
        """Initialize risk management components"""
        try:
            # Set default risk thresholds
            self.risk_thresholds = {
                RiskType.MARKET_RISK: 0.15,
                RiskType.CREDIT_RISK: 0.10,
                RiskType.LIQUIDITY_RISK: 0.20,
                RiskType.OPERATIONAL_RISK: 0.05,
                RiskType.CONCENTRATION_RISK: 0.25,
                RiskType.VOLATILITY_RISK: 0.30
            }
            
            # Initialize alert handlers
            for risk_level in RiskLevel:
                self.alert_handlers[risk_level] = []
            
            # Load configuration overrides
            if self.config:
                self.var_confidence_level = self.config.get("var_confidence_level", 0.95)
                self.risk_update_interval = self.config.get("risk_update_interval", 300)
                self.enable_real_time_monitoring = self.config.get("enable_real_time_monitoring", True)
                
                # Load custom thresholds
                custom_thresholds = self.config.get("risk_thresholds", {})
                for risk_type_str, threshold in custom_thresholds.items():
                    try:
                        risk_type = RiskType(risk_type_str)
                        self.risk_thresholds[risk_type] = threshold
                    except ValueError:
                        logger.warning(f"Invalid risk type in config: {risk_type_str}")
            
            logger.info("✅ Risk management components initialized")
            
        except Exception as e:
            logger.error(f"❌ Error initializing risk components: {e}")
    
    def add_risk_metric(
        self,
        risk_type: RiskType,
        value: float,
        weight: float = 1.0,
        description: str = ""
    ) -> RiskMetric:
        """Add or update a risk metric"""
        try:
            threshold = self.risk_thresholds.get(risk_type, 0.1)
            
            metric = RiskMetric(
                risk_type=risk_type,
                value=value,
                threshold=threshold,
                risk_level=RiskLevel.LOW,  # Will be calculated in __post_init__
                weight=weight,
                description=description
            )
            
            self.risk_metrics[risk_type] = metric
            
            # Emit metric update event
            self.emit_event("risk_metric_updated", {
                "risk_type": risk_type.value,
                "value": value,
                "threshold": threshold,
                "risk_level": metric.risk_level.value,
                "timestamp": datetime.now().isoformat()
            })
            
            # Check for alerts
            self._check_risk_alerts(metric)
            
            logger.info(f"✅ Risk metric updated: {risk_type.value} = {value}")
            return metric
            
        except Exception as e:
            logger.error(f"❌ Error adding risk metric: {e}")
            return None
    
    def _check_risk_alerts(self, metric: RiskMetric):
        """Check if risk metric triggers alerts"""
        if metric.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            alert = RiskAlert(
                alert_id=f"alert_{len(self.risk_alerts) + 1}_{datetime.now().timestamp()}",
                risk_type=metric.risk_type,
                risk_level=metric.risk_level,
                message=f"{metric.risk_type.value} risk level: {metric.risk_level.value} (Value: {metric.value:.4f}, Threshold: {metric.threshold:.4f})",
                current_value=metric.value,
                threshold=metric.threshold,
                timestamp=datetime.now()
            )
            
            self.risk_alerts.append(alert)
            
            # Limit alert history
            if len(self.risk_alerts) > self.max_alert_history:
                self.risk_alerts.pop(0)
            
            # Emit alert event
            self.emit_event("risk_alert_triggered", {
                "alert_id": alert.alert_id,
                "risk_type": metric.risk_type.value,
                "risk_level": metric.risk_level.value,
                "message": alert.message,
                "timestamp": alert.timestamp.isoformat()
            })
            
            # Execute alert handlers
            self._execute_alert_handlers(alert)
            
            logger.warning(f"⚠️ Risk alert triggered: {alert.message}")
    
    def _execute_alert_handlers(self, alert: RiskAlert):
        """Execute registered alert handlers"""
        handlers = self.alert_handlers.get(alert.risk_level, [])
        
        for handler in handlers:
            try:
                handler(alert)
            except Exception as e:
                logger.error(f"❌ Error executing alert handler: {e}")
    
    def register_alert_handler(self, risk_level: RiskLevel, handler: Callable):
        """Register a handler for risk alerts of a specific level"""
        if risk_level not in self.alert_handlers:
            self.alert_handlers[risk_level] = []
        
        self.alert_handlers[risk_level].append(handler)
        logger.info(f"✅ Alert handler registered for {risk_level.value}")
    
    def calculate_portfolio_risk(self, portfolio_data: Dict[str, Any]) -> PortfolioRiskProfile:
        """Calculate comprehensive portfolio risk profile"""
        try:
            # Extract portfolio components
            positions = portfolio_data.get("positions", {})
            weights = portfolio_data.get("weights", {})
            returns = portfolio_data.get("returns", {})
            
            if not positions or not weights:
                logger.warning("⚠️ Insufficient portfolio data for risk calculation")
                return None
            
            # Calculate individual risk metrics
            risk_metrics = {}
            total_risk_score = 0.0
            
            for asset, weight in weights.items():
                if asset in returns:
                    asset_returns = returns[asset]
                    
                    # Calculate volatility
                    volatility = np.std(asset_returns) if len(asset_returns) > 1 else 0.0
                    
                    # Create risk metric
                    metric = RiskMetric(
                        risk_type=RiskType.VOLATILITY_RISK,
                        value=volatility,
                        threshold=self.risk_thresholds[RiskType.VOLATILITY_RISK],
                        weight=weight,
                        description=f"Volatility risk for {asset}"
                    )
                    
                    risk_metrics[asset] = metric
                    total_risk_score += volatility * weight
            
            # Calculate Value at Risk (VaR)
            portfolio_returns = []
            for asset, weight in weights.items():
                if asset in returns:
                    portfolio_returns.extend([ret * weight for ret in returns[asset]])
            
            var_95 = np.percentile(portfolio_returns, (1 - self.var_confidence_level) * 100) if portfolio_returns else 0.0
            
            # Calculate correlation matrix
            correlation_matrix = {}
            assets = list(returns.keys())
            for i, asset1 in enumerate(assets):
                correlation_matrix[asset1] = {}
                for j, asset2 in enumerate(assets):
                    if i == j:
                        correlation_matrix[asset1][asset2] = 1.0
                    else:
                        corr = np.corrcoef(returns[asset1], returns[asset2])[0, 1] if len(returns[asset1]) > 1 and len(returns[asset2]) > 1 else 0.0
                        correlation_matrix[asset1][asset2] = corr if not np.isnan(corr) else 0.0
            
            # Create portfolio risk profile
            profile = PortfolioRiskProfile(
                total_risk_score=total_risk_score,
                risk_metrics=risk_metrics,
                risk_alerts=self.risk_alerts.copy(),
                var_95=var_95,
                max_drawdown=0.0,  # Would need historical data to calculate
                sharpe_ratio=0.0,   # Would need risk-free rate to calculate
                beta=1.0,           # Would need market data to calculate
                correlation_matrix=correlation_matrix
            )
            
            # Store profile
            portfolio_id = portfolio_data.get("portfolio_id", "default")
            self.portfolio_profiles[portfolio_id] = profile
            
            # Emit portfolio risk calculated event
            self.emit_event("portfolio_risk_calculated", {
                "portfolio_id": portfolio_id,
                "total_risk_score": total_risk_score,
                "var_95": var_95,
                "timestamp": datetime.now().isoformat()
            })
            
            logger.info(f"✅ Portfolio risk calculated for {portfolio_id}")
            return profile
            
        except Exception as e:
            logger.error(f"❌ Error calculating portfolio risk: {e}")
            return None
    
    def get_risk_summary(self) -> Dict[str, Any]:
        """Get comprehensive risk summary"""
        try:
            # Count risk levels
            risk_counts = {level.value: 0 for level in RiskLevel}
            for metric in self.risk_metrics.values():
                risk_counts[metric.risk_level.value] += 1
            
            # Count unacknowledged alerts
            unacknowledged_alerts = sum(1 for alert in self.risk_alerts if not alert.acknowledged)
            
            # Calculate average risk score
            if self.risk_metrics:
                avg_risk_score = sum(metric.value for metric in self.risk_metrics.values()) / len(self.risk_metrics)
            else:
                avg_risk_score = 0.0
            
            summary = {
                "total_metrics": len(self.risk_metrics),
                "risk_level_distribution": risk_counts,
                "total_alerts": len(self.risk_alerts),
                "unacknowledged_alerts": unacknowledged_alerts,
                "average_risk_score": avg_risk_score,
                "portfolio_profiles": len(self.portfolio_profiles),
                "last_updated": datetime.now().isoformat(),
                "monitoring_active": self.monitoring_active
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"❌ Error generating risk summary: {e}")
            return {}
    
    def acknowledge_alert(self, alert_id: str, acknowledged_by: str) -> bool:
        """Acknowledge a risk alert"""
        try:
            for alert in self.risk_alerts:
                if alert.alert_id == alert_id:
                    alert.acknowledged = True
                    alert.acknowledged_by = acknowledged_by
                    alert.acknowledged_at = datetime.now()
                    
                    # Emit alert acknowledged event
                    self.emit_event("risk_alert_acknowledged", {
                        "alert_id": alert_id,
                        "acknowledged_by": acknowledged_by,
                        "timestamp": alert.acknowledged_at.isoformat()
                    })
                    
                    logger.info(f"✅ Alert {alert_id} acknowledged by {acknowledged_by}")
                    return True
            
            logger.warning(f"⚠️ Alert {alert_id} not found")
            return False
            
        except Exception as e:
            logger.error(f"❌ Error acknowledging alert: {e}")
            return False
    
    def start_risk_monitoring(self):
        """Start real-time risk monitoring"""
        if self.monitoring_active:
            logger.info("⚠️ Risk monitoring already active")
            return
        
        self.monitoring_active = True
        
        # Emit monitoring start event
        self.emit_event("risk_monitoring_started", {
            "start_time": datetime.now().isoformat(),
            "update_interval": self.risk_update_interval
        })
        
        logger.info("✅ Risk monitoring started")
    
    def stop_risk_monitoring(self):
        """Stop real-time risk monitoring"""
        if not self.monitoring_active:
            logger.info("⚠️ Risk monitoring not active")
            return
        
        self.monitoring_active = False
        
        # Emit monitoring stop event
        self.emit_event("risk_monitoring_stopped", {
            "stop_time": datetime.now().isoformat()
        })
        
        logger.info("✅ Risk monitoring stopped")
    
    def update_risk_thresholds(self, new_thresholds: Dict[RiskType, float]):
        """Update risk thresholds"""
        try:
            for risk_type, threshold in new_thresholds.items():
                if isinstance(risk_type, str):
                    try:
                        risk_type = RiskType(risk_type)
                    except ValueError:
                        logger.warning(f"Invalid risk type: {risk_type}")
                        continue
                
                if threshold > 0:
                    self.risk_thresholds[risk_type] = threshold
                    
                    # Recalculate risk levels for existing metrics
                    if risk_type in self.risk_metrics:
                        metric = self.risk_metrics[risk_type]
                        metric.threshold = threshold
                        metric.calculate_risk_level()
            
            # Emit thresholds updated event
            self.emit_event("risk_thresholds_updated", {
                "new_thresholds": {k.value: v for k, v in new_thresholds.items()},
                "timestamp": datetime.now().isoformat()
            })
            
            logger.info("✅ Risk thresholds updated")
            
        except Exception as e:
            logger.error(f"❌ Error updating risk thresholds: {e}")
    
    def get_risk_metrics_by_type(self, risk_type: RiskType) -> List[RiskMetric]:
        """Get all risk metrics of a specific type"""
        return [metric for metric in self.risk_metrics.values() if metric.risk_type == risk_type]
    
    def get_alerts_by_level(self, risk_level: RiskLevel) -> List[RiskAlert]:
        """Get all alerts of a specific risk level"""
        return [alert for alert in self.risk_alerts if alert.risk_level == risk_level]
    
    def clear_old_alerts(self, days_old: int = 30):
        """Clear alerts older than specified days"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days_old)
            initial_count = len(self.risk_alerts)
            
            self.risk_alerts = [
                alert for alert in self.risk_alerts 
                if alert.timestamp > cutoff_date
            ]
            
            cleared_count = initial_count - len(self.risk_alerts)
            
            if cleared_count > 0:
                logger.info(f"✅ Cleared {cleared_count} old alerts")
                
                # Emit alerts cleared event
                self.emit_event("old_alerts_cleared", {
                    "cleared_count": cleared_count,
                    "cutoff_date": cutoff_date.isoformat(),
                    "timestamp": datetime.now().isoformat()
                })
            
        except Exception as e:
            logger.error(f"❌ Error clearing old alerts: {e}")
    
    def export_risk_report(self, format: str = "json") -> str:
        """Export comprehensive risk report"""
        try:
            report_data = {
                "risk_summary": self.get_risk_summary(),
                "risk_metrics": {
                    k.value: {
                        "value": v.value,
                        "threshold": v.threshold,
                        "risk_level": v.risk_level.value,
                        "weight": v.weight,
                        "description": v.description,
                        "last_updated": v.last_updated.isoformat()
                    } for k, v in self.risk_metrics.items()
                },
                "risk_alerts": [
                    {
                        "alert_id": alert.alert_id,
                        "risk_type": alert.risk_type.value,
                        "risk_level": alert.risk_level.value,
                        "message": alert.message,
                        "current_value": alert.current_value,
                        "threshold": alert.threshold,
                        "timestamp": alert.timestamp.isoformat(),
                        "acknowledged": alert.acknowledged,
                        "acknowledged_by": alert.acknowledged_by,
                        "acknowledged_at": alert.acknowledged_at.isoformat() if alert.acknowledged_at else None
                    } for alert in self.risk_alerts
                ],
                "portfolio_profiles": {
                    k: {
                        "total_risk_score": v.total_risk_score,
                        "var_95": v.var_95,
                        "max_drawdown": v.max_drawdown,
                        "sharpe_ratio": v.sharpe_ratio,
                        "beta": v.beta,
                        "last_updated": v.last_updated.isoformat()
                    } for k, v in self.portfolio_profiles.items()
                },
                "export_timestamp": datetime.now().isoformat()
            }
            
            if format.lower() == "json":
                return json.dumps(report_data, indent=2)
            else:
                # Could add other formats (CSV, Excel, etc.)
                return str(report_data)
                
        except Exception as e:
            logger.error(f"❌ Error exporting risk report: {e}")
            return ""
    
    def get_risk_metrics(self) -> Dict[str, Any]:
        """Get risk management performance metrics"""
        return {
            "total_metrics_tracked": len(self.risk_metrics),
            "total_alerts_generated": len(self.risk_alerts),
            "unacknowledged_alerts": sum(1 for alert in self.risk_alerts if not alert.acknowledged),
            "portfolio_profiles_managed": len(self.portfolio_profiles),
            "monitoring_active": self.monitoring_active,
            "uptime": self.get_uptime(),
            "last_activity": self.last_activity.isoformat() if self.last_activity else None
        }


