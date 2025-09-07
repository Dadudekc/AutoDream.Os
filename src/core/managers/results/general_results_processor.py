"""
General Results Processor - Phase-2 V2 Compliance Refactoring
==============================================================

Handles general result processing for unknown types.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

from __future__ import annotations
from typing import Dict, Any
from .base_results_manager import BaseResultsManager


class GeneralResultsProcessor(BaseResultsManager):
    """Processes general results for unknown types."""

    def _process_result_by_type(
        self, context, result_type: str, result_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process general results."""
        if result_type == "general":
            return self._process_general_result(context, result_data)
        return super()._process_result_by_type(context, result_type, result_data)

    def _process_general_result(
        self, context, result_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process general result data."""
        try:
            # Basic processing for unknown result types
            processed_data = {
                "processed": True,
                "data_type": type(result_data).__name__,
                "data_size": len(str(result_data)),
                "has_nested_data": isinstance(result_data, dict) and any(
                    isinstance(v, (dict, list)) for v in result_data.values()
                ),
            }
            
            # Add basic analysis
            if isinstance(result_data, dict):
                processed_data.update(self._analyze_dict_data(result_data))
            elif isinstance(result_data, list):
                processed_data.update(self._analyze_list_data(result_data))
            else:
                processed_data["simple_value"] = True
            
            return {
                "general_success": True,
                "processed_data": processed_data,
                "original_data": result_data,
            }
            
        except Exception as e:
            context.logger(f"Error processing general result: {e}")
            return {
                "general_success": False,
                "error": str(e),
                "original_data": result_data,
            }

    def _analyze_dict_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze dictionary data."""
        return {
            "key_count": len(data),
            "key_types": list(set(type(k).__name__ for k in data.keys())),
            "value_types": list(set(type(v).__name__ for v in data.values())),
            "nested_objects": sum(1 for v in data.values() if isinstance(v, dict)),
            "nested_arrays": sum(1 for v in data.values() if isinstance(v, list)),
        }

    def _analyze_list_data(self, data: list) -> Dict[str, Any]:
        """Analyze list data."""
        return {
            "item_count": len(data),
            "item_types": list(set(type(item).__name__ for item in data)),
            "has_duplicates": len(data) != len(set(str(item) for item in data)),
            "nested_objects": sum(1 for item in data if isinstance(item, dict)),
            "nested_arrays": sum(1 for item in data if isinstance(item, list)),
        }
