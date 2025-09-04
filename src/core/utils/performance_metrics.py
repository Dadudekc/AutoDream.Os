"""
Performance Metrics Utilities - V2 Compliant Performance Tracking
Focused utility for coordination and performance metrics
V2 Compliance: Under 300-line limit with focused functionality

@Author: Agent-6 - Gaming & Entertainment Specialist (Coordination & Communication V2 Compliance)
@Version: 1.0.0 - Performance Metrics Utilities
@License: MIT
"""



@dataclass
class CoordinationMetrics:
    """Standard coordination metrics structure."""
    messages_processed: int = 0
    successful_coordinations: int = 0
    average_response_time: float = 0.0
    average_execution_time: float = 0.0
    success_rate: float = 100.0
    vector_insights_used: int = 0


class PerformanceMetricsUtils:
    """
    Performance metrics utilities for coordination tracking.
    
    Provides functionality for:
    - Coordination metrics updates
    - Performance tracking
    - History management
    """

    @staticmethod
    def update_coordination_metrics(
        metrics: Dict[str, Any], 
        execution_time: float, 
        success: bool
    ) -> None:
        """
        Update coordination performance metrics.
        
        Args:
            metrics: Metrics dictionary to update
            execution_time: Execution time in seconds
            success: Whether the operation was successful
        """
        metrics["messages_processed"] = metrics.get("messages_processed", 0) + 1
        
        # Update average response time
        current_avg = metrics.get("average_response_time", 0.0)
        total_messages = metrics["messages_processed"]
        metrics["average_response_time"] = (
            (current_avg * (total_messages - 1) + execution_time) / total_messages
        )
        
        # Update success rate
        if not get_unified_validator().validate_required(success):
            current_success_rate = metrics.get("success_rate", 100.0)
            metrics["success_rate"] = (
                (current_success_rate * (total_messages - 1)) / total_messages
            )

    @staticmethod
    def update_performance_metrics(
        metrics: Dict[str, Any], 
        result: Any
    ) -> None:
        """
        Update performance metrics based on coordination result.
        
        Args:
            metrics: Metrics dictionary to update
            result: Coordination result object with status and execution_time
        """
        metrics["total_coordinations"] = metrics.get("total_coordinations", 0) + 1
        
        if get_unified_validator().validate_hasattr(result, 'status') and result.status == "coordinated":
            metrics["successful_coordinations"] = metrics.get("successful_coordinations", 0) + 1
        
        # Update average execution time
        if get_unified_validator().validate_hasattr(result, 'execution_time'):
            total_coordinations = metrics["total_coordinations"]
            current_avg = metrics.get("average_execution_time", 0.0)
            metrics["average_execution_time"] = (
                (current_avg * (total_coordinations - 1) + result.execution_time) / total_coordinations
            )

    @staticmethod
    def store_coordination_history(
        history: List[Dict[str, Any]], 
        message: Any, 
        result: Any, 
        execution_time: float
    ) -> None:
        """
        Store coordination history for pattern analysis.
        
        Args:
            history: History list to append to
            message: Message object
            result: Result object
            execution_time: Execution time in seconds
        """
        history_entry = {
            "timestamp": datetime.now().isoformat(),
            "message_id": get_unified_validator().safe_getattr(message, 'message_id', 'unknown'),
            "message_type": get_unified_validator().safe_getattr(message, 'message_type', 'unknown'),
            "recipient": get_unified_validator().safe_getattr(message, 'recipient', 'unknown'),
            "execution_time": execution_time,
            "success": True,
            "result_summary": str(result)[:100] if result else "No result"
        }
        
        history.append(history_entry)
        
        # Keep only last 100 entries
        if len(history) > 100:
            history[:] = history[-100:]

    @staticmethod
    def calculate_success_rate(
        total_operations: int, 
        successful_operations: int
    ) -> float:
        """
        Calculate success rate percentage.
        
        Args:
            total_operations: Total number of operations
            successful_operations: Number of successful operations
            
        Returns:
            Success rate as percentage (0.0 to 100.0)
        """
        if total_operations == 0:
            return 100.0
        
        return (successful_operations / total_operations) * 100.0

    @staticmethod
    def calculate_average_metric(
        current_average: float, 
        total_count: int, 
        new_value: float
    ) -> float:
        """
        Calculate rolling average for a metric.
        
        Args:
            current_average: Current average value
            total_count: Total count of values
            new_value: New value to include in average
            
        Returns:
            Updated average value
        """
        if total_count <= 1:
            return new_value
        
        return ((current_average * (total_count - 1)) + new_value) / total_count

    @staticmethod
    def get_performance_summary(metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get a summary of performance metrics.
        
        Args:
            metrics: Metrics dictionary
            
        Returns:
            Performance summary dictionary
        """
        total_coordinations = metrics.get("total_coordinations", 0)
        successful_coordinations = metrics.get("successful_coordinations", 0)
        
        success_rate = PerformanceMetricsUtils.calculate_success_rate(
            total_coordinations, successful_coordinations
        )
        
        return {
            "total_operations": total_coordinations,
            "successful_operations": successful_coordinations,
            "success_rate": success_rate,
            "average_execution_time": metrics.get("average_execution_time", 0.0),
            "average_response_time": metrics.get("average_response_time", 0.0),
            "vector_insights_used": metrics.get("vector_insights_used", 0)
        }


# Export main interface
__all__ = ["PerformanceMetricsUtils", "CoordinationMetrics"]
