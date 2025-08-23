"""
Financial Analytics Data Manager - V2 Compliant Data Persistence

This module handles data persistence, loading, and management for financial analytics.
Follows V2 standards with ≤200 LOC and single responsibility for data management.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import asdict

from .data_models import BacktestResult, PerformanceMetrics, RiskAnalysis

logger = logging.getLogger(__name__)


class DataManager:
    """Manages data persistence and loading for financial analytics"""
    
    def __init__(self, data_dir: str = "financial_analytics"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # File paths
        self.results_file = self.data_dir / "backtest_results.json"
        self.metrics_file = self.data_dir / "performance_metrics.json"
        self.risk_file = self.data_dir / "risk_analyses.json"
    
    def save_backtest_results(self, results: List[BacktestResult]) -> bool:
        """Save backtest results to file"""
        try:
            results_data = []
            for result in results:
                result_dict = asdict(result)
                # Convert datetime objects to ISO format
                if result_dict.get("start_date"):
                    result_dict["start_date"] = result.start_date.isoformat()
                if result_dict.get("end_date"):
                    result_dict["end_date"] = result.end_date.isoformat()
                if result_dict.get("timestamp"):
                    result_dict["timestamp"] = result.timestamp.isoformat()
                results_data.append(result_dict)
            
            with open(self.results_file, "w") as f:
                json.dump(results_data, f, indent=2, default=str)
            
            logger.info(f"Saved {len(results)} backtest results")
            return True
        except Exception as e:
            logger.error(f"Error saving backtest results: {e}")
            return False
    
    def load_backtest_results(self) -> List[BacktestResult]:
        """Load backtest results from file"""
        try:
            if not self.results_file.exists():
                logger.info("No backtest results file found")
                return []
            
            with open(self.results_file, "r") as f:
                results_data = json.load(f)
            
            results = []
            for result_data in results_data:
                try:
                    # Convert ISO format strings back to datetime objects
                    if "start_date" in result_data:
                        result_data["start_date"] = datetime.fromisoformat(
                            result_data["start_date"]
                        )
                    if "end_date" in result_data:
                        result_data["end_date"] = datetime.fromisoformat(
                            result_data["end_date"]
                        )
                    if "timestamp" in result_data:
                        result_data["timestamp"] = datetime.fromisoformat(
                            result_data["timestamp"]
                        )
                    
                    result = BacktestResult(**result_data)
                    results.append(result)
                except Exception as e:
                    logger.warning(f"Skipping invalid result data: {e}")
                    continue
            
            logger.info(f"Loaded {len(results)} backtest results")
            return results
        except Exception as e:
            logger.error(f"Error loading backtest results: {e}")
            return []
    
    def save_performance_metrics(self, metrics: Dict[str, PerformanceMetrics]) -> bool:
        """Save performance metrics to file"""
        try:
            metrics_data = {}
            for name, metric in metrics.items():
                try:
                    metrics_data[name] = {
                        "returns": metric.returns.tolist() if hasattr(metric.returns, 'tolist') else [],
                        "cumulative_returns": metric.cumulative_returns.tolist() if hasattr(metric.cumulative_returns, 'tolist') else [],
                        "drawdown": metric.drawdown.tolist() if hasattr(metric.drawdown, 'tolist') else [],
                        "value_at_risk": metric.value_at_risk,
                        "conditional_var": metric.conditional_var,
                        "sharpe_ratio": getattr(metric, 'sharpe_ratio', 0.0),
                        "sortino_ratio": getattr(metric, 'sortino_ratio', 0.0),
                        "calmar_ratio": getattr(metric, 'calmar_ratio', 0.0),
                        "information_ratio": getattr(metric, 'information_ratio', 0.0),
                        "treynor_ratio": getattr(metric, 'treynor_ratio', 0.0),
                        "jensen_alpha": getattr(metric, 'jensen_alpha', 0.0),
                        "tracking_error": getattr(metric, 'tracking_error', 0.0),
                        "correlation": getattr(metric, 'correlation', 0.0),
                    }
                except Exception as e:
                    logger.warning(f"Skipping invalid metric {name}: {e}")
                    continue
            
            with open(self.metrics_file, "w") as f:
                json.dump(metrics_data, f, indent=2, default=str)
            
            logger.info(f"Saved {len(metrics)} performance metrics")
            return True
        except Exception as e:
            logger.error(f"Error saving performance metrics: {e}")
            return False
    
    def load_performance_metrics(self) -> Dict[str, Dict[str, Any]]:
        """Load performance metrics from file"""
        try:
            if not self.metrics_file.exists():
                logger.info("No performance metrics file found")
                return {}
            
            with open(self.metrics_file, "r") as f:
                metrics_data = json.load(f)
            
            logger.info(f"Loaded {len(metrics_data)} performance metrics")
            return metrics_data
        except Exception as e:
            logger.error(f"Error loading performance metrics: {e}")
            return {}
    
    def save_risk_analyses(self, risk_analyses: Dict[str, RiskAnalysis]) -> bool:
        """Save risk analyses to file"""
        try:
            risk_data = {}
            for name, risk in risk_analyses.items():
                try:
                    risk_data[name] = asdict(risk)
                except Exception as e:
                    logger.warning(f"Skipping invalid risk analysis {name}: {e}")
                    continue
            
            with open(self.risk_file, "w") as f:
                json.dump(risk_data, f, indent=2, default=str)
            
            logger.info(f"Saved {len(risk_analyses)} risk analyses")
            return True
        except Exception as e:
            logger.error(f"Error saving risk analyses: {e}")
            return False
    
    def load_risk_analyses(self) -> Dict[str, Dict[str, Any]]:
        """Load risk analyses from file"""
        try:
            if not self.risk_file.exists():
                logger.info("No risk analyses file found")
                return {}
            
            with open(self.risk_file, "r") as f:
                risk_data = json.load(f)
            
            logger.info(f"Loaded {len(risk_data)} risk analyses")
            return risk_data
        except Exception as e:
            logger.error(f"Error loading risk analyses: {e}")
            return {}
    
    def save_all_data(self, results: List[BacktestResult], 
                     metrics: Dict[str, PerformanceMetrics],
                     risk_analyses: Dict[str, RiskAnalysis]) -> bool:
        """Save all financial analytics data"""
        try:
            success = True
            success &= self.save_backtest_results(results)
            success &= self.save_performance_metrics(metrics)
            success &= self.save_risk_analyses(risk_analyses)
            
            if success:
                logger.info("All financial analytics data saved successfully")
            else:
                logger.warning("Some data failed to save")
            
            return success
        except Exception as e:
            logger.error(f"Error saving all data: {e}")
            return False
    
    def load_all_data(self) -> tuple[List[BacktestResult], Dict[str, Dict[str, Any]], Dict[str, Dict[str, Any]]]:
        """Load all financial analytics data"""
        try:
            results = self.load_backtest_results()
            metrics = self.load_performance_metrics()
            risk_analyses = self.load_risk_analyses()
            
            logger.info("All financial analytics data loaded successfully")
            return results, metrics, risk_analyses
        except Exception as e:
            logger.error(f"Error loading all data: {e}")
            return [], {}, {}
    
    def clear_all_data(self) -> bool:
        """Clear all saved data files"""
        try:
            files_to_remove = [self.results_file, self.metrics_file, self.risk_file]
            for file_path in files_to_remove:
                if file_path.exists():
                    file_path.unlink()
                    logger.info(f"Removed {file_path}")
            
            logger.info("All financial analytics data cleared")
            return True
        except Exception as e:
            logger.error(f"Error clearing data: {e}")
            return False

