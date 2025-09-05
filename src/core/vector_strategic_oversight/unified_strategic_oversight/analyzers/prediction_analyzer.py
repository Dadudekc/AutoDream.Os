#!/usr/bin/env python3
"""
Prediction Analyzer - V2 Compliance Module

Author: Agent-6 (Coordination & Communication Specialist)
Mission: V2 Compliance - Modular Architecture
Status: REFACTORED - Clean separation of concerns
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass

from ..enums import ConfidenceLevel


@dataclass
class SuccessPrediction:
    """Success prediction result."""
    prediction_id: str
    task_id: str
    success_probability: float
    confidence_level: ConfidenceLevel
    key_factors: List[str]
    risk_factors: List[str]
    recommendations: List[str]
    predicted_at: datetime


class PredictionAnalyzer:
    """Analyzes and predicts task success probabilities."""
    
    def __init__(self):
        """Initialize prediction analyzer."""
        self.prediction_history: List[Dict[str, Any]] = []
        self.historical_data: List[Dict[str, Any]] = []
    
    async def predict_task_success(
        self,
        task_data: Dict[str, Any],
        historical_data: Optional[List[Dict[str, Any]]] = None
    ) -> SuccessPrediction:
        """Predict task success probability."""
        try:
            if historical_data:
                self.historical_data = historical_data
            
            # Calculate base probability
            base_probability = self._calculate_base_probability(task_data)
            
            # Adjust based on historical data
            if self.historical_data:
                historical_success_rate = self._calculate_historical_success_rate()
                base_probability = (base_probability + historical_success_rate) / 2
            
            # Determine confidence level
            confidence_level = self._determine_confidence_level(base_probability)
            
            return SuccessPrediction(
                prediction_id=f"pred_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                task_id=task_data.get("task_id", "unknown"),
                success_probability=max(0.0, min(1.0, base_probability)),
                confidence_level=confidence_level,
                key_factors=self._identify_key_factors(task_data),
                risk_factors=self._identify_risk_factors(task_data),
                recommendations=self._generate_recommendations(task_data, base_probability),
                predicted_at=datetime.now()
            )
            
        except Exception as e:
            # Return low-confidence prediction on error
            return SuccessPrediction(
                prediction_id=f"error_pred_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                task_id=task_data.get("task_id", "unknown"),
                success_probability=0.3,
                confidence_level=ConfidenceLevel.LOW,
                key_factors=[],
                risk_factors=["prediction_error"],
                recommendations=["Manual assessment required"],
                predicted_at=datetime.now()
            )
    
    def _calculate_base_probability(self, task_data: Dict[str, Any]) -> float:
        """Calculate base success probability."""
        # Mock calculation based on task complexity
        complexity = task_data.get("complexity", "medium")
        
        if complexity == "low":
            return 0.9
        elif complexity == "medium":
            return 0.7
        elif complexity == "high":
            return 0.5
        else:
            return 0.6
    
    def _calculate_historical_success_rate(self) -> float:
        """Calculate historical success rate."""
        if not self.historical_data:
            return 0.5
        
        successful_tasks = sum(1 for task in self.historical_data if task.get("success", False))
        total_tasks = len(self.historical_data)
        
        return successful_tasks / max(1, total_tasks)
    
    def _determine_confidence_level(self, probability: float) -> ConfidenceLevel:
        """Determine confidence level based on probability."""
        if probability > 0.8:
            return ConfidenceLevel.VERY_HIGH
        elif probability > 0.6:
            return ConfidenceLevel.HIGH
        elif probability > 0.4:
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW
    
    def _identify_key_factors(self, task_data: Dict[str, Any]) -> List[str]:
        """Identify key factors for success."""
        factors = ["task_complexity", "historical_performance"]
        
        if task_data.get("priority") == "high":
            factors.append("high_priority")
        
        if task_data.get("resources_available", True):
            factors.append("adequate_resources")
        
        return factors
    
    def _identify_risk_factors(self, task_data: Dict[str, Any]) -> List[str]:
        """Identify risk factors."""
        risks = ["high_complexity", "resource_constraints"]
        
        if task_data.get("complexity") == "high":
            risks.append("high_complexity")
        
        if not task_data.get("resources_available", True):
            risks.append("insufficient_resources")
        
        return risks
    
    def _generate_recommendations(
        self, 
        task_data: Dict[str, Any], 
        probability: float
    ) -> List[str]:
        """Generate recommendations based on prediction."""
        recommendations = ["Monitor progress closely", "Prepare contingency plans"]
        
        if probability < 0.5:
            recommendations.extend([
                "Consider breaking task into smaller parts",
                "Assign additional resources",
                "Increase monitoring frequency"
            ])
        
        if task_data.get("complexity") == "high":
            recommendations.append("Ensure experienced team members are assigned")
        
        return recommendations
    
    def add_historical_data(self, data: List[Dict[str, Any]]):
        """Add historical data for better predictions."""
        self.historical_data.extend(data)
    
    def get_prediction_summary(self) -> Dict[str, Any]:
        """Get prediction summary."""
        return {
            "total_predictions": len(self.prediction_history),
            "historical_data_points": len(self.historical_data),
            "average_confidence": self._calculate_average_confidence()
        }
    
    def _calculate_average_confidence(self) -> float:
        """Calculate average confidence level."""
        if not self.prediction_history:
            return 0.0
        
        confidence_values = {
            ConfidenceLevel.VERY_HIGH: 0.9,
            ConfidenceLevel.HIGH: 0.7,
            ConfidenceLevel.MEDIUM: 0.5,
            ConfidenceLevel.LOW: 0.3
        }
        
        total_confidence = sum(
            confidence_values.get(pred.get("confidence_level", ConfidenceLevel.LOW), 0.3)
            for pred in self.prediction_history
        )
        
        return total_confidence / len(self.prediction_history)