"""
Risk Management Service - Business Intelligence & Trading Systems
Agent-5: Business Intelligence & Trading Specialist
Performance & Health Systems Division

Provides comprehensive risk assessment, monitoring, and mitigation capabilities.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Callable
from dataclasses import dataclass, asdict
from pathlib import Path
from enum import Enum
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(level=logging.INFO)
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
    var_99: float  # Value at Risk (99% confidence)
    expected_shortfall: float
    stress_test_results: Dict[str, float]
    last_updated: datetime = None
    
    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.now()

class RiskManager:
    """Advanced risk management and monitoring system"""
    
    def __init__(self, portfolio_manager=None, data_dir: str = "risk_data"):
        self.portfolio_manager = portfolio_manager
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.risk_metrics: Dict[RiskType, RiskMetric] = {}
        self.risk_alerts: List[RiskAlert] = []
        self.risk_profile: PortfolioRiskProfile = None
        
        self.risk_file = self.data_dir / "risk_profile.json"
        self.alerts_file = self.data_dir / "risk_alerts.json"
        
        # Risk thresholds configuration
        self.risk_thresholds = {
            RiskType.MARKET_RISK: 0.25,      # 25% portfolio volatility
            RiskType.CONCENTRATION_RISK: 0.20, # 20% single position
            RiskType.LIQUIDITY_RISK: 0.15,    # 15% illiquid assets
            RiskType.VOLATILITY_RISK: 0.30,   # 30% annualized volatility
        }
        
        # Risk weights for composite scoring
        self.risk_weights = {
            RiskType.MARKET_RISK: 0.35,
            RiskType.CONCENTRATION_RISK: 0.25,
            RiskType.LIQUIDITY_RISK: 0.20,
            RiskType.VOLATILITY_RISK: 0.20,
        }
        
        self.load_risk_data()
        self.initialize_risk_metrics()
    
    def initialize_risk_metrics(self):
        """Initialize risk metrics with default values"""
        for risk_type, threshold in self.risk_thresholds.items():
            weight = self.risk_weights.get(risk_type, 0.25)
            self.risk_metrics[risk_type] = RiskMetric(
                risk_type=risk_type,
                value=0.0,
                threshold=threshold,
                risk_level=RiskLevel.LOW,  # Default to LOW risk level
                weight=weight,
                description=self.get_risk_description(risk_type)
            )
    
    def get_risk_description(self, risk_type: RiskType) -> str:
        """Get description for risk type"""
        descriptions = {
            RiskType.MARKET_RISK: "Risk of losses due to market movements",
            RiskType.CONCENTRATION_RISK: "Risk of over-concentration in single positions",
            RiskType.LIQUIDITY_RISK: "Risk of inability to exit positions quickly",
            RiskType.VOLATILITY_RISK: "Risk of excessive price volatility",
        }
        return descriptions.get(risk_type, "Unknown risk type")
    
    def calculate_market_risk(self) -> float:
        """Calculate market risk based on portfolio volatility"""
        if not self.portfolio_manager or not self.portfolio_manager.positions:
            return 0.0
        
        try:
            # Calculate portfolio volatility
            positions = list(self.portfolio_manager.positions.values())
            if len(positions) < 2:
                return 0.0
            
            # Simplified volatility calculation
            weights = [pos.market_value / self.portfolio_manager.metrics.total_value 
                      for pos in positions]
            
            # Assume correlation matrix (simplified)
            correlation = 0.5
            volatility = np.sqrt(np.sum(np.array(weights) ** 2)) * 0.15
            
            # Adjust for correlation
            adjusted_volatility = volatility * (1 + correlation * (len(positions) - 1) / len(positions))
            
            return min(adjusted_volatility, 1.0)  # Cap at 100%
            
        except Exception as e:
            logger.error(f"Error calculating market risk: {e}")
            return 0.0
    
    def calculate_concentration_risk(self) -> float:
        """Calculate concentration risk based on position sizes"""
        if not self.portfolio_manager or not self.portfolio_manager.positions:
            return 0.0
        
        try:
            total_value = self.portfolio_manager.metrics.total_value
            if total_value <= 0:
                return 0.0
            
            # Find largest position percentage
            max_position_pct = max(
                pos.market_value / total_value 
                for pos in self.portfolio_manager.positions.values()
            )
            
            return max_position_pct
            
        except Exception as e:
            logger.error(f"Error calculating concentration risk: {e}")
            return 0.0
    
    def calculate_liquidity_risk(self) -> float:
        """Calculate liquidity risk based on trading volume and position sizes"""
        if not self.portfolio_manager or not self.portfolio_manager.positions:
            return 0.0
        
        try:
            # Simplified liquidity risk calculation
            # In real implementation, would use actual trading volume data
            total_value = self.portfolio_manager.metrics.total_value
            if total_value <= 0:
                return 0.0
            
            # Assume larger positions have higher liquidity risk
            liquidity_risk = sum(
                (pos.market_value / total_value) ** 2 
                for pos in self.portfolio_manager.positions.values()
            )
            
            return min(liquidity_risk, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating liquidity risk: {e}")
            return 0.0
    
    def calculate_volatility_risk(self) -> float:
        """Calculate volatility risk based on price volatility"""
        if not self.portfolio_manager or not self.portfolio_manager.positions:
            return 0.0
        
        try:
            # Use portfolio volatility as volatility risk
            return self.calculate_market_risk()
            
        except Exception as e:
            logger.error(f"Error calculating volatility risk: {e}")
            return 0.0
    
    def calculate_var(self, confidence_level: float = 0.95) -> float:
        """Calculate Value at Risk"""
        if not self.portfolio_manager or not self.portfolio_manager.positions:
            return 0.0
        
        try:
            # Simplified VaR calculation
            portfolio_value = self.portfolio_manager.metrics.total_value
            volatility = self.calculate_market_risk()
            
            # Use normal distribution assumption
            z_score = 1.645 if confidence_level == 0.95 else 2.326  # 95% or 99%
            var = portfolio_value * volatility * z_score / np.sqrt(252)  # Daily VaR
            
            return var
            
        except Exception as e:
            logger.error(f"Error calculating VaR: {e}")
            return 0.0
    
    def calculate_expected_shortfall(self, confidence_level: float = 0.95) -> float:
        """Calculate Expected Shortfall (Conditional VaR)"""
        try:
            var = self.calculate_var(confidence_level)
            # Simplified ES calculation
            es = var * 1.4  # Assume ES is 40% higher than VaR
            
            return es
            
        except Exception as e:
            logger.error(f"Error calculating Expected Shortfall: {e}")
            return 0.0
    
    def run_stress_tests(self) -> Dict[str, float]:
        """Run portfolio stress tests"""
        if not self.portfolio_manager or not self.portfolio_manager.positions:
            return {}
        
        try:
            stress_tests = {}
            
            # Market crash scenario (-20% across all positions)
            crash_value = self.portfolio_manager.metrics.total_value * 0.8
            stress_tests["market_crash_20pct"] = crash_value
            
            # Interest rate shock (+2% impact on bond-like positions)
            # Simplified calculation
            rate_shock_impact = self.portfolio_manager.metrics.total_value * 0.05
            stress_tests["interest_rate_shock"] = (
                self.portfolio_manager.metrics.total_value - rate_shock_impact
            )
            
            # Sector rotation (technology -30%, others -10%)
            tech_exposure = sum(
                pos.market_value for pos in self.portfolio_manager.positions.values()
                if pos.sector == "Technology"
            )
            tech_impact = tech_exposure * 0.3
            other_impact = (self.portfolio_manager.metrics.total_value - tech_exposure) * 0.1
            stress_tests["sector_rotation"] = (
                self.portfolio_manager.metrics.total_value - tech_impact - other_impact
            )
            
            return stress_tests
            
        except Exception as e:
            logger.error(f"Error running stress tests: {e}")
            return {}
    
    def update_risk_metrics(self) -> None:
        """Update all risk metrics"""
        try:
            # Calculate individual risk metrics
            self.risk_metrics[RiskType.MARKET_RISK].value = self.calculate_market_risk()
            self.risk_metrics[RiskType.CONCENTRATION_RISK].value = self.calculate_concentration_risk()
            self.risk_metrics[RiskType.LIQUIDITY_RISK].value = self.calculate_liquidity_risk()
            self.risk_metrics[RiskType.VOLATILITY_RISK].value = self.calculate_volatility_risk()
            
            # Update risk levels
            for metric in self.risk_metrics.values():
                metric.calculate_risk_level()
            
            # Check for risk alerts
            self.check_risk_alerts()
            
            # Calculate composite risk score
            self.calculate_composite_risk_score()
            
            logger.info("Risk metrics updated successfully")
            
        except Exception as e:
            logger.error(f"Error updating risk metrics: {e}")
    
    def calculate_composite_risk_score(self) -> float:
        """Calculate composite risk score"""
        try:
            total_score = 0.0
            total_weight = 0.0
            
            for risk_type, metric in self.risk_metrics.items():
                weight = self.risk_weights.get(risk_type, 0.25)
                normalized_value = metric.value / metric.threshold if metric.threshold > 0 else 0
                
                total_score += normalized_value * weight
                total_weight += weight
            
            composite_score = total_score / total_weight if total_weight > 0 else 0.0
            
            return min(composite_score, 1.0)  # Cap at 100%
            
        except Exception as e:
            logger.error(f"Error calculating composite risk score: {e}")
            return 0.0
    
    def check_risk_alerts(self) -> None:
        """Check for risk threshold violations and create alerts"""
        try:
            for risk_type, metric in self.risk_metrics.items():
                if metric.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
                    # Check if alert already exists
                    existing_alert = next(
                        (alert for alert in self.risk_alerts 
                         if alert.risk_type == risk_type and not alert.acknowledged),
                        None
                    )
                    
                    if not existing_alert:
                        # Create new alert
                        alert = RiskAlert(
                            alert_id=f"{risk_type.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                            risk_type=risk_type,
                            risk_level=metric.risk_level,
                            message=f"{risk_type.value} threshold exceeded: {metric.value:.2%} > {metric.threshold:.2%}",
                            current_value=metric.value,
                            threshold=metric.threshold,
                            timestamp=datetime.now()
                        )
                        
                        self.risk_alerts.append(alert)
                        logger.warning(f"Risk alert created: {alert.message}")
            
            # Save alerts
            self.save_risk_data()
            
        except Exception as e:
            logger.error(f"Error checking risk alerts: {e}")
    
    def acknowledge_alert(self, alert_id: str, acknowledged_by: str) -> bool:
        """Acknowledge a risk alert"""
        try:
            alert = next(
                (alert for alert in self.risk_alerts if alert.alert_id == alert_id),
                None
            )
            
            if alert:
                alert.acknowledged = True
                alert.acknowledged_by = acknowledged_by
                alert.acknowledged_at = datetime.now()
                
                self.save_risk_data()
                logger.info(f"Alert {alert_id} acknowledged by {acknowledged_by}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error acknowledging alert {alert_id}: {e}")
            return False
    
    def get_risk_profile(self) -> PortfolioRiskProfile:
        """Get comprehensive risk profile"""
        try:
            # Update metrics if needed
            self.update_risk_metrics()
            
            # Calculate VaR and ES
            var_95 = self.calculate_var(0.95)
            var_99 = self.calculate_var(0.99)
            expected_shortfall = self.calculate_expected_shortfall(0.95)
            
            # Run stress tests
            stress_test_results = self.run_stress_tests()
            
            # Calculate composite risk score
            total_risk_score = self.calculate_composite_risk_score()
            
            self.risk_profile = PortfolioRiskProfile(
                total_risk_score=total_risk_score,
                risk_metrics=self.risk_metrics,
                risk_alerts=self.risk_alerts,
                var_95=var_95,
                var_99=var_99,
                expected_shortfall=expected_shortfall,
                stress_test_results=stress_test_results
            )
            
            return self.risk_profile
            
        except Exception as e:
            logger.error(f"Error getting risk profile: {e}")
            return None
    
    def get_risk_summary(self) -> Dict[str, Any]:
        """Get risk summary for reporting"""
        try:
            profile = self.get_risk_profile()
            if not profile:
                return {}
            
            # Count alerts by level
            alert_counts = {}
            for level in RiskLevel:
                alert_counts[level.value] = len([
                    alert for alert in profile.risk_alerts 
                    if alert.risk_level == level and not alert.acknowledged
                ])
            
            return {
                "total_risk_score": profile.total_risk_score,
                "risk_level": self.get_overall_risk_level(profile.total_risk_score),
                "alert_counts": alert_counts,
                "var_95": profile.var_95,
                "var_99": profile.var_99,
                "expected_shortfall": profile.expected_shortfall,
                "critical_risks": [
                    metric.risk_type.value for metric in profile.risk_metrics.values()
                    if metric.risk_level == RiskLevel.CRITICAL
                ],
                "last_updated": profile.last_updated.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting risk summary: {e}")
            return {}
    
    def get_overall_risk_level(self, risk_score: float) -> str:
        """Get overall risk level based on composite score"""
        if risk_score <= 0.5:
            return "LOW"
        elif risk_score <= 0.7:
            return "MEDIUM"
        elif risk_score <= 0.9:
            return "HIGH"
        else:
            return "CRITICAL"
    
    def save_risk_data(self) -> None:
        """Save risk data to persistent storage"""
        try:
            # Save risk profile
            if self.risk_profile:
                profile_data = asdict(self.risk_profile)
                with open(self.risk_file, 'w') as f:
                    json.dump(profile_data, f, indent=2, default=str)
            
            # Save alerts
            alerts_data = [asdict(alert) for alert in self.risk_alerts]
            with open(self.alerts_file, 'w') as f:
                json.dump(alerts_data, f, indent=2, default=str)
            
            logger.info("Risk data saved successfully")
            
        except Exception as e:
            logger.error(f"Error saving risk data: {e}")
    
    def load_risk_data(self) -> None:
        """Load risk data from persistent storage"""
        try:
            # Load alerts
            if self.alerts_file.exists():
                with open(self.alerts_file, 'r') as f:
                    alerts_data = json.load(f)
                
                for alert_data in alerts_data:
                    if "timestamp" in alert_data:
                        alert_data["timestamp"] = datetime.fromisoformat(alert_data["timestamp"])
                    if "acknowledged_at" in alert_data and alert_data["acknowledged_at"]:
                        alert_data["acknowledged_at"] = datetime.fromisoformat(alert_data["acknowledged_at"])
                    
                    alert = RiskAlert(**alert_data)
                    self.risk_alerts.append(alert)
                
                logger.info(f"Loaded {len(self.risk_alerts)} risk alerts")
            
        except Exception as e:
            logger.error(f"Error loading risk data: {e}")
            logger.info("Starting with empty risk data")

# Example usage and testing
if __name__ == "__main__":
    # Create risk manager
    rm = RiskManager()
    
    # Update risk metrics
    rm.update_risk_metrics()
    
    # Get risk profile
    profile = rm.get_risk_profile()
    
    # Get risk summary
    summary = rm.get_risk_summary()
    print("Risk Summary:")
    print(json.dumps(summary, indent=2))
    
    # Check for alerts
    print(f"\nActive Alerts: {len([a for a in rm.risk_alerts if not a.acknowledged])}")
