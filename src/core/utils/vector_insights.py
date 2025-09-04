"""
Vector Insights Utilities - V2 Compliant Vector Database Integration
Focused utility for vector database insights and enhancements
V2 Compliance: Under 300-line limit with focused functionality

@Author: Agent-6 - Gaming & Entertainment Specialist (Coordination & Communication V2 Compliance)
@Version: 1.0.0 - Vector Insights Utilities
@License: MIT
"""



class VectorInsightsUtils:
    """
    Vector insights utilities for enhanced coordination.
    
    Provides functionality for:
    - Data enhancement with vector insights
    - Recommendation extraction
    - Pattern analysis
    """

    @staticmethod
    def enhance_data_with_vector_insights(
        data: Dict[str, Any], 
        vector_db_service: Optional[Any], 
        query: str,
        limit: int = 3
    ) -> Dict[str, Any]:
        """
        Enhance data with vector database insights.
        
        Args:
            data: Data dictionary to enhance
            vector_db_service: Vector database service instance
            query: Query string for vector search
            limit: Maximum number of insights to retrieve
            
        Returns:
            Enhanced data dictionary
        """
        enhanced_data = data.copy()
        
        if not get_unified_validator().validate_required(vector_db_service):
            return enhanced_data
            
        try:
            # Get relevant insights
            insights = vector_db_service.search_similar(query=query, limit=limit)
            
            if insights:
                enhanced_data["vector_insights"] = {
                    "relevant_patterns": [insight.get("content", "") for insight in insights],
                    "confidence_scores": [insight.get("score", 0.0) for insight in insights],
                    "recommendations": VectorInsightsUtils.extract_recommendations_from_insights(insights)
                }
                
        except Exception as e:
            get_logger(__name__).info(f"Warning: Could not enhance data with vector insights: {e}")
            
        return enhanced_data

    @staticmethod
    def extract_recommendations_from_insights(insights: List[Dict[str, Any]]) -> List[str]:
        """
        Extract recommendations from vector insights.
        
        Args:
            insights: List of insight dictionaries
            
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        for insight in insights:
            metadata = insight.get("metadata", {})
            if metadata.get("recommendation"):
                recommendations.append(metadata["recommendation"])
                
        return recommendations[:3]  # Return top 3 recommendations

    @staticmethod
    def generate_coordination_recommendations(insights: List[Dict[str, Any]]) -> List[str]:
        """
        Generate coordination recommendations from vector insights.
        
        Args:
            insights: List of insight dictionaries
            
        Returns:
            List of recommendation strings
        """
        return VectorInsightsUtils.extract_recommendations_from_insights(insights)

    @staticmethod
    def save_coordination_insights(
        vector_db_service: Optional[Any], 
        coordination_history: List[Dict[str, Any]]
    ) -> None:
        """
        Save coordination insights to vector database.
        
        Args:
            vector_db_service: Vector database service instance
            coordination_history: List of coordination history entries
        """
        if not vector_db_service or not coordination_history:
            return
            
        try:
            # Save coordination patterns for future use
            for entry in coordination_history[-10:]:  # Save last 10 entries
                vector_db_service.add_document(
                    content=f"Coordination pattern: {entry['message_type']} -> {entry['recipient']}",
                    metadata={
                        "coordination_type": entry["message_type"],
                        "recipient": entry["recipient"],
                        "execution_time": entry["execution_time"],
                        "success": entry["success"],
                        "timestamp": entry["timestamp"]
                    }
                )
                
        except Exception as e:
            get_logger(__name__).info(f"Warning: Could not save coordination insights: {e}")

    @staticmethod
    def create_enhanced_handler(original_handler: callable, metrics: Dict[str, Any]) -> callable:
        """
        Create vector-enhanced wrapper for message handler.
        
        Args:
            original_handler: Original handler function
            metrics: Metrics dictionary to update
            
        Returns:
            Enhanced handler function
        """
        def enhanced_handler(message: Any) -> Any:
            start_time = datetime.now()
            
            try:
                # Execute original handler
                result = original_handler(message)
                
                # Track performance
                execution_time = (datetime.now() - start_time).total_seconds()
                PerformanceMetricsUtils.update_coordination_metrics(metrics, execution_time, True)
                
                return result
                
            except Exception as e:
                # Track error
                execution_time = (datetime.now() - start_time).total_seconds()
                PerformanceMetricsUtils.update_coordination_metrics(metrics, execution_time, False)
                raise e
                
        return enhanced_handler

    @staticmethod
    def analyze_pattern_effectiveness(
        coordination_history: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze effectiveness of coordination patterns.
        
        Args:
            coordination_history: List of coordination history entries
            
        Returns:
            Pattern effectiveness analysis
        """
        if not get_unified_validator().validate_required(coordination_history):
            return {"message": "No coordination history available for analysis"}
        
        # Group by message type
        pattern_stats = {}
        for entry in coordination_history:
            message_type = entry.get("message_type", "unknown")
            
            if message_type not in pattern_stats:
                pattern_stats[message_type] = {
                    "total_count": 0,
                    "success_count": 0,
                    "total_execution_time": 0.0,
                    "average_execution_time": 0.0
                }
            
            stats = pattern_stats[message_type]
            stats["total_count"] += 1
            stats["total_execution_time"] += entry.get("execution_time", 0.0)
            
            if entry.get("success", False):
                stats["success_count"] += 1
        
        # Calculate effectiveness metrics
        for message_type, stats in pattern_stats.items():
            stats["success_rate"] = (stats["success_count"] / stats["total_count"]) * 100
            stats["average_execution_time"] = stats["total_execution_time"] / stats["total_count"]
        
        return {
            "pattern_analysis": pattern_stats,
            "total_patterns": len(pattern_stats),
            "analysis_timestamp": datetime.now().isoformat()
        }

    @staticmethod
    def get_vector_insights_summary(
        vector_db_service: Optional[Any], 
        query: str, 
        limit: int = 5
    ) -> Dict[str, Any]:
        """
        Get a summary of vector insights for a query.
        
        Args:
            vector_db_service: Vector database service instance
            query: Query string for vector search
            limit: Maximum number of insights to retrieve
            
        Returns:
            Vector insights summary
        """
        if not get_unified_validator().validate_required(vector_db_service):
            return {"message": "Vector database service not available"}
        
        try:
            insights = vector_db_service.search_similar(query=query, limit=limit)
            
            if not get_unified_validator().validate_required(insights):
                return {"message": f"No insights found for query: {query}"}
            
            return {
                "query": query,
                "total_insights": len(insights),
                "insights": [
                    {
                        "content": insight.get("content", "")[:100] + "...",
                        "score": insight.get("score", 0.0),
                        "metadata": insight.get("metadata", {})
                    }
                    for insight in insights
                ],
                "recommendations": VectorInsightsUtils.extract_recommendations_from_insights(insights),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": f"Failed to get vector insights: {str(e)}"}


# Export main interface
__all__ = ["VectorInsightsUtils"]
